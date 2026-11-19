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
When the issue text contains one explicit `pytest-dev/pytest` PR or full commit
URL, or a repo-qualified reference labelled `PR`, the report reads GitHub check
runs for that PR's head and, while open, its test merge commit, or for the linked
commit. Each completed check appears with its own conclusion, commit SHA,
and check-run citation in the API and web report. Contradictory checks stay
separate; the report makes no overall CI verdict. If the linked checks cannot
be read or none have completed, it abstains on CI evidence. When one PR commit's
checks are unavailable, it cites checks from the other and records a partial
CI abstention. Issues without one unambiguous relevant link do not trigger CI
inspection; links described as unrelated, historical context, or background only
are excluded.
An explicitly paired PR and `merged as` commit count as one target; the commit
is inspected. Other multiple-link cases remain ambiguous and do not trigger CI.
The reader caps GitHub responses and marks incomplete check lists unavailable.
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
[OpenAI-compatible chat-completions endpoint](https://docs.ollama.com/api/openai-compatibility)
with JSON-schema structured output support.
`MODEL_BASE_URL` defaults to `http://127.0.0.1:11434/v1` (Ollama's local
endpoint). For example, after starting a local model server:

```sh
MODEL_NAME=your-model-name uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

Set `MODEL_BASE_URL` if your server uses a different URL. The model receives the
issue title and body, mechanically valid issue-text quote options, and the
report's available citation-backed statements. It
returns a pytest type label or unknown, an exact quote from the issue for a
suggested label, and citation IDs to include in the draft reply. The server
rejects free-text claims, unknown citations, and labels without an unnegated
cue in the quote's original issue context. With no model configured, the report
still works and marks the model suggestion as unavailable.

The [tested Windows Ollama / WSL app guide](docs/local-model.md) serves
Qwen2.5 Coder 3B Instruct Q4_K_M with 16K context and no paid model API.
[Issue #21's measurements](docs/evaluation/issue-21.md) record all three local
candidates, twenty-case field scores, GPU memory, serving errors and real
API/browser/agent checks. Windows and WSL connectivity is verified explicitly;
their localhost addresses are not assumed interchangeable.

## Bounded agent report

Select **Use bounded agent** in the web form, or send the same JSON issue body
to `POST /api/agent/triage`. This path uses the configured `MODEL_NAME` to choose
up to three actions and one final report selection. The only read actions are
`search_earlier_issues` for the supplied pytest issue number and `inspect_source`
for the supplied full commit SHA, path, and line. The server validates each
action, allows each tool at most once, derives the issue search query itself,
and caps each tool result at 5,000 characters. Verified documentation passages
are available as context before the first action. The final selection passes
through the same report and citation validation as `/api/triage`.

If a tool fails or the agent does not finish within the step limit, the report
records an abstention. The agent cannot post, edit, or execute commands. The
agent's usefulness depends on the configured model; model selection and quality
measurement are separate work, so the controlled-response tests here establish
behavior and safety boundaries rather than model quality.
Linked CI evidence follows the same explicit-link rule on both report endpoints;
it does not add an agent action.

## Replay the historical issue

Run the first time-frozen pytest replay with:

```sh
uv run --no-env-file python -m maintainer_copilot.replay
```

The command fetches the public title and body of [pytest issue #12081](https://github.com/pytest-dev/pytest/issues/12081)
and its earlier linked [issue #3448](https://github.com/pytest-dev/pytest/issues/3448).
It verifies each issue's opening timestamp and SHA-256 of `title + NUL + body`
against [case metadata](src/maintainer_copilot/cases/pytest_12081.json) before
building a report. Changed or unavailable content raises `CaseFlagged` before
the model runs. GitHub GraphQL reported `lastEditedAt: null` for both issues when
the case was verified; the metadata records that observation. The public
metadata stores the opening title and content hash, while the body is fetched
from GitHub, following [ADR-0003](docs/adr/0003-publish-evaluation-metadata.md).

The evidence cutoff is the opening time, March 6, 2024 at 00:03:25 UTC. The
repository evidence comes from pytest commit `03e54712dd123138aa4c1035a027e17d0dd9a86c`,
dated March 4, 2024. Replay checks that the recorded commit date matches
GitHub's commit record and precedes the cutoff before reading issue content.
An unavailable or mismatched commit flags the case. Template links,
documentation, and source inspection use that commit. The only earlier issue
in this first case is #3448, whose title and body were also verified. Replay
does not search the live issue index or read comments, labels, closures, or
duplicate decisions. Linked CI checks are
unavailable in the historical view and produce an abstention. The default model
response is controlled: it selects available cited reply statements and
abstains on issue type. It is a reproducible smoke replay, not a model quality
measurement or a scored evaluation outcome. Real-model selection and `llmfit`
results are recorded in [issue #21](docs/evaluation/issue-21.md); earlier quality
observations remain provisional.

The deterministic replay tests run with `pytest`. To check the recorded case
against public GitHub content and mutate post-cutoff activity in a controlled
reader, run:

```sh
RUN_LIVE_REPLAY=1 uv run --no-env-file pytest -q tests/test_replay.py -k recorded_case
```

Twenty case metadata files now live in
[`src/maintainer_copilot/cases/`](src/maintainer_copilot/cases/). Replay all twenty
with controlled model responses using:

```sh
uv run --no-env-file python -m maintainer_copilot.replay --all
```

Each result includes its issue number and human-review status. A case whose
public opening text or pinned commit no longer matches is printed as flagged.
The [first-five case review](docs/evaluation/first-five-cases.md) records the
confirmed expected outcomes, individual relationship judgments, provenance
checks, and the live replay result. All five have reviewer confirmation.
The [second case review](docs/evaluation/cases-six-through-ten.md) records
cases 6 through 10, their confirmation provenance, and ambiguous judgments.
The [third case review](docs/evaluation/cases-eleven-through-fifteen.md) records
cases 11 through 15, their provenance, difficult topical negatives, and review
status. The [fourth case review](docs/evaluation/cases-sixteen-through-twenty.md)
records cases 16 through 20 and their delegated confirmation. Pending outcomes cannot be scored until a human confirms them.
These controlled replays are smoke checks. The separate
[issue #21 real-model run](docs/evaluation/issue-21.md) evaluates all twenty cases;
the full workflow comparison remains #16.

## Score the first reviewed cases

Run the twenty-case field scorer and keyword-rule baseline with public GitHub
access:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > /tmp/evaluation-new-results.json
```

[Issue #12's methodology and provisional results](docs/evaluation/issue-12.md)
explain each field score, failures, latency and cost assumptions, and the
semantic judgments still awaiting human review. The checked-in
[results JSON](docs/evaluation/issue-12-results.json) keeps case-level outputs
and confirmed judgments inspectable. The command writes raw scores separately
so it does not replace the reviewed artifact. No model is selected by this
evaluation.

[Issue #13's ten-case results](docs/evaluation/issue-13.md) compare aggregate
and case-level scores with the original five-case run. Generated reply usefulness
and semantic citation judgments require separate human review; confirming a case's
expected outcome does not confirm its generated report.

[Issue #14's expanded-catalog run](docs/evaluation/issue-14.md) records the
completed replay and scoring of all fifteen cases. The five new outcomes were
reviewed by Codex and accepted through the requesting user's explicit delegation;
the case review records that attribution.

[Issue #15’s twenty-case benchmark](docs/evaluation/issue-15.md) records replay
integrity, field-level metrics, representative failures, and acceptance evidence.
All twenty outcomes are confirmed; the new five use Codex review accepted by
the requesting user. [Issue #21](docs/evaluation/issue-21.md) records real local
model responses; semantic report review remains pending and earlier quality
observations remain provisional.

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

## Inspect a report trace

Every report includes a `trace_id` and a `status` (`complete` or `partial`). The
web report links the ID to `GET /api/traces/{trace_id}` and shows the same trace
events below the report. For example:

```sh
trace_id=... # copy trace_id from the report
curl "http://127.0.0.1:8000/api/traces/$trace_id"
```

Each event identifies a retrieval, bounded agent tool action, or model call,
with its target (including a bounded search query preview or configured model
name), status, start offset, duration, result count, evidence references where
applicable, and a sanitized error when it fails. Model events include input and
output token counts when the model endpoint provides them. The trace omits
prompts, raw issue text, and raw model responses. A failed dependency leaves
supported report fields and citations available, marks the report `partial`, and
records an abstention for the unsupported field.

Traces are kept in memory in the current server process, up to the most recent
100 reports. They are unavailable after a restart or from another server worker;
the trace API returns 404 when an ID is no longer present. No model is required
to inspect a report trace.

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
