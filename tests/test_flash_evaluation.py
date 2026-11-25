"""Flash references at the agreed capped-client and evaluation-runner seams."""

import io
import json
from dataclasses import replace
from pathlib import Path
from typing import Any
from urllib.request import Request

import pytest
from test_hosted_evaluation import baseline_for
from test_local_evaluation import RecordedEvidence

from maintainer_copilot.flash_evaluation import (
    FLASH_MODELS,
    FlashBudget,
    FlashModel,
    evaluate_flash_reference,
)
from maintainer_copilot.model import ModelResponse, ModelUnavailable
from maintainer_copilot.source import PublicRepositorySource


@pytest.mark.parametrize("name", ["deepseek", "glm"])
def test_selected_flash_model_pins_provider_and_accounts_for_reasoning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    profile = FLASH_MODELS[name]

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        assert payload["model"] == profile.model_id
        assert payload["max_tokens"] == 4096
        assert payload["reasoning"] == {"effort": "low"}
        assert payload["provider"]["only"] == [profile.provider_slug]
        assert payload["provider"]["allow_fallbacks"] is False
        return io.BytesIO(
            json.dumps(
                {
                    "id": "recorded-request",
                    "model": profile.model_id,
                    "provider": profile.provider_name,
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": "{}"}}
                    ],
                    "usage": {
                        "prompt_tokens": 100,
                        "completion_tokens": 200,
                        "completion_tokens_details": {"reasoning_tokens": 190},
                        "cost": 0.0001,
                    },
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.flash_evaluation.urlopen", endpoint)
    budget = FlashBudget(tmp_path, prior_reserved_micro_usd=1_183_980)
    client = FlashModel("test-secret", profile, budget, 123)
    result = client.generate_json(
        "select",
        {},
        max_tokens=256,
        response_schema={"type": "object", "properties": {}},
    )
    assert isinstance(result, ModelResponse)
    assert result.output_tokens == 200
    assert client.calls[0]["reasoning_tokens"] == 190
    assert budget.summary()["reported_cost_micro_usd"] == 100
    assert budget.summary()["combined_reserved_micro_usd"] > 1_183_980
    assert "test-secret" not in budget.path.read_text()


@pytest.mark.parametrize("condition", ["valid", "changed", "invalid_selection"])
def test_runner_keeps_shared_eligibility_and_distinguishes_failed_predictions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, condition: str
) -> None:
    evidence = RecordedEvidence()
    baseline = baseline_for(evidence, tmp_path / "baseline.json")
    data = json.loads(baseline.read_text())
    prior = tmp_path / "prior"
    prior.mkdir()
    (prior / "hosted-requests.jsonl").write_text("")
    (prior / "results.json").write_text(
        json.dumps({**data, "accounting": {"reserved_micro_usd": 0}})
    )
    if condition == "changed":
        evidence.opening = replace(evidence.opening, body="edited after opening")

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        if request.get_method() == "POST":
            assert condition != "changed", "Flagged evidence must not reach inference"
            assert isinstance(request.data, bytes)
            payload = json.loads(request.data)
            p = next(p for p in FLASH_MODELS.values() if p.model_id == payload["model"])
            user = json.loads(payload["messages"][1]["content"])
            assert "expected_outcome" not in user and "human_review" not in user
            assert user["issue_body"] == evidence.opening.body
            output: dict[str, Any] = {
                "type_evidence_index": 999
                if condition == "invalid_selection"
                else None,
                "reply_citation_ids": [],
            }
            return io.BytesIO(
                json.dumps(
                    {
                        "model": p.model_id,
                        "provider": p.provider_name,
                        "choices": [
                            {
                                "finish_reason": "stop",
                                "message": {"content": json.dumps(output)},
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 100,
                            "completion_tokens": 200,
                            "cost": 0.0001,
                        },
                    }
                ).encode()
            )
        p = next(p for p in FLASH_MODELS.values() if p.model_id in request.full_url)
        return io.BytesIO(
            json.dumps(
                {
                    "data": {
                        "id": p.model_id,
                        "endpoints": [
                            {
                                "tag": p.provider_slug,
                                "name": p.version,
                                "provider_name": p.provider_name,
                                "pricing": {
                                    "prompt": str(p.input_nano_usd / 1e9),
                                    "completion": str(p.output_nano_usd / 1e9),
                                },
                                "supported_parameters": [
                                    "reasoning",
                                    "response_format",
                                    "structured_outputs",
                                    "max_tokens",
                                    "temperature",
                                ],
                            }
                        ],
                    }
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.flash_evaluation.urlopen", endpoint)
    result = evaluate_flash_reference(
        tmp_path / "run",
        "test-secret",
        cases=[evidence.case],
        baseline_path=baseline,
        prior_run=prior,
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    assert result["status"] == ("complete" if condition == "valid" else "incomplete")
    assert len(result["cases"]) == 2
    assert all(
        (r["scores"] is not None) == (condition == "valid") for r in result["cases"]
    )
    assert result["accounting"]["request_count"] == (0 if condition == "changed" else 2)
    assert all(
        a["completed"] == (1 if condition == "valid" else 0)
        for a in result["aggregate"].values()
    )
    for row in result["cases"]:
        assert row["expected_outcome"]["issue_type"] == "type: enhancement"
        if condition == "valid":
            assert row["report"]["issue_type"] is None
    assert result["common_paired_cases"] == (1 if condition == "valid" else 0)
    assert all(
        a["cases"] == result["common_paired_cases"]
        for a in result["paired_aggregate"].values()
    )


def test_shared_cap_includes_prior_reservations_and_both_models_across_restarts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        p = next(p for p in FLASH_MODELS.values() if p.model_id == payload["model"])
        summary = FlashBudget(tmp_path, prior_reserved_micro_usd=4_900_000).summary()
        assert summary["combined_reserved_micro_usd"] < 5_000_000
        assert summary["request_count"] == dispatches
        return io.BytesIO(
            json.dumps(
                {
                    "model": p.model_id,
                    "provider": p.provider_name,
                    "choices": [
                        {"finish_reason": "stop", "message": {"content": "{}"}}
                    ],
                    "usage": {
                        "prompt_tokens": 100,
                        "completion_tokens": 10,
                        "cost": 0.00002,
                    },
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.flash_evaluation.urlopen", endpoint)
    refused = False
    for number in range(50):
        for p in FLASH_MODELS.values():
            try:
                FlashModel(
                    "secret",
                    p,
                    FlashBudget(tmp_path, prior_reserved_micro_usd=4_900_000),
                    number,
                ).generate_json(
                    "x" * 100_000,
                    {},
                    max_tokens=256,
                    response_schema={"type": "object", "properties": {}},
                )
            except ModelUnavailable as exc:
                assert "budget exhausted" in str(exc)
                refused = True
                break
        if refused:
            break
    assert refused and 2 <= dispatches < 10
    assert (
        FlashBudget(tmp_path, prior_reserved_micro_usd=4_900_000).summary()[
            "request_count"
        ]
        == dispatches
    )


@pytest.mark.parametrize(
    "failure", ["timeout", "missing_usage", "wrong_provider", "interrupted"]
)
def test_uncertain_call_stops_both_models_and_retains_its_reservation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        if failure == "timeout":
            raise TimeoutError("private provider error")
        if failure == "interrupted":
            raise KeyboardInterrupt
        response: dict[str, Any] = {
            "model": FLASH_MODELS["deepseek"].model_id,
            "provider": "unexpected provider",
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "cost": 0.0001},
        }
        if failure == "missing_usage":
            del response["usage"]
        return io.BytesIO(json.dumps(response).encode())

    monkeypatch.setattr("maintainer_copilot.flash_evaluation.urlopen", endpoint)
    schema: dict[str, object] = {"type": "object", "properties": {}}
    expected = KeyboardInterrupt if failure == "interrupted" else ModelUnavailable
    with pytest.raises(expected):
        FlashModel(
            "secret",
            FLASH_MODELS["deepseek"],
            FlashBudget(tmp_path, prior_reserved_micro_usd=1_183_980),
            1,
        ).generate_json("select", {}, max_tokens=256, response_schema=schema)
    with pytest.raises(ModelUnavailable, match="halted"):
        FlashModel(
            "secret",
            FLASH_MODELS["glm"],
            FlashBudget(tmp_path, prior_reserved_micro_usd=1_183_980),
            2,
        ).generate_json("select", {}, max_tokens=256, response_schema=schema)
    assert dispatches == 1
    summary = FlashBudget(tmp_path, prior_reserved_micro_usd=1_183_980).summary()
    assert summary["halted"] is True
    assert summary["request_count"] == 1
    assert summary["reserved_micro_usd"] > 0
    assert (
        "private provider error"
        not in FlashBudget(
            tmp_path, prior_reserved_micro_usd=1_183_980
        ).path.read_text()
    )


def test_provider_decimal_cost_is_retained_without_float_rounding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    exact_cost = "0.0001000000000000000000000001"
    profile = FLASH_MODELS["deepseek"]

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        response = json.dumps(
            {
                "model": profile.model_id,
                "provider": profile.provider_name,
                "choices": [{"finish_reason": "stop", "message": {"content": "{}"}}],
                "usage": {
                    "prompt_tokens": 100,
                    "completion_tokens": 200,
                    "cost": 0.0001,
                },
            }
        ).replace('"cost": 0.0001', '"cost": ' + exact_cost)
        return io.BytesIO(response.encode())

    monkeypatch.setattr("maintainer_copilot.flash_evaluation.urlopen", endpoint)
    budget = FlashBudget(tmp_path, prior_reserved_micro_usd=1_183_980)
    client = FlashModel("secret", profile, budget, 1)
    client.generate_json(
        "select",
        {},
        max_tokens=256,
        response_schema={"type": "object", "properties": {}},
    )
    assert client.calls[0]["reported_cost_usd"] == exact_cost
    assert budget.summary()["reported_cost_micro_usd"] == 101
