# Classification agreement with thinking disabled

**Qwen3.5 4B achieved the predeclared historical gain.** It matched 38/50 expected types against the contemporaneous Qwen2.5-Coder 7B reference's 34/50, gaining seven cases and losing three. It recognized more regressions and questions, at the cost of three ordinary bugs. Gemma 4 E2B scored 32/50 with two gains and four losses. All three matched 5/6 on the separately reviewed contrasts. This makes Qwen3.5 a useful local reference for these difficult classes. The exposed cohorts and pending human ratings leave the 3B application-default decision open. [Frozen protocol](protocol.md) · [Full scorecard with all 56 cases](results.json)

## Fifty exposed historical openings

All 50 were eligible, and each candidate had 50 common valid pairs with the reference. The 7B reproduced all archived #62 historical and synthetic type selections. In the table a disagreement means the application accepted the output but its selected type differed from the recorded expectation. There were zero validation failures, transport failures, truncation of captured responses, valid abstentions or missing responses in any arm.

| Historical agreements | Qwen2.5-Coder 7B | Gemma 4 E2B | Qwen3.5 4B |
|---|---:|---:|---:|
| Bug (13) | 13 | 13 | 10 |
| Regression (8) | 5 | 4 | 7 |
| Question (7) | 1 | 1 | 4 |
| Docs (4) | 3 | 2 | 3 |
| Enhancement (14) | 12 | 12 | 13 |
| Selftests (2) | 0 | 0 | 1 |
| Proposal (1) | 0 | 0 | 0 |
| Expected null (1) | 0 | 0 | 0 |
| **Agreement / 50** | **34** | **32** | **38** |
| Valid disagreements / 50 | 16 | 18 | 12 |

Qwen3.5 called three of seven expected questions bugs, down from six for the reference. It called one of eight regressions a bug, down from three. In the opposite direction, one expected bug became regression and two became enhancement. Qwen3.5 retained the reference's docs result on all four docs cases. Gemma retained all 13 bugs, but called one expected regression backward compatibility and one expected question regression. The complete per-arm confusion matrices include every predicted type and the accepted null. [Confusion matrices and case predictions](results.json)

Each listed issue belongs to pytest-dev/pytest. A gain or loss is relative to the current 7B reference on a case where both decisions passed validation.

| Expected type | Gemma gains | Gemma losses | Qwen3.5 gains | Qwen3.5 losses |
|---|---|---|---|---|
| Bug | — | — | — | #12219 (regression), #12223 and #12249 (enhancement) |
| Regression | #12083 | #12263 and #12308 (bug) | #12083, #12293 | — |
| Question | — | — | #12189, #12242, #12287 | — |
| Docs | — | #12228 (enhancement) | — | — |
| Enhancement | #12290 | #12081 (bug) | #12290 | — |
| Selftests | — | — | #12352 | — |

## Six reviewed contrasts

The user reviewed these designed openings before #62. They are reused examples and were reported separately from the fifty. All six were eligible and all six were common valid pairs per comparison.

| Opening | Expected | 7B | Gemma | Qwen3.5 |
|---|---|---|---|---|
| XML A, duplicate entries in both versions | bug | bug | bug | bug |
| XML B, earlier version works and rollback restores it | regression | bug | bug | bug |
| Filter A, usage question about selecting an additional test | question | question | question | question |
| Filter B, selection includes an unmarked test | bug | bug | bug | bug |
| Paths A, correction requested to contradictory guidance | docs | docs | docs | docs |
| Paths B, working example and a usage question | question | question | question | question |

Each arm got both members of **2/3 pairs** right. Neither candidate gained or lost an agreement here. The explicit working-to-broken contrast in XML B still elicited bug from all three, despite the historical regression gains. [Reviewed openings](../../issue-62/proposed-contrasts.json)

## Serving measurements

| Cohort / arm | Input / output tokens | Model p50 / p95 ms | End-to-end p50 / p95 ms | Cache hits / calls | Peak device MiB |
|---|---:|---:|---:|---:|---:|
| Historical 7B | 96,216 / 1,449 | 948 / 3,200 | 952 / 3,208 | 49/50 | 5,370 |
| Historical Gemma | 97,301 / 1,606 | 393 / 725 | 396 / 733 | 48/50 | 5,370 |
| Historical Qwen3.5 | 96,385 / 1,463 | 859 / 2,805 | 862 / 2,815 | 49/50 | 4,278 |
| Reviewed 7B | 2,716 / 150 | 436 / 563 | 436 / 563 | 6/6 | 5,370 |
| Reviewed Gemma | 2,822 / 168 | 309 / 385 | 309 / 385 | 6/6 | 3,282 |
| Reviewed Qwen3.5 | 2,740 / 150 | 515 / 834 | 515 / 836 | 6/6 | 4,278 |

The first requests had zero cached tokens. The 7B started with no resident model and took **6.02 s**. Gemma took **10.58 s** with the 7B initially resident. Qwen3.5 took **6.28 s** with Gemma initially resident. Each case was dispatched once. The ordinary application tests ran during part of the reference arm and could contribute CPU or I/O noise. Fixed order, cold loading, native tokenization, Gemma's packaged speculative draft and prefix caching limit interpretation of latency. The six contrasts came last with a resident model. Among historical requests with cache hits, model p95 was 1,992 ms for 7B, 572 ms for Gemma and 1,598 ms for Qwen3.5.

GPU peaks are device-wide samples at 500 ms intervals. Gemma's historical 5,370 MiB peak includes the transition from 7B. Its highest sample after its first case was 3,282 MiB. Every post-call snapshot reported 16,384 context and equal positive GPU and total runner bytes for the pinned alias. Prior Windows measurements showed shared allocations and an unexpectedly small Ollama byte count for Gemma. These observations establish the reported placement and sampled use, with physical residency of every tensor unresolved. [Preflight telemetry](../preflight.md)

All three used the same serialized application inputs apart from alias. The largest reported prompt counts were 14,970 (7B), 8,493 (Gemma) and 14,970 (Qwen3.5). On pytest #12204, Gemma reported 8,195 input tokens for the opening for which both Qwens reported 14,970. Every reported input count plus the 256-token allowance fit 16,384. The endpoint supplied no independent pre-truncation length or truncation flag. Different reported counts alone cannot establish how much original text survived native rendering.

## Accounting, reproduction and limits

The freeze at `9680f9f` pins source `8ce9c03`, three exact manifests, native serving settings, 168 request hashes and the approved budget. The 7B's first charged request met every compatibility gate. All **168/168** durable reservations produced one HTTP 200, one stopped response, one application report and one trace. There were zero exposed reasoning characters. Actual output totaled **4,986 tokens** against the 43,008 ceiling. There were zero warm-ups, retries, repairs, model downloads or hosted calls in the scored phase. API fees were US$0; total operating cost and energy were unmeasured. [Freeze](freeze.json) · [Ordered request hashes](requests.json) · [Reservation ledger](run/reservations.jsonl)

The scored run used the evaluation-only `reasoning_effort: "none"` setting on every arm. The production default remains 3B. The historical data and the six designed contrasts have been exposed; no unseen holdout or new reviewer ratings were collected. An exact selected quote establishes provenance; semantic support, appropriateness of abstention and reply usefulness still require human review. No hosted or vLLM inference was part of this comparison.

Per-case files contain the bounded provider response, validated report, model and retrieval/tool trace, timing, GPU summary and residency. The scorecard includes every expected and predicted type and both candidate comparisons. [7B records](run/coder7b-ctx16k/) · [Gemma records](run/gemma4-e2b-16k-v1/) · [Qwen3.5 records](run/qwen35-4b-16k-v1/)

Recompute the publication offline from the repository root:

```sh
PYTHONPATH=src .venv/bin/python scripts/downloaded_scored_results.py | diff - docs/evaluation/downloaded-models/scored/results.json
```

With the locally retained, hash-verified public snapshot, this also exercises all 168 recorded responses through the production validation and replay paths. A metadata-only checkout audits the published records and replays the reviewed synthetic cases without bulk contributor issue text. All six earlier #20/#59/#60/#62 checks, the four-call downloaded-model preflight audit, Ruff lint/format and mypy passed. The application suite passed 504 tests with two opt-in public replay tests skipped.
