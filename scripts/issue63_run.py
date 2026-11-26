"""Freeze or execute the explicitly approved issue #63 local allocation once."""

import base64
import json
import os
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager
from hashlib import sha256
from ipaddress import ip_address
from time import perf_counter
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener
from uuid import UUID

from downloaded_scored_prepare import CACHE, restore
from issue62_compare import LocalOnly
from issue63_application import HERE, application, browser_package, integration
from issue63_prepare import prepare

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot import model as model_module
from maintainer_copilot.local_evaluation import _GpuMemory
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.paired_evaluation import PairedBudget
from maintainer_copilot.replay import load_cases, replay_case
from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import ROOT, _save

LIMITS = {
    "calls": 55,
    "output_per_call": 256,
    "total_output": 14080,
    "timeout": 20,
    "response_bytes": 65536,
    "context": 16384,
    "warmups": 0,
    "retries": 0,
    "downloads": 0,
    "hosted": 0,
    "api_usd": 0,
}
RUN = HERE / "run"
TRANSPORT = build_opener(ProxyHandler({}), LocalOnly())


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def metadata(base, route, payload=None):
    request = Request(
        base + route,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"},
    )
    with TRANSPORT.open(request, timeout=5) as response:
        raw = response.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("Metadata response exceeds bound")
    return json.loads(raw)


def serving_matches(inspection, selected=None):
    base = inspection["base_url"]
    address = urlsplit(base)
    if (
        address.scheme != "http"
        or address.port != 11434
        or address.path
        or address.username
        or address.password
        or not ip_address(address.hostname).is_private
    ):
        raise ValueError("Only the inspected private Ollama HTTP route is allowed")
    if metadata(base, "/api/version") != inspection["version"]:
        raise ValueError("Ollama version changed")
    tags = {m["name"]: m for m in metadata(base, "/api/tags")["models"]}
    for alias, expected in inspection["arms"].items():
        if selected is not None and alias != selected:
            continue
        if tags[alias]["digest"] != expected["digest"]:
            raise ValueError("Model alias changed: " + alias)
        show = metadata(base, "/api/show", {"model": alias})
        for key in ("parameters", "template", "renderer", "parser", "thinking"):
            if show.get(key) != expected[key]:
                raise ValueError("Serving setting changed: " + key)
        observed = sha256(
            json.dumps(show["model_info"], sort_keys=True).encode()
        ).hexdigest()
        if observed != expected["tokenizer_and_gguf_metadata_sha256"]:
            raise ValueError("Tokenizer/model metadata changed")


def freeze():
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
        raise ValueError("Commit the exact preparation before freezing")
    preview = read(HERE / "request-preview.json")
    if preview != prepare() or preview["expected_type_review"]["status"] != "confirmed":
        raise ValueError("Reviewed requests no longer reproduce")
    if any(row["error"] for row in preview["rows"]):
        raise ValueError(
            "Resolve or explicitly freeze flagged evidence before execution"
        )
    if preview["fixed_request_slots"] + preview["integration_slots"] != LIMITS["calls"]:
        raise ValueError("Unexpected request count")
    serving_matches(read(HERE / "serving-inspection.json"))
    files = [
        "proposal.md",
        "proposed-cases.json",
        "integration-inputs.json",
        "serving-inspection.json",
        "request-preview.json",
        "browser-tools.json",
    ]
    payload = {
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "limits": LIMITS,
        "sha256": {name: digest(HERE / name) for name in files},
        "snapshot_sha256": digest(CACHE),
        "source_sha256": {
            str(path.relative_to(ROOT)): digest(path)
            for path in [
                *sorted((ROOT / "src/maintainer_copilot").glob("*.py")),
                *sorted((ROOT / "scripts").glob("*.py")),
                ROOT / "scripts/issue63_browser.cjs",
            ]
        },
    }
    with (HERE / "freeze.json").open("x") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


class Capture:
    def __init__(self, allowed, base):
        self.budget = PairedBudget(
            RUN / "reservations.jsonl", allowed, per_model=25, total=LIMITS["calls"]
        )
        self.base = base
        self.slots = []
        self.alias = None
        self.calls = []
        self.fatal = None
        self.closed = False

    def close(self):
        self.closed = True
        self.slots = []

    @contextmanager
    def dispatch(self, request, *, timeout):
        if self.closed:
            raise ValueError("Evaluation transport is closed")
        body = json.loads(request.data)
        if (
            not self.slots
            or timeout != LIMITS["timeout"]
            or request.full_url != self.base + "/v1/chat/completions"
            or body.get("reasoning_effort") != "none"
            or body.get("max_tokens") != 256
            or body.get("model") != self.alias
        ):
            self.fatal = "Unplanned application request"
            raise ValueError(self.fatal)
        slot = self.slots.pop(0)
        try:
            self.budget.reserve(body["model"], slot, request.data)
        except Exception:
            self.fatal = "Request does not match frozen allocation"
            raise
        call = {
            "slot": slot,
            "alias": body["model"],
            "http_status": None,
            "transport_error": None,
            "raw_base64": None,
            "request_sha256": sha256(request.data).hexdigest(),
        }
        self.calls.append(call)
        started = perf_counter()
        try:
            with TRANSPORT.open(request, timeout=timeout) as response:
                call["http_status"] = response.status

                class Body:
                    def read(self, size):
                        raw = response.read(size)
                        call["raw_base64"] = base64.b64encode(raw).decode()
                        return raw

                yield Body()
        except HTTPError as exc:
            call["http_status"] = exc.code
            call["transport_error"] = type(exc).__name__
            with exc:
                call["raw_base64"] = base64.b64encode(exc.read(65537)).decode()
            raise
        except OSError as exc:
            cause = exc.reason if isinstance(exc, URLError) else exc
            call["transport_error"] = type(cause).__name__
            raise
        except BaseException as exc:
            call["transport_error"] = type(exc).__name__
            raise
        finally:
            call["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            _save(
                RUN
                / "calls"
                / f"{len(self.budget.ledger.read_text().splitlines()):02}.json",
                call,
            )


def plan():
    preview = read(HERE / "request-preview.json")
    aliases = list(read(HERE / "serving-inspection.json")["arms"])
    allowed, observations = {}, []
    for alias in aliases:
        for row in preview["rows"]:
            key = row["id"]
            allowed[alias, key] = row["wire_sha256"][alias]
            observations.append(
                {
                    "alias": alias,
                    "id": key,
                    "cohort": row["cohort"],
                    "expected": row["proposed_expected"],
                    "slots": [key],
                }
            )
            for field in (
                "opening_cutoff",
                "opening_content_sha256",
                "repository_commit",
                "candidate_numbers",
            ):
                if field in row:
                    observations[-1][field] = row[field]
    for row in preview["integrations"]:
        slots = [
            "i-" + row["id"] + "-" + str(i)
            for i in range(1, len(row["wire_sha256"]) + 1)
        ]
        for slot, hashed in zip(slots, row["wire_sha256"], strict=True):
            allowed[aliases[-1], slot] = hashed
        observations.append(
            {
                "alias": aliases[-1],
                "id": row["id"],
                "cohort": "integration",
                "kind": row["kind"],
                "input_id": row["input_id"],
                "expected": "type: bug",
                "slots": slots,
            }
        )
    return allowed, observations


def run():
    approved = read(HERE / "approval.json")
    if (
        approved.get("status") != "approved"
        or approved.get("reviewer") != "requesting user"
        or approved.get("freeze_sha256") != digest(HERE / "freeze.json")
        or approved.get("limits") != LIMITS
    ):
        raise ValueError(
            "Explicit approval of this exact frozen allocation is required"
        )
    frozen = read(HERE / "freeze.json")
    if frozen["limits"] != LIMITS or any(
        digest(HERE / name) != hashed for name, hashed in frozen["sha256"].items()
    ):
        raise ValueError("Frozen preparation changed")
    if digest(CACHE) != frozen["snapshot_sha256"]:
        raise ValueError("Historical evidence changed")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", frozen["source_commit"], "HEAD"],
        cwd=ROOT,
        check=True,
    )
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", frozen["source_commit"], "HEAD"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT) or not set(
        changed
    ) <= {
        "docs/evaluation/issue-63/freeze.json",
        "docs/evaluation/issue-63/approval.json",
    }:
        raise ValueError("Live run requires clean committed source/freeze/approval")
    inspection = read(HERE / "serving-inspection.json")
    browser_package()
    serving_matches(inspection)
    resident = metadata(inspection["base_url"], "/api/ps")["models"]
    if len(resident) > 1 or any(m["name"] not in inspection["arms"] for m in resident):
        raise ValueError(
            "Unrelated or nonserial runner is resident; no allocation started"
        )
    execute(inspection)


def execute(inspection):
    """CLI driver and offline-fixture seam; leaves the process transport closed."""
    allowed, observations = plan()
    RUN.mkdir()
    (RUN / "calls").mkdir()
    capture = Capture(allowed, inspection["base_url"])
    catalog = load_cases()
    historical = {f"h-{c.issue_number}": c for c in catalog}
    fresh = {c["id"]: c for c in read(HERE / "proposed-cases.json")["cases"]}
    inputs = {c["id"]: c for c in read(HERE / "integration-inputs.json")}
    evidence = restore()
    results = [
        dict(o, status="undispatched", report=None, calls=[]) for o in observations
    ]
    aliases = list(inspection["arms"])
    first = set()
    administrative = []
    row = None
    _save(RUN / "results.json", results)
    # This dedicated evaluator process must never restore a live unguarded
    # transport while a timed-out HTTP/browser worker might still be running.
    model_module.urlopen = capture.dispatch
    try:
        with application(inspection["base_url"], on_close=capture.close) as url:
            for row in results:
                alias, key = row["alias"], row["id"]
                capture.alias = alias
                capture.slots, capture.calls = list(row["slots"]), []
                serving_matches(inspection, alias)
                if alias not in first:
                    serving_matches(inspection)
                    residency = metadata(inspection["base_url"], "/api/ps")
                    if len(residency["models"]) > 1:
                        raise ValueError("Expected one serial runner at most")
                    for resident in residency["models"]:
                        if resident["name"] not in aliases:
                            raise ValueError(
                                "Unrelated model is resident; no unload authorized"
                            )
                        result = metadata(
                            inspection["base_url"],
                            "/api/generate",
                            {
                                "model": resident["name"],
                                "keep_alive": 0,
                                "stream": False,
                            },
                        )
                        administrative.append(
                            {
                                "request": {
                                    "model": resident["name"],
                                    "keep_alive": 0,
                                    "stream": False,
                                },
                                "response": result,
                            }
                        )
                        _save(RUN / "administrative.json", administrative)
                        if len(administrative) > 3:
                            raise ValueError(
                                "Administrative unload allocation exceeded"
                            )
                        if result.get("done_reason") != "unload":
                            raise ValueError(
                                "Administrative unload did not confirm unload"
                            )
                    if metadata(inspection["base_url"], "/api/ps")["models"]:
                        raise ValueError("Cannot verify empty cold-start residency")
                row["resident_before"] = metadata(inspection["base_url"], "/api/ps")
                started = perf_counter()
                with (
                    _GpuMemory(True) as gpu,
                    patch.dict(
                        os.environ,
                        {
                            "MODEL_NAME": alias,
                            "MODEL_REASONING_EFFORT": "none",
                            "MODEL_BASE_URL": inspection["base_url"] + "/v1",
                        },
                    ),
                ):
                    if row["cohort"] == "integration":
                        report = integration(row["kind"], inputs[row["input_id"]], url)
                    elif key in historical:
                        report = replay_case(
                            historical[key],
                            candidate_catalog=catalog,
                            keyword_filter=True,
                            model_client=OpenAICompatibleModel.from_environment(),
                            commit_source=evidence,
                            issue_source=evidence,
                            source_reader=evidence,
                        )
                    else:
                        opening = fresh[key]
                        report = triage_issue(
                            IssueUnderReview(
                                title=opening["title"], body=opening["body"]
                            ),
                            model_client=OpenAICompatibleModel.from_environment(),
                            documentation_topics=(),
                        )
                    elapsed = round((perf_counter() - started) * 1000, 3)
                row.update(
                    report=report.model_dump(mode="json"),
                    calls=capture.calls,
                    replay_ms=elapsed,
                    gpu=gpu.summary(),
                )
                row["trace"] = get_trace(UUID(row["report"]["trace_id"])).model_dump(
                    mode="json"
                )
                row["resident_after"] = metadata(inspection["base_url"], "/api/ps")
                row["reported_gpu_16k"] = any(
                    m["digest"] == inspection["arms"][alias]["digest"]
                    and m["context_length"] == 16384
                    and m["size"] == m["size_vram"] > 0
                    for m in row["resident_after"]["models"]
                )
                if not row["reported_gpu_16k"]:
                    capture.fatal = "Reported 16K GPU placement unavailable or changed"
                events = [e for e in row["trace"]["events"] if e["kind"] == "model"]
                row["status"] = (
                    "valid"
                    if events and all(e["status"] == "ok" for e in events)
                    else "model_error"
                )
                for call in row["calls"]:
                    raw = (
                        base64.b64decode(call["raw_base64"])
                        if call["raw_base64"]
                        else None
                    )
                    try:
                        envelope = json.loads(raw)
                        choice = envelope["choices"][0]
                        usage = envelope.get("usage")
                        usage = usage if isinstance(usage, dict) else {}
                        prompt, output = (
                            usage.get("prompt_tokens"),
                            usage.get("completion_tokens"),
                        )
                        call["usage"] = usage
                        call["truncation"] = "unknown"
                        if (
                            type(prompt) is not int
                            or type(output) is not int
                            or prompt < 0
                            or not 0 <= output <= 256
                            or prompt + 256 > 16384
                        ):
                            capture.fatal = (
                                "Usage missing or outside frozen token/context bounds"
                            )
                        if envelope["model"] != alias:
                            capture.fatal = "Returned model identity changed"
                        if any(
                            choice["message"].get(k)
                            for k in ("thinking", "reasoning", "reasoning_content")
                        ):
                            capture.fatal = (
                                "Thinking output exposed with explicit-off mode"
                            )
                        if choice["finish_reason"] != "stop":
                            row["status"] = "model_error"
                    except (
                        TypeError,
                        ValueError,
                        KeyError,
                        IndexError,
                        AttributeError,
                    ):
                        row["status"] = "model_error"
                if capture.fatal:
                    row["status"] = "invalid_observation"
                try:
                    serving_matches(inspection, alias)
                except Exception:
                    row["status"] = "identity_unverified"
                    raise
                _save(RUN / "results.json", results)
                print(alias, key, row["status"], flush=True)
                if capture.fatal or (alias not in first and row["status"] != "valid"):
                    raise ValueError(
                        capture.fatal or "First charged compatibility gate failed"
                    )
                first.add(alias)
        _save(
            RUN / "complete.json",
            {"charged": len(capture.budget.ledger.read_text().splitlines())},
        )
    except BaseException as exc:
        if row is not None:
            row["calls"] = capture.calls
            row["status"] = (
                ("interrupted" if capture.calls else "unavailable")
                if row["status"] == "undispatched"
                else row["status"]
            )
            row["error"] = str(exc)
        _save(RUN / "results.json", results)
        _save(
            RUN / "halt.json",
            {
                "error": str(exc),
                "id": row["id"] if row else None,
                "alias": row["alias"] if row else None,
            },
        )
        raise
    finally:
        capture.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("action", choices=("freeze", "run"))
    arguments = parser.parse_args()
    freeze() if arguments.action == "freeze" else run()
