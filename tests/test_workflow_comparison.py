"""Workflow comparison at the agreed replay and runner boundaries."""

import io
import json
from pathlib import Path
from urllib.request import Request

import pytest
from test_local_evaluation import RecordedEvidence
from test_replay import synthetic_case

from maintainer_copilot.agent import AgentStepRequest
from maintainer_copilot.model import ModelRequest, ModelUnavailable
from maintainer_copilot.replay import CaseFlagged, ControlledReplayModel, replay_case
from maintainer_copilot.source import PublicRepositorySource


def test_request_budget_survives_restart_and_counts_failed_dispatches(
    tmp_path: Path,
) -> None:
    from maintainer_copilot.workflow_comparison import RequestBudget

    budget = RequestBudget(tmp_path)
    budget.reserve("fixed_rag", 12224, {"max_tokens": 256})
    restarted = RequestBudget(tmp_path)
    with pytest.raises(ModelUnavailable, match="budget"):
        restarted.reserve("fixed_rag", 12224, {"max_tokens": 256})


def test_frozen_budget_allows_exactly_twenty_fixed_and_eighty_agent_dispatches(
    tmp_path: Path,
) -> None:
    from maintainer_copilot.workflow_comparison import RequestBudget

    budget = RequestBudget(tmp_path)
    for number in range(20):
        budget.reserve("fixed_rag", number, {"max_tokens": 256})
        for _ in range(4):
            budget.reserve("bounded_agent", number, {"max_tokens": 256})
    for method in ("fixed_rag", "bounded_agent", "keyword_rule"):
        with pytest.raises(ModelUnavailable, match="budget"):
            budget.reserve(method, 99999, {"max_tokens": 256})
    assert len((tmp_path / "requests.jsonl").read_text().splitlines()) == 100


def test_agent_replay_respects_historical_template_availability() -> None:
    case, github, repository = synthetic_case()
    case = case.model_copy(update={"template_profile": "generic"})
    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        agent_client=ReadingAgent(),
    )
    assert report.missing_details == []
    assert all(
        "/.github/ISSUE_TEMPLATE/" not in str(c.source_url) for c in report.citations
    )


def test_comparison_preserves_three_arms_and_reports_actual_inference_cost(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from maintainer_copilot.workflow_comparison import evaluate_comparison

    evidence = RecordedEvidence()

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert timeout == 20 and isinstance(request.data, bytes)
        payload = json.loads(request.data)
        data = json.loads(payload["messages"][1]["content"])
        assert payload["max_tokens"] == 256
        schema = payload["response_format"]["json_schema"]["schema"]
        output = (
            {"tool": "finish", "arguments": {}}
            if "enum" in schema
            else {
                "issue_type": "type: enhancement",
                "issue_type_quote": "Feature",
                "reply_citation_ids": data["required_reply_ids"],
            }
        )
        return io.BytesIO(
            json.dumps(
                {
                    "choices": [{"message": {"content": json.dumps(output)}}],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 10},
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    directory = tmp_path / "comparison"
    artifact = evaluate_comparison(
        directory,
        "http://model.test/v1",
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    summary = artifact["summary"]
    assert len(artifact["cases"]) == 3
    methods = summary["methods"]
    assert methods["keyword_rule"]["resources"]["dispatches"] == 0
    assert methods["fixed_rag"]["resources"]["input_tokens"] == 100
    assert methods["bounded_agent"]["resources"]["input_tokens"] == 200
    assert summary["paired_cases"] == 1
    assert summary["paired_agent_gain"] == 0
    assert summary["decision"]["workflow"] == "fixed_rag"
    assert {r["opening_content_sha256"] for r in artifact["cases"]} == {
        evidence.case.opening_content_sha256
    }
    reviews = json.loads((directory / "human-review.json").read_text())
    assert len(reviews) == 3 and all(r["rating"] is None for r in reviews)
    with pytest.raises(FileExistsError):
        evaluate_comparison(
            directory,
            "http://model.test/v1",
            cases=[evidence.case],
            commit_source=evidence,
            issue_source=evidence,
            source_reader=PublicRepositorySource(),
        )


class ReadingAgent:
    """External model stand-in; never evidence of model quality."""

    def __init__(self) -> None:
        self.inputs: list[object] = []

    def next_step(self, request: AgentStepRequest) -> object:
        self.inputs.append(request)
        used = {item.tool for item in request.observations}
        if "search_earlier_issues" not in used:
            return {
                "tool": "search_earlier_issues",
                "arguments": {"issue_number": request.issue.number},
            }
        if request.issue.source_location and "inspect_source" not in used:
            return {
                "tool": "inspect_source",
                "arguments": request.issue.source_location.model_dump(),
            }
        return {"tool": "finish", "arguments": {}}

    def generate(self, request: ModelRequest) -> object:
        self.inputs.append(request)
        return ControlledReplayModel().generate(request)


def test_agent_replay_uses_only_verified_historical_evidence() -> None:
    case, github, repository = synthetic_case()
    agent = ReadingAgent()
    report = replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        agent_client=agent,
        keyword_filter=True,
    )
    assert report.documentation_claims and report.source_claims
    assert report.related_issues
    assert all(
        case.repository_commit in str(c.source_url)
        for c in report.citations
        if "/blob/" in str(c.source_url)
    )
    assert {location.commit for location in repository.reads} == {
        case.repository_commit
    }
    assert all("later comment" not in str(request) for request in agent.inputs)

    original = github.issues[case.issue_number]
    github.issues[case.issue_number] = type(original)(
        original.number, original.title, "post-cutoff edit", original.created_at
    )
    uncalled = ReadingAgent()
    with pytest.raises(CaseFlagged, match="opening content changed"):
        replay_case(
            case,
            commit_source=repository,
            issue_source=github,
            source_reader=repository,
            agent_client=uncalled,
        )
    assert uncalled.inputs == []


def test_shared_integrity_failure_keeps_all_rows_and_dispatches_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from maintainer_copilot.workflow_comparison import evaluate_comparison

    evidence = RecordedEvidence()
    evidence.opening = type(evidence.opening)(
        evidence.opening.number,
        evidence.opening.title,
        "changed after cutoff",
        evidence.opening.created_at,
    )

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("Integrity failures must not dispatch inference")

    monkeypatch.setattr("maintainer_copilot.model.urlopen", forbidden)
    result = evaluate_comparison(
        tmp_path / "flagged",
        "http://model.test/v1",
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    assert len(result["cases"]) == 3
    assert len({r["error"] for r in result["cases"]}) == 1
    assert all(r["scores"] is None and r["model_calls"] == [] for r in result["cases"])
    assert result["summary"]["paired_cases"] == 0
    assert result["summary"]["missing_pairs"] == 1


def test_failed_inference_keeps_partial_reports_and_unknown_costs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from maintainer_copilot.workflow_comparison import evaluate_comparison

    evidence = RecordedEvidence()

    def offline(*args: object, **kwargs: object) -> None:
        raise OSError("unreachable")

    monkeypatch.setattr("maintainer_copilot.model.urlopen", offline)
    directory = tmp_path / "offline"
    result = evaluate_comparison(
        directory,
        "http://model.test/v1",
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    methods = result["summary"]["methods"]
    for name in ("fixed_rag", "bounded_agent"):
        assert methods[name]["partial_reports"] == 1
        assert methods[name]["model_errors"] >= 1
        assert methods[name]["resources"]["input_tokens"] is None
        assert methods[name]["resources"]["dispatches"] == 1
    assert len((directory / "requests.jsonl").read_text().splitlines()) == 2
