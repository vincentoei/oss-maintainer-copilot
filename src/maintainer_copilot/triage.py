"""The Python triage API and its validated report."""

import re
from collections.abc import Collection
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from maintainer_copilot import documentation, issue_search, pytest_profile


class IssueUnderReview(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    body: str
    number: int | None = Field(default=None, gt=0)


class Citation(BaseModel):
    id: str
    source_url: HttpUrl
    description: str
    passage: str | None = None


class DocumentationClaim(BaseModel):
    claim: str
    citation_id: str


class MissingReportDetail(BaseModel):
    name: str
    request: str
    citation_id: str


class Abstention(BaseModel):
    field: str
    reason: str


class IssueSuggestion(BaseModel):
    issue_number: int
    title: str
    url: HttpUrl
    reason: str
    citation_id: str


class TriageReport(BaseModel):
    trace_id: UUID
    issue_type: str | None
    duplicate_candidates: list[IssueSuggestion]
    related_issues: list[IssueSuggestion]
    missing_details: list[MissingReportDetail]
    documentation_claims: list[DocumentationClaim]
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
        citation_urls = {item.id: item.source_url for item in self.citations}
        if any(
            citation_urls.get(item.citation_id) != item.url
            for item in self.duplicate_candidates + self.related_issues
        ):
            raise ValueError("each suggested issue must cite its issue URL")
        reply_citation_ids = set(re.findall(r"\[(C\d+)\]", self.draft_reply))
        if not reply_citation_ids.issubset(citation_ids):
            raise ValueError("draft reply refers to an unknown citation")
        if any(
            detail.citation_id not in reply_citation_ids
            for detail in self.missing_details
        ):
            raise ValueError("draft reply must cite each requested detail")
        citation_by_id = {item.id: item for item in self.citations}
        for claim in self.documentation_claims:
            citation = citation_by_id.get(claim.citation_id)
            if citation is None or not citation.passage:
                raise ValueError("documentation claim must cite a passage")
        return self

    def validate_documentation_evidence(
        self, supplied_evidence: Collection[documentation.DocumentationEvidence]
    ) -> "TriageReport":
        """Check claims and citations against evidence returned by the source."""
        supplied = {
            (item.claim, item.passage.url, item.passage.text)
            for item in supplied_evidence
        }
        citation_by_id = {item.id: item for item in self.citations}
        for claim in self.documentation_claims:
            citation = citation_by_id[claim.citation_id]
            if (
                claim.claim,
                str(citation.source_url),
                citation.passage,
            ) not in supplied:
                raise ValueError(
                    "claim cites evidence not supplied by documentation source"
                )
        return self


def triage_issue(
    issue: IssueUnderReview,
    source: issue_search.IssueSource | None = None,
    documentation_source: documentation.DocumentationSource | None = None,
) -> TriageReport:
    """Build a reviewable report from pytest templates, issues, and documentation."""
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
        Abstention(field="issue_type", reason="No issue type evidence was assessed.")
    ]
    suggestions: list[issue_search.Match] = []
    if issue.number is None:
        search_reason = "A pytest issue number is needed to search only earlier issues."
    elif (query := issue_search.search_query(issue.title, issue.body)) is None:
        search_reason = "The report lacks enough specific details to compare issues."
    else:
        issue_source = source or issue_search.GitHubIssueSource()
        try:
            reviewed = issue_source.get_issue(issue.number)
            candidates = issue_source.search_issues(query, reviewed.created_at)
            suggestions = [
                match
                for candidate in candidates
                if candidate.number < reviewed.number
                and candidate.created_at < reviewed.created_at
                if (
                    match := issue_search.assess_match(
                        issue.title, issue.body, candidate
                    )
                )
                is not None
            ]
            search_reason = None
        except issue_search.IssueSearchError as exc:
            search_reason = str(exc)
    if search_reason is not None:
        abstentions.extend(
            Abstention(field=field, reason=search_reason)
            for field in ("duplicate_candidates", "related_issues")
        )
    suggestions.sort(key=lambda match: (-match.score, match.issue.number))
    duplicates: list[IssueSuggestion] = []
    related: list[IssueSuggestion] = []
    seen: set[int] = set()
    for match in suggestions:
        candidate = match.issue
        if candidate.number in seen:
            continue
        target = duplicates if match.kind == "duplicate" else related
        if len(target) >= 5:
            continue
        seen.add(candidate.number)
        citation_id = f"C{len(citations) + 1}"
        citation_url = HttpUrl(candidate.url)
        citations.append(
            Citation(
                id=citation_id,
                source_url=citation_url,
                description=f"pytest issue #{candidate.number}: {candidate.title}",
            )
        )
        target.append(
            IssueSuggestion(
                issue_number=candidate.number,
                title=candidate.title,
                url=citation_url,
                reason=match.reason,
                citation_id=citation_id,
            )
        )
    documentation_claims: list[DocumentationClaim] = []
    supplied_evidence: list[documentation.DocumentationEvidence] = []
    doc_source = documentation_source or documentation.PytestDocumentationSource()
    for topic in documentation.relevant_topics(issue.title, issue.body):
        try:
            passage = doc_source.get_passage(topic)
        except documentation.DocumentationError:
            passage = None
        if passage is None or (passage.url, passage.text) != (
            topic.url,
            topic.passage,
        ):
            abstentions.append(
                Abstention(
                    field="documentation_claims",
                    reason=f"pytest documentation passage unavailable: {topic.key}.",
                )
            )
            continue
        supplied_evidence.append(
            documentation.DocumentationEvidence(claim=topic.claim, passage=passage)
        )
        citation_id = f"C{len(citations) + 1}"
        citations.append(
            Citation(
                id=citation_id,
                source_url=HttpUrl(passage.url),
                description=f"pytest documentation: {topic.key.replace('_', ' ')}",
                passage=passage.text,
            )
        )
        documentation_claims.append(
            DocumentationClaim(claim=topic.claim, citation_id=citation_id)
        )
    if template is None:
        abstentions.append(
            Abstention(
                field="missing_details",
                reason="Issue text does not identify a bug or feature template.",
            )
        )

    report = TriageReport(
        trace_id=uuid4(),
        issue_type=None,
        duplicate_candidates=duplicates,
        related_issues=related,
        missing_details=details,
        documentation_claims=documentation_claims,
        draft_reply=reply,
        citations=citations,
        abstentions=abstentions,
    )
    return report.validate_documentation_evidence(supplied_evidence)
