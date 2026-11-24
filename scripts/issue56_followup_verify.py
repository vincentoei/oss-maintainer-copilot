"""Audit the final #56 pass without changing any earlier evaluation artifact."""

import hashlib
import json
import subprocess
from pathlib import Path

from comparison_verification import verify_comparison_records
from issue56_verify import compare, verify_assistant_reviews

from maintainer_copilot.evaluation import score_report
from maintainer_copilot.replay import load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/evaluation/issue-56/follow-up"


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def main():
    baseline = read(DIRECTORY / "baseline.json")
    assert all(
        hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        for path, digest in baseline["files"].items()
    ), "Preserved case/evaluation artifact changed"
    cases = load_cases()
    assert len(cases) == 40
    freeze = read(DIRECTORY / "freeze.json")
    result = read(DIRECTORY / "run/results.json")
    assert result["status"] == "complete" and result["comparison_issue"] == 56
    assert result["planned_cases"] == 40
    assert result["catalog_sha256"] == fingerprint(
        [case.model_dump(mode="json") for case in cases]
    )
    assert all(
        freeze[field] == result[field]
        for field in ("catalog_sha256", "protocol_sha256", "source_sha256")
    )
    protocol_path = "docs/evaluation/issue-56/follow-up/protocol.md"
    assert (
        result["protocol_sha256"]
        == hashlib.sha256((ROOT / protocol_path).read_bytes()).hexdigest()
    )
    assert (ROOT / protocol_path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{freeze['commit']}:{protocol_path}"], cwd=ROOT
    )
    for path, digest in result["source_sha256"].items():
        assert (
            hashlib.sha256(
                subprocess.check_output(
                    ["git", "show", f"{freeze['commit']}:{path}"], cwd=ROOT
                )
            ).hexdigest()
            == digest
        )
    # Distinguish the final wording fix from the live source. These checks
    # reuse saved responses, and do not constitute another inference pass.
    wording = read(DIRECTORY / "title-version-replay.json")
    assert wording["status"] == "passed" and wording["live_dispatches"] == 0
    final_source = wording["source_sha256"]
    assert set(final_source) == set(result["source_sha256"])
    assert [
        path
        for path, digest in final_source.items()
        if digest != result["source_sha256"][path]
    ] == ["src/maintainer_copilot/pytest_profile.py"]
    assert all(
        hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        for path, digest in final_source.items()
    )
    checks = read(DIRECTORY / "checks.json")
    assert checks["source_sha256"] == final_source
    assert all(check["exit_code"] == 0 for check in checks["checks"])
    reports = {(row["method"], row["issue_number"]): row for row in result["cases"]}
    expected_keys = {
        (method, number)
        for method in ("keyword_rule", "fixed_rag", "bounded_agent")
        for number in (12072, 12263)
    }
    assert len(wording["reports"]) == len(expected_keys) == 6
    assert {
        (row["method"], row["issue_number"]) for row in wording["reports"]
    } == expected_keys
    case_by_number = {case.issue_number: case for case in cases}
    for replay in wording["reports"]:
        before = reports[replay["method"], replay["issue_number"]]
        assert replay["source_report_sha256"] == fingerprint(before["report"])
        assert replay["recorded_requests_consumed"] == [
            call["request"] for call in before["model_calls"]
        ]
        after = TriageReport.model_validate(replay["after_report"])
        assert after.issue_type == before["report"]["issue_type"]
        assert after.issue_type_quote == before["report"]["issue_type_quote"]
        scores = score_report(
            case_by_number[replay["issue_number"]], after, before["candidate_numbers"]
        )
        assert all(
            scores[field] == before["scores"][field]
            for field in before["scores"]
            if field != "draft_reply_usefulness"
        )
        assert after.status == before["report"]["status"]
        assert (
            next(
                d.request
                for d in after.missing_details
                if d.name == "pytest and OS versions"
            )
            == "your operating system and release"
        )
    accounting = verify_comparison_records(DIRECTORY, result, cases)
    accounting["independent_human_report_reviews_pending"] = accounting.pop(
        "fresh_report_reviews_pending"
    )
    reviewed = verify_assistant_reviews(
        result, DIRECTORY / "review", DIRECTORY / "review-decisions.json"
    )
    for label, path in (
        ("issue18", ROOT / "docs/evaluation/issue-18/run/results.json"),
        ("initial56", ROOT / "docs/evaluation/issue-56/run/results.json"),
    ):
        write(DIRECTORY / f"comparison-{label}.json", compare(read(path), result))
    verification = {
        "status": "passed",
        "preserved_files": len(baseline["files"]),
        "frozen_source_commit": freeze["commit"],
        "assistant_review_fingerprints_verified": reviewed,
        "post_measurement_wording_replays": 6,
        "post_measurement_live_dispatches": 0,
        "independent_human_review": "not supplied; not claimed",
        "future_training_corpus": "not created; overlap remains unverified",
        **accounting,
    }
    write(DIRECTORY / "verification.json", verification)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
