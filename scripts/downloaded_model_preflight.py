"""Run the unscored application and thinking-disabled probes on pinned aliases."""

import hashlib
import io
import json
import subprocess
from argparse import ArgumentParser
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request

from downloaded_model_pull import DATA, LOCAL, PLAN, installed, local_json, save_new

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.local_evaluation import _GpuMemory
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.trace import get_trace

HASHES = DATA / "requests.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def invoke(alias, dispatch, observer):
    client = OpenAICompatibleModel(
        PLAN["local_host"] + "/v1", alias, response_observer=observer
    )
    with patch("maintainer_copilot.model.urlopen", dispatch):
        return triage_issue(
            IssueUnderReview(**PLAN["opening"]),
            documentation_topics=(),
            model_client=client,
        )


def wire(request, timeout, alias, mode):
    payload = json.loads(request.data)
    if (
        timeout != PLAN["timeout_seconds"]
        or request.full_url != PLAN["local_host"] + "/v1/chat/completions"
        or payload["model"] != alias
        or payload["max_tokens"] != PLAN["max_output_tokens"]
        or payload["response_format"]["json_schema"]["strict"] is not True
    ):
        raise RuntimeError("Probe no longer matches the plan")
    if mode == "reasoning_effort_none":
        payload["reasoning_effort"] = "none"
        return json.dumps(payload).encode()
    if mode != "application":
        raise ValueError("Unplanned probe")
    return request.data


def prepare():
    hashes = {}
    for model in PLAN["models"].values():
        alias = model["alias"]
        hashes[alias] = {}
        for mode in PLAN["modes"]:

            def capture(request, *, timeout, alias=alias, mode=mode):
                hashes[alias][mode] = sha(wire(request, timeout, alias, mode))
                return io.BytesIO(b"{}")

            invoke(alias, capture, None)
    save_new(HASHES, hashes)


def prepare_alias(name, model):
    tags = installed()
    parent = tags[model["tag"]]
    if (
        parent["digest"] != model["sha256"]
        or parent["details"]["quantization_level"] != "Q4_K_M"
        or local_json("/api/version")["version"] != PLAN["ollama_version"]
    ):
        raise ValueError("Unexpected parent identity, quantization or Ollama version")
    alias = model["alias"]
    if alias in tags:
        raise FileExistsError(alias)
    params = PLAN["parameters"]
    result = local_json(
        "/api/create",
        {"model": alias, "from": model["tag"], "parameters": params, "stream": False},
        timeout=180,
    )
    if result.get("status") != "success":
        raise ValueError(result)
    tag = installed()[alias]
    summaries = {}
    for ref in (model["tag"], alias):
        show = local_json("/api/show", {"model": ref})
        summaries[ref] = {
            key: val
            for key, val in show.items()
            if key
            in {
                "parameters",
                "template",
                "renderer",
                "parser",
                "thinking",
                "details",
                "capabilities",
            }
        }
    save_new(DATA / "run" / name / "alias.json", {"tag": tag, "show": summaries})
    if tag["details"]["parent_model"] != model["tag"]:
        raise ValueError("Unexpected parent alias")
    child = summaries[alias]
    if set(child["capabilities"]) != set(summaries[model["tag"]]["capabilities"]):
        raise ValueError("Alias changed capabilities")
    for key in ("template", "renderer", "parser"):
        if child.get(key) != summaries[model["tag"]].get(key):
            raise ValueError(f"Alias changed {key}")
    actual = dict(line.split(None, 1) for line in child["parameters"].splitlines())
    if any(float(actual[key]) != value for key, value in params.items()):
        raise ValueError("Alias parameter mismatch")
    return tag


def probe(name, model, tag, mode, expected_hash):
    alias = model["alias"]
    folder = DATA / "run" / name
    raw = []
    row = {
        "mode": mode,
        "alias": alias,
        "before": local_json("/api/ps"),
        "http_status": None,
    }

    def dispatch(request, *, timeout):
        data = wire(request, timeout, alias, mode)
        digest = sha(data)
        if digest != expected_hash or installed()[alias]["digest"] != tag["digest"]:
            raise RuntimeError("Frozen body or alias changed")
        save_new(
            folder / f"{mode}-reservation.json",
            {"request_sha256": digest, "alias_sha256": tag["digest"]},
        )
        req = Request(
            request.full_url, data=data, headers={"Content-Type": "application/json"}
        )
        try:
            response = LOCAL.open(req, timeout=timeout)
        except HTTPError as exc:
            row["http_status"] = exc.code
            with exc:
                row["server_error"] = exc.read(65537).decode(errors="replace")
            raise
        except OSError as exc:
            row["transport_error"] = str(exc)
            raise
        row["http_status"] = response.status
        return response

    with _GpuMemory(True) as gpu:
        report = invoke(alias, dispatch, raw.append)
    row["gpu"] = gpu.summary()
    row["after"] = local_json("/api/ps")
    row["model_event"] = next(
        event.model_dump(mode="json")
        for event in get_trace(report.trace_id).events
        if event.name == "triage_selection"
    )
    row["type"] = report.issue_type
    if raw:
        row["response_sha256"] = sha(raw[0])
        try:
            envelope = json.loads(raw[0])
            choice = envelope["choices"][0]
            message = choice["message"]
            row.update(
                response_model=envelope["model"],
                finish_reason=choice.get("finish_reason"),
                usage=envelope.get("usage"),
                content=message.get("content"),
                message_fields=sorted(message),
                reasoning_chars={
                    key: len(message.get(key) or "")
                    for key in ("thinking", "reasoning", "reasoning_content")
                },
            )
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            row["envelope_error"] = type(exc).__name__
    resident = [m for m in row["after"]["models"] if m["digest"] == tag["digest"]]
    row["full_gpu_16k"] = any(
        m["context_length"] == 16384 and m["size"] == m["size_vram"] > 0
        for m in resident
    )
    row["valid_application_json"] = (
        row["model_event"]["status"] == "ok"
        and row.get("response_model") == alias
        and row.get("finish_reason") == "stop"
    )
    save_new(folder / f"{mode}.json", row)
    print(
        name,
        mode,
        row["http_status"],
        row["valid_application_json"],
        row["full_gpu_16k"],
        flush=True,
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("action", choices=["prepare", *PLAN["models"]])
    action = parser.parse_args().action
    if action == "prepare":
        prepare()
        return
    for path in (HASHES, DATA / "preflight.json", __file__):
        subprocess.run(["git", "diff", "--quiet", "HEAD", "--", str(path)], check=True)
    model = PLAN["models"][action]
    tag = prepare_alias(action, model)
    expected = json.loads(HASHES.read_bytes())[model["alias"]]
    for mode in PLAN["modes"]:
        probe(action, model, tag, mode, expected[mode])


if __name__ == "__main__":
    main()
