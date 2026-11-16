import asyncio

import httpx2

from maintainer_copilot import IssueUnderReview, TriageReport, triage_issue
from maintainer_copilot.web import app


def test_web_interface_submits_issue_to_report_api() -> None:
    issue_data = {
        "title": "Bug: pytest crashes on Ubuntu",
        "body": "pytest 8.3.4 on Ubuntu 24.04 crashes during collection.",
    }

    async def request_report() -> tuple[httpx2.Response, httpx2.Response]:
        transport = httpx2.ASGITransport(app=app)
        async with httpx2.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            page = await client.get("/")
            response = await client.post(
                "/api/triage",
                json=issue_data,
            )
            return page, response

    page, response = asyncio.run(request_report())

    assert page.status_code == 200
    assert 'name="title"' in page.text
    assert 'name="body"' in page.text
    assert "Missing report details" in page.text
    assert "Draft reply" in page.text
    assert "Citations" in page.text
    assert "Abstentions" in page.text
    assert response.status_code == 200
    report = TriageReport.model_validate(response.json())
    assert [detail.name for detail in report.missing_details] == [
        "pip list output",
        "minimal example",
    ]
    assert report.trace_id
    python_report = triage_issue(IssueUnderReview(**issue_data))
    assert report.model_dump(exclude={"trace_id"}) == python_report.model_dump(
        exclude={"trace_id"}
    )
    assert len(report.citations) == 2
    assert {abstention.field for abstention in report.abstentions} == {
        "issue_type",
        "duplicate_candidates",
        "related_issues",
    }
