"""Historical replay contract: current GitHub activity cannot enter a report."""

import io
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request

import pytest
from pydantic import ValidationError

from maintainer_copilot import ci, issue_search
from maintainer_copilot import source as repository_source
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.replay import (
    CaseFlagged,
    ControlledReplayModel,
    GitHubCommitSource,
    HistoricalCase,
    RepositoryCommit,
    candidate_references,
    content_hash,
    load_case,
    load_cases,
    replay_case,
)
from maintainer_copilot.triage import IssueUnderReview


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
    def __init__(
        self,
        commit: str,
        committed_at: datetime,
        pinned_reader: repository_source.SourceReader | None = None,
    ) -> None:
        self.commit = commit
        self.committed_at = committed_at
        self.pinned_reader = pinned_reader
        self.later_code = "a post-cutoff fix"
        self.later_documentation = "a post-cutoff docs change"
        self.reads: list[repository_source.SourceLocation] = []
        self.commit_reads: list[str] = []

    def get_commit(self, sha: str) -> RepositoryCommit:
        self.commit_reads.append(sha)
        return RepositoryCommit(sha, self.committed_at)

    def get_excerpt(
        self, location: repository_source.SourceLocation
    ) -> repository_source.SourceExcerpt:
        self.reads.append(location)
        if location.commit != self.commit:
            later_text = (
                self.later_documentation
                if location.path == "doc/en/how-to/capture-stdout-stderr.rst"
                else self.later_code
            )
            return repository_source.SourceExcerpt(
                commit=location.commit,
                path=location.path,
                line=location.line,
                start_line=location.line,
                end_line=location.line,
                lines=[later_text],
                source_url=location.source_url,
            )
        if self.pinned_reader is not None:
            return self.pinned_reader.get_excerpt(location)
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
        ChangingRepository(case.repository_commit, case.repository_commit_at),
    )


@pytest.mark.parametrize("body_length", [16_001, 65_536])
def test_verified_replay_preserves_long_opening_without_relaxing_live_limit(
    body_length: int,
) -> None:
    case, github, repository = synthetic_case()
    body = ("traceback line\n" * body_length)[
        : body_length - len(" opening end")
    ] + " opening end"
    reviewed = issue_search.IssueRecord(
        case.issue_number, case.opening_title, body, case.opening_cutoff
    )
    github.issues[case.issue_number] = reviewed
    case = HistoricalCase.model_validate(
        {**case.model_dump(), "opening_content_sha256": content_hash(reviewed)}
    )
    observed = ObservedModel()

    with pytest.raises(ValidationError, match="16000"):
        IssueUnderReview(title=reviewed.title, body=body)

    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=observed,
    )

    assert report.status == "complete"
    assert observed.requests[0].issue_body == body


def test_replay_flags_openings_above_historical_limit_before_model_call() -> None:
    case, github, repository = synthetic_case()
    reviewed = issue_search.IssueRecord(
        case.issue_number, case.opening_title, "x" * 65_537, case.opening_cutoff
    )
    github.issues[case.issue_number] = reviewed
    case = HistoricalCase.model_validate(
        {**case.model_dump(), "opening_content_sha256": content_hash(reviewed)}
    )
    observed = ObservedModel()

    with pytest.raises(CaseFlagged, match="historical replay input limits"):
        replay_case(
            case,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            model_client=observed,
        )

    assert observed.requests == []


@pytest.mark.parametrize("recovers", [True, False])
def test_replay_retries_commit_timeout_once_before_flagging(
    monkeypatch: pytest.MonkeyPatch, recovers: bool
) -> None:
    case, github, repository = synthetic_case()
    attempts: list[str] = []

    def commit_response(request: Request, *, timeout: int) -> io.BytesIO:
        assert timeout == 8
        attempts.append(request.full_url)
        if not recovers or len(attempts) == 1:
            raise TimeoutError("commit lookup timed out")
        return io.BytesIO(
            json.dumps(
                {
                    "sha": case.repository_commit,
                    "committer": {"date": case.repository_commit_at.isoformat()},
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.replay.urlopen", commit_response)
    observed = ObservedModel()

    def replay() -> None:
        replay_case(
            case,
            commit_source=GitHubCommitSource(),
            issue_source=github,
            source_reader=repository,
            model_client=observed,
        )

    if recovers:
        replay()
        assert len(observed.requests) == 1
    else:
        with pytest.raises(CaseFlagged, match="commit is unavailable"):
            replay()
        assert observed.requests == []
        assert github.reads == []
    assert (
        attempts
        == [
            f"https://api.github.com/repos/pytest-dev/pytest/git/commits/{case.repository_commit}"
        ]
        * 2
    )


def test_replay_ignores_post_cutoff_activity_in_every_evidence_channel() -> None:
    case, github, repository = synthetic_case()
    model = ObservedModel()
    later_source = repository_source.SourceLocation(
        commit="f" * 40, path="src/_pytest/capture.py", line=935
    )
    later_documentation = repository_source.SourceLocation(
        commit="f" * 40,
        path="doc/en/how-to/capture-stdout-stderr.rst",
        line=110,
    )
    old_later_code = repository.get_excerpt(later_source).lines
    old_later_docs = repository.get_excerpt(later_documentation).lines
    repository.reads.clear()

    first = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=model,
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
    assert repository.get_excerpt(later_source).lines != old_later_code
    assert repository.get_excerpt(later_documentation).lines != old_later_docs
    repository.reads.clear()

    second = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=model,
    )
    assert first.model_dump(exclude={"trace_id"}) == second.model_dump(
        exclude={"trace_id"}
    )
    assert len(model.requests) == 2
    assert model.requests[0] == model.requests[1]
    assert github.reads == [case.issue_number, 3448, case.issue_number, 3448]
    assert repository.commit_reads == [case.repository_commit] * 2
    assert {location.commit for location in repository.reads} == {
        case.repository_commit
    }


def test_keyword_baseline_filters_the_frozen_candidate_by_query_terms() -> None:
    case, github, repository = synthetic_case()
    earlier = github.issues[case.earlier_issue.number]
    github.issues[earlier.number] = issue_search.IssueRecord(
        earlier.number,
        "Some report",
        "capfd.readouterr() resets streams",
        earlier.created_at,
    )
    data = case.model_dump()
    data["earlier_issue"]["content_sha256"] = content_hash(
        github.issues[earlier.number]
    )
    case = HistoricalCase.model_validate(data)

    paired = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=ControlledReplayModel(),
    )
    # The paired input still supports a capture connection, but deliberately
    # differs from the query's title terms. Filtering is a retrieval concern.
    data = case.model_dump()
    review = github.issues[case.issue_number]
    github.issues[case.issue_number] = issue_search.IssueRecord(
        review.number,
        "Feature: preserve retained buffers",
        review.body,
        review.created_at,
    )
    data["opening_title"] = github.issues[case.issue_number].title
    data["opening_content_sha256"] = content_hash(github.issues[case.issue_number])
    case = HistoricalCase.model_validate(data)
    filtered = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=ControlledReplayModel(),
        keyword_filter=True,
    )

    assert [item.issue_number for item in paired.related_issues] == [earlier.number]
    assert filtered.related_issues == []


def test_keyword_baseline_searches_verified_openings_before_the_cutoff() -> None:
    case, github, repository = synthetic_case()
    earlier_opening = issue_search.IssueRecord(
        10000,
        case.opening_title,
        github.issues[case.issue_number].body,
        datetime(2024, 3, 5, tzinfo=UTC),
    )
    data = case.model_dump()
    data["issue_number"] = earlier_opening.number
    data["opening_title"] = earlier_opening.title
    data["opening_cutoff"] = earlier_opening.created_at
    data["opening_content_sha256"] = content_hash(earlier_opening)
    earlier_case = HistoricalCase.model_validate(data)
    later = issue_search.IssueRecord(
        13000,
        "A later fix reveals the outcome",
        "This was fixed",
        datetime(2024, 3, 7, tzinfo=UTC),
    )
    data["issue_number"] = later.number
    data["opening_title"] = later.title
    data["opening_cutoff"] = later.created_at
    data["opening_content_sha256"] = content_hash(later)
    later_case = HistoricalCase.model_validate(data)
    github.issues[earlier_opening.number] = earlier_opening
    catalog = [earlier_case, later_case]

    assert {ref.number for ref in candidate_references(case, catalog)} == {3448, 10000}
    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=ControlledReplayModel(),
        keyword_filter=True,
        candidate_catalog=catalog,
    )

    assert 10000 in {item.issue_number for item in report.duplicate_candidates}
    assert 13000 not in github.reads
    assert any(str(item.source_url) == earlier_opening.url for item in report.citations)

    github.issues[earlier_opening.number] = issue_search.IssueRecord(
        earlier_opening.number,
        earlier_opening.title,
        earlier_opening.body + "\nA post-cutoff edit",
        earlier_opening.created_at,
    )
    observed = ObservedModel()
    with pytest.raises(CaseFlagged, match="opening content changed"):
        replay_case(
            case,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            model_client=observed,
            keyword_filter=True,
            candidate_catalog=catalog,
        )
    assert observed.requests == []


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
            case,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            model_client=model,
        )
    assert model.requests == []
    assert repository.reads == []


def test_unavailable_issue_is_flagged_before_scoring() -> None:
    case, github, repository = synthetic_case()
    del github.issues[3448]
    model = ObservedModel()

    with pytest.raises(CaseFlagged, match="is unavailable"):
        replay_case(
            case,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            model_client=model,
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
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=model,
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


def test_published_fifty_cases_preserve_coverage_and_group_shared_families() -> None:
    cases = load_cases()
    new_case_numbers = {
        12231,
        12242,
        12249,
        12255,
        12263,
        12273,
        12278,
        12281,
        12287,
        12290,
        12293,
        12298,
        12300,
        12303,
        12305,
        12307,
        12308,
        12312,
        12323,
        12328,
        12351,
        12352,
        12357,
        12360,
        12363,
        12366,
        12367,
        12371,
        12376,
        12377,
    }
    assert {case.issue_number for case in cases} == {
        7312,
        10156,
        12053,
        12072,
        12079,
        12081,
        12083,
        12116,
        12146,
        12189,
        12197,
        12201,
        12203,
        12204,
        12216,
        12219,
        12223,
        12224,
        12226,
        12228,
    } | new_case_numbers
    assert len({case.issue_family_id for case in cases}) == 46
    assert all(case.human_review.status == "confirmed" for case in cases)
    families = {case.issue_number: case.issue_family_id for case in cases}
    assert families[12263] == families[12273] == families[12278]
    assert families[12303] == families[12287]
    assert families[12376] == families[10156]
    assert any(case.expected_outcome.missing_details for case in cases)
    assert any(not case.expected_outcome.missing_details for case in cases)
    assert [case.expected_outcome.earlier_issue_relationship for case in cases].count(
        "duplicate_candidate"
    ) >= 1
    assert [case.expected_outcome.earlier_issue_relationship for case in cases].count(
        "nonduplicate"
    ) >= 1
    assert [case.expected_outcome.earlier_issue_relationship for case in cases].count(
        "uncertain"
    ) >= 1


@pytest.mark.parametrize(
    "number", [case.issue_number for case in load_cases() if case.issue_number != 12081]
)
def test_other_recorded_cases_replay_without_annotation_leakage(number: int) -> None:
    recorded = next(case for case in load_cases() if case.issue_number == number)
    reviewed = issue_search.IssueRecord(
        number,
        recorded.opening_title,
        "Opening report with a concrete pytest behavior and example.",
        recorded.opening_cutoff,
    )
    earlier = issue_search.IssueRecord(
        recorded.earlier_issue.number,
        "Earlier pytest issue with similar terminology",
        "A different report available at the opening cutoff.",
        recorded.earlier_issue.created_at,
    )
    data = recorded.model_dump()
    data["opening_content_sha256"] = content_hash(reviewed)
    data["earlier_issue"]["content_sha256"] = content_hash(earlier)
    data["expected_outcome"]["rationale"] = "SECRET LATER ANNOTATION"
    case = HistoricalCase.model_validate(data)
    github = ChangingGitHub(reviewed, earlier)
    repository = ChangingRepository(case.repository_commit, case.repository_commit_at)
    model = ObservedModel()

    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=model,
    )

    assert report.status == "complete"
    assert repository.reads == []
    assert len(model.requests) == 1
    assert "SECRET LATER ANNOTATION" not in str(model.requests[0])
    assert all(
        case.repository_commit in str(citation.source_url)
        for citation in report.citations
        if "/blob/" in str(citation.source_url)
    )


def test_confirmation_requires_a_named_reviewer_and_time() -> None:
    data = load_case().model_dump()
    data["human_review"]["reviewer"] = None
    data["human_review"]["confirmed_at"] = None
    with pytest.raises(ValueError, match="require a reviewer"):
        HistoricalCase.model_validate(data)


def test_forged_pre_cutoff_timestamp_cannot_admit_a_later_commit() -> None:
    case, github, repository = synthetic_case()
    data = case.model_dump()
    data["repository_commit"] = "f" * 40
    forged = HistoricalCase.model_validate(data)
    repository.committed_at = datetime(2024, 3, 7, tzinfo=UTC)
    model = ObservedModel()

    with pytest.raises(CaseFlagged, match="commit does not match the cutoff"):
        replay_case(
            forged,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            model_client=model,
        )
    assert repository.commit_reads == [forged.repository_commit]
    assert github.reads == []
    assert repository.reads == []
    assert model.requests == []


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_REPLAY") != "1", reason="requires public GitHub access"
)
def test_all_recorded_cases_replay_with_public_opening_text() -> None:
    for case in load_cases():
        report = replay_case(case)
        assert report.status == "complete", case.issue_number


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_REPLAY") != "1", reason="requires public GitHub access"
)
def test_recorded_case_ignores_later_activity_with_public_opening_text() -> None:
    """Use the checked-in case without copying contributor issue bodies into Git."""
    case = load_case()
    public_issues = issue_search.GitHubIssueSource()
    github = ChangingGitHub(
        public_issues.get_issue(case.issue_number),
        public_issues.get_issue(case.earlier_issue.number),
    )
    repository = ChangingRepository(
        case.repository_commit,
        case.repository_commit_at,
        pinned_reader=repository_source.PublicRepositorySource(),
    )
    model = ObservedModel()
    first = replay_case(
        case,
        commit_source=GitHubCommitSource(),
        issue_source=github,
        source_reader=repository,
        model_client=model,
    )
    assert first.status == "complete"
    assert first.documentation_claims and first.source_claims
    assert [item.issue_number for item in first.related_issues] == [3448]
    github.comments.append("later maintainer reply reveals a fix")
    github.labels.append("type: enhancement")
    github.duplicate_decisions.append("duplicate of #3448")
    github.later_search_results.append("later duplicate decision")
    later_location = repository_source.SourceLocation(
        commit="f" * 40, path="src/_pytest/capture.py", line=935
    )
    later_doc_location = repository_source.SourceLocation(
        commit="f" * 40,
        path="doc/en/how-to/capture-stdout-stderr.rst",
        line=110,
    )
    before_later_code = repository.get_excerpt(later_location).lines
    before_later_docs = repository.get_excerpt(later_doc_location).lines
    repository.later_code = "readouterr now preserves all output"
    repository.later_documentation = "later documentation describes the fix"
    assert repository.get_excerpt(later_location).lines != before_later_code
    assert repository.get_excerpt(later_doc_location).lines != before_later_docs
    repository.reads.clear()

    second = replay_case(
        case,
        commit_source=GitHubCommitSource(),
        issue_source=github,
        source_reader=repository,
        model_client=model,
    )
    assert first.model_dump(exclude={"trace_id"}) == second.model_dump(
        exclude={"trace_id"}
    )
    assert model.requests[0] == model.requests[1]
    assert {location.commit for location in repository.reads} == {
        case.repository_commit
    }


def test_verified_opening_citations_still_reject_newer_issues() -> None:
    from pydantic import HttpUrl

    from maintainer_copilot.evaluation import score_report

    case, github, repository = synthetic_case()
    reviewed = github.issues[case.issue_number]
    github.issues[case.issue_number] = issue_search.IssueRecord(
        reviewed.number,
        reviewed.title,
        reviewed.body + "\npytest 8.1.1\npluggy 1.4.0\n"
        "platform linux -- pytest-8.0.0, pluggy-1.3.0\n",
        reviewed.created_at,
    )
    data = case.model_dump()
    data["opening_content_sha256"] = content_hash(github.issues[case.issue_number])
    case = HistoricalCase.model_validate(data)
    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
    )
    opening = next(
        c
        for c in report.citations
        if str(c.source_url).endswith(f"/issues/{case.issue_number}")
    )
    assert "conflicting version evidence" in report.draft_reply
    assert score_report(case, report)["citation_validity"]["valid"]
    opening.source_url = HttpUrl(
        f"https://github.com/pytest-dev/pytest/issues/{case.issue_number + 1}"
    )
    assert not score_report(case, report)["citation_validity"]["valid"]


def test_live_registry_removal_does_not_change_historical_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from maintainer_copilot.registry import get_registry

    monkeypatch.setenv("REPOSITORY_REGISTRY_PATH", str(tmp_path / "registry.sqlite3"))
    get_registry().remove("pytest-default")
    case, github, repository = synthetic_case()
    report = replay_case(
        case, commit_source=repository, issue_source=github, source_reader=repository
    )
    assert report.context.repository == "pytest-dev/pytest"
    assert report.context.revision == case.repository_commit
    assert all(
        case.repository_commit in str(c.source_url) or "/issues/" in str(c.source_url)
        for c in report.citations
    )


def test_foreign_opening_with_matching_hash_is_flagged_before_inference() -> None:
    case, github, repository = synthetic_case()
    record = github.issues[case.issue_number]

    # The public reader must establish repository provenance as well as content.
    class ForeignReader:
        def get_issue(self, number: int) -> issue_search.IssueRecord:
            return issue_search.IssueRecord(
                record.number,
                record.title,
                record.body,
                record.created_at,
                "other/tool",
            )

        def search_issues(
            self, query: str, created_before: datetime
        ) -> list[issue_search.IssueRecord]:
            raise AssertionError("No live search in historical replay")

    with pytest.raises(CaseFlagged, match="repository"):
        replay_case(
            case,
            commit_source=repository,
            issue_source=ForeignReader(),
            source_reader=repository,
        )
