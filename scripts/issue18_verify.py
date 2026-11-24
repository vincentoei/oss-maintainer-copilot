"""Verify #18 metadata/accounting and publish deltas without network or inference."""

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.replay import candidate_references, load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import (
    METHODS,
    fingerprint,
    summarize_comparison,
)

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/evaluation/issue-18"


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def verify_metadata(*, allow_pending=False):
    baseline = read(DIRECTORY / "baseline.json")
    assert all(
        hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h
        for p, h in baseline["files"].items()
    ), "Preserved baseline artifact changed"
    cases = load_cases()
    assert len(cases) == len({c.issue_number for c in cases}) == 40
    original_numbers = {
        int(Path(p).stem.removeprefix("pytest_"))
        for p in baseline["files"]
        if p.startswith("src/maintainer_copilot/cases/")
    }
    assert len(original_numbers) == 30
    added = [c for c in cases if c.issue_number not in original_numbers]
    assert len(added) == 10
    provenance = read(DIRECTORY / "provenance.json")
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
    partitions = read(DIRECTORY / "partitions.json")
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


def compare_results(result, original_numbers):
    old = read(ROOT / "docs/evaluation/issue-17/run/results.json")
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
        ("previous_thirty", old["cases"]),
        (
            "rerun_original_thirty",
            [r for r in result["cases"] if r["issue_number"] in original_numbers],
        ),
        (
            "new_ten",
            [r for r in result["cases"] if r["issue_number"] not in original_numbers],
        ),
        ("expanded_forty", result["cases"]),
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
            "Field/status changes on original thirty; new ten reported separately. "
            "Report comparisons exclude volatile trace IDs. "
            "No causal model-improvement claim."
        ),
        "changed_case_workflow_rows": len(changed),
        "changed_cases": sorted({r["issue_number"] for r in changed}),
        "changes": changed,
        "original_case_comparisons": retained,
        "scores": groups,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args()
    assert not args.allow_pending or args.metadata_only
    catalog, original_numbers, metadata = verify_metadata(
        allow_pending=args.allow_pending
    )
    if args.metadata_only:
        write(DIRECTORY / "metadata-checks.json", metadata)
        print(json.dumps(metadata, indent=2))
        return
    result = read(DIRECTORY / "run/results.json")
    assert result["status"] == "complete" and result["planned_cases"] == 40
    assert result["comparison_issue"] == 18
    assert result["catalog_sha256"] == fingerprint(
        [c.model_dump(mode="json") for c in catalog]
    )
    assert (
        result["protocol_sha256"]
        == hashlib.sha256(
            (ROOT / "docs/evaluation/issue-18-protocol.md").read_bytes()
        ).hexdigest()
    )
    freeze = read(DIRECTORY / "freeze.json")
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
    for path in sorted((ROOT / "src/maintainer_copilot/cases").glob("*.json")):
        assert path.read_bytes() == subprocess.check_output(
            ["git", "show", f"{freeze['commit']}:{path.relative_to(ROOT)}"], cwd=ROOT
        )
    protocol_path = "docs/evaluation/issue-18-protocol.md"
    assert (ROOT / protocol_path).read_bytes() == subprocess.check_output(
        ["git", "show", f"{freeze['commit']}:{protocol_path}"], cwd=ROOT
    )
    cases = {c.issue_number: c for c in catalog}
    assert {r["issue_number"] for r in result["preflight"]} == set(cases)
    assert len(result["preflight"]) == 40
    assert Counter(
        (r["method"], r["issue_number"]) for r in result["cases"]
    ) == Counter((method, number) for method in METHODS for number in cases)
    requests = [
        json.loads(line)
        for line in (DIRECTORY / "run/requests.jsonl").read_text().splitlines()
    ]
    responses = [
        json.loads(line)
        for line in (DIRECTORY / "run/responses.jsonl").read_text().splitlines()
    ]
    assert len(requests) <= 200
    assert [r["request"] for r in requests] == list(range(1, len(requests) + 1))
    assert [r["request"] for r in responses] == [r["request"] for r in requests]
    counts = Counter((r["method"], r["issue_number"]) for r in requests)
    assert all(
        n in cases and count <= {"fixed_rag": 1, "bounded_agent": 4}[m]
        for (m, n), count in counts.items()
    )
    assert sum(r["method"] == "fixed_rag" for r in requests) <= 40
    assert sum(r["method"] == "bounded_agent" for r in requests) <= 160
    for request, response in zip(requests, responses, strict=True):
        assert request["case_count"] == 40 and request["max_tokens"] == 256
        assert all(response[k] == v for k, v in request.items())
        raw = response.get("raw_response_utf8")
        if raw is not None:
            assert (
                hashlib.sha256(raw.encode()).hexdigest()
                == response["raw_response_sha256"]
            )
            assert len(raw.encode()) == response["raw_response_bytes"] <= 65537
    calls = []
    for row in result["cases"]:
        c = cases[row["issue_number"]]
        assert row["opening_cutoff"] == c.opening_cutoff.isoformat()
        assert row["repository_commit"] == c.repository_commit
        assert row["opening_content_sha256"] == c.opening_content_sha256
        assert row["candidate_numbers"] == [
            r.number for r in candidate_references(c, catalog)
        ]
        if row["scores"] is not None:
            assert row["scores"] == score_report(
                c, TriageReport.model_validate(row["report"]), row["candidate_numbers"]
            )
        calls.extend(row["model_calls"])
    assert calls == responses
    assert result["summary"] == summarize_comparison(result)
    reviews = read(DIRECTORY / "run/human-review.json")
    identities = read(DIRECTORY / "run/review-key.json")
    reports = {(r["method"], r["issue_number"]): r["report"] for r in result["cases"]}
    assert len(reviews) == len(identities) == 120
    for review, identity in zip(reviews, identities, strict=True):
        assert review["code"] == identity["code"]
        assert (
            review["report_sha256"]
            == identity["report_sha256"]
            == fingerprint(reports[identity["method"], identity["issue_number"]])
        )
        assert review["status"] == "pending" and review["rating"] is None
    write(DIRECTORY / "comparison.json", compare_results(result, original_numbers))
    verification = {
        **metadata,
        "workflow_rows": len(result["cases"]),
        "shared_eligible_cases": sum(r["error"] is None for r in result["preflight"]),
        "dispatches": len(requests),
        "response_records": len(responses),
        "raw_responses": sum("raw_response_utf8" in r for r in responses),
        "score_recomputations": sum(r["scores"] is not None for r in result["cases"]),
        "fresh_report_reviews_pending": len(reviews),
    }
    write(DIRECTORY / "verification.json", verification)
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
