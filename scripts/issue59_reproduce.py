"""Replay a saved Qwen selection through the encoder/validator of its own era."""

import argparse
import hashlib
import json
from pathlib import Path

from maintainer_copilot.model import (
    ModelRequest,
    OpenAICompatibleModel,
    generate_validated,
)
from maintainer_copilot.workflow_comparison import fingerprint

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["before", "followup"])
    parser.add_argument("opening", type=Path)
    args = parser.parse_args()
    case = json.loads(
        (ROOT / "src/maintainer_copilot/cases/pytest_12377.json").read_bytes()
    )
    opening = json.loads(args.opening.read_bytes())
    title, body = opening["title"], opening["body"]
    if (
        hashlib.sha256(f"{title}\0{body}".encode()).hexdigest()
        != case["opening_content_sha256"]
    ):
        raise ValueError("Opening differs from the verified historical case")
    path = ROOT / "docs/evaluation/issue-60" / args.phase / "responses.jsonl"
    (record,) = (
        r
        for line in path.read_text().splitlines()
        if (r := json.loads(line))["issue_number"] == 12377
    )

    class Playback(OpenAICompatibleModel):
        def generate_json(
            self, system_prompt, user_data, *, max_tokens, response_schema=None
        ):
            for value, key in [
                (system_prompt, "prompt"),
                (user_data, "input"),
                (response_schema, "schema"),
            ]:
                if fingerprint(value) != record[f"{key}_sha256"]:
                    raise ValueError(f"Historical {key} mismatch")
            if max_tokens != record["max_tokens"]:
                raise ValueError("Output token limit changed")
            print(
                user_data.get(
                    "type_evidence_options", user_data.get("issue_quote_options")
                )
            )
            return json.loads(
                json.loads(record["raw_response_utf8"])["choices"][0]["message"][
                    "content"
                ]
            )

    result = generate_validated(
        Playback("", "playback"), ModelRequest(title, body, (), ())
    )
    print(result.issue_type, result.issue_type_quote)
    if result.issue_type != case["expected_outcome"]["issue_type"]:
        raise AssertionError(result.issue_type)


if __name__ == "__main__":
    main()
