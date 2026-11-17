"""Replay one historical pytest issue from verified opening and pinned evidence."""

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from importlib.resources import files

from pydantic import BaseModel, Field, model_validator

from maintainer_copilot import ci, documentation, issue_search, model
from maintainer_copilot import source as repository_source
from maintainer_copilot.triage import IssueUnderReview, TriageReport, triage_issue


class CaseFlagged(Exception):
    """A historical case cannot safely be scored or replayed."""


class EarlierIssue(BaseModel):
    number: int = Field(gt=0)
    created_at: datetime
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    last_edited_at: datetime | None


class HistoricalCase(BaseModel):
    issue_number: int = Field(gt=0)
    opening_title: str
    opening_cutoff: datetime
    opening_content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    opening_last_edited_at: datetime | None
    opening_verified_at: datetime
    repository_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    repository_commit_at: datetime
    earlier_issue: EarlierIssue

    @model_validator(mode="after")
    def validate_cutoff(self) -> "HistoricalCase":
        dates = (
            self.opening_cutoff,
            self.repository_commit_at,
            self.earlier_issue.created_at,
            self.opening_verified_at,
        )
        if any(value.tzinfo is None for value in dates):
            raise ValueError("historical case dates must include a timezone")
        if not (
            self.repository_commit_at < self.opening_cutoff
            and self.earlier_issue.created_at < self.opening_cutoff
            and self.opening_cutoff <= self.opening_verified_at
        ):
            raise ValueError("historical evidence must predate the opening cutoff")
        if (
            self.opening_last_edited_at is not None
            or self.earlier_issue.last_edited_at is not None
        ):
            raise ValueError("this case requires unedited issue content")
        return self


def load_case() -> HistoricalCase:
    """Load the reviewed public metadata for pytest issue #12081."""
    path = files("maintainer_copilot").joinpath("cases/pytest_12081.json")
    return HistoricalCase.model_validate_json(path.read_text(encoding="utf-8"))


def content_hash(issue: issue_search.IssueRecord) -> str:
    return hashlib.sha256(f"{issue.title}\0{issue.body}".encode()).hexdigest()


def _verified_issue(
    source: issue_search.IssueSource,
    number: int,
    created_at: datetime,
    expected_hash: str,
) -> issue_search.IssueRecord:
    try:
        issue = source.get_issue(number)
    except Exception as exc:
        raise CaseFlagged(f"pytest issue #{number} is unavailable") from exc
    if (
        issue.number != number
        or issue.created_at != created_at
        or content_hash(issue) != expected_hash
    ):
        raise CaseFlagged(f"pytest issue #{number} opening content changed")
    return issue


@dataclass(frozen=True)
class _FrozenIssues:
    reviewed: issue_search.IssueRecord
    earlier: issue_search.IssueRecord

    def get_issue(self, number: int) -> issue_search.IssueRecord:
        if number != self.reviewed.number:
            raise issue_search.IssueSearchError("Issue is outside the frozen case.")
        return self.reviewed

    def search_issues(
        self, query: str, created_before: datetime
    ) -> list[issue_search.IssueRecord]:
        if created_before != self.reviewed.created_at or not query:
            raise issue_search.IssueSearchError("Search is outside the frozen case.")
        return [self.earlier]


_CAPTURE_DOC_PATH = "doc/en/how-to/capture-stdout-stderr.rst"
_CAPTURE_DOC_LINES = (
    "The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures",
    "allow access to stdout/stderr output created during test execution.  Here is",
)
_CAPTURE_SOURCE_LINE = (
    '        """Read and return the captured output so far, resetting the internal'
)


def _capture_topic(commit: str) -> documentation.DocumentationTopic:
    return documentation.DocumentationTopic(
        key="capture",
        url=(
            "https://github.com/pytest-dev/pytest/blob/"
            f"{commit}/{_CAPTURE_DOC_PATH}#L109-L110"
        ),
        section="accessing-captured-output-from-a-test-function",
        passage=" ".join(_CAPTURE_DOC_LINES),
        claim=(
            "pytest documents that capture fixtures let tests access stdout and stderr "
            "created during execution."
        ),
        relevance=r"\b(?:capsys|capfd|capteesys|capsysbinary|capfdbinary)\b",
    )


@dataclass(frozen=True)
class _PinnedDocumentation:
    topic: documentation.DocumentationTopic
    commit: str
    reader: repository_source.SourceReader

    def get_passage(
        self, topic: documentation.DocumentationTopic
    ) -> documentation.DocumentationPassage | None:
        if topic != self.topic:
            return None
        excerpt = self.reader.get_excerpt(
            repository_source.SourceLocation(
                commit=self.commit, path=_CAPTURE_DOC_PATH, line=110
            )
        )
        offset = 109 - excerpt.start_line
        if (
            excerpt.commit != self.commit
            or excerpt.path != _CAPTURE_DOC_PATH
            or tuple(excerpt.lines[offset : offset + 2]) != _CAPTURE_DOC_LINES
        ):
            return None
        return documentation.DocumentationPassage(topic.url, topic.passage)


@dataclass(frozen=True)
class _PinnedSource:
    commit: str
    reader: repository_source.SourceReader

    def get_excerpt(
        self, location: repository_source.SourceLocation
    ) -> repository_source.SourceExcerpt:
        if (
            location.commit != self.commit
            or location.path != "src/_pytest/capture.py"
            or location.line != 935
        ):
            raise repository_source.SourceUnavailable("Source is outside the cutoff.")
        excerpt = self.reader.get_excerpt(location)
        if (
            excerpt.commit != self.commit
            or excerpt.path != location.path
            or not excerpt.start_line <= location.line <= excerpt.end_line
            or excerpt.lines[location.line - excerpt.start_line] != _CAPTURE_SOURCE_LINE
        ):
            raise repository_source.SourceUnavailable("Pinned source did not match.")
        return excerpt


class ControlledReplayModel:
    """Fixed evidence selection for a smoke replay, not a quality score."""

    def generate(self, request: model.ModelRequest) -> object:
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": [
                statement.citation_id for statement in request.reply_statements
            ],
        }


class _UnavailableHistoricalCI:
    """Keep live check runs out of historical model input."""

    def get_checks(self, link: ci.CILink) -> ci.CIInspection:
        return ci.CIInspection(())


def replay_case(
    case: HistoricalCase | None = None,
    *,
    issue_source: issue_search.IssueSource | None = None,
    source_reader: repository_source.SourceReader | None = None,
    model_client: model.ModelClient | None = None,
) -> TriageReport:
    """Verify public issue text, then triage with only pre-cutoff evidence."""
    case = case or load_case()
    public_issues = issue_source or issue_search.GitHubIssueSource()
    reviewed = _verified_issue(
        public_issues,
        case.issue_number,
        case.opening_cutoff,
        case.opening_content_sha256,
    )
    if reviewed.title != case.opening_title:
        raise CaseFlagged("the verified opening title changed")
    earlier = _verified_issue(
        public_issues,
        case.earlier_issue.number,
        case.earlier_issue.created_at,
        case.earlier_issue.content_sha256,
    )
    reader = source_reader or repository_source.PublicRepositorySource()
    topic = _capture_topic(case.repository_commit)
    issue = IssueUnderReview(
        number=reviewed.number,
        title=reviewed.title,
        body=reviewed.body,
        source_location=repository_source.SourceLocation(
            commit=case.repository_commit, path="src/_pytest/capture.py", line=935
        ),
    )
    return triage_issue(
        issue,
        source=_FrozenIssues(reviewed, earlier),
        documentation_source=_PinnedDocumentation(
            topic, case.repository_commit, reader
        ),
        source_reader=_PinnedSource(case.repository_commit, reader),
        model_client=model_client or ControlledReplayModel(),
        ci_source=_UnavailableHistoricalCI(),
        documentation_topics=(topic,),
        template_revision=case.repository_commit,
    )


if __name__ == "__main__":
    print(json.dumps(replay_case().model_dump(mode="json"), indent=2))
