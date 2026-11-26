"""Execute the source-frozen #62 comparison once, on the approved local host."""

import hashlib
import json
import os
import subprocess
from time import perf_counter
from unittest.mock import patch
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener

from issue62_prepare import ALIASES, DATA, PROBES, prepare

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.local_evaluation import (
    _GpuMemory,
    _LiveEvidenceCache,
    _ollama_json,
)
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.paired_evaluation import PairedBudget
from maintainer_copilot.replay import load_cases, replay_case
from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import (
    ROOT,
    _EvidenceSnapshot,
    _save,
    fingerprint,
)

HERE = DATA / "issue-62"
RUN = HERE / "run"
HOST = "http://172.17.48.1:11434"


class LocalOnly(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def check_freeze(*, live):
    freeze = json.loads((HERE / "freeze.json").read_bytes())
    source = freeze["runner_commit"]
    for name, digest in freeze["sha256"].items():
        data = (
            subprocess.check_output(["git", "show", f"{source}:{name}"], cwd=ROOT)
            if not live and name.startswith(("scripts/", "src/"))
            else (ROOT / name).read_bytes()
        )
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Frozen file changed: {name}")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", source, "HEAD"], cwd=ROOT, check=True
    )
    if live:
        subprocess.run(
            ["git", "diff", "--quiet", source, "--", "src", "scripts"],
            cwd=ROOT,
            check=True,
        )
        recorded = subprocess.check_output(
            ["git", "show", "HEAD:docs/evaluation/issue-62/freeze.json"], cwd=ROOT
        )
        if recorded != (HERE / "freeze.json").read_bytes():
            raise ValueError("Execution freeze must be committed before dispatch")
    if freeze["models"] != list(ALIASES) or (
        freeze["per_model"],
        freeze["total"],
        freeze["model_api_usd"],
        freeze["downloads"],
    ) != (56, 112, 0, 0):
        raise ValueError("Frozen budget or arms changed")
    return freeze


def check_serving():
    inventory = json.loads((HERE / "serving-inventory.json").read_bytes())
    if _ollama_json(HOST + "/api/version")["version"] != inventory["ollama_version"]:
        raise ValueError("Ollama version changed")
    tags = {m["name"]: m for m in _ollama_json(HOST + "/api/tags")["models"]}
    for arm in inventory["proposed_arms"]:
        tag = tags[arm["alias"]]
        if (tag["digest"], tag["details"]["quantization_level"]) != (
            arm["digest"],
            arm["quantization"],
        ):
            raise ValueError("Local alias changed")
        show = _ollama_json(HOST + "/api/show", {"model": arm["alias"]})
        if (fingerprint(show["template"]), show["parameters"]) != (
            arm["template_sha256"],
            arm["parameters"],
        ):
            raise ValueError("Template or serving options changed")
    return _ollama_json(HOST + "/api/ps")


def main():
    freeze = check_freeze(live=True)
    if RUN.exists():
        raise FileExistsError("The #62 run already exists")
    # Use the Windows Ollama WSL adapter directly, bypassing HTTP proxies.
    os.environ["no_proxy"] = "172.17.48.1"
    transport = build_opener(ProxyHandler({}), LocalOnly())
    cache = _LiveEvidenceCache()
    evidence = _EvidenceSnapshot(cache, cache, cache)
    current = prepare(evidence)
    evidence.frozen = True
    frozen = json.loads((HERE / "preparation.json").read_bytes())
    catalog = load_cases()
    cases = {f"h-{c.issue_number}": c for c in catalog}
    probes = {p["id"]: p for p in json.loads(PROBES.read_bytes())["cases"]}
    review = json.loads((HERE / "contrast-review.json").read_bytes())
    if (
        review["status"] != "confirmed"
        or review["probes_sha256"] != frozen["probes_file_sha256"]
        or current["fresh"] != frozen["fresh"]
    ):
        raise ValueError("Reviewed fresh request set changed")
    keys = list(cases) + list(probes)
    planned = frozen["historical"] + frozen["fresh"]
    if len(set(keys)) != 56 or len(planned) != 56:
        raise ValueError("Frozen request count changed")
    allowed = {
        (alias, key): row["wire"]["body_sha256"][alias]
        for key, row in zip(keys, planned, strict=True)
        for alias in ALIASES
    }
    flags = {
        key: row["error"] or "Historical request changed"
        for key, row, old in zip(
            cases, current["historical"], frozen["historical"], strict=True
        )
        if row != old or row["error"]
    }
    if not flags and not current["evidence_manifest_matches_issue60"]:
        raise ValueError("Evidence manifest differs from #60")
    initial = check_serving()
    RUN.mkdir()
    ledger = RUN / "reservations.jsonl"
    ledger.touch(exist_ok=False)
    budget = PairedBudget(
        ledger, allowed, per_model=freeze["per_model"], total=freeze["total"]
    )
    _save(
        RUN / "preflight.json",
        {"flags": flags, "residency": initial, "evidence_sha256": evidence.manifest()},
    )
    for alias in ALIASES:
        arm = RUN / alias.split(":")[1]
        arm.mkdir()
        _save(arm / "serving-before.json", check_serving())
        for key in keys:
            expected = (
                cases[key].expected_outcome.issue_type
                if key in cases
                else review["expected_types"][key]
            )
            row = {
                "case": key,
                "alias": alias,
                "expected": expected,
                "status": "unavailable",
                "error": flags.get(key),
            }
            if key not in flags:
                run_case(row, budget, transport, cases, probes, catalog, evidence)
            _save(arm / f"{key}.json", row)
        _save(arm / "serving-after.json", check_serving())


def run_case(row, budget, transport, cases, probes, catalog, evidence):
    key, alias = row["case"], row["alias"]
    raw = []
    fatal = []

    def dispatch(request, *, timeout):
        if timeout != 20 or request.full_url != HOST + "/v1/chat/completions":
            fatal.append("Unapproved route or timeout")
            raise ValueError(fatal[-1])
        try:
            budget.reserve(alias, key, request.data)
        except Exception as exc:
            fatal.append(str(exc))
            raise
        return transport.open(request, timeout=timeout)

    client = OpenAICompatibleModel(HOST + "/v1", alias, response_observer=raw.append)
    with _GpuMemory(True) as gpu, patch("maintainer_copilot.model.urlopen", dispatch):
        start = perf_counter()
        if key in cases:
            report = replay_case(
                cases[key],
                candidate_catalog=catalog,
                keyword_filter=True,
                model_client=client,
                commit_source=evidence,
                source_reader=evidence,
                issue_source=evidence,
            )
        else:
            p = probes[key]
            report = triage_issue(
                IssueUnderReview(title=p["title"], body=p["body"]),
                model_client=client,
                documentation_topics=(),
            )
        row["replay_ms"] = round((perf_counter() - start) * 1000, 3)
    if fatal:
        raise ValueError(fatal[0])
    trace = get_trace(report.trace_id)
    (event,) = (e for e in trace.events if e.name == "triage_selection")
    row.update(
        status=(
            "valid"
            if event.status == "ok"
            else "validation_error"
            if raw
            else "transport_error"
        ),
        report=report.model_dump(mode="json"),
        model_event=event.model_dump(mode="json"),
        gpu=gpu.summary(),
        raw_response=raw[0].decode(errors="replace") if raw else None,
    )
    if row["status"] != "valid":
        row["error"] = event.error


if __name__ == "__main__":
    main()
