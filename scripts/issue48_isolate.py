"""Replay all cases with a select-all controlled client; never quality evidence."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from maintainer_copilot.local_evaluation import _LiveEvidenceCache
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.replay import load_cases, replay_case


class SelectAll:
    def __init__(self) -> None:
        self.request: ModelRequest | None = None

    def generate(self, request: ModelRequest) -> object:
        self.request = request
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": [s.citation_id for s in request.reply_statements],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Refuse to overwrite preserved isolation evidence.
    with args.output.open("x") as handle:
        handle.write('{"status":"starting"}\n')
    cache = _LiveEvidenceCache()
    catalog = load_cases()
    rows = []
    for case in catalog:
        client = SelectAll()
        report = replay_case(
            case,
            model_client=client,
            candidate_catalog=catalog,
            keyword_filter=True,
            commit_source=cache,
            issue_source=cache,
            source_reader=cache,
        )
        assert client.request is not None
        rows.append(
            {
                "issue_number": case.issue_number,
                "template_profile": case.template_profile,
                "content_sha256": case.opening_content_sha256,
                "opening_cutoff": case.opening_cutoff.isoformat(),
                "repository_commit": case.repository_commit,
                "required_reply_ids": client.request.required_reply_ids,
                "available_statements": [
                    asdict(s) for s in client.request.reply_statements
                ],
                "controlled_report": report.model_dump(mode="json"),
            }
        )
    args.output.write_text(
        json.dumps(
            {
                "scope": (
                    "Controlled select-all supplied statements only; "
                    "not real-model quality"
                ),
                "cases": rows,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Verified and isolated {len(rows)} cases")


if __name__ == "__main__":
    main()
