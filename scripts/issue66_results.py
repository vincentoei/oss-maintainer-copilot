"""Audit issue #66 reservations and reproduce public reports without inference."""

import base64
import io
import json
import socket
from collections import Counter
from contextlib import redirect_stdout
from unittest.mock import patch

from issue66_prepare import (
    ARMS,
    BASE,
    HERE,
    LIMITS,
    MODEL,
    construct_report,
    digest,
    inputs,
    no_network,
    prepare,
    read,
)

from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import ROOT, fingerprint


def audit():
    if not __debug__:
        raise RuntimeError("Run assertions without Python optimization")
    # Its frozen status text describes preparation, before approval/execution.
    with redirect_stdout(io.StringIO()):
        prepare(check=True)
    frozen = read(HERE / "freeze.json")
    approval = read(HERE / "approval.json")
    assert approval["approved_freeze_sha256"] == digest(HERE / "freeze.json")
    for name, expected in frozen["source_sha256"].items():
        assert digest(ROOT / name) == expected, name
    for name, expected in frozen["archive_sha256"].items():
        assert digest(ROOT / name) == expected, name
    run = HERE / "run"
    assert (
        read(run / "proposal.json")["approved_freeze_sha256"]
        == (approval["approved_freeze_sha256"])
    )
    planned = read(HERE / "requests.json")
    allowed = {(r["arm"], r["id"]): r for r in planned}
    ledger_path = run / "reservations.jsonl"
    ledger = [json.loads(line) for line in ledger_path.read_text().splitlines()]
    assert len(ledger) <= LIMITS["calls"]
    seen = set()
    for i, charge in enumerate(ledger, 1):
        key = charge["alias"], charge["case"]
        assert key not in seen
        seen.add(key)
        assert charge["sequence"] == i
        assert charge["body_sha256"] == allowed[key]["request_sha256"]
        assert key == (planned[i - 1]["arm"], planned[i - 1]["id"])
    cases, evidence, catalog = inputs()
    case_by_id = {c["id"]: c for c in cases}
    arm_by_id = dict(ARMS)
    stored = read(run / "results.json")
    indexed = {(r["arm"], r["id"]): r for r in stored}
    assert len(indexed) == len(stored)
    assert set(indexed) <= seen
    results, usage, model_errors = [], Counter(), []
    with (
        patch("socket.create_connection", no_network),
        patch.object(socket.socket, "connect", no_network),
    ):
        for charge in ledger:
            key = charge["alias"], charge["case"]
            expected = allowed[key]
            row = indexed.get(key)
            if row is None:
                results.append(
                    {
                        **expected,
                        "status": "charged_without_report",
                        "selected_type": None,
                        "exact_match": False,
                        "acceptable_match": False,
                    }
                )
                model_errors.append(list(key))
                continue
            assert row["expected"] == expected["expected"]
            assert row["cohort"] == expected["cohort"]
            assert row == read(run / f"{key[0]}-{key[1]}-report.json")
            assert len(row["calls"]) == 1
            call = row["calls"][0]
            assert call == read(run / f"{key[0]}-{key[1]}-call.json")
            assert row["trace"]["trace_id"] == row["report"]["trace_id"]
            captured = []

            def recorded(request, *, timeout, call=call, captured=captured):
                from hashlib import sha256
                from urllib.error import HTTPError

                assert request.full_url == BASE + "/chat/completions"
                assert timeout == 20
                captured.append(sha256(request.data).hexdigest())
                if call["raw_base64"] is None:
                    raise TimeoutError("Recorded missing response")
                raw = base64.b64decode(call["raw_base64"], validate=True)
                if call["http_status"] != 200:
                    raise HTTPError(
                        request.full_url,
                        call["http_status"],
                        "Recorded",
                        {},
                        io.BytesIO(raw),
                    )
                return io.BytesIO(raw)

            with patch("maintainer_copilot.model.urlopen", recorded):
                rebuilt = construct_report(
                    case_by_id[key[1]],
                    arm_by_id[key[0]](BASE, MODEL, reasoning_effort="none"),
                    evidence,
                    catalog,
                )
            assert captured == [charge["body_sha256"]]
            assert rebuilt.model_dump(mode="json", exclude={"trace_id"}) == {
                k: v for k, v in row["report"].items() if k != "trace_id"
            }
            trace = get_trace(rebuilt.trace_id)
            assert trace is not None
            assert [
                (e.kind, e.name, e.status, e.input_tokens, e.output_tokens)
                for e in trace.events
            ] == [
                (
                    e["kind"],
                    e["name"],
                    e["status"],
                    e["input_tokens"],
                    e["output_tokens"],
                )
                for e in row["trace"]["events"]
            ]
            valid = all(
                e["status"] == "ok"
                for e in row["trace"]["events"]
                if e["kind"] == "model"
            )
            if not valid:
                model_errors.append(list(key))
            if call["raw_base64"] is not None:
                raw = base64.b64decode(call["raw_base64"], validate=True)
                assert len(raw) <= 65536
                envelope = json.loads(raw)
                assert envelope["model"] == MODEL
                measured = envelope["usage"]
                assert type(measured["completion_tokens"]) is int
                assert 0 <= measured["completion_tokens"] <= 256
                assert type(measured["prompt_tokens"]) is int
                assert 0 <= measured["prompt_tokens"] <= 16384 - 256
                usage.update(
                    input_tokens=measured["prompt_tokens"],
                    output_tokens=measured["completion_tokens"],
                )
                choice = envelope["choices"][0]
                assert choice["finish_reason"] == "stop"
                assert not any(
                    choice["message"].get(k)
                    for k in ("thinking", "reasoning", "reasoning_content")
                )
            results.append(
                {
                    **expected,
                    "status": "valid" if valid else "model_error",
                    "report_status": row["report"]["status"],
                    "selected_type": row["report"]["issue_type"],
                    "selected_quote": row["report"]["issue_type_quote"],
                    "report_sha256": fingerprint(row["report"]),
                    "exact_match": valid
                    and row["report"]["issue_type"] == expected["expected"],
                    "acceptable_match": valid
                    and row["report"]["issue_type"] in expected["acceptable_types"],
                    "abstained": valid and row["report"]["issue_type"] is None,
                }
            )
    assert usage["output_tokens"] <= LIMITS["total_output"]
    summary = {}
    for cohort in ("development", "previously_exposed", "exposed_diagnostic"):
        summary[cohort] = {}
        for arm, _ in ARMS:
            subset = [r for r in results if r["arm"] == arm and r["cohort"] == cohort]
            summary[cohort][arm] = {
                "planned": sum(
                    r["arm"] == arm and r["cohort"] == cohort for r in planned
                ),
                "charged": len(subset),
                "valid": sum(r["status"] == "valid" for r in subset),
                "exact_match": sum(r["exact_match"] for r in subset),
                "acceptable_match": sum(r["acceptable_match"] for r in subset),
                "abstentions": [r["id"] for r in subset if r.get("abstained")],
                "failures": [r["id"] for r in subset if r["status"] != "valid"],
            }
    outcome_by_key = {(r["arm"], r["id"]): r for r in results}
    pairs = []
    for case in cases:
        key = case["id"]
        left, right = (outcome_by_key.get((arm, key)) for arm, _ in ARMS)
        field_changes = []
        if ("control", key) in indexed and ("candidate", key) in indexed:
            before = indexed["control", key]["report"]
            after = indexed["candidate", key]["report"]
            field_changes = [
                field
                for field in before
                if field not in ("trace_id", "issue_type", "issue_type_quote")
                and before[field] != after[field]
            ]
        pairs.append(
            {
                "id": key,
                "cohort": case["cohort"],
                "control": left["selected_type"] if left else "undispatched",
                "candidate": right["selected_type"] if right else "undispatched",
                "exact_gain": bool(
                    left and right and right["exact_match"] and not left["exact_match"]
                ),
                "exact_loss": bool(
                    left and right and left["exact_match"] and not right["exact_match"]
                ),
                "common_exact_failure": bool(
                    left
                    and right
                    and not left["exact_match"]
                    and not right["exact_match"]
                ),
                "non_type_field_changes": field_changes,
            }
        )
    result = {
        "verified": True,
        "approved_freeze_sha256": approval["approved_freeze_sha256"],
        "charged": len(ledger),
        "reports_rebuilt": len(stored),
        "execution_complete": (run / "complete.json").exists()
        and not (run / "halt.json").exists(),
        "charged_without_report": len(ledger) - len(stored),
        "model_errors": model_errors,
        "usage": dict(usage),
        "archives_preserved": len(frozen["archive_sha256"]),
        "cohorts": summary,
        "outcomes": results,
        "pairs": pairs,
        "semantic_review": (
            "Separate attributed review required; exact match is not semantic support."
        ),
        "limits": (
            "Small exposed/development cases; fixed paired order, native "
            "cache/residency; no generalization or model-side input "
            "preservation guarantee."
        ),
    }
    ratings_path = HERE / "semantic-ratings.json"
    if ratings_path.exists():
        review = read(ratings_path)
        ratings = review["ratings"]
        rated = {(r["arm"], r["id"]): r for r in ratings}
        assert len(rated) == len(ratings) == len(stored)
        assert set(rated) == set(indexed)
        for key, rating in rated.items():
            report = indexed[key]["report"]
            assert rating["report_sha256"] == fingerprint(report)
            assert rating["selected_type"] == report["issue_type"]
            assert rating["selected_quote"] == report["issue_type_quote"]
            assert rating["reason"]
            if report["issue_type"] is None:
                assert rating["semantic_type_support"] == "N/A"
                assert rating["quote_relevance"] == "N/A"
                assert rating["abstention_appropriate"] in ("yes", "no", "uncertain")
            else:
                assert rating["semantic_type_support"] in ("yes", "no", "uncertain")
                assert rating["quote_relevance"] in ("yes", "no", "uncertain")
                assert rating["abstention_appropriate"] is None

        def supported(rating):
            if rating["selected_type"] is None:
                return rating["abstention_appropriate"] == "yes"
            return (
                rating["semantic_type_support"] == "yes"
                and rating["quote_relevance"] == "yes"
            )

        result["attributed_ai_review"] = {
            "review_kind": review["review_kind"],
            "reviewer": review["reviewer"],
            "human_review_status": review["human_review_status"],
            "reports_rated": len(ratings),
            "counts": {
                arm: {
                    field: dict(Counter(r[field] for r in ratings if r["arm"] == arm))
                    for field in ("semantic_type_support", "quote_relevance")
                }
                for arm, _ in ARMS
            },
            "paired_support_gains": [
                case["id"]
                for case in cases
                if not supported(rated["control", case["id"]])
                and supported(rated["candidate", case["id"]])
            ],
            "paired_support_losses": [
                case["id"]
                for case in cases
                if supported(rated["control", case["id"]])
                and not supported(rated["candidate", case["id"]])
            ],
        }
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
