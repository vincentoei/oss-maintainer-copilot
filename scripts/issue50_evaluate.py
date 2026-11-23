"""One frozen development pass. Pilot inference requires a separate human gate."""

import argparse
import fcntl
import hashlib
import json
import os
import platform
import re
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from maintainer_copilot import model
from maintainer_copilot.local_evaluation import (
    _LiveEvidenceCache,
    _ollama_json,
    evaluate_local_model,
)


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=["A", "B"], required=True)
    parser.add_argument("--ollama-url", required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--recover-flagged", action="store_true")
    args = parser.parse_args()
    os.environ["GITHUB_TOKEN"] = subprocess.check_output(
        ["gh", "auth", "token"], text=True
    ).strip()
    root = args.directory
    root.mkdir(parents=True, exist_ok=True)
    suffix = "-recovered" if args.recover_flagged else ""
    output = root / f"development-2-{args.arm}{suffix}.json"
    marker = root / f"development-2-{args.arm}{suffix}.started"
    skip = []
    if args.recover_flagged:
        previous = json.loads((root / f"development-2-{args.arm}.json").read_text())
        skip = [c["issue_number"] for c in previous["cases"] if not c["error"]]
        if any(c["model_calls"] for c in previous["cases"] if c["error"]):
            parser.error("Cannot recover cases that already dispatched inference")
    if output.exists() or marker.exists():
        parser.error("Arm already started; no automatic repetition allowed")
    if args.arm == "B" and not (root / "development-2-A.json").exists():
        parser.error("Complete same-model control A before candidate B")
    base = args.ollama_url.rstrip("/")
    name = "pytest-triage:coder3b-ctx16k"
    baseline = json.loads(
        Path("docs/evaluation/issue-48-serving-review.json").read_text()
    )
    tags = _ollama_json(base + "/api/tags")
    identity = next(m for m in tags["models"] if m["name"] == name)
    if identity["digest"] != baseline["identity"]["digest"]:
        raise ValueError("Selected 3B digest changed")
    serving = _ollama_json(base + "/api/show", {"model": name})
    params = dict(re.findall(r"^(\w+)\s+(\S+)\s*$", serving["parameters"], re.M))
    if set(params) != set(baseline["parameters"]) or any(
        float(params[k]) != float(v) for k, v in baseline["parameters"].items()
    ):
        raise ValueError("Serving settings changed")
    marker.write_text(datetime.now(UTC).isoformat())
    (root / f"serving-2-{args.arm}{suffix}.json").write_text(
        json.dumps(
            {
                "identity": identity,
                "show": serving,
                "version": _ollama_json(base + "/api/version"),
                "platform": platform.platform(),
            },
            indent=2,
        )
        + "\n"
    )

    class Observed(model.OpenAICompatibleModel):
        drafting = args.arm == "B"
        evidence_enabled = True
        report_max_tokens = 512

        def generate_json(
            self, system_prompt, user_data, *, max_tokens, response_schema=None
        ):
            with (root / "requests.jsonl").open("a+") as ledger:
                fcntl.flock(ledger, fcntl.LOCK_EX)
                ledger.seek(0)
                records = [json.loads(line) for line in ledger if line.strip()]
                development_count = sum(
                    r.get("partition") == "development" for r in records
                )
                if len(records) >= 120 or development_count >= 60:
                    raise model.ModelUnavailable("Experiment request budget exhausted")
                record = {
                    "request": len(records) + 1,
                    "arm": args.arm,
                    "partition": "development",
                    "iteration": 2,
                    "warmup": False,
                    "dispatched_at": datetime.now(UTC).isoformat(),
                    "prompt_sha256": sha(system_prompt),
                    "input_sha256": sha(user_data),
                    "schema_sha256": sha(response_schema),
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
                with (root / "responses.jsonl").open("a") as handle:
                    handle.write(
                        json.dumps({**record, "error": type(exc).__name__}) + "\n"
                    )
                raise
            with (root / "responses.jsonl").open("a") as handle:
                handle.write(
                    json.dumps(
                        {
                            **record,
                            "response": asdict(response)
                            if isinstance(response, model.ModelResponse)
                            else response,
                        }
                    )
                    + "\n"
                )
            return response

    cache = _LiveEvidenceCache()
    result = evaluate_local_model(
        Observed(base + "/v1", name),
        commit_source=cache,
        issue_source=cache,
        source_reader=cache,
        measure_gpu=True,
        skip_issue_numbers=skip,
    )
    output.write_text(json.dumps(result, indent=2) + "\n")
    (root / f"residency-2-{args.arm}{suffix}.json").write_text(
        json.dumps(_ollama_json(base + "/api/ps"), indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
