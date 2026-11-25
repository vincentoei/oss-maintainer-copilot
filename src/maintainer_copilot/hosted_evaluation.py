"""One separately capped hosted quality reference for a frozen local comparison."""

import argparse
import fcntl
import hashlib
import json
import os
from collections.abc import Collection
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any
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


class HostedBudget:
    """Durable, nonrefundable worst-case reservations; failures stay charged."""

    def __init__(self, directory: Path) -> None:
        self.path = directory / "hosted-requests.jsonl"

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
        }


class HostedModel(model.OpenAICompatibleModel):
    """Use the existing selection prompt with one authenticated, capped POST."""

    def __init__(self, api_key: str, budget: HostedBudget, issue_number: int) -> None:
        if not api_key.strip():
            raise ValueError("OPENAI_API_KEY is required")
        super().__init__("https://api.openai.com/v1", MODEL)
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
                "model": MODEL,
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
            }
        ).encode()
        record = self.budget.reserve(body, self.issue_number)
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
                provider_request_id=envelope.get("id"),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_micro_usd=input_tokens * INPUT_MICRO_USD
                + output_tokens * OUTPUT_MICRO_USD,
                response_sha256=hashlib.sha256(raw).hexdigest(),
            )
            if envelope["model"] != MODEL:
                raise ValueError("Hosted model snapshot differs from frozen reference")
            try:
                output = json.loads(envelope["choices"][0]["message"]["content"])
            except (KeyError, IndexError, TypeError, ValueError):
                record["output_error"] = "Hosted selection unavailable or malformed"
                return model.ModelResponse(
                    None, input_tokens, output_tokens, record["output_error"]
                )
            record["output"] = output
            return model.ModelResponse(output, input_tokens, output_tokens)
        except Exception as exc:
            record["accounting_error"] = type(exc).__name__
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
    directory.mkdir(parents=True, exist_ok=False)
    budget = HostedBudget(directory)
    evidence = _EvidenceSnapshot(commit_source, issue_source, source_reader)
    artifact: dict[str, Any] = {
        "status": "preflight",
        "recorded_at": datetime.now(UTC).isoformat(),
        "method": "hosted_quality_reference",
        "model_version": MODEL,
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
        client = HostedModel(api_key, budget, case.issue_number)
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
                    scores = score_report(case, report, numbers)
                    error = client.calls[-1].get("accounting_error") or client.calls[
                        -1
                    ].get("output_error")
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
    artifact["local_fixed_aggregate"] = (
        baseline.get("summary", {}).get("methods", {}).get("fixed_rag")
    )
    artifact["paired_scoreable_cases"] = sum(
        row["scores"] is not None and row["local_fixed_scores"] is not None
        for row in artifact["cases"]
    )
    artifact["accounting"] = budget.summary()
    _save(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    key = os.getenv("OPENAI_API_KEY", "")
    if not args.preflight_only and not key.strip():
        parser.error("OPENAI_API_KEY is required; no hosted requests made")
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
    )


if __name__ == "__main__":
    main()
