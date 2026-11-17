"""Issue #6 behavior at the report API with controlled model responses."""

import asyncio
from typing import Any, cast

import httpx2
import pytest

from maintainer_copilot.documentation import (
    DocumentationPassage,
    DocumentationSource,
    DocumentationTopic,
)
from maintainer_copilot.model import ModelUnavailable
from maintainer_copilot.web import (
    app,
    get_documentation_source,
    get_model_client,
)


class FixedModel:
    def __init__(self, response: object | Exception) -> None:
        self.response = response
        self.requests: list[object] = []

    def generate(self, request: object) -> object:
        self.requests.append(request)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def report_for(
    model: FixedModel, title: str = "Bug: collection fails"
) -> dict[str, Any]:
    async def fixed_model() -> FixedModel:
        return model

    app.dependency_overrides[get_model_client] = fixed_model

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
        ) as client:
            return await client.post(
                "/api/triage",
                json={"title": title, "body": ""},
            )

    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def test_model_suggests_type_and_selects_cited_reply_claim() -> None:
    model = FixedModel(
        {
            "issue_type": "type: bug",
            "issue_type_quote": "Bug: collection fails",
            "reply_citation_ids": ["C1", "C2", "C3", "C4"],
        }
    )

    report = report_for(model)

    assert report["issue_type"] == "type: bug"
    assert report["issue_type_quote"] == "Bug: collection fails"
    assert "[C1]" in report["draft_reply"]
    assert report["citations"][0]["id"] == "C1"
    assert not any(item["field"] == "issue_type" for item in report["abstentions"])
    assert len(model.requests) == 1


def test_model_reply_can_select_verified_documentation_evidence() -> None:
    class ApprovedDocumentation:
        def get_passage(self, topic: DocumentationTopic) -> DocumentationPassage:
            return DocumentationPassage(topic.url, topic.passage)

    async def fixed_documentation() -> DocumentationSource:
        return ApprovedDocumentation()

    app.dependency_overrides[get_documentation_source] = fixed_documentation
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: bug",
                "issue_type_quote": "Bug: capsys fails",
                "reply_citation_ids": ["C1", "C2", "C3", "C4", "C5"],
            }
        ),
        title="Bug: capsys fails",
    )

    assert "pytest documents" in report["draft_reply"]
    assert "[C5]" in report["draft_reply"]
    assert report["documentation_claims"][0]["citation_id"] == "C5"
    assert report["citations"][4]["passage"]


def test_model_accepts_other_pytest_type_when_issue_quote_supports_it() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: docs",
                "issue_type_quote": "Docs: clarify collection guide",
                "reply_citation_ids": [],
            }
        ),
        title="Docs: clarify collection guide",
    )

    assert report["issue_type"] == "type: docs"
    assert report["issue_type_quote"] == "Docs: clarify collection guide"


@pytest.mark.parametrize(
    "response",
    [
        {
            "issue_type": "type: bug",
            "issue_type_quote": "Bug: collection fails",
            "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            "draft_reply": "Pytest 99 fixes this issue. [C1]",
        },
        {
            "issue_type": "type: bug",
            "issue_type_quote": "Bug: collection fails",
            "reply_citation_ids": ["C1", "C2", "C3", "C4", "C99"],
        },
        {
            "issue_type": "type: bug",
            "issue_type_quote": "Bug: collection fails on Windows",
            "reply_citation_ids": ["C1", "C2", "C3", "C4"],
        },
        {
            "issue_type": "type: imaginary",
            "issue_type_quote": "Bug: collection fails",
            "reply_citation_ids": ["C1", "C2", "C3", "C4"],
        },
        {
            "issue_type": "type: docs",
            "issue_type_quote": "Bug: collection fails",
            "reply_citation_ids": ["C1", "C2", "C3", "C4"],
        },
    ],
)
def test_invalid_model_output_abstains_without_displaying_claims(
    response: object,
) -> None:
    report = report_for(FixedModel(response))

    assert report["issue_type"] is None
    assert "Pytest 99" not in report["draft_reply"]
    assert "[C99]" not in report["draft_reply"]
    assert any(
        item["field"] == "issue_type" and "failed validation" in item["reason"]
        for item in report["abstentions"]
    )
    assert not any(item["field"] == "draft_reply" for item in report["abstentions"])


def test_model_failure_keeps_cited_template_reply_and_abstains() -> None:
    report = report_for(FixedModel(ModelUnavailable("model offline")))

    assert report["issue_type"] is None
    assert "[C1]" in report["draft_reply"]
    assert any(
        item["field"] == "issue_type" and "unavailable" in item["reason"]
        for item in report["abstentions"]
    )
    assert not any(item["field"] == "draft_reply" for item in report["abstentions"])


def test_model_can_abstain_on_issue_type() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": None,
                "issue_type_quote": None,
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        )
    )

    assert report["issue_type"] is None
    assert report["issue_type_quote"] is None
    assert "[C1]" in report["draft_reply"]
    assert any(item["field"] == "issue_type" for item in report["abstentions"])


def test_model_abstains_from_reply_when_no_supported_claim_exists() -> None:
    report = report_for(
        FixedModel(
            {"issue_type": None, "issue_type_quote": None, "reply_citation_ids": []}
        ),
        title="Question about collection",
    )

    assert report["citations"] == []
    assert "cannot substantiate" in report["draft_reply"]
    assert any(item["field"] == "draft_reply" for item in report["abstentions"])


def test_negated_type_cue_does_not_ground_a_suggestion() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: bug",
                "issue_type_quote": "No bug found",
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        ),
        title="No bug found",
    )

    assert report["issue_type"] is None
    assert any(item["field"] == "issue_type" for item in report["abstentions"])


def test_branch_routing_label_is_not_an_issue_type_suggestion() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: feature-branch",
                "issue_type_quote": "Feature request: add fixture",
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        ),
        title="Feature request: add fixture",
    )

    assert report["issue_type"] is None
    assert any(item["field"] == "issue_type" for item in report["abstentions"])


def test_postcue_negation_does_not_ground_a_suggestion() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: bug",
                "issue_type_quote": "Bug is not present",
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        ),
        title="Bug is not present",
    )

    assert report["issue_type"] is None
    assert any(item["field"] == "issue_type" for item in report["abstentions"])


def test_cropped_quote_cannot_hide_negation_in_issue_text() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: bug",
                "issue_type_quote": "bug",
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        ),
        title="Feature request, not a bug",
    )

    assert report["issue_type"] is None
    assert any(item["field"] == "issue_type" for item in report["abstentions"])


def test_short_quote_in_positive_issue_context_can_support_type() -> None:
    report = report_for(
        FixedModel(
            {
                "issue_type": "type: bug",
                "issue_type_quote": "Bug",
                "reply_citation_ids": ["C1", "C2", "C3", "C4"],
            }
        )
    )

    assert report["issue_type"] == "type: bug"
    assert report["issue_type_quote"] == "Bug"


def test_unexpected_replacement_model_failure_returns_cited_report() -> None:
    report = report_for(FixedModel(RuntimeError("model process exited")))

    assert report["issue_type"] is None
    assert "[C1]" in report["draft_reply"]
    assert any(
        item["field"] == "issue_type" and "unavailable" in item["reason"]
        for item in report["abstentions"]
    )
