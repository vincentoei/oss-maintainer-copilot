"""A model swap must preserve the request and validator at both public report paths."""

import hashlib
import importlib
import io
import json
from pathlib import Path
from typing import Any
from urllib.request import Request
from uuid import UUID

import pytest
from test_triage_quality_replay import replay_opening

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.local_evaluation import _GpuMemory
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.paired_evaluation import PairedBudget
from maintainer_copilot.trace import get_trace

PROBES = json.loads(
    (
        Path(__file__).resolve().parents[1]
        / "docs/evaluation/issue-62/proposed-contrasts.json"
    ).read_bytes()
)["cases"]


@pytest.mark.parametrize("path", ["fixed", "historical_replay"])
def test_model_identity_is_only_wire_difference(
    monkeypatch: pytest.MonkeyPatch, path: str
) -> None:
    payloads: list[dict[str, object]] = []
    aliases = ("pytest-triage:coder3b-ctx16k", "pytest-triage:coder7b-ctx16k")

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        payloads.append(payload)
        assert timeout == 20
        assert payload["max_tokens"] == 256
        assert payload["temperature"] == 0
        user_data = json.loads(payload["messages"][1]["content"])
        assert "proposed_type" not in user_data and "review_status" not in user_data
        # Return the same deliberately invalid selection for both aliases.
        selection = {
            "issue_type": "foreign",
            "quote_index": 0,
            "reply_citation_ids": [],
        }
        return io.BytesIO(
            json.dumps(
                {"choices": [{"message": {"content": json.dumps(selection)}}]}
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    for probe in PROBES:
        payloads.clear()
        for alias in aliases:
            client = OpenAICompatibleModel("http://model.test/v1", alias)
            if path == "historical_replay":
                report = replay_opening(
                    probe["title"], probe["body"], model_client=client
                )
            else:
                report = triage_issue(
                    IssueUnderReview(title=probe["title"], body=probe["body"]),
                    model_client=client,
                    documentation_topics=(),
                )
            assert report.issue_type is None
            assert report.status == "partial"
        left, right = payloads
        assert (left.pop("model"), right.pop("model")) == aliases
        assert left == right


def test_paired_budget_refuses_drift_duplicate_after_restart_and_cap(
    tmp_path: Path,
) -> None:
    body = b'{"model":"control"}'
    allowed = {
        (arm, case): hashlib.sha256(body).hexdigest()
        for arm in ["control", "candidate"]
        for case in ["one", "two", "three"]
    }
    ledger = tmp_path / "reservations.jsonl"
    budget = PairedBudget(ledger, allowed, per_model=2, total=3)
    with pytest.raises(ValueError, match="differs"):
        budget.reserve("control", "one", b"{}")
    with pytest.raises(ValueError, match="differs"):
        budget.reserve("control", "unknown", body)
    assert not ledger.exists()
    budget.reserve("control", "one", body)
    # A lost response still spends its reservation after restarting the client.
    restarted = PairedBudget(ledger, allowed, per_model=2, total=3)
    with pytest.raises(ValueError, match="Duplicate"):
        restarted.reserve("control", "one", body)
    restarted.reserve("control", "two", body)
    with pytest.raises(ValueError, match="exhausted"):
        restarted.reserve("control", "three", body)
    restarted.reserve("candidate", "one", body)
    with pytest.raises(ValueError, match="exhausted"):
        restarted.reserve("candidate", "two", body)
    assert [
        json.loads(line)["sequence"] for line in ledger.read_text().splitlines()
    ] == [1, 2, 3]


@pytest.mark.parametrize("failure", [ConnectionResetError, TimeoutError])
def test_charged_response_read_failure_survives_saved_report_audit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: type[OSError]
) -> None:
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    runner = importlib.import_module("issue62_compare")
    scored = importlib.import_module("downloaded_scored_run")
    auditor = importlib.import_module("downloaded_scored_results")
    monkeypatch.setattr(runner, "_GpuMemory", lambda enabled: _GpuMemory(False))
    alias = "triage-eval:qwen35-4b-16k-v1"
    requests = json.loads(
        (root / "docs/evaluation/downloaded-models/scored/requests.json").read_bytes()
    )
    ledger = tmp_path / "reservations.jsonl"
    budget = PairedBudget(
        ledger,
        {(alias, "xml-A"): requests["xml-A"]["sha256"][alias]},
        per_model=1,
        total=1,
    )

    class BrokenBody(io.BytesIO):
        status = 200

        def read(self, size: int | None = -1) -> bytes:
            raise failure("Response body interrupted")

    class Transport:
        def open(self, request: Request, *, timeout: int) -> BrokenBody:
            assert timeout == 20
            assert len(ledger.read_text().splitlines()) == 1
            return BrokenBody()

    monkeypatch.setattr(scored, "TRANSPORT", Transport())
    charged = scored.ChargedRequest(budget)
    row: dict[str, Any] = {"case": "xml-A", "alias": alias, "expected": "type: bug"}
    probes = {p["id"]: p for p in PROBES}
    runner.run_case(row, charged, charged, {}, probes, [], None)
    assert row["status"] == "transport_error"
    assert row["http_status"] == 200
    assert row["transport_error"] == failure.__name__
    trace = get_trace(UUID(row["report"]["trace_id"]))
    assert trace is not None
    row["trace"] = trace.model_dump(mode="json")
    scored.annotate(row, "unused-digest", {"models": []})
    reservation = json.loads(ledger.read_text())
    auditor.audit_row(row, reservation, "unused-digest", {}, probes, [], None)
    metrics = auditor.arm_metrics([row])
    assert metrics["planned"] == 1
    assert metrics["correct"] == 0
    assert metrics["statuses"] == {"transport_error": 1}
