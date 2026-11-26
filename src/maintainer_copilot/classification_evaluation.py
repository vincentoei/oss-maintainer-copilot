"""Frozen Qwen before/after measurements and inference-free label availability."""

import argparse
import hashlib
from collections.abc import Collection
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from maintainer_copilot import issue_search, model, source
from maintainer_copilot.evaluation import (
    CaseResult,
    KeywordRuleModel,
    aggregate,
    score_report,
)
from maintainer_copilot.local_evaluation import _GpuMemory, _LiveEvidenceCache
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
    MODEL_NAME,
    ROOT,
    _EvidenceSnapshot,
    _MeasuredEndpoint,
    _save,
    fingerprint,
    serving_snapshot,
)


class AvailabilityModel(model.OpenAICompatibleModel):
    """Exercise the real encoder without sending its request to a model server."""

    def __init__(self) -> None:
        super().__init__("http://unused.invalid", "availability-audit-no-inference")
        self.offered: list[str] = []

    def generate_json(
        self,
        system_prompt: str,
        user_data: object,
        *,
        max_tokens: int,
        response_schema: dict[str, object] | None = None,
    ) -> object:
        if not isinstance(user_data, dict) or not isinstance(response_schema, dict):
            raise ValueError("Classification encoder did not expose its contract")
        if "type_evidence_options" in user_data:
            self.offered = [o["issue_type"] for o in user_data["type_evidence_options"]]
            return {"type_evidence_index": None, "reply_citation_ids": []}
        properties = response_schema.get("properties")
        if not isinstance(properties, dict):
            raise ValueError("Classification schema unavailable")
        self.offered = [
            label for label in properties["issue_type"]["enum"] if label is not None
        ]
        return {"issue_type": None, "issue_type_quote": None, "reply_citation_ids": []}


def evaluate_classification(
    directory: Path,
    base_url: str,
    *,
    phase: str,
    cases: Collection[HistoricalCase],
    commit_source: CommitSource,
    issue_source: issue_search.IssueSource,
    source_reader: source.SourceReader,
    serving: dict[str, Any] | None = None,
    measure_gpu: bool = False,
) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=False)
    catalog = sorted(cases, key=lambda c: c.issue_number)
    evidence = _EvidenceSnapshot(commit_source, issue_source, source_reader)
    artifact: dict[str, Any] = {
        "phase": phase,
        "status": "preflight",
        "recorded_at": datetime.now(UTC).isoformat(),
        "model": MODEL_NAME,
        "serving": serving,
        "catalog_sha256": fingerprint([c.model_dump(mode="json") for c in catalog]),
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / "src/maintainer_copilot").glob("*.py"))
        },
        "generation": {
            "max_tokens": 256,
            "timeout_seconds": 20,
            "max_dispatches": 50,
            "warmups": 0,
            "retries": 0,
        },
        "preflight": [],
        "cases": [],
        "report_review": "pending_human_review; no prior ratings transferred",
        "model_api_usd": 0,
    }
    output = directory / "results.json"
    _save(output, artifact)
    for case in catalog:
        audit = AvailabilityModel()
        error = None
        try:
            audit_report = replay_case(
                case,
                model_client=audit,
                candidate_catalog=catalog,
                keyword_filter=True,
                commit_source=evidence,
                issue_source=evidence,
                source_reader=evidence,
            )
            trace = get_trace(audit_report.trace_id)
            if trace is None or any(
                e.status != "ok"
                for e in trace.events
                if e.name
                in (
                    "get_documentation_passage",
                    "get_source_excerpt",
                    "triage_selection",
                )
            ):
                raise CaseFlagged(
                    "Evidence or inference-free contract audit unavailable"
                )
        except (CaseFlagged, ValueError) as exc:
            error = str(exc)
        expected = case.expected_outcome.issue_type
        artifact["preflight"].append(
            {
                "issue_number": case.issue_number,
                "error": error,
                "opening_cutoff": case.opening_cutoff.isoformat(),
                "opening_content_sha256": case.opening_content_sha256,
                "repository_commit": case.repository_commit,
                "offered_types": audit.offered if error is None else None,
                "expected_type": expected,
                "expected_reachable": (expected is None or expected in audit.offered)
                if error is None
                else None,
            }
        )
        _save(output, artifact)
    evidence.frozen = True
    artifact["evidence_sha256"] = evidence.manifest()
    artifact["status"] = "running"
    results = []
    for case, preflight in zip(catalog, artifact["preflight"], strict=True):
        client = _MeasuredEndpoint(
            base_url, "fixed_rag", case.issue_number, directory, 50
        )
        report = None
        scores = None
        keyword = None
        keyword_scores = None
        error = preflight["error"]
        numbers = [r.number for r in candidate_references(case, catalog)]
        with _GpuMemory(measure_gpu) as gpu:
            started = perf_counter()
            if error is None:
                try:
                    keyword = replay_case(
                        case,
                        model_client=KeywordRuleModel(),
                        candidate_catalog=catalog,
                        keyword_filter=True,
                        commit_source=evidence,
                        issue_source=evidence,
                        source_reader=evidence,
                    )
                    keyword_scores = score_report(case, keyword, numbers)
                    report = replay_case(
                        case,
                        model_client=client,
                        candidate_catalog=catalog,
                        keyword_filter=True,
                        commit_source=evidence,
                        issue_source=evidence,
                        source_reader=evidence,
                    )
                    trace = get_trace(report.trace_id)
                    if (
                        not client.calls
                        or trace is None
                        or any(
                            e.kind == "model" and e.status != "ok" for e in trace.events
                        )
                    ):
                        error = "Inference failed/refused; fallback is unscored"
                    else:
                        scores = score_report(case, report, numbers)
                except (CaseFlagged, ValueError) as exc:
                    error = str(exc)
            latency = round((perf_counter() - started) * 1000, 3)
        result = CaseResult(
            case.issue_number,
            phase,
            case.opening_cutoff.isoformat(),
            case.repository_commit,
            latency,
            len(numbers),
            error,
            scores,
        )
        results.append(result)
        trace = get_trace(report.trace_id) if report else None
        artifact["cases"].append(
            {
                **asdict(result),
                "opening_content_sha256": case.opening_content_sha256,
                "candidate_numbers": numbers,
                "report": report.model_dump(mode="json") if report else None,
                "trace": trace.model_dump(mode="json") if trace else None,
                "model_calls": client.calls,
                "gpu_memory": gpu.summary(),
                "keyword_report": keyword.model_dump(mode="json") if keyword else None,
                "keyword_scores": keyword_scores,
            }
        )
        _save(output, artifact)
        print(f"{phase} #{case.issue_number}: {error or 'scored'}", flush=True)
    artifact["aggregate"] = aggregate(results)
    artifact["status"] = (
        "complete" if all(r.error is None for r in results) else "incomplete"
    )
    _save(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--phase", choices=("before", "after"), required=True)
    parser.add_argument("--ollama-url", required=True)
    args = parser.parse_args()
    cases = load_cases()
    if len(cases) != 50 or any(c.human_review.status != "confirmed" for c in cases):
        parser.error("The frozen fifty confirmed cases are required")
    base = args.ollama_url.rstrip("/")
    serving = serving_snapshot(base)
    cache = _LiveEvidenceCache()
    result = evaluate_classification(
        args.directory,
        base + "/v1",
        phase=args.phase,
        cases=cases,
        commit_source=cache,
        issue_source=cache,
        source_reader=cache,
        serving=serving,
        measure_gpu=True,
    )
    result["serving_after"] = serving_snapshot(base)
    _save(args.directory / "results.json", result)


if __name__ == "__main__":
    main()
