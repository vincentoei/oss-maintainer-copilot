"""Thin HTTP and browser interface for the Python triage API."""

from importlib.resources import files
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse

from maintainer_copilot import IssueUnderReview, TriageReport, triage_issue
from maintainer_copilot.issue_search import GitHubIssueSource

app = FastAPI(title="Open-source Maintainer Copilot")


async def get_issue_source() -> GitHubIssueSource:
    return GitHubIssueSource()


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = files("maintainer_copilot").joinpath("index.html").read_text()
    return HTMLResponse(html)


@app.post("/api/triage", response_model=TriageReport)
async def create_report(
    issue: IssueUnderReview,
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
) -> TriageReport:
    return triage_issue(issue, source)
