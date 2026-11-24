"""Serve the existing app with a durable twelve-dispatch smoke-check budget."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
from time import perf_counter
from typing import Any
from urllib.request import Request, urlopen

import uvicorn

from maintainer_copilot.agent import OpenAICompatibleAgent
from maintainer_copilot.web import app, get_agent_client, get_model_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--directory", type=Path, required=True)
parser.add_argument("--ollama-url", required=True)
parser.add_argument("--port", type=int, default=8033)
args = parser.parse_args()
directory: Path = args.directory
directory.mkdir(parents=True, exist_ok=True)
base = args.ollama_url.rstrip("/")
name = "pytest-triage:coder3b-ctx16k"


def ollama(path: str, payload: object | None = None) -> Any:
    request = Request(
        base + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read(2_000_000))


identity = next(m for m in ollama("/api/tags")["models"] if m["name"] == name)
assert (
    identity["digest"]
    == "3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8"
)
assert identity["details"]["quantization_level"] == "Q4_K_M"
show = ollama("/api/show", {"model": name})
settings = dict(
    line.split(maxsplit=1) for line in show["parameters"].strip().splitlines()
)
assert settings == {
    "repeat_penalty": "1",
    "seed": "42",
    "temperature": "0",
    "top_k": "20",
    "top_p": "0.8",
    "num_ctx": "16384",
}
serving = {
    "identity": identity,
    "parameters": settings,
    "template_sha256": hashlib.sha256(show["template"].encode()).hexdigest(),
    "version": ollama("/api/version"),
    "model_info": show["model_info"],
}
if not (directory / "serving.json").exists():
    (directory / "serving.json").write_text(json.dumps(serving, indent=2) + "\n")
else:
    assert json.loads((directory / "serving.json").read_text()) == serving
os.environ["REPOSITORY_REGISTRY_PATH"] = str(directory / "repositories.sqlite3")
os.environ.pop("MODEL_DRAFTING", None)


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


class BudgetedClient(OpenAICompatibleAgent):
    def generate_json(
        self,
        system_prompt: str,
        user_data: object,
        *,
        max_tokens: int,
        response_schema: dict[str, object] | None = None,
    ) -> object:
        with (directory / "requests.jsonl").open("a+") as ledger:
            fcntl.flock(ledger, fcntl.LOCK_EX)
            ledger.seek(0)
            count = len(ledger.readlines())
            if count >= 12:
                raise RuntimeError("Declared twelve-dispatch budget exhausted")
            record = {
                "request": count + 1,
                "prompt_sha256": fingerprint(system_prompt),
                "input_sha256": fingerprint(user_data),
                "schema_sha256": fingerprint(response_schema),
                "max_tokens": max_tokens,
                "repository": user_data.get("repository")
                if isinstance(user_data, dict)
                else None,
            }
            ledger.write(json.dumps(record) + "\n")
            ledger.flush()
            os.fsync(ledger.fileno())
        self.raw = None

        def capture(body: bytes) -> None:
            self.raw = body

        self.response_observer = capture
        started = perf_counter()
        try:
            result = super().generate_json(
                system_prompt,
                user_data,
                max_tokens=max_tokens,
                response_schema=response_schema,
            )
            record["transport"] = "returned"
            return result
        except Exception:
            record["transport"] = "failed"
            raise
        finally:
            record["seconds"] = perf_counter() - started
            record["raw_response"] = (
                self.raw.decode("utf-8", errors="replace") if self.raw else None
            )
            (directory / f"response-{count + 1}.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )


async def client() -> BudgetedClient:
    return BudgetedClient(base + "/v1", name)


app.dependency_overrides[get_model_client] = client
app.dependency_overrides[get_agent_client] = client
uvicorn.run(app, host="127.0.0.1", port=args.port)
