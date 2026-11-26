"""Audit #62 preparation against the archived requests, without any public reads."""

import hashlib
import json

from issue62_prepare import DATA, PROBES, Capture

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.replay import load_cases
from maintainer_copilot.workflow_comparison import fingerprint


def main():
    if not __debug__:
        raise RuntimeError(
            "Run the artifact assertions with Python optimization disabled"
        )
    prep = json.loads((DATA / "issue-62/preparation.json").read_bytes())
    probe_bytes = PROBES.read_bytes()
    probes = json.loads(probe_bytes)
    original = DATA / "issue-60/followup"
    baseline = json.loads((original / "results.json").read_bytes())
    archived_requests = [
        json.loads(line)
        for line in (original / "requests.jsonl").read_text().splitlines()
    ]
    assert (
        prep["catalog_sha256"]
        == baseline["catalog_sha256"]
        == fingerprint([case.model_dump(mode="json") for case in load_cases()])
    )
    assert prep["model_dispatches"] == 0
    assert prep["evidence_manifest_matches_issue60"]
    assert len(prep["historical"]) == 50
    for row, old, wire in zip(
        prep["historical"], baseline["cases"], archived_requests, strict=True
    ):
        for key in (
            "issue_number",
            "opening_cutoff",
            "opening_content_sha256",
            "repository_commit",
            "candidate_numbers",
        ):
            assert row[key] == old[key], (row["issue_number"], key)
        assert row["error"] is None and row["issue_number"] == wire["issue_number"]
        assert row["request"] == {
            key: wire[key]
            for key in ("prompt_sha256", "input_sha256", "schema_sha256", "max_tokens")
        }
    assert hashlib.sha256(probe_bytes).hexdigest() == prep["probes_file_sha256"]
    assert probes["review_status"] == prep["review_status_at_preparation"]
    assert len({p["id"] for p in probes["cases"]}) == len(probes["cases"]) == 6
    for probe, row in zip(probes["cases"], prep["fresh"], strict=True):
        capture = Capture()
        triage_issue(
            IssueUnderReview(title=probe["title"], body=probe["body"]),
            documentation_topics=(),
            model_client=capture,
        )
        assert row["id"] == probe["id"] and row["request"] == capture.request
        assert row["wire"] == capture.wire
    print("Verified 50 archived inputs and 6 synthetic inputs. No model calls.")


if __name__ == "__main__":
    main()
