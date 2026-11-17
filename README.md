# Open-source Maintainer Copilot

The application turns a pasted pytest issue into a reviewable triage report. It
checks a fixed view of pytest's bug and feature templates, drafts requests for
missing details, and cites the relevant template lines. When given a public
pytest issue number, it searches earlier public pytest issues and shows ranked
duplicate candidates and related issues with reasons and links. It abstains from
those judgments when the number or sufficient issue detail is missing, or when
GitHub search fails. For issues about capture fixtures or fixture scope, it
retrieves the relevant section of the public pytest documentation and adds a
linked passage only when that section supports the corresponding report claim.
If the passage is unavailable or changed, the report abstains from that claim.
Report generation checks each claim against passages returned during that request;
parsing a saved report alone cannot establish where a passage came from.
When a reviewer supplies a pytest source commit, repository path, and line,
the report quotes the inspected line and links to its exact commit and location.
The web interface also links to the inspected excerpt. Unavailable source
produces an abstention instead of a claim.
The report can suggest a pytest `type:*` label and show the exact issue-text
quote used for that suggestion. A model selects from evidence-backed reply
statements; the server checks its response and adds citation markers before
display. If the model is unavailable or returns unsupported content, the report
shows an abstention and retains the cited template-detail reply.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python
3.12, then run:

```sh
uv sync --locked --group dev
uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

To enable model suggestions, set `MODEL_NAME` to a model served by an
[OpenAI-compatible chat-completions endpoint](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx).
`MODEL_BASE_URL` defaults to `http://127.0.0.1:11434/v1` (Ollama's local
endpoint). For example, after starting a local model server:

```sh
MODEL_NAME=your-model-name uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

Set `MODEL_BASE_URL` if your server uses a different URL. The model receives the
issue title and body plus the report's available citation-backed statements. It
returns a pytest type label or unknown, an exact quote from the issue for a
suggested label, and citation IDs to include in the draft reply. The server
rejects free-text claims, unknown citations, and labels without an unnegated
cue in the quote's original issue context. With no model configured, the report
still works and marks the model suggestion as unavailable.

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

## Inspect pytest source

`GET /api/source` accepts a full lowercase 40-character commit SHA, a relative
repository file path, and a positive line number. For example:

```sh
curl --get http://127.0.0.1:8000/api/source \
  --data-urlencode 'commit=36eed6b7b0eb59760fc4b33e90bdaac5057388f0' \
  --data-urlencode 'path=src/_pytest/capture.py' \
  --data-urlencode 'line=1014'
```

The response contains at most 11 lines around the requested line, a GitHub
permalink, and the commit and path that were read. Inspection is limited to the
public `pytest-dev/pytest` repository, 256 KiB per file, and 4,096 excerpt
characters. Invalid arguments return HTTP 422; unavailable, oversized, or
out-of-range source returns HTTP 404. The operation only reads source.
The report API accepts the same values in an optional `source_location` object
inside `POST /api/triage`; the web form exposes those fields directly.

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
