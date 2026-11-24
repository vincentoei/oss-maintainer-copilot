"""Bounded Markdown structure used for template applicability and citations."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Heading:
    name: str
    line: int
    start: int
    end: int


def without_comments(text: str) -> str:
    # Retain newlines so template citations keep their original line numbers.
    return re.sub(
        r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S
    )


def markdown_headings(text: str) -> list[Heading]:
    """Recognize ATX sections, excluding indented and fenced code examples."""
    headings = []
    fence: tuple[str, int] | None = None
    offset = 0
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        start = offset
        offset += len(line)
        if fence is not None:
            if re.fullmatch(
                rf" {{0,3}}{re.escape(fence[0])}{{{fence[1]},}}[ \t]*\r?\n?", line
            ):
                fence = None
            continue
        if opening := re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", line):
            marker, info = opening.groups()
            if marker[0] != "`" or "`" not in info:
                fence = marker[0], len(marker)
                continue
        if match := re.match(r"^#{1,6}[ \t]+(.+?)[ \t]*\r?\n?$", line):
            name = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(1)).strip()
            headings.append(Heading(name, number, start, offset))
    return headings
