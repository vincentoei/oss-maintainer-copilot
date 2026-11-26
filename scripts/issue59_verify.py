"""Compare the frozen paired requests and score their saved responses offline."""

import json
from pathlib import Path

from issue59_compare import GUIDANCE

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.replay import load_cases
from maintainer_copilot.workflow_comparison import fingerprint

DATA = Path(__file__).resolve().parents[1] / "docs/evaluation"
RUN = DATA / "issue-59/run"


def read(path):
    return json.loads(path.read_bytes())


def replay_probe(probe, arm, recorded, output):
    class Playback(OpenAICompatibleModel):
        def generate_json(
            self, system_prompt, user_data, *, max_tokens, response_schema=None
        ):
            prompt = system_prompt + (GUIDANCE if arm == "candidate" else "")
            assert recorded == dict(
                prompt_sha256=fingerprint(prompt),
                input_sha256=fingerprint(user_data),
                schema_sha256=fingerprint(response_schema),
                max_tokens=max_tokens,
            )
            return output

    return triage_issue(
        IssueUnderReview(title=probe["title"], body=probe["body"]),
        model_client=Playback("", "archived"),
        documentation_topics=(),
    )


def main():
    if not __debug__:
        raise RuntimeError(
            "Run the artifact assertions with Python optimization disabled"
        )
    previous = DATA / "issue-60/followup"
    old_requests = {
        r["issue_number"]: r
        for r in map(json.loads, (previous / "requests.jsonl").read_text().splitlines())
    }
    old_reports = {
        r["issue_number"]: r["report"] for r in read(previous / "results.json")["cases"]
    }
    old_outputs = {
        r["issue_number"]: r["response"]["output"]
        for r in map(
            json.loads, (previous / "responses.jsonl").read_text().splitlines()
        )
    }
    probes = read(DATA / "issue-59/probes.json")
    expected = {c.issue_number: c.expected_outcome.issue_type for c in load_cases()}
    expected.update({i: p["expected"] for i, p in enumerate(probes, start=1)})
    targets = {10156, 12189, 12228, 12287, 12298, 12360, 12377}
    planned = {
        (arm, "fixed_rag", i) for arm in ("baseline", "candidate") for i in range(1, 5)
    }
    planned.update((arm, "bounded_agent", 12377) for arm in ("baseline", "candidate"))
    planned.update(("candidate", "fixed_rag", i) for i in targets)
    rows = read(RUN / "results.json")
    assert len(rows) == len(planned)
    requests = {}
    types = {}
    prompt_hashes = {}
    agent_call_counts = {}
    for r in rows:
        arm, method, n = key = r["arm"], r["method"], r["number"]
        planned.remove(key)
        directory = RUN / arm / f"{method}-{n}"
        calls = sorted(directory.glob("*-request.json"))
        if method == "bounded_agent":
            agent_call_counts[arm] = len(calls)
        assert 0 < len(calls) <= (4 if method == "bounded_agent" else 1)
        assert len(calls) == len(list(directory.glob("*-response.json")))
        for i in range(1, len(calls) + 1):
            request = read(directory / f"{i}-request.json")
            response = read(directory / f"{i}-response.json")
            assert request["max_tokens"] == 256 and response["error"] is None
            if i < len(calls):
                assert method == "bounded_agent"
                other = RUN / "baseline" / directory.name
                assert request == read(other / f"{i}-request.json")
                assert (
                    response["output"] == read(other / f"{i}-response.json")["output"]
                )
        requests[key] = request
        report = r["report"]
        assert response["output"]["issue_type"] == report["issue_type"]
        assert report["issue_type"] is not None and r["expected"] == expected[n]
        if n <= len(probes):
            replayed = replay_probe(probes[n - 1], arm, request, response["output"])
            assert (replayed.issue_type, replayed.issue_type_quote) == (
                report["issue_type"],
                report["issue_type_quote"],
            )
            prompt_hashes[arm] = request["prompt_sha256"]
        else:
            assert response["output"] == old_outputs[n]
            assert report["issue_type_quote"] == old_reports[n]["issue_type_quote"]
        types[key] = report["issue_type"]
    assert agent_call_counts["baseline"] == agent_call_counts["candidate"]
    assert not planned
    assert len(list(RUN.rglob("*-request.json"))) == 21
    scores = {}
    for group, method, numbers in [
        ("historical", "fixed_rag", sorted(targets)),
        ("synthetic", "fixed_rag", range(1, 5)),
        ("agent", "bounded_agent", [12377]),
    ]:
        pairs = []
        for n in numbers:
            key = "candidate", method, n
            if group == "historical":
                before, prediction = old_requests[n], old_reports[n]["issue_type"]
            else:
                before, prediction = (
                    requests["baseline", method, n],
                    types["baseline", method, n],
                )
            after = requests[key]
            assert before["input_sha256"] == after["input_sha256"]
            assert before["schema_sha256"] == after["schema_sha256"]
            assert before["prompt_sha256"] == prompt_hashes["baseline"]
            assert after["prompt_sha256"] == prompt_hashes["candidate"]
            pairs.append((prediction, types[key], expected[n]))
        scores[group] = dict(
            before=sum(a == e for a, b, e in pairs),
            candidate=sum(b == e for a, b, e in pairs),
            changed=sum(a != b for a, b, e in pairs),
            count=len(pairs),
        )
    assert [(s["before"], s["candidate"], s["changed"]) for s in scores.values()] == [
        (1, 1, 0),
        (3, 3, 0),
        (1, 1, 0),
    ]
    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    main()
