"""Audit the two requested Flash references without network or inference."""

import argparse
import hashlib
import json
from decimal import ROUND_CEILING, Decimal
from pathlib import Path
from typing import Any

from issue20_verify import verify_recorded_source

from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.flash_evaluation import FLASH_MODELS
from maintainer_copilot.replay import candidate_references, load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]


def verify(directory: Path) -> dict[str, Any]:
    freeze = json.loads(
        (ROOT / "docs/evaluation/issue-20/flash/freeze.json").read_text()
    )
    result = json.loads((directory / "results.json").read_text())
    for name, digest in freeze["preserved_references"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    verify_recorded_source(
        ROOT, freeze["source_sha256"], freeze["implementation_commit"]
    )
    assert result["source_sha256"] == freeze["source_sha256"]
    assert (
        hashlib.sha256(
            (ROOT / "docs/evaluation/issue-20-flash-protocol.md").read_bytes()
        ).hexdigest()
        == freeze["protocol_sha256"]
    )
    baseline_path = ROOT / "docs/evaluation/issue-19/post-quality/run/results.json"
    prior_path = ROOT / "docs/evaluation/issue-20/run/results.json"
    prior_ledger_path = ROOT / "docs/evaluation/issue-20/run/hosted-requests.jsonl"
    for path, field in (
        (baseline_path, "baseline_sha256"),
        (prior_path, "prior_results_sha256"),
        (prior_ledger_path, "prior_ledger_sha256"),
    ):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == result[field]
    baseline = json.loads(baseline_path.read_text())
    prior = json.loads(prior_path.read_text())
    local = {
        r["issue_number"]: r for r in baseline["cases"] if r["method"] == "fixed_rag"
    }
    gpt41 = {r["issue_number"]: r for r in prior["cases"]}
    catalog = sorted(load_cases(), key=lambda c: c.issue_number)
    numbers = [c.issue_number for c in catalog]
    assert len(catalog) == 50
    assert (
        fingerprint([c.model_dump(mode="json") for c in catalog])
        == result["catalog_sha256"]
        == prior["catalog_sha256"]
        == baseline["catalog_sha256"]
    )
    assert [r["issue_number"] for r in result["preflight"]] == numbers
    assert len(result["cases"]) == 100
    by_method = {
        name: {r["issue_number"]: r for r in result["cases"] if r["method"] == name}
        for name in FLASH_MODELS
    }
    for name, rows in by_method.items():
        assert sorted(rows) == numbers
        assert len([r for r in result["cases"] if r["method"] == name]) == 50
        for case in catalog:
            row = rows[case.issue_number]
            assert row["opening_cutoff"] == case.opening_cutoff.isoformat()
            assert row["repository_commit"] == case.repository_commit
            assert row["opening_content_sha256"] == case.opening_content_sha256
            assert (
                row["candidate_numbers"]
                == [r.number for r in candidate_references(case, catalog)]
                == local[case.issue_number]["candidate_numbers"]
            )
            assert row["case_review"] == case.human_review.model_dump(mode="json")
            assert row["expected_outcome"] == case.expected_outcome.model_dump(
                mode="json"
            )
            assert row["local_fixed_scores"] == local[case.issue_number]["scores"]
            assert row["gpt41_scores"] == gpt41[case.issue_number]["scores"]
            if row["scores"] is not None:
                assert row["error"] is None
                assert len(row["hosted_calls"]) == 1
                report = TriageReport.model_validate(row["report"])
                assert (
                    score_report(case, report, row["candidate_numbers"])
                    == row["scores"]
                )
                assert row["scores"]["draft_reply_usefulness"]["rating"] is None
                assert all(
                    e["status"] == "ok"
                    for e in row["trace"]["events"]
                    if e["kind"] == "model"
                )
            else:
                assert row["error"] is not None
    ledger = [
        json.loads(line)
        for line in (directory / "hosted-requests.jsonl").read_text().splitlines()
    ]
    prior_ledger = [
        json.loads(line) for line in prior_ledger_path.read_text().splitlines()
    ]
    prior_reserved = sum(
        r["reserved_micro_usd"] for r in prior_ledger if r["event"] == "reserved"
    )
    reserved = prior_reserved
    pending: set[int] = set()
    halted = False
    charges = []
    responses = []
    profiles = {p.model_id: p for p in FLASH_MODELS.values()}
    for event in ledger:
        if event["event"] == "reserved":
            assert not halted and not pending
            assert event["request"] == len(charges) + 1
            assert event["prior_reserved_micro_usd"] == prior_reserved
            profile = profiles[event["model"]]
            assert event["provider"] == profile.provider_slug
            assert event["version"] == profile.version
            assert event["input_nano_usd"] == profile.input_nano_usd
            assert event["output_nano_usd"] == profile.output_nano_usd
            assert event["max_output_tokens"] == 4096
            assert (
                event["reserved_micro_usd"]
                == (
                    event["input_token_bound"] * profile.input_nano_usd
                    + 4096 * profile.output_nano_usd
                    + 999
                )
                // 1000
            )
            reserved += event["reserved_micro_usd"]
            assert reserved <= 4_999_999
            pending.add(event["request"])
            charges.append(event)
        elif event["event"] == "response":
            assert event["request"] in pending
            charge = charges[event["request"] - 1]
            for field, value in charge.items():
                if field != "event":
                    assert event[field] == value
            pending.remove(event["request"])
            responses.append(event)
            if event.get("accounting_error"):
                halted = True
            else:
                profile = profiles[event["model"]]
                assert event["returned_model"] == profile.model_id
                assert event["returned_provider"] == profile.provider_name
                assert 0 <= event["input_tokens"] <= event["input_token_bound"]
                assert 0 <= event["output_tokens"] <= 4096
                assert (
                    event["cost_micro_usd"]
                    == (
                        event["input_tokens"] * profile.input_nano_usd
                        + event["output_tokens"] * profile.output_nano_usd
                        + 999
                    )
                    // 1000
                )
                if event["reasoning_tokens"] is not None:
                    assert 0 <= event["reasoning_tokens"] <= event["output_tokens"]
                cost = Decimal(event["reported_cost_usd"])
                assert cost.is_finite() and cost >= 0
                assert (
                    int((cost * 1_000_000).to_integral_value(rounding=ROUND_CEILING))
                    == event["reported_cost_micro_usd"]
                    <= event["reserved_micro_usd"]
                )
        else:
            assert event["event"] == "halted"
            halted = True
    assert not pending
    assert len(charges) <= 100
    assert len({(r["model"], r["issue_number"]) for r in charges}) == len(charges)
    calls = [c for r in result["cases"] for c in r["hosted_calls"]]
    for row in result["cases"]:
        for call in row["hosted_calls"]:
            assert call["issue_number"] == row["issue_number"]
            assert call["model"] == FLASH_MODELS[row["method"]].model_id
    assert len(calls) == len(charges) == len(responses)
    for call, response in zip(calls, responses, strict=True):
        assert {**call, "event": "response"} == response
    assert result["accounting"]["combined_reserved_micro_usd"] == reserved
    assert result["accounting"]["request_count"] == len(charges)
    assert result["accounting"]["halted"] == halted
    assert result["accounting"]["reserved_micro_usd"] == reserved - prior_reserved
    known = [r for r in responses if r.get("cost_micro_usd") is not None]
    assert result["accounting"]["known_cost_micro_usd"] == sum(
        r["cost_micro_usd"] for r in known
    )
    assert result["accounting"]["unknown_usage_requests"] == len(charges) - len(known)
    if len(known) == len(charges):
        assert (
            result["accounting"]["cost_micro_usd"]
            == result["accounting"]["known_cost_micro_usd"]
        )
        assert result["accounting"]["input_tokens"] == sum(
            r["input_tokens"] for r in known
        )
        assert result["accounting"]["output_tokens"] == sum(
            r["output_tokens"] for r in known
        )
        assert result["accounting"]["reported_cost_micro_usd"] == sum(
            r["reported_cost_micro_usd"] for r in known
        )
    summaries = {}
    for name, profile in FLASH_MODELS.items():
        model_calls = [r for r in responses if r["model"] == profile.model_id]
        assert len(model_calls) <= 50
        known = [r for r in model_calls if "reported_cost_usd" in r]
        total = sum((Decimal(r["reported_cost_usd"]) for r in known), Decimal(0))
        summaries[name] = {
            "requests": len(model_calls),
            "known_usage_requests": len(known),
            "input_tokens": sum(r["input_tokens"] for r in known),
            "output_tokens": sum(r["output_tokens"] for r in known),
            "reasoning_tokens": sum(r["reasoning_tokens"] for r in known)
            if all(r["reasoning_tokens"] is not None for r in known)
            else None,
            "reported_cost_usd": str(total),
        }
        endpoint = result["providers"][name]["endpoint"]
        assert (
            endpoint["tag"] == profile.provider_slug
            and profile.version in endpoint["name"]
        )
    fields = tuple(CaseResult.__dataclass_fields__)
    for name in FLASH_MODELS:
        assert (
            aggregate(
                [
                    CaseResult(**{k: r[k] for k in fields})
                    for r in by_method[name].values()
                ]
            )
            == result["aggregate"][name]
        )
    common = [
        n
        for n in numbers
        if all(by_method[name][n]["scores"] is not None for name in FLASH_MODELS)
        and local[n]["scores"] is not None
        and gpt41[n]["scores"] is not None
    ]
    assert common == result["paired_case_numbers"]
    assert len(common) == result["common_paired_cases"]
    for name, rows in {"qwen3b": local, "gpt41": gpt41, **by_method}.items():
        assert result["paired_aggregate"][name] == aggregate(
            [
                CaseResult(
                    n,
                    name,
                    rows[n]["opening_cutoff"],
                    rows[n]["repository_commit"],
                    rows[n]["latency_ms"],
                    len(rows[n]["candidate_numbers"]),
                    None,
                    rows[n]["scores"],
                )
                for n in common
            ]
        )
    combined_cost = Decimal(
        prior["accounting"]["reported_cost_micro_usd"]
    ) / 1_000_000 + sum(
        (
            Decimal(r["reported_cost_usd"])
            for r in responses
            if "reported_cost_usd" in r
        ),
        Decimal(0),
    )
    assert combined_cost < 5
    assert result["status"] == (
        "complete"
        if all(row["error"] is None for row in result["cases"])
        else "incomplete"
    )
    return {
        "verified": True,
        "status": result["status"],
        "case_rows": len(result["cases"]),
        "eligible_cases": sum(r["error"] is None for r in result["preflight"]),
        "common_paired_cases": len(common),
        "models": summaries,
        "combined_reported_cost_usd": str(combined_cost),
        "combined_reserved_micro_usd": reserved,
        "preserved_references_and_source_freeze": True,
        "report_semantics_and_usefulness": "pending_human_review",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=ROOT / "docs/evaluation/issue-20/flash/run"
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), indent=2))


if __name__ == "__main__":
    main()
