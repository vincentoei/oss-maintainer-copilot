"""Issue #3 behavior at the public report API seam."""

import asyncio
from datetime import UTC, datetime
from typing import Any, cast
from urllib.parse import parse_qs, urlsplit

import httpx2

from maintainer_copilot.issue_search import (
    GitHubIssueSource,
    IssueRecord,
    IssueSearchError,
    IssueSource,
)
from maintainer_copilot.web import app, get_issue_source

REVIEW_TITLE = "FixtureLookupError with indirect parametrization"
REVIEW_BODY = (
    "FixtureLookupError when an indirect parametrized fixture uses a session fixture."
)


class FixtureIssueSource:
    def __init__(self, candidates: list[IssueRecord]) -> None:
        self.candidates = candidates
        self.queries: list[tuple[str, datetime]] = []

    def get_issue(self, number: int) -> IssueRecord:
        assert number == 500
        return IssueRecord(
            number=500,
            title=REVIEW_TITLE,
            body=REVIEW_BODY,
            created_at=datetime(2024, 5, 10, tzinfo=UTC),
        )

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        self.queries.append((query, created_before))
        return self.candidates


def issue(number: int, title: str, body: str, day: int) -> IssueRecord:
    return IssueRecord(
        number=number,
        title=title,
        body=body,
        created_at=datetime(2024, 5, day, tzinfo=UTC),
    )


def report_for(source: IssueSource, title: str, body: str) -> dict[str, Any]:
    async def fixture_source() -> IssueSource:
        return source

    app.dependency_overrides[get_issue_source] = fixture_source

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post(
                "/api/triage", json={"number": 500, "title": title, "body": body}
            )

    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def test_duplicate_is_cited_and_self_and_later_issues_are_excluded() -> None:
    source = FixtureIssueSource(
        [
            issue(
                410,
                REVIEW_TITLE,
                REVIEW_BODY,
                8,
            ),
            issue(500, "Same issue", "Same issue", 10),
            issue(
                501,
                REVIEW_TITLE,
                REVIEW_BODY,
                11,
            ),
            issue(
                400,
                REVIEW_TITLE,
                REVIEW_BODY,
                12,
            ),
        ]
    )

    report = report_for(
        source,
        REVIEW_TITLE,
        REVIEW_BODY,
    )

    assert [item["issue_number"] for item in report["duplicate_candidates"]] == [410]
    candidate = report["duplicate_candidates"][0]
    assert "indirect" in candidate["reason"]
    assert candidate["url"] == "https://github.com/pytest-dev/pytest/issues/410"
    assert any(
        citation["id"] == candidate["citation_id"]
        and citation["source_url"] == candidate["url"]
        for citation in report["citations"]
    )
    assert source.queries and source.queries[0][1] == datetime(2024, 5, 10, tzinfo=UTC)


def test_related_issue_has_its_own_reason_and_citation() -> None:
    source = FixtureIssueSource(
        [
            issue(
                390,
                "FixtureLookupError in plugin fixture teardown",
                "FixtureLookupError occurs during fixture teardown in plugin hooks.",
                7,
            )
        ]
    )

    report = report_for(
        source,
        REVIEW_TITLE,
        REVIEW_BODY,
    )

    assert report["duplicate_candidates"] == []
    assert [item["issue_number"] for item in report["related_issues"]] == [390]
    related = report["related_issues"][0]
    assert "same failure or request is not established" in related["reason"]
    assert any(
        citation["id"] == related["citation_id"]
        and citation["source_url"] == related["url"]
        for citation in report["citations"]
    )
    assert " OR " in source.queries[0][0]


def test_negated_shared_condition_is_related_instead_of_duplicate() -> None:
    source = FixtureIssueSource(
        [
            issue(
                392,
                REVIEW_TITLE,
                "FixtureLookupError when an indirect parametrized fixture "
                "does not use a session fixture.",
                7,
            )
        ]
    )

    report = report_for(source, REVIEW_TITLE, REVIEW_BODY)

    assert report["duplicate_candidates"] == []
    assert [item["issue_number"] for item in report["related_issues"]] == [392]
    assert "negates" in report["related_issues"][0]["reason"]


def test_opposing_feature_requests_are_related_instead_of_duplicates() -> None:
    source = FixtureIssueSource(
        [
            issue(
                393,
                "Feature request: disable fixture caching",
                "Please disable fixture caching in repeated test runs.",
                7,
            )
        ]
    )

    report = report_for(
        source,
        "Feature request: enable fixture caching",
        "Please enable fixture caching in repeated test runs.",
    )

    assert report["duplicate_candidates"] == []
    assert [item["issue_number"] for item in report["related_issues"]] == [393]


def test_same_topic_with_different_fixture_scope_is_related() -> None:
    source = FixtureIssueSource(
        [
            issue(
                391,
                REVIEW_TITLE,
                "FixtureLookupError when an indirect parametrized fixture "
                "uses a function fixture.",
                7,
            )
        ]
    )

    report = report_for(source, REVIEW_TITLE, REVIEW_BODY)

    assert report["duplicate_candidates"] == []
    assert [item["issue_number"] for item in report["related_issues"]] == [391]
    assert "different fixture scopes" in report["related_issues"][0]["reason"]


def test_unrelated_search_result_is_not_suggested() -> None:
    source = FixtureIssueSource(
        [
            issue(
                380,
                "Assertion rewriting renders the wrong source line",
                "Rewritten assertions show the wrong source line in traceback output.",
                6,
            )
        ]
    )

    report = report_for(
        source,
        REVIEW_TITLE,
        REVIEW_BODY,
    )

    assert report["duplicate_candidates"] == []
    assert report["related_issues"] == []
    assert not {"duplicate_candidates", "related_issues"} & {
        item["field"] for item in report["abstentions"]
    }


def test_insufficient_issue_text_abstains_without_searching() -> None:
    source = FixtureIssueSource([])

    report = report_for(source, "Bug", "It fails.")

    assert source.queries == []
    assert report["duplicate_candidates"] == []
    assert report["related_issues"] == []
    assert {"duplicate_candidates", "related_issues"} <= {
        item["field"] for item in report["abstentions"]
    }


def test_duplicate_candidates_are_ranked_by_match_strength() -> None:
    source = FixtureIssueSource(
        [
            issue(
                360,
                REVIEW_TITLE + " on Windows",
                REVIEW_BODY + " This happens on Windows.",
                5,
            ),
            issue(350, REVIEW_TITLE, REVIEW_BODY, 4),
        ]
    )

    report = report_for(source, REVIEW_TITLE, REVIEW_BODY)

    assert [item["issue_number"] for item in report["duplicate_candidates"]] == [
        350,
        360,
    ]


def test_matching_feature_requests_can_be_duplicate_candidates() -> None:
    source = FixtureIssueSource(
        [
            issue(
                340,
                "Feature: fixture dependency graph",
                "Please add a fixture dependency graph for finding cycles "
                "in large suites.",
                3,
            )
        ]
    )

    report = report_for(
        source,
        "Feature request: display fixture dependency graph",
        "Please add a fixture dependency graph for finding cycles in large suites.",
    )

    assert [item["issue_number"] for item in report["duplicate_candidates"]] == [340]


def test_search_error_abstains_instead_of_claiming_no_matches() -> None:
    class UnavailableSource(FixtureIssueSource):
        def search_issues(
            self, query: str, created_before: datetime
        ) -> list[IssueRecord]:
            raise IssueSearchError("GitHub issue search is unavailable.")

    report = report_for(UnavailableSource([]), REVIEW_TITLE, REVIEW_BODY)

    assert report["duplicate_candidates"] == []
    assert report["related_issues"] == []
    assert {"duplicate_candidates", "related_issues"} <= {
        item["field"] for item in report["abstentions"]
    }


def test_api_search_includes_a_match_from_the_second_github_page() -> None:
    class PagedSource(GitHubIssueSource):
        def __init__(self) -> None:
            self.pages: list[int] = []

        def _get_json(self, url: str) -> dict[str, object]:
            if url.endswith("/issues/500"):
                return {
                    "number": 500,
                    "title": REVIEW_TITLE,
                    "body": REVIEW_BODY,
                    "created_at": "2024-05-10T00:00:00Z",
                }
            page = int(parse_qs(urlsplit(url).query).get("page", ["1"])[0])
            self.pages.append(page)
            unrelated = {
                "title": "Indirect assertion rewriting renders the wrong source line",
                "body": "Rewritten assertions show the wrong source line.",
                "created_at": "2024-05-01T00:00:00Z",
            }
            first_page = [{**unrelated, "number": number} for number in range(1, 101)]
            match = {
                "number": 410,
                "title": REVIEW_TITLE,
                "body": REVIEW_BODY,
                "created_at": "2024-05-08T00:00:00Z",
            }
            return {
                "total_count": 101,
                "incomplete_results": False,
                "items": first_page if page == 1 else [match],
            }

    source = PagedSource()

    report = report_for(source, REVIEW_TITLE, REVIEW_BODY)

    assert source.pages == [1, 2]
    assert [item["issue_number"] for item in report["duplicate_candidates"]] == [410]
