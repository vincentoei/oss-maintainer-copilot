"""Audit the saved issue #20 reference without network access or inference."""

import argparse
import hashlib
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.replay import candidate_references, load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]


def verify_recorded_source(root: Path, hashes: dict[str, str], commit: str) -> None:
    """Check the frozen Git source, allowing current implementation to evolve."""
    for name, digest in hashes.items():
        recorded = subprocess.check_output(
            ["git", "show", f"{commit}:{name}"], cwd=root
        )
        assert hashlib.sha256(recorded).hexdigest() == digest


def verify(directory: Path) -> dict[str, Any]:
    freeze = json.loads((ROOT / "docs/evaluation/issue-20/freeze.json").read_text())
    baseline_path = ROOT / "docs/evaluation/issue-19/post-quality/run/results.json"
    baseline = json.loads(baseline_path.read_text())
    result = json.loads((directory / "results.json").read_text())
    ledger = [
        json.loads(line)
        for line in (directory / "hosted-requests.jsonl").read_text().splitlines()
    ]
    assert (
        hashlib.sha256(baseline_path.read_bytes()).hexdigest()
        == (freeze["local_baseline_sha256"])
        == result["baseline_sha256"]
    )
    assert (
        hashlib.sha256(
            (ROOT / "docs/evaluation/issue-20-protocol.md").read_bytes()
        ).hexdigest()
        == freeze["protocol_sha256"]
    )
    assert result["source_sha256"] == freeze["source_sha256"]
    verify_recorded_source(
        ROOT, freeze["source_sha256"], freeze["implementation_commit"]
    )
    catalog = sorted(load_cases(), key=lambda c: c.issue_number)
    numbers = [c.issue_number for c in catalog]
    assert len(catalog) == 50
    assert (
        fingerprint([c.model_dump(mode="json") for c in catalog])
        == (baseline["catalog_sha256"])
        == result["catalog_sha256"]
    )
    assert [r["issue_number"] for r in result["cases"]] == numbers
    assert [r["issue_number"] for r in result["preflight"]] == numbers
    local = {
        r["issue_number"]: r for r in baseline["cases"] if r["method"] == "fixed_rag"
    }
    for entry in result["preflight"]:
        assert entry["local_error"] == local[entry["issue_number"]]["error"]
        assert entry["eligible"] == (
            entry["error"] is None and entry["local_error"] is None
        )
    scored = 0
    for case, row in zip(catalog, result["cases"], strict=True):
        assert row["opening_cutoff"] == case.opening_cutoff.isoformat()
        assert row["repository_commit"] == case.repository_commit
        assert row["opening_content_sha256"] == case.opening_content_sha256
        assert (
            row["candidate_numbers"]
            == [r.number for r in candidate_references(case, catalog)]
            == local[case.issue_number]["candidate_numbers"]
        )
        assert row["expected_outcome"] == case.expected_outcome.model_dump(mode="json")
        assert row["case_review"] == case.human_review.model_dump(mode="json")
        assert row["local_fixed_scores"] == local[case.issue_number]["scores"]
        if row["scores"] is not None:
            assert row["error"] is None
            report = TriageReport.model_validate(row["hosted_report"])
            assert score_report(case, report, row["candidate_numbers"]) == row["scores"]
            assert row["scores"]["draft_reply_usefulness"]["rating"] is None
            assert all(
                e["status"] == "ok"
                for e in row["trace"]["events"]
                if e["kind"] == "model"
            )
            scored += 1
        else:
            assert row["error"] is not None
    charges = [r for r in ledger if r["event"] == "reserved"]
    responses = [r for r in ledger if r["event"] == "response"]
    assert len(charges) <= 50
    assert len({r["issue_number"] for r in charges}) == len(charges)
    reserved = 0
    for index, charge in enumerate(charges, 1):
        assert charge["request"] == index
        assert charge["provider"] == "openrouter"
        assert charge["model"] == "gpt-4.1-2025-04-14"
        assert charge["max_output_tokens"] == 256
        assert charge["input_token_bound"] > 4096
        assert charge["reserved_micro_usd"] == (
            charge["input_token_bound"] * 2 + 256 * 8
        )
        reserved += charge["reserved_micro_usd"]
        assert reserved < 5_000_000
    for response in responses:
        charge = charges[response["request"] - 1]
        if not response.get("accounting_error"):
            assert response["returned_model"] == "openai/gpt-4.1"
            assert response["returned_provider"] == "OpenAI"
            assert 0 <= response["input_tokens"] <= charge["input_token_bound"]
            assert 0 <= response["output_tokens"] <= 256
            assert response["cost_micro_usd"] == (
                response["input_tokens"] * 2 + response["output_tokens"] * 8
            )
            assert (
                0
                <= response["reported_cost_micro_usd"]
                <= (charge["reserved_micro_usd"])
            )
    calls = [c for r in result["cases"] for c in r["model_calls"]]
    assert len(calls) == len(charges) == len(responses)
    for call, response in zip(calls, responses, strict=True):
        assert {**call, "event": "response"} == response
    accounting = result["accounting"]
    assert accounting["request_count"] == len(charges)
    assert accounting["reserved_micro_usd"] == reserved
    assert accounting["cap_micro_usd"] == 4_999_999
    known = [r for r in responses if r.get("cost_micro_usd") is not None]
    assert accounting["known_cost_micro_usd"] == sum(r["cost_micro_usd"] for r in known)
    assert accounting["unknown_usage_requests"] == len(charges) - len(known)
    reported = [r["reported_cost_micro_usd"] for r in responses]
    assert accounting["reported_cost_micro_usd"] == sum(reported)
    if len(known) == len(charges):
        assert accounting["cost_micro_usd"] == accounting["known_cost_micro_usd"]
        assert accounting["input_tokens"] == sum(r["input_tokens"] for r in known)
        assert accounting["output_tokens"] == sum(r["output_tokens"] for r in known)
    fields = tuple(CaseResult.__dataclass_fields__)
    rows = [CaseResult(**{k: r[k] for k in fields}) for r in result["cases"]]
    assert result["aggregate"] == aggregate(rows)
    paired = [r for r in rows if r.scores and local[r.issue_number]["scores"]]
    assert result["paired_scoreable_cases"] == len(paired)
    assert result["hosted_paired_aggregate"] == aggregate(paired)
    assert result["local_fixed_aggregate"] == aggregate(
        [
            CaseResult(
                **{
                    **asdict(row),
                    "method": "local_fixed_rag",
                    "latency_ms": local[row.issue_number]["latency_ms"],
                    "scores": local[row.issue_number]["scores"],
                }
            )
            for row in paired
        ]
    )
    assert result["attribution"]["report_semantics_and_usefulness"] == (
        "pending_human_review"
    )
    assert result["provider_identity"]["endpoint"]["tag"] == "openai"
    return {
        "verified": True,
        "status": result["status"],
        "cases": len(catalog),
        "eligible": sum(r["eligible"] for r in result["preflight"]),
        "scored": scored,
        "paired_cases": len(paired),
        "accounting": accounting,
        "preserved_local_baseline": True,
        "source_and_protocol_match_freeze": True,
        "scores_recomputed": scored,
        "semantic_review": "pending_human_review",
        "upstream_snapshot_attestation": "OpenRouter alias limitation disclosed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=ROOT / "docs/evaluation/issue-20/run"
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), indent=2))


if __name__ == "__main__":
    main()
