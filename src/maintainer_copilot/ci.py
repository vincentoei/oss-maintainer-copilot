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
    r"\b(?:unrelated|irrelevant|not relevant|do not use|do not inspect|ignore)\b",
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
    """Accept one distinct explicit link in the target repository's issue text."""
    text = f"{title}\n{body}"
    links: set[CILink] = set()
    for match in _LINK.finditer(text):
        if _is_unrelated(text, match.start(), match.end()):
            continue
        links.add(
            CILink("pull", match[2]) if match[1] else CILink("commit", match[4].lower())
        )
    for match in _SHORT_PR.finditer(text):
        if not _is_unrelated(text, match.start(), match.end()):
            links.add(CILink("pull", match[1]))
    return next(iter(links)) if len(links) == 1 else None


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
    qualifier = re.match(
        r"\s*(?:(?:it|this)\s+)?(?:is\s+)?"
        r"(?:unrelated|irrelevant|not relevant|not related)\b",
        next_line,
        re.IGNORECASE,
    )
    if qualifier and not _LINK.search(next_line) and not _SHORT_PR.search(next_line):
        following += f" {next_line}"
    return bool(_UNRELATED.search(f"{preceding} {following}"))


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
