"""Issue #8: linked CI evidence through the report's public API."""

import asyncio
import json
from email.message import Message
from io import BytesIO
from typing import Any, cast
from urllib.error import HTTPError
from urllib.request import Request

import httpx2
import pytest
from pydantic import HttpUrl

from maintainer_copilot.agent import AgentStepRequest
from maintainer_copilot.ci import (
    CheckResult,
    CIInspection,
    CILink,
    CIUnavailable,
    PublicCISource,
    linked_target,
)
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.triage import IssueUnderReview, TriageReport, triage_issue
from maintainer_copilot.web import (
    app,
    get_agent_client,
    get_ci_source,
    get_model_client,
)

COMMIT = "36eed6b7b0eb59760fc4b33e90bdaac5057388f0"
PR_URL = "https://github.com/pytest-dev/pytest/pull/123"
COMMIT_URL = f"https://github.com/pytest-dev/pytest/commit/{COMMIT}"


def check(name: str, conclusion: str, run_id: int) -> CheckResult:
    return CheckResult(
        name=name,
        conclusion=conclusion,
        commit=COMMIT,
        url=HttpUrl(
            f"https://github.com/pytest-dev/pytest/actions/runs/77/job/{run_id}"
        ),
    )


class FixedCI:
    def __init__(
        self,
        checks: list[CheckResult] | None = None,
        fail: bool = False,
        partial: bool = False,
    ):
        self.checks = checks or []
        self.fail = fail
        self.partial = partial
        self.reads: list[CILink] = []

    def get_checks(self, link: CILink) -> CIInspection:
        self.reads.append(link)
        if self.fail:
            raise CIUnavailable("fixture failure")
        return CIInspection(tuple(self.checks), partial=self.partial)


class ControlledModel:
    def __init__(self) -> None:
        self.requests: list[ModelRequest] = []

    def generate(self, request: ModelRequest) -> object:
        self.requests.append(request)
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": [
                item.citation_id for item in request.reply_statements
            ],
        }


class ControlledAgent(ControlledModel):
    def __init__(self) -> None:
        super().__init__()
        self.steps: list[AgentStepRequest] = []

    def next_step(self, request: AgentStepRequest) -> object:
        self.steps.append(request)
        return {"tool": "finish", "arguments": {}}


def report_for(
    body: str,
    ci_source: FixedCI,
    model: ControlledModel | None = None,
    endpoint: str = "/api/triage",
) -> dict[str, Any]:
    model = model or ControlledModel()

    async def fixed_ci() -> FixedCI:
        return ci_source

    async def fixed_model() -> ControlledModel:
        return model

    app.dependency_overrides[get_ci_source] = fixed_ci
    app.dependency_overrides[get_model_client] = fixed_model
    app.dependency_overrides[get_agent_client] = fixed_model

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            return await client.post(
                endpoint,
                json={"title": "CI diagnostic", "body": body},
            )

    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


@pytest.mark.parametrize(
    ("body", "link"),
    [
        (f"Relevant PR: {PR_URL}", CILink("pull", "123")),
        (f"Upstream PR: {PR_URL}; do not ignore its checks.", CILink("pull", "123")),
        (f"Relevant commit: {COMMIT_URL}", CILink("commit", COMMIT)),
    ],
)
def test_linked_pr_or_commit_yields_specific_cited_result(
    body: str, link: CILink
) -> None:
    source = FixedCI([check("linux tests", "failure", 42)])
    model = ControlledModel()

    report = report_for(body, source, model)

    TriageReport.model_validate(report)
    assert source.reads == [link]
    assert report["ci_results"] == [
        {
            "check_name": "linux tests",
            "conclusion": "failure",
            "commit": COMMIT,
            "citation_id": "C1",
        }
    ]
    assert report["citations"] == [
        {
            "id": "C1",
            "source_url": "https://github.com/pytest-dev/pytest/actions/runs/77/job/42",
            "description": "pytest CI check: linux tests",
            "passage": f"linux tests: failure at commit {COMMIT}",
            "source_location": None,
        }
    ]
    assert "CI" not in report["draft_reply"]
    assert model.requests[0].reply_statements == ()


@pytest.mark.parametrize(
    "body",
    [
        "Collection fails without a linked change.",
        "Unrelated PR: https://github.com/another/project/pull/123",
        f"For historical context, see {PR_URL}; it predates this regression.",
        f"Do not use {PR_URL}; it is unrelated.",
        f"Do not use\n{PR_URL}",
        f"PR: {PR_URL}\nis unrelated.",
        f"Two possible links: {PR_URL} and {COMMIT_URL}",
    ],
)
def test_unlinked_or_ambiguous_issue_never_reads_ci(body: str) -> None:
    source = FixedCI([check("linux tests", "success", 42)])

    report = report_for(body, source)

    assert source.reads == []
    assert report["ci_results"] == []
    assert not any(item["field"] == "ci_results" for item in report["abstentions"])


@pytest.mark.parametrize("source", [FixedCI(fail=True), FixedCI()])
def test_linked_unavailable_ci_abstains_without_a_result(source: FixedCI) -> None:
    report = report_for(PR_URL, source)

    assert source.reads == [CILink("pull", "123")]
    assert report["ci_results"] == []
    assert report["citations"] == []
    assert any(item["field"] == "ci_results" for item in report["abstentions"])
    assert "CI check" not in report["draft_reply"]


def test_partial_ci_evidence_is_cited_with_an_abstention() -> None:
    source = FixedCI([check("PR merge tests", "success", 43)], partial=True)

    report = report_for(PR_URL, source)

    assert report["ci_results"][0]["check_name"] == "PR merge tests"
    assert report["citations"][0]["source_url"].endswith("/job/43")
    assert any(
        item["field"] == "ci_results" and "Some" in item["reason"]
        for item in report["abstentions"]
    )


def test_conflicting_checks_remain_separate_without_overall_verdict() -> None:
    source = FixedCI(
        [check("linux tests", "failure", 42), check("linux tests", "success", 43)]
    )

    report = report_for(COMMIT_URL, source)

    assert [item["conclusion"] for item in report["ci_results"]] == [
        "failure",
        "success",
    ]
    assert [item["citation_id"] for item in report["ci_results"]] == ["C1", "C2"]
    assert [item["source_url"] for item in report["citations"]] == [
        "https://github.com/pytest-dev/pytest/actions/runs/77/job/42",
        "https://github.com/pytest-dev/pytest/actions/runs/77/job/43",
    ]
    assert "CI" not in report["draft_reply"]


def test_ci_result_must_match_evidence_read_for_this_report() -> None:
    source = FixedCI([check("linux tests", "failure", 42)])
    report = triage_issue(
        IssueUnderReview(title="CI diagnostic", body=COMMIT_URL),
        model_client=ControlledModel(),
        ci_source=source,
    )

    report.ci_results[0].conclusion = "success"
    with pytest.raises(ValueError, match="not supplied"):
        report.validate_ci_evidence(source.checks)


def test_bounded_agent_report_uses_only_explicit_link_for_ci() -> None:
    source = FixedCI([check("linux tests", "success", 42)])
    agent = ControlledAgent()

    linked = report_for(PR_URL, source, agent, "/api/agent/triage")
    unlinked = report_for("No linked change.", source, agent, "/api/agent/triage")

    assert len(linked["ci_results"]) == 1
    assert unlinked["ci_results"] == []
    assert source.reads == [CILink("pull", "123")]
    assert len(agent.steps) == 2
    assert all(step.observations == () for step in agent.steps)


def test_web_page_renders_each_ci_result_with_its_citation() -> None:
    async def get_page() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.get("/")

    page = asyncio.run(get_page())

    assert page.status_code == 200
    assert '<ul id="ci-results"' in page.text
    assert 'fillList("ci-results", report.ci_results' in page.text
    assert "link.href = citation.source_url" in page.text
    assert "result.check_name" in page.text
    assert "result.conclusion" in page.text


def test_public_source_resolves_pr_head_and_cites_verified_check_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested: list[str] = []
    payloads = [
        {"head": {"sha": COMMIT}},
        {
            "total_count": 1,
            "check_runs": [
                {
                    "id": 42,
                    "name": "linux tests",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": COMMIT,
                    "html_url": "https://github.com/pytest-dev/pytest/actions/runs/77/job/42",
                }
            ],
        },
    ]

    def fetch(request: Request, timeout: int) -> BytesIO:
        requested.append(request.full_url)
        assert timeout == 5
        return BytesIO(json.dumps(payloads[len(requested) - 1]).encode())

    monkeypatch.setattr("maintainer_copilot.ci.urlopen", fetch)

    results = PublicCISource().get_checks(CILink("pull", "123"))

    assert results == CIInspection((check("linux tests", "success", 42),))
    assert requested == [
        "https://api.github.com/repos/pytest-dev/pytest/pulls/123",
        f"https://api.github.com/repos/pytest-dev/pytest/commits/{COMMIT}/check-runs?per_page=100&filter=all",
    ]


def test_open_pr_includes_checks_on_its_test_merge_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merge_commit = "a" * 40
    requested: list[str] = []
    payloads = [
        {
            "state": "open",
            "head": {"sha": COMMIT},
            "merge_commit_sha": merge_commit,
        },
        {"total_count": 0, "check_runs": []},
        {
            "total_count": 1,
            "check_runs": [
                {
                    "id": 43,
                    "name": "PR merge tests",
                    "status": "completed",
                    "conclusion": "failure",
                    "head_sha": merge_commit,
                    "html_url": "https://github.com/pytest-dev/pytest/actions/runs/78/job/43",
                }
            ],
        },
    ]

    def fetch(request: Request, timeout: int) -> BytesIO:
        requested.append(request.full_url)
        return BytesIO(json.dumps(payloads[len(requested) - 1]).encode())

    monkeypatch.setattr("maintainer_copilot.ci.urlopen", fetch)

    results = PublicCISource().get_checks(CILink("pull", "123"))

    assert results == CIInspection(
        (
            CheckResult(
                name="PR merge tests",
                conclusion="failure",
                commit=merge_commit,
                url=HttpUrl(
                    "https://github.com/pytest-dev/pytest/actions/runs/78/job/43"
                ),
            ),
        )
    )
    assert requested == [
        "https://api.github.com/repos/pytest-dev/pytest/pulls/123",
        f"https://api.github.com/repos/pytest-dev/pytest/commits/{COMMIT}/check-runs?per_page=100&filter=all",
        f"https://api.github.com/repos/pytest-dev/pytest/commits/{merge_commit}/check-runs?per_page=100&filter=all",
    ]


def test_open_pr_keeps_merge_checks_when_head_lookup_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    merge_commit = "a" * 40
    requests = 0

    def fetch(request: Request, timeout: int) -> BytesIO:
        nonlocal requests
        requests += 1
        if requests == 1:
            return BytesIO(
                json.dumps(
                    {
                        "state": "open",
                        "head": {"sha": COMMIT},
                        "merge_commit_sha": merge_commit,
                    }
                ).encode()
            )
        if requests == 2:
            raise HTTPError(request.full_url, 404, "Not Found", Message(), None)
        return BytesIO(
            json.dumps(
                {
                    "total_count": 1,
                    "check_runs": [
                        {
                            "id": 43,
                            "name": "PR merge tests",
                            "status": "completed",
                            "conclusion": "success",
                            "head_sha": merge_commit,
                            "html_url": "https://github.com/pytest-dev/pytest/actions/runs/78/job/43",
                        }
                    ],
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.ci.urlopen", fetch)

    result = PublicCISource().get_checks(CILink("pull", "123"))

    assert result.partial is True
    assert [item.name for item in result.checks] == ["PR merge tests"]
    assert requests == 3


@pytest.mark.parametrize(
    "bad_run",
    [
        {"head_sha": "0" * 40},
        {"html_url": "https://evil.example/ci/42"},
        {"conclusion": ["success"]},
    ],
)
def test_public_source_rejects_unverified_results(
    monkeypatch: pytest.MonkeyPatch, bad_run: dict[str, object]
) -> None:
    run: dict[str, object] = {
        "id": 42,
        "name": "linux tests",
        "status": "completed",
        "conclusion": "success",
        "head_sha": COMMIT,
        "html_url": "https://github.com/pytest-dev/pytest/runs/42",
    }
    run.update(bad_run)
    monkeypatch.setattr(
        "maintainer_copilot.ci.urlopen",
        lambda request, timeout: BytesIO(
            json.dumps({"total_count": 1, "check_runs": [run]}).encode()
        ),
    )

    with pytest.raises(CIUnavailable):
        PublicCISource().get_checks(CILink("commit", COMMIT))


def test_public_source_rejects_incomplete_check_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "maintainer_copilot.ci.urlopen",
        lambda request, timeout: BytesIO(
            json.dumps({"total_count": 101, "check_runs": []}).encode()
        ),
    )

    with pytest.raises(CIUnavailable, match="incomplete"):
        PublicCISource().get_checks(CILink("commit", COMMIT))


@pytest.mark.parametrize(
    "link", [CILink("pull", "../secrets"), CILink("commit", "main")]
)
def test_public_source_rejects_invalid_targets_before_request(
    monkeypatch: pytest.MonkeyPatch, link: CILink
) -> None:
    def unexpected_fetch(request: Request, timeout: int) -> BytesIO:
        raise AssertionError("invalid target reached GitHub")

    monkeypatch.setattr("maintainer_copilot.ci.urlopen", unexpected_fetch)

    with pytest.raises(CIUnavailable, match="invalid"):
        PublicCISource().get_checks(link)


def test_link_parser_requires_one_complete_pytest_url() -> None:
    assert linked_target("", f"See ({PR_URL}) and {PR_URL}") == CILink("pull", "123")
    assert linked_target("", "Related PR: pytest-dev/pytest#123") == CILink(
        "pull", "123"
    )
    assert linked_target("", "pytest-dev/pytest#123") is None
    assert linked_target("", f"Do not use {PR_URL}; it is unrelated.") is None
    assert linked_target("", f"Do not use\n{PR_URL}") is None
    assert linked_target("", f"PR: {PR_URL}\nis unrelated.") is None
    assert linked_target(
        "", f"Unrelated background: prior bug. Relevant PR: {PR_URL}"
    ) == CILink("pull", "123")
    assert linked_target(
        "",
        "Unrelated PR: https://github.com/pytest-dev/pytest/pull/123\n"
        "Relevant PR: https://github.com/pytest-dev/pytest/pull/456",
    ) == CILink("pull", "456")
    assert linked_target("", f"{COMMIT_URL}x") is None
    assert linked_target("", f"{COMMIT_URL}.evil") is None
    assert linked_target("", f"{PR_URL}.evil") is None
    assert linked_target("", "PR pytest-dev/pytest#123.evil") is None
    assert linked_target("", f"https://evil.example/?next={PR_URL}") is None
