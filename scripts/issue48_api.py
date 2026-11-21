"""Verify both real report APIs against the focused #48 integration server."""

import argparse
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--openings", type=Path, required=True)
parser.add_argument("--calls", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
if args.output.exists():
    parser.error("Use a new output artifact path")
openings = json.loads(args.openings.read_text())
rows = []
ledger = args.calls
for number in [12116, 12146, 12219, 12224]:
    for endpoint in ["/api/triage", "/api/agent/triage"]:
        issue = openings[str(number)]
        start = time.perf_counter()
        first = len(json.loads(ledger.read_text())) if ledger.exists() else 0
        request = Request(
            "http://127.0.0.1:8001" + endpoint,
            data=json.dumps(
                {"number": number, "title": issue["title"], "body": issue["body"]}
            ).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=60) as r:
            report = json.load(r)
            status = r.status
        with urlopen("http://127.0.0.1:8001/api/traces/" + report["trace_id"]) as r:
            trace = json.load(r)
        calls = json.loads(ledger.read_text())[first:]
        assertions = {
            "http_ok": status == 200,
            "matching_trace": trace["trace_id"] == report["trace_id"],
            "real_model_usage": any(
                e["kind"] == "model"
                and e["status"] == "ok"
                and (e["input_tokens"] or 0) > 0
                for e in trace["events"]
            ),
            "model_calls_bounded": len(
                [e for e in trace["events"] if e["kind"] == "model"]
            )
            <= 4,
        }
        if number == 12116:
            assertions["supplied_packages_not_requested"] = "pip list output" not in [
                d["name"] for d in report["missing_details"]
            ]
        if number == 12146:
            assertions["targeted_comparison"] = (
                "same pytest version and identical tuple values"
                in report["draft_reply"]
            )
        if number == 12219:
            assertions["minimized_failing_case"] = (
                "minimized failing example" in report["draft_reply"]
            )
        if number == 12224:
            assertions["argument_file_mismatch_removed"] = 11871 not in [
                s["issue_number"]
                for s in report["related_issues"] + report["duplicate_candidates"]
            ]
        rows.append(
            {
                "issue_number": number,
                "endpoint": endpoint,
                "input_content_sha256": hashlib.sha256(
                    (issue["title"] + "\0" + issue["body"]).encode()
                ).hexdigest(),
                "latency_ms": round((time.perf_counter() - start) * 1000, 3),
                "assertions": assertions,
                "report": report,
                "trace": trace,
                "model_calls": calls,
            }
        )
        print(number, endpoint, assertions, flush=True)
args.output.write_text(
    json.dumps(
        {
            "recorded_at": datetime.now(UTC).isoformat(),
            "scope": (
                "Real existing API and bounded-agent integration with content-verified "
                "original openings and frozen eligible keyword candidate catalog. "
                "Ordinary live documentation source; separate from historical field "
                "scoring. No controlled model responses."
            ),
            "cases": rows,
        },
        indent=2,
    )
    + "\n"
)
assert all(all(row["assertions"].values()) for row in rows)
