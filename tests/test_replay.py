"""Historical replay contract: current GitHub activity cannot enter a report."""

from datetime import UTC, datetime

import pytest

from maintainer_copilot import ci, issue_search
from maintainer_copilot import source as repository_source
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.replay import (
    CaseFlagged,
    ControlledReplayModel,
    HistoricalCase,
    content_hash,
    load_case,
    replay_case,
)


class ChangingGitHub(issue_search.GitHubIssueSource):
    def __init__(
        self, reviewed: issue_search.IssueRecord, earlier: issue_search.IssueRecord
    ) -> None:
        self.issues = {reviewed.number: reviewed, earlier.number: earlier}
        self.comments = ["later comment says this is a duplicate"]
        self.labels = ["type: bug"]
        self.duplicate_decisions = ["closed as duplicate"]
        self.later_search_results = ["post-cutoff duplicate"]
        self.reads: list[int] = []

    def _get_json(self, url: str) -> dict[str, object]:
        number = int(url.rsplit("/", 1)[-1])
        self.reads.append(number)
        issue = self.issues[number]
        return {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "created_at": issue.created_at.isoformat(),
            "comments": self.comments,
            "labels": self.labels,
            "state": "closed",
            "state_reason": self.duplicate_decisions,
        }

    def search_issues(
        self, query: str, created_before: datetime
    ) -> list[issue_search.IssueRecord]:
        raise AssertionError("replay must not search the live issue index")


class ChangingRepository:
    def __init__(self, commit: str) -> None:
        self.commit = commit
        self.later_code = "a post-cutoff fix"
        self.later_documentation = "a post-cutoff docs change"
        self.reads: list[repository_source.SourceLocation] = []

    def get_excerpt(
        self, location: repository_source.SourceLocation
    ) -> repository_source.SourceExcerpt:
        self.reads.append(location)
        assert location.commit == self.commit
        if location.path == "doc/en/how-to/capture-stdout-stderr.rst":
            assert location.line == 110
            lines = [
                "Accessing captured output from a test function",
                "-----------------------------------------------",
                "",
                (
                    "The ``capsys``, ``capsysbinary``, ``capfd``, and "
                    "``capfdbinary`` fixtures"
                ),
                (
                    "allow access to stdout/stderr output created during test "
                    "execution.  Here is"
                ),
            ]
            start = 106
        else:
            assert location.path == "src/_pytest/capture.py"
            assert location.line == 935
            lines = [
                "    def readouterr(self) -> CaptureResult[AnyStr]:",
                (
                    '        """Read and return the captured output so far, '
                    "resetting the internal"
                ),
                "        buffer.",
            ]
            start = 934
        return repository_source.SourceExcerpt(
            commit=location.commit,
            path=location.path,
            line=location.line,
            start_line=start,
            end_line=start + len(lines) - 1,
            lines=lines,
            source_url=location.source_url,
        )


class ObservedModel:
    def __init__(self) -> None:
        self.requests: list[ModelRequest] = []

    def generate(self, request: ModelRequest) -> object:
        self.requests.append(request)
        return ControlledReplayModel().generate(request)


def synthetic_case() -> tuple[HistoricalCase, ChangingGitHub, ChangingRepository]:
    original = load_case()
    reviewed = issue_search.IssueRecord(
        number=original.issue_number,
        title="Feature: capsys output after readouterr",
        body=(
            "## What's the problem this feature will solve?\n"
            "I need captured output to remain visible after calling "
            "capsys.readouterr().\n"
            "## Describe the solution you'd like\n"
            "Please add an option to preserve the output.\n"
        ),
        created_at=original.opening_cutoff,
    )
    earlier = issue_search.IssueRecord(
        number=original.earlier_issue.number,
        title="capture: keep all output for Captured stdout call",
        body="capfd.readouterr() resets what pytest displays in failed tests.",
        created_at=original.earlier_issue.created_at,
    )
    data = original.model_dump()
    data["opening_title"] = reviewed.title
    data["opening_content_sha256"] = content_hash(reviewed)
    data["earlier_issue"]["content_sha256"] = content_hash(earlier)
    case = HistoricalCase.model_validate(data)
    return (
        case,
        ChangingGitHub(reviewed, earlier),
        ChangingRepository(case.repository_commit),
    )


def test_replay_ignores_post_cutoff_activity_in_every_evidence_channel() -> None:
    case, github, repository = synthetic_case()
    model = ObservedModel()

    first = replay_case(
        case, issue_source=github, source_reader=repository, model_client=model
    )
    assert first.status == "complete"
    assert first.related_issues or first.duplicate_candidates
    assert first.missing_details
    assert first.documentation_claims and first.source_claims
    assert all(
        case.repository_commit in str(citation.source_url)
        for citation in first.citations
        if "github.com/pytest-dev/pytest/blob/" in str(citation.source_url)
    )

    github.comments.append("later maintainer reply reveals the fix")
    github.labels.append("type: enhancement")
    github.duplicate_decisions.append("duplicate of #3448")
    github.later_search_results.append("new duplicate after the cutoff")
    repository.later_code = "readouterr now copies output"
    repository.later_documentation = "the docs now explain the fix"

    second = replay_case(
        case, issue_source=github, source_reader=repository, model_client=model
    )
    assert first.model_dump(exclude={"trace_id"}) == second.model_dump(
        exclude={"trace_id"}
    )
    assert len(model.requests) == 2
    assert model.requests[0] == model.requests[1]
    assert github.reads == [case.issue_number, 3448, case.issue_number, 3448]
    assert {location.commit for location in repository.reads} == {
        case.repository_commit
    }


@pytest.mark.parametrize("changed_number", [12081, 3448])
def test_changed_issue_content_is_flagged_before_model_or_source_reads(
    changed_number: int,
) -> None:
    case, github, repository = synthetic_case()
    original = github.issues[changed_number]
    github.issues[changed_number] = issue_search.IssueRecord(
        original.number,
        original.title,
        original.body + "\nA later edit reveals the answer.",
        original.created_at,
    )
    model = ObservedModel()

    with pytest.raises(CaseFlagged, match="opening content changed"):
        replay_case(
            case, issue_source=github, source_reader=repository, model_client=model
        )
    assert model.requests == []
    assert repository.reads == []


def test_unavailable_issue_is_flagged_before_scoring() -> None:
    case, github, repository = synthetic_case()
    del github.issues[3448]
    model = ObservedModel()

    with pytest.raises(CaseFlagged, match="is unavailable"):
        replay_case(
            case, issue_source=github, source_reader=repository, model_client=model
        )
    assert model.requests == []
    assert repository.reads == []


def test_replay_never_fetches_live_ci_for_an_opening_pr_link(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case, github, repository = synthetic_case()
    original = github.issues[case.issue_number]
    linked = issue_search.IssueRecord(
        original.number,
        original.title,
        original.body + "\nRelevant PR: https://github.com/pytest-dev/pytest/pull/1234",
        original.created_at,
    )
    github.issues[case.issue_number] = linked
    data = case.model_dump()
    data["opening_content_sha256"] = content_hash(linked)
    case = HistoricalCase.model_validate(data)
    live_calls: list[ci.CILink] = []

    def live_checks(self: ci.PublicCISource, link: ci.CILink) -> ci.CIInspection:
        live_calls.append(link)
        return ci.CIInspection(())

    monkeypatch.setattr(ci.PublicCISource, "get_checks", live_checks)
    model = ObservedModel()
    report = replay_case(
        case, issue_source=github, source_reader=repository, model_client=model
    )

    assert live_calls == []
    assert report.ci_results == []
    assert any(item.field == "ci_results" for item in report.abstentions)
    assert all(
        "CI check" not in item.text for item in model.requests[0].reply_statements
    )


def test_case_rejects_repository_evidence_after_opening() -> None:
    data = load_case().model_dump()
    data["repository_commit_at"] = datetime(2024, 3, 7, tzinfo=UTC)

    with pytest.raises(ValueError, match="predate the opening cutoff"):
        HistoricalCase.model_validate(data)
