"""Read check results only for an explicitly linked pytest PR or commit."""

import json
import os
import re
from dataclasses import dataclass
from typing import Literal, Protocol
from urllib.error import URLError
from urllib.request import Request, urlopen

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

MAX_RESPONSE_BYTES = 262_144
MAX_CHECKS = 100
_LINK = re.compile(
    r"(?<![A-Za-z0-9/=?&])https://github\.com/pytest-dev/pytest/"
    r"(?:(pull)/([1-9][0-9]*)|(commit)/([0-9a-fA-F]{40}))"
    r"(?=$|[\s/?#)\]>]|[.,;:!](?=\s|$))"
)
_SHORT_PR = re.compile(
    r"\b(?:PR|pull request)\s*:?\s+pytest-dev/pytest#([1-9][0-9]*)"
    r"(?=$|[\s)\]>]|[.,;:!](?=\s|$))",
    re.IGNORECASE,
)
_UNRELATED = re.compile(
    r"\b(?:unrelated|irrelevant|not relevant|do not use|do not inspect|ignore|"
    r"historical context|background only|predates (?:this|the) regression)\b",
    re.IGNORECASE,
)
_DO_NOT_IGNORE = re.compile(r"\b(?:do not|don't|never)\s+ignore\b", re.IGNORECASE)
_MERGED_AS = re.compile(r"\s*,?\s*merged as\s+", re.IGNORECASE)
_FOLLOWING_EXCLUSION = re.compile(
    r"\s*(?:(?:it|this|that)(?:\s+(?:PR|commit))?\s+)?"
    r"(?:is|was)\s+(?:unrelated|irrelevant|not relevant|not related)\b",
    re.IGNORECASE,
)
_SHA = re.compile(r"[0-9a-f]{40}")
_CONCLUSIONS = frozenset(
    {
        "success",
        "failure",
        "neutral",
        "cancelled",
        "timed_out",
        "action_required",
        "skipped",
        "stale",
        "startup_failure",
    }
)


class CIUnavailable(Exception):
    """The linked CI evidence could not be verified."""


@dataclass(frozen=True)
class CILink:
    kind: Literal["pull", "commit"]
    value: str


def linked_target(title: str, body: str) -> CILink | None:
    """Accept one target link or a PR explicitly paired with its merge commit."""
    links: set[CILink] = set()
    merged_pairs: list[tuple[CILink, CILink]] = []
    for text in (title, body):
        matches = list(_LINK.finditer(text))
        for match in matches:
            if not _is_unrelated(text, match.start(), match.end()):
                links.add(
                    CILink("pull", match[2])
                    if match[1]
                    else CILink("commit", match[4].lower())
                )
        for first, second in zip(matches, matches[1:], strict=False):
            if (
                first[1]
                and second[3]
                and _MERGED_AS.fullmatch(text[first.end() : second.start()])
            ):
                merged_pairs.append(
                    (CILink("pull", first[2]), CILink("commit", second[4].lower()))
                )
        for match in _SHORT_PR.finditer(text):
            if not _is_unrelated(text, match.start(), match.end()):
                links.add(CILink("pull", match[1]))
    if len(links) == 1:
        return next(iter(links))
    for pull, commit in merged_pairs:
        if links == {pull, commit}:
            return commit
    return None


def _is_unrelated(text: str, start: int, end: int) -> bool:
    before = text[max(0, start - 100) : start]
    current_line = before.rsplit("\n", 1)[-1]
    if current_line.strip():
        before = current_line
    boundaries = list(re.finditer(r"[.!?;](?=\s)", before))
    preceding = before[boundaries[-1].end() :] if boundaries else before
    after = text[end : end + 100]
    current_line, _, next_line = after.partition("\n")
    boundary = re.search(r"[.!?](?=\s|$)", current_line)
    following = current_line[: boundary.start()] if boundary else current_line
    adjacent = current_line[boundary.end() :] if boundary else ""
    if not adjacent.strip():
        adjacent = next_line
    clause = re.split(r"[.!?](?=\s|$)|\n", adjacent, maxsplit=1)[0]
    if (
        _FOLLOWING_EXCLUSION.match(clause)
        and not _LINK.search(clause)
        and not _SHORT_PR.search(clause)
    ):
        return True
    context = _DO_NOT_IGNORE.sub("", f"{preceding} {following}")
    return bool(_UNRELATED.search(context))


class CheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    name: str = Field(min_length=1, max_length=200)
    conclusion: str
    commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    url: HttpUrl


@dataclass(frozen=True)
class CIInspection:
    checks: tuple[CheckResult, ...]
    partial: bool = False


class CISource(Protocol):
    def get_checks(self, link: CILink) -> CIInspection: ...


class PublicCISource:
    """Fetch bounded GitHub API responses for pytest only."""

    def _get(self, path: str) -> object:
        headers = {"Accept": "application/vnd.github+json"}
        if token := os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
        request = Request(
            f"https://api.github.com/repos/pytest-dev/pytest/{path}",
            headers=headers,
        )
        try:
            with urlopen(request, timeout=5) as response:
                body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise CIUnavailable("GitHub CI response exceeds the inspection limit.")
            return json.loads(body)
        except (OSError, URLError, ValueError) as exc:
            raise CIUnavailable("Linked CI data is unavailable.") from exc

    def get_checks(self, link: CILink) -> CIInspection:
        if link.kind == "pull":
            if not re.fullmatch(r"[1-9][0-9]*", link.value):
                raise CIUnavailable("Linked pull request is invalid.")
        elif link.kind == "commit":
            if not _SHA.fullmatch(link.value):
                raise CIUnavailable("Linked commit is invalid.")
        else:
            raise CIUnavailable("Linked CI target is invalid.")
        if link.kind == "pull":
            pull = self._get(f"pulls/{link.value}")
            if not isinstance(pull, dict):
                raise CIUnavailable("Linked pull request data is invalid.")
            head = pull.get("head")
            head_commit = head.get("sha") if isinstance(head, dict) else None
            if not isinstance(head_commit, str) or not _SHA.fullmatch(head_commit):
                raise CIUnavailable("Linked commit is unavailable.")
            commits = [head_commit]
            if pull.get("state") == "open":
                merge_commit = pull.get("merge_commit_sha")
                if merge_commit is not None:
                    if not isinstance(merge_commit, str) or not _SHA.fullmatch(
                        merge_commit
                    ):
                        raise CIUnavailable("Linked test merge commit is invalid.")
                    if merge_commit != head_commit:
                        commits.append(merge_commit)
        else:
            commits = [link.value]

        checks: list[CheckResult] = []
        unavailable = 0
        last_error: CIUnavailable | None = None
        for commit in commits:
            try:
                checks.extend(self._checks_for_commit(commit))
            except CIUnavailable as exc:
                unavailable += 1
                last_error = exc
        if unavailable == len(commits):
            assert last_error is not None
            raise last_error
        return CIInspection(tuple(checks), partial=unavailable > 0)

    def _checks_for_commit(self, commit: str) -> list[CheckResult]:
        payload = self._get(
            f"commits/{commit}/check-runs?per_page={MAX_CHECKS}&filter=all"
        )
        if not isinstance(payload, dict):
            raise CIUnavailable("Linked check results are invalid.")
        runs = payload.get("check_runs")
        count = payload.get("total_count")
        if (
            not isinstance(runs, list)
            or type(count) is not int
            or count > MAX_CHECKS
            or count != len(runs)
        ):
            raise CIUnavailable("Linked check results are incomplete.")
        checks: list[CheckResult] = []
        for run in runs:
            if not isinstance(run, dict):
                raise CIUnavailable("Linked check result is invalid.")
            if run.get("status") != "completed":
                continue
            run_id = run.get("id")
            url = run.get("html_url")
            valid_url = isinstance(url, str) and bool(
                re.fullmatch(
                    rf"https://github\.com/pytest-dev/pytest/"
                    rf"(?:runs/{run_id}|actions/runs/[1-9][0-9]*/job/{run_id})",
                    url,
                )
            )
            conclusion = run.get("conclusion")
            if (
                type(run_id) is not int
                or run_id <= 0
                or not isinstance(url, str)
                or not valid_url
                or run.get("head_sha") != commit
                or not isinstance(conclusion, str)
                or conclusion not in _CONCLUSIONS
            ):
                raise CIUnavailable("Linked check result could not be verified.")
            try:
                checks.append(
                    CheckResult(
                        name=run["name"],
                        conclusion=run["conclusion"],
                        commit=commit,
                        url=HttpUrl(url),
                    )
                )
            except (KeyError, ValueError) as exc:
                raise CIUnavailable("Linked check result is invalid.") from exc
        return checks
