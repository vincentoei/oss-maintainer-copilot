"""Thin HTTP and browser interface for the Python triage API."""

import os
from importlib.resources import files
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from maintainer_copilot import (
    IssueUnderReview,
    TriageReport,
    triage_issue,
)
from maintainer_copilot.agent import (
    AgentClient,
    OpenAICompatibleAgent,
    OpenAICompatibleDraftingAgent,
    triage_issue_with_agent,
)
from maintainer_copilot.ci import CISource, PublicCISource
from maintainer_copilot.documentation import (
    DocumentationSource,
    PublicDocumentationSource,
)
from maintainer_copilot.issue_search import GitHubIssueSource
from maintainer_copilot.model import (
    ModelClient,
    OpenAICompatibleDraftingModel,
    OpenAICompatibleModel,
)
from maintainer_copilot.registry import (
    Registration,
    RegistrationError,
    RegistrationRequest,
    RepositoryConfiguration,
    RepositoryRegistry,
    get_registry,
)
from maintainer_copilot.repository import RepositoryContext
from maintainer_copilot.source import (
    PublicRepositorySource,
    SourceExcerpt,
    SourceLocation,
    SourceReader,
    SourceUnavailable,
)
from maintainer_copilot.trace import TraceRecord, get_trace

app = FastAPI(title="Open-source Maintainer Copilot")


async def get_registry_dependency() -> RepositoryRegistry:
    return get_registry()


async def get_repository_context(
    issue: IssueUnderReview,
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
) -> RepositoryContext:
    try:
        return registry.resolve(issue.registration_id)
    except RegistrationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


async def get_issue_source(
    context: Annotated[RepositoryContext, Depends(get_repository_context)],
) -> GitHubIssueSource:
    return GitHubIssueSource(context.repository)


async def get_documentation_source(
    context: Annotated[RepositoryContext, Depends(get_repository_context)],
) -> DocumentationSource:
    return PublicDocumentationSource(context.documentation)


async def get_source_reader() -> SourceReader:
    return PublicRepositorySource()


async def get_ci_source(
    context: Annotated[RepositoryContext, Depends(get_repository_context)],
) -> CISource:
    return PublicCISource(context.repository)


@app.get("/api/repositories", response_model=list[Registration])
def list_repositories(
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
) -> list[Registration]:
    return registry.list()


@app.post("/api/repositories", response_model=Registration)
def add_repository(
    payload: RegistrationRequest,
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
) -> Registration:
    try:
        return registry.add(payload.repository, payload.configuration)
    except RegistrationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/repositories/{registration_id}/refresh", response_model=Registration)
def refresh_repository(
    registration_id: str,
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
    configuration: RepositoryConfiguration | None = None,
) -> Registration:
    try:
        return registry.refresh(registration_id, configuration)
    except RegistrationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.delete("/api/repositories/{registration_id}", status_code=204)
def remove_repository(
    registration_id: str,
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
) -> None:
    try:
        registry.remove(registration_id)
    except RegistrationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


async def get_model_client() -> ModelClient:
    if os.getenv("MODEL_DRAFTING") == "1":
        return OpenAICompatibleDraftingModel.from_environment()
    return OpenAICompatibleModel.from_environment()


async def get_agent_client() -> AgentClient:
    if os.getenv("MODEL_DRAFTING") == "1":
        return OpenAICompatibleDraftingAgent.from_environment()
    return OpenAICompatibleAgent.from_environment()


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = files("maintainer_copilot").joinpath("index.html").read_text()
    return HTMLResponse(html)


class SourceInspectionQuery(SourceLocation):
    registration_id: str | None = None


@app.get("/api/source", response_model=SourceExcerpt)
async def inspect_source(
    http_request: Request,
    location: Annotated[SourceInspectionQuery, Query()],
    source: Annotated[SourceReader, Depends(get_source_reader)],
    registry: Annotated[RepositoryRegistry, Depends(get_registry_dependency)],
) -> SourceExcerpt:
    try:
        context = registry.resolve(location.registration_id)
        if (
            "repository" in http_request.query_params
            and location.repository != context.repository
        ):
            raise RegistrationError("Source location belongs to another repository.")
        return source.get_excerpt(
            SourceLocation(
                repository=context.repository,
                commit=location.commit,
                path=location.path,
                line=location.line,
            )
        )
    except RegistrationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SourceUnavailable as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/traces/{trace_id}", response_model=TraceRecord)
async def inspect_trace(trace_id: UUID) -> TraceRecord:
    record = get_trace(trace_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Trace not found.")
    return record


@app.post("/api/triage", response_model=TriageReport)
def create_report(
    issue: IssueUnderReview,
    context: Annotated[RepositoryContext, Depends(get_repository_context)],
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
    documentation_source: Annotated[
        DocumentationSource, Depends(get_documentation_source)
    ],
    source_reader: Annotated[SourceReader, Depends(get_source_reader)],
    model_client: Annotated[ModelClient, Depends(get_model_client)],
    ci_source: Annotated[CISource, Depends(get_ci_source)],
) -> TriageReport:
    try:
        return triage_issue(
            issue,
            source,
            documentation_source,
            source_reader,
            model_client,
            ci_source,
            context=context,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/agent/triage", response_model=TriageReport)
def create_agent_report(
    issue: IssueUnderReview,
    context: Annotated[RepositoryContext, Depends(get_repository_context)],
    source: Annotated[GitHubIssueSource, Depends(get_issue_source)],
    documentation_source: Annotated[
        DocumentationSource, Depends(get_documentation_source)
    ],
    source_reader: Annotated[SourceReader, Depends(get_source_reader)],
    agent_client: Annotated[AgentClient, Depends(get_agent_client)],
    ci_source: Annotated[CISource, Depends(get_ci_source)],
) -> TriageReport:
    try:
        return triage_issue_with_agent(
            issue,
            source,
            documentation_source,
            source_reader,
            agent_client,
            ci_source,
            context=context,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
