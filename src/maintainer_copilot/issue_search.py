"""Read public repository issues and identify plausible earlier matches."""

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, Protocol
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from maintainer_copilot import pytest_profile
from maintainer_copilot.repository import DEFAULT_REPOSITORY, repository_identity


class IssueSearchError(Exception):
    """GitHub issue evidence could not be read reliably."""


@dataclass(frozen=True)
class IssueRecord:
    number: int
    title: str
    body: str
    created_at: datetime

    repository: str = DEFAULT_REPOSITORY

    @property
    def url(self) -> str:
        return f"https://github.com/{self.repository}/issues/{self.number}"


class IssueSource(Protocol):
    def get_issue(self, number: int) -> IssueRecord: ...

    def search_issues(
        self, query: str, created_before: datetime
    ) -> list[IssueRecord]: ...


class GitHubIssueSource:
    """The two read-only GitHub calls needed for a historical issue search."""

    repository = DEFAULT_REPOSITORY

    def __init__(self, repository: str = DEFAULT_REPOSITORY) -> None:
        self.repository = repository_identity(repository)

    def _get_json(self, url: str) -> dict[str, object]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "oss-maintainer-copilot",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token := os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
        try:
            with urlopen(Request(url, headers=headers), timeout=8) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                raise ValueError("GitHub response exceeds the size limit")
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("expected an object")
            return data
        except (URLError, TimeoutError, ValueError, OSError) as exc:
            raise IssueSearchError("GitHub issue search is unavailable.") from exc

    def get_issue(self, number: int) -> IssueRecord:
        data = self._get_json(
            f"https://api.github.com/repos/{self.repository}/issues/{number}"
        )
        if "pull_request" in data:
            raise IssueSearchError("The supplied number refers to a pull request.")
        try:
            record = _record(data, self.repository)
        except (KeyError, TypeError, ValueError) as exc:
            raise IssueSearchError("GitHub returned incomplete issue data.") from exc
        if record.number != number:
            raise IssueSearchError("GitHub returned a different issue number.")
        return record

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        cutoff = created_before.astimezone(UTC).isoformat(timespec="seconds")
        search = (
            f"{query} repo:{self.repository} is:issue in:title,body created:<{cutoff}"
        )
        collected: list[dict[str, object]] = []
        total_count: int | None = None
        page = 1
        while True:
            url = "https://api.github.com/search/issues?" + urlencode(
                {"q": search, "per_page": 100, "page": page}
            )
            data = self._get_json(url)
            count = data.get("total_count")
            items = data.get("items")
            if (
                data.get("incomplete_results")
                or type(count) is not int
                or not isinstance(items, list)
                or any(not isinstance(item, dict) for item in items)
            ):
                raise IssueSearchError("GitHub returned incomplete search results.")
            if count < 0:
                raise IssueSearchError("GitHub returned incomplete search results.")
            if count > 1000:
                raise IssueSearchError("GitHub search exceeds its 1,000-result limit.")
            if total_count is not None and count != total_count:
                raise IssueSearchError("GitHub search changed during pagination.")
            total_count = count
            collected.extend(items)
            if len(collected) > count:
                raise IssueSearchError("GitHub returned incomplete search results.")
            if len(collected) == count:
                break
            if not items or page >= 10:
                raise IssueSearchError("GitHub returned incomplete search results.")
            page += 1
        try:
            return [
                _record(item, self.repository)
                for item in collected
                if "pull_request" not in item
            ]
        except (KeyError, TypeError, ValueError) as exc:
            raise IssueSearchError("GitHub returned incomplete issue data.") from exc


def _record(
    data: dict[str, object], repository: str = DEFAULT_REPOSITORY
) -> IssueRecord:
    expected_url = f"https://github.com/{repository}/issues/{data['number']}"
    if data.get("html_url", expected_url) != expected_url:
        raise ValueError("Issue URL belongs to another repository")
    created_at = datetime.fromisoformat(str(data["created_at"]).replace("Z", "+00:00"))
    return IssueRecord(
        repository=repository,
        number=int(str(data["number"])),
        title=str(data["title"]),
        body=str(data.get("body") or ""),
        created_at=created_at,
    )


_STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "before",
    "bug",
    "can",
    "does",
    "during",
    "error",
    "fails",
    "failure",
    "feature",
    "for",
    "from",
    "have",
    "issue",
    "not",
    "request",
    "should",
    "support",
    "test",
    "tests",
    "that",
    "the",
    "this",
    "using",
    "when",
    "with",
    "would",
    "your",
}


def _terms(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z][a-z0-9_]{2,}", text.lower())
        if token not in _STOPWORDS
    }


def _fixture_scopes(text: str) -> set[str]:
    return set(
        re.findall(
            r"\b(function|class|module|package|session)(?:-scoped)?\s+fixture\b",
            text.lower(),
        )
    )


def _negated_terms(text: str) -> set[str]:
    words = re.findall(r"[a-z][a-z0-9_]*", text.lower())
    negated: set[str] = set()
    for index, word in enumerate(words):
        if word in {"not", "never", "without", "cannot"}:
            negated.update(_terms(" ".join(words[index + 1 : index + 5])))
    return negated


def _opposing_actions(first: str, second: str) -> bool:
    first_terms = _terms(first)
    second_terms = _terms(second)
    for pair in (
        {"enable", "disable"},
        {"add", "remove"},
        {"show", "hide"},
        {"allow", "prevent"},
    ):
        first_action = first_terms & pair
        second_action = second_terms & pair
        if (
            len(first_action) == len(second_action) == 1
            and first_action != second_action
        ):
            return True
    return False


def search_query(
    title: str, body: str, *, excluded: frozenset[str] = pytest_profile.SEARCH_STOPWORDS
) -> str | None:
    """Use a small, safe set of distinctive words for GitHub's search query."""
    title_terms = _terms(title) - excluded
    body_terms = _terms(body) - excluded
    if len(title_terms | body_terms) < 3 or len(body_terms) < 2:
        return None
    terms = sorted(title_terms, key=lambda term: (-len(term), term))[:3]
    if len(terms) < 2:
        terms.extend(
            sorted(body_terms - title_terms, key=lambda term: (-len(term), term))[:2]
        )
    return "(" + " OR ".join(terms[:3]) + ")"


@dataclass(frozen=True)
class Match:
    issue: IssueRecord
    kind: Literal["duplicate", "related"]
    reason: str
    score: float


class Connection(Protocol):
    @property
    def key(self) -> str: ...
    @property
    def description(self) -> str: ...
    @property
    def patterns(self) -> tuple[str, ...]: ...


@dataclass(frozen=True)
class _Connection:
    key: str
    description: str
    patterns: tuple[str, ...]


def _excerpt(text: str, connection: Connection) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "```", "~~~"))
    ]
    cue = connection.patterns[-1]
    for line in lines:
        if match := re.search(cue, line, re.I):
            start = max(0, match.start() - 24)
            return (
                ("…" if start else "")
                + line[start : start + 100]
                + ("…" if len(line) > start + 100 else "")
            )
    prose = next((line for line in lines if len(line.split()) >= 6), None)
    value = prose or (lines[0] if lines else "")
    return value[:100] + ("…" if len(value) > 100 else "")


def assess_match(
    title: str, body: str, candidate: IssueRecord, *, project_connections: bool = True
) -> Match | None:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    candidate_body = re.sub(r"<!--.*?-->", "", candidate.body, flags=re.S)
    excluded = pytest_profile.SEARCH_STOPWORDS if project_connections else frozenset()
    title_terms = _terms(title) - excluded
    body_terms = _terms(body) - excluded
    other_title = _terms(candidate.title) - excluded
    other_body = _terms(candidate_body) - excluded
    shared_title = title_terms & other_title
    shared_body = body_terms & other_body
    title_similarity = (
        2 * len(shared_title) / max(1, len(title_terms) + len(other_title))
    )
    body_similarity = 2 * len(shared_body) / max(1, len(body_terms) + len(other_body))
    score = 2 * title_similarity + body_similarity
    connection: Connection | None = (
        pytest_profile.match_connection(
            title + "\n" + body, candidate.title + "\n" + candidate_body
        )
        if project_connections
        else None
    )
    if connection is None:
        # Strong matching titles can still identify an unlisted topic. Two
        # generic words such as "JUnit XML" are insufficient for this fallback.
        if len(shared_title) < 3 or title_similarity < 0.6 or body_similarity < 0.3:
            return None
        connection = _Connection(
            "matching_title",
            f'the behavior in "{title[:72]}"',
            (
                r"\b(?:"
                + "|".join(re.escape(term) for term in sorted(shared_title))
                + r")\b",
            ),
        )
    different_scopes, different_polarity, opposing_actions, distinction = (
        pytest_profile.match_distinction(
            body, candidate_body, title, candidate.title, connection.key
        )
        if project_connections
        else (
            False,
            bool((_negated_terms(body) ^ _negated_terms(candidate_body)) & shared_body),
            _opposing_actions(
                title + " " + body, candidate.title + " " + candidate_body
            ),
            "The same failure or request is not established.",
        )
    )
    reason = (
        f"Both concern {connection.description}. "
        f'This report: "{_excerpt(body, connection)}"; '
        f'earlier: "{_excerpt(candidate_body, connection)}". {distinction}'
    )
    if (
        project_connections
        and len(shared_title) >= 2
        and title_similarity >= 0.6
        and len(shared_body) >= 2
        and body_similarity >= 0.3
        and not different_scopes
        and not different_polarity
        and not opposing_actions
    ):
        return Match(candidate, "duplicate", reason, score)
    return Match(candidate, "related", reason, score)
