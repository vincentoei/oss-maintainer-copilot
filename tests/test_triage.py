import pytest
from pydantic import ValidationError

from maintainer_copilot import IssueUnderReview, TriageReport, triage_issue


def test_bug_report_requests_only_missing_template_details_with_citations() -> None:
    issue = IssueUnderReview(
        title="Bug: pytest fails on Ubuntu",
        body=(
            "Running pytest on Ubuntu 24.04 raises an error during collection. "
            "pytest version: 8.3.4.\n\n"
            "Minimal example:\n```python\ndef test_example():\n    assert True\n```"
        ),
    )

    report = triage_issue(issue)

    assert [detail.name for detail in report.missing_details] == ["pip list output"]
    assert report.missing_details[0].citation_id == "C1"
    assert str(report.citations[0].source_url) == (
        "https://github.com/pytest-dev/pytest/blob/"
        "50234b4e670064c42a4c29cb6258115a2079ba4c/"
        ".github/ISSUE_TEMPLATE/1_bug_report.md#L14"
    )
    assert "pip list" in report.draft_reply
    assert "[C1]" in report.draft_reply
    assert report.issue_type is None
    assert report.duplicate_candidates == []
    assert report.related_issues == []
    assert report.trace_id


def test_bug_detail_citations_match_pinned_template_lines() -> None:
    report = triage_issue(IssueUnderReview(title="Bug: collection fails", body=""))

    assert {
        detail.name: str(citation.source_url).rsplit("#", 1)[-1]
        for detail, citation in zip(
            report.missing_details, report.citations, strict=True
        )
    } == {
        "bug description": "L13",
        "pip list output": "L14",
        "pytest and OS versions": "L15",
        "minimal example": "L16",
    }


def test_feature_request_skips_supplied_details() -> None:
    issue = IssueUnderReview(
        title="Feature request: show fixture dependency graph",
        body=(
            "#### What's the problem this feature will solve?\n"
            "I cannot see which fixture depends on another in a large test suite.\n\n"
            "#### Describe the solution you'd like\n"
            "Please add a command to show the graph. For example, this would help "
            "debug a fixture cycle in a project.\n\n"
            "#### Alternative Solutions\n"
            "<!-- Have you tried to work around this? -->\n"
        ),
    )

    report = triage_issue(issue)

    assert [detail.name for detail in report.missing_details] == [
        "alternative solutions"
    ]
    assert "pip list" not in report.draft_reply
    assert "pytest and OS versions" not in report.draft_reply
    assert str(report.citations[0].source_url).endswith("/2_feature_request.md#L21")


def test_bug_metadata_without_narrative_still_requests_description() -> None:
    issue = IssueUnderReview(
        title="Bug: collection fails",
        body=(
            "pytest version: 8.3.4\n"
            "OS: Ubuntu 24.04\n"
            "pip list:\npytest 8.3.4\npluggy 1.5.0\n\n"
            "Minimal example:\n```python\ndef test_example():\n    assert True\n```"
        ),
    )

    report = triage_issue(issue)

    assert [detail.name for detail in report.missing_details] == ["bug description"]


def test_report_rejects_draft_reply_with_unknown_citation() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Bug: pytest fails", body="pytest fails during collection."
        )
    )
    payload = report.model_dump(mode="json")
    payload["draft_reply"] += " Refer to [C99]."

    with pytest.raises(ValidationError, match="unknown citation"):
        TriageReport.model_validate(payload)


def test_empty_pip_list_heading_does_not_count_as_supplied_output() -> None:
    issue = IssueUnderReview(
        title="Bug: collection fails",
        body=(
            "Collecting tests fails before any test is executed on my machine.\n"
            "pytest version: 8.3.4\nOS: Ubuntu 24.04\n"
            "pip list:\n\n"
            "Minimal example:\n```python\ndef test_example():\n    assert True\n```"
        ),
    )

    report = triage_issue(issue)

    assert [detail.name for detail in report.missing_details] == ["pip list output"]


def test_unknown_template_abstains_instead_of_requesting_inapplicable_details() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Question about collection",
            body="I would like to discuss how test collection is intended to work.",
        )
    )

    assert report.issue_type is None
    assert report.missing_details == []
    assert report.citations == []
    assert "missing_details" in {item.field for item in report.abstentions}


def test_empty_minimal_example_does_not_count_as_supplied() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Bug: collection fails",
            body=(
                "Collecting tests fails before any test is executed on my machine.\n"
                "pytest version: 8.3.4\nOS: Ubuntu 24.04\n"
                "pip list:\npytest 8.3.4\n\n"
                "Minimal example:\n```python\n```"
            ),
        )
    )

    assert [detail.name for detail in report.missing_details] == ["minimal example"]


def test_feature_template_headings_select_details_with_neutral_title() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Fixture dependency graph",
            body=(
                "#### What's the problem this feature will solve?\n"
                "A fixture cycle is hard to locate in a large project.\n\n"
                "#### Describe the solution you'd like\n"
                "Show a graph of fixture dependencies. For example, this would "
                "show a cycle before tests run.\n"
            ),
        )
    )

    assert [detail.name for detail in report.missing_details] == [
        "alternative solutions"
    ]


def test_error_traceback_is_not_a_minimal_example() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Bug: collection fails",
            body=(
                "Collecting tests fails before any test is executed on my machine.\n"
                "pytest version: 8.3.4\nOS: Ubuntu 24.04\n"
                "pip list:\npytest 8.3.4\n\n"
                "```text\nTraceback (most recent call last):\nRuntimeError: boom\n```"
            ),
        )
    )

    assert [detail.name for detail in report.missing_details] == ["minimal example"]


def test_bug_prefix_wins_when_title_mentions_feature() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Bug: feature flags fail during collection",
            body=(
                "Collection fails when feature flags are enabled on this project. "
                "pytest version: 8.3.4. OS: Ubuntu 24.04.\n"
                "Minimal example:\n```python\ndef test_example():\n    assert True\n```"
            ),
        )
    )

    assert [detail.name for detail in report.missing_details] == ["pip list output"]
    assert str(report.citations[0].source_url).endswith("/1_bug_report.md#L14")


def test_concrete_feature_use_case_is_not_requested_again() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Feature request: show fixture cycles",
            body=(
                "#### What's the problem this feature will solve?\n"
                "We maintain a monorepo with 900 fixtures and need to see which "
                "fixture creates a cycle.\n\n"
                "#### Describe the solution you'd like\n"
                "Show a graph of fixture dependencies.\n\n"
                "#### Alternative Solutions\nNone.\n"
            ),
        )
    )

    assert report.missing_details == []


def test_explicit_freebsd_version_is_not_requested_again() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Bug: collection fails on FreeBSD",
            body=(
                "Collecting tests fails before any test is executed on my machine.\n"
                "pytest version: 8.3.4\nOS: FreeBSD 14.1\n"
                "pip list:\npytest 8.3.4\n\n"
                "Minimal example:\n```python\ndef test_example():\n    assert True\n```"
            ),
        )
    )

    assert report.missing_details == []


def test_feature_solution_without_usage_context_still_requests_use_case() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Feature request: fixture graph",
            body=(
                "#### What's the problem this feature will solve?\n"
                "There is no graph view for fixture dependencies.\n\n"
                "#### Describe the solution you'd like\n"
                "Our proposed solution is a graph view that works in the terminal.\n\n"
                "#### Alternative Solutions\nNone.\n"
            ),
        )
    )

    assert [detail.name for detail in report.missing_details] == ["real-world use case"]


def test_feature_use_case_in_monorepo_context_is_not_requested_again() -> None:
    report = triage_issue(
        IssueUnderReview(
            title="Feature request: fixture graph",
            body=(
                "#### What's the problem this feature will solve?\n"
                "In a monorepo with 900 fixtures, a graph would show which fixture "
                "creates a cycle before CI times out.\n\n"
                "#### Describe the solution you'd like\n"
                "Show a fixture dependency graph.\n\n"
                "#### Alternative Solutions\nNone.\n"
            ),
        )
    )

    assert report.missing_details == []
