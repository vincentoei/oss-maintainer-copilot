# Issue #20: requested DeepSeek and GLM Flash comparison

Both requested models completed **50 requests on the same fifty eligible cases**
without failed inference, missing usage, retries or repairs. Type agreement with
the confirmed annotations is **32/50 for DeepSeek V4.1 Flash** and **29/50 for
GLM 5.3 Flash**, compared with saved results of **31/50 for GPT-4.1** and
**29/50 for Qwen 3B**. DeepSeek's lead over GPT-4.1 is one case on this small,
previously exposed development set; it does not establish a general winner.

Exact OpenRouter-reported inference cost is **US$0.01807918** for DeepSeek and
**US$0.01142197** for GLM. The new passes total **US$0.02950115**; combined with
the earlier GPT-4.1 pass, total reported spending is **US$0.20073915**, below the
original US$5 cap. Total conservative reservations, including GPT-4.1's full
unrefunded allowance, are **US$1.530026**. No default model or workflow changed.

## Acceptance evidence

| Requirement | Evidence |
| --- | --- |
| Try the exact requested models | [Results](issue-20/flash/run/results.json) preserve requested/returned aliases `deepseek/deepseek-v4.1-flash` and `z-ai/glm-5.3-flash`, pinned DeepInfra FP8 and Z.AI FP8 providers, advertised dated versions and selected endpoint metadata. All 100 responses matched the requested model/provider. |
| Same eligible cases and cutoffs, with model version, requests, tokens and cost | Shared public preflight verified all fifty cases. Each model has fifty scored rows with unchanged opening cutoff/hash, repository commit, candidate list, expected outcome and original reviewer attribution. [Offline verification](issue-20/flash/verification.json) recomputes all 100 scores and checks frozen sources and preserved references. |
| Keep the original separate US$5 cap | The [shared ledger](issue-20/flash/run/hosted-requests.jsonl) retains 100 durable pre-dispatch reservations and 100 responses. Every cumulative sum includes GPT-4.1's US$1.183980 reservation and remains below US$4.999999. New reservations total US$0.346046, making US$1.530026 combined. Actual reported totals and token counts are independently audited. The shared-cap/restart/failure checks verify refusal before dispatch. |
| Separate predictions from reviewed outcomes | Every row keeps `report`, `expected_outcome`, `case_review`, model `scores`, `local_fixed_scores` and `gpt41_scores` distinct. All four paired aggregates use exactly the same fifty successful case IDs. Fresh semantic citation support and reply usefulness remain pending human review. |

## Freeze and model settings

The user selected these two models after the completed GPT-4.1 reference and
authorized use of the existing OpenRouter credential. Source correction
`52fbc8d8785230e1f1c406483335509896eb1cab`, the
[protocol](issue-20-flash-protocol.md), [model reasoning metadata](issue-20/flash/model-metadata.json)
and [source/reference freeze](issue-20/flash/freeze.json) were committed before
inference. The freeze commit is `f9f9f7b`; this pass began
**2026-11-25 16:03:58 UTC**. Earlier evaluator source, cases and artifacts remain
unchanged; their existing audit continues to pass.

| Setting | DeepSeek | GLM |
| --- | --- | --- |
| OpenRouter model alias | `deepseek/deepseek-v4.1-flash` | `z-ai/glm-5.3-flash` |
| Advertised dated version | `deepseek-v4.1-flash-20260910` | `glm-5.3-flash-20260826` |
| Pinned provider slug / returned provider | `deepinfra/fp8` / `DeepInfra` | `z-ai/fp8` / `Z.AI` |
| Advertised quantization | FP8 | FP8 |
| Frozen input / output US$/million | 0.14 / 0.42 | 0.15 / 0.50 |
| Reasoning effort / total completion cap | low / 4,096 tokens | low / 4,096 tokens |
| Temperature / timeout / response bytes | 0 / 120 s / 65,536 | 0 / 120 s / 65,536 |

The model catalog reports GLM reasoning mandatory; both passes therefore use low
reasoning. These settings differ from the earlier non-reasoning runs' 256-token
completion allowance. The issue input, fixed selection prompt, evidence view and
JSON selection contract are preserved. This comparison includes the cost and
latency consequences of those serving/settings differences; it is not a pure
weight-only experiment. Model order alternates for each successive case. Routing
fallback and automatic transforms are disabled, parameters required, and maximum
provider prices bounded before dispatch.

Advertised version names and quantization come from OpenRouter metadata;
completion aliases do not independently attest upstream weights or snapshots.
The request and response record those identity limitations rather than implying
stronger attestation. Provider invoices, credit purchase fees, taxes and unrelated
account activity are outside this recorded inference cost. The bound retains
the documented conservative input-byte/framing and provider-contract assumptions.
Credentials remain in ignored local storage and are absent from published files.

## Comparison and resources

Qwen and GPT-4.1 columns reuse their preserved prior fifty-case measurements;
neither was rerun. All four models have the same fifty paired cases. The two
Flash models each have four application-status partial reports caused by
unavailable historical CI, matching the earlier runs. Those are not inference
failures. All 100 model requests returned usable validated selections.

| Measurement | Saved Qwen 3B | Saved GPT-4.1 | DeepSeek V4.1 Flash | GLM 5.3 Flash |
| --- | ---: | ---: | ---: | ---: |
| Type agreement | 29/50 | 31/50 | **32/50** | 29/50 |
| Exact missing-detail agreement | 43/50 | 43/50 | 43/50 | 43/50 |
| Expected-earlier-issue retrieval | 6/50 | 6/50 | 6/50 | 6/50 |
| Relationship exactness | 2/47 | 2/47 | 2/47 | 2/47 |
| Structural citation checks | 50/50 | 50/50 | 50/50 | 50/50 |
| Inference requests | 50 | 50 | 50 | 50 |
| Input tokens | 81,934 | 81,499 | 82,076 | 78,639 |
| Total completion tokens | 1,287 | 1,030 | 15,687 | 1,418 |
| Reported reasoning tokens | non-reasoning path | non-reasoning model | 14,530 | 286 |
| Mean report latency, ms | 411.66 | 1,435.67 | 3,163.15 | 4,238.17 |
| Nearest-rank p50 / p95, ms | 301.230 / 855.583 | 1,340.106 / 2,372.882 | 2,310.097 / 6,680.974 | 3,180.676 / 11,792.107 |
| Reported marginal model API cost, US$ | 0, local Ollama | 0.171238 | 0.01807918 | 0.01142197 |
| Fresh usefulness / semantic support | pending | pending | pending | pending |

DeepSeek used substantially more reported reasoning tokens than GLM at the same
requested low effort. These are provider-reported counts. Low effort does not
imply equal computation across model families or providers. Decimal reported
costs are retained exactly; the ledger also keeps conservative full-rate
token-price estimates and upward-rounded microdollar totals. Cached-input
discounts can make reported cost lower than the full-rate estimate.

Missing-detail recognition and duplicate retrieval are deterministic parts of
this fixed workflow, so their unchanged scores do not establish equal model
ability on those tasks. Three uncertain relationships remain unscored, and
relationship exactness requires retrieving the annotated earlier issue even for
nonduplicates. Structural citation checks can pass vacuously and cannot establish
semantic support. Local hardware/electricity and total operating costs are
unmeasured. Timing comes from different providers and measurement times and
does not isolate model speed or establish a service-level guarantee.

## Case changes

DeepSeek corrects GPT-4.1's **#12223** disagreement, selecting the confirmed bug
type instead of question. It loses none of GPT-4.1's correct type predictions.
Against Qwen it gains **#12308**, **#12367** and **#12377**, without a type
regression. It still disagrees with eighteen confirmed type annotations.

GLM has no correct-type gains over GPT-4.1 and loses **#12360** and **#12363**:
it abstains on the former's docs type and predicts docs instead of enhancement
on the latter. Against Qwen it gains #12308/#12367/#12377 but loses
#12223/#12360/#12363, yielding the same 29/50 total with different failures.
At #12223 it abstains rather than selecting the confirmed bug type. The
[type-change artifact](issue-20/flash/type-changes.json) retains all prediction
differences, including changes where both predictions remain incorrect.

Expected outcomes and their accepted review attribution are unchanged, including
explicitly accepted Codex delegation; this is not a uniformly independent human
assessment. The #12083 detail annotation disagreement and other baseline
ambiguities remain visible. Development-case exposure, unknown model-training
overlap and single-pass variability limit generalization. No new human ratings
of generated reply usefulness or semantic support were supplied. This pass does
not authorize default-model promotion.

## Validation and reproduction

[Recorded checks](issue-20/flash/checks.json) passed lint, formatting, strict
typechecking, **28 focused hosted/Flash checks** and the full suite:
**472 passed, 2 skipped**. The skipped tests are opt-in public replay checks;
this pass independently verified public evidence for all fifty cases. The
[two-axis review](issue-20-flash-code-review.md) has zero Standards findings and
zero remaining Spec findings after correcting exact decimal-cost retention.

Audit every source/reference hash, all 100 recomputed scores, all 200 ledger
events and the common fifty-case cohort without credentials, network or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_flash_verify.py
```

The original `scripts/issue20_verify.py` audit also passes. With an environment
containing `OPENROUTER_API_KEY`, the protocol's command can start a new paid
experiment in a fresh directory. The archived pass is immutable; the original
cap applies to this recorded experiment, and no paid inference was repeated
after inspecting its results.
