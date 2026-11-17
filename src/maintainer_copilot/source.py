"""Bounded, read-only inspection of a pytest repository file at a commit."""

import re
from dataclasses import dataclass
from typing import Protocol
from urllib.error import URLError
from urllib.request import Request, urlopen

from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_SOURCE_BYTES = 262_144
MAX_EXCERPT_CHARS = 4_096
EXCERPT_RADIUS = 5


class SourceUnavailable(Exception):
    """The requested source could not be inspected reliably."""


class SourceLocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    path: str = Field(min_length=1, max_length=256)
    line: int = Field(gt=0, le=100_000)

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9._/-]+", value) or any(
            segment in {"", ".", ".."} for segment in value.split("/")
        ):
            raise ValueError("path must be a relative repository file path")
        return value

    @property
    def raw_url(self) -> str:
        return (
            "https://raw.githubusercontent.com/pytest-dev/pytest/"
            f"{self.commit}/{self.path}"
        )

    @property
    def source_url(self) -> str:
        return (
            "https://github.com/pytest-dev/pytest/blob/"
            f"{self.commit}/{self.path}#L{self.line}"
        )


class SourceExcerpt(BaseModel):
    commit: str
    path: str
    line: int
    start_line: int
    end_line: int
    lines: list[str]
    source_url: str


@dataclass(frozen=True)
class SourceEvidence:
    claim: str
    excerpt: SourceExcerpt
    passage: str


class SourceReader(Protocol):
    def get_excerpt(self, location: SourceLocation) -> SourceExcerpt: ...


class PublicRepositorySource:
    """Fetch only from the fixed public pytest repository, with a byte cap."""

    def get_excerpt(self, location: SourceLocation) -> SourceExcerpt:
        request = Request(location.raw_url, method="GET")
        try:
            with urlopen(request, timeout=5) as response:
                source = response.read(MAX_SOURCE_BYTES + 1)
            if len(source) > MAX_SOURCE_BYTES:
                raise SourceUnavailable("Source file exceeds the inspection limit.")
            lines = source.decode("utf-8").splitlines()
        except (OSError, URLError, UnicodeError) as exc:
            raise SourceUnavailable("Source file is unavailable.") from exc
        if location.line > len(lines):
            raise SourceUnavailable("Source line is unavailable.")
        start = max(1, location.line - EXCERPT_RADIUS)
        end = min(len(lines), location.line + EXCERPT_RADIUS)
        excerpt_lines = lines[start - 1 : end]
        if sum(len(line) + 1 for line in excerpt_lines) > MAX_EXCERPT_CHARS:
            raise SourceUnavailable("Source excerpt exceeds the inspection limit.")
        return SourceExcerpt(
            commit=location.commit,
            path=location.path,
            line=location.line,
            start_line=start,
            end_line=end,
            lines=excerpt_lines,
            source_url=location.source_url,
        )
