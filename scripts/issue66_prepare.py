"""Inference-free issue #66 diagnosis and exact request freeze. Never dispatches."""

import argparse
import base64
import io
import json
import socket
from hashlib import sha256
from unittest.mock import patch

from downloaded_scored_prepare import CACHE, restore
from issue66_candidate import SUPPORT_INSTRUCTION, SemanticSupportCandidate

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import load_cases, replay_case
from maintainer_copilot.workflow_comparison import ROOT, fingerprint

HERE = ROOT / "docs/evaluation/issue-66"
OLD = ROOT / "docs/evaluation/issue-63"
LOCAL = ROOT / ".local/issue66/prepared"
MODEL = "pytest-triage:qwen35-4b-ctx16k"
BASE = "http://172.17.48.1:11434/v1"
BASELINE = "2194e338e2a82a9f54ab1ef06903944508523fa3"
LIMITS = {"calls": 48, "per_arm": 24, "output_per_call": 256, "total_output": 12288}


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def no_network(*args, **kwargs):
    raise RuntimeError("Issue #66 preparation forbids network access")


def inputs():
    assert digest(CACHE) == read(OLD / "freeze.json")["snapshot_sha256"]
    evidence = restore()
    catalog = load_cases()
    historical = {f"h-{c.issue_number}": c for c in catalog}
    examples = read(HERE / "cases.json")["cases"]
    prior = read(OLD / "proposed-cases.json")["cases"]
    cases = (
        [dict(c, cohort="development") for c in examples]
        + [
            dict(c, cohort="previously_exposed", expected=c["proposed_type"])
            for c in prior
        ]
        + [
            {
                "id": key,
                "cohort": "exposed_diagnostic",
                "expected": historical[key].expected_outcome.issue_type,
            }
            for key in ("h-12219", "h-12223", "h-12249")
        ]
    )
    assert len(cases) == LIMITS["per_arm"]
    assert len({c["id"] for c in cases}) == len(cases)
    return cases, evidence, catalog


def construct_report(case, client, evidence, catalog):
    if case["cohort"] == "exposed_diagnostic":
        return replay_case(
            next(c for c in catalog if f"h-{c.issue_number}" == case["id"]),
            candidate_catalog=catalog,
            keyword_filter=True,
            model_client=client,
            commit_source=evidence,
            issue_source=evidence,
            source_reader=evidence,
        )
    return triage_issue(
        IssueUnderReview(title=case["title"], body=case["body"]),
        model_client=client,
        documentation_topics=(),
    )


def build():
    if not __debug__:
        raise RuntimeError("Run assertions without Python optimization")
    cases, evidence, catalog = inputs()
    payloads, rows, diagnoses = {}, [], []

    # Deny real sockets even if a future public report dependency changes.
    with (
        patch("socket.create_connection", no_network),
        patch.object(socket.socket, "connect", no_network),
    ):
        for case in cases:
            pair = []
            for arm, cls in (
                ("control", OpenAICompatibleModel),
                ("candidate", SemanticSupportCandidate),
            ):
                captured = []

                def endpoint(request, *, timeout, captured=captured):
                    assert timeout == 20
                    assert request.full_url == BASE + "/chat/completions"
                    captured.append(request.data)
                    return io.BytesIO(
                        b'{"choices":[{"message":{"content":'
                        b'"{\\"issue_type\\":null,\\"quote_index\\":null,'
                        b'\\"reply_citation_ids\\":[]}"}}]}'
                    )

                with patch("maintainer_copilot.model.urlopen", endpoint):
                    report = construct_report(
                        case,
                        cls(BASE, MODEL, reasoning_effort="none"),
                        evidence,
                        catalog,
                    )
                assert len(captured) == 1
                assert report.issue_type is None
                assert any(a.field == "issue_type" for a in report.abstentions)
                body = captured[0]
                payload = json.loads(body)
                pair.append(payload)
                user = json.loads(payload["messages"][1]["content"])
                schema = payload["response_format"]["json_schema"]["schema"]
                assert schema["properties"]["issue_type"]["enum"] == [
                    *report.context.type_labels,
                    None,
                ]
                assert payload["max_tokens"] == 256
                assert payload["temperature"] == 0
                assert payload["reasoning_effort"] == "none"
                assert not {"expected", "acceptable_types", "reason"} & user.keys()
                if case["id"] == "omitted-support":
                    assert "reinstalling" in user["issue_body"]
                    assert not any(
                        "reinstalling" in q["quote"]
                        for q in user["issue_quote_options"]
                    )
                key = f"{arm}/{case['id']}"
                payloads[key] = body
                rows.append(
                    {
                        "arm": arm,
                        "id": case["id"],
                        "cohort": case["cohort"],
                        "expected": case["expected"],
                        "acceptable_types": case.get(
                            "acceptable_types", [case["expected"]]
                        ),
                        "request_sha256": sha256(body).hexdigest(),
                        "null_report_sha256": fingerprint(
                            report.model_dump(mode="json", exclude={"trace_id"})
                        ),
                        "quote_options": len(user["issue_quote_options"]),
                    }
                )
            control, candidate = pair
            assert candidate["messages"][0]["content"] == (
                control["messages"][0]["content"] + SUPPORT_INSTRUCTION
            )
            candidate["messages"][0]["content"] = control["messages"][0]["content"]
            assert candidate == control

        # Rebuild the actual archived Qwen reports, checking exact outgoing bytes
        # and entire report contents, not just the selected type/quote fields.
        key = read(OLD / "review/key.json")
        ratings = read(OLD / "review/codex-ratings.json")["ratings"]
        saved = read(OLD / "run/results.json")
        for case in cases:
            if case["cohort"] != "exposed_diagnostic":
                continue
            row = next(
                r for r in saved if r["id"] == case["id"] and "qwen35" in r["alias"]
            )
            assert len(row["calls"]) == 1
            call = row["calls"][0]
            captured = []

            def recorded(request, *, timeout, call=call, captured=captured):
                assert timeout == 20
                assert sha256(request.data).hexdigest() == call["request_sha256"]
                captured.append(json.loads(request.data))
                return io.BytesIO(base64.b64decode(call["raw_base64"], validate=True))

            with patch("maintainer_copilot.model.urlopen", recorded):
                report = construct_report(
                    case,
                    OpenAICompatibleModel(BASE, row["alias"], reasoning_effort="none"),
                    evidence,
                    catalog,
                )
            assert len(captured) == 1
            assert report.model_dump(mode="json", exclude={"trace_id"}) == {
                k: v for k, v in row["report"].items() if k != "trace_id"
            }
            code = next(
                k for k in key if k["case"] == row["id"] and k["alias"] == row["alias"]
            )
            assert fingerprint(row["report"]) == code["report_sha256"]
            rating = next(r for r in ratings if r["code"] == code["code"])
            assert rating["report_sha256"] == code["report_sha256"]
            user = json.loads(captured[0]["messages"][1]["content"])
            diagnoses.append(
                {
                    "id": case["id"],
                    "code": code["code"],
                    "archived_expected": case["expected"],
                    "selected_type": report.issue_type,
                    "selected_quote": report.issue_type_quote,
                    "report_sha256": code["report_sha256"],
                    "request_sha256": call["request_sha256"],
                    "quote_options": user["issue_quote_options"],
                    "prior_attributed_review": rating,
                }
            )
    return payloads, rows, diagnoses


def prepare(check):
    payloads, rows, diagnoses = build()
    # ADR-0003: full diagnostic requests and quote options remain local-only.
    public_diagnoses = [
        {k: v for k, v in row.items() if k != "quote_options"} for row in diagnoses
    ]
    outputs = {
        "requests.json": rows,
        "diagnosis.json": public_diagnoses,
        "synthetic-requests.json": {
            key: json.loads(body)
            for key, body in payloads.items()
            if not key.split("/")[1].startswith("h-")
        },
    }
    sources = [
        "scripts/issue66_candidate.py",
        "scripts/issue66_prepare.py",
        "scripts/issue66_run.py",
        "tests/test_issue66_semantic_support.py",
        "docs/evaluation/issue-66/cases.json",
        "docs/evaluation/issue-66/protocol.md",
    ]
    sources += [str(p.relative_to(ROOT)) for p in (ROOT / "src").rglob("*.py")]
    old_files = sorted(
        p
        for directory in (
            ROOT / "docs/evaluation",
            ROOT / "src/maintainer_copilot/cases",
        )
        for p in directory.rglob("*")
        if p.is_file() and HERE not in p.parents
    )
    outputs["freeze.json"] = {
        "status": "prepared; no execution authorization",
        "baseline_commit": BASELINE,
        "model": MODEL,
        "base_url": BASE,
        "limits": LIMITS,
        "snapshot_sha256": digest(CACHE),
        "source_sha256": {name: digest(ROOT / name) for name in sorted(sources)},
        "archive_sha256": {str(p.relative_to(ROOT)): digest(p) for p in old_files},
        "artifact_sha256": {
            name: sha256((json.dumps(value, indent=2) + "\n").encode()).hexdigest()
            for name, value in outputs.items()
        },
    }
    for name, value in outputs.items():
        content = json.dumps(value, indent=2) + "\n"
        if check:
            assert (HERE / name).read_text() == content, name
        else:
            with (HERE / name).open("x") as handle:
                handle.write(content)
    if not check:
        LOCAL.mkdir(parents=True, exist_ok=False)
        for key, body in payloads.items():
            target = LOCAL / (key.replace("/", "-") + ".json")
            target.write_bytes(body)
        (LOCAL / "diagnosis-with-options.json").write_text(
            json.dumps(diagnoses, indent=2) + "\n"
        )
    print(
        json.dumps(
            {
                "verified": True,
                "model_dispatches": 0,
                "exact_requests": len(rows),
                "archived_reports_rebuilt": len(diagnoses),
                "archives_preserved": len(old_files),
                "candidate_diff": "system prompt suffix only",
                "candidate_semantic_effectiveness": (
                    "unverified; execution not authorized"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    prepare(parser.parse_args().check)
