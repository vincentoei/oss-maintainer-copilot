"""Repository registration and selection at public application seams."""

import asyncio
import json
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx2
import pytest

from maintainer_copilot.web import app

SHA = "a" * 40
FORM = """name: Crash report
labels: [bug]
body:
  - type: textarea
    id: reproduction
    attributes:
      label: Reproduction
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version
    validations:
      required: true
"""


def request(method: str, path: str, **kwargs: Any) -> httpx2.Response:
    async def run() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(run())


def test_register_restart_and_remove_preserves_default_and_stable_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REPOSITORY_REGISTRY_PATH", str(tmp_path / "registry.sqlite3"))
    # Registration is exercised through HTTP; network is the replaceable boundary.
    import maintainer_copilot.registry as registry

    def fetch(req: Any, timeout: int) -> BytesIO:
        assert timeout == 5
        url = req.full_url
        if url.endswith("repos/astral-sh/ruff"):
            data: object = {
                "id": 545473891,
                "full_name": "astral-sh/ruff",
                "private": False,
                "visibility": "public",
                "has_issues": True,
                "default_branch": "main",
            }
        elif "/commits/" in url:
            data = {"sha": SHA}
        elif "/labels?" in url:
            data = [{"name": "bug"}, {"name": "question"}]
        elif "/contents/.github/ISSUE_TEMPLATE?" in url:
            data = [{"name": "bug.yaml", "type": "file"}]
        elif url.endswith("/bug.yaml"):
            return BytesIO(FORM.encode())
        else:
            return BytesIO(
                b"# Project documentation\nUse the command to reproduce crashes.\n"
            )
        return BytesIO(json.dumps(data).encode())

    monkeypatch.setattr(registry, "urlopen", fetch)
    added = request(
        "POST",
        "/api/repositories",
        json={"repository": "https://github.com/astral-sh/ruff"},
    )
    assert added.status_code == 200, added.text
    saved = added.json()
    assert saved["context"]["repository"] == "astral-sh/ruff"
    assert saved["context"]["revision"] == SHA
    again = request("POST", "/api/repositories", json={"repository": "astral-sh/ruff"})
    assert again.json()["id"] == saved["id"]
    # A new registry instance represents a restarted application, using the same file.
    restarted = registry.RepositoryRegistry(tmp_path / "registry.sqlite3")
    assert restarted.resolve(saved["id"]).repository == "astral-sh/ruff"
    listed = request("GET", "/api/repositories").json()
    assert len(listed) == 2
    assert request("DELETE", f"/api/repositories/{saved['id']}").status_code == 204
    assert (
        request(
            "POST",
            "/api/triage",
            json={"title": "Crash", "body": "", "registration_id": saved["id"]},
        ).status_code
        == 422
    )
    assert len(request("GET", "/api/repositories").json()) == 1


def test_web_exposes_registration_selection_refresh_and_removal() -> None:
    page = request("GET", "/")
    assert page.status_code == 200
    assert 'id="repository-select"' in page.text
    assert 'id="repository-add"' in page.text
    assert 'id="repository-refresh"' in page.text
    assert 'id="repository-remove"' in page.text
    assert "registration_id:" in page.text
    assert "report.context.repository" in page.text
    assert "report.context.revision" in page.text


@pytest.fixture
def public_github(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Synthetic public GitHub service: independent identities, mutable revisions."""
    import maintainer_copilot.registry as registry

    monkeypatch.setenv("REPOSITORY_REGISTRY_PATH", str(tmp_path / "registry.sqlite3"))
    state: dict[str, Any] = {
        "sha": SHA,
        "form": FORM,
        "labels": ["bug", "question"],
        "issues": True,
        "private": False,
        "failed": False,
        "calls": [],
        "filename": "bug.yaml",
    }
    identities = {"astral-sh/ruff": 1, "acme/widget": 2, "other/tool": 3}

    def fetch(req: Any, timeout: int) -> BytesIO:
        assert timeout == 5
        assert "Authorization" not in req.headers
        url = req.full_url
        state["calls"].append(url)
        if state["failed"]:
            raise OSError("offline")
        identity = next((name for name in identities if f"/{name}" in url), None)
        if identity is None:
            raise OSError("not found")
        if url == f"https://api.github.com/repos/{identity}":
            data: object = {
                "id": identities[identity],
                "full_name": identity,
                "private": state["private"],
                "visibility": "private" if state["private"] else "public",
                "has_issues": state["issues"],
                "default_branch": "main",
            }
        elif "/commits/" in url:
            data = {"sha": state["sha"]}
        elif "/labels?" in url:
            data = [{"name": name} for name in state["labels"]]
        elif "/contents/" in url:
            data = (
                [{"name": state["filename"], "type": "file"}] if state["form"] else []
            )
        elif url.endswith(state["filename"]):
            return BytesIO(state["form"].encode())
        else:
            return BytesIO(b"# Documentation\nThe widget command reproduces a crash.\n")
        return BytesIO(json.dumps(data).encode())

    monkeypatch.setattr(registry, "urlopen", fetch)
    monkeypatch.setattr("maintainer_copilot.documentation.urlopen", fetch)
    return state


def register(identity: str = "astral-sh/ruff", **configuration: Any) -> dict[str, Any]:
    response = request(
        "POST",
        "/api/repositories",
        json={"repository": identity, "configuration": configuration},
    )
    assert response.status_code == 200, response.text
    return dict(response.json())


class SelectingModel:
    def __init__(self, label: str | None = "bug") -> None:
        self.label = label
        self.requests: list[Any] = []

    def next_step(self, request: Any) -> object:
        self.requests.append(request)
        if request.issue.number and not request.observations:
            return {
                "tool": "search_earlier_issues",
                "arguments": {"issue_number": request.issue.number},
            }
        return {"tool": "finish", "arguments": {}}

    def generate(self, request: Any) -> object:
        self.requests.append(request)
        return {
            "issue_type": self.label,
            "issue_type_quote": "bug" if self.label else None,
            "reply_citation_ids": list(request.required_reply_ids),
        }


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_selected_generic_form_requires_only_declared_absent_fields(
    public_github: dict[str, Any],
    endpoint: str,
) -> None:
    from maintainer_copilot import IssueUnderReview, triage_issue
    from maintainer_copilot.registry import get_registry
    from maintainer_copilot.web import get_agent_client, get_model_client

    saved = register()
    model = SelectingModel()

    async def model_dependency() -> SelectingModel:
        return model

    app.dependency_overrides[get_model_client] = model_dependency
    app.dependency_overrides[get_agent_client] = model_dependency
    payload = {
        "registration_id": saved["id"],
        "title": "A bug in the widget command",
        "body": "### Reproduction\nwidget --crash\n### Version\n_No response_",
    }
    try:
        response = request("POST", endpoint, json=payload)
        assert response.status_code == 200, response.text
        report = response.json()
        assert report["issue_type"] == "bug"
        assert [d["name"] for d in report["missing_details"]] == ["Version"]
        assert report["context"]["registration_id"] == saved["id"]
        assert all("astral-sh/ruff" in c["source_url"] for c in report["citations"])
        trace = request("GET", f"/api/traces/{report['trace_id']}").json()
        assert trace["context"]["repository"] == "astral-sh/ruff"
        assert model.requests[-1].context.repository == "astral-sh/ruff"
        # Python selection uses the same persisted registration identity.
        python_report = triage_issue(
            IssueUnderReview.model_validate(payload),
            model_client=model,
            registry=get_registry(),
        )
        assert python_report.context.repository == "astral-sh/ruff"
        assert [d.name for d in python_report.missing_details] == ["Version"]
        payload["body"] = "### Reproduction\nwidget --crash\n### Version\n1.2.3"
        supplied = request("POST", endpoint, json=payload).json()
        assert supplied["missing_details"] == []
        # No form headings means applicability and requirements are unestablished.
        payload["body"] = "A detailed description of the bug or problem"
        unknown = request("POST", endpoint, json=payload).json()
        assert unknown["missing_details"] == []
        assert any(a["field"] == "missing_details" for a in unknown["abstentions"])
        assert "pytest" not in json.dumps(unknown)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize("identity", ["acme/widget", "other/tool"])
def test_generic_identities_abstain_on_unestablished_templates_and_labels(
    public_github: dict[str, Any],
    identity: str,
) -> None:
    public_github["form"] = ""
    public_github["labels"] = ["maintenance"]
    saved = register(identity)
    assert saved["context"]["status"] == "limited"
    from maintainer_copilot import IssueUnderReview, triage_issue

    report = triage_issue(
        IssueUnderReview(registration_id=saved["id"], title="bug", body=""),
        model_client=SelectingModel("type: bug"),
    )
    assert report.issue_type is None
    assert report.missing_details == []
    assert report.context.repository == identity
    assert any("validation" in a.reason for a in report.abstentions)


@pytest.mark.parametrize(
    "invalid",
    [
        "https://gitlab.com/acme/widget",
        "acme",
        "acme/widget/issues/1",
        "acme/..",
        "https://github.com/acme/widget?x=1",
    ],
)
def test_invalid_registration_creates_no_usable_entry(
    public_github: dict[str, Any], invalid: str
) -> None:
    response = request("POST", "/api/repositories", json={"repository": invalid})
    assert response.status_code == 422
    assert len(request("GET", "/api/repositories").json()) == 1
    assert public_github["calls"] == []


@pytest.mark.parametrize("failure", ["private", "failed"])
def test_private_nonexistent_and_inaccessible_registration_fails(
    public_github: dict[str, Any],
    failure: str,
) -> None:
    public_github[failure] = True
    response = request("POST", "/api/repositories", json={"repository": "acme/widget"})
    assert response.status_code == 422
    assert "public GitHub" in response.json()["detail"]
    assert len(request("GET", "/api/repositories").json()) == 1


def test_removed_default_requires_selection_even_after_restart(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot.registry import get_registry

    saved = register("acme/widget")
    assert request("DELETE", "/api/repositories/pytest-default").status_code == 204
    assert len(get_registry().list()) == 1
    for endpoint in ("/api/triage", "/api/agent/triage"):
        response = request("POST", endpoint, json={"title": "Bug", "body": ""})
        assert response.status_code == 422
        assert "No default repository" in response.json()["detail"]
        response = request(
            "POST",
            endpoint,
            json={"title": "Bug", "body": "", "registration_id": "unknown"},
        )
        assert response.status_code == 422
    assert (
        request(
            "POST",
            "/api/triage",
            json={"title": "Bug", "body": "", "registration_id": saved["id"]},
        ).status_code
        == 200
    )


def test_refresh_snapshot_failure_and_disabled_issues(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot.registry import get_registry

    saved = register()
    snapshot = get_registry().resolve(saved["id"])
    public_github["sha"] = "b" * 40
    updated = request("POST", f"/api/repositories/{saved['id']}/refresh")
    assert updated.status_code == 200
    assert updated.json()["context"]["revision"] == "b" * 40
    assert snapshot.revision == SHA
    public_github["failed"] = True
    failed = request("POST", f"/api/repositories/{saved['id']}/refresh").json()
    assert failed["context"]["status"] == "error"
    assert (
        request(
            "POST",
            "/api/triage",
            json={"title": "Bug", "body": "", "registration_id": saved["id"]},
        ).status_code
        == 422
    )
    public_github["failed"] = False
    public_github["issues"] = False
    disabled = register("acme/widget")
    assert disabled["context"]["status"] == "error"
    assert any("disabled" in error for error in disabled["context"]["errors"])


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_reused_issue_numbers_and_wrong_repository_evidence_are_isolated(
    public_github: dict[str, Any],
    endpoint: str,
) -> None:
    from datetime import UTC, datetime

    from maintainer_copilot.issue_search import IssueRecord
    from maintainer_copilot.web import (
        get_agent_client,
        get_issue_source,
        get_model_client,
    )

    registrations = [
        register(name) for name in ("astral-sh/ruff", "acme/widget", "other/tool")
    ]
    title = "Widget command crashes unexpectedly"
    body = "The widget command crashes unexpectedly on startup with a config file."
    wrong_repository = False
    model = SelectingModel(None)

    async def issues_dependency() -> Any:
        # The replaced service captures the current selected identity; each report
        # still validates the identity carried by its returned evidence.
        identity = active["context"]["repository"]

        class Issues:
            def get_issue(self, number: int) -> IssueRecord:
                return IssueRecord(
                    number, title, body, datetime(2025, 1, 2, tzinfo=UTC), identity
                )

            def search_issues(self, query: str, cutoff: Any) -> list[IssueRecord]:
                return [
                    IssueRecord(
                        7,
                        title,
                        body,
                        datetime(2025, 1, 1, tzinfo=UTC),
                        "pytest-dev/pytest" if wrong_repository else identity,
                    )
                ]

        return Issues()

    async def model_dependency() -> SelectingModel:
        return model

    app.dependency_overrides[get_issue_source] = issues_dependency
    app.dependency_overrides[get_model_client] = model_dependency
    app.dependency_overrides[get_agent_client] = model_dependency
    try:
        for active in registrations:
            response = request(
                "POST",
                endpoint,
                json={
                    "registration_id": active["id"],
                    "number": 20,
                    "title": title,
                    "body": body,
                },
            )
            assert response.status_code == 200, response.text
            report = response.json()
            assert report["related_issues"][0]["issue_number"] == 7
            assert active["context"]["repository"] in report["related_issues"][0]["url"]
            assert (
                report["duplicate_candidates"] == []
            )  # lexical overlap alone abstains
        wrong_repository = True
        rejected = request(
            "POST",
            endpoint,
            json={
                "registration_id": active["id"],
                "number": 20,
                "title": title,
                "body": body,
            },
        ).json()
        assert rejected["duplicate_candidates"] == rejected["related_issues"] == []
        assert rejected["status"] == "partial"
        assert all("pytest-dev" not in c["source_url"] for c in rejected["citations"])
    finally:
        app.dependency_overrides.clear()


def test_source_inspection_uses_selected_registration_and_rejects_wrong_repo(
    public_github: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    saved = register("acme/widget")
    urls: list[str] = []

    def fetch(req: Any, timeout: int) -> BytesIO:
        urls.append(req.full_url)
        return BytesIO(b"first line\nsecond line\n")

    monkeypatch.setattr("maintainer_copilot.source.urlopen", fetch)
    params = {
        "registration_id": saved["id"],
        "commit": SHA,
        "path": "src/main.rs",
        "line": 1,
    }
    response = request("GET", "/api/source", params=params)
    assert response.status_code == 200, response.text
    assert (
        response.json()["source_url"]
        == f"https://github.com/acme/widget/blob/{SHA}/src/main.rs#L1"
    )
    assert urls == [f"https://raw.githubusercontent.com/acme/widget/{SHA}/src/main.rs"]
    params["repository"] = "other/tool"
    assert request("GET", "/api/source", params=params).status_code == 422
    assert len(urls) == 1


def test_fixed_report_rejects_oversized_source_excerpt_from_reader(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot import IssueUnderReview, triage_issue
    from maintainer_copilot.source import SourceExcerpt, SourceLocation

    saved = register("other/tool")
    location = SourceLocation(
        repository="other/tool", commit=SHA, path="src/main.rs", line=1
    )

    class OversizedReader:
        def get_excerpt(self, location: SourceLocation) -> SourceExcerpt:
            return SourceExcerpt(
                commit=SHA,
                path=location.path,
                line=1,
                start_line=1,
                end_line=1,
                lines=["x" * 4097],
                source_url=location.source_url,
            )

    report = triage_issue(
        IssueUnderReview(
            registration_id=saved["id"], title="Bug", body="", source_location=location
        ),
        source_reader=OversizedReader(),
        model_client=SelectingModel(None),
    )
    assert report.source_claims == []
    assert any(a.field == "source_claims" for a in report.abstentions)


def test_refresh_during_report_keeps_its_original_context(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot.web import get_model_client

    saved = register()

    class RefreshingModel(SelectingModel):
        def generate(self, model_request: Any) -> object:
            public_github["sha"] = "c" * 40
            assert (
                request("POST", f"/api/repositories/{saved['id']}/refresh").status_code
                == 200
            )
            return super().generate(model_request)

    async def model_dependency() -> RefreshingModel:
        return RefreshingModel()

    app.dependency_overrides[get_model_client] = model_dependency
    try:
        report = request(
            "POST",
            "/api/triage",
            json={
                "registration_id": saved["id"],
                "title": "bug",
                "body": "### Reproduction\nwidget --crash\n### Version\n_No response_",
            },
        ).json()
        assert report["context"]["revision"] == SHA
        assert all(SHA in c["source_url"] for c in report["citations"])
        trace = request("GET", f"/api/traces/{report['trace_id']}").json()
        assert trace["context"]["revision"] == SHA
        current = request("GET", "/api/repositories").json()
        assert (
            next(entry for entry in current if entry["id"] == saved["id"])["context"][
                "revision"
            ]
            == "c" * 40
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_foreign_links_do_not_authorize_ci_and_model_cannot_author_sources(
    public_github: dict[str, Any],
    endpoint: str,
) -> None:
    from maintainer_copilot.web import get_agent_client, get_ci_source, get_model_client

    saved = register("other/tool")

    class NoCI:
        def get_checks(self, link: Any) -> Any:
            raise AssertionError("foreign links cannot authorize CI reads")

    async def ci_dependency() -> NoCI:
        return NoCI()

    class AuthoringModel(SelectingModel):
        def generate(self, request: Any) -> object:
            return {
                "issue_type": None,
                "issue_type_quote": None,
                "reply_citation_ids": [],
                "source_url": "https://github.com/pytest-dev/pytest/issues/7",
            }

    async def model_dependency() -> SelectingModel:
        return AuthoringModel(None)

    app.dependency_overrides[get_model_client] = model_dependency
    app.dependency_overrides[get_agent_client] = model_dependency
    app.dependency_overrides[get_ci_source] = ci_dependency
    try:
        report = request(
            "POST",
            endpoint,
            json={
                "registration_id": saved["id"],
                "title": "bug",
                "body": "See https://github.com/pytest-dev/pytest/pull/7",
            },
        ).json()
        assert report["ci_results"] == []
        assert report["issue_type"] is None
        assert report["status"] == "partial"
        assert any("validation" in a["reason"] for a in report["abstentions"])
        assert all(
            event["name"] != "get_ci_checks"
            for event in request("GET", f"/api/traces/{report['trace_id']}").json()[
                "events"
            ]
        )
    finally:
        app.dependency_overrides.clear()


def test_unknown_source_selection_and_mismatched_report_citations_fail(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot import IssueUnderReview, TriageReport, triage_issue

    saved = register()
    assert (
        request(
            "GET",
            "/api/source",
            params={
                "registration_id": "unknown",
                "commit": SHA,
                "path": "file.rs",
                "line": 1,
            },
        ).status_code
        == 422
    )
    report = triage_issue(
        IssueUnderReview(
            registration_id=saved["id"],
            title="bug",
            body="### Reproduction\n_No response_\n### Version\n1.0",
        ),
        model_client=SelectingModel(),
    )
    data = report.model_dump(mode="json")
    data["citations"][0]["source_url"] = (
        f"https://github.com/acme/widget/blob/{SHA}/template.yaml#L1"
    )
    with pytest.raises(ValueError, match="another repository"):
        TriageReport.model_validate(data)


def test_parallel_registration_and_reports_keep_context_separate(
    public_github: dict[str, Any],
) -> None:
    from concurrent.futures import ThreadPoolExecutor

    from maintainer_copilot import IssueUnderReview, triage_issue

    # Concurrent first-open initialization and duplicate adds are also idempotent.
    with ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(register, ["acme/widget"] * 4))
    assert len({entry["id"] for entry in entries}) == 1
    other = register("other/tool")

    def build(entry: dict[str, Any]) -> Any:
        return triage_issue(
            IssueUnderReview(
                registration_id=entry["id"],
                title="bug",
                body="### Reproduction\n_No response_\n### Version\n1.0",
            ),
            model_client=SelectingModel(),
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = list(pool.map(build, [entries[0], other] * 3))
    assert [r.context.repository for r in reports] == ["acme/widget", "other/tool"] * 3
    for report in reports:
        assert all(
            report.context.repository in str(c.source_url) for c in report.citations
        )


def test_unsupported_form_fields_and_preparation_limits_are_inspectable(
    public_github: dict[str, Any],
) -> None:
    public_github["form"] = (
        FORM + "  - type: dropdown\n    attributes:\n      label: Platform\n"
        "      options: [Linux, Windows]\n"
    )
    saved = register()
    assert saved["context"]["status"] == "limited"
    assert any("unsupported dropdown" in error for error in saved["context"]["errors"])
    assert len(public_github["calls"]) <= 12
    assert saved["context"]["templates"][0]["format"] == "issue-form"
    assert [field["name"] for field in saved["context"]["templates"][0]["fields"]] == [
        "Reproduction",
        "Version",
    ]


def test_markdown_headings_only_become_required_through_configuration(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot import IssueUnderReview, triage_issue

    public_github["filename"] = "bug.md"
    public_github["form"] = (
        "---\nname: Defect\nlabels: bug\n---\n"
        "### Reproduction\n### Expected behavior\n### Additional context\n"
    )
    saved = register("acme/widget")
    assert saved["context"]["status"] == "limited"
    configuration = {
        "markdown_required_fields": {".github/ISSUE_TEMPLATE/bug.md": ["Reproduction"]}
    }
    updated = request(
        "POST", f"/api/repositories/{saved['id']}/refresh", json=configuration
    )
    assert updated.status_code == 200
    assert updated.json()["context"]["status"] == "ready"
    body = (
        "### Reproduction\n_No response_\n### Expected behavior\n_No response_\n"
        "### Additional context\n_No response_"
    )
    report = triage_issue(
        IssueUnderReview(registration_id=saved["id"], title="bug", body=body),
        model_client=SelectingModel(),
    )
    assert [detail.name for detail in report.missing_details] == ["Reproduction"]
    assert (
        report.citations[0].source_url.path
        == f"/acme/widget/blob/{SHA}/.github/ISSUE_TEMPLATE/bug.md"
    )


def test_exact_form_heading_set_distinguishes_overlapping_templates(
    public_github: dict[str, Any],
) -> None:
    from maintainer_copilot import IssueUnderReview, triage_issue
    from maintainer_copilot.registry import get_registry

    saved = register()
    context = get_registry().resolve(saved["id"])
    shorter = context.templates[0].model_copy(
        update={"name": "Short form", "fields": context.templates[0].fields[:1]}
    )
    context = context.model_copy(update={"templates": (*context.templates, shorter)})
    report = triage_issue(
        IssueUnderReview(
            registration_id=saved["id"],
            title="bug",
            body="### Reproduction\n_No response_\n### Version\n1.0",
        ),
        model_client=SelectingModel(),
        context=context,
    )
    assert [detail.name for detail in report.missing_details] == ["Reproduction"]


@pytest.mark.parametrize(
    "body",
    [
        "<!--\n### Reproduction\n### Version\n-->",
        (
            "### Reproduction\n_No response_\n### Reproduction\nwidget --crash\n"
            "### Version\n1.0"
        ),
    ],
)
def test_untrusted_comments_and_duplicate_headings_cannot_establish_missing_fields(
    public_github: dict[str, Any],
    body: str,
) -> None:
    from maintainer_copilot import IssueUnderReview, triage_issue

    saved = register()
    report = triage_issue(
        IssueUnderReview(registration_id=saved["id"], title="bug", body=body),
        model_client=SelectingModel(),
    )
    assert report.missing_details == []
    assert any(a.field == "missing_details" for a in report.abstentions)


@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_selected_repository_reaches_actual_github_issue_transport(
    public_github: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    endpoint: str,
) -> None:
    from urllib.parse import parse_qs, urlsplit

    from maintainer_copilot.web import get_agent_client, get_model_client

    saved = register("acme/widget")
    urls: list[str] = []
    title = "Widget command crashes unexpectedly"
    body = "The widget command crashes unexpectedly on startup with a config file."

    def fetch(req: Any, timeout: int) -> BytesIO:
        assert timeout == 8
        urls.append(req.full_url)
        if "/search/issues?" in req.full_url:
            query = parse_qs(urlsplit(req.full_url).query)["q"][0]
            assert "repo:acme/widget" in query
            assert "repo:pytest-dev/pytest" not in query
            data = {
                "total_count": 1,
                "incomplete_results": False,
                "items": [
                    {
                        "number": 7,
                        "title": title,
                        "body": body,
                        "created_at": "2025-01-01T00:00:00Z",
                        "html_url": "https://github.com/acme/widget/issues/7",
                    }
                ],
            }
        else:
            assert req.full_url == "https://api.github.com/repos/acme/widget/issues/20"
            data = {
                "number": 20,
                "title": title,
                "body": body,
                "created_at": "2025-01-02T00:00:00Z",
                "html_url": "https://github.com/acme/widget/issues/20",
            }
        return BytesIO(json.dumps(data).encode())

    monkeypatch.setattr("maintainer_copilot.issue_search.urlopen", fetch)

    async def model_dependency() -> SelectingModel:
        return SelectingModel(None)

    app.dependency_overrides[get_agent_client] = model_dependency
    app.dependency_overrides[get_model_client] = model_dependency
    try:
        response = request(
            "POST",
            endpoint,
            json={
                "registration_id": saved["id"],
                "number": 20,
                "title": title,
                "body": body,
            },
        )
        assert response.status_code == 200, response.text
        assert (
            response.json()["related_issues"][0]["url"]
            == "https://github.com/acme/widget/issues/7"
        )
        assert len(urls) == 2
    finally:
        app.dependency_overrides.clear()
