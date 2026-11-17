"""Retrieve bounded, verifiable passages from approved public documentation."""

from collections.abc import Collection
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Protocol
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class DocumentationTopic:
    key: str
    url: str
    section: str
    passage: str
    claim: str
    relevance: str


@dataclass(frozen=True)
class DocumentationPassage:
    url: str
    text: str


@dataclass(frozen=True)
class DocumentationEvidence:
    claim: str
    passage: DocumentationPassage


class DocumentationSource(Protocol):
    def get_passage(self, topic: DocumentationTopic) -> DocumentationPassage | None: ...


class DocumentationError(Exception):
    """Public pytest documentation could not be read reliably."""


class _SectionParagraph(HTMLParser):
    def __init__(self, section: str) -> None:
        super().__init__()
        self.section = section
        self.depth = 0
        self.in_paragraph = False
        self.parts: list[str] = []
        self.paragraph: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "section":
            if self.depth:
                self.depth += 1
            elif dict(attrs).get("id") == self.section:
                self.depth = 1
        elif self.depth and tag == "p" and self.paragraph is None:
            self.in_paragraph = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "p" and self.in_paragraph:
            self.paragraph = " ".join("".join(self.parts).split())
            self.in_paragraph = False
        elif tag == "section" and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.in_paragraph:
            self.parts.append(data)


class PublicDocumentationSource:
    def __init__(self, approved_topics: Collection[DocumentationTopic]) -> None:
        self.approved_topics = frozenset(approved_topics)

    def get_passage(self, topic: DocumentationTopic) -> DocumentationPassage | None:
        if topic not in self.approved_topics:
            return None
        try:
            request = Request(
                topic.url.split("#", 1)[0],
                headers={"User-Agent": "oss-maintainer-copilot"},
            )
            with urlopen(request, timeout=8) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                raise ValueError("documentation page exceeds size limit")
            parser = _SectionParagraph(topic.section)
            parser.feed(body.decode("utf-8"))
        except (URLError, TimeoutError, ValueError, UnicodeError, OSError) as exc:
            raise DocumentationError("pytest documentation is unavailable.") from exc
        if parser.paragraph is None or topic.passage not in parser.paragraph:
            return None
        return DocumentationPassage(url=topic.url, text=topic.passage)
