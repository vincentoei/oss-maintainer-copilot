"""Public report guardrails for the unadopted issue #66 prompt experiment."""

import importlib
import io
import json
from pathlib import Path
from urllib.request import Request

import pytest

from maintainer_copilot import IssueUnderReview, triage_issue


def test_candidate_keeps_exact_quotes_and_exposes_semantic_validation_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    candidate = importlib.import_module("issue66_candidate")
    body = "The hook never runs in this project."

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        user = json.loads(payload["messages"][1]["content"])
        assert user["issue_body"] == body
        assert user["issue_quote_options"][1] == {"index": 1, "quote": body}
        return io.BytesIO(
            json.dumps(
                {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "issue_type": "type: regression",
                                        "quote_index": 1,
                                        "reply_citation_ids": [],
                                    }
                                )
                            }
                        }
                    ]
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    report = triage_issue(
        IssueUnderReview(title="Hook execution", body=body),
        model_client=candidate.SemanticSupportCandidate("http://model.test/v1", "test"),
        documentation_topics=(),
    )
    # The proposed prompt is guidance, not a semantic validator. Retain a known
    # unsupported selection to prevent claiming exact copying proves regression.
    assert report.issue_type == "type: regression"
    assert report.issue_type_quote == body
