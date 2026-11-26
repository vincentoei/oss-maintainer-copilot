"""Audit the completed paired ledgers and calculate scores without inference."""

import base64
import hashlib
import json
from collections import Counter, defaultdict
from math import ceil

from issue62_compare import ALIASES, HERE, RUN, check_freeze
from issue62_prepare import DATA

from maintainer_copilot.replay import load_cases
from maintainer_copilot.triage import TriageReport


def read(path):
    return json.loads(path.read_bytes())


def quantiles(values):
    if not values:
        return None
    ranked = sorted(values)
    return {f"p{p}": ranked[ceil(len(ranked) * p / 100) - 1] for p in (50, 95)}


def prediction(row):
    if row["status"] != "valid":
        return row["status"]
    return row["report"]["issue_type"] or "null"


def correct(row):
    return row["status"] == "valid" and row["expected"] == row["report"]["issue_type"]


def arm_metrics(rows):
    confusion = defaultdict(Counter)
    for r in rows:
        confusion[r["expected"] or "null"][prediction(r)] += 1
    events = [r["model_event"] for r in rows if "model_event" in r]
    gpu = [
        r["gpu"]["peak_sampled_used_mib"]
        for r in rows
        if "gpu" in r and r["gpu"]["peak_sampled_used_mib"] is not None
    ]
    return dict(
        correct=sum(map(correct, rows)),
        planned=len(rows),
        statuses=Counter(r["status"] for r in rows),
        type_abstentions=sum(prediction(r) == "null" for r in rows),
        confusion=confusion,
        model_ms=quantiles([e["duration_ms"] for e in events]),
        replay_ms=quantiles([r["replay_ms"] for r in rows if "replay_ms" in r]),
        tokens={
            k: {
                "sum_known": sum(e[k] for e in events if e[k] is not None),
                "missing": sum(e[k] is None for e in events),
            }
            for k in ("input_tokens", "output_tokens")
        },
        peak_device_mib=max(gpu, default=None),
        rows_without_gpu=len(events) - len(gpu),
    )


def summarize():
    if not __debug__:
        raise RuntimeError(
            "Run the artifact assertions with Python optimization disabled"
        )
    freeze = check_freeze(live=False)
    plan = read(HERE / "preparation.json")
    review = read(HERE / "contrast-review.json")
    historical = {
        f"h-{c.issue_number}": c.expected_outcome.issue_type for c in load_cases()
    }
    fresh = review["expected_types"]
    requests = {
        **{f"h-{r['issue_number']}": r for r in plan["historical"]},
        **{r["id"]: r for r in plan["fresh"]},
    }
    reservations = [
        json.loads(line)
        for line in (RUN / "reservations.jsonl").read_text().splitlines()
    ]
    assert len(reservations) <= freeze["total"]
    charged = set()
    for seq, r in enumerate(reservations, start=1):
        key = r["alias"], r["case"]
        assert key not in charged and r["sequence"] == seq
        assert (
            r["body_sha256"] == requests[r["case"]]["wire"]["body_sha256"][r["alias"]]
        )
        charged.add(key)
    arms = []
    flags = read(RUN / "preflight.json")["flags"]
    for alias in ALIASES:
        rows = {}
        path = RUN / alias.split(":")[1]
        assert sum(a == alias for a, _ in charged) <= freeze["per_model"]
        for key, expected in (historical | fresh).items():
            file = path / f"{key}.json"
            if not file.exists():
                status = (
                    "charged_without_result"
                    if (alias, key) in charged
                    else "undispatched"
                )
                rows[key] = {
                    "expected": expected,
                    "case": key,
                    "status": "unavailable" if key in flags else status,
                }
                continue
            row = read(file)
            assert (row["case"], row["expected"], row["alias"]) == (
                key,
                expected,
                alias,
            )
            if key in flags:
                assert row["status"] == "unavailable" and (alias, key) not in charged
            else:
                assert (alias, key) in charged
                report = TriageReport.model_validate(row["report"])
                event = row["model_event"]
                assert row["status"] in {
                    "valid",
                    "validation_error",
                    "transport_error",
                    "identity_error",
                }
                if row["status"] != "identity_error":
                    assert (event["status"] == "ok") == (row["status"] == "valid")
                if row["raw_sha256"] is not None:
                    data = (
                        row["raw_response"].encode()
                        if row["raw_response"] is not None
                        else base64.b64decode(row["raw_base64"], validate=True)
                    )
                    assert (
                        len(data) <= 65536
                        and hashlib.sha256(data).hexdigest() == row["raw_sha256"]
                    )
                if row["status"] == "valid":
                    envelope = json.loads(row["raw_response"])
                    output = json.loads(envelope["choices"][0]["message"]["content"])
                    assert (
                        envelope["model"] == alias
                        and output["issue_type"] == report.issue_type
                    )
                    assert (output["quote_index"] is None) == (
                        report.issue_type_quote is None
                    )
                    usage = envelope.get("usage")
                    for event_key, usage_key in [
                        ("input_tokens", "prompt_tokens"),
                        ("output_tokens", "completion_tokens"),
                    ]:
                        value = (
                            usage.get(usage_key) if isinstance(usage, dict) else None
                        )
                        assert event[event_key] == (
                            value if type(value) is int and value >= 0 else None
                        )
            rows[key] = row
        arms.append(rows)
    summary = {
        "dispatches": len(charged),
        "max_dispatches": freeze["total"],
        "model_api_usd": 0,
    }
    for name, keys in (("historical", historical), ("reviewed_synthetic", fresh)):
        pairs = [
            (a, b)
            for a, b in ((arms[0][k], arms[1][k]) for k in keys)
            if a["status"] == b["status"] == "valid"
        ]
        summary[name] = {
            "planned": len(keys),
            "eligible": sum(k not in flags for k in keys),
            "common_valid": len(pairs),
            "gains": [b["case"] for a, b in pairs if correct(b) and not correct(a)],
            "regressions": [
                b["case"] for a, b in pairs if correct(a) and not correct(b)
            ],
            "nonvalid_transitions": {
                k: [arms[0][k]["status"], arms[1][k]["status"]]
                for k in keys
                if any(arm[k]["status"] != "valid" for arm in arms)
            },
            "arms": {
                alias: arm_metrics([arm[k] for k in keys])
                for alias, arm in zip(ALIASES, arms, strict=True)
            },
        }
    reference = read(DATA / "issue-60/followup/results.json")
    summary["control_drift"] = [
        r["issue_number"]
        for r in reference["cases"]
        if prediction(arms[0][f"h-{r['issue_number']}"])
        != (r["report"]["issue_type"] or "null")
    ]
    summary["complete_fresh_pairs"] = {
        alias: {
            pair: all(correct(arm[f"{pair}-{side}"]) for side in ("A", "B"))
            for pair in ("xml", "filter", "paths")
        }
        for alias, arm in zip(ALIASES, arms, strict=True)
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(summarize(), indent=2))
