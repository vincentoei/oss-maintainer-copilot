"""Verify frozen issue #16 artifacts without network access or inference."""

import hashlib
import json
from collections import Counter
from pathlib import Path

from maintainer_copilot.evaluation import score_report
from maintainer_copilot.replay import load_cases
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import fingerprint, summarize_comparison


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root / "docs/evaluation/issue-16"
    result = json.loads((directory / "results.json").read_text())
    requests = [
        json.loads(line)
        for line in (directory / "requests.jsonl").read_text().splitlines()
    ]
    responses = [
        json.loads(line)
        for line in (directory / "responses.jsonl").read_text().splitlines()
    ]
    baseline = json.loads((root / "docs/evaluation/issue-16-baseline.json").read_text())
    assert all(
        hashlib.sha256((root / p).read_bytes()).hexdigest() == h
        for p, h in baseline["files"].items()
    )
    assert all(
        hashlib.sha256((root / p).read_bytes()).hexdigest() == h
        for p, h in result["source_sha256"].items()
    )
    assert (
        hashlib.sha256(
            (root / "docs/evaluation/issue-16-protocol.md").read_bytes()
        ).hexdigest()
        == result["protocol_sha256"]
    )
    catalog = load_cases()
    cases = {c.issue_number: c for c in catalog}
    assert (
        fingerprint([c.model_dump(mode="json") for c in catalog])
        == result["catalog_sha256"]
    )
    assert result["status"] == "complete" and len(result["cases"]) == 60
    assert len(result["preflight"]) == 20 and all(
        c["error"] is None for c in result["preflight"]
    )
    ids = [r["request"] for r in requests]
    assert ids == list(range(1, len(requests) + 1)) and len(ids) <= 100
    assert [r["request"] for r in responses] == ids
    assert Counter(
        (r["method"], r["issue_number"]) for r in result["cases"]
    ) == Counter(
        (method, number)
        for method in ("keyword_rule", "fixed_rag", "bounded_agent")
        for number in cases
    )
    dispatched = Counter((r["method"], r["issue_number"]) for r in requests)
    for (method, number), count in dispatched.items():
        assert number in cases and count <= {"fixed_rag": 1, "bounded_agent": 4}[method]
    assert sum(r["method"] == "fixed_rag" for r in requests) <= 20
    assert sum(r["method"] == "bounded_agent" for r in requests) <= 80
    for response, request in zip(responses, requests, strict=True):
        assert all(response[k] == v for k, v in request.items())
        assert request["max_tokens"] == 256
        raw = response["raw_response_utf8"].encode()
        assert hashlib.sha256(raw).hexdigest() == response["raw_response_sha256"]
        assert len(raw) == response["raw_response_bytes"] <= 65537
    row_calls = []
    for row in result["cases"]:
        case = cases[row["issue_number"]]
        assert row["opening_cutoff"] == case.opening_cutoff.isoformat()
        assert row["repository_commit"] == case.repository_commit
        assert row["opening_content_sha256"] == case.opening_content_sha256
        assert row["scores"] == score_report(
            case, TriageReport.model_validate(row["report"]), row["candidate_numbers"]
        )
        row_calls.extend(row["model_calls"])
        assert row["gpu_memory"]["sample_count"] == len(
            row["gpu_memory"]["samples_mib"]
        )
    assert row_calls == responses
    assert summarize_comparison(result) == result["summary"]
    reviews = json.loads((directory / "human-review.json").read_text())
    key = json.loads((directory / "review-key.json").read_text())
    reports = {(r["method"], r["issue_number"]): r["report"] for r in result["cases"]}
    assert len(reviews) == len(key) == 60
    for review, identity in zip(reviews, key, strict=True):
        assert review["code"] == identity["code"]
        assert (
            review["report_sha256"]
            == identity["report_sha256"]
            == fingerprint(reports[(identity["method"], identity["issue_number"])])
        )
        assert review["status"] == "pending" and review["rating"] is None
    verification = {
        "status": "passed",
        "preserved_baseline_files": len(baseline["files"]),
        "source_files_unchanged_since_inference_freeze": len(result["source_sha256"]),
        "case_rows": len(result["cases"]),
        "shared_eligible_cases": len(cases),
        "charged_dispatches": len(requests),
        "raw_responses": len(responses),
        "score_recomputations": 60,
        "human_reviews_pending": len(reviews),
        "scope": "Offline integrity/accounting checks; no semantic human review.",
    }
    (directory / "verification.json").write_text(
        json.dumps(verification, indent=2) + "\n"
    )
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
