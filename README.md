# Open-source Maintainer Copilot

The application registers multiple public GitHub repositories and turns an issue
for one selected repository into a reviewable triage report. Add a URL or
owner/repo in the web interface, inspect readiness, select the active repository,
and explicitly refresh or remove registration. New repositories use a generic
profile without Python changes. [Repository setup, API examples, persistence and
supported context limits](docs/repositories.md) describe the reusable behavior.
Issue #33 extends #1's original pytest-first release; pytest stays the seeded
default and retains the established profile described below. It
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
MODEL_NAME=pytest-triage:qwen35-4b-ctx16k MODEL_REASONING_EFFORT=none \
  uv run --no-env-file uvicorn maintainer_copilot.web:app --reload
```

Set `MODEL_BASE_URL` if your server uses a different URL. For compatible endpoints,
`MODEL_REASONING_EFFORT=none` explicitly disables thinking in fixed reports and
both bounded-agent planning and final reporting. Leave it unset or empty to omit
the provider parameter and preserve existing behavior. Other values are rejected.
This opt-in setting supports the [#63 evaluation](docs/evaluation/issue-63/proposal.md);
it does not change the selected model.

The model receives the issue title and body, all valid type labels from the resolved repository profile,
a bounded set of exact issue excerpts, and the report's available citation-backed
statements. It selects a suggested
label or unknown, an independent excerpt index, and citation IDs for the draft
reply. The server maps a valid index back to its original issue-text quote.
The server rejects unknown labels, fabricated/oversized quotes, unknown citations
and extra free-text claims. It validates quote provenance, not whether the quote
semantically justifies the label. Semantic fit, negation and ambiguity remain
model judgments requiring review. The independent keyword baseline keeps its
literal-cue rules. With no model configured, the report still works and marks
model suggestions unavailable.


The [Windows Ollama / WSL app guide](docs/local-model.md) recommends
Qwen3.5 4B Q4_K_M with 16K context and thinking explicitly disabled, with no paid
model API. The [maintainer decision](docs/evaluation/issue-63/promotion-decision.md)
accepts its known semantic-support limitations after the comparison and independent
AI review; the original promotion gates were not all passed. Qwen2.5 Coder 3B
remains selectable for lower-memory use. It does not automatically catch semantic
errors in the selected model's report.
[Issue #21's measurements](docs/evaluation/issue-21.md) record all three local
candidates, twenty-case field scores, GPU memory, serving errors and real
API/browser/agent checks. Windows and WSL connectivity is verified explicitly;
their localhost addresses are not assumed interchangeable.
The [issue #45 follow-up](docs/evaluation/issue-45.md) fixes redundant feature
detail requests found during that validation and records a fresh twenty-case run.

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

Fifty case metadata files now live in
[`src/maintainer_copilot/cases/`](src/maintainer_copilot/cases/). Replay all fifty
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
The [fifth case review](docs/evaluation/cases-twenty-one-through-thirty.md)
records cases 21 through 30, their explicitly delegated confirmations and the
28-family evaluation exclusion manifest. Shared failures stay in one family;
the uncertain case keeps its uncertainty in scoring.
These controlled replays are smoke checks. The separate
[issue #21 real-model run](docs/evaluation/issue-21.md) evaluates all twenty cases;
the full workflow comparison remains #16.

## Score the first reviewed cases

Run the field scorer and keyword-rule baseline with public GitHub
access:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > /tmp/evaluation-new-results.json
```

Issue #18 adds [ten confirmed case reviews](docs/evaluation/cases-thirty-one-through-forty.md).
Their outcomes use Codex review explicitly accepted by the requesting user. The [forty-case protocol](docs/evaluation/issue-18-protocol.md)
keeps all three workflows and caps a single comparison at 200 inference dispatches
(40 fixed, at most 160 agent). Use a fresh directory:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison --issue 18 \
  --ollama-url http://172.17.48.1:11434 --directory /tmp/issue-18-new-run
```

The `--issue 16` and `--issue 17` modes retain their archived twenty- and
thirty-case catalogs. The [forty-case results and acceptance evidence](docs/evaluation/issue-18.md)
include updated field scores, case changes and newly observed failures. Verify
the saved comparison and family/chronology checks without network or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue18_verify.py
```

Issue #19 adds the final [ten reviewed cases](docs/evaluation/cases-forty-one-through-fifty.md),
bringing the catalog to fifty. After issue #56 / PR #57 merged, a
[separate frozen comparison](docs/evaluation/issue-19/post-quality/protocol.md)
measures the merged detail-recognition and label/quote-pairing fixes on those
same cases. It retains the three workflows and selected model, with at most
250 inference dispatches. Keep Ollama running, use its current Windows host
address and choose a fresh directory:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison --issue 19 \
  --ollama-url http://172.17.48.1:11434 \
  --baseline docs/evaluation/issue-19/post-quality/baseline.json \
  --protocol docs/evaluation/issue-19/post-quality/protocol.md \
  --directory /tmp/issue-19-post-quality-new-run
```

The [comparison after merged fixes](docs/evaluation/issue-19-post-quality.md)
records field scores, latency, cost, failures and remaining review. The
[original fifty-case comparison](docs/evaluation/issue-19.md) remains archived
with its original source and results. Changed or unavailable public content is
flagged before inference. Earlier `--issue 16`, `17`, `18` and `56` modes retain
their archived catalogs. Audit the updated fifty-case run offline with:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue19_post_quality_verify.py --check-only
```

### Verify the stacked classification evaluations

From a full-history clone, run the four offline audits. They read saved outputs,
case annotations and the original Git objects. They require neither credentials
nor a model server.

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_flash_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue60_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue59_verify.py
```

**#20 — hosted quality reference.** Three hosted models processed the same 50
cases and cutoffs using the old label/quote contract. The recorded experiment
reserved US$1.530026 and reported US$0.20073915 in inference charges against
the shared US$5 cap. For historical reproduction, the GPT-4.1 protocol command
belongs in a checkout of `8fba053`. The Flash command belongs in a checkout
of `52fbc8d`, which contains the GPT-4.1 results and ledger it reads.
Running these paid commands at the current tip uses a different classifier.
A fresh paid experiment has its own output directory and spending decision.
[GPT-4.1 evidence](docs/evaluation/issue-20.md) · [Flash evidence](docs/evaluation/issue-20-flash.md)

**#60 — label availability.** The indexed-quote contract makes every type
reachable. Qwen retained 29/50 agreement with six gains and six regressions.
The archive includes the failed free-quote candidate, both budgets and pending
human review. [Comparison](docs/evaluation/issue-60.md)

To regenerate the before and final availability rows, use the current audit
driver with each frozen Python package. From the repository root after
`uv sync --locked --group dev`, the commands below read public GitHub evidence,
verify openings and capture label options with zero model dispatches. Set
`GITHUB_TOKEN` in the environment for authenticated GitHub read limits.

```sh
audit_dir=$(mktemp -d)
for revision in 1e4aec5 8d52071; do
  mkdir "$audit_dir/$revision"
  git archive "$revision" src | tar -x -C "$audit_dir/$revision"
  phase=before
  if [ "$revision" = 8d52071 ]; then phase=after; fi
  PYTHONPATH="$audit_dir/$revision/src" .venv/bin/python \
    src/maintainer_copilot/classification_evaluation.py --availability-only \
    --phase "$phase" --directory "$audit_dir/$phase"
done
```

Each output `results.json` records the audit driver hash, the frozen package
hashes and one preflight row per case. Check `error`
before interpreting `expected_reachable`: a flagged opening has a null result.
The corresponding stored rows are in the #60 `before` and `followup` directories.

**#59 — docs versus question.** Both prompts returned docs for pytest #12377
and missed the obsolete-helper counterexample. The candidate is confined to
the diagnostic runner. [Paired results and reproducer](docs/evaluation/issue-59.md)

The [#62 local comparison](docs/evaluation/issue-62.md) measured the installed
Qwen 3B and 7B models on the corrected contract. A separately capped
[downloaded-model comparison](docs/evaluation/downloaded-models/scored/report.md)
then measured Qwen3.5 4B at 38/50, Qwen2.5-Coder 7B at 34/50 and Gemma 4 E2B
at 32/50 exposed historical type agreements. All three matched 5/6 reviewed
synthetic expectations. These results leave the default-model decision open;
semantic support and reply usefulness remain pending. See the
[publication review](docs/evaluation/local-comparison-review.md).

Audit the additional measurements without model calls:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue62_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/downloaded_model_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/downloaded_scored_results.py
```

The requested [triage-quality follow-up](docs/evaluation/issue-56.md) preserves
the forty cases and all prior results. It fixes report-detail recognition and
model label/quote pairing, then measures one separately frozen comparison with
`--issue 56`. Reproduce the saved comparison audit without inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue56_verify.py
```

Its report-review sidecars explicitly attribute semantic/usefulness judgments to
Codex. Original pending independent human-review files remain unchanged.

The [remaining quality fixes and final measurement](docs/evaluation/issue-56-follow-up.md)
cover observed body failures, working controls, version identities and required
investigative questions while preserving the earlier passes. Audit the final
saved pass with `PYTHONPATH=src uv run --locked --no-env-file python scripts/issue56_followup_verify.py`.

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

Open <http://127.0.0.1:8000> to paste an issue. Enter its selected repository issue number
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

## Inspect repository source

`GET /api/source` accepts a full lowercase 40-character commit SHA, a relative
repository file path, and a positive line number. For example:

```sh
curl --get http://127.0.0.1:8000/api/source \
  --data-urlencode 'commit=36eed6b7b0eb59760fc4b33e90bdaac5057388f0' \
  --data-urlencode 'path=src/_pytest/capture.py' \
  --data-urlencode 'line=1014'
```

The response contains at most 11 lines around the requested line, a GitHub
permalink, and the commit and path that were read. Inspection uses the selected registration (pytest by default), 256 KiB per file, and 4,096 excerpt
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

Issue #48: [diagnosis, bounded fixes and evaluation evidence](docs/evaluation/issue-48.md).
Final human review: 3 useful, 7 partly useful and 10 not useful; retrieval-score regressions and remaining failures are recorded.

Issue #50: [bounded drafting experiment and retain-baseline decision](docs/evaluation/issue-50.md).
All sixty replies received explicit human review. Drafting failed the frozen
promotion thresholds; the default remains the selected 3B selection-only path.
The experimental MODEL_DRAFTING=1 path is retained for inspection, not promoted.

Issue #16 compares the keyword-rule baseline, fixed legacy RAG workflow and bounded
agent on the same twenty cases. Read the [frozen comparison protocol](docs/evaluation/issue-16-protocol.md)
before running a new experiment. The evaluator verifies the preserved baseline
and exact selected 3B identity/settings, freezes public evidence before timing,
and refuses to overwrite or resume a started directory:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison \
  --ollama-url http://172.17.48.1:11434 --directory /tmp/issue-16-new-run
```

Use the current Windows host address from the local model guide. This command
performs real inference: one pass, no warm-ups/retries, at most 100 dispatches.
It retains reports, traces, responses, a durable request ledger, paired field and
resource metrics, plus a fresh blinded review sheet and separate identity key.
Human usefulness and semantic citation support stay pending until explicitly
reviewed; automated field scores cannot authorize promotion. Keep the selected
3B and fixed legacy demo default unless every protocol gate passes.

The [completed #16 comparison and acceptance evidence](docs/evaluation/issue-16.md)
retain the fixed legacy workflow: no paired exact-field gain from the agent,
with 1.70x p95 latency, 2.29x tokens and two additional partial reports.
Fresh human usefulness and semantic reviews remain explicitly unverified.

Issue #17 expands the same three workflows to thirty cases. The
[expansion protocol](docs/evaluation/issue-17-protocol.md) preserves the prior
twenty-case artifacts, keeps the selected model and legacy prompts, and caps a
single pass at 150 inference dispatches (30 fixed, at most 120 agent). The
original `--issue 16` mode still selects its original twenty cases. For a new
thirty-case run, use a fresh directory:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison --issue 17 \
  --ollama-url http://172.17.48.1:11434 --directory /tmp/issue-17-new-run
```

The [completed expansion and acceptance evidence](docs/evaluation/issue-17.md)
separate changes on the original twenty from scores on the new ten. Verify the
published metadata, partition checks, run accounting and score deltas offline:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue17_verify.py
```

Case confirmation does not rate generated replies. Fresh semantic citation and
reply usefulness reviews remain separate; the fixed legacy demo stays default.

Verified historical replay accepts full openings up to 65,536 characters while
live requests retain the 16,000-character limit. See the
[replay follow-up](docs/evaluation/issue-17/follow-up/README.md) for the oversized
case check. The offline verifier reads application source from the original
`8640bae` inference commit, so that commit must be available in the checkout.
