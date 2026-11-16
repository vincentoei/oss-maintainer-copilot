"""The Python triage API and its validated report."""

import re
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from maintainer_copilot import pytest_profile


class IssueUnderReview(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    body: str


class Citation(BaseModel):
    id: str
    source_url: HttpUrl
    description: str


class MissingReportDetail(BaseModel):
    name: str
    request: str
    citation_id: str


class Abstention(BaseModel):
    field: str
    reason: str


class TriageReport(BaseModel):
    trace_id: UUID
    issue_type: str | None
    duplicate_candidates: list[dict[str, str]]
    related_issues: list[dict[str, str]]
    missing_details: list[MissingReportDetail]
    draft_reply: str
    citations: list[Citation]
    abstentions: list[Abstention]

    @model_validator(mode="after")
    def validate_citations(self) -> "TriageReport":
        citation_ids = [citation.id for citation in self.citations]
        if len(citation_ids) != len(set(citation_ids)):
            raise ValueError("citation IDs must be unique")
        if any(
            detail.citation_id not in citation_ids for detail in self.missing_details
        ):
            raise ValueError("each missing detail must have a citation")
        reply_citation_ids = set(re.findall(r"\[(C\d+)\]", self.draft_reply))
        if not reply_citation_ids.issubset(citation_ids):
            raise ValueError("draft reply refers to an unknown citation")
        if any(
            detail.citation_id not in reply_citation_ids
            for detail in self.missing_details
        ):
            raise ValueError("draft reply must cite each requested detail")
        return self


def triage_issue(issue: IssueUnderReview) -> TriageReport:
    """Build a reviewable report from the fixed pytest template evidence."""
    template = pytest_profile.template_for(issue.title, issue.body)
    if template == "bug":
        missing = pytest_profile.missing_bug_details(issue.body)
    elif template == "feature":
        missing = pytest_profile.missing_feature_details(issue.body)
    else:
        missing = []

    details = [
        MissingReportDetail(
            name=detail.name,
            request=detail.request,
            citation_id=f"C{index}",
        )
        for index, detail in enumerate(missing, start=1)
    ]
    citations = (
        [
            Citation(
                id=f"C{index}",
                source_url=HttpUrl(pytest_profile.citation_url(template, detail.line)),
                description=f"pytest {template} report template: {detail.name}",
            )
            for index, detail in enumerate(missing, start=1)
        ]
        if template is not None
        else []
    )
    reply = "Thanks for sharing this issue."
    if details:
        requests = "\n".join(
            f"- {detail.request} [{detail.citation_id}]" for detail in details
        )
        reply += f" Could you add the following details?\n{requests}"

    abstentions = [
        Abstention(field="issue_type", reason="No issue type evidence was assessed."),
        Abstention(
            field="duplicate_candidates", reason="Earlier issues were not searched."
        ),
        Abstention(field="related_issues", reason="Earlier issues were not searched."),
    ]
    if template is None:
        abstentions.append(
            Abstention(
                field="missing_details",
                reason="Issue text does not identify a bug or feature template.",
            )
        )

    return TriageReport(
        trace_id=uuid4(),
        issue_type=None,
        duplicate_candidates=[],
        related_issues=[],
        missing_details=details,
        draft_reply=reply,
        citations=citations,
        abstentions=abstentions,
    )
