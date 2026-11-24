"""Run the bounded real HTTP smoke flow against issue33_serve.py."""

import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

root = Path("docs/evaluation/issue-33")
output = root / "http-reports.json"
if output.exists():
    raise SystemExit("Refusing to overwrite smoke evidence")
base = "http://127.0.0.1:8033"


def call(
    path: str, payload: object | None = None, *, method: str | None = None
) -> dict[str, object]:
    request = Request(
        base + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    try:
        with urlopen(request, timeout=85) as response:
            body = response.read()
            return {
                "status": response.status,
                "body": json.loads(body) if body else None,
            }
    except HTTPError as exc:
        return {"status": exc.code, "body": json.load(exc)}


result = {"list_after_restart": call("/api/repositories"), "reports": []}
entries = result["list_after_restart"]["body"]
assert (
    entries
    == json.loads((root / "browser-registration.json").read_text())["before_restart"]
)
result["restart_persistence"] = True
(root / "http-source-hashes.json").write_text(
    json.dumps(
        {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path("src/maintainer_copilot").glob("*.py")
        },
        indent=2,
    )
    + "\n"
)
for repository in ("pytest-dev/pytest", "astral-sh/ruff"):
    entry = next(e for e in entries if e["context"]["repository"] == repository)
    payload = {
        "registration_id": entry["id"],
        "title": "Bug: collection fails in a local project",
        "body": "Synthetic smoke opening: collection fails when running a test file.",
    }
    if repository == "astral-sh/ruff":
        payload.update(
            title="Ruff bug report smoke",
            body="### Summary\n_No response_\n### Version\n_No response_",
            source_location={
                "commit": entry["context"]["revision"],
                "path": "does-not-exist-issue33.rs",
                "line": 1,
            },
        )
    response = call("/api/triage", payload)
    assert response["status"] == 200, response
    report = response["body"]
    trace = call(f"/api/traces/{report['trace_id']}")
    assert report["context"]["repository"] == repository
    assert trace["body"]["context"]["repository"] == repository
    if repository == "astral-sh/ruff":
        assert report["status"] == "partial" and not report["source_claims"]
        assert [d["name"] for d in report["missing_details"]] == ["Summary"]
    result["reports"].append(
        {"endpoint": "/api/triage", "response": response, "trace": trace}
    )
    output.write_text(json.dumps(result, indent=2) + "\n")

entry = next(e for e in entries if e["context"]["repository"] == "astral-sh/ruff")
response = call(
    "/api/agent/triage",
    {
        "registration_id": entry["id"],
        "title": "Ruff report smoke",
        "body": (
            "### Summary\nSynthetic smoke opening: the ruff command reports "
            "a failure.\n### Version\n0.17.6"
        ),
    },
)
assert response["status"] == 200, response
report = response["body"]
trace = call(f"/api/traces/{report['trace_id']}")
assert report["context"]["repository"] == "astral-sh/ruff"
assert len([e for e in trace["body"]["events"] if e["kind"] == "model"]) <= 4
result["reports"].append(
    {"endpoint": "/api/agent/triage", "response": response, "trace": trace}
)
result["source_inspection"] = call(
    f"/api/source?registration_id={entry['id']}&commit={entry['context']['revision']}&path=README.md&line=1"
)
assert result["source_inspection"]["status"] == 200
result["refresh"] = call(f"/api/repositories/{entry['id']}/refresh", {}, method="POST")
assert result["refresh"]["status"] == 200
result["remove"] = call(f"/api/repositories/{entry['id']}", method="DELETE")
assert result["remove"]["status"] == 204
result["removed_selection"] = call(
    "/api/triage", {"registration_id": entry["id"], "title": "Smoke", "body": ""}
)
assert result["removed_selection"]["status"] == 422
result["human_review"] = (
    "Pending explicit usefulness and semantic-support review; capability smoke only."
)
output.write_text(json.dumps(result, indent=2) + "\n")
print(
    json.dumps(
        {
            "restart_persistence": True,
            "reports": len(result["reports"]),
            "source_inspection": result["source_inspection"]["status"],
            "removed_selection": result["removed_selection"]["status"],
        }
    )
)
