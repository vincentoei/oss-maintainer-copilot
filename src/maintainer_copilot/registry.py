"""Local registrations and bounded, anonymous public-GitHub preparation."""

import json
import os
import re
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from threading import BoundedSemaphore
from typing import Any, Literal
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
from uuid import NAMESPACE_URL, uuid5

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from maintainer_copilot.documentation import DocumentationTopic
from maintainer_copilot.repository import (
    DEFAULT_GITHUB_ID,
    DEFAULT_REGISTRATION_ID,
    PreparedTemplate,
    RepositoryContext,
    TemplateField,
    legacy_context,
    repository_identity,
)
from maintainer_copilot.templates import markdown_headings, without_comments

MAX_FETCHES = 12
MAX_BYTES = 262_144
MAX_TEMPLATES = 4
MAX_DOCUMENTS = 3
MAX_PASSAGE_CHARS = 2_000
# Four preparations per process, each sequential. Acquisition is bounded too.
_PREPARATIONS = BoundedSemaphore(4)


class RegistrationError(ValueError):
    """An actionable setup/selection error, never an implicit fallback."""


class RepositoryConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    documentation_paths: tuple[str, ...] = (
        "README.md",
        "CONTRIBUTING.md",
        "docs/README.md",
    )
    # Markdown requirements must be declared explicitly; headings alone are not
    # requirements.
    markdown_required_fields: dict[str, tuple[str, ...]] = Field(default_factory=dict)
    type_labels: tuple[str, ...] = ()

    @field_validator("documentation_paths")
    @classmethod
    def validate_paths(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if len(values) > MAX_DOCUMENTS:
            raise ValueError("At most three documentation paths are supported.")
        for value in values:
            validate_path(value)
        return values

    @field_validator("markdown_required_fields")
    @classmethod
    def validate_mappings(
        cls, values: dict[str, tuple[str, ...]]
    ) -> dict[str, tuple[str, ...]]:
        if len(values) > MAX_TEMPLATES:
            raise ValueError("At most four template mappings are supported.")
        for path, headings in values.items():
            validate_path(path)
            if not path.startswith(".github/ISSUE_TEMPLATE/") or len(headings) > 20:
                raise ValueError(
                    "Use issue-template paths and at most twenty headings."
                )
        return values

    @field_validator("type_labels")
    @classmethod
    def validate_labels(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if len(values) > 20 or any(not 1 <= len(label) <= 100 for label in values):
            raise ValueError("Use at most twenty labels, each up to 100 characters.")
        return values


def validate_path(path: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9._/-]{1,256}", path) or any(
        part in {"", ".", ".."} for part in path.split("/")
    ):
        raise ValueError("Use a relative repository file path.")


class RegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    repository: str = Field(max_length=256)
    configuration: RepositoryConfiguration = Field(
        default_factory=RepositoryConfiguration
    )


class Registration(BaseModel):
    id: str
    github_id: int | None = None
    configuration: RepositoryConfiguration = Field(
        default_factory=RepositoryConfiguration
    )
    context: RepositoryContext
    is_default: bool = False


class _Preparation:
    def __init__(self) -> None:
        self.calls = 0
        self.errors: list[str] = []

    def read(self, url: str, *, optional: bool = False) -> bytes | None:
        if self.calls >= MAX_FETCHES:
            self.errors.append(
                "Fetch budget exhausted; refresh with fewer configured sources."
            )
            return None
        self.calls += 1
        # Deliberately anonymous: credentials must not make private
        # repositories eligible.
        request = Request(
            url,
            headers={
                "User-Agent": "oss-maintainer-copilot",
                "Accept": "application/vnd.github+json",
            },
        )
        try:
            with urlopen(request, timeout=5) as response:
                body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError("Response exceeds 256 KiB.")
            return bytes(body)
        except HTTPError as exc:
            if exc.code == 404 and optional:
                return None
        except (OSError, ValueError):
            pass
        self.errors.append(
            f"Unavailable or oversized context: {url}. Check public access and refresh."
        )
        return None

    def json(self, url: str, *, optional: bool = False) -> Any:
        body = self.read(url, optional=optional)
        if body is None:
            return None
        try:
            return json.loads(body)
        except ValueError:
            self.errors.append(f"Invalid JSON context: {url}. Refresh later.")
            return None

    def text(self, url: str) -> str | None:
        body = self.read(url, optional=True)
        if body is None:
            return None
        try:
            return body.decode("utf-8")
        except UnicodeError:
            self.errors.append(f"Unsupported non-UTF-8 context: {url}.")
            return None


def _template(
    path: str, text: str, config: RepositoryConfiguration, errors: list[str]
) -> PreparedTemplate | None:
    kind: Literal["markdown", "issue-form"]
    try:
        if path.endswith(".md"):
            parts = text.split("---", 2)
            metadata = (
                yaml.safe_load(parts[1])
                if text.startswith("---\n") and len(parts) == 3
                else {}
            )
            if not isinstance(metadata, dict):
                raise ValueError("Invalid Markdown front matter")
            headings = [
                (heading.name, heading.line)
                for heading in markdown_headings(without_comments(text))
            ]
            if len(headings) > 20:
                errors.append(
                    f"{path}: exceeds twenty supported headings; template omitted, "
                    "including its requirements."
                )
                return None
            required = config.markdown_required_fields.get(path, ())
            if not set(required).issubset({name for name, _ in headings}):
                raise ValueError("Configured required headings are unavailable")
            if not required:
                errors.append(
                    f"{path}: Markdown headings do not establish required "
                    f"details; configure markdown_required_fields."
                )
            fields = tuple(
                TemplateField(name=name, line=line, required=name in required)
                for name, line in headings
            )
            kind = "markdown"
        else:
            metadata = yaml.safe_load(text)
            if not isinstance(metadata, dict) or not isinstance(
                metadata.get("body"), list
            ):
                raise ValueError("Unsupported issue-form structure")
            field_list = []
            for item in metadata["body"]:
                if not isinstance(item, dict):
                    raise ValueError("Unsupported issue-form field")
                if item.get("type") == "markdown":
                    continue
                if item.get("type") not in {"input", "textarea"}:
                    errors.append(
                        f"{path}: unsupported {item.get('type')} field; "
                        f"missing-detail detection abstains for it."
                    )
                    continue
                attrs = item.get("attributes", {})
                label = attrs.get("label") if isinstance(attrs, dict) else None
                validations = item.get("validations", {})
                if not isinstance(label, str) or not isinstance(validations, dict):
                    raise ValueError("Field label/validation unavailable")
                # Citation points to the exact label declaration in the pinned form.
                lines = [
                    n
                    for n, line in enumerate(text.splitlines(), 1)
                    if re.match(r"\s*label:\s*", line) and label in line
                ]
                if len(lines) != 1:
                    raise ValueError("Ambiguous form label location")
                field_list.append(
                    TemplateField(
                        name=label,
                        line=lines[0],
                        required=validations.get("required") is True,
                    )
                )
            if len(field_list) > 20:
                raise ValueError("More than twenty form fields")
            fields = tuple(field_list)
            kind = "issue-form"
        if not fields or len({f.name for f in fields}) != len(fields):
            raise ValueError("No unambiguous supported fields")
        labels = metadata.get("labels", [])
        if isinstance(labels, str):
            labels = [label.strip() for label in labels.split(",") if label.strip()]
        if not isinstance(labels, list) or any(
            not isinstance(label, str) for label in labels
        ):
            raise ValueError("Unsupported template labels")
        return PreparedTemplate(
            name=str(metadata.get("name", path)),
            path=path,
            format=kind,
            fields=fields,
            labels=tuple(labels),
        )
    except (ValueError, yaml.YAMLError, RecursionError):
        errors.append(
            f"{path}: unsupported template; inspect it or refine configuration."
        )
        return None


def prepare_repository(
    value: str, config: RepositoryConfiguration, *, registration_id: str | None = None
) -> tuple[int, RepositoryContext]:
    try:
        identity = repository_identity(value)
    except ValueError as exc:
        raise RegistrationError(str(exc)) from exc
    if not _PREPARATIONS.acquire(timeout=5):
        raise RegistrationError("Repository preparation is busy; retry later.")
    try:
        return _prepare(identity, config, registration_id)
    finally:
        _PREPARATIONS.release()


def _prepare(
    identity: str, config: RepositoryConfiguration, registration_id: str | None
) -> tuple[int, RepositoryContext]:
    prep = _Preparation()
    metadata = prep.json(f"https://api.github.com/repos/{identity}")
    if (
        not isinstance(metadata, dict)
        or metadata.get("private") is not False
        or metadata.get("visibility", "public") != "public"
    ):
        raise RegistrationError(
            "Repository is nonexistent, inaccessible or private. Use a public "
            "GitHub repository."
        )
    github_id = metadata.get("id")
    canonical = metadata.get("full_name")
    branch = metadata.get("default_branch")
    if (
        type(github_id) is not int
        or not isinstance(canonical, str)
        or not isinstance(branch, str)
    ):
        raise RegistrationError(
            "GitHub did not return a canonical repository identity and default branch."
        )
    canonical = repository_identity(canonical)
    api = f"https://api.github.com/repos/{canonical}"
    commit = prep.json(f"{api}/commits/{quote(branch, safe='')}")
    sha = commit.get("sha") if isinstance(commit, dict) else None
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RegistrationError(
            "Cannot resolve the repository revision; it may be empty. Refresh "
            "after a public commit exists."
        )
    raw = f"https://raw.githubusercontent.com/{canonical}/{sha}"
    labels_data = prep.json(f"{api}/labels?per_page=100")
    labels: tuple[str, ...] = ()
    if isinstance(labels_data, list) and all(
        isinstance(item, dict) and isinstance(item.get("name"), str)
        for item in labels_data
    ):
        labels = tuple(item["name"] for item in labels_data)
        if len(labels) >= 100:
            prep.errors.append(
                "Labels capped at 100; type suggestions use only verified "
                "available labels."
            )
    else:
        prep.errors.append("Labels unavailable; type suggestions abstain.")
    templates: list[PreparedTemplate] = []
    if metadata.get("has_issues") is not True:
        prep.errors.append(
            "Issues are disabled; enable issues on GitHub to triage existing issues."
        )
    listing = prep.json(
        f"{api}/contents/.github/ISSUE_TEMPLATE?ref={sha}", optional=True
    )
    if isinstance(listing, list):
        names = sorted(
            item["name"]
            for item in listing
            if isinstance(item, dict)
            and item.get("type") == "file"
            and isinstance(item.get("name"), str)
            and item["name"].endswith((".md", ".yml", ".yaml"))
            and item["name"] != "config.yml"
        )
        if len(names) > MAX_TEMPLATES:
            prep.errors.append(
                "Templates capped at four; additional templates omitted."
            )
        for name in names[:MAX_TEMPLATES]:
            path = f".github/ISSUE_TEMPLATE/{name}"
            try:
                validate_path(path)
            except ValueError:
                prep.errors.append("Unsupported template path omitted.")
                continue
            text = prep.text(f"{raw}/{path}")
            if text is None:
                prep.errors.append(f"Template unavailable: {path}.")
            elif template := _template(path, text, config, prep.errors):
                templates.append(template)
    if not templates:
        prep.errors.append(
            "No supported issue templates. Missing-detail detection abstains; "
            "configure supported templates or use source inspection."
        )
    documents = []
    for path in config.documentation_paths:
        text = prep.text(f"{raw}/{path}")
        if text is None:
            prep.errors.append(
                f"Documentation unavailable: {path}; configure an existing path "
                f"and refresh."
            )
            continue
        # One bounded extractive passage per file; expose omissions rather
        # than truncating.
        selected: list[str] = []
        for line in text.splitlines()[:20]:
            if (
                sum(len(value) + 1 for value in selected) + len(line)
                > MAX_PASSAGE_CHARS
            ):
                break
            selected.append(line)
        if not selected:
            prep.errors.append(f"Documentation has no bounded passage: {path}.")
            continue
        if len(selected) < len(text.splitlines()):
            prep.errors.append(
                f"Documentation excerpt only: {path}, lines 1-{len(selected)}; "
                f"remaining content omitted."
            )
        passage = "\n".join(selected)
        words = sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9_]{4,}", passage.lower())))[
            :60
        ]
        documents.append(
            DocumentationTopic(
                key=path,
                url=f"https://github.com/{canonical}/blob/{sha}/{path}#L1-L{len(selected)}",
                section="",
                passage=passage,
                claim=f"{canonical} {path} contains the cited passage.",
                relevance=r"\b(?:" + "|".join(map(re.escape, words)) + r")\b"
                if words
                else r"(?!)",
            )
        )
    selected_labels = set(config.type_labels) | {
        label for template in templates for label in template.labels
    }
    cues = tuple(
        (label, r"\b" + re.escape(label) + r"\b")
        for label in sorted(selected_labels)
        if label in labels
    )
    if selected_labels - set(labels):
        prep.errors.append(
            "Configured/template type labels absent from available labels; "
            "unsupported labels omitted."
        )
    if not cues:
        prep.errors.append(
            "No established type-label mapping; type suggestions abstain. "
            "Configure type_labels to refine."
        )
    return github_id, RepositoryContext(
        registration_id=registration_id
        or str(uuid5(NAMESPACE_URL, f"github-repository:{github_id}")),
        repository=canonical,
        revision=sha,
        templates=tuple(templates),
        labels=labels,
        type_cues=cues,
        documentation=tuple(documents),
        status="error"
        if metadata.get("has_issues") is not True
        else "limited"
        if prep.errors
        else "ready",
        errors=tuple(prep.errors),
        prepared_at=datetime.now(UTC).isoformat(),
    )


class RepositoryRegistry:
    """Transactional snapshots; refresh replaces future requests' context only."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                "CREATE TABLE IF NOT EXISTS registrations (id TEXT PRIMARY "
                "KEY, github_id INTEGER UNIQUE, data TEXT NOT NULL)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)"
            )
            if (
                db.execute(
                    "SELECT value FROM settings WHERE key='initialized'"
                ).fetchone()
                is None
            ):
                seed = Registration(
                    id=DEFAULT_REGISTRATION_ID,
                    github_id=DEFAULT_GITHUB_ID,
                    context=legacy_context(),
                    is_default=True,
                )
                db.execute(
                    "INSERT INTO registrations VALUES (?, ?, ?)",
                    (seed.id, seed.github_id, seed.model_dump_json()),
                )
                db.execute("INSERT INTO settings VALUES ('initialized', '1')")

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path, timeout=5)
        try:
            with db:
                yield db
        finally:
            db.close()

    def list(self) -> list[Registration]:
        with self._connect() as db:
            return [
                Registration.model_validate_json(row[0])
                for row in db.execute("SELECT data FROM registrations ORDER BY id")
            ]

    def get(self, registration_id: str) -> Registration:
        with self._connect() as db:
            row = db.execute(
                "SELECT data FROM registrations WHERE id=?", (registration_id,)
            ).fetchone()
        if row is None:
            raise RegistrationError(
                "Unknown or removed repository registration. Select a "
                "registered repository."
            )
        return Registration.model_validate_json(row[0])

    def resolve(self, registration_id: str | None = None) -> RepositoryContext:
        if registration_id is None:
            defaults = [entry for entry in self.list() if entry.is_default]
            if not defaults:
                raise RegistrationError(
                    "No default repository. Register and explicitly select a "
                    "repository."
                )
            registration_id = defaults[0].id
        context = self.get(registration_id).context
        if context.status == "error":
            raise RegistrationError(
                "Repository context is in error. Inspect preparation errors "
                "and refresh."
            )
        return context

    def add(
        self, repository: str, configuration: RepositoryConfiguration | None = None
    ) -> Registration:
        config = configuration or RepositoryConfiguration()
        github_id, context = prepare_repository(repository, config)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT data FROM registrations WHERE github_id=?", (github_id,)
            ).fetchone()
            # The seeded adapter also has a stable identity when registered by URL.
            if row is None:
                row = next(
                    (
                        (entry.model_dump_json(),)
                        for entry in self.list()
                        if entry.context.repository.lower()
                        == context.repository.lower()
                    ),
                    None,
                )
            if row is not None:
                return Registration.model_validate_json(row[0])
            entry = Registration(
                id=context.registration_id,
                github_id=github_id,
                context=context,
                configuration=config,
            )
            db.execute(
                "INSERT INTO registrations VALUES (?, ?, ?)",
                (entry.id, github_id, entry.model_dump_json()),
            )
        return entry

    def refresh(
        self, registration_id: str, configuration: RepositoryConfiguration | None = None
    ) -> Registration:
        previous = self.get(registration_id)
        config = configuration or previous.configuration
        try:
            github_id, context = prepare_repository(
                previous.context.repository, config, registration_id=previous.id
            )
            if previous.github_id is not None and github_id != previous.github_id:
                raise RegistrationError(
                    "Repository identity changed; remove and register explicitly."
                )
            if previous.context.profile == "pytest":
                # The legacy adapter has verified, revision-specific requirements. A
                # fresh generic view cannot silently transplant those requirements.
                context = context.model_copy(
                    update={
                        "errors": context.errors
                        + (
                            "Refreshed context uses generic template "
                            "interpretation; historical pytest adapter "
                            "remains pinned for replay.",
                        ),
                        "status": "limited",
                    }
                )
            updated = previous.model_copy(
                update={
                    "github_id": github_id,
                    "context": context,
                    "configuration": config,
                }
            )
        except RegistrationError as exc:
            updated = previous.model_copy(
                update={
                    "context": previous.context.model_copy(
                        update={"status": "error", "errors": (str(exc),)}
                    )
                }
            )
        with self._connect() as db:
            changed = db.execute(
                "UPDATE registrations SET github_id=?, data=? WHERE id=?",
                (updated.github_id, updated.model_dump_json(), registration_id),
            ).rowcount
            if not changed:
                raise RegistrationError("Registration removed during refresh.")
        return updated

    def remove(self, registration_id: str) -> None:
        with self._connect() as db:
            if not db.execute(
                "DELETE FROM registrations WHERE id=?", (registration_id,)
            ).rowcount:
                raise RegistrationError("Unknown or removed repository registration.")


def get_registry() -> RepositoryRegistry:
    return RepositoryRegistry(
        os.getenv("REPOSITORY_REGISTRY_PATH", ".local/repositories.sqlite3")
    )
