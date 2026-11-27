"""Audit planned slots, raw evidence and fresh report playback without inference."""

import base64
import copy
import io
import json
import os
import random
import tempfile
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from downloaded_scored_prepare import CACHE, restore
from fastapi.testclient import TestClient
from issue20_verify import verify_recorded_source
from issue62_results import quantiles
from issue63_run import HERE, LIMITS, RUN, digest, plan, read

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import load_cases, replay_case
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.web import app
from maintainer_copilot.workflow_comparison import ROOT, fingerprint


def reconcile(planned, stored, ledger, allowed):
    """Never refund a durable charge because its report/call write was interrupted."""
    assert len(stored) == len(planned)
    reserved = {}
    for i, entry in enumerate(ledger, 1):
        key = entry["alias"], entry["case"]
        assert entry["sequence"] == i and key not in reserved
        assert entry["body_sha256"] == allowed[key]
        reserved[key] = (i, entry)
    result = []
    for original, expected in zip(stored, planned, strict=True):
        row = copy.deepcopy(original)
        assert all(row[k] == value for k, value in expected.items())
        saved = {c["slot"]: c for c in row["calls"]}
        assert len(saved) == len(row["calls"])
        calls, missing = [], False
        for slot in row["slots"]:
            key = row["alias"], slot
            if key not in reserved:
                assert slot not in saved
                continue
            i, charge = reserved[key]
            path = RUN / "calls" / f"{i:02}.json"
            try:
                recorded = read(path)
            except (OSError, ValueError):
                recorded = saved.get(slot) or {
                    "slot": slot,
                    "alias": row["alias"],
                    "http_status": None,
                    "transport_error": "ResponseNotRecorded",
                    "raw_base64": None,
                    "request_sha256": charge["body_sha256"],
                    "latency_ms": None,
                }
                missing = True
            if slot in saved and not missing:
                assert all(saved[slot][k] == v for k, v in recorded.items())
                calls.append(saved[slot])
            else:
                missing = True
                calls.append(recorded)
        if calls and (missing or row["report"] is None):
            row["unverified_report"] = row["report"]
            row.update(status="charged_without_result", report=None, trace=None)
        row["calls"] = calls
        result.append(row)
    return result


def replay_report(row, frozen):
    """Rebuild complete reports; historical text remains local-only under ADR-0003."""
    if row["cohort"] == "exposed_bug_loss" and not CACHE.exists():
        return False
    remaining = list(row["calls"])

    def response(request, *, timeout):
        assert remaining and timeout == 20
        call = remaining.pop(0)
        assert sha256(request.data).hexdigest() == call["request_sha256"]
        if call["raw_base64"] is None:
            raise TimeoutError("Recorded missing response")
        response = io.BytesIO(base64.b64decode(call["raw_base64"]))
        if call["http_status"] != 200:
            raise HTTPError(
                request.full_url, call["http_status"], "Recorded", {}, response
            )
        return response

    with tempfile.TemporaryDirectory(prefix="issue63-audit-") as directory:
        with (
            patch.dict(
                os.environ,
                {
                    "MODEL_NAME": row["alias"],
                    "MODEL_REASONING_EFFORT": "none",
                    "MODEL_BASE_URL": read(HERE / "serving-inspection.json")["base_url"]
                    + "/v1",
                    "MODEL_DRAFTING": "0",
                    "REPOSITORY_REGISTRY_PATH": str(
                        Path(directory) / "registry.sqlite3"
                    ),
                },
            ),
            patch("maintainer_copilot.model.urlopen", response),
        ):
            if row["cohort"] == "exposed_bug_loss":
                assert digest(CACHE) == frozen["snapshot_sha256"]
                catalog = load_cases()
                case = next(c for c in catalog if f"h-{c.issue_number}" == row["id"])
                evidence = restore()
                report = replay_case(
                    case,
                    candidate_catalog=catalog,
                    keyword_filter=True,
                    model_client=OpenAICompatibleModel.from_environment(),
                    commit_source=evidence,
                    issue_source=evidence,
                    source_reader=evidence,
                )
            elif row["cohort"] == "fresh_synthetic":
                opening = next(
                    c
                    for c in read(HERE / "proposed-cases.json")["cases"]
                    if c["id"] == row["id"]
                )
                report = triage_issue(
                    IssueUnderReview(title=opening["title"], body=opening["body"]),
                    model_client=OpenAICompatibleModel.from_environment(),
                    documentation_topics=(),
                )
            else:
                opening = next(
                    c
                    for c in read(HERE / "integration-inputs.json")
                    if c["id"] == row["input_id"]
                )
                payload = {key: opening[key] for key in ("title", "body")}
                if row["kind"] == "python":
                    report = triage_issue(
                        IssueUnderReview(**payload),
                        model_client=OpenAICompatibleModel.from_environment(),
                    )
                else:
                    route = (
                        "/api/agent/triage" if row["kind"] == "agent" else "/api/triage"
                    )
                    with TestClient(app) as client:
                        received = client.post(route, json=payload)
                        assert received.status_code == 200
                        report = TriageReport.model_validate(received.json())
    assert not remaining
    rebuilt = report.model_dump(mode="json")
    assert {k: v for k, v in rebuilt["context"].items() if k != "prepared_at"} == {
        k: v for k, v in row["report"]["context"].items() if k != "prepared_at"
    }
    assert {k: v for k, v in rebuilt.items() if k not in ("trace_id", "context")} == {
        k: v for k, v in row["report"].items() if k not in ("trace_id", "context")
    }
    return True


def summarize():
    if not __debug__:
        raise RuntimeError("Run the audit without Python optimization")
    frozen = read(HERE / "freeze.json")
    assert frozen["limits"] == LIMITS
    verify_recorded_source(ROOT, frozen["source_sha256"], frozen["source_commit"])
    assert all(
        digest(HERE / name) == hashed for name, hashed in frozen["sha256"].items()
    )
    allowed, planned = plan()
    assert len(allowed) == LIMITS["calls"] == 55
    path = RUN / "reservations.jsonl"
    ledger = (
        [json.loads(line) for line in path.read_text().splitlines()]
        if path.exists()
        else []
    )
    assert len(ledger) <= LIMITS["calls"]
    assert len({(r["alias"], r["case"]) for r in ledger}) == len(ledger)
    try:
        stored = read(RUN / "results.json")
    except (OSError, ValueError):
        stored = [
            dict(row, status="undispatched", report=None, calls=[]) for row in planned
        ]
    rows = reconcile(planned, stored, ledger, allowed)
    assert len(rows) == len(planned) == 53
    seen = []
    usage = Counter()
    reported_output_bound_violations = 0
    groups = defaultdict(list)
    base_fields = {
        "slot",
        "alias",
        "http_status",
        "transport_error",
        "raw_base64",
        "request_sha256",
        "latency_ms",
    }
    replayed = 0
    unreplayed = []
    inspection = read(HERE / "serving-inspection.json")
    for row, expected in zip(rows, planned, strict=True):
        assert all(row[k] == value for k, value in expected.items())
        assert [c["slot"] for c in row["calls"]] == row["slots"][: len(row["calls"])]
        assert len(row["calls"]) <= len(row["slots"])
        for call in row["calls"]:
            index = len(seen) + 1
            try:
                recorded = read(RUN / "calls" / f"{index:02}.json")
            except (OSError, ValueError):
                assert row["status"] == "charged_without_result"
                recorded = {k: call[k] for k in base_fields}
            assert base_fields <= set(recorded)
            assert all(call[k] == value for k, value in recorded.items())
            reserved = ledger[index - 1]
            assert reserved["sequence"] == index
            assert reserved["alias"] == row["alias"] == call["alias"]
            assert reserved["case"] == call["slot"]
            assert (
                reserved["body_sha256"]
                == call["request_sha256"]
                == allowed[row["alias"], call["slot"]]
            )
            seen.append((row["alias"], call["slot"]))
            raw = (
                base64.b64decode(call["raw_base64"], validate=True)
                if call["raw_base64"]
                else None
            )
            assert raw is None or len(raw) <= 65537
            try:
                measured = json.loads(raw).get("usage") or {}
            except (TypeError, ValueError, AttributeError):
                measured = {}
            if not isinstance(measured, dict):
                measured = {}
            for source, target in (
                ("prompt_tokens", "input_tokens"),
                ("completion_tokens", "output_tokens"),
            ):
                value = measured.get(source)
                if type(value) is int and value >= 0:
                    usage[target] += value
                    if target == "output_tokens" and value > 256:
                        reported_output_bound_violations += 1
                else:
                    usage["unknown_" + target + "_calls"] += 1
            if row["status"] == "valid":
                assert call["http_status"] == 200 and call["transport_error"] is None
                envelope = json.loads(raw)
                choice = envelope["choices"][0]
                assert (
                    envelope["model"] == row["alias"]
                    and choice["finish_reason"] == "stop"
                )
                assert not any(
                    choice["message"].get(k)
                    for k in ("thinking", "reasoning", "reasoning_content")
                )
                measured = envelope["usage"]
                assert call["usage"] == measured and call["truncation"] == "unknown"
                assert (
                    type(measured["prompt_tokens"]) is int
                    and measured["prompt_tokens"] >= 0
                )
                assert type(measured["completion_tokens"]) is int
                assert 0 <= measured["completion_tokens"] <= 256
                assert measured["prompt_tokens"] + 256 <= 16384
        if row["report"] is not None:
            TriageReport.model_validate(row["report"])
            assert row["trace"]["trace_id"] == row["report"]["trace_id"]
        if "reported_gpu_16k" in row:
            computed_gpu = any(
                m["digest"] == inspection["arms"][row["alias"]]["digest"]
                and m["context_length"] == 16384
                and m["size"] == m["size_vram"] > 0
                for m in row["resident_after"]["models"]
            )
            assert row["reported_gpu_16k"] is computed_gpu
        if row["status"] == "valid":
            assert row["report"] and len(row["calls"]) == len(row["slots"])
            assert row["reported_gpu_16k"] is True
            assert computed_gpu is True
            assert all(
                e["status"] == "ok"
                for e in row["trace"]["events"]
                if e["kind"] == "model"
            )
            final = json.loads(base64.b64decode(row["calls"][-1]["raw_base64"]))
            selection = json.loads(final["choices"][0]["message"]["content"])
            assert selection["issue_type"] == row["report"]["issue_type"]
            assert (selection["quote_index"] is None) == (
                row["report"]["issue_type_quote"] is None
            )
            if selection["issue_type"] is not None:
                assert (
                    selection["issue_type"]
                    in TriageReport.model_validate(row["report"]).context.type_labels
                )
        if row["report"] is not None and row["calls"]:
            if replay_report(row, frozen):
                replayed += 1
            else:
                unreplayed.append((row["alias"], row["id"]))
        groups[row["cohort"], row["alias"]].append(row)
    assert len(seen) == len(ledger)
    if (RUN / "complete.json").exists():
        assert read(RUN / "complete.json")["charged"] == len(ledger)
    incomplete = any(
        r["status"]
        in ("undispatched", "interrupted", "unavailable", "charged_without_result")
        for r in rows
    )
    administrative = (
        read(RUN / "administrative.json")
        if (RUN / "administrative.json").exists()
        else []
    )
    assert len(administrative) <= 3
    aliases = list(read(HERE / "serving-inspection.json")["arms"])
    for item in administrative:
        assert item["request"] == {
            "model": item["request"]["model"],
            "keep_alive": 0,
            "stream": False,
        }
        assert item["request"]["model"] in aliases
        assert item["response"]["done_reason"] == "unload"
    summary = {}
    for (cohort, alias), observations in groups.items():
        confusion = defaultdict(Counter)
        for row in observations:
            prediction = (
                row["report"]["issue_type"]
                if row["status"] == "valid"
                else row["status"]
            )
            confusion[row["expected"] or "null"][prediction or "null"] += 1
        cached = []
        peak = []
        for row in observations:
            memory = (row.get("gpu") or {}).get("peak_sampled_used_mib")
            if memory is not None:
                peak.append(memory)
            for call in row["calls"]:
                try:
                    measured = json.loads(base64.b64decode(call["raw_base64"]))["usage"]
                    details = measured.get("prompt_tokens_details") or {}
                    count = details.get("cached_tokens")
                    cached.append(count if type(count) is int and count >= 0 else None)
                except (TypeError, ValueError, KeyError, AttributeError):
                    cached.append(None)
        summary.setdefault(cohort, {})[alias] = {
            "planned": len(observations),
            "correct": sum(
                r["status"] == "valid" and r["expected"] == r["report"]["issue_type"]
                for r in observations
            ),
            "statuses": Counter(r["status"] for r in observations),
            "valid_abstentions": sum(
                r["status"] == "valid" and r["report"]["issue_type"] is None
                for r in observations
            ),
            "confusion": confusion,
            "model_latency_ms": quantiles(
                [
                    c["latency_ms"]
                    for r in observations
                    for c in r["calls"]
                    if c["latency_ms"] is not None
                ]
            ),
            "model_latency_by_stage_ms": {
                stage: quantiles(
                    [
                        c["latency_ms"]
                        for r in observations
                        for c in r["calls"]
                        if c["latency_ms"] is not None
                        and (
                            "planner"
                            if c["slot"].startswith("i-agent-")
                            and c["slot"].endswith("-1")
                            else "report"
                        )
                        == stage
                    ]
                )
                for stage in ("planner", "report")
            },
            "end_to_end_latency_ms": quantiles(
                [r["replay_ms"] for r in observations if "replay_ms" in r]
            ),
            "peak_sampled_device_mib": max(peak, default=None),
            "reported_cache_hit_calls": sum(
                value is not None and value > 0 for value in cached
            ),
            "cache_unknown_calls": sum(value is None for value in cached),
            "model_cold_observations": [
                r["id"]
                for r in observations
                if r.get("resident_before") == {"models": []}
            ],
            "gpu_measurement_errors": [
                r["id"] for r in observations if (r.get("gpu") or {}).get("error")
            ],
        }
    comparisons = {}
    candidate = aliases[-1]
    unchanged = (
        "missing_details",
        "duplicate_candidates",
        "related_issues",
        "documentation_claims",
        "source_claims",
        "ci_results",
    )
    for cohort in ("fresh_synthetic", "exposed_bug_loss"):
        indexed = {
            alias: {r["id"]: r for r in groups[cohort, alias]} for alias in aliases
        }
        comparisons[cohort] = {}
        for control in aliases[:-1]:
            gains, losses, common = [], [], []
            for key, left in indexed[control].items():
                right = indexed[candidate][key]
                if left["report"] and right["report"]:
                    for field in unchanged:
                        assert left["report"][field] == right["report"][field]
                if left["status"] == right["status"] == "valid":
                    common.append(key)
                    old = left["report"]["issue_type"] == left["expected"]
                    new = right["report"]["issue_type"] == right["expected"]
                    if new and not old:
                        gains.append(key)
                    if old and not new:
                        losses.append(key)
            comparisons[cohort][control] = {
                "common_valid": common,
                "gains": gains,
                "losses": losses,
            }
    return {
        "verified": True,
        "charged": len(ledger),
        "usage_known_all_calls": usage,
        "reported_output_within_budget": (
            usage["output_tokens"] <= LIMITS["total_output"]
            and not usage["unknown_output_tokens_calls"]
            and not reported_output_bound_violations
        ),
        "reports_replayed": replayed,
        "historical_reports_not_replayed_without_private_snapshot": unreplayed,
        "execution_status": (
            "interrupted_or_incomplete"
            if incomplete
            or (RUN / "halt.json").exists()
            or not (RUN / "complete.json").exists()
            else "complete"
        ),
        "charged_without_result": sum(
            r["status"] == "charged_without_result" for r in rows
        ),
        "cohorts": summary,
        "candidate_paired_comparisons": comparisons,
        "unrelated_fixed_report_fields_unchanged": True,
        "decision": "pending_actual_human_report_review",
        "limits": (
            "Small designed set; historical diagnostics exposed; "
            "truncation/physical residency not independently proven."
        ),
    }


def review():
    rows = [r for r in read(RUN / "results.json") if r["report"] is not None]
    random.Random(63).shuffle(rows)
    directory = HERE / "review"
    directory.mkdir()
    key, ratings, markdown = (
        [],
        [],
        [
            "# Method-hidden report review\n",
            "Rate semantic type support, quote relevance, unsupported claims and "
            "reply usefulness (0/1/2). Preserve reasons. Do not consult the identity "
            "key or copy prior ratings.\n",
        ],
    )
    fresh = {c["id"]: c for c in read(HERE / "proposed-cases.json")["cases"]}
    for i, row in enumerate(rows, 1):
        code = f"R{i:02}"
        hashed = fingerprint(row["report"])
        key.append(
            {
                "code": code,
                "case": row["id"],
                "alias": row["alias"],
                "report_sha256": hashed,
            }
        )
        ratings.append(
            {
                "code": code,
                "report_sha256": hashed,
                "status": "pending",
                "reviewer": None,
                "semantic_type_support": None,
                "quote_relevance": None,
                "unsupported_claims": None,
                "reply_usefulness": None,
                "reason": None,
            }
        )
        report = row["report"]
        markdown.append(f"\n## {code}\n\nReport fingerprint: `{hashed}`\n")
        if row["id"] in fresh:
            opening = fresh[row["id"]]
            markdown.append(opening["title"] + "\n\n" + opening["body"] + "\n")
        elif row["cohort"] == "integration":
            markdown.append(
                "Synthetic application input: "
                + row["input_id"]
                + ". Inspect the exact title/body in [integration inputs]"
                "(../integration-inputs.json). The long form adds observation "
                "lines to the same exit-status opening, not a new quality case.\n"
            )
        else:
            number = row["id"].removeprefix("h-")
            markdown.append(
                f"Historical pytest #{number}: inspect its opening at the "
                "recorded cutoff; no later labels or comments.\n"
            )
        markdown.append(
            "\nSuggested type: "
            + str(report["issue_type"])
            + "\n\nQuote: "
            + str(report["issue_type_quote"])
            + "\n\n"
            + report["draft_reply"]
            + "\n"
        )
        for citation in report["citations"]:
            markdown.append(
                f"- [{citation['id']}]({citation['source_url']}): "
                f"{citation['description']}\n"
            )
        markdown.append("\nRatings / reviewer / reasons: pending\n")
    for name, value in (("key.json", key), ("ratings.json", ratings)):
        (directory / name).write_text(json.dumps(value, indent=2) + "\n")
    (directory / "reports.md").write_text("\n".join(markdown))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--make-review", action="store_true")
    args = parser.parse_args()
    print(json.dumps(summarize(), indent=2))
    if args.make_review:
        review()
