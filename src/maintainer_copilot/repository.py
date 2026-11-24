"""Immutable target-repository context and profile policy for one report."""

import re
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator

from maintainer_copilot import pytest_profile
from maintainer_copilot.documentation import DocumentationTopic
from maintainer_copilot.follow_up import FollowUp, supported_follow_up
from maintainer_copilot.label_evidence import quote_supports_label
from maintainer_copilot.templates import markdown_headings, without_comments

DEFAULT_REPOSITORY = pytest_profile.REPOSITORY
DEFAULT_GITHUB_ID = pytest_profile.GITHUB_ID
DEFAULT_REGISTRATION_ID = "pytest-default"


def repository_identity(value: str) -> str:
    """Accept an exact GitHub repository URL or owner/name, never arbitrary URLs."""
    value = value.strip()
    if value.startswith("https://github.com/"):
        parsed = urlsplit(value)
        if parsed.query or parsed.fragment or parsed.netloc != "github.com":
            raise ValueError("Use a GitHub repository URL without query or fragment.")
        value = parsed.path.strip("/")
    if value.endswith(".git"):
        value = value[:-4]
    if not re.fullmatch(
        r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9_.-]{1,100}", value
    ):
        raise ValueError("Use https://github.com/owner/repo or owner/repo.")
    if value.split("/")[1] in {".", ".."}:
        raise ValueError("Invalid repository name.")
    return value


class TemplateField(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    name: str
    line: int = Field(gt=0)
    required: bool = False


class PreparedTemplate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    name: str
    path: str
    format: Literal["markdown", "issue-form"]
    labels: tuple[str, ...] = ()
    fields: tuple[TemplateField, ...] = ()


class DetailRequest(BaseModel):
    name: str
    request: str
    url: str
    description: str


class RepositoryContext(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    registration_id: str
    repository: str
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    profile: Literal["pytest", "generic"] = "generic"
    status: Literal["ready", "limited", "error"] = "limited"
    errors: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    type_cues: tuple[tuple[str, str], ...] = ()
    templates: tuple[PreparedTemplate, ...] = ()
    documentation: tuple[DocumentationTopic, ...] = ()
    prepared_at: str = ""
    structured_templates: bool = True

    @field_validator("repository")
    @classmethod
    def validate_repository(cls, value: str) -> str:
        if repository_identity(value) != value:
            raise ValueError("repository must be a canonical owner/repo identity")
        return value

    @property
    def display_name(self) -> str:
        return (
            pytest_profile.DISPLAY_NAME if self.profile == "pytest" else self.repository
        )

    @property
    def type_labels(self) -> tuple[str, ...]:
        return tuple(label for label, _ in self.type_cues)

    def owns_url(self, url: str) -> bool:
        parsed = urlsplit(url)
        if parsed.scheme == "https" and parsed.netloc == "github.com":
            return parsed.path.startswith(f"/{self.repository}/")
        return self.profile == "pytest" and pytest_profile.owns_documentation_url(url)

    def relevant_topics(self, title: str, body: str) -> list[DocumentationTopic]:
        return [
            topic
            for topic in self.documentation
            if re.search(topic.relevance, f"{title}\n{body}", re.I)
        ]

    def missing_details(self, title: str, body: str) -> list[DetailRequest] | None:
        if not self.structured_templates:
            return None
        if self.profile == "pytest":
            return pytest_profile.profile_details(title, body, self.revision)
        # Match the actual rendered form's headings, not inferred bug/feature words.
        content = without_comments(body)
        sections = markdown_headings(content)
        heading_list = [section.name for section in sections]
        headings = set(heading_list)
        if len(headings) != len(heading_list):
            return None
        matches = [
            template
            for template in self.templates
            if template.fields and {f.name for f in template.fields}.issubset(headings)
        ]
        exact = [
            template
            for template in matches
            if {f.name for f in template.fields} == headings
        ]
        if exact:
            matches = exact
        if len(matches) != 1:
            return None
        template = matches[0]
        missing = []
        for field in template.fields:
            if not field.required:
                continue
            section_index = next(
                index
                for index, section in enumerate(sections)
                if section.name == field.name
            )
            section = sections[section_index]
            next_start = (
                sections[section_index + 1].start
                if section_index + 1 < len(sections)
                else len(content)
            )
            answer = content[section.end : next_start].strip()
            # Arbitrary prose outside sections cannot prove a section is missing.
            if answer and answer.lower() not in {
                "_no response_",
                "no response",
                "todo",
                "tbd",
            }:
                continue
            missing.append(
                DetailRequest(
                    name=field.name,
                    request=f"the required {field.name} field",
                    url=f"https://github.com/{self.repository}/blob/{self.revision}/{template.path}#L{field.line}",
                    description=(
                        f"{self.repository} {template.name} template: {field.name}"
                    ),
                )
            )
        return missing

    def follow_up(self, body: str) -> FollowUp | None:
        return supported_follow_up(body) if self.profile == "pytest" else None

    def quote_supports_label(self, label: str, quote: str, issue_text: str) -> bool:
        return quote_supports_label(dict(self.type_cues), label, quote, issue_text)

    def search_query(self, title: str, body: str) -> str | None:
        from maintainer_copilot.issue_search import search_query

        excluded = (
            pytest_profile.SEARCH_STOPWORDS if self.profile == "pytest" else frozenset()
        )
        return search_query(title, body, excluded=excluded)

    def assess_match(
        self, title: str, body: str, candidate: "IssueRecord"
    ) -> "Match | None":
        from maintainer_copilot.issue_search import assess_match

        return assess_match(
            title, body, candidate, project_connections=self.profile == "pytest"
        )


# Imports are only needed for annotations, avoiding a retrieval/context cycle.
from typing import TYPE_CHECKING  # noqa: E402

if TYPE_CHECKING:
    from maintainer_copilot.issue_search import IssueRecord, Match


def legacy_context(
    *,
    revision: str | None = None,
    documentation_topics: tuple[DocumentationTopic, ...] | None = None,
    structured_templates: bool = True,
) -> RepositoryContext:
    return RepositoryContext(
        registration_id=DEFAULT_REGISTRATION_ID,
        repository=DEFAULT_REPOSITORY,
        revision=revision or pytest_profile.TEMPLATE_REVISION,
        profile="pytest",
        status="ready",
        templates=tuple(
            PreparedTemplate(
                name=name,
                path=f".github/ISSUE_TEMPLATE/{filename}",
                format="markdown",
                fields=tuple(
                    TemplateField(name=detail.name, line=detail.line, required=True)
                    for detail in details
                ),
            )
            for name, filename, details in pytest_profile.PREPARED_TEMPLATES
        ),
        labels=pytest_profile.TYPE_LABELS,
        type_cues=tuple(pytest_profile.TYPE_EVIDENCE_CUES.items()),
        documentation=documentation_topics
        if documentation_topics is not None
        else pytest_profile.DOCUMENTATION_TOPICS,
        structured_templates=structured_templates,
    )
