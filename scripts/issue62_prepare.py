"""Reconstruct paired input fingerprints without a model server or predictions."""

import argparse
import hashlib
import io
import json
from pathlib import Path
from unittest.mock import patch

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.classification_evaluation import AvailabilityModel
from maintainer_copilot.local_evaluation import _LiveEvidenceCache
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import (
    CaseFlagged,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import ROOT, _EvidenceSnapshot, fingerprint

DATA = ROOT / "docs/evaluation"
PROBES = DATA / "issue-62/proposed-contrasts.json"

ALIASES = ("pytest-triage:coder3b-ctx16k", "pytest-triage:coder7b-ctx16k")


def wire_fingerprints(prompt, user_data, max_tokens, schema):
    # Exercise the actual JSON serializer. The local stub never opens a socket.
    hashes = {}
    inputs = []

    def receive(request, *, timeout):
        body = json.loads(request.data)
        alias = body.pop("model")
        hashes[alias] = hashlib.sha256(request.data).hexdigest()
        inputs.append(body)
        return io.BytesIO(b'{"choices":[{"message":{"content":"{}"}}]}')

    with patch("maintainer_copilot.model.urlopen", receive):
        for alias in ALIASES:
            client = OpenAICompatibleModel("http://unused.invalid/v1", alias)
            client.generate_json(
                prompt, user_data, max_tokens=max_tokens, response_schema=schema
            )
    if tuple(hashes) != ALIASES or len(inputs) != 2 or inputs[0] != inputs[1]:
        raise ValueError("Paired application requests differ beyond model identity")
    return {"body_sha256": hashes, "body_without_alias_sha256": fingerprint(inputs[0])}


class Capture(AvailabilityModel):
    def __init__(self):
        super().__init__()
        self.request = None
        self.wire = None

    def generate_json(
        self, system_prompt, user_data, *, max_tokens, response_schema=None
    ):
        self.wire = wire_fingerprints(
            system_prompt, user_data, max_tokens, response_schema
        )
        self.request = {
            "prompt_sha256": fingerprint(system_prompt),
            "input_sha256": fingerprint(user_data),
            "schema_sha256": fingerprint(response_schema),
            "max_tokens": max_tokens,
        }
        return super().generate_json(
            system_prompt,
            user_data,
            max_tokens=max_tokens,
            response_schema=response_schema,
        )


def prepare(evidence=None):
    baseline = DATA / "issue-60/followup"
    original = json.loads((baseline / "results.json").read_bytes())
    requests = {
        r["issue_number"]: r
        for r in map(json.loads, (baseline / "requests.jsonl").read_text().splitlines())
    }
    catalog = load_cases()
    catalog_hash = fingerprint([c.model_dump(mode="json") for c in catalog])
    if len(catalog) != 50 or catalog_hash != original["catalog_sha256"]:
        raise ValueError("Reviewed historical catalog changed")
    if evidence is None:
        cache = _LiveEvidenceCache()
        evidence = _EvidenceSnapshot(cache, cache, cache)
    historical = []
    for case, archived in zip(catalog, original["cases"], strict=True):
        capture = Capture()
        error = None
        candidates = [ref.number for ref in candidate_references(case, catalog)]
        record = requests[case.issue_number]
        try:
            if (
                case.issue_number != archived["issue_number"]
                or candidates != archived["candidate_numbers"]
            ):
                raise CaseFlagged("Historical candidate pool changed")
            report = replay_case(
                case,
                candidate_catalog=catalog,
                keyword_filter=True,
                model_client=capture,
                issue_source=evidence,
                source_reader=evidence,
                commit_source=evidence,
            )
            trace = get_trace(report.trace_id)
            if trace is None or any(
                event.status != "ok"
                for event in trace.events
                if event.name
                in {
                    "triage_selection",
                    "get_documentation_passage",
                    "get_source_excerpt",
                }
            ):
                raise CaseFlagged("Historical evidence or model request unavailable")
            if capture.request is None or any(
                record[key] != value for key, value in capture.request.items()
            ):
                raise CaseFlagged("Encoded request differs from archived #60 input")
        except (CaseFlagged, ValueError) as exc:
            error = str(exc)
        historical.append(
            {
                "issue_number": case.issue_number,
                "opening_cutoff": case.opening_cutoff.isoformat(),
                "opening_content_sha256": case.opening_content_sha256,
                "repository_commit": case.repository_commit,
                "candidate_numbers": candidates,
                "request": capture.request,
                "wire": capture.wire,
                "error": error,
            }
        )
    probe_bytes = PROBES.read_bytes()
    probes = json.loads(probe_bytes)
    fresh = []
    for probe in probes["cases"]:
        capture = Capture()
        triage_issue(
            IssueUnderReview(title=probe["title"], body=probe["body"]),
            documentation_topics=(),
            model_client=capture,
        )
        if capture.request is None:
            raise ValueError(
                f"Fresh opening {probe['id']} did not reach the model boundary"
            )
        fresh.append(
            {"id": probe["id"], "request": capture.request, "wire": capture.wire}
        )
    return {
        "stage": "request preparation only",
        "model_dispatches": 0,
        "catalog_sha256": catalog_hash,
        "probes_file_sha256": hashlib.sha256(probe_bytes).hexdigest(),
        "review_status_at_preparation": probes["review_status"],
        "evidence_manifest_matches_issue60": evidence.manifest()
        == original["evidence_sha256"],
        "historical": historical,
        "fresh": fresh,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output file")
    manifest = prepare()
    with args.output.open("x") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    print(
        f"Historical rows: {len(manifest['historical'])}; flagged: "
        f"{sum(row['error'] is not None for row in manifest['historical'])}; "
        f"fresh: {len(manifest['fresh'])}; model dispatches: 0"
    )


if __name__ == "__main__":
    main()
