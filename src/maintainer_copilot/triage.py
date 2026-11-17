"""The Python triage API and its validated report."""

import re
from collections.abc import Collection
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    ValidationError,
    model_validator,
)

from maintainer_copilot import ci, documentation, issue_search, model, pytest_profile
from maintainer_copilot import source as repository_source
from maintainer_copilot.trace import TraceRecorder


class IssueUnderReview(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    body: str
    number: int | None = Field(default=None, gt=0)
    source_location: repository_source.SourceLocation | None = None


class Citation(BaseModel):
    id: str
    source_url: HttpUrl
    description: str
    passage: str | None = None
    source_location: repository_source.SourceLocation | None = None


class DocumentationClaim(BaseModel):
    claim: str
    citation_id: str


class SourceClaim(BaseModel):
    claim: str
    citation_id: str


class CIResult(BaseModel):
    check_name: str
    conclusion: str
    commit: str
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
    status: Literal["complete", "partial"]
    issue_type: str | None
    issue_type_quote: str | None
    duplicate_candidates: list[IssueSuggestion]
    related_issues: list[IssueSuggestion]
    missing_details: list[MissingReportDetail]
    documentation_claims: list[DocumentationClaim]
    source_claims: list[SourceClaim]
    ci_results: list[CIResult]
    draft_reply: str
    citations: list[Citation]
    abstentions: list[Abstention]

    @model_validator(mode="after")
    def validate_citations(self) -> "TriageReport":
        if (
            self.issue_type is not None
            and self.issue_type not in pytest_profile.TYPE_LABELS
        ):
            raise ValueError("issue type must be a pytest type label")
        if (self.issue_type is None) != (self.issue_type_quote is None):
            raise ValueError("issue type must include an issue-text quote")
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
        for source_claim in self.source_claims:
            citation = citation_by_id.get(source_claim.citation_id)
            if (
                citation is None
                or citation.source_location is None
                or citation.passage is None
                or str(citation.source_url) != citation.source_location.source_url
            ):
                raise ValueError("source claim must cite a commit and source line")
        for result in self.ci_results:
            citation = citation_by_id.get(result.citation_id)
            if citation is None or not citation.passage:
                raise ValueError("CI result must cite a check run")
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

    def validate_source_evidence(
        self, supplied_evidence: Collection[repository_source.SourceEvidence]
    ) -> "TriageReport":
        """Check source claims against excerpts read during this report request."""
        supplied = {
            (
                item.claim,
                item.excerpt.source_url,
                item.excerpt.commit,
                item.excerpt.path,
                item.excerpt.line,
                item.passage,
            )
            for item in supplied_evidence
        }
        citation_by_id = {item.id: item for item in self.citations}
        for claim in self.source_claims:
            citation = citation_by_id[claim.citation_id]
            location = citation.source_location
            assert location is not None
            if (
                claim.claim,
                str(citation.source_url),
                location.commit,
                location.path,
                location.line,
                citation.passage,
            ) not in supplied:
                raise ValueError("claim cites evidence not supplied by source reader")
        return self

    def validate_ci_evidence(
        self, supplied_evidence: Collection[ci.CheckResult]
    ) -> "TriageReport":
        """Check each result against a check run read during this report request."""
        supplied = {
            (item.name, item.conclusion, item.commit, str(item.url))
            for item in supplied_evidence
        }
        citation_by_id = {item.id: item for item in self.citations}
        for result in self.ci_results:
            citation = citation_by_id[result.citation_id]
            if (
                result.check_name,
                result.conclusion,
                result.commit,
                str(citation.source_url),
            ) not in supplied or citation.passage != (
                f"{result.check_name}: {result.conclusion} at commit {result.commit}"
            ):
                raise ValueError("CI result cites evidence not supplied by CI source")
        return self


def triage_issue(
    issue: IssueUnderReview,
    source: issue_search.IssueSource | None = None,
    documentation_source: documentation.DocumentationSource | None = None,
    source_reader: repository_source.SourceReader | None = None,
    model_client: model.ModelClient | None = None,
    ci_source: ci.CISource | None = None,
    trace: TraceRecorder | None = None,
) -> TriageReport:
    """Build a reviewable report from pytest templates, issues, and documentation."""
    recorder = trace or TraceRecorder()
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

    abstentions: list[Abstention] = []
    suggestions: list[issue_search.Match] = []
    if issue.number is None:
        search_reason = "A pytest issue number is needed to search only earlier issues."
    elif (query := issue_search.search_query(issue.title, issue.body)) is None:
        search_reason = "The report lacks enough specific details to compare issues."
    else:
        issue_source = source or issue_search.GitHubIssueSource()
        try:
            with recorder.call(
                "retrieval", "get_issue", f"pytest issue #{issue.number}"
            ) as event:
                reviewed = issue_source.get_issue(issue.number)
                if reviewed.number != issue.number:
                    raise issue_search.IssueSearchError("Wrong issue returned.")
                event.result_count = 1
            with recorder.call(
                "retrieval",
                "search_issues",
                f"query {query[:256]} before {reviewed.created_at.isoformat()}",
            ) as search_event:
                candidates = issue_source.search_issues(query, reviewed.created_at)
                search_event.result_count = len(candidates)
            with recorder.call("retrieval", "assess_matches") as event:
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
                event.result_count = len(suggestions)
            search_reason = None
        except Exception:
            search_reason = "Earlier pytest issue lookup is unavailable."
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
    if search_reason is None:
        search_event.references = [str(item.url) for item in duplicates + related]
    documentation_claims: list[DocumentationClaim] = []
    supplied_evidence: list[documentation.DocumentationEvidence] = []
    doc_source = documentation_source or documentation.PublicDocumentationSource(
        pytest_profile.DOCUMENTATION_TOPICS
    )
    for topic in pytest_profile.relevant_documentation_topics(issue.title, issue.body):
        try:
            with recorder.call(
                "retrieval", "get_documentation_passage", topic.key
            ) as event:
                passage = doc_source.get_passage(topic)
                event.result_count = 1 if passage is not None else 0
        except Exception:
            passage = None
        if passage is None or (passage.url, passage.text) != (
            topic.url,
            topic.passage,
        ):
            if event.status == "ok":
                event.status = "partial"
                event.error = "Verified documentation passage unavailable."
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
        event.references = [passage.url]
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
    source_claims: list[SourceClaim] = []
    supplied_source_evidence: list[repository_source.SourceEvidence] = []
    if issue.source_location is not None:
        location = issue.source_location
        reader = source_reader or repository_source.PublicRepositorySource()
        try:
            with recorder.call(
                "retrieval", "get_source_excerpt", location.source_url
            ) as event:
                excerpt = reader.get_excerpt(location)
                event.result_count = 1
        except Exception:
            excerpt = None
        if (
            excerpt is None
            or excerpt.commit != location.commit
            or excerpt.path != location.path
            or excerpt.line != location.line
            or excerpt.source_url != location.source_url
            or not excerpt.start_line <= location.line <= excerpt.end_line
            or len(excerpt.lines) != excerpt.end_line - excerpt.start_line + 1
        ):
            if event.status == "ok":
                event.status = "partial"
                event.error = "Requested source excerpt unavailable."
            abstentions.append(
                Abstention(
                    field="source_claims",
                    reason="Requested pytest source line is unavailable.",
                )
            )
        else:
            source_line = excerpt.lines[location.line - excerpt.start_line]
            claim = (
                f"At commit {location.commit}, pytest source {location.path}:"
                f"{location.line} contains the cited line."
            )
            supplied_source_evidence.append(
                repository_source.SourceEvidence(claim, excerpt, source_line)
            )
            event.references = [excerpt.source_url]
            citation_id = f"C{len(citations) + 1}"
            citations.append(
                Citation(
                    id=citation_id,
                    source_url=HttpUrl(excerpt.source_url),
                    description=f"pytest source: {location.path}:{location.line}",
                    passage=source_line,
                    source_location=location,
                )
            )
            source_claims.append(SourceClaim(claim=claim, citation_id=citation_id))
    ci_results: list[CIResult] = []
    supplied_ci_evidence: list[ci.CheckResult] = []
    if link := ci.linked_target(issue.title, issue.body):
        try:
            with recorder.call(
                "retrieval", "get_ci_checks", f"{link.kind}:{link.value}"
            ) as event:
                inspection = (ci_source or ci.PublicCISource()).get_checks(link)
                event.result_count = len(inspection.checks)
        except Exception:
            inspection = ci.CIInspection(())
        if inspection.partial or not inspection.checks:
            if event.status == "ok":
                event.status = "partial"
                event.error = "Linked CI results unavailable or incomplete."
        if inspection.partial and inspection.checks:
            abstentions.append(
                Abstention(
                    field="ci_results",
                    reason="Some linked pytest CI results are unavailable.",
                )
            )
        if not inspection.checks:
            abstentions.append(
                Abstention(
                    field="ci_results",
                    reason="Linked pytest CI results are unavailable.",
                )
            )
        for check in inspection.checks:
            if len(event.references) < 10:
                event.references.append(str(check.url))
            citation_id = f"C{len(citations) + 1}"
            citations.append(
                Citation(
                    id=citation_id,
                    source_url=check.url,
                    description=f"pytest CI check: {check.name}",
                    passage=(
                        f"{check.name}: {check.conclusion} at commit {check.commit}"
                    ),
                )
            )
            ci_results.append(
                CIResult(
                    check_name=check.name,
                    conclusion=check.conclusion,
                    commit=check.commit,
                    citation_id=citation_id,
                )
            )
            supplied_ci_evidence.append(check)
    if template is None:
        abstentions.append(
            Abstention(
                field="missing_details",
                reason="Issue text does not identify a bug or feature template.",
            )
        )

    citation_by_id = {item.id: item for item in citations}
    reply_statements = [
        model.ReplyStatement(
            detail.citation_id,
            f"Could you add {detail.request}?",
            str(citation_by_id[detail.citation_id].source_url),
        )
        for detail in details
    ]
    reply_statements.extend(
        model.ReplyStatement(
            item.citation_id,
            f"Earlier issue #{item.issue_number} may be relevant: {item.reason}",
            str(citation_by_id[item.citation_id].source_url),
        )
        for item in duplicates + related
    )
    reply_statements.extend(
        model.ReplyStatement(
            claim.citation_id,
            claim.claim,
            str(citation_by_id[claim.citation_id].source_url),
        )
        for claim in documentation_claims + source_claims
    )
    model_request = model.ModelRequest(
        issue_title=issue.title,
        issue_body=issue.body,
        reply_statements=tuple(reply_statements),
        required_reply_ids=tuple(detail.citation_id for detail in details),
    )
    try:
        client = model_client or model.OpenAICompatibleModel.from_environment()
        with recorder.call(
            "model", "triage_selection", model.model_identity(client)
        ) as event:
            suggestion = model.generate_validated(client, model_request, event)
    except (model.ModelUnavailable, ValidationError, ValueError) as exc:
        issue_type = None
        issue_type_quote = None
        model_reason = (
            "Model unavailable; no issue type suggestion was produced."
            if isinstance(exc, model.ModelUnavailable)
            else "Model output failed validation; no issue type was suggested."
        )
        abstentions.append(Abstention(field="issue_type", reason=model_reason))
        if not details:
            reply += (
                " I cannot substantiate a specific reply from the available evidence."
            )
            abstentions.append(
                Abstention(
                    field="draft_reply",
                    reason="Model did not select a supported reply claim.",
                )
            )
    else:
        issue_type = suggestion.issue_type
        issue_type_quote = suggestion.issue_type_quote
        if issue_type is None:
            abstentions.append(
                Abstention(
                    field="issue_type",
                    reason=(
                        "Model found insufficient issue-text evidence for a type label."
                    ),
                )
            )
        statement_by_id = {
            statement.citation_id: statement for statement in reply_statements
        }
        reply = "Thanks for sharing this issue."
        if suggestion.reply_citation_ids:
            reply += "\n" + "\n".join(
                f"- {statement_by_id[citation_id].text} [{citation_id}]"
                for citation_id in suggestion.reply_citation_ids
            )
        else:
            reply += (
                " I cannot substantiate a specific request from the available evidence."
            )
            abstentions.append(
                Abstention(
                    field="draft_reply",
                    reason="No supported reply claim was selected.",
                )
            )

    report = TriageReport(
        trace_id=recorder.trace_id,
        status=recorder.status,
        issue_type=issue_type,
        issue_type_quote=issue_type_quote,
        duplicate_candidates=duplicates,
        related_issues=related,
        missing_details=details,
        documentation_claims=documentation_claims,
        source_claims=source_claims,
        ci_results=ci_results,
        draft_reply=reply,
        citations=citations,
        abstentions=abstentions,
    )
    validated = (
        report.validate_documentation_evidence(supplied_evidence)
        .validate_source_evidence(supplied_source_evidence)
        .validate_ci_evidence(supplied_ci_evidence)
    )
    recorder.save()
    return validated
