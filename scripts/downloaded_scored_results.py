"""Reconcile the frozen ledger and replay saved responses without a model server."""

import base64
import io
import json
from collections import Counter
from hashlib import sha256
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from downloaded_model_pull import DATA
from downloaded_scored_prepare import (
    ALIASES,
    CACHE,
    HERE,
    OLD,
    REFERENCE,
    prepare,
    read,
    restore,
    with_effort,
)
from downloaded_scored_run import LIMITS, RUN, annotate
from issue62_compare import run_case
from issue62_prepare import PROBES
from issue62_results import arm_metrics, correct, prediction, quantiles

from maintainer_copilot.local_evaluation import _GpuMemory
from maintainer_copilot.replay import load_cases


class RecordedResponse(io.BytesIO):
    status = 200


class Replay:
    def __init__(self, row, reserved):
        self.row = row
        self.reserved = reserved
        self.sent = False

    def reserve(self, alias, key, body):
        assert (alias, key, sha256(with_effort(body)).hexdigest()) == (
            self.reserved["alias"],
            self.reserved["case"],
            self.reserved["body_sha256"],
        )

    def open(self, request, *, timeout):
        assert not self.sent and timeout == LIMITS["timeout_seconds"]
        self.sent = True
        r = self.row
        data = (
            r["raw_response"].encode()
            if r["raw_response"] is not None
            else (
                base64.b64decode(r["raw_base64"], validate=True)
                if "raw_base64" in r
                else None
            )
        )
        assert r["raw_sha256"] == (
            sha256(data).hexdigest() if data is not None else None
        )
        if r["http_status"] is None:
            assert data is None and r["transport_error"]
            if r["transport_error"] == "TimeoutError":
                raise TimeoutError()
            raise URLError(OSError(r["transport_error"]))
        assert data is not None and len(data) <= 65536
        response = RecordedResponse(data + (b" " if r["truncated"] else b""))
        if r["http_status"] != 200:
            raise HTTPError(
                request.full_url, r["http_status"], "Recorded", {}, response
            )
        return response


def audit_row(
    row,
    reservation,
    digest,
    cases,
    probes,
    catalog,
    snapshot,
    *,
    missing_telemetry=False,
):
    event = row["model_event"]
    assert row["trace"]["trace_id"] == row["report"]["trace_id"]
    assert [e for e in row["trace"]["events"] if e["name"] == "triage_selection"] == [
        event
    ]
    raw = (
        row["raw_response"].encode()
        if row["raw_response"] is not None
        else (
            base64.b64decode(row["raw_base64"], validate=True)
            if "raw_base64" in row
            else None
        )
    )
    assert row["raw_sha256"] == (sha256(raw).hexdigest() if raw is not None else None)
    if row["http_status"] is None:
        assert row["transport_error"] and event["status"] == "error" and raw is None
    if row["status"] == "valid" and not missing_telemetry:
        assert row["http_status"] == 200 and event["status"] == "ok" and raw
        envelope = json.loads(raw)
        choice = envelope["choices"][0]
        assert envelope["model"] == row["alias"] and choice["finish_reason"] == "stop"
        assert (
            json.loads(choice["message"]["content"])["issue_type"]
            == row["report"]["issue_type"]
        )
    # Recompute provider-derived fields even in a metadata-only checkout.
    observed = dict(row)
    observed["status"] = "valid" if event["status"] == "ok" else "validation_error"
    if row["transport_error"] or raw is None:
        observed["status"] = "transport_error"
    if raw:
        try:
            envelope = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            envelope = None
        if isinstance(envelope, dict) and (
            "model" in envelope or observed["status"] == "valid"
        ):
            if envelope.get("model") != row["alias"]:
                observed["status"] = "identity_error"
    residency = row.get("resident_after", {"models": []})
    if not missing_telemetry:
        assert "resident_after" in row
    annotate(observed, digest, residency)
    for key in ("finish_reason", "usage", "context_flag", "reasoning_chars", "gpu_16k"):
        if missing_telemetry:
            row[key] = None if key == "gpu_16k" else observed[key]
        else:
            assert row[key] == observed[key], (row["case"], key)
    assert observed["status"] == row["status"] or missing_telemetry
    if event["status"] == "ok":
        assert row["status"] in ("valid", "validation_error", "identity_error")
        for name, field in (
            ("input_tokens", "prompt_tokens"),
            ("output_tokens", "completion_tokens"),
        ):
            count = (observed["usage"] or {}).get(field)
            assert event[name] == (count if type(count) is int and count >= 0 else None)
    elif row["http_status"] is None:
        assert row["status"] == "transport_error"
    if snapshot is None and row["case"] in cases:
        # Historical text is local-only under ADR-0003. Metadata-only clones
        # can reconcile the reservations, response, trace and scored report.
        return
    replay = Replay(row, reservation)
    checked = {k: row[k] for k in ("case", "alias", "expected")}
    with patch("issue62_compare._GpuMemory", lambda enabled: _GpuMemory(False)):
        run_case(checked, replay, replay, cases, probes, catalog, snapshot)
    assert replay.sent
    annotate(checked, digest, residency)
    for key in (
        "status",
        "http_status",
        "finish_reason",
        "usage",
        "reasoning_chars",
        "context_flag",
        "gpu_16k",
        "raw_sha256",
    ):
        assert checked[key] == observed[key], (row["case"], key)
    assert {k: v for k, v in checked["report"].items() if k != "trace_id"} == {
        k: v for k, v in row["report"].items() if k != "trace_id"
    }
    for key in ("status", "error", "input_tokens", "output_tokens"):
        assert checked["model_event"][key] == row["model_event"][key]


def resources(rows):
    result = arm_metrics(rows)
    valid = result["statuses"]["valid"]
    result["valid_disagreements"] = valid - result["correct"]
    measured = [r for r in rows if "model_event" in r]
    usage = [r.get("usage") or {} for r in measured]
    cached = [
        (u.get("prompt_tokens_details") or {}).get("cached_tokens") for u in usage
    ]
    result.update(
        cached_prompt_tokens=sum(n for n in cached if n is not None),
        rows_with_reported_cache=sum(n is not None for n in cached),
        rows_with_cache_hit=sum(n is not None and n > 0 for n in cached),
        cached_hit_model_ms=quantiles(
            [
                r["model_event"]["duration_ms"]
                for r, n in zip(measured, cached, strict=True)
                if n
            ]
        ),
        finish_reasons=Counter(r.get("finish_reason") or "unknown" for r in measured),
        context_flags=Counter(r["context_flag"] for r in measured),
        max_prompt_tokens=max(
            (u["prompt_tokens"] for u in usage if u.get("prompt_tokens") is not None),
            default=None,
        ),
        exposed_reasoning_chars=sum(r["reasoning_chars"] or 0 for r in measured),
        unknown_reasoning=sum(r["reasoning_chars"] is None for r in measured),
        full_gpu_16k_rows=sum(r["gpu_16k"] is True for r in measured),
    )
    return result


def summarize():
    if not __debug__:
        raise RuntimeError("Run the audit without Python optimization")
    frozen = read(HERE / "freeze.json")
    plan = read(HERE / "requests.json")
    assert frozen["limits"] == LIMITS
    if CACHE.exists():
        assert sha256(CACHE.read_bytes()).hexdigest() == frozen["snapshot_sha256"]
        assert plan == prepare()
    assert (
        frozen["model_order"] == list(ALIASES) and frozen["reasoning_effort"] == "none"
    )
    for key, path in (
        ("request_set_sha256", HERE / "requests.json"),
        ("scored_protocol_sha256", HERE / "protocol.md"),
        ("protocol_sha256", DATA / "comparison.md"),
    ):
        assert sha256(path.read_bytes()).hexdigest() == frozen[key]
    ledger = [
        json.loads(line)
        for line in (RUN / "reservations.jsonl").read_text().splitlines()
    ]
    order = [(a, k) for a in ALIASES for k, p in plan.items() if not p["error"]]
    charged = {}
    for index, record in enumerate(ledger):
        alias, key = order[index]
        assert (
            record["alias"],
            record["case"],
            record["sequence"],
            record["body_sha256"],
        ) == (alias, key, index + 1, plan[key]["sha256"][alias])
        charged[alias, key] = record
    assert len(charged) == len(ledger) <= LIMITS["total"]
    snapshot = restore() if CACHE.exists() else None
    catalog = load_cases()
    cases = {f"h-{c.issue_number}": c for c in catalog}
    probes = {c["id"]: c for c in read(PROBES)["cases"]}
    halt_record = read(RUN / "halt.json") if (RUN / "halt.json").exists() else {}
    arms = {}
    first_calls = {}
    for alias in ALIASES:
        arms[alias] = rows = {}
        records = [r for r in ledger if r["alias"] == alias]
        assert len(records) <= LIMITS["per_arm"]
        for key, p in plan.items():
            path = RUN / alias.split(":")[1] / f"{key}.json"
            reservation = charged.get((alias, key))
            if not path.exists():
                status = "charged_without_result" if reservation else "undispatched"
                rows[key] = dict(
                    case=key,
                    expected=p["expected"],
                    status="unavailable" if p["error"] else status,
                )
                continue
            row = read(path)
            assert (row["alias"], row["case"], row["expected"]) == (
                alias,
                key,
                p["expected"],
            )
            if p["error"]:
                assert reservation is None and row["status"] == "unavailable"
            else:
                assert reservation
                missing_telemetry = "resident_after" not in row
                if missing_telemetry:
                    assert (halt_record.get("alias"), halt_record.get("case")) == (
                        alias,
                        key,
                    )
                    assert halt_record["reason"].startswith("Telemetry failed:")
                audit_row(
                    row,
                    reservation,
                    frozen["serving"]["arms"][alias]["digest"],
                    cases,
                    probes,
                    catalog,
                    snapshot,
                    missing_telemetry=missing_telemetry,
                )
                if missing_telemetry:
                    row["status"] = "telemetry_incomplete"
            rows[key] = row
        if records:
            first = rows[records[0]["case"]]
            first_calls[alias] = {
                "case": first["case"],
                "status": first["status"],
                "model_ms": first.get("model_event", {}).get("duration_ms"),
                "before": [
                    m["name"]
                    for m in first.get("resident_before", {}).get("models", [])
                ],
                "cached_tokens": (
                    (first.get("usage") or {}).get("prompt_tokens_details") or {}
                ).get("cached_tokens"),
            }
    complete = RUN / "complete.json"
    halt = RUN / "halt.json"
    if complete.exists():
        assert not halt.exists() and read(complete)["charged"] == len(ledger) == len(
            order
        )
        assert all(
            r["status"] not in ("charged_without_result", "undispatched")
            for arm in arms.values()
            for r in arm.values()
        )
    if ledger:
        first = arms[REFERENCE][ledger[0]["case"]]
        if first["status"] != "valid" or not first.get("gpu_16k"):
            assert len(ledger) == 1 and not complete.exists()
    if halt.exists() and read(halt).get("charged", True):
        assert (read(halt)["alias"], read(halt)["case"]) == order[len(ledger) - 1]
    result = {
        "dispatches": len(ledger),
        "allocated_output_tokens": len(ledger) * 256,
        "model_api_usd": 0,
        "halt": read(halt) if halt.exists() else None,
        "complete": complete.exists(),
        "first_calls": first_calls,
    }
    for cohort in ("historical", "fresh"):
        keys = [k for k, p in plan.items() if p["cohort"] == cohort]
        metrics = {a: resources([arms[a][k] for k in keys]) for a in ALIASES}
        reference = arms[REFERENCE]
        comparisons = {}
        for alias in ALIASES[1:]:
            candidate = arms[alias]
            common = [
                k
                for k in keys
                if reference[k]["status"] == candidate[k]["status"] == "valid"
            ]
            comparisons[alias] = {
                "common_valid": len(common),
                "gains": [
                    k
                    for k in common
                    if correct(candidate[k]) and not correct(reference[k])
                ],
                "regressions": [
                    k
                    for k in common
                    if correct(reference[k]) and not correct(candidate[k])
                ],
                "nonvalid_transitions": {
                    k: [prediction(reference[k]), prediction(candidate[k])]
                    for k in keys
                    if k not in common
                },
            }
        result[cohort] = {
            "planned": len(keys),
            "eligible": sum(not plan[k]["error"] for k in keys),
            "arms": metrics,
            "paired": comparisons,
            "cases": [
                {
                    "case": k,
                    "expected": plan[k]["expected"],
                    "predictions": {a: prediction(arms[a][k]) for a in ALIASES},
                    "eligibility_flag": plan[k]["error"],
                }
                for k in keys
            ],
        }
        result[cohort]["reference_drift_from_62"] = [
            k
            for k in keys
            if prediction(reference[k])
            != prediction(read(OLD / "run/coder7b-ctx16k" / f"{k}.json"))
            and reference[k]["status"] == "valid"
        ]
    result["complete_contrast_pairs"] = {
        a: {
            pair: all(correct(arms[a][f"{pair}-{s}"]) for s in ("A", "B"))
            for pair in ("xml", "filter", "paths")
        }
        for a in ALIASES
    }
    return result


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
