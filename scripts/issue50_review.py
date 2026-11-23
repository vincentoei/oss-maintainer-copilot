"""Make fresh anonymous review sheets; never transfer or infer human ratings."""

import hashlib
import json
import random
from pathlib import Path

root = Path("/tmp/issue-50-run")
destination = Path("docs/evaluation/issue-50")
destination.mkdir(exist_ok=True)
out = destination / "human-review.json"
sheet = destination / "human-review.md"
if out.exists() or sheet.exists():
    raise SystemExit("Review sheets already exist; do not overwrite reviews")
control_parts = [
    json.loads((root / "development-2-A.json").read_text()),
    json.loads((root / "development-2-A-recovered.json").read_text()),
]
control = {c["issue_number"]: c for part in control_parts for c in part["cases"]}
candidate = json.loads((root / "development-2-B.json").read_text())
expected_ids = {c["issue_number"] for c in control_parts[0]["cases"]}
assert set(control) == expected_ids
assert {c["issue_number"] for c in candidate["cases"]} == expected_ids
assert len(expected_ids) == 20
rows = [(n, "A", c) for n, c in control.items()]
rows += [(c["issue_number"], "B", c) for c in candidate["cases"]]
random.Random(50).shuffle(rows)
review = []
key = []
lines = [
    "# Issue #50 fresh anonymous development review",
    "",
    "Review each reply: useful / partly useful / not useful, with a reason.",
    "Separately mark each factual assertion or question presupposition supported /",
    "unsupported / unsure; assess supplied-detail redundancy, relationships and",
    "abstention. Citation syntax and exact quotes do not establish semantic support.",
    "Failures remain in denominators. No #48 rating is transferred.",
    "",
]
for index, (number, arm, record) in enumerate(rows, 1):
    code = f"R{index:02}"
    report = record["report"]
    draft = report["draft_reply"] if report else None
    fingerprint = hashlib.sha256(
        json.dumps(report, sort_keys=True).encode()
    ).hexdigest()
    draft_hash = hashlib.sha256(draft.encode()).hexdigest() if draft else None
    key.append({"code": code, "arm": arm, "issue_number": number})
    review.append(
        {
            "code": code,
            "issue_number": number,
            "report_sha256": fingerprint,
            "draft_reply_sha256": draft_hash,
            "usefulness": {"status": "pending"},
            "semantic_support": {"status": "pending"},
            "relationship_quality": {"status": "pending"},
            "abstention": {"status": "pending"},
        }
    )
    lines.extend(
        [
            f"## {code}: pytest #{number}",
            "",
            f"[Opening](https://github.com/pytest-dev/pytest/issues/{number})",
            f"Cutoff: {record['opening_cutoff']}; "
            f"revision: {record['repository_commit']}.",
            "",
            draft or f"No report: {record['error']}",
            "",
        ]
    )
    if report:
        lines += ["Evidence supplied in report:", ""]
        for citation in report["citations"]:
            lines.append(f"- [{citation['id']}] {citation['source_url']}")
            if citation["passage"]:
                lines.extend(["", "> " + citation["passage"].replace("\n", "\n> "), ""])
        lines += ["Review: pending. Reason: pending. Semantic support: pending.", ""]
out.write_text(json.dumps(review, indent=2) + "\n")
sheet.write_text("\n".join(lines))
(destination / "review-identity-key.json").write_text(json.dumps(key, indent=2) + "\n")
