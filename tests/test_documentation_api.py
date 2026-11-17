"""Issue #4 behavior at the report API and evidence validation seams."""

import asyncio
from io import BytesIO
from typing import Any, cast

import httpx2
import pytest

from maintainer_copilot import TriageReport
from maintainer_copilot.documentation import (
    TOPICS,
    DocumentationEvidence,
    DocumentationPassage,
    DocumentationSource,
    DocumentationTopic,
    PytestDocumentationSource,
)
from maintainer_copilot.web import app, get_documentation_source

CAPTURE_URL = (
    "https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html"
    "#accessing-captured-output-from-a-test-function"
)
CAPTURE_PASSAGE = (
    "fixtures allow access to stdout/stderr output created during test execution."
)
SCOPE_URL = "https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes"
SCOPE_PASSAGE = (
    "Fixtures are created when first requested by a test, and are destroyed "
    "based on their scope"
)


class FixedDocumentationSource:
    def __init__(self, passages: dict[str, DocumentationPassage]) -> None:
        self.passages = passages
        self.requested: list[str] = []

    def get_passage(self, topic: DocumentationTopic) -> DocumentationPassage | None:
        self.requested.append(topic.key)
        return self.passages.get(topic.key)


def report_for(source: DocumentationSource, title: str) -> dict[str, Any]:
    async def fixed_source() -> DocumentationSource:
        return source

    app.dependency_overrides[get_documentation_source] = fixed_source

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post("/api/triage", json={"title": title, "body": ""})

    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def test_relevant_pytest_documentation_is_cited_in_api_report() -> None:
    report = report_for(
        FixedDocumentationSource(
            {"capture": DocumentationPassage(CAPTURE_URL, CAPTURE_PASSAGE)}
        ),
        "Bug: capsys cannot capture stdout",
    )

    assert len(report["documentation_claims"]) == 1
    claim = report["documentation_claims"][0]
    assert "stdout and stderr" in claim["claim"]
    citation = next(
        item for item in report["citations"] if item["id"] == claim["citation_id"]
    )
    assert citation["source_url"] == CAPTURE_URL
    assert citation["passage"] == CAPTURE_PASSAGE


def test_fixture_scope_claim_uses_its_own_verified_passage() -> None:
    report = report_for(
        FixedDocumentationSource(
            {"fixture_scope": DocumentationPassage(SCOPE_URL, SCOPE_PASSAGE)}
        ),
        "Bug: fixture scope teardown happens too soon",
    )

    claim = report["documentation_claims"][0]
    assert "fixture scope" in claim["claim"]
    citation = next(
        item for item in report["citations"] if item["id"] == claim["citation_id"]
    )
    assert citation["source_url"] == SCOPE_URL
    assert citation["passage"] == SCOPE_PASSAGE


def test_documentation_is_omitted_when_irrelevant_or_passage_is_missing() -> None:
    source = FixedDocumentationSource({})
    unrelated = report_for(source, "Bug: collection hangs")
    missing = report_for(source, "Bug: capsys cannot capture stdout")

    assert unrelated["documentation_claims"] == []
    assert missing["documentation_claims"] == []
    assert all(item["passage"] is None for item in missing["citations"])
    assert "documentation_claims" in {item["field"] for item in missing["abstentions"]}
    assert source.requested == ["capture"]


def test_mismatched_retrieved_passage_does_not_support_claim() -> None:
    report = report_for(
        FixedDocumentationSource(
            {"capture": DocumentationPassage(CAPTURE_URL, "Unrelated paragraph.")}
        ),
        "Bug: capsys cannot capture stdout",
    )

    assert report["documentation_claims"] == []
    assert not any(item["passage"] for item in report["citations"])


def test_documentation_source_extracts_passage_from_the_linked_section(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = (
        "<section id='unrelated'><p>fixtures allow access to stdout/stderr "
        "output created during test execution.</p></section>"
        "<section id='accessing-captured-output-from-a-test-function'>"
        "<h2>Accessing captured output</h2>"
        "<p>The <code>capsys</code> fixtures allow access to "
        "<code>stdout</code>/<code>stderr</code> output created during "
        "test execution.</p></section>"
    )
    monkeypatch.setattr(
        "maintainer_copilot.documentation.urlopen",
        lambda request, timeout: BytesIO(html.encode()),
    )

    assert PytestDocumentationSource().get_passage(TOPICS[0]) == DocumentationPassage(
        CAPTURE_URL, CAPTURE_PASSAGE
    )


def test_report_rejects_claim_not_supported_by_supplied_passage() -> None:
    report = report_for(
        FixedDocumentationSource(
            {"capture": DocumentationPassage(CAPTURE_URL, CAPTURE_PASSAGE)}
        ),
        "Bug: capsys cannot capture stdout",
    )
    report["documentation_claims"][0]["claim"] = (
        "pytest guarantees that capsys captures subprocess output."
    )

    supplied = [
        DocumentationEvidence(
            claim=TOPICS[0].claim,
            passage=DocumentationPassage(CAPTURE_URL, CAPTURE_PASSAGE),
        )
    ]
    with pytest.raises(ValueError, match="not supplied by documentation source"):
        TriageReport.model_validate(report).validate_documentation_evidence(supplied)


def test_fixed_evidence_rejects_claim_citing_unsupplied_passage() -> None:
    report = report_for(
        FixedDocumentationSource({}), "Bug: capsys cannot capture stdout"
    )
    report["citations"].append(
        {
            "id": "C99",
            "source_url": CAPTURE_URL,
            "description": "forged documentation citation",
            "passage": CAPTURE_PASSAGE,
        }
    )
    report["documentation_claims"] = [{"claim": TOPICS[0].claim, "citation_id": "C99"}]

    with pytest.raises(ValueError, match="not supplied by documentation source"):
        TriageReport.model_validate(report).validate_documentation_evidence([])
