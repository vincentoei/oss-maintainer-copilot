"""Issue #48 regressions at the fixed and bounded report APIs."""

import asyncio
from datetime import UTC, datetime
from typing import Any, cast

import httpx2
import pytest

from maintainer_copilot.agent import AgentStepRequest
from maintainer_copilot.issue_search import IssueRecord, IssueSource
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.web import (
    app,
    get_agent_client,
    get_issue_source,
    get_model_client,
)


class SelectAllStatements:
    """Controlled isolation of supplied choices; never model-quality evidence."""

    def next_step(self, request: AgentStepRequest) -> object:
        if request.issue.number is not None and not request.observations:
            return {
                "tool": "search_earlier_issues",
                "arguments": {
                    "issue_number": request.issue.number,
                },
            }
        return {"tool": "finish", "arguments": {}}

    def generate(self, request: ModelRequest) -> object:
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": [s.citation_id for s in request.reply_statements],
        }


def report_for(
    title: str, body: str, endpoint: str, source: IssueSource | None = None
) -> dict[str, Any]:
    async def controlled_client() -> SelectAllStatements:
        return SelectAllStatements()

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post(
                endpoint,
                json={
                    "title": title,
                    "body": body,
                    "number": 500 if source else None,
                },
            )

    app.dependency_overrides[get_model_client] = controlled_client
    app.dependency_overrides[get_agent_client] = controlled_client
    if source is not None:

        async def issue_source() -> IssueSource:
            return source

        app.dependency_overrides[get_issue_source] = issue_source
    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_package_table_without_a_pip_heading_is_supplied(endpoint: str) -> None:
    report = report_for(
        "Bug: fixture lookup fails",
        "Fixture lookup fails while collecting this module.\n"
        "```\nPackage     Version\n----------- -------\n"
        "pluggy      1.4.0\npytest      8.1.1\n```\n"
        "pytest 8.1.1 on Ubuntu 22.04\n"
        "```python\ndef test_lookup():\n    assert False\n```",
        endpoint,
    )
    assert report["missing_details"] == []
    assert "pip list" not in report["draft_reply"]


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_conflicting_versions_get_a_targeted_clarification(endpoint: str) -> None:
    report = report_for(
        "ExceptionGroup traceback grows between tests",
        "My session fixture raises ExceptionGroup and the traceback grows.\n"
        "pip list:\npytest 8.1.1\npluggy 1.4.0\nmacOS 14.3\n"
        "platform darwin -- Python 3.12.0, pytest-8.0.0, pluggy-1.3.0\n"
        "def test_one():\n    pass\n",
        endpoint,
        EarlierIssues([]),
    )
    assert "which pytest/pluggy versions produced" in report["draft_reply"]
    assert "8.1.1" in report["draft_reply"]
    assert "8.0.0" in report["draft_reply"]


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
@pytest.mark.parametrize(
    ("problem", "solution", "missing"),
    [
        (
            "I'm currently writing tests that use Windows and POSIX paths to check "
            "cross-platform behavior. I'm making use of `pytest.mark.skipif` and "
            "copy my tests because only parameters differ.",
            "Allow conditional parametrization.",
            [],
        ),
        (
            "CI systems rely on Bash scripts and passing quotes into bash is tricky.",
            "Allow marker negation without quotation marks.",
            ["alternative solutions"],
        ),
        (
            "The documentation does not specify the TOML shapes of addopts. "
            "For example `addopts = ['--verbose', '-p no:cov']` is confusing.",
            "Document accepted configuration types on the configuration-options page.",
            ["alternative solutions"],
        ),
        (
            "I want to run selected subsets of tests to investigate dependencies "
            "between tests.",
            "Read selected test names from a file.",
            ["alternative solutions"],
        ),
    ],
)
def test_concrete_feature_scenarios_are_acknowledged(
    endpoint: str, problem: str, solution: str, missing: list[str]
) -> None:
    report = report_for(
        "Feature: improve test workflows",
        "What's the problem this feature will solve?\n"
        + problem
        + "\nDescribe the solution you'd like\n"
        + solution
        + "\nAlternative Solutions\n",
        endpoint,
    )
    assert [d["name"] for d in report["missing_details"]] == missing
    assert "real-world use case" not in report["draft_reply"]


class EarlierIssues:
    def __init__(self, candidates: list[IssueRecord]) -> None:
        self.candidates = candidates

    def get_issue(self, number: int) -> IssueRecord:
        return IssueRecord(
            number, "Opening", "Opening", datetime(2024, 5, 1, tzinfo=UTC)
        )

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        return self.candidates


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_template_overlap_does_not_link_session_control_to_argument_files(
    endpoint: str,
) -> None:
    source = EarlierIssues(
        [
            IssueRecord(
                400,
                "Read test selection arguments from a file",
                "What's the problem this feature will solve?\n"
                "Passing a long list of files into the pytest CLI is confusing.\n"
                "Describe the solution you'd like\n"
                "Read each argument from a text file.\n"
                "Alternative Solutions\nPass the list through the CLI.",
                datetime(2024, 4, 1, tzinfo=UTC),
            )
        ]
    )
    report = report_for(
        "More granular scripting interface",
        "What's the problem this feature will solve?\n"
        "Our project calls pytest.main for each file in Pyodide. Session fixtures "
        "initialize again for every call.\nDescribe the solution you'd like\n"
        "Expose session start, run_test and end APIs.\nAlternative Solutions\n"
        "Currently restart Pyodide per file.",
        endpoint,
        source,
    )
    assert report["duplicate_candidates"] == []
    assert report["related_issues"] == []


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_fixture_parameter_connection_explains_both_requests(endpoint: str) -> None:
    source = EarlierIssues(
        [
            IssueRecord(
                400,
                "Using fixtures in pytest.mark.parametrize",
                "@pytest.mark.parametrize('arg', [a, b])\n"
                "The test receives the fixture function instead of its value. "
                "I can work around it with a meta fixture.",
                datetime(2024, 4, 1, tzinfo=UTC),
            )
        ]
    )
    report = report_for(
        "Feature: fixture-derived parameter values",
        "The configuration comes from a session fixture. "
        "Please add pytest.mark.parametrize parameters_fixture support "
        "so the fixture supplies parameter values.",
        endpoint,
        source,
    )
    matches = report["duplicate_candidates"] + report["related_issues"]
    assert [s["issue_number"] for s in matches] == [400]
    assert "fixture-derived parameter values" in matches[0]["reason"]
    assert "session" in matches[0]["reason"]
    assert "fixture function" in matches[0]["reason"]
    assert "Shared topic:" not in report["draft_reply"]


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
@pytest.mark.parametrize(
    ("body", "expected"),
    [
        (
            "Scenario 1 with hardcoded values: parametrize scope='class'.\n"
            "pytest-8.1.1\nScenario 2 uses variables: parametrize scope='class'.\n"
            "pytest-7.4.4\nThe tuple values are printed in a different order.",
            "same pytest version and identical tuple values",
        ),
        (
            "setUpModule is not called in the ported project.\n"
            "Interestingly, the hook does seem to be honored in a minimized example.\n"
            "def test_ok():\n    pass\n",
            "minimized failing example",
        ),
    ],
)
def test_supported_comparison_is_available_without_claiming_a_root_cause(
    endpoint: str,
    body: str,
    expected: str,
) -> None:
    report = report_for(
        "Investigate reported behavior", body, endpoint, EarlierIssues([])
    )
    assert expected in report["draft_reply"]
    assert "root cause" not in report["draft_reply"]
    cited_ids = [c["id"] for c in report["citations"] if c["passage"]]
    assert cited_ids
    assert any(f"[{cid}]" in report["draft_reply"] for cid in cited_ids)


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_insufficient_evidence_does_not_invent_an_investigation(endpoint: str) -> None:
    report = report_for(
        "Unexpected behavior", "It behaves differently.", endpoint, EarlierIssues([])
    )
    assert "cannot substantiate" in report["draft_reply"]
    assert any(a["field"] == "draft_reply" for a in report["abstentions"])


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_genuinely_absent_packages_stay_missing(endpoint: str) -> None:
    report = report_for(
        "Bug: collection fails",
        "The suite errors while collecting tests.\nPackage Version\n--- ---\n"
        "pytest 8.1.1 on Ubuntu 22.04\n",
        endpoint,
    )
    assert "pip list output" in [d["name"] for d in report["missing_details"]]


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_deliberate_version_comparison_is_not_called_conflicting(endpoint: str) -> None:
    report = report_for(
        "Collection changed after upgrade",
        "With pytest 7 the command collects three tests; with pytest 8 only one.\n"
        "platform linux -- Python 3.12, pytest-7.0.0, pluggy-1.4.0\n"
        "platform linux -- Python 3.12, pytest-8.0.2, pluggy-1.4.0\n",
        endpoint,
        EarlierIssues([]),
    )
    assert "conflicting" not in report["draft_reply"]


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_common_assertion_error_does_not_establish_a_relationship(
    endpoint: str,
) -> None:
    report = report_for(
        "JUnit message attribute is too large",
        "The parser crashes on a large XML attribute. AssertionError: huge diff.",
        endpoint,
        EarlierIssues(
            [
                IssueRecord(
                    400,
                    "Capture output disappears",
                    "AssertionError after capfd.readouterr().",
                    datetime(2024, 4, 1, tzinfo=UTC),
                )
            ]
        ),
    )
    assert report["related_issues"] == []


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_untrusted_model_cannot_add_a_diagnosis_to_follow_up(
    endpoint: str,
) -> None:
    class UnsupportedDiagnosis(SelectAllStatements):
        def generate(self, request: ModelRequest) -> object:
            return {
                "issue_type": None,
                "issue_type_quote": None,
                "reply_citation_ids": ["C999"],
                "diagnosis": "The fixture cache is broken.",
            }

    async def controlled_client() -> UnsupportedDiagnosis:
        return UnsupportedDiagnosis()

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post(
                endpoint,
                json={
                    "title": "Unexpected output",
                    "body": "pytest 8.1.1\npluggy 1.4.0\npytest-8.0.0, pluggy-1.3.0",
                    "number": 500,
                },
            )

    async def issues() -> IssueSource:
        return EarlierIssues([])

    app.dependency_overrides[get_model_client] = controlled_client
    app.dependency_overrides[get_agent_client] = controlled_client
    app.dependency_overrides[get_issue_source] = issues
    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    report = response.json()
    assert report["status"] == "partial"
    assert "fixture cache is broken" not in report["draft_reply"]
    assert "C999" not in report["draft_reply"]
    assert any("validation" in a["reason"] for a in report["abstentions"])
