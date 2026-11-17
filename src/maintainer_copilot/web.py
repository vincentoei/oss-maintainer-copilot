"""Thin HTTP and browser interface for the Python triage API."""

from importlib.resources import files
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse

from maintainer_copilot import (
    IssueUnderReview,
    TriageReport,
    pytest_profile,
    triage_issue,
)
from maintainer_copilot.documentation import (
    DocumentationSource,
    PublicDocumentationSource,
)
from maintainer_copilot.issue_search import GitHubIssueSource

app = FastAPI(title="Open-source Maintainer Copilot")


async def get_issue_source() -> GitHubIssueSource:
    return GitHubIssueSource()


async def get_documentation_source() -> DocumentationSource:
    return PublicDocumentationSource(pytest_profile.DOCUMENTATION_TOPICS)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = files("maintainer_copilot").joinpath("index.html").read_text()
    return HTMLResponse(html)


@app.post("/api/triage", response_model=TriageReport)
async def create_report(
    issue: IssueUnderReview,
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
    documentation_source: Annotated[
        DocumentationSource, Depends(get_documentation_source)
    ],
) -> TriageReport:
    return triage_issue(issue, source, documentation_source)
