# #62 · Local classification under the indexed-quote contract

**Qwen2.5-Coder 7B improved agreement on these cases.** On 50 exposed historical
openings it scored **34/50** to the contemporaneous 3B control's **29/50**, with
seven gains and two regressions. On six separately reviewed synthetic openings
it scored **5/6** to **3/6**. Both arms completed every call with a valid,
non-null selection. The largest historical gain was recognizing regressions.
Help requests with failure symptoms remain a weakness.

The 7B is a viable local quality reference on the existing laptop. Its
historical median model-call latency was 895 ms versus 537 ms, with 5,370
versus 2,754 MiB peak sampled device use. These results support using it when
reviewing the difficult categories. The limited cohorts and pending human
report ratings give insufficient grounds to promote it as the application
default. [Offline scores and confusion matrices](issue-62/results.json)

## Historical comparison

Both arms saw the same 50 verified openings and candidate pools, with zero
changed/unavailable cases and 50 common valid pairs. The control reproduced
all 50 archived #60 type selections. A gain means the 7B matched an accepted
type the control missed. A regression means it lost an agreement the control
had. Historical issue numbers in this section belong to pytest-dev/pytest.

| Expected historical type | Count | 3B predictions | 7B predictions |
|---|---:|---|---|
| Bug | 13 | 13 bug | 13 bug |
| Regression | 8 | 1 regression, 7 bug | 5 regression, 3 bug |
| Question | 7 | 7 bug | 1 question, 6 bug |
| Docs | 4 | 1 docs, 2 enhancement, 1 bug | 3 docs, 1 bug |
| Enhancement | 14 | 14 enhancement | 12 enhancement, 2 docs |
| Selftests | 2 | 2 bug | 2 bug |
| Proposal | 1 | 1 enhancement | 1 enhancement |
| Null | 1 | 1 bug | 1 bug |

- Four regression gains were pytest #12263, #12308, #12328 and #12367. Both
  models still recognized all 13 expected bugs. This improved specificity
  on these reports without a compensating loss on expected bugs.
- The 7B recovered the fixture-lifetime question #12298. Six other questions
  still went to bug. The accepted null on #12278 also went to bug in both arms.
- Documentation requests #10156 and #12228 moved from enhancement to docs.
  Both arms retained docs for the obsolete `pytest.config` report #12377 and
  incorrectly returned bug on #12360. In the opposite direction, #12290 and
  #12363 requested enhancements to the docs website; the 7B assigned docs.
  In both it cited the feature-template heading. These are the two regressions.

## Fresh, user-reviewed synthetic contrasts

The requesting user confirmed all six proposed types before inference. Each
pair shares a title and changes the opening body. The 7B got both members of
two pairs right; the 3B completed none of the three pairs correctly.

| Opening | Expected | 3B | 7B |
|---|---|---|---|
| XML A, duplicate entries in both versions | bug | bug | bug |
| XML B, older version writes one entry and switching back restores it | regression | bug | bug |
| Filter A, marker selection works and author asks how to include another test | question | bug | question |
| Filter B, selection also includes an unmarked test | bug | bug | bug |
| Paths A, asks to correct a contradictory reference sentence | docs | docs | docs |
| Paths B, working reference example and a one-invocation usage question | question | docs | question |

The fresh XML result limits the inference from the four historical regression
gains. The filter pair likewise shows that label agreement alone is incomplete:
the 7B got Filter A's type right while selecting the short final fragment
“g either file?”. No human rating of that quote or reply is attributed here.
These are designed contrasts with user-reviewed types. They provide six
observations, separate from the historical cohort. [Exact openings](issue-62/proposed-contrasts.json) · [Type confirmation](issue-62/contrast-review.json)

## Serving cost and validation

| Cohort / arm | Calls | Input / output tokens | Model p50 / p95 ms | Replay p50 / p95 ms | Sampled peak MiB |
|---|---:|---:|---:|---:|---:|
| Historical 3B | 50 | 96,216 / 1,680 | 537 / 1,824 | 542 / 1,833 | 2,754 |
| Historical 7B | 50 | 96,216 / 1,449 | 895 / 3,427 | 911 / 3,437 | 5,370 |
| Reviewed synthetic 3B | 6 | 2,716 / 174 | 312 / 349 | 312 / 349 | 2,754 |
| Reviewed synthetic 7B | 6 | 2,716 / 150 | 459 / 489 | 459 / 489 | 5,370 |

All **112/112** reservations produced one HTTP 200 response and one report.
Zero model validation failures, transport errors, type abstentions, missing
token counts or rows without GPU measurements. Zero downloads, hosted calls,
repairs or retries. Model API cost was **US$0**. Per-call records preserve the
bounded provider response, selected index, mapped quote, latency, usage,
status and GPU samples. [Durable ledger](issue-62/run/reservations.jsonl) · [Control reports](issue-62/run/coder3b-ctx16k/) · [Candidate reports](issue-62/run/coder7b-ctx16k/)

The 3B arm ran first. Its first call took 5.73 s with neither model resident
before the arm. The 7B's first call took 6.24 s with the 3B resident before
switching models. Each arm ended with one 16,384-context model resident and
Ollama reporting its full size in VRAM. These first-call times include request
processing as well as loading. The largest reported prompt was 14,970 tokens
for both models; all reported prompt-plus-output totals fit the configured
context. The API supplied no independent prompt-truncation flag. GPU peaks
are device-wide samples, including other processes. Token counts and latency
describe one serial pass; energy and total operating costs were unmeasured.

## Acceptance evidence

| Requirement | Evidence |
|---|---|
| Updated main, preserve history, independent scope | New investigation from merge `6d7fe21`, tracked in [#62](https://github.com/vincentoei/oss-maintainer-copilot/issues/62). Catalog, previous ledgers, #20/#59/#60 artifacts and production classifier/default are preserved. |
| Inspect hardware; name hypotheses, arms and constraints | [Read-only inventory](issue-62/serving-inventory.json) and [approved protocol](issue-62/protocol.md). Both installed Q4_K_M aliases ran on Ollama 0.40.16 with the same template, sampler, seed, context and limits. The 3B measures control drift; 7B tests a second same-family checkpoint. |
| Preserve taxonomy, evidence, contract and application behavior | The [preparation manifest](issue-62/preparation.json) matches all 50 #60 prompt/input/schema hashes, output limits, candidate IDs and opening metadata. A stub serialized both aliases on all 56 inputs. The live budget guard matched the full request-body SHA before each HTTP dispatch. Historical replay revalidated openings against one shared snapshot. No #59 guidance or additional tools. [Run preflight](issue-62/run/preflight.json) |
| Separate human expectations and freeze before dispatch | User confirmed all six fresh types and authorized the bounded run. Freeze commit `f6865f3` pins runner `48bb6f3`, reviewed texts, both model identities, settings, explicit budgets and file hashes. [Freeze](issue-62/freeze.json) |
| Full denominators, errors, confusion, gains/losses and resource observations | Both tables above and the [machine-readable summary](issue-62/results.json). Error/skip rows cannot earn agreement, and the offline scorer retains undispatched and charged-without-result rows if interrupted. |
| Deterministic validation and review | Both aliases passed fixed and historical-replay wire-parity and foreign-label rejection tests. Budget tests cover altered or unknown payloads, restarts, duplicate reservations and both limits. Independent review before dispatch led to checks for unexpected response model identity, lossless bounded error evidence, missing usage and partial-run scoring. Offline fault simulations covered all four. Full suite 504 passed, two opt-in public replay tests skipped; Ruff and mypy passed. |

From a full-history clone with the project environment, these commands audit
the prepared inputs and recompute the scored publication without calling
Ollama or GitHub:

```sh
PYTHONPATH=src .venv/bin/python scripts/issue62_verify.py
PYTHONPATH=src .venv/bin/python scripts/issue62_results.py | diff - docs/evaluation/issue-62/results.json
```

**Remaining unverified.** The 50 historical cases were already exposed during
development. The six synthetic openings are small and intentionally matched.
Some accepted types depend on judgment about intent, causation or the target
of a requested change. Evidence proves quote provenance; fresh human judgments
of semantic support, abstention quality and reply usefulness remain pending.
This run gives no vLLM throughput result, new-contract hosted score, or
estimate of general performance on incoming issues.
