"""Serve the existing app with real inference and verified frozen candidate reads.

Full issue bodies stay in a temporary acquisition file, never in this repository.
Documentation uses the ordinary live source; this integration is not field scoring.
"""

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import uvicorn

from maintainer_copilot import model
from maintainer_copilot.agent import OpenAICompatibleAgent
from maintainer_copilot.issue_search import _record
from maintainer_copilot.replay import (
    _FrozenIssues,
    candidate_references,
    content_hash,
    load_cases,
)
from maintainer_copilot.web import (
    app,
    get_agent_client,
    get_issue_source,
    get_model_client,
)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--openings", type=Path, required=True)
parser.add_argument("--calls", type=Path, required=True)
parser.add_argument("--ollama-url", required=True)
parser.add_argument("--port", type=int, default=8001)
args = parser.parse_args()
if args.calls.exists():
    parser.error("Use a new calls artifact path")
records = {int(n): _record(d) for n, d in json.loads(args.openings.read_text()).items()}
catalog = load_cases()
cases = {c.issue_number: c for c in catalog}
for case in catalog:
    assert content_hash(records[case.issue_number]) == case.opening_content_sha256
    assert records[case.issue_number].created_at == case.opening_cutoff
    for ref in candidate_references(case, catalog):
        assert content_hash(records[ref.number]) == ref.content_sha256
        assert records[ref.number].created_at == ref.created_at


class FrozenCatalog:
    def get_issue(self, n):
        assert n in cases
        return records[n]

    def search_issues(self, q, before):
        case = next(c for c in catalog if c.opening_cutoff == before)
        candidates = tuple(
            records[r.number] for r in candidate_references(case, catalog)
        )
        return _FrozenIssues(
            records[case.issue_number], candidates, True
        ).search_issues(q, before)


ledger = []


class Observed(OpenAICompatibleAgent):
    def generate_json(
        self, system_prompt, user_data, *, max_tokens, response_schema=None
    ):
        response = super().generate_json(
            system_prompt,
            user_data,
            max_tokens=max_tokens,
            response_schema=response_schema,
        )
        call = {
            "system_prompt_sha256": hashlib.sha256(system_prompt.encode()).hexdigest(),
            "user_data_sha256": hashlib.sha256(
                json.dumps(user_data).encode()
            ).hexdigest(),
            "max_tokens": max_tokens,
            "schema_sha256": hashlib.sha256(
                json.dumps(response_schema, sort_keys=True).encode()
            ).hexdigest(),
        }
        if isinstance(response, model.ModelResponse):
            call.update(asdict(response))
        ledger.append(call)
        args.calls.write_text(json.dumps(ledger, indent=2) + "\n")
        return response


client = Observed(args.ollama_url.rstrip("/") + "/v1", "pytest-triage:coder3b-ctx16k")


async def source():
    return FrozenCatalog()


async def model_client():
    return client


app.dependency_overrides[get_issue_source] = source
app.dependency_overrides[get_model_client] = model_client
app.dependency_overrides[get_agent_client] = model_client
uvicorn.run(app, host="127.0.0.1", port=args.port)
