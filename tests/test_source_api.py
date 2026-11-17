"""Issue #5 behavior at the public source inspection and report API seams."""

import asyncio
from email.message import Message
from io import BytesIO
from typing import Any, cast
from urllib.error import HTTPError

import httpx2
import pytest

from maintainer_copilot.web import app

COMMIT = "36eed6b7b0eb59760fc4b33e90bdaac5057388f0"
PATH = "src/_pytest/capture.py"


def get(path: str, params: dict[str, str | int]) -> httpx2.Response:
    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.get(path, params=params)

    return asyncio.run(request())


def post_report(location: dict[str, str | int]) -> httpx2.Response:
    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post(
                "/api/triage",
                json={
                    "title": "Bug: inspect source citation",
                    "body": "",
                    "source_location": location,
                },
            )

    return asyncio.run(request())


def test_valid_source_citation_reads_pinned_file_and_returns_bounded_excerpt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = "\n".join(f"line {number}" for number in range(1, 31)).encode()
    requested: list[tuple[str, int]] = []

    class BoundedResponse(BytesIO):
        def read(self, size: int | None = -1) -> bytes:
            assert size is not None and 0 < size <= 262_145
            return super().read(size)

    def fetch(request: Any, timeout: int) -> BoundedResponse:
        requested.append((request.full_url, timeout))
        return BoundedResponse(source)

    monkeypatch.setattr("maintainer_copilot.source.urlopen", fetch)

    response = get("/api/source", {"commit": COMMIT, "path": PATH, "line": 15})

    assert response.status_code == 200, response.text
    assert cast(dict[str, Any], response.json()) == {
        "commit": COMMIT,
        "path": PATH,
        "line": 15,
        "start_line": 10,
        "end_line": 20,
        "lines": [f"line {number}" for number in range(10, 21)],
        "source_url": (
            f"https://github.com/pytest-dev/pytest/blob/{COMMIT}/{PATH}#L15"
        ),
    }
    assert requested == [
        (f"https://raw.githubusercontent.com/pytest-dev/pytest/{COMMIT}/{PATH}", 5)
    ]


@pytest.mark.parametrize(
    ("commit", "path"),
    [
        ("main", PATH),
        (COMMIT[:12], PATH),
        (COMMIT + "\n", PATH),
        (COMMIT, "../secrets.py"),
        (COMMIT, "/etc/passwd"),
        (COMMIT, "src//capture.py"),
        (COMMIT, "src\\capture.py"),
        (COMMIT, "src/%2e%2e/capture.py"),
    ],
)
def test_invalid_commit_or_path_is_rejected_before_source_access(
    monkeypatch: pytest.MonkeyPatch, commit: str, path: str
) -> None:
    def unexpected_fetch(request: Any, timeout: int) -> None:
        raise AssertionError("invalid input reached the source reader")

    monkeypatch.setattr("maintainer_copilot.source.urlopen", unexpected_fetch)

    response = get("/api/source", {"commit": commit, "path": path, "line": 1})

    assert response.status_code == 422


def test_unavailable_source_returns_clear_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing(request: Any, timeout: int) -> None:
        raise HTTPError(request.full_url, 404, "Not Found", Message(), None)

    monkeypatch.setattr("maintainer_copilot.source.urlopen", missing)

    response = get("/api/source", {"commit": COMMIT, "path": PATH, "line": 15})

    assert response.status_code == 404
    assert response.json() == {"detail": "Source file is unavailable."}


@pytest.mark.parametrize(
    "location",
    [
        {"commit": "main", "path": PATH, "line": 1014},
        {"commit": COMMIT, "path": "../capture.py", "line": 1014},
    ],
)
def test_report_rejects_invalid_source_location_before_reading(
    monkeypatch: pytest.MonkeyPatch, location: dict[str, str | int]
) -> None:
    def unexpected_fetch(request: Any, timeout: int) -> None:
        raise AssertionError("invalid report input reached the source reader")

    monkeypatch.setattr("maintainer_copilot.source.urlopen", unexpected_fetch)

    response = post_report(location)

    assert response.status_code == 422


def test_oversized_source_and_out_of_range_line_are_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "maintainer_copilot.source.urlopen",
        lambda request, timeout: BytesIO(b"x" * 262_145),
    )
    oversized = get("/api/source", {"commit": COMMIT, "path": PATH, "line": 1})
    assert oversized.status_code == 404
    assert oversized.json() == {"detail": "Source file exceeds the inspection limit."}

    monkeypatch.setattr(
        "maintainer_copilot.source.urlopen",
        lambda request, timeout: BytesIO(b"one line\n"),
    )
    absent_line = get("/api/source", {"commit": COMMIT, "path": PATH, "line": 15})
    assert absent_line.status_code == 404
    assert absent_line.json() == {"detail": "Source line is unavailable."}

    monkeypatch.setattr(
        "maintainer_copilot.source.urlopen",
        lambda request, timeout: BytesIO(b"x" * 4_097),
    )
    oversized_excerpt = get("/api/source", {"commit": COMMIT, "path": PATH, "line": 1})
    assert oversized_excerpt.status_code == 404
    assert oversized_excerpt.json() == {
        "detail": "Source excerpt exceeds the inspection limit."
    }


def test_report_cites_only_inspected_pytest_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_lines = [f"line {number}" for number in range(1, 1021)]
    source_lines[1013] = (
        '    r"""Enable text capturing of writes to ``sys.stdout`` and ``sys.stderr``.'
    )
    requested: list[str] = []

    def fetch(request: Any, timeout: int) -> BytesIO:
        requested.append(request.full_url)
        return BytesIO("\n".join(source_lines).encode())

    monkeypatch.setattr("maintainer_copilot.source.urlopen", fetch)
    response = post_report({"commit": COMMIT, "path": PATH, "line": 1014})

    assert response.status_code == 200, response.text
    report = cast(dict[str, Any], response.json())
    assert report["source_claims"] == [
        {
            "claim": (
                f"At commit {COMMIT}, pytest source {PATH}:1014 reads: "
                f"{source_lines[1013].strip()}"
            ),
            "citation_id": "C5",
        }
    ]
    citation = next(
        item
        for item in report["citations"]
        if item["id"] == report["source_claims"][0]["citation_id"]
    )
    assert citation["source_url"] == (
        f"https://github.com/pytest-dev/pytest/blob/{COMMIT}/{PATH}#L1014"
    )
    assert citation["source_location"] == {
        "commit": COMMIT,
        "path": PATH,
        "line": 1014,
    }
    assert citation["passage"] == source_lines[1013].strip()
    assert requested == [
        f"https://raw.githubusercontent.com/pytest-dev/pytest/{COMMIT}/{PATH}"
    ]


def test_report_abstains_when_requested_source_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing(request: Any, timeout: int) -> None:
        raise HTTPError(request.full_url, 404, "Not Found", Message(), None)

    monkeypatch.setattr("maintainer_copilot.source.urlopen", missing)
    response = post_report({"commit": COMMIT, "path": PATH, "line": 1014})

    assert response.status_code == 200, response.text
    report = cast(dict[str, Any], response.json())
    assert report["source_claims"] == []
    assert "source_claims" in {item["field"] for item in report["abstentions"]}
