"""Issue #60 audit and measurement behavior at the public evaluator seam."""

import io
import json
from dataclasses import replace
from pathlib import Path
from urllib.request import Request

import pytest
from test_local_evaluation import RecordedEvidence

from maintainer_copilot.classification_evaluation import evaluate_classification
from maintainer_copilot.source import PublicRepositorySource


@pytest.mark.parametrize("changed", [False, True])
def test_availability_audit_is_inference_free_and_flags_changed_openings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    changed: bool,
) -> None:
    evidence = RecordedEvidence()
    if changed:
        evidence.opening = replace(evidence.opening, body="a later edit")
    dispatches = 0

    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        nonlocal dispatches
        dispatches += 1
        assert not changed
        assert len((tmp_path / "run/requests.jsonl").read_text().splitlines()) == 1
        return io.BytesIO(
            json.dumps(
                {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "issue_type": "type: enhancement",
                                        "issue_type_quote": "Feature",
                                        "reply_citation_ids": [],
                                    }
                                )
                            }
                        }
                    ],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 20},
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    result = evaluate_classification(
        tmp_path / "run",
        "http://model.test/v1",
        phase="after",
        cases=[evidence.case],
        commit_source=evidence,
        issue_source=evidence,
        source_reader=PublicRepositorySource(),
    )
    assert dispatches == (0 if changed else 1)
    assert len(result["cases"]) == 1
    if changed:
        assert result["preflight"][0]["expected_reachable"] is None
        assert result["cases"][0]["scores"] is None
        assert not (tmp_path / "run/requests.jsonl").exists()
    else:
        assert result["preflight"][0]["expected_reachable"] is True
        assert len(result["preflight"][0]["offered_types"]) == 13
        assert result["cases"][0]["scores"]["issue_type"]["correct"] is True
