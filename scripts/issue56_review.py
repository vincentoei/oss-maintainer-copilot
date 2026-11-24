"""Publish attributed assistant reviews from explicit, manually assessed decisions."""

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from maintainer_copilot.replay import (
    allowed_case_citation_urls,
    candidate_references,
    load_cases,
)
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def verified_openings(catalog, evidence):
    expected = {}
    for case in catalog:
        entries = [
            (case.issue_number, case.opening_cutoff, case.opening_content_sha256),
            *(
                (ref.number, ref.created_at, ref.content_sha256)
                for ref in candidate_references(case, catalog)
            ),
        ]
        for number, created_at, digest in entries:
            assert expected.setdefault(number, (created_at, digest)) == (
                created_at,
                digest,
            )
        commit = read(evidence / f"commit-{case.repository_commit}.json")
        assert commit["sha"] == case.repository_commit
        assert (
            datetime.fromisoformat(commit["committed_at"].replace("Z", "+00:00"))
            == case.repository_commit_at
        )
    openings = {}
    for number, (created_at, digest) in expected.items():
        opening = read(evidence / f"issue-{number}.json")
        assert opening["number"] == number
        assert (
            datetime.fromisoformat(opening["created_at"].replace("Z", "+00:00"))
            == created_at
        )
        assert (
            hashlib.sha256(
                (opening["title"] + "\0" + opening["body"]).encode()
            ).hexdigest()
            == digest
        ), f"Changed opening #{number}"
        openings[number] = opening
    return openings


def citation_evidence(citation, evidence, openings, pinned_files):
    url = citation["source_url"]
    if issue := re.fullmatch(r"https://github.com/pytest-dev/pytest/issues/(\d+)", url):
        opening = openings[int(issue[1])]
        passage = citation.get("passage")
        if passage:
            assert all(line in opening["body"] for line in passage.splitlines())
        return {
            "url": url,
            "opening_content_sha256": hashlib.sha256(
                (opening["title"] + "\0" + opening["body"]).encode()
            ).hexdigest(),
        }
    blob = re.fullmatch(
        r"https://github.com/pytest-dev/pytest/blob/([0-9a-f]{40})/(.+)#L(\d+)(?:-L(\d+))?",
        url,
    )
    assert blob is not None, f"Unsupported review evidence: {url}"
    pinned = read(evidence / f"file-{blob[1]}-{blob[2].replace('/', '_')}.json")
    expected = pinned_files[blob[1] + "/" + blob[2]]
    assert pinned["commit"] == expected["commit"] == blob[1]
    assert pinned["path"] == expected["path"] == blob[2]
    assert (
        hashlib.sha256(pinned["text"].encode()).hexdigest()
        == pinned["sha256"]
        == expected["sha256"]
    )
    lines = pinned["text"].splitlines()[int(blob[3]) - 1 : int(blob[4] or blob[3])]
    assert lines
    passage = citation.get("passage")
    if passage:
        assert passage in "\n".join(lines) or passage == " ".join(lines)
    return {"url": url, "file_sha256": pinned["sha256"], "cited_lines": lines}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-issue", type=int, choices=(18, 56), required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    result = read(ROOT / f"docs/evaluation/issue-{args.source_issue}/run/results.json")
    identities = read(
        ROOT / f"docs/evaluation/issue-{args.source_issue}/run/review-key.json"
    )
    decisions = read(args.decisions)
    catalog = load_cases()
    cases = {case.issue_number: case for case in catalog}
    openings = verified_openings(catalog, args.evidence)
    pinned_files = read(ROOT / "docs/evaluation/issue-56/review-evidence.json")[
        "pinned_files"
    ]
    assert set(decisions) == {str(r["issue_number"]) for r in result["cases"]}
    codes = {(x["method"], x["issue_number"]): x for x in identities}
    reviews = []
    groups = {}
    reviewed_at = datetime.now(UTC).isoformat()
    for row in result["cases"]:
        case = cases[row["issue_number"]]
        assert row["opening_content_sha256"] == case.opening_content_sha256
        assert row["opening_cutoff"] == case.opening_cutoff.isoformat()
        assert row["repository_commit"] == case.repository_commit
        report = row["report"]
        identity = codes[row["method"], row["issue_number"]]
        assert fingerprint(report) == identity["report_sha256"]
        note = decisions[str(row["issue_number"])]
        note = {**note, **note.get("method_overrides", {}).get(row["method"], {})}
        assert type(note["rating"]) is int and note["rating"] in (0, 1, 2)
        assert note["reason"] and note["semantic_support"] in (
            "supported",
            "partially_supported",
            "unsupported",
            "abstained",
        )
        assert report is not None, "Unavailable reports need explicit review handling"
        allowed = allowed_case_citation_urls(
            case, [r.number for r in candidate_references(case, catalog)]
        )
        assert all(c["source_url"] in allowed for c in report["citations"])
        claims = {
            k: v
            for k, v in report.items()
            if k not in ("trace_id", "context", "issue_type", "issue_type_quote")
        }
        group_key = row["issue_number"], fingerprint(claims)
        group = groups.setdefault(group_key, f"G{len(groups) + 1:03}")
        redundant = note.get("redundant", [])
        assert set(redundant) <= {d["name"] for d in report["missing_details"]}
        reviews.append(
            {
                "code": identity["code"],
                "method": row["method"],
                "issue_number": row["issue_number"],
                "report_sha256": fingerprint(report),
                "opening_content_sha256": row["opening_content_sha256"],
                "reviewer": "Codex",
                "reviewed_at": reviewed_at,
                "independent_human_review": False,
                "blinded": False,
                "review_group": group,
                "status": "assistant_reviewed",
                "rating": note["rating"],
                "reason": note["reason"],
                "semantic_support": note["semantic_support"],
                "unsupported_claims_or_presuppositions": [
                    *note.get("unsupported_presuppositions", []),
                    *(
                        f"Request assumes {d} is absent despite supplied information."
                        for d in redundant
                    ),
                ],
                "redundant_requests": redundant,
                "missing_requests": note.get("missing", []),
                "relationships": note.get(
                    "relationships", "No relationship claim needing semantic support."
                ),
                "abstention": (
                    "Reviewed in the reason; unavailable historical CI remains "
                    "a legitimate abstention."
                ),
                "type_field": row["scores"]["issue_type"],
                "evidence": [
                    citation_evidence(c, args.evidence, openings, pinned_files)
                    for c in report["citations"]
                ],
            }
        )
    summary = {
        "source_issue": args.source_issue,
        "reviewer": "Codex",
        "independent_human_review": False,
        "blinded": False,
        "reports": len(reviews),
        "review_groups": len(groups),
        "historical_opening_identities_verified": len(openings),
        "pinned_file_identity_manifest": (
            "docs/evaluation/issue-56/review-evidence.json"
        ),
        "rating_counts": dict(Counter(r["rating"] for r in reviews)),
        "semantic_support_counts": dict(
            Counter(r["semantic_support"] for r in reviews)
        ),
        "by_method": {
            method: {
                "reports": sum(r["method"] == method for r in reviews),
                "rating_total": sum(
                    r["rating"] for r in reviews if r["method"] == method
                ),
                "redundant_request_reports": sum(
                    bool(r["redundant_requests"])
                    for r in reviews
                    if r["method"] == method
                ),
            }
            for method in sorted({r["method"] for r in reviews})
        },
        "method": (
            "Explicit case-by-case Codex decisions after reading verified openings, "
            "pinned templates/docs/source and earlier openings. Identical claim "
            "content for the same opening is grouped. Type-field agreement is "
            "reported separately. "
            "Citation identity checks verify references, not semantic support. "
            "No old human ratings were transferred; no workflow promotion follows."
        ),
    }
    args.directory.mkdir(parents=True, exist_ok=False)
    for filename, value in (("reviews.json", reviews), ("summary.json", summary)):
        (args.directory / filename).write_text(json.dumps(value, indent=2) + "\n")
    lines = [
        f"# Issue #{args.source_issue} Codex report review",
        "",
        summary["method"],
        "",
        "This is an attributed assistant assessment, not independent human review.",
        "",
    ]
    for r in reviews:
        lines.extend(
            [
                f"## {r['code']}: #{r['issue_number']} / {r['method']}",
                "",
                f"Report: `{r['report_sha256']}`; group {r['review_group']}.",
                "",
                f"Usefulness: {r['rating']}/2. "
                f"Semantic support: {r['semantic_support']}.",
                "",
                r["reason"],
                "",
            ]
        )
    (args.directory / "review.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
