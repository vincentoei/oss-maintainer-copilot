"""Audit the separately frozen #56 pass and compare every row with archived #18."""

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from comparison_verification import verify_comparison_records

from maintainer_copilot.evaluation import CaseResult, aggregate
from maintainer_copilot.replay import candidate_references, load_cases
from maintainer_copilot.workflow_comparison import METHODS, fingerprint

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/evaluation/issue-56"
FIELDS = (
    "duplicate_retrieval",
    "duplicate_judgment",
    "issue_type",
    "missing_details",
    "citation_validity",
    "abstention",
)


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def verify_assistant_reviews(result, folder, decisions_path):
    reviews = read(folder / "reviews.json")
    decisions = read(decisions_path)
    reports = {(r["method"], r["issue_number"]): r for r in result["cases"]}
    assert Counter((r["method"], r["issue_number"]) for r in reviews) == Counter(
        reports.keys()
    )
    for review in reviews:
        row = reports[review["method"], review["issue_number"]]
        assert review["report_sha256"] == fingerprint(row["report"])
        assert review["opening_content_sha256"] == row["opening_content_sha256"]
        assert review["reviewer"] == "Codex"
        assert review["independent_human_review"] is review["blinded"] is False
        note = decisions[str(row["issue_number"])]
        note = {**note, **note.get("method_overrides", {}).get(row["method"], {})}
        assert review["rating"] in (0, 1, 2)
        assert all(
            review[field] == note[field]
            for field in ("rating", "reason", "semantic_support")
        )
    summary = read(folder / "summary.json")
    assert summary["reports"] == len(reviews) == 120
    assert summary["rating_counts"] == dict(Counter(str(r["rating"]) for r in reviews))
    return len(reviews)


def compare(before, after):
    old = {(r["method"], r["issue_number"]): r for r in before["cases"]}
    new = {(r["method"], r["issue_number"]): r for r in after["cases"]}
    assert set(old) == set(new)
    comparisons = []
    for key, row in new.items():
        prior = old[key]
        assert row["candidate_numbers"] == prior["candidate_numbers"]
        assert all(
            row[field] == prior[field]
            for field in (
                "opening_cutoff",
                "repository_commit",
                "opening_content_sha256",
            )
        )
        changes = {
            field: {
                "before": prior["scores"].get(field),
                "after": row["scores"].get(field),
            }
            for field in FIELDS
            if prior["scores"] is not None
            and row["scores"] is not None
            and prior["scores"].get(field) != row["scores"].get(field)
        }
        for field, previous, current in (
            ("error", prior["error"], row["error"]),
            (
                "score_availability",
                prior["scores"] is not None,
                row["scores"] is not None,
            ),
            (
                "report_status",
                (prior["report"] or {}).get("status"),
                (row["report"] or {}).get("status"),
            ),
        ):
            if previous != current:
                changes[field] = {"before": previous, "after": current}
        comparisons.append(
            {
                "method": key[0],
                "issue_number": key[1],
                "changes": changes,
                "report_changed": fingerprint(
                    {
                        k: v
                        for k, v in (prior["report"] or {}).items()
                        if k != "trace_id"
                    }
                )
                != fingerprint(
                    {k: v for k, v in (row["report"] or {}).items() if k != "trace_id"}
                ),
            }
        )
    fields = tuple(CaseResult.__dataclass_fields__)
    return {
        "scope": (
            "Same forty openings, cutoffs, expected outcomes and candidate pools. "
            "All 120 rows retained; report comparison excludes trace IDs. "
            "Changed implementation/schema/prompt and serving nondeterminism "
            "limit causal attribution. Development-set gains are not generalization."
        ),
        "rows": comparisons,
        "scores": {
            label: {
                method: aggregate(
                    [
                        CaseResult(**{field: row[field] for field in fields})
                        for row in result["cases"]
                        if row["method"] == method
                    ]
                )
                for method in METHODS
            }
            for label, result in (("before", before), ("after", after))
        },
        "field_transitions": {
            method: {
                field: [
                    {"before": json.loads(a), "after": json.loads(b), "count": count}
                    for (a, b), count in Counter(
                        (
                            json.dumps(
                                (old[key]["scores"] or {}).get(field), sort_keys=True
                            ),
                            json.dumps(
                                (new[key]["scores"] or {}).get(field), sort_keys=True
                            ),
                        )
                        for key in new
                        if key[0] == method
                    ).items()
                ]
                for field in FIELDS
            }
            for method in METHODS
        },
        "before_resource_summary": before["summary"],
        "after_resource_summary": after["summary"],
    }


def main():
    baseline = read(DIRECTORY / "baseline.json")
    assert all(
        hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
        for path, digest in baseline["files"].items()
    ), "Preserved baseline artifact changed"
    cases = load_cases()
    assert len(cases) == 40
    partitions = read(ROOT / "docs/evaluation/issue-18/partitions.json")
    for case in cases:
        assert case.issue_number in partitions["evaluation"][case.issue_family_id]
        assert all(
            ref.created_at < case.opening_cutoff
            for ref in candidate_references(case, cases)
        )
    result = read(DIRECTORY / "run/results.json")
    freeze = read(DIRECTORY / "freeze.json")
    assert result["status"] == "complete"
    assert result["comparison_issue"] == 56 and result["planned_cases"] == 40
    assert result["catalog_sha256"] == fingerprint(
        [case.model_dump(mode="json") for case in cases]
    )
    protocol_path = "docs/evaluation/issue-56-protocol.md"
    assert (
        result["protocol_sha256"]
        == hashlib.sha256((ROOT / protocol_path).read_bytes()).hexdigest()
    )
    assert all(
        result[field] == freeze[field]
        for field in ("catalog_sha256", "protocol_sha256", "source_sha256")
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
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    assert (ROOT / protocol_path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{freeze['commit']}:{protocol_path}"], cwd=ROOT
    )
    accounting = verify_comparison_records(DIRECTORY, result, cases)
    before = read(ROOT / "docs/evaluation/issue-18/run/results.json")
    assistant_reviews = {
        label: verify_assistant_reviews(
            reviewed,
            DIRECTORY / f"{label}-review",
            DIRECTORY / f"{label}-review-decisions.json",
        )
        for label, reviewed in (("archived", before), ("candidate", result))
    }
    write(DIRECTORY / "comparison.json", compare(before, result))
    verification = {
        "status": "passed",
        "preserved_files": len(baseline["files"]),
        "case_count": len(cases),
        "same_candidate_pools": True,
        "frozen_source_commit": freeze["commit"],
        "assistant_review_fingerprints_verified": assistant_reviews,
        "future_training_corpus": "not created; overlap audit remains unverified",
        **accounting,
    }
    write(DIRECTORY / "verification.json", verification)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
