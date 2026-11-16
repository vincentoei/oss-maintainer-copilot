# Open-source Maintainer Copilot

The first application slice turns a pasted pytest issue into a reviewable triage
report. It checks the issue against a fixed view of pytest's bug and feature
templates, drafts requests for missing details, and cites the relevant template
lines. Issue type, duplicates, and related issues remain unassessed in this slice.
The application reads no live repository data and makes no model or GPU calls.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python
3.12, then run:

```sh
uv sync --locked --group dev
uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

Open <http://127.0.0.1:8000> to paste an issue. The same operation is available
from Python:

```python
from maintainer_copilot import IssueUnderReview, triage_issue

report = triage_issue(
    IssueUnderReview(
        title="Bug: collection fails", body="pytest fails during collection"
    )
)
print(report.model_dump_json(indent=2))
```

## Deterministic checks

```sh
uv run --no-env-file ruff check .
uv run --no-env-file ruff format --check .
uv run --no-env-file mypy src tests
uv run --no-env-file pytest
```

GitHub Actions runs these checks on pushes and pull requests. The template
citations point to pytest commit `50234b4e670064c42a4c29cb6258115a2079ba4c`;
tests use the same fixed evidence and require no network access.
