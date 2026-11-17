"""Deterministic checks for the public evaluation scorer."""

from uuid import UUID

from maintainer_copilot.evaluation import (
    CaseResult,
    KeywordRuleModel,
    aggregate,
    citation_errors,
    score_report,
)
from maintainer_copilot.model import ModelRequest, ReplyStatement
from maintainer_copilot.replay import HistoricalCase, load_cases
from maintainer_copilot.triage import TriageReport


def case_for(number: int) -> HistoricalCase:
    return next(case for case in load_cases() if case.issue_number == number)


def report_for(
    case: HistoricalCase,
    *,
    duplicate: bool,
    issue_type: str | None,
    later_citation: bool = False,
) -> TriageReport:
    url = f"https://github.com/pytest-dev/pytest/issues/{case.earlier_issue.number}"
    suggestion = {
        "issue_number": case.earlier_issue.number,
        "title": "Earlier issue",
        "url": url,
        "reason": "Shared failure",
        "citation_id": "C1",
    }
    return TriageReport.model_validate(
        {
            "trace_id": str(UUID(int=1)),
            "status": "complete",
            "issue_type": issue_type,
            "issue_type_quote": "Feature" if issue_type else None,
            "duplicate_candidates": [suggestion] if duplicate else [],
            "related_issues": [] if duplicate else [suggestion],
            "missing_details": [],
            "documentation_claims": [],
            "source_claims": [],
            "ci_results": [],
            "draft_reply": "Earlier issue may be relevant [C1]",
            "citations": [
                {"id": "C1", "source_url": url, "description": "Earlier issue"},
                *(
                    [
                        {
                            "id": "C2",
                            "source_url": (
                                "https://github.com/pytest-dev/pytest/blob/"
                                f"{'f' * 40}/wrong.py#L1"
                            ),
                            "description": "Later source",
                        }
                    ]
                    if later_citation
                    else []
                ),
            ],
            "abstentions": [],
        }
    )


def test_field_scores_keep_retrieval_judgment_and_reply_review_separate() -> None:
    case = case_for(12081)
    scores = score_report(
        case, report_for(case, duplicate=False, issue_type="type: enhancement")
    )

    assert scores["duplicate_retrieval"]["found"] is True
    assert scores["duplicate_judgment"]["correct"] is False
    assert scores["issue_type"]["correct"] is True
    assert scores["missing_details"]["exact"] is True
    assert scores["citation_validity"]["valid"] is True
    assert scores["draft_reply_usefulness"]["rating"] is None


def test_uncertain_relationship_is_reserved_for_review() -> None:
    case = case_for(12083)
    scores = score_report(case, report_for(case, duplicate=True, issue_type=None))

    assert scores["duplicate_judgment"]["correct"] is None
    assert scores["duplicate_judgment"]["review_status"] == "pending_human_review"
    assert scores["missing_details"]["recall"] == 0


def test_citation_check_rejects_post_cutoff_source() -> None:
    case = case_for(12081)
    report = report_for(case, duplicate=True, issue_type=None, later_citation=True)

    assert citation_errors(case, report) == [
        "C2: source is outside the evidence cutoff"
    ]


def test_aggregate_excludes_pending_human_review_from_accuracy() -> None:
    uncertain = case_for(12083)
    result = CaseResult(
        issue_number=uncertain.issue_number,
        method="keyword_rule",
        opening_cutoff=uncertain.opening_cutoff.isoformat(),
        repository_commit=uncertain.repository_commit,
        latency_ms=10,
        error=None,
        scores=score_report(
            uncertain, report_for(uncertain, duplicate=False, issue_type=None)
        ),
    )

    summary = aggregate([result])

    assert summary["duplicate_judgment_accuracy"] is None
    assert summary["duplicate_retrieval_recall"] == 1
    assert summary["draft_reply_usefulness"] == "pending_human_review"


def test_keyword_rule_baseline_uses_opening_text_and_cited_statements() -> None:
    response = KeywordRuleModel().generate(
        ModelRequest(
            issue_title="Feature: preserve capture",
            issue_body="Please allow readouterr to keep output.",
            reply_statements=(
                ReplyStatement("C1", "Earlier issue", "https://example.org/1"),
            ),
            required_reply_ids=(),
        )
    )

    assert response == {
        "issue_type": "type: enhancement",
        "issue_type_quote": "Feature",
        "reply_citation_ids": ["C1"],
    }
