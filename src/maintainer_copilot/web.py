"""Thin HTTP and browser interface for the Python triage API."""

from importlib.resources import files

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from maintainer_copilot import IssueUnderReview, TriageReport, triage_issue

app = FastAPI(title="Open-source Maintainer Copilot")


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = files("maintainer_copilot").joinpath("index.html").read_text()
    return HTMLResponse(html)


@app.post("/api/triage", response_model=TriageReport)
async def create_report(issue: IssueUnderReview) -> TriageReport:
    return triage_issue(issue)
