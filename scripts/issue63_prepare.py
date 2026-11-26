"""Capture the proposed fixed requests without contacting a model server."""

import io
import json
import os
from hashlib import sha256
from unittest.mock import patch

from downloaded_scored_prepare import CACHE, restore
from issue63_application import application, integration

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import (
    CaseFlagged,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.workflow_comparison import ROOT, fingerprint

HERE = ROOT / "docs/evaluation/issue-63"


def prepare():
    cases_path = HERE / "proposed-cases.json"
    draft = json.loads(cases_path.read_bytes())
    inspection = json.loads((HERE / "serving-inspection.json").read_bytes())
    if inspection["status"] != "verified" or inspection["model_dispatches"] != 0:
        raise ValueError("Verified metadata-only model inspection is required")
    aliases = list(inspection["arms"])
    if len(aliases) != 3 or len(draft["cases"]) != 12:
        raise ValueError("Proposed arms or case count changed")
    catalog = load_cases()
    historical = {c.issue_number: c for c in catalog}
    if (
        sha256(CACHE.read_bytes()).hexdigest()
        != json.loads(
            (ROOT / "docs/evaluation/downloaded-models/scored/freeze.json").read_bytes()
        )["snapshot_sha256"]
    ):
        raise ValueError("Retained historical evidence snapshot changed")
    evidence = restore()
    rows = []
    integrations = []

    def capture(key, cohort, expected, invoke):
        wire = {}
        normalized = []
        error = None
        for alias in aliases:
            observed = []

            def endpoint(request, *, timeout, alias=alias, observed=observed):
                if timeout != 20 or request.full_url != (
                    inspection["base_url"] + "/v1/chat/completions"
                ):
                    raise ValueError("Unexpected application route or deadline")
                body = json.loads(request.data)
                if body["model"] != alias or body["reasoning_effort"] != "none":
                    raise ValueError("Application model/effort differs from proposal")
                user = json.loads(body["messages"][1]["content"])
                if {"expected", "proposed_type", "review_status"} & user.keys():
                    raise ValueError("Annotation leaked into the model input")
                observed.append(sha256(request.data).hexdigest())
                body.pop("model")
                normalized.append(fingerprint(body))
                return io.BytesIO(
                    json.dumps(
                        {
                            "choices": [
                                {
                                    "message": {
                                        "content": json.dumps(
                                            {
                                                "issue_type": None,
                                                "quote_index": None,
                                                "reply_citation_ids": [],
                                            }
                                        )
                                    }
                                }
                            ]
                        }
                    ).encode()
                )

            with (
                patch.dict(
                    os.environ,
                    {
                        "MODEL_NAME": alias,
                        "MODEL_BASE_URL": inspection["base_url"] + "/v1",
                        "MODEL_REASONING_EFFORT": "none",
                    },
                ),
                patch("maintainer_copilot.model.urlopen", endpoint),
            ):
                try:
                    invoke(OpenAICompatibleModel.from_environment())
                except (CaseFlagged, ValueError) as exc:
                    error = str(exc)
            if len(observed) != 1:
                error = error or "No single application request was captured"
            else:
                wire[alias] = observed[0]
        if not error and (len(normalized) != 3 or len(set(normalized)) != 1):
            raise ValueError("Paired fixed requests differ beyond model identity")
        rows.append(
            {
                "id": key,
                "cohort": cohort,
                "proposed_expected": expected,
                "error": error,
                "wire_sha256": wire,
                "normalized_sha256": normalized[0] if not error else None,
            }
        )

    for case in draft["cases"]:
        capture(
            case["id"],
            "fresh_synthetic",
            case["proposed_type"],
            lambda client, case=case: triage_issue(
                IssueUnderReview(title=case["title"], body=case["body"]),
                model_client=client,
                documentation_topics=(),
            ),
        )
    for number in (12219, 12223, 12249):
        case = historical[number]
        capture(
            f"h-{number}",
            "exposed_bug_loss",
            case.expected_outcome.issue_type,
            lambda client, case=case: replay_case(
                case,
                model_client=client,
                candidate_catalog=catalog,
                keyword_filter=True,
                commit_source=evidence,
                issue_source=evidence,
                source_reader=evidence,
            ),
        )
        rows[-1].update(
            opening_cutoff=case.opening_cutoff.isoformat(),
            opening_content_sha256=case.opening_content_sha256,
            repository_commit=case.repository_commit,
            candidate_numbers=[r.number for r in candidate_references(case, catalog)],
        )
    active = []

    def integration_capture(request, *, timeout):
        if (
            timeout != 20
            or request.full_url != inspection["base_url"] + "/v1/chat/completions"
        ):
            raise ValueError("Unexpected integration route/deadline")
        body = json.loads(request.data)
        if body["model"] != aliases[-1] or body["reasoning_effort"] != "none":
            raise ValueError("Unexpected integration model/thinking mode")
        active.append(sha256(request.data).hexdigest())
        schema = body["response_format"]["json_schema"]["schema"]
        output = (
            {"tool": "finish", "arguments": {}}
            if "enum" in schema
            else {"issue_type": None, "quote_index": None, "reply_citation_ids": []}
        )
        return io.BytesIO(
            json.dumps(
                {"choices": [{"message": {"content": json.dumps(output)}}]}
            ).encode()
        )

    with patch("maintainer_copilot.model.urlopen", integration_capture):
        with application(inspection["base_url"]) as url:
            for kind in ("python", "api", "browser", "agent"):
                for opening in json.loads(
                    (HERE / "integration-inputs.json").read_bytes()
                ):
                    active.clear()
                    integration(kind, opening, url)
                    if len(active) != (2 if kind == "agent" else 1):
                        raise ValueError(
                            "Integration did not capture the exact call count"
                        )
                    integrations.append(
                        {
                            "id": kind + "-" + opening["id"],
                            "kind": kind,
                            "input_id": opening["id"],
                            "wire_sha256": list(active),
                        }
                    )
    return {
        "status": "draft_not_authorized_for_execution",
        "expected_type_review": draft["review"],
        "cases_sha256": sha256(cases_path.read_bytes()).hexdigest(),
        "model_dispatches": 0,
        "fixed_observations": len(rows),
        "fixed_request_slots": len(rows) * len(aliases),
        "integration_slots": sum(len(r["wire_sha256"]) for r in integrations),
        "integrations": integrations,
        "rows": rows,
    }


if __name__ == "__main__":
    print(json.dumps(prepare(), indent=2))
