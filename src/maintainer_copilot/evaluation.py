"""Field-level scoring of time-frozen pytest triage reports."""

import argparse
import json
import re
from collections.abc import Collection
from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any

from maintainer_copilot import model, pytest_profile
from maintainer_copilot.replay import (
    CaseFlagged,
    HistoricalCase,
    allowed_case_citation_urls,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.triage import TriageReport


class KeywordRuleModel:
    """Select an issue type from literal cues and include all cited reply rules."""

    def generate(self, request: model.ModelRequest) -> object:
        issue_text = f"{request.issue_title}\n{request.issue_body}"
        priority = pytest_profile.BASELINE_TYPE_PRIORITY
        labels = priority + tuple(
            label for label in pytest_profile.TYPE_LABELS if label not in priority
        )
        for passage in (request.issue_title, request.issue_body):
            for label in labels:
                for match in re.finditer(
                    pytest_profile.TYPE_EVIDENCE_CUES[label], passage, re.I
                ):
                    quote = match.group()
                    if pytest_profile.type_quote_supports_label(
                        label, quote, issue_text
                    ):
                        return {
                            "issue_type": label,
                            "issue_type_quote": quote,
                            "reply_citation_ids": [
                                item.citation_id for item in request.reply_statements
                            ],
                        }
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": [
                item.citation_id for item in request.reply_statements
            ],
        }


def citation_errors(
    case: HistoricalCase,
    report: TriageReport,
    candidate_numbers: Collection[int] | None = None,
) -> list[str]:
    """Check saved citations against this case's verified evidence boundary."""
    errors: list[str] = []
    verified_numbers = set(candidate_numbers or (case.earlier_issue.number,))
    allowed = allowed_case_citation_urls(case, verified_numbers)
    citation_by_id = {item.id: item for item in report.citations}
    for citation in report.citations:
        url = str(citation.source_url)
        if url not in allowed:
            errors.append(f"{citation.id}: source is outside the evidence cutoff")
        if (
            citation.source_location
            and citation.source_location.commit != case.repository_commit
        ):
            errors.append(f"{citation.id}: source location uses a different commit")
    for item in report.duplicate_candidates + report.related_issues:
        if item.issue_number not in verified_numbers:
            errors.append(f"{item.citation_id}: unverified earlier issue")
        if item.citation_id not in citation_by_id:
            errors.append(f"{item.citation_id}: missing issue citation")
    if report.ci_results:
        errors.append("historical CI results are unavailable")
    for detail in report.missing_details:
        detail_citation = citation_by_id.get(detail.citation_id)
        if detail_citation is None or "/.github/ISSUE_TEMPLATE/" not in str(
            detail_citation.source_url
        ):
            errors.append(f"{detail.citation_id}: missing pinned template citation")
        if f"[{detail.citation_id}]" not in report.draft_reply:
            errors.append(f"{detail.citation_id}: missing draft citation")
    for citation_id in re.findall(r"\[(C\d+)\]", report.draft_reply):
        if citation_id not in citation_by_id:
            errors.append(f"{citation_id}: unknown draft citation")
    return errors


def score_report(
    case: HistoricalCase,
    report: TriageReport,
    candidate_numbers: Collection[int] | None = None,
) -> dict[str, Any]:
    """Score exact fields, and mark semantic judgments for human review."""
    if case.human_review.status != "confirmed":
        raise ValueError("case needs a confirmed human review before scoring")
    expected = case.expected_outcome
    earlier = case.earlier_issue.number
    retrieved_numbers = sorted(
        {
            item.issue_number
            for item in report.duplicate_candidates + report.related_issues
        }
    )
    found = earlier in retrieved_numbers
    duplicate = earlier in {item.issue_number for item in report.duplicate_candidates}
    if expected.earlier_issue_relationship == "uncertain":
        duplicate_judgment: bool | None = None
    else:
        duplicate_judgment = (
            duplicate == (expected.earlier_issue_relationship == "duplicate_candidate")
            and found
        )
    actual_details = {item.name for item in report.missing_details}
    expected_details = set(expected.missing_details)
    true_positive = len(actual_details & expected_details)
    precision = true_positive / len(actual_details) if actual_details else 1.0
    recall = true_positive / len(expected_details) if expected_details else 1.0
    errors = citation_errors(case, report, candidate_numbers)
    abstained = {item.field for item in report.abstentions}
    duplicate_abstention_expected = expected.earlier_issue_relationship == "uncertain"
    return {
        "duplicate_retrieval": {
            "found": found,
            "expected_issue": earlier,
            "retrieved_issues": retrieved_numbers,
            "other_issues_unreviewed": [
                number for number in retrieved_numbers if number != earlier
            ],
        },
        "duplicate_judgment": {
            "correct": duplicate_judgment,
            "expected": expected.earlier_issue_relationship,
            "observed": "duplicate_candidate"
            if duplicate
            else "related_issue"
            if found
            else "not_retrieved",
            "review_status": "pending_human_review"
            if duplicate_judgment is None
            else "exact",
        },
        "issue_type": {
            "correct": report.issue_type == expected.issue_type,
            "expected": expected.issue_type,
            "observed": report.issue_type,
        },
        "missing_details": {
            "exact": actual_details == expected_details,
            "precision": precision,
            "recall": recall,
            "expected": sorted(expected_details),
            "observed": sorted(actual_details),
        },
        "citation_validity": {
            "valid": not errors,
            "checked": len(report.citations),
            "errors": errors,
            "semantic_review_status": "pending_human_review",
        },
        "abstention": {
            "observed_fields": sorted(abstained),
            "issue_type_appropriate": ("issue_type" in abstained)
            == (expected.issue_type is None),
            "duplicate_expected": duplicate_abstention_expected,
            "duplicate_observed": "duplicate_candidates" in abstained,
            "duplicate_appropriate": ("duplicate_candidates" in abstained)
            == duplicate_abstention_expected,
            "other_fields_review_status": "pending_human_review",
        },
        "draft_reply_usefulness": {
            "review_status": "pending_human_review",
            "rating": None,
            "rubric": (
                "Does the reply ask for needed details and explain relevant "
                "evidence without misleading claims?"
            ),
            "draft_reply": report.draft_reply,
            "citations": [
                {
                    "id": citation.id,
                    "source_url": str(citation.source_url),
                    "description": citation.description,
                    "passage": citation.passage,
                }
                for citation in report.citations
            ],
        },
    }


@dataclass(frozen=True)
class CaseResult:
    issue_number: int
    method: str
    opening_cutoff: str
    repository_commit: str
    latency_ms: float
    candidate_pool_size: int
    error: str | None
    scores: dict[str, Any] | None


def evaluate_case(
    case: HistoricalCase,
    method: str,
    catalog: Collection[HistoricalCase] | None = None,
) -> CaseResult:
    """Run one method against a verified historical case."""
    if method not in ("controlled", "keyword_rule"):
        raise ValueError("unknown evaluation method")
    started = perf_counter()
    pool_size = 0
    try:
        candidate_catalog = (
            (catalog if catalog is not None else load_cases())
            if method == "keyword_rule"
            else ()
        )
        candidate_numbers = tuple(
            reference.number
            for reference in candidate_references(case, candidate_catalog)
        )
        pool_size = len(candidate_numbers)
        report = replay_case(
            case,
            model_client=(KeywordRuleModel() if method == "keyword_rule" else None),
            keyword_filter=method == "keyword_rule",
            candidate_catalog=candidate_catalog,
        )
        scores = score_report(case, report, candidate_numbers)
        error = None
    except (CaseFlagged, ValueError) as exc:
        scores = None
        error = str(exc)
    return CaseResult(
        issue_number=case.issue_number,
        method=method,
        opening_cutoff=case.opening_cutoff.isoformat(),
        repository_commit=case.repository_commit,
        latency_ms=round((perf_counter() - started) * 1000, 2),
        candidate_pool_size=pool_size,
        error=error,
        scores=scores,
    )


def aggregate(results: list[CaseResult]) -> dict[str, Any]:
    """Summarize independent field scores without converting pending reviews to wins."""
    complete = [item for item in results if item.scores is not None]
    failures = []
    for item in complete:
        assert item.scores is not None
        for field, metric in item.scores.items():
            if isinstance(metric, dict) and (
                metric.get("correct") is False
                or metric.get("exact") is False
                or metric.get("valid") is False
                or metric.get("found") is False
                or metric.get("issue_type_appropriate") is False
                or metric.get("duplicate_appropriate") is False
            ):
                failures.append({"issue_number": item.issue_number, "field": field})
    representative = []
    seen_fields: set[str] = set()
    for failure in failures:
        field_name = str(failure["field"])
        if field_name not in seen_fields:
            representative.append(failure)
            seen_fields.add(field_name)
    return {
        "cases": len(results),
        "completed": len(complete),
        "errors": [
            {"issue_number": item.issue_number, "error": item.error}
            for item in results
            if item.error is not None
        ],
        "mean_latency_ms": round(
            sum(item.latency_ms for item in results) / len(results), 2
        )
        if results
        else None,
        "mean_candidate_pool_size": round(
            sum(item.candidate_pool_size for item in results) / len(results), 2
        )
        if results
        else None,
        "duplicate_retrieval_recall": _mean(complete, "duplicate_retrieval", "found"),
        "duplicate_judgment_accuracy": _mean(complete, "duplicate_judgment", "correct"),
        "issue_type_accuracy": _mean(complete, "issue_type", "correct"),
        "missing_details_exact": _mean(complete, "missing_details", "exact"),
        "missing_details_precision": _mean(complete, "missing_details", "precision"),
        "missing_details_recall": _mean(complete, "missing_details", "recall"),
        "citation_validity_rate": _mean(complete, "citation_validity", "valid"),
        "issue_type_abstention_appropriateness": _mean(
            complete, "abstention", "issue_type_appropriate"
        ),
        "duplicate_abstention_appropriateness": _mean(
            complete, "abstention", "duplicate_appropriate"
        ),
        "draft_reply_usefulness": "pending_human_review",
        "representative_failures": representative[:5],
    }


def _mean(results: list[CaseResult], field: str, key: str) -> float | None:
    values = [
        item.scores[field][key]
        for item in results
        if item.scores is not None and item.scores[field][key] is not None
    ]
    return round(sum(values) / len(values), 3) if values else None


def evaluate_all() -> dict[str, Any]:
    cases = load_cases()
    groups = {
        method: [evaluate_case(case, method, catalog=cases) for case in cases]
        for method in ("controlled", "keyword_rule")
    }
    return {
        "methods": {
            method: {
                "aggregate": aggregate(results),
                "cases": [asdict(item) for item in results],
            }
            for method, results in groups.items()
        },
        "cost_assumptions": {
            "model_api_usd": 0,
            "github_api_usd": 0,
            "scope": (
                "No paid model calls; public GitHub reads have no per-request "
                "charge. CPU, network, and hosting costs excluded."
            ),
        },
        "methodology": (
            "Both methods replay the same verified issue text, earlier issue, "
            "and pinned pytest commit. The keyword-rule baseline searches all "
            "hash-verified opening issues in the published case catalog that "
            "precede each cutoff, applies lexical match and template rules, "
            "and selects type by cue. Controlled responses are a one-pair smoke "
            "comparator, not model quality."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score reviewed historical cases")
    parser.parse_args()
    print(json.dumps(evaluate_all(), indent=2))
