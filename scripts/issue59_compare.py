"""Run the predeclared issue 59 paired diagnostic with frozen public evidence."""

import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.agent import OpenAICompatibleAgent
from maintainer_copilot.classification_evaluation import AvailabilityModel
from maintainer_copilot.local_evaluation import _LiveEvidenceCache
from maintainer_copilot.replay import load_cases, replay_case
from maintainer_copilot.workflow_comparison import (
    MODEL_NAME,
    ROOT,
    _EvidenceSnapshot,
    _save,
    fingerprint,
    serving_snapshot,
)

DATA = ROOT / "docs/evaluation"
TARGET = (10156, 12189, 12228, 12287, 12298, 12360, 12377)
GUIDANCE = (
    " If the requested change is to correct or complete published instructions, "
    "classify the report as documentation. If the reporter wants help applying the "
    "instructions to their own situation, classify it as a question. A question can "
    "point out a documentation defect, and a usage question can cite documentation."
)


class Preflight(AvailabilityModel):
    def __init__(self, record):
        super().__init__()
        self.record = record
        self.matches = False

    def generate_json(self, prompt, user_data, *, max_tokens, response_schema=None):
        self.matches = all(
            fingerprint(value) == self.record[key + "_sha256"]
            for key, value in (
                ("input", user_data),
                ("schema", response_schema),
                ("prompt", prompt),
            )
        )
        return super().generate_json(
            prompt,
            user_data,
            max_tokens=max_tokens,
            response_schema=response_schema,
        )


class Endpoint(OpenAICompatibleAgent):
    def __init__(self, base, directory, number, method, arm):
        super().__init__(base + "/v1", MODEL_NAME)
        self.output = directory / f"{method}-{number}"
        self.output.mkdir()
        self.limit = 4 if method == "bounded_agent" else 1
        self.calls = 0
        self.arm = arm

    def generate_json(
        self, system_prompt, user_data, *, max_tokens, response_schema=None
    ):
        if self.calls >= self.limit or max_tokens != 256:
            raise ValueError("Frozen dispatch limit reached")
        if self.arm == "candidate" and "quote_index" in response_schema.get(
            "properties", {}
        ):
            system_prompt += GUIDANCE
        self.calls += 1
        with (self.output / f"{self.calls}-request.json").open("x") as handle:
            json.dump(
                dict(
                    prompt_sha256=fingerprint(system_prompt),
                    input_sha256=fingerprint(user_data),
                    schema_sha256=fingerprint(response_schema),
                    max_tokens=max_tokens,
                ),
                handle,
            )
            handle.flush()
            os.fsync(handle.fileno())
        response = super().generate_json(
            system_prompt,
            user_data,
            max_tokens=max_tokens,
            response_schema=response_schema,
        )
        _save(self.output / f"{self.calls}-response.json", asdict(response))
        return response


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("ollama_url")
    args = parser.parse_args()
    baseline = DATA / "issue-60/followup"
    records = {
        r["issue_number"]: r
        for line in (baseline / "requests.jsonl").read_text().splitlines()
        if (r := json.loads(line))
    }
    cases = {c.issue_number: c for c in load_cases()}
    cache = _LiveEvidenceCache()
    evidence = _EvidenceSnapshot(cache, cache, cache)
    replay = dict(
        commit_source=evidence,
        source_reader=evidence,
        issue_source=evidence,
        candidate_catalog=cases.values(),
        keyword_filter=True,
    )
    for number in TARGET:
        check = Preflight(records[number])
        replay_case(cases[number], model_client=check, **replay)
        if not check.matches:
            raise ValueError(f"Historical request mismatch for {number}")
    evidence.frozen = True
    server = serving_snapshot(args.ollama_url)
    original = json.loads((baseline / "results.json").read_bytes())["serving"]
    for key in ("version", "template_sha256"):
        if server[key] != original[key]:
            raise ValueError(f"Serving {key} changed")
    args.directory.mkdir(exist_ok=False)
    _save(
        args.directory / "serving.json",
        {k: server[k] for k in ("version", "identity", "template_sha256")}
        | {"parameters": server["show"]["parameters"]},
    )
    probes = json.loads((DATA / "issue-59/probes.json").read_text())
    results = []

    def run_arm(arm):
        directory = args.directory / arm
        directory.mkdir()

        def run(number, method, expected, probe=None):
            client = Endpoint(args.ollama_url, directory, number, method, arm)
            if probe:
                report = triage_issue(
                    IssueUnderReview(title=probe["title"], body=probe["body"]),
                    model_client=client,
                    documentation_topics=(),
                )
            else:
                kwargs = (
                    {"agent_client": client}
                    if method == "bounded_agent"
                    else {"model_client": client}
                )
                report = replay_case(cases[number], **kwargs, **replay)
            results.append(
                dict(
                    arm=arm,
                    number=number,
                    method=method,
                    expected=expected,
                    report=report.model_dump(mode="json"),
                )
            )
            _save(args.directory / "results.json", results)

        if arm == "candidate":
            for n in TARGET:
                run(n, "fixed_rag", cases[n].expected_outcome.issue_type)
        for index, probe in enumerate(probes, start=1):
            run(index, "fixed_rag", probe["expected"], probe)
        run(12377, "bounded_agent", cases[12377].expected_outcome.issue_type)

    for arm in ("baseline", "candidate"):
        run_arm(arm)


if __name__ == "__main__":
    main()
