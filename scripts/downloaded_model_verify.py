"""Replay recorded compatibility probes through the application, without Ollama."""

import base64
import hashlib
import io
import json

from downloaded_model_preflight import HASHES, invoke, wire
from downloaded_model_pull import DATA, PLAN

from maintainer_copilot.trace import get_trace


def read(path):
    return json.loads(path.read_bytes())


def verify_response(alias, mode, row, body, reservation):
    seen = []

    def replay(request, *, timeout):
        seen.append(hashlib.sha256(wire(request, timeout, alias, mode)).hexdigest())
        return io.BytesIO(body)

    report = invoke(alias, replay, None)
    assert seen == [reservation["request_sha256"]]
    trace = get_trace(report.trace_id)
    (event,) = (e for e in trace.events if e.name == "triage_selection")
    assert event.status == row["model_event"]["status"]
    assert report.issue_type == row["type"]
    envelope = json.loads(body)
    choice = envelope["choices"][0]
    assert row["valid_application_json"] == (
        event.status == "ok"
        and envelope["model"] == alias
        and choice["finish_reason"] == "stop"
    )
    assert row["reasoning_chars"] == {
        k: len(choice["message"].get(k) or "")
        for k in ("thinking", "reasoning", "reasoning_content")
    }


def verify():
    if not __debug__:
        raise RuntimeError("Run the audit without Python optimization")
    hashes = read(HASHES)
    bytes_planned = 0
    calls = 0
    for name, model in PLAN["models"].items():
        manifest = (DATA / "manifests" / f"{name}.json").read_bytes()
        assert hashlib.sha256(manifest).hexdigest() == model["sha256"]
        artifact = json.loads(manifest)
        bytes_planned += sum(
            x["size"] for x in [artifact["config"], *artifact["layers"]]
        )
        folder = DATA / "run" / name
        assert read(folder / "pull-reservation.json") == model
        assert read(folder / "installed.json")["digest"] == model["sha256"]
        alias_record = read(folder / "alias.json")
        alias = model["alias"]
        tag = alias_record["tag"]
        assert tag["name"] == alias and tag["details"]["parent_model"] == model["tag"]
        for mode in PLAN["modes"]:
            reservation = read(folder / f"{mode}-reservation.json")
            assert reservation["alias_sha256"] == tag["digest"]
            assert reservation["request_sha256"] == hashes[alias][mode]
            row = read(folder / f"{mode}.json")
            assert row["alias"] == alias and row["mode"] == mode
            body = b""
            if "response_base64" in row:
                body = base64.b64decode(row["response_base64"], validate=True)
                assert hashlib.sha256(body).hexdigest() == row["response_sha256"]
            if row["http_status"] == 200:
                verify_response(alias, mode, row, body, reservation)
            else:
                assert not row["valid_application_json"]
            assert row["full_gpu_16k"] == any(
                m["digest"] == tag["digest"]
                and m["context_length"] == PLAN["parameters"]["num_ctx"]
                and m["size"] == m["size_vram"] > 0
                for m in row["after"]["models"]
            )
            calls += 1
    assert calls == PLAN["max_preflight_requests"]
    assert len(list((DATA / "run").glob("*/*-reservation.json"))) == calls + len(
        PLAN["models"]
    )
    assert bytes_planned == PLAN["max_manifest_payload_bytes"]
    print(f"Verified {calls} unscored reservations and their results offline.")


if __name__ == "__main__":
    verify()
