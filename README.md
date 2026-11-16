# Open-source Maintainer Copilot

The application turns a pasted pytest issue into a reviewable triage report. It
checks a fixed view of pytest's bug and feature templates, drafts requests for
missing details, and cites the relevant template lines. When given a public
pytest issue number, it searches earlier public pytest issues and shows ranked
duplicate candidates and related issues with reasons and links. It abstains from
those judgments when the number or sufficient issue detail is missing, or when
GitHub search fails. Issue type remains unassessed. The application makes no
model or GPU calls.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python
3.12, then run:

```sh
uv sync --locked --group dev
uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

Open <http://127.0.0.1:8000> to paste an issue. Enter its pytest issue number
to search only issues opened before it. For a newly drafted issue without a
number, the report still checks template details and abstains on earlier issue
matches. The same operation is available from Python:

```python
from maintainer_copilot import IssueUnderReview, triage_issue

report = triage_issue(
    IssueUnderReview(
        title="Bug: collection fails", body="pytest fails during collection"
    )
)
print(report.model_dump_json(indent=2))
```

Pass `number=<pytest issue number>` to `IssueUnderReview` to include earlier
issue search. GitHub's public API is used without credentials; setting
`GITHUB_TOKEN` increases the available API rate limit. Candidate titles and
bodies reflect GitHub's current issue text, so historical evaluation still
requires verified opening versions as described in ADR-0001. If a broad query
exceeds GitHub's 1,000-result search window, the report abstains on issue
matches.

## Deterministic checks

```sh
uv run --no-env-file ruff check .
uv run --no-env-file ruff format --check .
uv run --no-env-file mypy src tests
uv run --no-env-file pytest
```

GitHub Actions runs these checks on pushes and pull requests. The template
citations point to pytest commit `50234b4e670064c42a4c29cb6258115a2079ba4c`;
issue-search API fixtures use fixed records and require no network access.
