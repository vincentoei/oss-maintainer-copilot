"""One separately capped hosted quality reference for a frozen local comparison."""

import argparse
import fcntl
import hashlib
import json
import os
from collections.abc import Collection
from dataclasses import asdict
from datetime import UTC, datetime
from decimal import ROUND_CEILING, Decimal
from pathlib import Path
from time import perf_counter
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from maintainer_copilot import issue_search, model, source
from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.local_evaluation import _LiveEvidenceCache
from maintainer_copilot.replay import (
    CaseFlagged,
    CommitSource,
    HistoricalCase,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import (
    ROOT,
    _EvidenceSnapshot,
    _save,
    fingerprint,
)

MODEL = "gpt-4.1-2025-04-14"
CAP_MICRO_USD = 4_999_999
INPUT_MICRO_USD = 2
OUTPUT_MICRO_USD = 8
BASELINE = ROOT / "docs/evaluation/issue-19/post-quality/run/results.json"
PROVIDERS = {
    "openai": ("https://api.openai.com/v1", MODEL, "OPENAI_API_KEY"),
    "openrouter": (
        "https://openrouter.ai/api/v1",
        "openai/gpt-4.1",
        "OPENROUTER_API_KEY",
    ),
}


def _provider_identity(provider: str) -> dict[str, Any]:
    if provider == "openai":
        return {"model": MODEL, "provider": "OpenAI"}
    if provider != "openrouter":
        raise ValueError("Unsupported hosted provider")
    request = Request(
        "https://openrouter.ai/api/v1/models/openai/gpt-4.1/endpoints",
        headers={"User-Agent": "oss-maintainer-copilot"},
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read(65_537)
    if len(raw) > 65_536:
        raise ValueError("OpenRouter endpoint metadata exceeds limit")
    endpoints = json.loads(raw)["data"]["endpoints"]
    endpoint = next((e for e in endpoints if e["tag"] == "openai"), None)
    if endpoint is None or f"openai/{MODEL}" not in endpoint["name"]:
        raise ValueError("OpenRouter dated model identity unavailable")
    for name, maximum in (("prompt", "0.000002"), ("completion", "0.000008")):
        price = Decimal(endpoint["pricing"][name])
        if not price.is_finite() or not 0 <= price <= Decimal(maximum):
            raise ValueError("OpenRouter pricing exceeds frozen reservation rates")
    return {"endpoint": endpoint, "metadata_sha256": hashlib.sha256(raw).hexdigest()}


class HostedBudget:
    """Durable, nonrefundable worst-case reservations; failures stay charged."""

    def __init__(self, directory: Path, *, provider: str = "openai") -> None:
        self.path = directory / "hosted-requests.jsonl"
        self.provider = provider

    def records(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text().splitlines()]

    def _append(self, record: dict[str, Any]) -> None:
        with self.path.open("a") as handle:
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def reserve(self, body: bytes, issue_number: int) -> dict[str, Any]:
        # Byte-level BPE cannot use more tokens than bytes of visible input.
        # Reserve the ENTIRE serialized request plus 4096 tokens for framing
        # and schema expansion. This is deliberately much larger than billing
        # usage. Never refund it, even after successful calls or process death.
        input_bound = len(body) + 4096
        reserved = input_bound * INPUT_MICRO_USD + 256 * OUTPUT_MICRO_USD
        with self.path.open("a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            records = [json.loads(line) for line in handle]
            charges = [r for r in records if r["event"] == "reserved"]
            if any(r["provider"] != self.provider for r in charges):
                raise model.ModelUnavailable("Frozen hosted provider changed")
            finished = {r["request"] for r in records if r["event"] == "response"}
            if any(r["event"] == "halted" for r in records) or any(
                r["request"] not in finished for r in charges
            ):
                raise model.ModelUnavailable("Hosted accounting halted; no more calls")
            if (
                sum(r["reserved_micro_usd"] for r in charges) + reserved > CAP_MICRO_USD
                or len(charges) >= 50
                or any(r["issue_number"] == issue_number for r in charges)
            ):
                raise model.ModelUnavailable("Separate hosted budget exhausted")
            record = {
                "event": "reserved",
                "request": len(charges) + 1,
                "issue_number": issue_number,
                "model": MODEL,
                "provider": self.provider,
                "input_token_bound": input_bound,
                "max_output_tokens": 256,
                "reserved_micro_usd": reserved,
                "payload_sha256": hashlib.sha256(body).hexdigest(),
                "recorded_at": datetime.now(UTC).isoformat(),
            }
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record

    def finish(self, record: dict[str, Any]) -> None:
        self._append({**record, "event": "response"})
        if record.get("accounting_error"):
            self._append({"event": "halted", "request": record["request"]})

    def summary(self) -> dict[str, Any]:
        records = self.records()
        charges = [r for r in records if r["event"] == "reserved"]
        responses = [r for r in records if r["event"] == "response"]
        known = [r for r in responses if r.get("cost_micro_usd") is not None]
        complete = len(known) == len(charges)
        reported = [r.get("reported_cost_micro_usd") for r in responses]
        return {
            "cap_micro_usd": CAP_MICRO_USD,
            "request_count": len(charges),
            "reserved_micro_usd": sum(r["reserved_micro_usd"] for r in charges),
            "known_cost_micro_usd": sum(r["cost_micro_usd"] for r in known),
            "cost_micro_usd": sum(r["cost_micro_usd"] for r in known)
            if complete
            else None,
            "input_tokens": sum(r["input_tokens"] for r in known) if complete else None,
            "output_tokens": sum(r["output_tokens"] for r in known)
            if complete
            else None,
            "unknown_usage_requests": len(charges) - len(known),
            "halted": any(r["event"] == "halted" for r in records),
            "reported_cost_micro_usd": sum(reported)
            if len(reported) == len(charges) and all(v is not None for v in reported)
            else None,
        }


class HostedModel(model.OpenAICompatibleModel):
    """Use the existing selection prompt with one authenticated, capped POST."""

    def __init__(
        self,
        api_key: str,
        budget: HostedBudget,
        issue_number: int,
        *,
        provider: str = "openai",
    ) -> None:
        if not api_key.strip():
            raise ValueError("A hosted API key is required")
        base_url, request_model, _ = PROVIDERS[provider]
        super().__init__(base_url, request_model)
        if budget.provider != provider:
            raise ValueError("Hosted client and budget provider differ")
        self.provider = provider
        self.api_key = api_key
        self.budget = budget
        self.issue_number = issue_number
        self.calls: list[dict[str, Any]] = []

    def generate_json(
        self,
        system_prompt: str,
        user_data: object,
        *,
        max_tokens: int,
        response_schema: dict[str, object] | None = None,
    ) -> object:
        if max_tokens != 256 or response_schema is None:
            raise model.ModelUnavailable(
                "Hosted reference requires selection-only JSON"
            )
        # OpenAI strict structured output requires additionalProperties=false.
        schema = {**response_schema, "additionalProperties": False}
        raw_properties = schema.get("properties")
        if not isinstance(raw_properties, dict):
            raise model.ModelUnavailable("Hosted selection schema has no properties")
        properties = dict(raw_properties)
        if "type_evidence_index" in properties:
            properties["type_evidence_index"] = {
                **properties["type_evidence_index"],
                "type": ["integer", "null"],
            }
        schema["properties"] = properties
        body = json.dumps(
            {
                "model": self.model_name,
                "temperature": 0,
                "max_tokens": max_tokens,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "triage_selection",
                        "strict": True,
                        "schema": schema,
                    },
                },
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_data)},
                ],
                **(
                    {
                        "provider": {
                            "only": ["openai"],
                            "allow_fallbacks": False,
                            "require_parameters": True,
                            "max_price": {"prompt": 2, "completion": 8},
                        },
                        "transforms": [],
                    }
                    if self.provider == "openrouter"
                    else {}
                ),
            }
        ).encode()
        record = self.budget.reserve(body, self.issue_number)
        record["accounting_error"] = "InterruptedRequest"
        started = perf_counter()
        try:
            request = Request(
                f"{self.base_url}/chat/completions",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                method="POST",
            )
            with urlopen(request, timeout=60) as response:
                raw = response.read(65_537)
            if len(raw) > 65_536:
                raise ValueError("Hosted response exceeds size limit")
            envelope = json.loads(raw)
            usage = envelope["usage"]
            input_tokens = usage["prompt_tokens"]
            output_tokens = usage["completion_tokens"]
            if (
                type(input_tokens) is not int
                or type(output_tokens) is not int
                or not 0 <= input_tokens <= record["input_token_bound"]
                or not 0 <= output_tokens <= max_tokens
            ):
                raise ValueError("Hosted usage is outside reserved bounds")
            record.update(
                returned_model=envelope["model"],
                returned_provider=envelope.get("provider"),
                provider_request_id=envelope.get("id"),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_micro_usd=input_tokens * INPUT_MICRO_USD
                + output_tokens * OUTPUT_MICRO_USD,
                response_sha256=hashlib.sha256(raw).hexdigest(),
            )
            if self.provider == "openrouter":
                reported_cost = Decimal(str(usage["cost"]))
                if not reported_cost.is_finite() or reported_cost < 0:
                    raise ValueError("OpenRouter reported an invalid cost")
                record["reported_cost_micro_usd"] = int(
                    (reported_cost * 1_000_000).to_integral_value(
                        rounding=ROUND_CEILING
                    )
                )
                if record["reported_cost_micro_usd"] > record["reserved_micro_usd"]:
                    raise ValueError("OpenRouter cost exceeds reserved bound")
                if envelope.get("provider") != "OpenAI":
                    raise ValueError("OpenRouter returned an unrequested provider")
            if envelope["model"] != self.model_name:
                raise ValueError("Hosted model snapshot differs from frozen reference")
            del record["accounting_error"]
            try:
                output = json.loads(envelope["choices"][0]["message"]["content"])
            except (KeyError, IndexError, TypeError, ValueError):
                record["output_error"] = "Hosted selection unavailable or malformed"
                return model.ModelResponse(
                    None, input_tokens, output_tokens, record["output_error"]
                )
            return model.ModelResponse(output, input_tokens, output_tokens)
        except Exception as exc:
            record["accounting_error"] = type(exc).__name__
            if isinstance(exc, HTTPError):
                record["provider_http_status"] = exc.code
            raise model.ModelUnavailable(
                "Hosted request failed; accounting halted"
            ) from exc
        finally:
            record["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            self.budget.finish(record)
            self.calls.append(record)


def evaluate_hosted_reference(
    directory: Path,
    api_key: str,
    *,
    cases: Collection[HistoricalCase],
    baseline_path: Path,
    commit_source: CommitSource,
    issue_source: issue_search.IssueSource,
    source_reader: source.SourceReader,
    preflight_only: bool = False,
    provider: str = "openai",
) -> dict[str, Any]:
    """Keep baseline eligibility, candidates and cutoffs; flag drift before paying."""
    if not preflight_only and not api_key.strip():
        raise ValueError("OPENAI_API_KEY is required; no controlled fallback")
    catalog = sorted(cases, key=lambda c: c.issue_number)
    baseline = json.loads(baseline_path.read_text())
    if (
        baseline["status"] != "complete"
        or fingerprint([c.model_dump(mode="json") for c in catalog])
        != baseline["catalog_sha256"]
        or any(c.human_review.status != "confirmed" for c in catalog)
    ):
        raise ValueError("Confirmed catalog must match frozen local comparison")
    local_rows = [r for r in baseline["cases"] if r["method"] == "fixed_rag"]
    if sorted(r["issue_number"] for r in local_rows) != [
        c.issue_number for c in catalog
    ]:
        raise ValueError("Local comparison requires exactly one fixed row per case")
    local = {r["issue_number"]: r for r in local_rows}
    for case in catalog:
        row = local[case.issue_number]
        if any(
            row[key] != value
            for key, value in {
                "opening_cutoff": case.opening_cutoff.isoformat(),
                "repository_commit": case.repository_commit,
                "opening_content_sha256": case.opening_content_sha256,
                "candidate_numbers": [
                    r.number for r in candidate_references(case, catalog)
                ],
            }.items()
        ):
            raise ValueError("Local case metadata or candidate pool changed")
    if directory.exists():
        raise FileExistsError("Run directory already exists; resume/overwrite refused")
    provider_identity = _provider_identity(provider)
    directory.mkdir(parents=True, exist_ok=False)
    budget = HostedBudget(directory, provider=provider)
    evidence = _EvidenceSnapshot(commit_source, issue_source, source_reader)
    artifact: dict[str, Any] = {
        "status": "preflight",
        "recorded_at": datetime.now(UTC).isoformat(),
        "method": "hosted_quality_reference",
        "model_version": MODEL,
        "provider": provider,
        "provider_identity": provider_identity,
        "requested_model": PROVIDERS[provider][1],
        "snapshot_verification": "Exact response model required"
        if provider == "openai"
        else "OpenRouter alias with pinned OpenAI provider; upstream dated snapshot "
        "is not independently attested by the completion response",
        "baseline_sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        "catalog_sha256": baseline["catalog_sha256"],
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / "src/maintainer_copilot").glob("*.py"))
        },
        "pricing": {
            "input_micro_usd_per_token": INPUT_MICRO_USD,
            "output_micro_usd_per_token": OUTPUT_MICRO_USD,
            "source": "https://developers.openai.com/api/docs/models/gpt-4.1",
            "scope": "Standard token rates; cached input charged at full rate. "
            "Excludes taxes, hardware, network and unrelated account activity.",
            "cost_basis": "Conservative token-price estimate, not a provider invoice",
        },
        "generation": {"temperature": 0, "max_tokens": 256, "timeout_seconds": 60},
        "attribution": {
            "hosted_output": "Model prediction, never an expected triage outcome",
            "expected_outcome": "Confirmed case annotation; reviewer recorded per case",
            "report_semantics_and_usefulness": "pending_human_review",
        },
        "preflight": [],
        "cases": [],
    }
    output = directory / "results.json"
    _save(output, artifact)
    for case in catalog:
        error = None
        try:
            preflight_report = replay_case(
                case,
                commit_source=evidence,
                issue_source=evidence,
                source_reader=evidence,
                candidate_catalog=catalog,
                keyword_filter=True,
            )
            trace = get_trace(preflight_report.trace_id)
            if trace is None or any(
                e.name in ("get_documentation_passage", "get_source_excerpt")
                and e.status != "ok"
                for e in trace.events
            ):
                raise CaseFlagged("Historical repository evidence unavailable")
        except (CaseFlagged, ValueError) as exc:
            error = str(exc)
        baseline_error = local[case.issue_number]["error"]
        artifact["preflight"].append(
            {
                "issue_number": case.issue_number,
                "error": error,
                "local_error": baseline_error,
                "eligible": error is None and baseline_error is None,
            }
        )
        _save(output, artifact)
    evidence.frozen = True
    artifact["evidence_sha256"] = evidence.manifest()
    artifact["accounting"] = budget.summary()
    if preflight_only:
        artifact["status"] = "preflight_only"
        _save(output, artifact)
        return artifact
    artifact["status"] = "running"
    results: list[CaseResult] = []
    for case, preflight in zip(catalog, artifact["preflight"], strict=True):
        client = HostedModel(api_key, budget, case.issue_number, provider=provider)
        report = None
        scores = None
        error = preflight["error"] or preflight["local_error"]
        numbers = local[case.issue_number]["candidate_numbers"]
        started = perf_counter()
        if preflight["eligible"]:
            try:
                report = replay_case(
                    case,
                    model_client=client,
                    commit_source=evidence,
                    issue_source=evidence,
                    source_reader=evidence,
                    candidate_catalog=catalog,
                    keyword_filter=True,
                )
                if not client.calls:
                    error = "Hosted dispatch refused by separate budget"
                else:
                    error = client.calls[-1].get("accounting_error") or client.calls[
                        -1
                    ].get("output_error")
                    report_trace = get_trace(report.trace_id)
                    if report_trace is None or any(
                        e.kind == "model" and e.status != "ok"
                        for e in report_trace.events
                    ):
                        error = error or "Hosted selection failed report validation"
                    if error is None:
                        scores = score_report(case, report, numbers)
            except (CaseFlagged, ValueError) as exc:
                error = str(exc)
        result = CaseResult(
            case.issue_number,
            "hosted_quality_reference",
            case.opening_cutoff.isoformat(),
            case.repository_commit,
            round((perf_counter() - started) * 1000, 3),
            len(numbers),
            error,
            scores,
        )
        results.append(result)
        report_trace = get_trace(report.trace_id) if report else None
        artifact["cases"].append(
            {
                **asdict(result),
                "candidate_numbers": numbers,
                "opening_content_sha256": case.opening_content_sha256,
                "hosted_report": report.model_dump(mode="json") if report else None,
                "expected_outcome": case.expected_outcome.model_dump(mode="json"),
                "case_review": case.human_review.model_dump(mode="json"),
                "local_fixed_scores": local[case.issue_number]["scores"],
                "model_calls": client.calls,
                "trace": report_trace.model_dump(mode="json") if report_trace else None,
            }
        )
        artifact["accounting"] = budget.summary()
        _save(output, artifact)
    artifact["status"] = (
        "complete" if all(r.error is None for r in results) else "incomplete"
    )
    artifact["aggregate"] = aggregate(results)
    artifact["local_fixed_full_catalog_aggregate"] = (
        baseline.get("summary", {}).get("methods", {}).get("fixed_rag")
    )
    paired = [
        r for r in results if r.scores is not None and local[r.issue_number]["scores"]
    ]
    artifact["paired_scoreable_cases"] = len(paired)
    artifact["hosted_paired_aggregate"] = aggregate(paired)
    artifact["local_fixed_aggregate"] = aggregate(
        [
            CaseResult(
                r.issue_number,
                "local_fixed_rag",
                r.opening_cutoff,
                r.repository_commit,
                local[r.issue_number].get("latency_ms", 0),
                r.candidate_pool_size,
                None,
                local[r.issue_number]["scores"],
            )
            for r in paired
        ]
    )
    paired_numbers = {r.issue_number for r in paired}
    artifact["excluded_from_pairing"] = [
        {"issue_number": r.issue_number, "reason": r.error or "Local score unavailable"}
        for r in results
        if r.issue_number not in paired_numbers
    ]
    artifact["accounting"] = budget.summary()
    _save(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--provider", choices=tuple(PROVIDERS), default="openai")
    args = parser.parse_args()
    key_name = PROVIDERS[args.provider][2]
    key = os.getenv(key_name, "")
    if not args.preflight_only and not key.strip():
        parser.error(f"{key_name} is required; no hosted requests made")
    evidence = _LiveEvidenceCache()
    evaluate_hosted_reference(
        args.directory,
        key,
        cases=load_cases(),
        baseline_path=BASELINE,
        commit_source=evidence,
        issue_source=evidence,
        source_reader=evidence,
        preflight_only=args.preflight_only,
        provider=args.provider,
    )


if __name__ == "__main__":
    main()
