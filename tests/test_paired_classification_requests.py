"""A model swap must preserve the request and validator at both public report paths."""

import io
import json
from pathlib import Path
from urllib.request import Request

import pytest
from test_triage_quality_replay import replay_opening

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel

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
