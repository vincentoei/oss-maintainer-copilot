"""Frozen one-pass pilot; explicit human case confirmation is mandatory."""

# All model methods run synchronously before advancing either loop.
# ruff: noqa: B023

import fcntl
import hashlib
import json
import os
import platform
import re
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from maintainer_copilot import model
from maintainer_copilot.issue_search import GitHubIssueSource
from maintainer_copilot.local_evaluation import _GpuMemory, _ollama_json
from maintainer_copilot.replay import GitHubCommitSource, _FrozenIssues, content_hash
from maintainer_copilot.trace import get_trace
from maintainer_copilot.triage import IssueUnderReview, triage_issue

ROOT = Path("/tmp/issue-50-run")
BASE = "http://172.17.48.1:11434"
manifest = json.loads(Path("docs/evaluation/issue-50-pilot.json").read_text())
assert manifest["status"] == "human_confirmed_frozen_before_inference"
assert len(manifest["cases"]) == 5
assert all(c["human_review"]["status"] == "confirmed" for c in manifest["cases"])
os.environ["GITHUB_TOKEN"] = subprocess.check_output(
    ["gh", "auth", "token"], text=True
).strip()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


# Verify all openings and cutoff revisions before any inference.
openings = {}
for case in manifest["cases"]:
    opening = GitHubIssueSource().get_issue(case["issue_number"])
    assert content_hash(opening) == case["opening_content_sha256"]
    assert (
        opening.created_at.isoformat()
        == datetime.fromisoformat(
            case["opening_cutoff"].replace("Z", "+00:00")
        ).isoformat()
    )
    commit = GitHubCommitSource().get_commit(case["repository_commit"])
    assert commit.sha == case["repository_commit"]
    assert commit.committed_at < opening.created_at
    openings[case["issue_number"]] = opening

for arm, alias in [
    ("A", "pytest-triage:coder3b-ctx16k"),
    ("B", "pytest-triage:coder3b-ctx16k"),
    ("C", "pytest-triage:qwen3-4b-ctx16k"),
    ("D", "pytest-triage:coder7b-ctx16k"),
]:
    output = ROOT / f"pilot-{arm}.json"
    if output.exists():
        raise SystemExit(f"Pilot {arm} already attempted; do not rerun")
    result = {
        "arm": arm,
        "alias": alias,
        "partition": "reserved-pilot",
        "application_commit": "1b4d500",
        "pilot_manifest_sha256": fingerprint(manifest),
        "opened_at": datetime.now(UTC).isoformat(),
        "platform": platform.platform(),
        "cases": [],
        "review_status": "pending",
    }
    output.write_text(json.dumps(result, indent=2) + "\n")
    try:
        tags = _ollama_json(BASE + "/api/tags")
        identity = next(m for m in tags["models"] if m["name"] == alias)
        show = _ollama_json(BASE + "/api/show", {"model": alias})
        params = dict(re.findall(r"^(\w+)\s+(\S+)\s*$", show["parameters"], re.M))
        expected = dict(
            num_ctx=16384, temperature=0, seed=42, top_k=20, top_p=0.8, repeat_penalty=1
        )
        assert all(float(params[k]) == v for k, v in expected.items())
        assert identity["details"]["quantization_level"] == "Q4_K_M"
        baseline = json.loads(
            Path("docs/evaluation/issue-21-selection.json").read_text()
        )
        source_name = {
            "A": "qwen2.5-coder:3b-instruct-q4_K_M",
            "B": "qwen2.5-coder:3b-instruct-q4_K_M",
            "C": "qwen3:4b-instruct-2507-q4_K_M",
            "D": "qwen2.5-coder:7b-instruct-q4_K_M",
        }[arm]
        source_identity = next(m for m in tags["models"] if m["name"] == source_name)
        assert (
            source_identity["digest"]
            == baseline["models"][source_name]["identity"]["digest"]
        )
        result["serving"] = {
            "identity": identity,
            "show": show,
            "source_identity": source_identity,
            "version": _ollama_json(BASE + "/api/version"),
            "template_sha256": fingerprint(show.get("template")),
        }
    except Exception as exc:
        result["serving_error"] = type(exc).__name__
        output.write_text(json.dumps(result, indent=2) + "\n")
        continue

    class Observed(model.OpenAICompatibleModel):
        drafting = arm != "A"
        evidence_enabled = True
        report_max_tokens = 512

        def generate_json(
            self, system_prompt, user_data, *, max_tokens, response_schema=None
        ):
            with (ROOT / "requests.jsonl").open("a+") as ledger:
                fcntl.flock(ledger, fcntl.LOCK_EX)
                ledger.seek(0)
                records = [json.loads(line) for line in ledger if line.strip()]
                if len(records) >= 120:
                    raise model.ModelUnavailable("Experiment budget exhausted")
                record = {
                    "request": len(records) + 1,
                    "partition": "reserved-pilot",
                    "arm": arm,
                    "issue_number": current_case["issue_number"],
                    "warmup": False,
                    "max_tokens": max_tokens,
                    "prompt_sha256": fingerprint(system_prompt),
                    "schema_sha256": fingerprint(response_schema),
                    "input_sha256": fingerprint(user_data),
                    "evidence_sha256": fingerprint(user_data.get("evidence_passages")),
                    "at": datetime.now(UTC).isoformat(),
                }
                if any(
                    r.get("partition") == "reserved-pilot"
                    and r.get("arm") == arm
                    and r.get("issue_number") == current_case["issue_number"]
                    for r in records
                ):
                    raise model.ModelUnavailable("Pilot case already dispatched")
                ledger.write(json.dumps(record) + "\n")
                ledger.flush()
                os.fsync(ledger.fileno())
            try:
                response = super().generate_json(
                    system_prompt,
                    user_data,
                    max_tokens=max_tokens,
                    response_schema=response_schema,
                )
            except Exception as exc:
                calls.append(
                    {
                        **record,
                        "error": type(exc).__name__,
                        "provider_error": type(exc.__cause__).__name__,
                    }
                )
                raise
            else:
                calls.append(
                    {
                        **record,
                        "response": asdict(response)
                        if isinstance(response, model.ModelResponse)
                        else response,
                    }
                )
                return response

    for current_case in manifest["cases"]:
        opening = openings[current_case["issue_number"]]
        calls = []
        started = perf_counter()
        report = None
        error = None
        with _GpuMemory(True) as gpu:
            try:
                report = triage_issue(
                    IssueUnderReview(
                        number=opening.number, title=opening.title, body=opening.body
                    ),
                    source=_FrozenIssues(opening, (), True),
                    model_client=Observed(BASE + "/v1", alias),
                    documentation_topics=(),
                    template_revision=current_case["repository_commit"],
                )
            except Exception as exc:
                error = type(exc).__name__
        try:
            residency = _ollama_json(BASE + "/api/ps")
        except Exception as exc:
            residency = {"error": type(exc).__name__}
        trace = get_trace(report.trace_id) if report else None
        result["cases"].append(
            {
                "issue_number": opening.number,
                "error": error,
                "latency_ms": round((perf_counter() - started) * 1000, 3),
                "opening_content_sha256": content_hash(opening),
                "opening_cutoff": current_case["opening_cutoff"],
                "repository_commit": current_case["repository_commit"],
                "report": report.model_dump(mode="json") if report else None,
                "trace": trace.model_dump(mode="json") if trace else None,
                "model_calls": calls,
                "gpu_memory": gpu.summary(),
                "residency": residency,
                "review_status": "pending",
            }
        )
        output.write_text(json.dumps(result, indent=2) + "\n")
        print(arm, opening.number, report.status if report else error, flush=True)
