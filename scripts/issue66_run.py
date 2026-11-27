"""Bounded issue #66 executor. Requires separate explicit maintainer approval."""

import argparse
import base64
import io
import json
import os
import time
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from issue66_candidate import SemanticSupportCandidate
from issue66_prepare import (
    BASE,
    HERE,
    LIMITS,
    MODEL,
    OLD,
    construct_report,
    digest,
    inputs,
    prepare,
    read,
)

from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.paired_evaluation import PairedBudget
from maintainer_copilot.trace import get_trace


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirects are forbidden")


def save(path, value):
    # Exclusive, durable writes preserve partial runs and refuse overwrite.
    with path.open("x") as handle:
        handle.write(json.dumps(value, indent=2) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def metadata(transport, route, payload=None):
    assert route in ("/api/version", "/api/tags", "/api/show", "/api/ps")
    request = Request(
        BASE.removesuffix("/v1") + route,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"},
    )
    with transport.open(request, timeout=5) as response:
        raw = response.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("Metadata response exceeds bound")
    return json.loads(raw)


def serving(transport):
    from hashlib import sha256

    inspection = read(OLD / "serving-inspection.json")
    expected = inspection["arms"]["triage-eval:qwen35-4b-16k-v1"]
    assert metadata(transport, "/api/version") == inspection["version"]
    tags = {m["name"]: m for m in metadata(transport, "/api/tags")["models"]}
    assert tags[MODEL]["digest"] == expected["digest"]
    show = metadata(transport, "/api/show", {"model": MODEL})
    for key in ("template", "renderer", "parser", "thinking"):
        assert show.get(key) == expected[key], key
    assert dict(
        line.split(None, 1) for line in show["parameters"].splitlines()
    ) == dict(line.split(None, 1) for line in expected["parameters"].splitlines())
    assert (
        sha256(json.dumps(show["model_info"], sort_keys=True).encode()).hexdigest()
        == (expected["tokenizer_and_gguf_metadata_sha256"])
    )
    return {"version": inspection["version"], "tag": tags[MODEL], "show": show}


def execute(approved_freeze):
    if not __debug__:
        raise RuntimeError("Run assertions without Python optimization")
    if approved_freeze != digest(HERE / "freeze.json"):
        raise ValueError("Approval must identify this exact frozen proposal")
    # This does not establish user approval: the operator must obtain it first.
    # It makes accidental use against a changed proposal fail before networking.
    prepare(check=True)
    cases, evidence, catalog = inputs()
    rows = read(HERE / "requests.json")
    allowed = {(r["arm"], r["id"]): r["request_sha256"] for r in rows}
    assert len(allowed) == LIMITS["calls"]
    run = HERE / "run"
    run.mkdir(exist_ok=False)
    save(run / "proposal.json", {"approved_freeze_sha256": approved_freeze})
    budget = PairedBudget(
        run / "reservations.jsonl",
        allowed,
        per_model=LIMITS["per_arm"],
        total=LIMITS["calls"],
    )
    # Fixed numeric private route, no proxy, redirect, retry or alternate host.
    transport = build_opener(ProxyHandler({}), NoRedirect())
    results = []
    try:
        save(run / "serving-before.json", serving(transport))
        for case in cases:
            for arm, cls in (
                ("control", OpenAICompatibleModel),
                ("candidate", SemanticSupportCandidate),
            ):
                calls = []
                native_before = serving(transport)
                residency = metadata(transport, "/api/ps")

                def endpoint(request, *, timeout, arm=arm, case=case, calls=calls):
                    assert request.full_url == BASE + "/chat/completions"
                    assert timeout == 20
                    assert not calls
                    budget.reserve(arm, case["id"], request.data)
                    call = {"http_status": None, "raw_base64": None, "error": None}
                    calls.append(call)
                    started = time.perf_counter()
                    raw = None
                    try:
                        with transport.open(request, timeout=20) as response:
                            call["http_status"] = response.status
                            raw = response.read(65537)
                        return io.BytesIO(raw)
                    except HTTPError as exc:
                        call["http_status"] = exc.code
                        raw = exc.read(65537)
                        call["error"] = type(exc).__name__
                        raise
                    except Exception as exc:
                        call["error"] = type(exc).__name__
                        raise
                    finally:
                        call["latency_ms"] = (time.perf_counter() - started) * 1000
                        call["raw_base64"] = (
                            base64.b64encode(raw).decode() if raw is not None else None
                        )
                        save(run / f"{arm}-{case['id']}-call.json", call)

                started = time.perf_counter()
                with patch("maintainer_copilot.model.urlopen", endpoint):
                    report = construct_report(
                        case,
                        cls(BASE, MODEL, reasoning_effort="none"),
                        evidence,
                        catalog,
                    )
                row = {
                    "arm": arm,
                    "id": case["id"],
                    "expected": case["expected"],
                    "cohort": case["cohort"],
                    "report": report.model_dump(mode="json"),
                    "trace": get_trace(report.trace_id).model_dump(mode="json"),
                    "calls": calls,
                    "report_latency_ms": (time.perf_counter() - started) * 1000,
                    "residency_before": residency,
                }
                save(run / f"{arm}-{case['id']}-report.json", row)
                results.append(row)
                assert len(calls) == 1
                # Failed/invalid reports are saved and retained in the denominator.
                # Continue the fixed allocation unless identity/guardrails drift.
                assert serving(transport) == native_before
                call = calls[0]
                if call["http_status"] == 200 and call["raw_base64"] is not None:
                    raw = base64.b64decode(call["raw_base64"])
                    assert len(raw) <= 65536
                    envelope = json.loads(raw)
                    assert envelope["model"] == MODEL
                    usage = envelope["usage"]
                    assert type(usage["completion_tokens"]) is int
                    assert 0 <= usage["completion_tokens"] <= 256
                    assert type(usage["prompt_tokens"]) is int
                    assert 0 <= usage["prompt_tokens"] <= 16384 - 256
                    message = envelope["choices"][0]["message"]
                    assert not any(
                        message.get(k)
                        for k in ("thinking", "reasoning", "reasoning_content")
                    )
        assert len(results) == LIMITS["calls"]
        save(run / "complete.json", {"reports": len(results)})
    except BaseException as exc:
        save(run / "halt.json", {"error": type(exc).__name__, "reports": len(results)})
        raise
    finally:
        save(run / "results.json", results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-freeze-sha256", required=True)
    execute(parser.parse_args().approved_freeze_sha256)
