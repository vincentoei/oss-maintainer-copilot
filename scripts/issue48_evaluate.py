"""Verify #48's frozen serving contract before the twenty-case real run."""

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from maintainer_copilot.local_evaluation import _ollama_json
from maintainer_copilot.local_evaluation import main as evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ollama-url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--serving-output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.serving_output.exists():
        parser.error(
            "Use new artifact paths; preserved results must not be overwritten"
        )
    base = args.ollama_url.rstrip("/")
    name = "pytest-triage:coder3b-ctx16k"
    version = _ollama_json(f"{base}/api/version")
    tags = _ollama_json(f"{base}/api/tags")
    baseline = json.loads(Path("docs/evaluation/issue-45-results.json").read_text())
    before = baseline["models"][name]
    identity = next(m for m in tags["models"] if m["name"] == name)
    info = _ollama_json(f"{base}/api/show", {"model": name})
    if identity["digest"] != before["identity"]["digest"]:
        raise ValueError("Serving digest differs from the preserved selected model")
    if identity["details"]["quantization_level"] != "Q4_K_M":
        raise ValueError("Serving quantization differs")
    params = dict(re.findall(r"^(\w+)\s+(\S+)\s*$", info["parameters"], re.M))
    expected = {
        "num_ctx": 16384,
        "temperature": 0,
        "seed": 42,
        "top_k": 20,
        "top_p": 0.8,
        "repeat_penalty": 1,
    }
    if set(params) != set(expected) or any(
        float(params[key]) != value for key, value in expected.items()
    ):
        raise ValueError("Serving generation parameters differ from #48's contract")
    with args.serving_output.open("x") as handle:
        json.dump(
            {
                "recorded_at": datetime.now(UTC).isoformat(),
                "ollama_url": base,
                "server": version,
                "identity": identity,
                "parameters": params,
                "expected": expected,
                "verification": (
                    "exact baseline digest, Q4_K_M and alias parameters passed"
                ),
            },
            handle,
            indent=2,
        )
        handle.write("\n")
    sys.argv = [
        "local_evaluation",
        "--ollama-url",
        base,
        "--model",
        name,
        "--output",
        str(args.output),
    ]
    evaluate()


if __name__ == "__main__":
    main()
