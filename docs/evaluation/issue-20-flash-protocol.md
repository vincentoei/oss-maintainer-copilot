# Issue #20: requested DeepSeek and GLM Flash comparison

The user explicitly requested DeepSeek V4.1 Flash and GLM 5.3 Flash after the
GPT-4.1 comparison. This authorizes one additional pass per selected model on
the same fifty confirmed cases. Preserve all earlier artifacts, the selected
Qwen 3B/default workflow, every expected outcome and original reviewer attribution.
Keep the original evaluator unchanged so its source-freeze audit still passes.
No prompt tuning, model search, replacement cases or training is included.

## Frozen models and settings

| Model alias | Advertised version | Pinned provider | Input/output US$/million tokens |
| --- | --- | --- | --- |
| `deepseek/deepseek-v4.1-flash` | `deepseek-v4.1-flash-20260910` | `deepinfra/fp8` (DeepInfra, FP8) | 0.14 / 0.42 |
| `z-ai/glm-5.3-flash` | `glm-5.3-flash-20260826` | `z-ai/fp8` (Z.AI, FP8) | 0.15 / 0.50 |

Prices and supported parameters come from the public OpenRouter
[DeepSeek endpoints](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints)
and [GLM endpoints](https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints).
Before creating the run, read metadata again and require the exact provider slug,
provider name, advertised version, supported parameters and prices at or below
these ceilings. Retain selected endpoint metadata and the complete-response hash.
Version names remain provider-advertised; a completion alias does not independently
attest the upstream weights or dated snapshot.

The [public model catalog](https://openrouter.ai/api/v1/models) reports reasoning
mandatory for GLM, with low/high/max supported; DeepSeek also supports low.
Use **low reasoning for both**, **4,096 total completion tokens**, temperature 0,
120-second transport timeout and 65,536 response bytes. Reasoning tokens count
inside the completion allowance and are recorded separately where supplied.
These settings differ from the earlier non-reasoning models' 256-token budget;
disclose that cost/latency/quality comparison limitation. The issue inputs, fixed
workflow prompt and structured selection contract are unchanged. No images,
audio, model tools, drafting or free-form maintainer claims are requested.

Require strict JSON-schema output, supported parameters, no provider fallback,
no automatic transforms and the frozen maximum routing prices. Requests use the
already authorized `OPENROUTER_API_KEY` from ignored local storage. Do not print
or publish credentials. Do not publish full issue bodies, raw reasoning, or
unvalidated free-text responses.

## Cases, order and accounting

Verify exact catalog fingerprint, confirmation, IDs, cutoffs, commits, opening
hashes and candidate pools against the saved local and GPT-4.1 results. Acquire
public evidence in a shared preflight, retaining every flag; freeze reads and
failures before inference. Annotation fields and post-cutoff evidence remain
outside model inputs. One request per model per eligible case, at most 100 new
dispatches total. Alternate which model runs first for successive cases.
No warm-up, inference retry, repair, second pass or post-result adjustment.

The two models share one durable request ledger and the **original US$4.999999
cap**. Carry forward GPT-4.1's full **US$1.183980 reservation**, rather than
resetting its budget or refunding its unused allowance. Before every new POST,
lock and fsync a reservation: one input token per serialized request byte plus
4,096 framing/schema tokens, and all 4,096 output tokens at the frozen rates.
Calculate rates in integer nanodollars; round reservations and per-call costs
up to microdollars. Retain the provider's exact decimal reported cost as well.
Never release reservations. Check the cumulative prior plus new reservations
before dispatch, including after restart and when switching models.

Transport, identity, usage or cost uncertainty halts both models. Missing usage
stays unknown; interrupted/failed calls remain charged. Reject future calls when
a prior durable response contains an accounting error, even if a separate halt
marker was not written. Out-of-budget and repeated-case calls are refused before
HTTP. Truncated/malformed selections and report-validation failures remain
visible, retained and unscored; never score their fallback as model quality.

The bound retains the original protocol's conservative text-token/framing and
provider-rate assumptions. Unrelated account activity, taxes and credit purchase
fees are outside inference cost. A new run directory is mandatory. User selection
of these two new models supersedes the original single-model restriction only
for these separately frozen passes; it does not permit rerunning GPT-4.1.

## Publication and checks

Publish all 100 rows, model identities, request/reservation/usage/cost records,
failure types and provider settings. Distinguish predictions, confirmed expected
outcomes, original reviewer attribution, and pending fresh semantic/usefulness
review. Aggregate each model's available reports with explicit denominators;
compare Qwen, GPT-4.1 and both Flash models on exactly the common successful case
IDs. Preserve all exclusions and annotation ambiguity. Report type gains and
regressions, unchanged deterministic detail/duplicate fields, latency, reasoning
and total tokens, exact reported costs and conservative reservations. No automatic
model promotion follows from this development-set comparison.

Use the already agreed evaluation-runner and capped-client test boundaries.
Verify provider routing, reasoning accounting, shared cap across prior/current
models and restarts, failure halting, changed evidence, invalid selections and
common pairing. Run strict typechecking, focused tests, the full suite and the
two-axis code review before publishing. Commit source and protocol before paid
inference and audit the saved results offline afterward.

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.flash_evaluation --directory /tmp/issue20-flash-new
```
