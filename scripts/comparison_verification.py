"""Shared offline integrity checks for archived workflow-comparison records."""

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from maintainer_copilot.evaluation import score_report
from maintainer_copilot.replay import HistoricalCase, candidate_references
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.workflow_comparison import (
    METHODS,
    fingerprint,
    summarize_comparison,
)


def read(path: Path) -> Any:
    return json.loads(path.read_text())


def verify_comparison_records(
    directory: Path, result: dict[str, Any], catalog: list[HistoricalCase]
) -> dict[str, Any]:
    """Verify every row, charged dispatch, score and fresh review fingerprint."""
    case_count = result["planned_cases"]
    assert len(catalog) == case_count
    cases = {c.issue_number: c for c in catalog}
    assert {r["issue_number"] for r in result["preflight"]} == set(cases)
    assert len(result["preflight"]) == case_count
    assert Counter(
        (r["method"], r["issue_number"]) for r in result["cases"]
    ) == Counter((method, number) for method in METHODS for number in cases)
    requests = [
        json.loads(line)
        for line in (directory / "run/requests.jsonl").read_text().splitlines()
    ]
    responses = [
        json.loads(line)
        for line in (directory / "run/responses.jsonl").read_text().splitlines()
    ]
    assert len(requests) <= case_count * 5
    assert [r["request"] for r in requests] == list(range(1, len(requests) + 1))
    assert [r["request"] for r in responses] == [r["request"] for r in requests]
    counts = Counter((r["method"], r["issue_number"]) for r in requests)
    assert all(
        n in cases and count <= {"fixed_rag": 1, "bounded_agent": 4}[m]
        for (m, n), count in counts.items()
    )
    assert sum(r["method"] == "fixed_rag" for r in requests) <= case_count
    assert sum(r["method"] == "bounded_agent" for r in requests) <= case_count * 4
    for request, response in zip(requests, responses, strict=True):
        assert request["case_count"] == case_count and request["max_tokens"] == 256
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
    reviews = read(directory / "run/human-review.json")
    identities = read(directory / "run/review-key.json")
    reports = {(r["method"], r["issue_number"]): r["report"] for r in result["cases"]}
    assert len(reviews) == len(identities) == case_count * len(METHODS)
    for review, identity in zip(reviews, identities, strict=True):
        assert review["code"] == identity["code"]
        assert (
            review["report_sha256"]
            == identity["report_sha256"]
            == fingerprint(reports[identity["method"], identity["issue_number"]])
        )
        assert review["status"] == "pending" and review["rating"] is None
    return {
        "workflow_rows": len(result["cases"]),
        "shared_eligible_cases": sum(r["error"] is None for r in result["preflight"]),
        "dispatches": len(requests),
        "response_records": len(responses),
        "raw_responses": sum("raw_response_utf8" in r for r in responses),
        "score_recomputations": sum(r["scores"] is not None for r in result["cases"]),
        "fresh_report_reviews_pending": len(reviews),
    }
