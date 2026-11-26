"""User-selected Flash references, sharing the original issue #20 spending cap."""

import argparse
import fcntl
import hashlib
import json
import os
from collections.abc import Collection
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import ROUND_CEILING, Decimal
from pathlib import Path
from time import perf_counter
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from maintainer_copilot import issue_search, model, source
from maintainer_copilot.evaluation import CaseResult, aggregate
from maintainer_copilot.hosted_evaluation import BASELINE, CAP_MICRO_USD, HostedBudget
from maintainer_copilot.local_evaluation import _LiveEvidenceCache, evaluate_local_model
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

MAX_COMPLETION_TOKENS = 4096
PRIOR_RUN = ROOT / "docs/evaluation/issue-20/run"


@dataclass(frozen=True)
class FlashProfile:
    model_id: str
    version: str
    provider_slug: str
    provider_name: str
    input_nano_usd: int
    output_nano_usd: int


FLASH_MODELS = {
    "deepseek": FlashProfile(
        "deepseek/deepseek-v4.1-flash",
        "deepseek-v4.1-flash-20260910",
        "deepinfra/fp8",
        "DeepInfra",
        140,
        420,
    ),
    "glm": FlashProfile(
        "z-ai/glm-5.3-flash",
        "glm-5.3-flash-20260826",
        "z-ai/fp8",
        "Z.AI",
        150,
        500,
    ),
}


class FlashBudget(HostedBudget):
    """One ledger for both models, including all prior GPT-4.1 reservations."""

    def __init__(self, directory: Path, *, prior_reserved_micro_usd: int) -> None:
        super().__init__(directory, provider="openrouter")
        if not 0 <= prior_reserved_micro_usd <= CAP_MICRO_USD:
            raise ValueError("Prior hosted reservations are outside the original cap")
        self.prior_reserved = prior_reserved_micro_usd

    def reserve_flash(
        self, body: bytes, number: int, profile: FlashProfile
    ) -> dict[str, Any]:
        input_bound = len(body) + 4096
        reserved = (
            input_bound * profile.input_nano_usd
            + MAX_COMPLETION_TOKENS * profile.output_nano_usd
            + 999
        ) // 1000
        with self.path.open("a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            records = [json.loads(line) for line in handle]
            charges = [r for r in records if r["event"] == "reserved"]
            if any(
                r["prior_reserved_micro_usd"] != self.prior_reserved for r in charges
            ):
                raise model.ModelUnavailable("Frozen prior hosted accounting changed")
            finished = {r["request"] for r in records if r["event"] == "response"}
            if any(
                r.get("accounting_error") or r["event"] == "halted" for r in records
            ) or any(r["request"] not in finished for r in charges):
                raise model.ModelUnavailable("Shared hosted accounting halted")
            same_model = [r for r in charges if r["model"] == profile.model_id]
            if (
                self.prior_reserved
                + sum(r["reserved_micro_usd"] for r in charges)
                + reserved
                > CAP_MICRO_USD
                or len(charges) >= 100
                or len(same_model) >= 50
                or any(r["issue_number"] == number for r in same_model)
            ):
                raise model.ModelUnavailable("Shared hosted budget exhausted")
            record = {
                "event": "reserved",
                "request": len(charges) + 1,
                "issue_number": number,
                "model": profile.model_id,
                "version": profile.version,
                "provider": profile.provider_slug,
                "input_nano_usd": profile.input_nano_usd,
                "output_nano_usd": profile.output_nano_usd,
                "prior_reserved_micro_usd": self.prior_reserved,
                "input_token_bound": input_bound,
                "max_output_tokens": MAX_COMPLETION_TOKENS,
                "reserved_micro_usd": reserved,
                "payload_sha256": hashlib.sha256(body).hexdigest(),
                "recorded_at": datetime.now(UTC).isoformat(),
            }
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record

    def summary(self) -> dict[str, Any]:
        summary = super().summary()
        return {
            **summary,
            "prior_reserved_micro_usd": self.prior_reserved,
            "combined_reserved_micro_usd": self.prior_reserved
            + summary["reserved_micro_usd"],
        }


class FlashModel(model.OpenAICompatibleModel):
    """Keep the legacy selection prompt; bound and price reasoning explicitly."""

    def __init__(
        self, key: str, profile: FlashProfile, budget: FlashBudget, number: int
    ) -> None:
        if not key.strip():
            raise ValueError("OPENROUTER_API_KEY is required")
        super().__init__("https://openrouter.ai/api/v1", profile.model_id)
        self.key, self.profile, self.budget, self.number = key, profile, budget, number
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
                "Flash reference requires the selection contract"
            )
        schema = {**response_schema, "additionalProperties": False}
        raw_properties = schema.get("properties")
        if not isinstance(raw_properties, dict):
            raise model.ModelUnavailable("Selection schema properties unavailable")
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
                "max_tokens": MAX_COMPLETION_TOKENS,
                "reasoning": {"effort": "low"},
                "transforms": [],
                "provider": {
                    "only": [self.profile.provider_slug],
                    "allow_fallbacks": False,
                    "require_parameters": True,
                    "max_price": {
                        "prompt": self.profile.input_nano_usd / 1000,
                        "completion": self.profile.output_nano_usd / 1000,
                    },
                },
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
        record = self.budget.reserve_flash(body, self.number, self.profile)
        record["accounting_error"] = "InterruptedRequest"
        started = perf_counter()
        try:
            request = Request(
                self.base_url + "/chat/completions",
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.key}",
                },
            )
            with urlopen(request, timeout=120) as response:
                raw = response.read(65_537)
            if len(raw) > 65_536:
                raise ValueError("Response exceeds bounded transport limit")
            envelope = json.loads(raw, parse_float=Decimal)
            usage = envelope["usage"]
            input_tokens, output_tokens = (
                usage["prompt_tokens"],
                usage["completion_tokens"],
            )
            if (
                type(input_tokens) is not int
                or type(output_tokens) is not int
                or not 0 <= input_tokens <= record["input_token_bound"]
                or not 0 <= output_tokens <= MAX_COMPLETION_TOKENS
            ):
                raise ValueError("Usage exceeds reserved bounds")
            cost = Decimal(str(usage["cost"]))
            if not cost.is_finite() or cost < 0:
                raise ValueError("Invalid reported cost")
            reported = int((cost * 1_000_000).to_integral_value(rounding=ROUND_CEILING))
            reasoning = usage.get("completion_tokens_details", {}).get(
                "reasoning_tokens"
            )
            if reasoning is not None and (
                type(reasoning) is not int or not 0 <= reasoning <= output_tokens
            ):
                raise ValueError("Invalid reasoning-token use")
            record.update(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                reasoning_tokens=reasoning,
                reported_cost_usd=str(cost),
                reported_cost_micro_usd=reported,
                cost_micro_usd=(
                    input_tokens * self.profile.input_nano_usd
                    + output_tokens * self.profile.output_nano_usd
                    + 999
                )
                // 1000,
                returned_model=envelope["model"],
                returned_provider=envelope.get("provider"),
                provider_request_id=envelope.get("id"),
                response_sha256=hashlib.sha256(raw).hexdigest(),
            )
            if (
                reported > record["reserved_micro_usd"]
                or envelope["model"] != self.model_name
                or envelope.get("provider") != self.profile.provider_name
            ):
                raise ValueError("Cost or provider identity differs from frozen bounds")
            del record["accounting_error"]
            choice = envelope["choices"][0]
            record["finish_reason"] = choice.get("finish_reason")
            try:
                if choice.get("finish_reason") != "stop":
                    raise ValueError("Completion did not finish normally")
                output = json.loads(choice["message"]["content"])
            except (KeyError, IndexError, ValueError, TypeError):
                record["output_error"] = "Selection unavailable or completion truncated"
                return model.ModelResponse(
                    None, input_tokens, output_tokens, record["output_error"]
                )
            return model.ModelResponse(output, input_tokens, output_tokens)
        except Exception as exc:
            record["accounting_error"] = type(exc).__name__
            if isinstance(exc, HTTPError):
                record["provider_http_status"] = exc.code
            raise model.ModelUnavailable(
                "Flash request failed; shared accounting halted"
            ) from exc
        finally:
            record["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            self.budget.finish(record)
            self.calls.append(record)


def endpoint_identity(profile: FlashProfile) -> dict[str, Any]:
    request = Request(
        "https://openrouter.ai/api/v1/models/" + profile.model_id + "/endpoints",
        headers={"User-Agent": "oss-maintainer-copilot"},
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read(262_145)
    if len(raw) > 262_144:
        raise ValueError("Endpoint metadata exceeds size limit")
    data = json.loads(raw)["data"]
    endpoint = next(
        (e for e in data["endpoints"] if e["tag"] == profile.provider_slug), None
    )
    if (
        data["id"] != profile.model_id
        or endpoint is None
        or profile.version not in endpoint["name"]
        or endpoint["provider_name"] != profile.provider_name
    ):
        raise ValueError("Requested Flash version or provider unavailable")
    required = {
        "reasoning",
        "response_format",
        "structured_outputs",
        "max_tokens",
        "temperature",
    }
    if not required.issubset(endpoint["supported_parameters"]):
        raise ValueError("Pinned provider cannot honor the frozen parameters")
    for field, rate in (
        ("prompt", profile.input_nano_usd),
        ("completion", profile.output_nano_usd),
    ):
        price = Decimal(endpoint["pricing"][field])
        if not price.is_finite() or not 0 <= price * 1_000_000_000 <= rate:
            raise ValueError("Pinned provider price exceeds frozen rates")
    return {"endpoint": endpoint, "metadata_sha256": hashlib.sha256(raw).hexdigest()}


def evaluate_flash_reference(
    directory: Path,
    key: str,
    *,
    cases: Collection[HistoricalCase],
    baseline_path: Path,
    prior_run: Path,
    commit_source: CommitSource,
    issue_source: issue_search.IssueSource,
    source_reader: source.SourceReader,
) -> dict[str, Any]:
    """Freeze one common evidence view and retain every row for both selected models."""
    if not key.strip():
        raise ValueError("OPENROUTER_API_KEY is required")
    if directory.exists():
        raise FileExistsError("Existing experiment refused; no resume or overwrite")
    catalog = sorted(cases, key=lambda c: c.issue_number)
    baseline = json.loads(baseline_path.read_text())
    prior = json.loads((prior_run / "results.json").read_text())
    ledger = [
        json.loads(line)
        for line in (prior_run / "hosted-requests.jsonl").read_text().splitlines()
    ]
    prior_reserved = sum(
        r["reserved_micro_usd"] for r in ledger if r["event"] == "reserved"
    )
    if (
        baseline["status"] != "complete"
        or prior["status"] != "complete"
        or prior_reserved != prior["accounting"]["reserved_micro_usd"]
        or fingerprint([c.model_dump(mode="json") for c in catalog])
        != baseline["catalog_sha256"]
        or baseline["catalog_sha256"] != prior["catalog_sha256"]
        or any(c.human_review.status != "confirmed" for c in catalog)
    ):
        raise ValueError("Frozen catalog or prior hosted accounting changed")
    local = {
        r["issue_number"]: r for r in baseline["cases"] if r["method"] == "fixed_rag"
    }
    previous = {r["issue_number"]: r for r in prior["cases"]}
    if sorted(local) != [c.issue_number for c in catalog] or sorted(previous) != sorted(
        local
    ):
        raise ValueError("Reference case IDs differ")
    for case in catalog:
        for row in (local[case.issue_number], previous[case.issue_number]):
            for field, value in {
                "opening_cutoff": case.opening_cutoff.isoformat(),
                "repository_commit": case.repository_commit,
                "opening_content_sha256": case.opening_content_sha256,
                "candidate_numbers": [
                    r.number for r in candidate_references(case, catalog)
                ],
            }.items():
                if row[field] != value:
                    raise ValueError("Reference cutoff, opening or candidates changed")
    identities = {
        name: endpoint_identity(profile) for name, profile in FLASH_MODELS.items()
    }
    directory.mkdir(parents=True)
    budget = FlashBudget(directory, prior_reserved_micro_usd=prior_reserved)
    evidence = _EvidenceSnapshot(commit_source, issue_source, source_reader)
    artifact: dict[str, Any] = {
        "status": "preflight",
        "recorded_at": datetime.now(UTC).isoformat(),
        "catalog_sha256": baseline["catalog_sha256"],
        "baseline_sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        "prior_results_sha256": hashlib.sha256(
            (prior_run / "results.json").read_bytes()
        ).hexdigest(),
        "prior_ledger_sha256": hashlib.sha256(
            (prior_run / "hosted-requests.jsonl").read_bytes()
        ).hexdigest(),
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / "src/maintainer_copilot").glob("*.py"))
        },
        "generation": {
            "temperature": 0,
            "max_completion_tokens": 4096,
            "reasoning_effort": "low",
            "timeout_seconds": 120,
        },
        "attribution": "Hosted predictions differ from confirmed case annotations; "
        "fresh report usefulness and semantic support remain pending human review.",
        "providers": identities,
        "preflight": [],
        "cases": [],
    }
    path = directory / "results.json"
    _save(path, artifact)
    for case in catalog:
        error = (
            local[case.issue_number]["error"] or previous[case.issue_number]["error"]
        )
        if error is None:
            try:
                report = replay_case(
                    case,
                    commit_source=evidence,
                    issue_source=evidence,
                    source_reader=evidence,
                    candidate_catalog=catalog,
                    keyword_filter=True,
                )
                trace = get_trace(report.trace_id)
                if trace is None or any(
                    e.name in ("get_documentation_passage", "get_source_excerpt")
                    and e.status != "ok"
                    for e in trace.events
                ):
                    raise CaseFlagged("Historical repository evidence unavailable")
            except (CaseFlagged, ValueError) as exc:
                error = str(exc)
        artifact["preflight"].append(
            {"issue_number": case.issue_number, "error": error}
        )
        _save(path, artifact)
    evidence.frozen = True
    artifact["evidence_sha256"] = evidence.manifest()
    artifact["status"] = "running"
    for index, (case, preflight) in enumerate(
        zip(catalog, artifact["preflight"], strict=True)
    ):
        names = list(FLASH_MODELS) if index % 2 == 0 else list(reversed(FLASH_MODELS))
        for name in names:
            client = FlashModel(key, FLASH_MODELS[name], budget, case.issue_number)
            error = preflight["error"]
            if error is None:
                evaluated = evaluate_local_model(
                    client,
                    cases=catalog,
                    commit_source=evidence,
                    issue_source=evidence,
                    source_reader=evidence,
                    skip_issue_numbers=[c.issue_number for c in catalog if c != case],
                )
                record = evaluated["cases"][0]
                failed_model = record["trace"] is None or any(
                    e["kind"] == "model" and e["status"] != "ok"
                    for e in record["trace"]["events"]
                )
                if failed_model or not client.calls:
                    error = (
                        "Hosted inference failed or was refused; fallback is unscored"
                    )
                    record["scores"] = None
                    for observed_call in record["model_calls"]:
                        observed_call.pop("response", None)
            else:
                record = {
                    "issue_number": case.issue_number,
                    "report": None,
                    "trace": None,
                    "scores": None,
                    "latency_ms": 0.0,
                    "model_calls": [],
                }
            artifact["cases"].append(
                {
                    **record,
                    "method": name,
                    "error": error or record.get("error"),
                    "opening_cutoff": case.opening_cutoff.isoformat(),
                    "repository_commit": case.repository_commit,
                    "opening_content_sha256": case.opening_content_sha256,
                    "candidate_numbers": local[case.issue_number]["candidate_numbers"],
                    "candidate_pool_size": len(
                        local[case.issue_number]["candidate_numbers"]
                    ),
                    "expected_outcome": case.expected_outcome.model_dump(mode="json"),
                    "case_review": case.human_review.model_dump(mode="json"),
                    "local_fixed_scores": local[case.issue_number]["scores"],
                    "gpt41_scores": previous[case.issue_number]["scores"],
                    "hosted_calls": client.calls,
                }
            )
            artifact["accounting"] = budget.summary()
            _save(path, artifact)
    fields = tuple(CaseResult.__dataclass_fields__)
    artifact["aggregate"] = {}
    for name in FLASH_MODELS:
        rows = [r for r in artifact["cases"] if r["method"] == name]
        artifact["aggregate"][name] = aggregate(
            [CaseResult(**{k: r.get(k) for k in fields}) for r in rows]
        )
    by_method = {
        name: {r["issue_number"]: r for r in artifact["cases"] if r["method"] == name}
        for name in FLASH_MODELS
    }
    common = [
        c.issue_number
        for c in catalog
        if all(
            by_method[name][c.issue_number]["scores"] is not None
            for name in FLASH_MODELS
        )
        and local[c.issue_number]["scores"] is not None
        and previous[c.issue_number]["scores"] is not None
    ]
    artifact["common_paired_cases"] = len(common)
    artifact["paired_case_numbers"] = common
    artifact["paired_aggregate"] = {}
    for name, records in {"qwen3b": local, "gpt41": previous, **by_method}.items():
        paired = []
        for number in common:
            row = records[number]
            paired.append(
                CaseResult(
                    number,
                    name,
                    row["opening_cutoff"],
                    row["repository_commit"],
                    row.get("latency_ms", 0.0),
                    len(row["candidate_numbers"]),
                    None,
                    row["scores"],
                )
            )
        artifact["paired_aggregate"][name] = aggregate(paired)
    artifact["status"] = (
        "complete"
        if all(r["error"] is None for r in artifact["cases"])
        else "incomplete"
    )
    _save(path, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    evidence = _LiveEvidenceCache()
    evaluate_flash_reference(
        args.directory,
        os.getenv("OPENROUTER_API_KEY", ""),
        cases=load_cases(),
        baseline_path=BASELINE,
        prior_run=PRIOR_RUN,
        commit_source=evidence,
        issue_source=evidence,
        source_reader=evidence,
    )


if __name__ == "__main__":
    main()
