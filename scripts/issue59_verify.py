"""Compare the frozen paired requests and score their saved responses offline."""

import json
from pathlib import Path

from maintainer_copilot.replay import load_cases

DATA = Path(__file__).resolve().parents[1] / "docs/evaluation"
RUN = DATA / "issue-59/run"


def read(path):
    return json.loads(path.read_bytes())


def main():
    previous = DATA / "issue-60/followup"
    old_requests = {
        r["issue_number"]: r
        for r in map(json.loads, (previous / "requests.jsonl").read_text().splitlines())
    }
    old_reports = {
        r["issue_number"]: r["report"] for r in read(previous / "results.json")["cases"]
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
    for r in rows:
        arm, method, n = key = r["arm"], r["method"], r["number"]
        planned.remove(key)
        directory = RUN / arm / f"{method}-{n}"
        calls = sorted(directory.glob("*-request.json"))
        assert 0 < len(calls) <= (4 if method == "bounded_agent" else 1)
        assert len(calls) == len(list(directory.glob("*-response.json")))
        for i in range(1, len(calls) + 1):
            request = read(directory / f"{i}-request.json")
            response = read(directory / f"{i}-response.json")
            assert request["max_tokens"] == 256 and response["error"] is None
        requests[key] = request
        report = r["report"]
        assert response["output"]["issue_type"] == report["issue_type"]
        assert report["issue_type"] is not None and r["expected"] == expected[n]
        types[key] = report["issue_type"]
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
            assert before["prompt_sha256"] != after["prompt_sha256"]
            pairs.append((prediction, types[key], expected[n]))
        scores[group] = dict(
            before=sum(a == e for a, b, e in pairs),
            candidate=sum(b == e for a, b, e in pairs),
            changed=sum(a != b for a, b, e in pairs),
            count=len(pairs),
        )
    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    main()
