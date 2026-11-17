"""Issue #9 trace inspection through the public report and trace APIs."""

import asyncio
import json
from datetime import UTC, datetime
from io import BytesIO
from typing import Any, cast
from uuid import uuid4

import httpx2
import pytest

from maintainer_copilot import model as model_module
from maintainer_copilot.issue_search import IssueRecord, IssueSearchError
from maintainer_copilot.model import ModelRequest, ModelResponse, OpenAICompatibleModel
from maintainer_copilot.web import (
    app,
    get_agent_client,
    get_issue_source,
    get_model_client,
)

TITLE = "Bug: FixtureLookupError with indirect parametrization"
BODY = (
    "FixtureLookupError when an indirect parametrized fixture uses a session fixture."
)


class FixedIssues:
    def get_issue(self, number: int) -> IssueRecord:
        return IssueRecord(number, TITLE, BODY, datetime(2024, 5, 10, tzinfo=UTC))

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        return [IssueRecord(410, TITLE, BODY, datetime(2024, 5, 8, tzinfo=UTC))]


class FixedModel:
    def generate(self, request: ModelRequest) -> object:
        return {
            "issue_type": "type: bug",
            "issue_type_quote": TITLE,
            "reply_citation_ids": [
                statement.citation_id for statement in request.reply_statements
            ],
        }


def report_and_trace(
    issues: object, model: object
) -> tuple[dict[str, Any], dict[str, Any], str]:
    async def fixed_issues() -> object:
        return issues

    async def fixed_model() -> object:
        return model

    app.dependency_overrides[get_issue_source] = fixed_issues
    app.dependency_overrides[get_model_client] = fixed_model

    async def request() -> tuple[httpx2.Response, httpx2.Response, httpx2.Response]:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            report = await client.post(
                "/api/triage", json={"number": 500, "title": TITLE, "body": BODY}
            )
            trace_id = report.json()["trace_id"]
            trace = await client.get(f"/api/traces/{trace_id}")
            page = await client.get("/")
            return report, trace, page

    try:
        report, trace, page = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert report.status_code == trace.status_code == page.status_code == 200
    return (
        cast(dict[str, Any], report.json()),
        cast(dict[str, Any], trace.json()),
        page.text,
    )


def test_report_trace_records_successful_retrieval_and_model_calls() -> None:
    report, trace, page = report_and_trace(FixedIssues(), FixedModel())

    assert report["status"] == "complete"
    assert report["duplicate_candidates"][0]["issue_number"] == 410
    assert trace["trace_id"] == report["trace_id"]
    assert trace["status"] == "complete"
    assert {(item["kind"], item["name"]) for item in trace["events"]} >= {
        ("retrieval", "get_issue"),
        ("retrieval", "search_issues"),
        ("model", "triage_selection"),
    }
    assert all(item["duration_ms"] >= 0 for item in trace["events"])
    assert all(item["started_ms"] >= 0 for item in trace["events"])
    assert all(item["status"] == "ok" for item in trace["events"])
    assert any(
        item["name"] == "search_issues"
        and item["result_count"] == 1
        and "OR" in item["target"]
        and "https://github.com/pytest-dev/pytest/issues/410" in item["references"]
        for item in trace["events"]
    )
    assert any(
        item["name"] == "triage_selection" and item["target"] == "FixedModel"
        for item in trace["events"]
    )
    assert 'id="trace-link"' in page
    assert 'id="trace-events"' in page


def test_failed_lookup_returns_partial_report_and_sanitized_trace_error() -> None:
    class FailedIssues(FixedIssues):
        def search_issues(
            self, query: str, created_before: datetime
        ) -> list[IssueRecord]:
            raise IssueSearchError("private upstream detail")

    report, trace, _ = report_and_trace(FailedIssues(), FixedModel())

    assert report["status"] == trace["status"] == "partial"
    assert report["duplicate_candidates"] == report["related_issues"] == []
    assert {"duplicate_candidates", "related_issues"}.issubset(
        {item["field"] for item in report["abstentions"]}
    )
    failed = [item for item in trace["events"] if item["status"] == "error"]
    assert [(item["kind"], item["name"]) for item in failed] == [
        ("retrieval", "search_issues")
    ]
    assert "private upstream detail" not in str(trace)


def test_wrong_issue_lookup_abstains_instead_of_citing_unrelated_results() -> None:
    class WrongIssues(FixedIssues):
        def get_issue(self, number: int) -> IssueRecord:
            return IssueRecord(501, TITLE, BODY, datetime(2024, 5, 10, tzinfo=UTC))

    report, trace, _ = report_and_trace(WrongIssues(), FixedModel())

    assert report["status"] == "partial"
    assert report["duplicate_candidates"] == []
    assert any(
        item["name"] == "get_issue" and item["status"] == "error"
        for item in trace["events"]
    )


def test_failed_model_returns_partial_report_without_unsupported_type() -> None:
    class FailedModel:
        def generate(self, request: ModelRequest) -> object:
            raise RuntimeError("private model detail")

    report, trace, _ = report_and_trace(FixedIssues(), FailedModel())

    assert report["status"] == trace["status"] == "partial"
    assert report["issue_type"] is None
    assert report["issue_type_quote"] is None
    assert report["duplicate_candidates"][0]["issue_number"] == 410
    assert any(item["field"] == "issue_type" for item in report["abstentions"])
    failed = [item for item in trace["events"] if item["status"] == "error"]
    assert [(item["kind"], item["name"]) for item in failed] == [
        ("model", "triage_selection")
    ]
    assert "private model detail" not in str(trace)


def test_trace_includes_available_model_token_counts() -> None:
    class MeteredModel(FixedModel):
        def generate(self, request: ModelRequest) -> object:
            return ModelResponse(super().generate(request), 37, 12)

    report, trace, _ = report_and_trace(FixedIssues(), MeteredModel())

    assert report["status"] == "complete"
    model_call = next(item for item in trace["events"] if item["kind"] == "model")
    assert model_call["input_tokens"] == 37
    assert model_call["output_tokens"] == 12


class FixedAgent(FixedModel):
    def __init__(self) -> None:
        self.steps = 0

    def next_step(self, request: object) -> object:
        self.steps += 1
        if self.steps == 1:
            return ModelResponse(
                {"tool": "search_earlier_issues", "arguments": {"issue_number": 500}},
                20,
                5,
            )
        return {"tool": "finish", "arguments": {}}


def agent_report_and_trace(issues: object) -> tuple[dict[str, Any], dict[str, Any]]:
    async def fixed_issues() -> object:
        return issues

    async def fixed_agent() -> object:
        return FixedAgent()

    app.dependency_overrides[get_issue_source] = fixed_issues
    app.dependency_overrides[get_agent_client] = fixed_agent

    async def request() -> tuple[httpx2.Response, httpx2.Response]:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            report = await client.post(
                "/api/agent/triage",
                json={"number": 500, "title": TITLE, "body": BODY},
            )
            trace = await client.get(f"/api/traces/{report.json()['trace_id']}")
            return report, trace

    try:
        report, trace = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert report.status_code == trace.status_code == 200
    return cast(dict[str, Any], report.json()), cast(dict[str, Any], trace.json())


def test_agent_trace_records_tool_actions_and_model_decisions() -> None:
    report, trace = agent_report_and_trace(FixedIssues())

    assert report["status"] == trace["status"] == "complete"
    assert report["duplicate_candidates"][0]["issue_number"] == 410
    assert ("tool", "search_earlier_issues") in {
        (item["kind"], item["name"]) for item in trace["events"]
    }
    decisions = [item for item in trace["events"] if item["name"] == "agent_action"]
    assert len(decisions) == 2
    assert decisions[0]["input_tokens"] == 20
    assert decisions[0]["output_tokens"] == 5
    assert all(item["target"] == "FixedAgent" for item in decisions)


def test_failed_agent_tool_is_visible_and_report_is_partial() -> None:
    class FailedIssues(FixedIssues):
        def search_issues(
            self, query: str, created_before: datetime
        ) -> list[IssueRecord]:
            raise IssueSearchError("private upstream detail")

    report, trace = agent_report_and_trace(FailedIssues())

    assert report["status"] == trace["status"] == "partial"
    assert report["duplicate_candidates"] == []
    assert any(
        item["field"] == "duplicate_candidates" for item in report["abstentions"]
    )
    assert any(
        item["kind"] == "tool"
        and item["name"] == "search_earlier_issues"
        and item["status"] == "error"
        for item in trace["events"]
    )


def test_openai_compatible_response_preserves_available_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    envelope = {
        "choices": [{"message": {"content": json.dumps({"tool": "finish"})}}],
        "usage": {"prompt_tokens": 31, "completion_tokens": 7},
    }
    monkeypatch.setattr(
        model_module,
        "urlopen",
        lambda request, timeout: BytesIO(json.dumps(envelope).encode()),
    )

    response = OpenAICompatibleModel(
        "http://example.test/v1", "controlled"
    ).generate_json("Select an action.", {}, max_tokens=20)

    assert response == ModelResponse({"tool": "finish"}, 31, 7)


def test_unknown_trace_reference_returns_not_found() -> None:
    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.get(f"/api/traces/{uuid4()}")

    response = asyncio.run(request())

    assert response.status_code == 404


def test_malformed_model_content_still_records_provider_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    envelope = {
        "choices": [{"message": {"content": "invalid JSON"}}],
        "usage": {"prompt_tokens": 23, "completion_tokens": 4},
    }
    monkeypatch.setattr(
        model_module,
        "urlopen",
        lambda request, timeout: BytesIO(json.dumps(envelope).encode()),
    )

    async def fixed_model() -> OpenAICompatibleModel:
        return OpenAICompatibleModel("http://example.test/v1", "controlled")

    app.dependency_overrides[get_model_client] = fixed_model

    async def request() -> tuple[httpx2.Response, httpx2.Response]:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            report = await client.post(
                "/api/triage", json={"title": TITLE, "body": BODY}
            )
            trace = await client.get(f"/api/traces/{report.json()['trace_id']}")
            return report, trace

    try:
        report, trace = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()

    assert report.status_code == trace.status_code == 200
    assert report.json()["status"] == "partial"
    assert report.json()["issue_type"] is None
    model_call = next(
        item for item in trace.json()["events"] if item["name"] == "triage_selection"
    )
    assert model_call["status"] == "error"
    assert model_call["target"] == "controlled"
    assert (model_call["input_tokens"], model_call["output_tokens"]) == (23, 4)
