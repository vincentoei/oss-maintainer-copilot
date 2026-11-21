"""Present the final #48 replies with immutable before ratings and pending reviews."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

NAME = "pytest-triage:coder3b-ctx16k"


def fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest()


def present(report: dict[str, Any]) -> list[str]:
    lines = ["> " + line for line in report["draft_reply"].splitlines()]
    lines += [
        "",
        f"Report status: {report['status']}; type: {report['issue_type']}.",
        "Missing details: "
        + (", ".join(d["name"] for d in report["missing_details"]) or "none"),
        "",
    ]
    for item in report["duplicate_candidates"] + report["related_issues"]:
        lines += [f"- Relationship #{item['issue_number']}: {item['reason']}"]
    for citation in report["citations"]:
        lines += [
            f"- [{citation['id']}: {citation['description']}]({citation['source_url']})"
        ]
        if citation.get("passage"):
            lines += ["  Evidence: " + citation["passage"].replace("\n", " / ")]
    lines += [""]
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--review-json", type=Path, required=True)
    parser.add_argument("--presentation", type=Path, required=True)
    args = parser.parse_args()
    if args.review_json.exists() or args.presentation.exists():
        parser.error("Use new output paths; existing reviews are immutable")
    after = json.loads(args.results.read_text())
    before = json.loads(Path("docs/evaluation/issue-45-results.json").read_text())
    reviews = json.loads(Path("docs/evaluation/issue-45-human-review.json").read_text())
    old_cases = {c["issue_number"]: c for c in before["models"][NAME]["cases"]}
    old_reviews = {c["issue_number"]: c for c in reviews["cases"]}
    cases = after["models"][NAME]["cases"]
    assert len(cases) == 20 and {c["issue_number"] for c in cases} == set(old_cases)
    lines = [
        "# Issue #48: twenty-reply human review",
        "",
        "Rate each new reply **useful**, **partly useful**, or **not useful**, "
        "with a reason. Unsure stays pending. Rubric: Does the reply ask for "
        "needed details and explain relevant evidence without misleading claims?",
        "",
        "Before ratings belong only to #45. New ratings, separate citation "
        "support, relationship labels and other-field abstention judgments are "
        "pending until explicitly reviewed. These development-informed cases "
        "provide regression evidence, not independent generalization evidence.",
        "",
    ]
    pending = []
    for case in cases:
        n = case["issue_number"]
        report = case["report"]
        assert report is not None
        old_review = old_reviews[n]["draft_reply_usefulness"]
        real_response = bool(case["model_calls"]) and all(
            call.get("response") is not None for call in case["model_calls"]
        )
        lines += [
            f"## #{n}",
            "",
            f"[Opening](https://github.com/pytest-dev/pytest/issues/{n}); "
            f"cutoff `{case['opening_cutoff']}`; pinned commit "
            f"`{case['repository_commit']}`.",
            "",
            f"Before: **{old_review['rating']}** — {old_review['reason']}",
            "",
        ]
        lines += present(old_cases[n]["report"])
        lines += [f"After (real response received: {real_response}):", ""]
        lines += present(report)
        lines += ["New usefulness rating: **pending**. Reason: **pending**.", ""]
        pending.append(
            {
                "issue_number": n,
                "opening_cutoff": case["opening_cutoff"],
                "repository_commit": case["repository_commit"],
                "trace_id": report["trace_id"],
                "report_sha256": fingerprint(report),
                "draft_reply_sha256": hashlib.sha256(
                    report["draft_reply"].encode()
                ).hexdigest(),
                "before_rating": old_review["rating"],
                "real_response_received": real_response,
                "draft_reply_usefulness": {
                    "review_status": "pending_human_review",
                    "rating": None,
                    "reason": None,
                    "reviewer": None,
                },
                "separate_semantic_judgments": "pending_human_review",
            }
        )
    args.review_json.write_text(
        json.dumps(
            {
                "source": {
                    "artifact": str(args.results),
                    "sha256": hashlib.sha256(args.results.read_bytes()).hexdigest(),
                    "model_name": NAME,
                    "run_recorded_at": after["recorded_at"],
                },
                "rubric": reviews["rubric"],
                "summary": {
                    "cases": 20,
                    "reply_usefulness_reviewed": 0,
                    "reply_usefulness_pending": 20,
                },
                "scope": "Fresh run ratings only; no rating transferred from #45.",
                "cases": pending,
            },
            indent=2,
        )
        + "\n"
    )
    args.presentation.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
