"""Shared offline audit for frozen ten-case benchmark expansions."""

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from comparison_verification import verify_comparison_records

from maintainer_copilot.evaluation import CaseResult, aggregate
from maintainer_copilot.replay import candidate_references
from maintainer_copilot.workflow_comparison import (
    CASE_COUNTS,
    METHODS,
    fingerprint,
    load_comparison_cases,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def verify_metadata(directory, issue, *, allow_pending=False):
    baseline = read(directory / "baseline.json")
    assert all(
        hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h
        for p, h in baseline["files"].items()
    ), "Preserved baseline artifact changed"
    cases = load_comparison_cases(issue)
    assert len(cases) == len({c.issue_number for c in cases}) == CASE_COUNTS[issue]
    original_numbers = {
        int(Path(p).stem.removeprefix("pytest_"))
        for p in baseline["files"]
        if p.startswith("src/maintainer_copilot/cases/")
    }
    assert len(original_numbers) == CASE_COUNTS[issue] - 10
    added = [c for c in cases if c.issue_number not in original_numbers]
    assert len(added) == 10
    provenance = read(directory / "provenance.json")
    for c in added:
        if not allow_pending:
            assert c.human_review.status == "confirmed"
        assert c.opening_verified_at.isoformat() == provenance["verified_at"]
        for number, digest, created in (
            (c.issue_number, c.opening_content_sha256, c.opening_cutoff),
            (
                c.earlier_issue.number,
                c.earlier_issue.content_sha256,
                c.earlier_issue.created_at,
            ),
        ):
            opening = provenance["openings"][str(number)]
            assert opening["content_sha256"] == digest
            assert opening["rest_graphql_agree"] and opening["last_edited_at"] is None
            assert opening["created_at"] == created.strftime("%Y-%m-%dT%H:%M:%SZ")
        commit = provenance["commits"][str(c.issue_number)]
        assert commit["sha"] == c.repository_commit
        assert commit["committed_at"] == c.repository_commit_at.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        for filename in ("1_bug_report.md", "2_feature_request.md"):
            template = provenance["templates"][c.repository_commit + "/" + filename]
            assert template["commit"] == c.repository_commit
            assert template["path"] == ".github/ISSUE_TEMPLATE/" + filename
            assert (
                hashlib.sha256(
                    ("\n".join(template["lines"]) + "\n").encode()
                ).hexdigest()
                == template["sha256"]
            )
    partitions = read(directory / "partitions.json")
    family_by_member = {}
    for family, members in partitions["evaluation"].items():
        for member in members:
            assert member not in family_by_member, "Family member assigned twice"
            family_by_member[member] = family
    for c in cases:
        assert family_by_member[c.issue_number] == c.issue_family_id
        if c.expected_outcome.earlier_issue_relationship in (
            "duplicate_candidate",
            "uncertain",
        ):
            assert family_by_member[c.earlier_issue.number] == c.issue_family_id
        assert all(
            r.created_at < c.opening_cutoff for r in candidate_references(c, cases)
        )
    assert not set(partitions["training"]["families"]) & set(partitions["evaluation"])
    assert not set(partitions["training"]["members"]) & set(family_by_member)
    coverage = Counter(c.expected_outcome.earlier_issue_relationship for c in cases)
    assert all(
        coverage[key] > 0
        for key in ("duplicate_candidate", "nonduplicate", "uncertain")
    )
    assert any(c.expected_outcome.missing_details for c in cases)
    assert any(not c.expected_outcome.missing_details for c in cases)
    metadata = {
        "status": "passed",
        "preserved_files": len(baseline["files"]),
        "case_count": len(cases),
        "new_confirmed_cases": sum(c.human_review.status == "confirmed" for c in added),
        "new_pending_cases": sum(c.human_review.status == "pending" for c in added),
        "family_count": len(partitions["evaluation"]),
        "family_members": len(family_by_member),
        "relationship_coverage": dict(coverage),
        "training_partition": "not_created; external/future corpus unverified",
    }
    return cases, original_numbers, metadata


def compare_results(result, original_numbers, previous_issue):
    old = read(ROOT / f"docs/evaluation/issue-{previous_issue}/run/results.json")
    names = {30: "thirty", 40: "forty", 50: "fifty"}
    previous = names[CASE_COUNTS[previous_issue]]
    expanded = names[result["planned_cases"]]
    old_rows = {(r["method"], r["issue_number"]): r for r in old["cases"]}
    changed = []
    retained = []
    for row in result["cases"]:
        key = row["method"], row["issue_number"]
        if key not in old_rows:
            continue
        before = old_rows[key]
        changes = {}
        # Scores include exact fields plus explicit abstention and retrieval coverage.
        for field in (
            "duplicate_retrieval",
            "duplicate_judgment",
            "issue_type",
            "missing_details",
            "citation_validity",
            "abstention",
        ):
            old_score = (before["scores"] or {}).get(field)
            new_score = (row["scores"] or {}).get(field)
            if old_score != new_score:
                changes[field] = {"before": old_score, "after": new_score}
        if before["error"] != row["error"]:
            changes["error"] = {"before": before["error"], "after": row["error"]}
        old_status = (before["report"] or {}).get("status")
        new_status = (row["report"] or {}).get("status")
        if old_status != new_status:
            changes["report_status"] = {"before": old_status, "after": new_status}
        entry = {
            "method": row["method"],
            "issue_number": row["issue_number"],
            "added_candidates": sorted(
                set(row["candidate_numbers"]) - set(before["candidate_numbers"])
            ),
            "removed_candidates": sorted(
                set(before["candidate_numbers"]) - set(row["candidate_numbers"])
            ),
            "report_changed": fingerprint(
                {k: v for k, v in (row["report"] or {}).items() if k != "trace_id"}
            )
            != fingerprint(
                {k: v for k, v in (before["report"] or {}).items() if k != "trace_id"}
            ),
            "changes": changes,
        }
        retained.append(entry)
        if changes:
            changed.append(entry)
    fields = tuple(CaseResult.__dataclass_fields__)
    groups = {}
    for label, rows in (
        (f"previous_{previous}", old["cases"]),
        (
            f"rerun_original_{previous}",
            [r for r in result["cases"] if r["issue_number"] in original_numbers],
        ),
        (
            "new_ten",
            [r for r in result["cases"] if r["issue_number"] not in original_numbers],
        ),
        (f"expanded_{expanded}", result["cases"]),
    ):
        groups[label] = {
            method: aggregate(
                [
                    CaseResult(**{f: r[f] for f in fields})
                    for r in rows
                    if r["method"] == method
                ]
            )
            for method in METHODS
        }
    return {
        "scope": (
            f"Field/status changes on original {previous}; "
            "new ten reported separately. "
            "Report comparisons exclude volatile trace IDs. "
            "No causal model-improvement claim."
        ),
        "changed_case_workflow_rows": len(changed),
        "changed_cases": sorted({r["issue_number"] for r in changed}),
        "changes": changed,
        "original_case_comparisons": retained,
        "scores": groups,
    }


def main(*, issue, previous_issue):
    directory = ROOT / f"docs/evaluation/issue-{issue}"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args()
    assert not args.allow_pending or args.metadata_only
    catalog, original_numbers, metadata = verify_metadata(
        directory, issue, allow_pending=args.allow_pending
    )
    if args.metadata_only:
        if not args.check_only:
            write(directory / "metadata-checks.json", metadata)
        print(json.dumps(metadata, indent=2))
        return
    result = read(directory / "run/results.json")
    assert (
        result["status"] == "complete" and result["planned_cases"] == CASE_COUNTS[issue]
    )
    assert result["comparison_issue"] == issue
    assert result["catalog_sha256"] == fingerprint(
        [c.model_dump(mode="json") for c in catalog]
    )
    assert (
        result["protocol_sha256"]
        == hashlib.sha256(
            (ROOT / f"docs/evaluation/issue-{issue}-protocol.md").read_bytes()
        ).hexdigest()
    )
    freeze = read(directory / "freeze.json")
    assert all(
        result[field] == freeze[field]
        for field in ("catalog_sha256", "protocol_sha256", "source_sha256")
    )
    assert all(
        hashlib.sha256(
            subprocess.check_output(
                ["git", "show", f"{freeze['commit']}:{p}"],
                cwd=ROOT,
            )
        ).hexdigest()
        == h
        for p, h in result["source_sha256"].items()
    )
    for case in catalog:
        path = ROOT / f"src/maintainer_copilot/cases/pytest_{case.issue_number}.json"
        assert path.read_bytes() == subprocess.check_output(
            ["git", "show", f"{freeze['commit']}:{path.relative_to(ROOT)}"], cwd=ROOT
        )
    protocol_path = f"docs/evaluation/issue-{issue}-protocol.md"
    assert (ROOT / protocol_path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{freeze['commit']}:{protocol_path}"], cwd=ROOT
    )
    accounting = verify_comparison_records(directory, result, catalog)
    comparison = compare_results(result, original_numbers, previous_issue)
    verification = {**metadata, **accounting}
    if args.check_only:
        assert read(directory / "comparison.json") == comparison
        assert read(directory / "verification.json") == verification
    else:
        write(directory / "comparison.json", comparison)
        write(directory / "verification.json", verification)
    print(json.dumps(verification, indent=2))
