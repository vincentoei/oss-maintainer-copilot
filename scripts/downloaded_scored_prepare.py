"""Acquire once, then freeze matched public replay inputs without model dispatch."""

import io
import json
from argparse import ArgumentParser
from dataclasses import asdict
from datetime import datetime
from hashlib import sha256
from unittest.mock import patch

import issue62_prepare as previous
from downloaded_model_pull import DATA, PLAN, save_new

from maintainer_copilot.issue_search import IssueRecord
from maintainer_copilot.local_evaluation import _LiveEvidenceCache
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import RepositoryCommit, load_cases
from maintainer_copilot.source import SourceExcerpt
from maintainer_copilot.workflow_comparison import _EvidenceSnapshot

HERE = DATA / "scored"
CACHE = previous.ROOT / ".local/downloaded-scored/snapshot.json"
REFERENCE = "pytest-triage:coder7b-ctx16k"
ALIASES = (REFERENCE, *(m["alias"] for m in PLAN["models"].values()))
OLD = previous.DATA / "issue-62"


def read(path):
    return json.loads(path.read_bytes())


def acquire():
    cache = _LiveEvidenceCache()
    evidence = _EvidenceSnapshot(cache, cache, cache)
    result = previous.prepare(evidence)
    snapshot = {
        "commits": [
            asdict(c) | {"committed_at": c.committed_at.isoformat()}
            for c in cache.commits.values()
        ],
        "issues": [
            asdict(i) | {"created_at": i.created_at.isoformat()}
            for i in cache.issues.values()
        ],
        "excerpts": [e.model_dump(mode="json") for e in cache.excerpts.values()],
        "flags": {
            str(r["issue_number"]): r["error"]
            for r in result["historical"]
            if r["error"]
        },
        "manifest": evidence.manifest(),
    }
    save_new(CACHE, snapshot)


def restore():
    saved = read(CACHE)
    # A miss raises before any public read. Flagged cases never reach inference.
    evidence = _EvidenceSnapshot(None, None, None)
    evidence.frozen = True
    for c in saved["commits"]:
        evidence.commit_cache["commit", c["sha"]] = RepositoryCommit(
            c["sha"], datetime.fromisoformat(c["committed_at"])
        )
    for i in saved["issues"]:
        evidence.issue_cache["issue", i["number"]] = IssueRecord(
            **(i | {"created_at": datetime.fromisoformat(i["created_at"])})
        )
    for item in saved["excerpts"]:
        e = SourceExcerpt.model_validate(item)
        evidence.source_cache["source", e.commit, e.path, e.line] = e
    return evidence


def with_effort(body):
    payload = json.loads(body)
    if "reasoning_effort" in payload or payload["max_tokens"] != 256:
        raise ValueError("Application transport or output cap changed")
    return json.dumps(payload | {"reasoning_effort": "none"}).encode()


def prepare():
    original = read(OLD / "preparation.json")
    review = read(OLD / "contrast-review.json")
    if (
        review["status"] != "confirmed"
        or review["probes_sha256"] != sha256(previous.PROBES.read_bytes()).hexdigest()
    ):
        raise ValueError("Reviewed contrast inputs changed")
    evidence = restore()
    hashes = {}

    def matched(prompt, data, limit, schema):
        old_wire = original_encoder(prompt, data, limit, schema)

        def capture(request, *, timeout):
            body = json.loads(request.data)
            identity = body["model"]
            if identity == REFERENCE:
                assert (
                    sha256(request.data).hexdigest()
                    == old_wire["body_sha256"][REFERENCE]
                )
            hashes.setdefault(old_wire["body_without_alias_sha256"], {})[identity] = (
                sha256(with_effort(request.data)).hexdigest()
            )
            return io.BytesIO(b'{"choices":[{"message":{"content":"{}"}}]}')

        with patch("maintainer_copilot.model.urlopen", capture):
            for alias in ALIASES:
                OpenAICompatibleModel("http://unused.invalid/v1", alias).generate_json(
                    prompt, data, max_tokens=limit, response_schema=schema
                )
        return old_wire

    original_encoder = previous.wire_fingerprints
    with patch.object(previous, "wire_fingerprints", matched):
        current = previous.prepare(evidence)
    snapshot = read(CACHE)
    if not snapshot["flags"] and (
        evidence.manifest() != read(OLD / "run/preflight.json")["evidence_sha256"]
        or not current["evidence_manifest_matches_issue60"]
    ):
        raise ValueError("Verified public evidence differs from #62")
    expectations = {
        f"h-{c.issue_number}": c.expected_outcome.issue_type for c in load_cases()
    } | review["expected_types"]
    rows = {}
    for cohort in ("historical", "fresh"):
        for new, old in zip(current[cohort], original[cohort], strict=True):
            key = f"h-{old['issue_number']}" if cohort == "historical" else old["id"]
            error = snapshot["flags"].get(str(old.get("issue_number"))) or new.get(
                "error"
            )
            if new != old:
                error = error or "Inputs differ from #62 preflight"
            body_hashes = (
                {} if error else hashes[new["wire"]["body_without_alias_sha256"]]
            )
            if not error and set(body_hashes) != set(ALIASES):
                raise ValueError("Missing application serialization")
            rows[key] = dict(
                cohort=cohort,
                expected=expectations[key],
                error=error,
                sha256=body_hashes,
            )
    if set(rows) != set(expectations):
        raise ValueError("Unexpected cases")
    if len(rows) != 56:
        raise ValueError("Unexpected case count")
    return rows


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("action", choices=["acquire", "prepare"])
    if parser.parse_args().action == "acquire":
        acquire()
    else:
        save_new(HERE / "requests.json", prepare())
