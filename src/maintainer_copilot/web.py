"""Thin HTTP and browser interface for the Python triage API."""

from importlib.resources import files
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from maintainer_copilot import (
    IssueUnderReview,
    TriageReport,
    pytest_profile,
    triage_issue,
)
from maintainer_copilot.agent import (
    AgentClient,
    OpenAICompatibleAgent,
    triage_issue_with_agent,
)
from maintainer_copilot.ci import CISource, PublicCISource
from maintainer_copilot.documentation import (
    DocumentationSource,
    PublicDocumentationSource,
)
from maintainer_copilot.issue_search import GitHubIssueSource
from maintainer_copilot.model import ModelClient, OpenAICompatibleModel
from maintainer_copilot.source import (
    PublicRepositorySource,
    SourceExcerpt,
    SourceLocation,
    SourceReader,
    SourceUnavailable,
)

app = FastAPI(title="Open-source Maintainer Copilot")


async def get_issue_source() -> GitHubIssueSource:
    return GitHubIssueSource()


async def get_documentation_source() -> DocumentationSource:
    return PublicDocumentationSource(pytest_profile.DOCUMENTATION_TOPICS)


async def get_source_reader() -> SourceReader:
    return PublicRepositorySource()


async def get_ci_source() -> CISource:
    return PublicCISource()


async def get_model_client() -> ModelClient:
    return OpenAICompatibleModel.from_environment()


async def get_agent_client() -> AgentClient:
    return OpenAICompatibleAgent.from_environment()


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = files("maintainer_copilot").joinpath("index.html").read_text()
    return HTMLResponse(html)


@app.get("/api/source", response_model=SourceExcerpt)
async def inspect_source(
    location: Annotated[SourceLocation, Query()],
    source: Annotated[SourceReader, Depends(get_source_reader)],
) -> SourceExcerpt:
    try:
        return source.get_excerpt(location)
    except SourceUnavailable as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/triage", response_model=TriageReport)
async def create_report(
    issue: IssueUnderReview,
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
    documentation_source: Annotated[
        DocumentationSource, Depends(get_documentation_source)
    ],
    source_reader: Annotated[SourceReader, Depends(get_source_reader)],
    model_client: Annotated[ModelClient, Depends(get_model_client)],
    ci_source: Annotated[CISource, Depends(get_ci_source)],
) -> TriageReport:
    return triage_issue(
        issue, source, documentation_source, source_reader, model_client, ci_source
    )


@app.post("/api/agent/triage", response_model=TriageReport)
async def create_agent_report(
    issue: IssueUnderReview,
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
    documentation_source: Annotated[
        DocumentationSource, Depends(get_documentation_source)
    ],
    source_reader: Annotated[SourceReader, Depends(get_source_reader)],
    agent_client: Annotated[AgentClient, Depends(get_agent_client)],
    ci_source: Annotated[CISource, Depends(get_ci_source)],
) -> TriageReport:
    return triage_issue_with_agent(
        issue, source, documentation_source, source_reader, agent_client, ci_source
    )
