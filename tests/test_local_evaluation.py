"""Local evaluation output at the public runner boundary; no quality claims."""

from datetime import datetime
from pathlib import Path

import pytest

from maintainer_copilot.issue_search import IssueRecord
from maintainer_copilot.local_evaluation import evaluate_local_model, main
from maintainer_copilot.model import (
    ModelRequest,
    ModelResponse,
    ModelUnavailable,
    OpenAICompatibleModel,
)
from maintainer_copilot.replay import (
    HistoricalCase,
    RepositoryCommit,
    content_hash,
    load_cases,
)


class RecordedEvidence:
    def __init__(self) -> None:
        original = next(case for case in load_cases() if case.issue_number == 12224)
        self.opening = IssueRecord(
            original.issue_number,
            "Feature: expose fixture metadata",
            "A new API would help plugins inspect fixture metadata.",
            original.opening_cutoff,
        )
        self.earlier = IssueRecord(
            original.earlier_issue.number,
            "Docs: registering fixtures",
            "Clarify dynamic fixture registration.",
            original.earlier_issue.created_at,
        )
        data = original.model_dump()
        data["opening_title"] = self.opening.title
        data["opening_content_sha256"] = content_hash(self.opening)
        data["earlier_issue"]["content_sha256"] = content_hash(self.earlier)
        self.case = HistoricalCase.model_validate(data)

    def get_commit(self, sha: str) -> RepositoryCommit:
        return RepositoryCommit(sha, self.case.repository_commit_at)

    def get_issue(self, number: int) -> IssueRecord:
        return {self.opening.number: self.opening, self.earlier.number: self.earlier}[
            number
        ]

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        raise AssertionError("historical evaluation must not search live issues")


class EndpointStandIn(OpenAICompatibleModel):
    """Controlled external-model stand-in, used only for deterministic tests."""

    def __init__(self) -> None:
        super().__init__("http://localhost:11434/v1", "test:model")

    def generate(self, request: ModelRequest) -> object:
        return ModelResponse(
            {
                "issue_type": "type: enhancement",
                "issue_type_quote": "Feature",
                "reply_citation_ids": list(request.required_reply_ids),
            },
            input_tokens=123,
            output_tokens=25,
        )


def test_local_runner_scores_model_output_and_keeps_inspectable_evidence() -> None:
    evidence = RecordedEvidence()

    result = evaluate_local_model(
        EndpointStandIn(),
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
    )

    assert result["method"] == "local_model"
    assert result["model_name"] == "test:model"
    assert result["aggregate"]["completed"] == 1
    assert result["aggregate"]["issue_type_accuracy"] == 1.0
    case = result["cases"][0]
    assert case["opening_cutoff"] == evidence.case.opening_cutoff.isoformat()
    assert case["repository_commit"] == evidence.case.repository_commit
    assert case["report"]["issue_type"] == "type: enhancement"
    assert case["model_calls"][0]["response"]["issue_type_quote"] == "Feature"
    assert case["model_calls"][0]["input_tokens"] == 123
    assert case["trace"]["trace_id"] == case["report"]["trace_id"]
    assert case["scores"]["draft_reply_usefulness"]["rating"] is None


def test_model_failure_is_visible_even_when_the_fallback_report_can_be_scored() -> None:
    class OfflineEndpoint(EndpointStandIn):
        def generate(self, request: ModelRequest) -> object:
            raise ModelUnavailable("offline")

    evidence = RecordedEvidence()
    result = evaluate_local_model(
        OfflineEndpoint(),
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
    )

    assert result["aggregate"]["completed"] == 1
    assert result["model_call_count"] == 1
    assert result["model_error_count"] == 1
    case = result["cases"][0]
    assert case["report"]["status"] == "partial"
    assert case["report"]["issue_type"] is None
    assert case["model_calls"][0]["error"] == "Model client failed."
    assert any(
        event["kind"] == "model" and event["status"] == "error"
        for event in case["trace"]["events"]
    )


def test_cli_refuses_to_overwrite_an_existing_evaluation_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifact = tmp_path / "baseline.json"
    artifact.write_text("preserved baseline\n")
    monkeypatch.setattr(
        "sys.argv", ["local_evaluation", "--model", "unused", "--output", str(artifact)]
    )

    with pytest.raises(FileExistsError):
        main()

    assert artifact.read_text() == "preserved baseline\n"
