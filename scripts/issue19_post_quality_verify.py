"""Audit the separately frozen fifty-case comparison after merged PR #57."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from comparison_verification import verify_comparison_records
from expansion_verification import verify_metadata
from issue56_verify import compare

from maintainer_copilot.workflow_comparison import (
    METHODS,
    fingerprint,
    summarize_comparison,
)

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/evaluation/issue-19/post-quality"


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def subset(artifact, numbers):
    selected = {
        **artifact,
        "cases": [r for r in artifact["cases"] if r["issue_number"] in numbers],
        "preflight": [r for r in artifact["preflight"] if r["issue_number"] in numbers],
    }
    selected["summary"] = summarize_comparison(selected)
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    baseline = read(DIRECTORY / "baseline.json")
    assert all(digest(ROOT / p) == h for p, h in baseline["files"].items())
    catalog, original_numbers, metadata = verify_metadata(
        ROOT / "docs/evaluation/issue-19", 19
    )
    metadata["preserved_files"] = len(baseline["files"])
    if args.metadata_only:
        print(json.dumps(metadata, indent=2))
        return
    result = read(DIRECTORY / "run/results.json")
    freeze = read(DIRECTORY / "freeze.json")
    assert result["status"] == "complete"
    assert result["comparison_issue"] == 19 and result["planned_cases"] == 50
    assert result["catalog_sha256"] == fingerprint(
        [c.model_dump(mode="json") for c in catalog]
    )
    assert all(
        result[f] == freeze[f]
        for f in ("catalog_sha256", "protocol_sha256", "source_sha256")
    )
    assert result["protocol_sha256"] == digest(DIRECTORY / "protocol.md")
    assert freeze["baseline_sha256"] == digest(DIRECTORY / "baseline.json")
    pinned = {
        **result["source_sha256"],
        str((DIRECTORY / "protocol.md").relative_to(ROOT)): result["protocol_sha256"],
        str((DIRECTORY / "baseline.json").relative_to(ROOT)): freeze["baseline_sha256"],
        **{
            f"src/maintainer_copilot/cases/pytest_{c.issue_number}.json": digest(
                ROOT / f"src/maintainer_copilot/cases/pytest_{c.issue_number}.json"
            )
            for c in catalog
        },
    }
    for path, expected in pinned.items():
        assert digest(ROOT / path) == expected
        assert (
            hashlib.sha256(
                subprocess.check_output(
                    ["git", "show", f"{freeze['commit']}:{path}"], cwd=ROOT
                )
            ).hexdigest()
            == expected
        )
    accounting = verify_comparison_records(DIRECTORY, result, catalog)
    previous = read(ROOT / "docs/evaluation/issue-19/run/results.json")
    comparison = compare(previous, result)
    comparison["scope"] = (
        "Same fifty confirmed openings, expected outcomes, cutoffs and candidate "
        "pools. All 150 rows retained. Merged quality fixes change source, "
        "selection prompt/schema and deterministic report policy. No tuning or "
        "generalization claim; single-pass serving differences remain possible."
    )
    original = subset(result, original_numbers)
    additions = {c.issue_number for c in catalog} - original_numbers
    new_ten = subset(result, additions)
    comparison["subsets"] = {
        "original_forty": original["summary"]["methods"],
        "new_ten": new_ten["summary"]["methods"],
    }
    forty = compare(
        read(ROOT / "docs/evaluation/issue-56/follow-up/run/results.json"), original
    )
    forty["scope"] = (
        "Same original forty cases and candidate pools. Prior #56 live source "
        "0035e14 preceded its final title-version wording fix; this pass uses "
        "the actual merged wording/source and the fifty-case catalog. "
        "Resource summaries compare the observed forty-case subset."
    )
    regressions = []
    for before, after in zip(previous["cases"], result["cases"], strict=True):
        assert (before["method"], before["issue_number"]) == (
            after["method"],
            after["issue_number"],
        )
        for field, key in (
            ("issue_type", "correct"),
            ("missing_details", "exact"),
            ("duplicate_judgment", "correct"),
        ):
            old = (before["scores"] or {}).get(field, {}).get(key)
            new = (after["scores"] or {}).get(field, {}).get(key)
            if old is True and new is not True:
                regressions.append(
                    {
                        "method": after["method"],
                        "issue_number": after["issue_number"],
                        "field": field,
                        "before": old,
                        "after": new,
                    }
                )
    verification = {
        **metadata,
        **accounting,
        "frozen_source_commit": freeze["commit"],
        "prior_fifty_compared_rows": len(comparison["rows"]),
        "prior_quality_compared_rows": len(forty["rows"]),
        "exact_field_regressions": regressions,
        "methods": list(METHODS),
        "fresh_semantic_usefulness_review": "pending; no prior ratings transferred",
    }
    for name, value in (
        ("comparison-original-fifty.json", comparison),
        ("comparison-quality-forty.json", forty),
        ("verification.json", verification),
    ):
        if args.check_only:
            assert read(DIRECTORY / name) == value
        else:
            write(DIRECTORY / name, value)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
