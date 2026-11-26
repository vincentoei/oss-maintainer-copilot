"""Audit frozen issue #60 results without network access or model inference."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from issue20_verify import verify_recorded_source

from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.replay import candidate_references, load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]


def verify(directory: Path) -> dict[str, Any]:
    freeze = json.loads((directory / "freeze.json").read_text())
    preservation = json.loads((directory / "preservation.json").read_text())
    assert (
        hashlib.sha256((directory / "preservation.json").read_bytes()).hexdigest()
        == freeze["preservation_sha256"]
    )
    for name, digest in preservation["files"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    assert (
        hashlib.sha256(
            (ROOT / "docs/evaluation/issue-60-protocol.md").read_bytes()
        ).hexdigest()
        == freeze["protocol_sha256"]
    )
    assert (
        hashlib.sha256((directory / "reviewed-examples.json").read_bytes()).hexdigest()
        == freeze["reviewed_examples_sha256"]
    )
    examples = json.loads((directory / "reviewed-examples.json").read_text())
    assert (
        examples["review"]["status"] == "confirmed" and len(examples["examples"]) == 4
    )
    cases = sorted(load_cases(), key=lambda c: c.issue_number)
    numbers = [c.issue_number for c in cases]
    assert len(cases) == 50
    catalog = fingerprint([c.model_dump(mode="json") for c in cases])
    assert catalog == freeze["catalog_sha256"]
    followup_path = directory / "followup-freeze.json"
    followup = json.loads(followup_path.read_text()) if followup_path.exists() else None
    if followup:
        assert (
            hashlib.sha256(
                (ROOT / "docs/evaluation/issue-60-followup-protocol.md").read_bytes()
            ).hexdigest()
            == followup["protocol_sha256"]
        )
        for name, digest in followup["original_runs"].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    phase_names = ("before", "after", "followup") if followup else ("before", "after")
    phases = {}
    resources = {}
    total_requests = 0
    for phase in phase_names:
        path = directory / phase
        result = json.loads((path / "results.json").read_text())
        phases[phase] = result
        assert result["phase"] == ("after" if phase == "followup" else phase)
        assert result["catalog_sha256"] == catalog
        source_hashes = (
            followup["source_sha256"]
            if phase == "followup"
            else freeze[phase + "_source_sha256"]
        )
        source_commit = (
            followup["implementation_commit"]
            if phase == "followup"
            else freeze[phase + "_commit"]
        )
        assert result["source_sha256"] == source_hashes
        verify_recorded_source(ROOT, source_hashes, source_commit)
        assert [r["issue_number"] for r in result["preflight"]] == numbers
        assert [r["issue_number"] for r in result["cases"]] == numbers
        requests = [
            json.loads(line)
            for line in (path / "requests.jsonl").read_text().splitlines()
        ]
        responses = [
            json.loads(line)
            for line in (path / "responses.jsonl").read_text().splitlines()
        ]
        calls = [call for row in result["cases"] for call in row["model_calls"]]
        assert len(requests) == len(responses) == len(calls) <= 50
        assert len({r["issue_number"] for r in requests}) == len(requests)
        for index, (request, response, call) in enumerate(
            zip(requests, responses, calls, strict=True), 1
        ):
            assert request["request"] == index
            assert request["method"] == "fixed_rag" and request["max_tokens"] == 256
            assert request["case_count"] == 50
            assert all(response[k] == v for k, v in request.items())
            assert response == call
            if "raw_response_utf8" in response:
                raw = response["raw_response_utf8"].encode()
                assert (
                    hashlib.sha256(raw).hexdigest() == response["raw_response_sha256"]
                )
        total_requests += len(requests)
        results = []
        for case, audit, row in zip(
            cases, result["preflight"], result["cases"], strict=True
        ):
            assert (
                row["opening_cutoff"]
                == audit["opening_cutoff"]
                == case.opening_cutoff.isoformat()
            )
            assert (
                row["opening_content_sha256"]
                == audit["opening_content_sha256"]
                == case.opening_content_sha256
            )
            assert (
                row["repository_commit"]
                == audit["repository_commit"]
                == case.repository_commit
            )
            assert row["candidate_numbers"] == [
                c.number for c in candidate_references(case, cases)
            ]
            assert audit["expected_type"] == case.expected_outcome.issue_type
            if audit["error"] is None:
                assert audit["expected_reachable"] == (
                    audit["expected_type"] is None
                    or audit["expected_type"] in audit["offered_types"]
                )
            else:
                assert audit["expected_reachable"] is None
                assert not row["model_calls"] and row["scores"] is None
            for call in row["model_calls"]:
                assert call["issue_number"] == case.issue_number
            if row["scores"] is not None:
                report = TriageReport.model_validate(row["report"])
                assert (
                    score_report(case, report, row["candidate_numbers"])
                    == row["scores"]
                )
                assert row["error"] is None
                assert all(
                    e["status"] == "ok"
                    for e in row["trace"]["events"]
                    if e["kind"] == "model"
                )
                assert row["scores"]["draft_reply_usefulness"]["rating"] is None
            else:
                assert row["error"] is not None
            if row["keyword_report"]:
                keyword = TriageReport.model_validate(row["keyword_report"])
                assert (
                    score_report(case, keyword, row["candidate_numbers"])
                    == row["keyword_scores"]
                )
            results.append(
                CaseResult(**{k: row[k] for k in CaseResult.__dataclass_fields__})
            )
        assert aggregate(results) == result["aggregate"]
        usage = [c.get("response") or {} for c in calls]
        resources[phase] = {
            "dispatches": len(requests),
            "input_tokens": sum(r["input_tokens"] for r in usage)
            if all(type(r.get("input_tokens")) is int for r in usage)
            else None,
            "output_tokens": sum(r["output_tokens"] for r in usage)
            if all(type(r.get("output_tokens")) is int for r in usage)
            else None,
        }
    assert total_requests <= (150 if followup else 100)
    before, after = phases["before"], phases["followup" if followup else "after"]
    assert before["generation"] == after["generation"]
    for field in ("version", "template_sha256"):
        assert before["serving"][field] == after["serving"][field]
    assert (
        before["serving"]["identity"]["digest"]
        == after["serving"]["identity"]["digest"]
    )
    assert (
        before["serving"]["show"]["parameters"]
        == after["serving"]["show"]["parameters"]
    )
    for result in phases.values():
        assert before["generation"] == result["generation"]
        assert before["serving"]["version"] == result["serving"]["version"]
        assert (
            before["serving"]["identity"]["digest"]
            == result["serving"]["identity"]["digest"]
        )
        assert (
            before["serving"]["show"]["parameters"]
            == result["serving"]["show"]["parameters"]
        )
        assert (
            before["serving"]["template_sha256"] == result["serving"]["template_sha256"]
        )
        for field in ("version", "template_sha256"):
            assert result["serving"][field] == result["serving_after"][field]
        assert (
            result["serving"]["identity"]["digest"]
            == result["serving_after"]["identity"]["digest"]
        )
        assert (
            result["serving"]["show"]["parameters"]
            == result["serving_after"]["show"]["parameters"]
        )
        assert before["evidence_sha256"] == result["evidence_sha256"]
    key = json.loads((directory / "review/review-key.json").read_text())
    expected_reports = {
        (phase, row["issue_number"]): fingerprint(row["report"])
        for phase, result in phases.items()
        for row in result["cases"]
    }
    assert len(key) == len(expected_reports) == 50 * len(phases)
    assert len({r["code"] for r in key}) == len(key)
    assert {(r["method"], r["issue_number"]) for r in key} == set(expected_reports)
    for entry in key:
        assert (
            expected_reports[entry["method"], entry["issue_number"]]
            == entry["report_sha256"]
        )
    for name in ("human-review.json", "classification-review.json"):
        ratings = json.loads((directory / "review" / name).read_text())
        assert [(r["code"], r["report_sha256"]) for r in ratings] == [
            (r["code"], r["report_sha256"]) for r in key
        ]
        # This publication claims no fresh human report ratings.
        assert all(r["status"] == "pending" for r in ratings)
        assert all(
            value is None
            for row in ratings
            for name, value in row.items()
            if name not in ("code", "report_sha256", "status")
        )
    gains, regressions, paired = [], [], []
    unchanged = (
        "missing_details",
        "duplicate_candidates",
        "related_issues",
        "documentation_claims",
        "source_claims",
        "ci_results",
    )
    changes = json.loads((directory / "type-changes.json").read_text())
    assert len(changes) == 50
    for left, right, change in zip(
        before["cases"], after["cases"], changes, strict=True
    ):
        assert left["keyword_scores"] == right["keyword_scores"]
        if left["report"] and right["report"]:
            for field in unchanged:
                assert left["report"][field] == right["report"][field]
        if left["scores"] is not None and right["scores"] is not None:
            paired.append(left["issue_number"])
        before_correct = bool(
            left["scores"] and left["scores"]["issue_type"]["correct"]
        )
        after_correct = bool(
            right["scores"] and right["scores"]["issue_type"]["correct"]
        )
        assert change == {
            "issue_number": left["issue_number"],
            "expected": next(
                c.expected_outcome.issue_type
                for c in cases
                if c.issue_number == left["issue_number"]
            ),
            "before": left["report"]["issue_type"],
            "followup": right["report"]["issue_type"],
            "before_correct": before_correct,
            "followup_correct": after_correct,
            "before_error": left["error"],
            "followup_error": right["error"],
            "before_quote": left["report"]["issue_type_quote"],
            "followup_quote": right["report"]["issue_type_quote"],
        }
        if after_correct and not before_correct:
            gains.append(left["issue_number"])
        if before_correct and not after_correct:
            regressions.append(left["issue_number"])
    counts = {}
    for phase, result in phases.items():
        counts[phase] = {
            "catalog": 50,
            "eligible": sum(r["error"] is None for r in result["preflight"]),
            "unreachable_expected_types": sum(
                r["expected_reachable"] is False for r in result["preflight"]
            ),
            "audit_flags": sum(r["error"] is not None for r in result["preflight"]),
            "scored": sum(r["scores"] is not None for r in result["cases"]),
            "type_correct_over_50": sum(
                bool(r["scores"] and r["scores"]["issue_type"]["correct"])
                for r in result["cases"]
            ),
            "model_failures": sum(r["error"] is not None for r in result["cases"]),
            "abstentions": sum(
                bool(r["report"] and r["report"]["issue_type"] is None)
                for r in result["cases"]
            ),
            **resources[phase],
        }
    return {
        "verified": True,
        "preserved_files": len(preservation["files"]),
        "counts": counts,
        "total_dispatches": total_requests,
        "final_phase": "followup" if followup else "after",
        "complete_pairs": len(paired),
        "paired_case_numbers": paired,
        "type_gains": gains,
        "type_regressions": regressions,
        "keyword_fields_and_unrelated_report_fields_unchanged": True,
        "fresh_pending_review_rows": len(key),
        "model_api_usd": 0,
        "semantic_and_usefulness_review": "pending_human_review",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=ROOT / "docs/evaluation/issue-60"
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), indent=2))


if __name__ == "__main__":
    main()
