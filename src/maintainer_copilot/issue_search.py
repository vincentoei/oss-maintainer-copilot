"""Read public pytest issues and identify plausible earlier matches."""

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, Protocol
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class IssueSearchError(Exception):
    """GitHub issue evidence could not be read reliably."""


@dataclass(frozen=True)
class IssueRecord:
    number: int
    title: str
    body: str
    created_at: datetime

    @property
    def url(self) -> str:
        return f"https://github.com/pytest-dev/pytest/issues/{self.number}"


class IssueSource(Protocol):
    def get_issue(self, number: int) -> IssueRecord: ...

    def search_issues(
        self, query: str, created_before: datetime
    ) -> list[IssueRecord]: ...


class GitHubIssueSource:
    """The two read-only GitHub calls needed for a historical issue search."""

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
                data = json.load(response)
            if not isinstance(data, dict):
                raise ValueError("expected an object")
            return data
        except (URLError, TimeoutError, ValueError, OSError) as exc:
            raise IssueSearchError("GitHub issue search is unavailable.") from exc

    def get_issue(self, number: int) -> IssueRecord:
        data = self._get_json(
            f"https://api.github.com/repos/pytest-dev/pytest/issues/{number}"
        )
        if "pull_request" in data:
            raise IssueSearchError("The supplied number refers to a pull request.")
        try:
            record = _record(data)
        except (KeyError, TypeError, ValueError) as exc:
            raise IssueSearchError("GitHub returned incomplete issue data.") from exc
        if record.number != number:
            raise IssueSearchError("GitHub returned a different issue number.")
        return record

    def search_issues(self, query: str, created_before: datetime) -> list[IssueRecord]:
        cutoff = created_before.astimezone(UTC).isoformat(timespec="seconds")
        search = (
            f"{query} repo:pytest-dev/pytest is:issue in:title,body created:<{cutoff}"
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
            return [_record(item) for item in collected if "pull_request" not in item]
        except (KeyError, TypeError, ValueError) as exc:
            raise IssueSearchError("GitHub returned incomplete issue data.") from exc


def _record(data: dict[str, object]) -> IssueRecord:
    created_at = datetime.fromisoformat(str(data["created_at"]).replace("Z", "+00:00"))
    return IssueRecord(
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
    "pytest",
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


def search_query(title: str, body: str) -> str | None:
    """Use a small, safe set of distinctive words for GitHub's search query."""
    title_terms = _terms(title)
    body_terms = _terms(body)
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


# Bounded connections require behavior-bearing evidence in both reports. Shared
# template headings, stack-frame vocabulary and URLs cannot establish a match.
_CONNECTIONS = (
    (
        "fixture-derived parameter values",
        (
            r"\bfixtures?\b",
            r"\bparametrize\b",
            r"parameters_fixture|fixture[- ]derived parameter|"
            r"Using fixtures in.*parametrize|"
            r"fixture.{0,20}(?:_value_|supplies parameter|provides parameter)",
        ),
    ),
    (
        "readouterr consuming captured output",
        (
            r"\breadouterr\b",
            r"reset|consum|missing|keep.*output|(?:remain|preserve).*?(?:visible|output)",
        ),
    ),
    (
        "the call_runtest_hook import failure",
        (
            r"call_runtest_hook",
            r"ImportError|cannot import",
        ),
    ),
    ("custom debugger selection with --pdbcls", (r"--pdbcls",)),
    (
        "reading test-selection arguments from a file",
        (
            r"\b(?:text file|from (?:a )?file|from-file)\b",
            r"\b(?:arguments?|subsets?|positional)\b",
        ),
    ),
    ("module setup/teardown hooks", (r"setUpModule", r"tearDownModule")),
    ("fixture caching", (r"fixture cach",)),
)


def _connection(first: str, second: str) -> str | None:
    for description, patterns in _CONNECTIONS:
        if all(
            re.search(pattern, text, re.I)
            for text in (first, second)
            for pattern in patterns
        ):
            return description
    # A named exception is a stronger anchor than generic stack-frame words.
    exceptions = set(re.findall(r"\b[A-Z][a-zA-Z]+(?:Error|Exception)\b", first))
    shared = sorted(
        name
        for name in exceptions
        if name in second
        and name
        not in {
            "AssertionError",
            "ValueError",
            "TypeError",
            "RuntimeError",
            "ImportError",
            "ExceptionGroup",
            "BaseException",
        }
    )
    return f"the {shared[0]} failure" if shared else None


def _excerpt(text: str, connection: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "```", "~~~"))
    ]
    cue = next(
        (
            patterns[-1]
            for description, patterns in _CONNECTIONS
            if description == connection
        ),
        r"\w+(?:Error|Exception)\b",
    )
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


def assess_match(title: str, body: str, candidate: IssueRecord) -> Match | None:
    title_terms = _terms(title)
    body_terms = _terms(body)
    other_title = _terms(candidate.title)
    other_body = _terms(candidate.body)
    shared_title = title_terms & other_title
    shared_body = body_terms & other_body
    title_similarity = (
        2 * len(shared_title) / max(1, len(title_terms) + len(other_title))
    )
    body_similarity = 2 * len(shared_body) / max(1, len(body_terms) + len(other_body))
    score = 2 * title_similarity + body_similarity
    connection = _connection(
        title + "\n" + body, candidate.title + "\n" + candidate.body
    )
    if connection is None:
        # Strong matching titles can still identify an unlisted topic. Two
        # generic words such as "JUnit XML" are insufficient for this fallback.
        if len(shared_title) < 3 or title_similarity < 0.6 or body_similarity < 0.3:
            return None
        connection = f'the behavior in "{title[:72]}"'
    review_scopes = _fixture_scopes(body)
    candidate_scopes = _fixture_scopes(candidate.body)
    different_scopes = bool(
        review_scopes
        and candidate_scopes
        and review_scopes.isdisjoint(candidate_scopes)
    )
    different_polarity = bool(
        (_negated_terms(body) ^ _negated_terms(candidate.body)) & shared_body
    )
    opposing_actions = _opposing_actions(
        title + " " + body, candidate.title + " " + candidate.body
    )
    distinction = (
        "The reports describe different fixture scopes."
        if different_scopes
        else "One report negates a shared condition."
        if different_polarity and connection.endswith("FixtureLookupError failure")
        else "The reports request opposing actions."
        if opposing_actions
        else "This requests session-derived parameters; the earlier example passes "
        "fixture functions instead of values."
        if connection == "fixture-derived parameter values"
        and "session" in body
        and re.search(r"fixture _?function_?", candidate.body)
        else "This requests a configuration setting; the earlier issue concerns "
        "command-line help."
        if connection == "custom debugger selection with --pdbcls"
        and "configuration" in title.lower()
        and "help" in candidate.title.lower()
        else "This proposes retaining output via a new API; the earlier issue "
        "asks to keep captured output."
        if connection == "readouterr consuming captured output" and "copyouterr" in body
        else "This reports hooks not running in a project; the earlier issue "
        "questions the documentation."
        if connection == "module setup/teardown hooks"
        and "docs" in candidate.title.lower()
        and "not invoked" in title.lower()
        else "the same failure or request is not established."
    )
    reason = (
        f'Both concern {connection}. This report: "{_excerpt(body, connection)}"; '
        f'earlier: "{_excerpt(candidate.body, connection)}". {distinction}'
    )
    if (
        len(shared_title) >= 2
        and title_similarity >= 0.6
        and len(shared_body) >= 2
        and body_similarity >= 0.3
        and not different_scopes
        and not different_polarity
        and not opposing_actions
    ):
        return Match(candidate, "duplicate", reason, score)
    return Match(candidate, "related", reason, score)
