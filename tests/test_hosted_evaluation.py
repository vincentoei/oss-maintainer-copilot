"""Hosted-reference behavior at the agreed runner and capped-client seams."""

import io
import json
from dataclasses import replace
from pathlib import Path
from typing import Any
from urllib.request import Request

import pytest
from test_local_evaluation import RecordedEvidence

from maintainer_copilot.evaluation import score_report
from maintainer_copilot.hosted_evaluation import (
    MODEL,
    HostedBudget,
    HostedModel,
    evaluate_hosted_reference,
    main,
)
from maintainer_copilot.model import ModelResponse, ModelUnavailable
from maintainer_copilot.replay import candidate_references, replay_case
from maintainer_copilot.source import PublicRepositorySource
from maintainer_copilot.workflow_comparison import fingerprint


def baseline_for(evidence: RecordedEvidence, path: Path) -> Path:
    case = evidence.case
    report = replay_case(case, commit_source=evidence, issue_source=evidence)
    path.write_text(
        json.dumps(
            {
                "status": "complete",
                "catalog_sha256": fingerprint([case.model_dump(mode="json")]),
                "summary": {"methods": {"fixed_rag": {"cases": 1, "completed": 1}}},
                "cases": [
                    {
                        "method": "fixed_rag",
                        "issue_number": case.issue_number,
                        "opening_cutoff": case.opening_cutoff.isoformat(),
                        "repository_commit": case.repository_commit,
                        "opening_content_sha256": case.opening_content_sha256,
                        "candidate_numbers": [
                            r.number for r in candidate_references(case, [case])
                        ],
                        "scores": score_report(case, report),
                        "error": None,
                    }
                ],
            }
        )
    )
    return path


def hosted_response(output: object) -> io.BytesIO:
    return io.BytesIO(
        json.dumps(
            {
                "model": MODEL,
                "id": "recorded-provider-request",
                "choices": [{"message": {"content": json.dumps(output)}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 10},
            }
        ).encode()
    )


def test_invalid_hosted_selection_is_not_scored_as_a_successful_reference(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = RecordedEvidence()

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        return hosted_response(
            {
                "issue_type": "type: invalid",
                "quote_index": 0,
                "reply_citation_ids": [],
            }
        )

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    result: dict[str, Any] = evaluate_hosted_reference(
        tmp_path / "run",
        "test-secret",
        cases=[evidence.case],
        baseline_path=baseline_for(evidence, tmp_path / "baseline.json"),
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    assert result["status"] == "incomplete"
    assert result["cases"][0]["scores"] is None
    assert result["cases"][0]["error"]
    assert result["cases"][0]["hosted_report"]["status"] == "partial"
    assert result["accounting"]["request_count"] == 1
    assert result["accounting"]["cost_micro_usd"] == 280
    assert result["local_fixed_aggregate"]["cases"] == 0
    assert result["hosted_paired_aggregate"]["cases"] == 0
    assert result["excluded_from_pairing"][0]["issue_number"] == 12224


def test_openrouter_request_pins_provider_and_records_actual_reported_cost(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert request.full_url == "https://openrouter.ai/api/v1/chat/completions"
        assert request.get_header("Authorization") == "Bearer test-router-secret"
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        assert payload["model"] == "openai/gpt-4.1"
        assert payload["provider"]["only"] == ["openai"]
        assert payload["provider"]["allow_fallbacks"] is False
        assert payload["provider"]["max_price"] == {"prompt": 2, "completion": 8}
        response = json.loads(hosted_response({}).read())
        response["model"] = "openai/gpt-4.1"
        response["provider"] = "OpenAI"
        response["usage"]["cost"] = 0.00028
        return io.BytesIO(json.dumps(response).encode())

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    budget = HostedBudget(tmp_path, provider="openrouter")
    client = HostedModel("test-router-secret", budget, 123, provider="openrouter")
    result = client.generate_json(
        "select",
        {},
        max_tokens=256,
        response_schema={"type": "object", "properties": {}},
    )
    assert isinstance(result, ModelResponse)
    assert budget.summary()["reported_cost_micro_usd"] == 280
    assert client.calls[0]["returned_model"] == "openai/gpt-4.1"
    assert client.calls[0]["returned_provider"] == "OpenAI"
    assert "test-router-secret" not in budget.path.read_text()


def test_monetary_cap_refuses_dispatch_before_five_dollars_even_after_restart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        summary = HostedBudget(tmp_path).summary()
        assert summary["request_count"] == dispatches
        assert summary["reserved_micro_usd"] < 5_000_000
        return hosted_response({})

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    for number in range(50):
        client = HostedModel("test-secret", HostedBudget(tmp_path), number)
        try:
            client.generate_json(
                "x" * 100_000,
                {},
                max_tokens=256,
                response_schema={"type": "object", "properties": {}},
            )
        except ModelUnavailable as exc:
            assert "budget exhausted" in str(exc)
            break
    assert 20 <= dispatches < 25  # Monetary cap is reached before the 50-call cap.
    summary = HostedBudget(tmp_path).summary()
    assert summary["request_count"] == dispatches
    assert summary["reserved_micro_usd"] < 5_000_000
    assert summary["cost_micro_usd"] == dispatches * 280


@pytest.mark.parametrize("failure", ["timeout", "missing_usage", "wrong_model"])
def test_ambiguous_provider_failure_retains_charge_and_stops_future_requests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        if failure == "timeout":
            raise TimeoutError("private provider message")
        response = json.loads(hosted_response({}).read())
        if failure == "missing_usage":
            del response["usage"]
        else:
            response["model"] = "unexpected-model"
        return io.BytesIO(json.dumps(response).encode())

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    for number in (1, 2):
        client = HostedModel("test-secret", HostedBudget(tmp_path), number)
        with pytest.raises(ModelUnavailable, match="halted"):
            client.generate_json(
                "select",
                {},
                max_tokens=256,
                response_schema={"type": "object", "properties": {}},
            )
    assert dispatches == 1
    summary = HostedBudget(tmp_path).summary()
    assert summary["request_count"] == 1
    assert summary["reserved_micro_usd"] > 0
    if failure != "wrong_model":
        assert summary["cost_micro_usd"] is None
        assert summary["input_tokens"] is None
    assert "private provider message" not in HostedBudget(tmp_path).path.read_text()


def test_runner_pairs_same_cutoff_and_keeps_model_output_separate_from_annotation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = RecordedEvidence()

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        user = json.loads(payload["messages"][1]["content"])
        assert not any(
            forbidden in user for forbidden in ("expected_outcome", "human_review")
        )
        assert user["issue_body"] == evidence.opening.body
        return hosted_response(
            {"issue_type": None, "quote_index": None, "reply_citation_ids": []}
        )

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    directory = tmp_path / "run"
    result = evaluate_hosted_reference(
        directory,
        "test-secret",
        cases=[evidence.case],
        baseline_path=baseline_for(evidence, tmp_path / "baseline.json"),
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    row = result["cases"][0]
    assert result["model_version"] == "gpt-4.1-2025-04-14"
    assert result["status"] == "complete"
    assert row["opening_cutoff"] == evidence.case.opening_cutoff.isoformat()
    assert row["repository_commit"] == evidence.case.repository_commit
    assert row["hosted_report"]["issue_type"] is None
    assert row["expected_outcome"]["issue_type"] == "type: enhancement"
    assert row["scores"]["issue_type"]["correct"] is False
    assert row["case_review"]["reviewer"] == evidence.case.human_review.reviewer
    assert result["paired_scoreable_cases"] == 1
    assert result["local_fixed_aggregate"]["cases"] == 1
    assert result["hosted_paired_aggregate"]["cases"] == 1
    assert "test-secret" not in (directory / "results.json").read_text()
    assert result["accounting"]["input_tokens"] == 100
    assert result["accounting"]["output_tokens"] == 10


def test_changed_opening_is_retained_unscored_without_a_hosted_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = RecordedEvidence()
    baseline = baseline_for(evidence, tmp_path / "baseline.json")
    evidence.opening = replace(evidence.opening, body="later edited contributor text")

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        pytest.fail("Flagged openings must not reach the paid endpoint")

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    result = evaluate_hosted_reference(
        tmp_path / "run",
        "test-secret",
        cases=[evidence.case],
        baseline_path=baseline,
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    assert len(result["cases"]) == 1
    assert result["cases"][0]["scores"] is None
    assert result["preflight"][0]["eligible"] is False
    assert result["accounting"]["request_count"] == 0
    assert result["paired_scoreable_cases"] == 0
    assert result["local_fixed_aggregate"]["cases"] == 0


def test_openrouter_run_refuses_changed_price_before_inference_or_directory_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    evidence = RecordedEvidence()

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert request.full_url.endswith("/models/openai/gpt-4.1/endpoints")
        return io.BytesIO(
            json.dumps(
                {
                    "data": {
                        "endpoints": [
                            {
                                "tag": "openai",
                                "name": "OpenAI | openai/gpt-4.1-2025-04-14",
                                "pricing": {
                                    "prompt": "0.000003",
                                    "completion": "0.000008",
                                },
                            }
                        ]
                    }
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    directory = tmp_path / "run"
    with pytest.raises(ValueError, match="pricing"):
        evaluate_hosted_reference(
            directory,
            "test-router-secret",
            cases=[evidence.case],
            baseline_path=baseline_for(evidence, tmp_path / "baseline.json"),
            commit_source=evidence,
            issue_source=evidence,
            source_reader=PublicRepositorySource(),
            provider="openrouter",
        )
    assert not directory.exists()


def test_interrupted_request_halts_accounting_across_restart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        raise KeyboardInterrupt

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    schema: dict[str, object] = {"type": "object", "properties": {}}
    with pytest.raises(KeyboardInterrupt):
        HostedModel("secret", HostedBudget(tmp_path), 1).generate_json(
            "select", {}, max_tokens=256, response_schema=schema
        )
    with pytest.raises(ModelUnavailable, match="halted"):
        HostedModel("secret", HostedBudget(tmp_path), 2).generate_json(
            "select", {}, max_tokens=256, response_schema=schema
        )
    assert dispatches == 1
    assert HostedBudget(tmp_path).summary()["cost_micro_usd"] is None


@pytest.mark.parametrize("provider", ["openai", "openrouter"])
def test_cli_missing_credentials_refuses_before_creating_a_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, provider: str
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    directory = tmp_path / "run"
    monkeypatch.setattr(
        "sys.argv",
        ["hosted_evaluation", "--provider", provider, "--directory", str(directory)],
    )
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    assert not directory.exists()


@pytest.mark.parametrize("change", ["cutoff", "catalog", "review", "existing"])
def test_runner_refuses_changed_comparison_or_existing_directory_before_dispatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, change: str
) -> None:
    evidence = RecordedEvidence()
    baseline = baseline_for(evidence, tmp_path / "baseline.json")
    data = json.loads(baseline.read_text())
    directory = tmp_path / "run"
    if change == "cutoff":
        data["cases"][0]["opening_cutoff"] = "2020-01-01T00:00:00+00:00"
    elif change == "catalog":
        data["catalog_sha256"] = "0" * 64
    elif change == "review":
        evidence.case = evidence.case.model_copy(
            update={
                "human_review": evidence.case.human_review.model_copy(
                    update={"status": "pending"}
                )
            }
        )
    else:
        directory.mkdir()
        (directory / "preserve.txt").write_text("original")
    baseline.write_text(json.dumps(data))

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        pytest.fail("Invalid runs must not reach the provider")

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    with pytest.raises((ValueError, FileExistsError)):
        evaluate_hosted_reference(
            directory,
            "test-secret",
            cases=[evidence.case],
            baseline_path=baseline,
            commit_source=evidence,
            issue_source=evidence,
            source_reader=PublicRepositorySource(),
        )
    if change == "existing":
        assert (directory / "preserve.txt").read_text() == "original"
    else:
        assert not directory.exists()


def test_crash_between_failed_response_and_halt_marker_cannot_reopen_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        raise TimeoutError

    monkeypatch.setattr("maintainer_copilot.hosted_evaluation.urlopen", endpoint)
    schema: dict[str, object] = {"type": "object", "properties": {}}
    budget = HostedBudget(tmp_path)
    with pytest.raises(ModelUnavailable):
        HostedModel("secret", budget, 1).generate_json(
            "select", {}, max_tokens=256, response_schema=schema
        )
    # Model a process death after the response fsync, before the halt-marker write.
    rows = budget.records()
    budget.path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows if row["event"] != "halted")
    )
    with pytest.raises(ModelUnavailable):
        HostedModel("secret", HostedBudget(tmp_path), 2).generate_json(
            "select", {}, max_tokens=256, response_schema=schema
        )
    assert dispatches == 1
    assert HostedBudget(tmp_path).summary()["halted"] is True
