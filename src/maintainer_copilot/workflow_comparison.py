"""Frozen, single-pass keyword/fixed-RAG/agent historical comparisons."""

import argparse
import fcntl
import hashlib
import itertools
import json
import math
import os
import platform
import random
import re
import sys
from collections.abc import Callable, Collection
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Literal

from maintainer_copilot import agent, issue_search, model, source
from maintainer_copilot.evaluation import (
    CaseResult,
    KeywordRuleModel,
    aggregate,
    score_report,
)
from maintainer_copilot.local_evaluation import (
    _GpuMemory,
    _LiveEvidenceCache,
    _ollama_json,
)
from maintainer_copilot.replay import (
    CaseFlagged,
    CommitSource,
    HistoricalCase,
    RepositoryCommit,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.trace import get_trace

METHODS = ("keyword_rule", "fixed_rag", "bounded_agent")
MODEL_NAME = "pytest-triage:coder3b-ctx16k"
MODEL_DIGEST = "3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8"
ROOT = Path(__file__).resolve().parents[2]
CASE_COUNTS = {16: 20, 17: 30, 18: 40, 56: 40}


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _save(path: Path, value: object) -> None:
    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


class RequestBudget:
    """Charge before dispatch, including failures and ambiguous interruptions."""

    def __init__(self, directory: Path, *, case_count: int = 20) -> None:
        if case_count not in CASE_COUNTS.values():
            raise ValueError("Comparison budget requires twenty, thirty or forty cases")
        self.path = directory / "requests.jsonl"
        self.case_count = case_count

    def reserve(
        self, method: str, issue_number: int, metadata: dict[str, Any]
    ) -> dict[str, Any]:
        limit = {"fixed_rag": 1, "bounded_agent": 4}.get(method, 0)
        with self.path.open("a+") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            previous = [json.loads(line) for line in handle]
            if any(r.get("case_count", 20) != self.case_count for r in previous):
                raise model.ModelUnavailable("Frozen inference budget changed")
            used = sum(
                r["method"] == method and r["issue_number"] == issue_number
                for r in previous
            )
            arm_used = sum(r["method"] == method for r in previous)
            arm_limit = {
                "fixed_rag": self.case_count,
                "bounded_agent": self.case_count * 4,
            }.get(method, 0)
            if (
                len(previous) >= self.case_count * 5
                or used >= limit
                or arm_used >= arm_limit
            ):
                raise model.ModelUnavailable("Frozen inference budget exhausted")
            if metadata.get("max_tokens") != 256:
                raise model.ModelUnavailable("Frozen output budget is 256 tokens")
            record = {
                **metadata,
                "request": len(previous) + 1,
                "method": method,
                "issue_number": issue_number,
                "case_count": self.case_count,
                "dispatched_at": datetime.now(UTC).isoformat(),
            }
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            return record


class _MeasuredEndpoint(agent.OpenAICompatibleAgent):
    """Keep legacy prompts and schemas; observe every actual HTTP dispatch."""

    def __init__(
        self,
        base_url: str,
        method: str,
        number: int,
        directory: Path,
        case_count: int,
    ) -> None:
        super().__init__(base_url, MODEL_NAME, response_observer=self._capture_response)
        self.method = method
        self.number = number
        self.directory = directory
        self.case_count = case_count
        self.calls: list[dict[str, Any]] = []
        self.raw_response: bytes | None = None

    def _capture_response(self, body: bytes) -> None:
        self.raw_response = body

    def generate_json(
        self,
        system_prompt: str,
        user_data: object,
        *,
        max_tokens: int,
        response_schema: dict[str, object] | None = None,
    ) -> object:
        record = RequestBudget(self.directory, case_count=self.case_count).reserve(
            self.method,
            self.number,
            {
                "prompt_sha256": fingerprint(system_prompt),
                "input_sha256": fingerprint(user_data),
                "schema_sha256": fingerprint(response_schema),
                "max_tokens": max_tokens,
            },
        )
        started = perf_counter()
        self.raw_response = None
        try:
            response = super().generate_json(
                system_prompt,
                user_data,
                max_tokens=max_tokens,
                response_schema=response_schema,
            )
            record["response"] = (
                asdict(response)
                if isinstance(response, model.ModelResponse)
                else response
            )
            return response
        except Exception as exc:
            record["error_type"] = type(exc).__name__
            raise
        finally:
            if self.raw_response is not None:
                record.update(
                    raw_response_utf8=self.raw_response.decode(errors="replace"),
                    raw_response_sha256=hashlib.sha256(self.raw_response).hexdigest(),
                    raw_response_bytes=len(self.raw_response),
                    raw_response_truncated=len(self.raw_response) > 65536,
                )
            record["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            self.calls.append(record)
            with (self.directory / "responses.jsonl").open("a") as handle:
                handle.write(json.dumps(record) + "\n")
                handle.flush()
                os.fsync(handle.fileno())


class _EvidenceSnapshot:
    """Freeze successful and failed public reads before any arm is timed."""

    def __init__(
        self,
        commits: CommitSource,
        issues: issue_search.IssueSource,
        reader: source.SourceReader,
    ) -> None:
        self.commits = commits
        self.issues = issues
        self.reader = reader
        self.commit_cache: dict[object, RepositoryCommit] = {}
        self.issue_cache: dict[object, issue_search.IssueRecord] = {}
        self.source_cache: dict[object, source.SourceExcerpt] = {}
        self.failures: dict[object, Exception] = {}
        self.frozen = False

    def _read[T](
        self,
        key: object,
        cache: dict[object, T],
        read: Callable[[], T],
    ) -> T:
        if key in self.failures:
            raise self.failures[key]
        if key not in cache:
            if self.frozen:
                raise CaseFlagged("Evidence was not acquired in shared preflight")
            try:
                cache[key] = read()
            except Exception as exc:
                self.failures[key] = exc
                raise
        return cache[key]

    def get_commit(self, sha: str) -> RepositoryCommit:
        return self._read(
            ("commit", sha), self.commit_cache, lambda: self.commits.get_commit(sha)
        )

    def get_issue(self, number: int) -> issue_search.IssueRecord:
        return self._read(
            ("issue", number), self.issue_cache, lambda: self.issues.get_issue(number)
        )

    def get_excerpt(self, location: source.SourceLocation) -> source.SourceExcerpt:
        key = ("source", location.commit, location.path, location.line)
        return self._read(
            key, self.source_cache, lambda: self.reader.get_excerpt(location)
        )

    def search_issues(
        self,
        query: str,
        created_before: datetime,
    ) -> list[issue_search.IssueRecord]:
        raise CaseFlagged("Historical comparison cannot search the live issue index")

    def manifest(self) -> dict[str, Any]:
        return {
            "commits": {
                str(k): fingerprint(
                    {"sha": v.sha, "committed_at": v.committed_at.isoformat()}
                )
                for k, v in self.commit_cache.items()
            },
            "issues": {
                str(k): fingerprint(
                    {
                        "number": v.number,
                        "title": v.title,
                        "body": v.body,
                        "created_at": v.created_at.isoformat(),
                    }
                )
                for k, v in self.issue_cache.items()
            },
            "excerpts": {
                str(k): fingerprint(v.model_dump(mode="json"))
                for k, v in self.source_cache.items()
            },
            "failures": {str(k): type(v).__name__ for k, v in self.failures.items()},
        }


def evaluate_comparison(
    directory: Path,
    base_url: str,
    *,
    cases: Collection[HistoricalCase],
    commit_source: CommitSource,
    issue_source: issue_search.IssueSource,
    source_reader: source.SourceReader,
    measure_gpu: bool = False,
    serving: dict[str, Any] | None = None,
    comparison_issue: Literal[16, 17, 18, 56] = 16,
    protocol_path: Path | None = None,
) -> dict[str, Any]:
    """Run once with shared eligibility; never replace or silently drop a case."""
    directory.mkdir(parents=True, exist_ok=False)
    catalog = sorted(cases, key=lambda case: case.issue_number)
    case_count = CASE_COUNTS[comparison_issue]
    evidence = _EvidenceSnapshot(commit_source, issue_source, source_reader)
    artifact: dict[str, Any] = {
        "status": "running",
        "recorded_at": datetime.now(UTC).isoformat(),
        "comparison_issue": comparison_issue,
        "planned_cases": case_count,
        "protocol_sha256": hashlib.sha256(
            (
                protocol_path
                or ROOT / f"docs/evaluation/issue-{comparison_issue}-protocol.md"
            ).read_bytes()
        ).hexdigest(),
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / "src/maintainer_copilot").glob("*.py"))
        },
        "catalog_sha256": fingerprint([c.model_dump(mode="json") for c in catalog]),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "serving": serving,
        "generation": {
            "max_tokens": 256,
            "timeout_seconds": 20,
            "response_bytes": 65536,
            "drafting": False,
        },
        "preflight": [],
        "cases": [],
    }
    output = directory / "results.json"
    _save(output, artifact)
    for case in catalog:
        started = perf_counter()
        error = None
        preflight_trace = None
        try:
            preflight_report = replay_case(
                case,
                commit_source=evidence,
                issue_source=evidence,
                source_reader=evidence,
                candidate_catalog=catalog,
                keyword_filter=True,
            )
            preflight_trace = get_trace(preflight_report.trace_id)
            if preflight_trace is None:
                raise CaseFlagged("Historical evidence verification trace unavailable")
            failed_evidence = [
                e.name
                for e in preflight_trace.events
                if e.name in ("get_documentation_passage", "get_source_excerpt")
                and e.status != "ok"
            ]
            if failed_evidence:
                raise CaseFlagged(
                    "Historical evidence could not be verified: "
                    + ", ".join(failed_evidence)
                )
        except (CaseFlagged, ValueError) as exc:
            error = str(exc)
        artifact["preflight"].append(
            {
                "issue_number": case.issue_number,
                "error": error,
                "trace": preflight_trace.model_dump(mode="json")
                if preflight_trace
                else None,
                "latency_ms": round((perf_counter() - started) * 1000, 3),
            }
        )
        _save(output, artifact)
    evidence.frozen = True
    artifact["evidence_sha256"] = evidence.manifest()
    _save(output, artifact)
    orders = list(itertools.permutations(METHODS))
    for index, case in enumerate(catalog):
        for method in orders[index % len(orders)]:
            client = _MeasuredEndpoint(
                base_url, method, case.issue_number, directory, case_count
            )
            report = None
            scores = None
            trace = None
            error = artifact["preflight"][index]["error"]
            numbers = [ref.number for ref in candidate_references(case, catalog)]
            with _GpuMemory(measure_gpu) as gpu:
                started = perf_counter()
                if error is None:
                    try:
                        report = replay_case(
                            case,
                            commit_source=evidence,
                            issue_source=evidence,
                            source_reader=evidence,
                            candidate_catalog=catalog,
                            keyword_filter=True,
                            model_client=KeywordRuleModel()
                            if method == "keyword_rule"
                            else client
                            if method == "fixed_rag"
                            else None,
                            agent_client=client if method == "bounded_agent" else None,
                        )
                        trace = get_trace(report.trace_id)
                        scores = score_report(case, report, numbers)
                    except (CaseFlagged, ValueError) as exc:
                        error = str(exc)
                latency_ms = round((perf_counter() - started) * 1000, 3)
            record = {
                **asdict(
                    CaseResult(
                        case.issue_number,
                        method,
                        case.opening_cutoff.isoformat(),
                        case.repository_commit,
                        latency_ms,
                        len(numbers),
                        error,
                        scores,
                    )
                ),
                "execution_index": len(artifact["cases"]),
                "opening_content_sha256": case.opening_content_sha256,
                "candidate_numbers": numbers,
                "report": report.model_dump(mode="json") if report else None,
                "trace": trace.model_dump(mode="json") if trace else None,
                "model_calls": client.calls,
                "gpu_memory": {**gpu.summary(), "samples_mib": list(gpu.samples)},
            }
            artifact["cases"].append(record)
            _save(output, artifact)
            status = report.status if report else "unavailable"
            print(
                f"{method} #{case.issue_number}: {error or status}",
                file=sys.stderr,
                flush=True,
            )
    artifact["status"] = "complete"
    artifact["summary"] = summarize_comparison(artifact)
    _save(output, artifact)
    write_review_sheet(directory, artifact)
    return artifact


def _usage(records: list[dict[str, Any]]) -> dict[str, Any]:
    calls = [call for row in records for call in row["model_calls"]]
    totals: dict[str, int | None] = {}
    for field in ("input_tokens", "output_tokens"):
        counts = [(call.get("response") or {}).get(field) for call in calls]
        totals[field] = (
            sum(int(c) for c in counts if c is not None)
            if all(type(count) is int for count in counts)
            else None
        )
    return {
        "dispatches": len(calls),
        **totals,
        "usage_missing_calls": sum(
            any(
                (call.get("response") or {}).get(f) is None
                for f in ("input_tokens", "output_tokens")
            )
            for call in calls
        ),
    }


def _exact_quality(row: dict[str, Any]) -> float | None:
    scores = row["scores"]
    if scores is None:
        return None
    values = [
        scores["issue_type"]["correct"],
        scores["missing_details"]["exact"],
        scores["duplicate_judgment"]["correct"],
    ]
    known = [int(value) for value in values if value is not None]
    return sum(known) / len(known)


def summarize_comparison(artifact: dict[str, Any]) -> dict[str, Any]:
    """Field and paired metrics; unknown semantics/usage never become successes."""
    groups = {
        method: [r for r in artifact["cases"] if r["method"] == method]
        for method in METHODS
    }
    methods: dict[str, Any] = {}
    fields = tuple(CaseResult.__dataclass_fields__)
    for method, rows in groups.items():
        results = [CaseResult(**{key: row[key] for key in fields}) for row in rows]
        latencies = sorted(r["latency_ms"] for r in rows)
        events = [
            event for row in rows if row["trace"] for event in row["trace"]["events"]
        ]
        methods[method] = {
            **aggregate(results),
            "denominators": {
                "catalog": len(artifact["preflight"]),
                "rows": len(rows),
                "scoreable_reports": sum(r["scores"] is not None for r in rows),
                "known_relationships": sum(
                    r["scores"] is not None
                    and r["scores"]["duplicate_judgment"]["correct"] is not None
                    for r in rows
                ),
            },
            "partial_reports": sum(
                r["report"] is not None and r["report"]["status"] == "partial"
                for r in rows
            ),
            "model_errors": sum(
                e["kind"] == "model" and e["status"] != "ok" for e in events
            ),
            "tool_errors": sum(
                e["kind"] == "tool" and e["status"] != "ok" for e in events
            ),
            "p50_latency_ms": latencies[math.ceil(len(latencies) * 0.5) - 1]
            if latencies
            else None,
            "p95_latency_ms": latencies[math.ceil(len(latencies) * 0.95) - 1]
            if latencies
            else None,
            "resources": _usage(rows),
            "peak_sampled_gpu_mib": max(
                (
                    r["gpu_memory"]["peak_sampled_used_mib"]
                    for r in rows
                    if r["gpu_memory"]["peak_sampled_used_mib"] is not None
                ),
                default=None,
            ),
            "representative_error": next(
                (
                    {"issue_number": r["issue_number"], "error": r["error"]}
                    for r in rows
                    if r["error"]
                ),
                None,
            ),
            "representative_model_failure": next(
                (
                    {"issue_number": r["issue_number"], "event": event}
                    for r in rows
                    if r["trace"]
                    for event in r["trace"]["events"]
                    if event["kind"] == "model" and event["status"] != "ok"
                ),
                None,
            ),
        }
    by_number = {
        method: {r["issue_number"]: r for r in rows} for method, rows in groups.items()
    }
    paired = []
    for case in artifact["preflight"]:
        number = case["issue_number"]
        qualities = {
            m: _exact_quality(by_number[m][number]) if number in by_number[m] else None
            for m in METHODS
        }
        fixed, bounded = qualities["fixed_rag"], qualities["bounded_agent"]
        paired.append(
            {
                "issue_number": number,
                "quality": qualities,
                "agent_minus_fixed": bounded - fixed
                if bounded is not None and fixed is not None
                else None,
            }
        )
    gains = [
        p["agent_minus_fixed"] for p in paired if p["agent_minus_fixed"] is not None
    ]
    fixed_method, agent_method = methods["fixed_rag"], methods["bounded_agent"]
    fixed_p95, agent_p95 = (
        fixed_method["p95_latency_ms"],
        agent_method["p95_latency_ms"],
    )
    latency_ratio = agent_p95 / fixed_p95 if fixed_p95 else None
    token_totals = {}
    for method in ("fixed_rag", "bounded_agent"):
        usage = methods[method]["resources"]
        token_totals[method] = (
            usage["input_tokens"] + usage["output_tokens"]
            if usage["input_tokens"] is not None and usage["output_tokens"] is not None
            else None
        )
    fixed_tokens, agent_tokens = (
        token_totals["fixed_rag"],
        token_totals["bounded_agent"],
    )
    token_ratio = (
        agent_tokens / fixed_tokens
        if (fixed_tokens and agent_tokens is not None)
        else None
    )
    field_deltas = {
        field: agent_method[field] - fixed_method[field]
        if agent_method[field] is not None and fixed_method[field] is not None
        else None
        for field in (
            "issue_type_accuracy",
            "missing_details_exact",
            "duplicate_judgment_accuracy",
            "citation_validity_rate",
        )
    }
    gain = sum(gains) / len(gains) if gains else None
    residency = artifact.get("serving_after", {}).get("residency", {}).get("models", [])
    loaded = next((m for m in residency if m.get("digest") == MODEL_DIGEST), None)
    gpu_peaks = [m["peak_sampled_gpu_mib"] for m in methods.values()]
    planned_cases = artifact.get("planned_cases", 20)
    pairs_gate = {
        20: "twenty_complete_pairs",
        30: "thirty_complete_pairs",
        40: "forty_complete_pairs",
    }[planned_cases]
    gates = {
        pairs_gate: len(gains) == planned_cases
        and all(
            methods[m]["completed"] == planned_cases
            and methods[m]["partial_reports"] == 0
            for m in ("fixed_rag", "bounded_agent")
        ),
        "no_additional_errors": all(
            agent_method[f] <= fixed_method[f]
            for f in ("partial_reports", "model_errors", "tool_errors")
        ),
        "paired_exact_gain_at_least_0_05": gain >= 0.05 if gain is not None else None,
        "no_field_drop_over_0_05": all(
            v is not None and v >= -0.05 - 1e-9
            for k, v in field_deltas.items()
            if k != "citation_validity_rate"
        ),
        "structural_citations_no_lower": field_deltas["citation_validity_rate"] >= 0
        if field_deltas["citation_validity_rate"] is not None
        else None,
        "p95_at_most_80s_and_2x_fixed": agent_p95 <= 80000 and latency_ratio <= 2
        if agent_p95 is not None and latency_ratio is not None
        else None,
        "tokens_at_most_2x_fixed": token_ratio <= 2
        if token_ratio is not None
        else None,
        "full_gpu_residency_ctx16k": loaded.get("size") == loaded.get("size_vram")
        and loaded.get("context_length") == 16384
        if loaded
        and type(loaded.get("size")) is int
        and loaded["size"] > 0
        and type(loaded.get("size_vram")) is int
        else None,
        "sampled_gpu_at_most_7680_mib": max(gpu_peaks) <= 7680
        if all(p is not None for p in gpu_peaks)
        else None,
        "fresh_human_gain_and_support": None,
    }
    return {
        "methods": methods,
        "paired": paired,
        "paired_agent_gain": gain,
        "paired_cases": len(gains),
        "missing_pairs": len(paired) - len(gains),
        "agent_vs_fixed": {
            "field_accuracy_deltas": field_deltas,
            "p95_latency_ratio": latency_ratio,
            "total_token_ratio": token_ratio,
            "dispatch_delta": agent_method["resources"]["dispatches"]
            - fixed_method["resources"]["dispatches"],
            "promotion_gates": gates,
        },
        "decision": {
            "workflow": "fixed_rag",
            "status": "retain_legacy_default",
            "reason": "Fresh human usefulness/semantic reviews are pending; "
            "promotion requires every frozen gate, not exact scores alone.",
        },
        "cost": {
            "marginal_model_api_usd": 0,
            "marginal_github_api_usd": 0,
            "unmeasured": ["hardware", "electricity", "network", "hosting"],
            "scope": "Local serving only; tokens/time are resource proxies, "
            "not a measured total dollar cost.",
        },
        "limitations": [
            "Exact fields use scoreable reports, including fallbacks; see coverage.",
            "Structural citation checks do not establish semantic support.",
            "Uncertain relationships and extra retrieved issues need human review.",
            "Latency excludes shared evidence acquisition and includes cold loads.",
            "GPU samples are device-wide and cannot establish true peaks.",
            f"Already exposed {planned_cases}-case development set; "
            "no generalization claim.",
        ],
    }


def write_review_sheet(directory: Path, artifact: dict[str, Any]) -> None:
    rows = list(artifact["cases"])
    random.Random(16).shuffle(rows)
    reviews, identities = [], []
    lines = [
        f"# Issue #{artifact.get('comparison_issue', 16)} fresh blinded reply review",
        "",
        "Rate useful (2), partly useful (1), or not useful (0). Preserve "
        "verbatim reasons. Review semantic support, unsupported claims or "
        "presuppositions, redundant requests, relationships and abstentions. "
        "Do not consult the separate identity key or transfer old ratings.",
        "",
    ]
    for index, row in enumerate(rows, 1):
        code = f"R{index:02}"
        report = row["report"]
        report_hash = fingerprint(report)
        identities.append(
            {
                "code": code,
                "method": row["method"],
                "issue_number": row["issue_number"],
                "report_sha256": report_hash,
            }
        )
        reviews.append(
            {
                "code": code,
                "report_sha256": report_hash,
                "status": "pending",
                "rating": None,
                "reason": None,
                "semantic_support": None,
                "unsupported_claims": None,
                "redundancy": None,
                "relationships": None,
                "abstention": None,
            }
        )
        lines.extend(
            [
                f"## {code}: pytest #{row['issue_number']}",
                "",
                f"Report fingerprint: `{report_hash}`",
                "",
                report["draft_reply"] if report else f"Unavailable: {row['error']}",
                "",
                "Evidence:",
                "",
            ]
        )
        if report:
            for citation in report["citations"]:
                lines.extend(
                    [
                        f"- [{citation['id']}]({citation['source_url']}): "
                        f"{citation['description']}"
                    ]
                )
                if citation.get("passage"):
                    lines.append(f"  Passage: {citation['passage']}")
        lines.extend(["", "Rating / verbatim reason / semantic notes: pending", ""])
    _save(directory / "human-review.json", reviews)
    _save(directory / "review-key.json", identities)
    (directory / "human-review.md").write_text("\n".join(lines))


def serving_snapshot(base: str) -> dict[str, Any]:
    """Read-only identity preflight. No warm-up or model creation."""
    baseline = json.loads(
        (ROOT / "docs/evaluation/issue-48-serving-review.json").read_text()
    )
    tags = _ollama_json(base + "/api/tags")
    identity = next(
        (item for item in tags["models"] if item["name"] == MODEL_NAME), None
    )
    if identity is None or identity["digest"] != MODEL_DIGEST:
        raise ValueError("Selected 3B identity missing or changed")
    if identity["details"]["quantization_level"] != "Q4_K_M":
        raise ValueError("Selected 3B quantization changed")
    info = _ollama_json(base + "/api/show", {"model": MODEL_NAME})
    parameters = dict(re.findall(r"^(\w+)\s+(\S+)\s*$", info["parameters"], re.M))
    if set(parameters) != set(baseline["parameters"]) or any(
        float(parameters[k]) != float(v) for k, v in baseline["parameters"].items()
    ):
        raise ValueError("Selected 3B serving settings changed")
    return {
        "identity": identity,
        "show": info,
        "template_sha256": fingerprint(info.get("template")),
        "version": _ollama_json(base + "/api/version"),
        "residency": _ollama_json(base + "/api/ps"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ollama-url", required=True)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--issue", type=int, choices=tuple(CASE_COUNTS), default=16)
    parser.add_argument("--protocol", type=Path)
    args = parser.parse_args()
    if args.directory.exists():
        parser.error("Run directory already exists; repetition/overwrite refused")
    baseline_path = (
        ROOT / f"docs/evaluation/issue-{args.issue}/baseline.json"
        if args.issue != 16
        else ROOT / "docs/evaluation/issue-16-baseline.json"
    )
    baseline = json.loads(baseline_path.read_text())
    for name, expected in baseline["files"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            parser.error(f"Preserved baseline changed: {name}")
    cases = load_cases()
    if args.issue in (16, 17):
        # Preserve archived run catalogs after subsequent expansions.
        original = json.loads(
            (
                ROOT / "docs/evaluation/issue-16/results.json"
                if args.issue == 16
                else ROOT / "docs/evaluation/issue-17/run/results.json"
            ).read_text()
        )
        numbers = {row["issue_number"] for row in original["preflight"]}
        cases = [case for case in cases if case.issue_number in numbers]
    expected_count = CASE_COUNTS[args.issue]
    if len(cases) != expected_count:
        parser.error(f"Frozen comparison requires {expected_count} cases")
    if any(case.human_review.status != "confirmed" for case in cases):
        parser.error("All expected outcomes require confirmed case review")
    base = args.ollama_url.rstrip("/")
    serving = serving_snapshot(base)
    evidence = _LiveEvidenceCache()
    result = evaluate_comparison(
        args.directory,
        base + "/v1",
        cases=cases,
        commit_source=evidence,
        issue_source=evidence,
        source_reader=evidence,
        measure_gpu=True,
        serving=serving,
        comparison_issue=args.issue,
        protocol_path=args.protocol,
    )
    try:
        result["serving_after"] = serving_snapshot(base)
    except Exception as exc:
        result["serving_after_error"] = type(exc).__name__
    result["summary"] = summarize_comparison(result)
    _save(args.directory / "results.json", result)


if __name__ == "__main__":
    main()
