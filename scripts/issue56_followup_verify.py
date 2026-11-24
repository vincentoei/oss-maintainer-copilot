"""Audit the final #56 pass without changing any earlier evaluation artifact."""

import hashlib
import json
import subprocess
from pathlib import Path

from comparison_verification import verify_comparison_records
from issue56_verify import compare, verify_assistant_reviews

from maintainer_copilot.replay import load_cases
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
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        assert (
            hashlib.sha256(
                subprocess.check_output(
                    ["git", "show", f"{freeze['commit']}:{path}"], cwd=ROOT
                )
            ).hexdigest()
            == digest
        )
    accounting = verify_comparison_records(DIRECTORY, result, cases)
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
        "independent_human_review": "not supplied; not claimed",
        "future_training_corpus": "not created; overlap remains unverified",
        **accounting,
    }
    write(DIRECTORY / "verification.json", verification)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
