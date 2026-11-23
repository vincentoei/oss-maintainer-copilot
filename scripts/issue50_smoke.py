"""Real-inference checks through both public HTTP interfaces using ASGI transport."""

import asyncio
import fcntl
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import httpx2

from maintainer_copilot.agent import OpenAICompatibleDraftingAgent
from maintainer_copilot.issue_search import GitHubIssueSource
from maintainer_copilot.model import ModelResponse
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

ROOT = Path("/tmp/issue-50-run")
SERVE_WEB = "--serve-web" in sys.argv
OUTPUT = ROOT / ("web-started.json" if SERVE_WEB else "api-smoke.json")
if OUTPUT.exists():
    raise SystemExit("Smoke already attempted; preserve the previous artifact")
OUTPUT.write_text('{"status":"started"}\n')
os.environ["GITHUB_TOKEN"] = subprocess.check_output(
    ["gh", "auth", "token"], text=True
).strip()
catalog = load_cases()
case = next(c for c in catalog if c.issue_number == 12201)
public = GitHubIssueSource()
opening = public.get_issue(case.issue_number)
assert content_hash(opening) == case.opening_content_sha256
assert opening.created_at == case.opening_cutoff
candidates = []
for reference in candidate_references(case, catalog):
    candidate = public.get_issue(reference.number)
    assert content_hash(candidate) == reference.content_sha256
    assert candidate.created_at == reference.created_at
    candidates.append(candidate)

calls = []


class Observed(OpenAICompatibleDraftingAgent):
    def generate_json(
        self, system_prompt, user_data, *, max_tokens, response_schema=None
    ):
        with (ROOT / "requests.jsonl").open("a+") as ledger:
            fcntl.flock(ledger, fcntl.LOCK_EX)
            ledger.seek(0)
            previous = [json.loads(line) for line in ledger if line.strip()]
            if len(previous) >= 120:
                raise ValueError("Request budget exhausted")
            record = {
                "request": len(previous) + 1,
                "partition": "api-smoke",
                "prompt_sha256": hashlib.sha256(system_prompt.encode()).hexdigest(),
                "input_sha256": hashlib.sha256(
                    json.dumps(user_data).encode()
                ).hexdigest(),
                "schema_sha256": hashlib.sha256(
                    json.dumps(response_schema).encode()
                ).hexdigest(),
                "max_tokens": max_tokens,
            }
            ledger.write(json.dumps(record) + "\n")
            ledger.flush()
            os.fsync(ledger.fileno())
        try:
            response = super().generate_json(
                system_prompt,
                user_data,
                max_tokens=max_tokens,
                response_schema=response_schema,
            )
        except Exception as exc:
            calls.append({**record, "error": type(exc).__name__})
            raise
        else:
            calls.append(
                {
                    **record,
                    "response": asdict(response)
                    if isinstance(response, ModelResponse)
                    else response,
                }
            )
            return response
        finally:
            (
                ROOT / ("web-model-calls.json" if SERVE_WEB else "api-smoke-calls.json")
            ).write_text(json.dumps(calls, indent=2) + "\n")


async def client():
    return Observed("http://172.17.48.1:11434/v1", "pytest-triage:coder3b-ctx16k")


async def issues():
    return _FrozenIssues(opening, tuple(candidates), True)


async def main():
    app.dependency_overrides[get_model_client] = client
    app.dependency_overrides[get_agent_client] = client
    app.dependency_overrides[get_issue_source] = issues
    reports = []
    try:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://test"
        ) as http:
            for endpoint in ["/api/triage", "/api/agent/triage"]:
                response = await http.post(
                    endpoint,
                    json={
                        "title": opening.title,
                        "body": opening.body,
                        "number": opening.number,
                    },
                )
                data = response.json()
                trace = await http.get(f"/api/traces/{data['trace_id']}")
                reports.append(
                    {
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "report": data,
                        "trace": trace.json(),
                    }
                )
                OUTPUT.write_text(json.dumps(reports, indent=2) + "\n")
    finally:
        app.dependency_overrides.clear()


if SERVE_WEB:
    import uvicorn

    app.dependency_overrides[get_model_client] = client
    app.dependency_overrides[get_agent_client] = client
    app.dependency_overrides[get_issue_source] = issues
    (ROOT / "web-opening.json").write_text(
        json.dumps(
            {
                "title": opening.title,
                "body": opening.body,
                "number": opening.number,
            }
        )
    )
    uvicorn.run(app, host="127.0.0.1", port=8002)
else:
    asyncio.run(main())
