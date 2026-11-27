# Issue #66: semantic-support experiment proposal

Status: **prepared, not authorized or executed**. No new model calls, downloads,
hosted requests or spending. The current application is unchanged at baseline
`2194e338e2a82a9f54ab1ef06903944508523fa3`. This protocol cannot authorize itself.
The recommended Qwen3.5 4B configuration and #63's explicit policy exception stay
in effect. No archived expected outcome, response, rating or loss is rewritten.

## Bounded correction and review

The control is the unchanged application `OpenAICompatibleModel`. The candidate
is [SemanticSupportCandidate](../../../scripts/issue66_candidate.py), used only
by this evaluation. It appends one fixed system instruction to the real encoder.
It asks separately whether the full input supports a category and whether the
selected quote expresses its evidence. Regression needs a credible same-behavior
working-to-broken version comparison retained in the selected quote. Old feature
support alone is insufficient. A requested extension needs a quote expressing
the request. Where no offered quote supports a category, abstain.

No sampler, schema, validator, taxonomy, resolved label list, retrieval, report
construction or reply policy changes. No literal keyword requirement, per-issue
answer, extra model call, repair prompt or model substitution. The instruction
uses ordinary bug/regression/enhancement concepts only where the resolved
repository labels have those meanings; every resolved type plus null remains
reachable independently of lexical cues. This does **not** enforce semantic
support: an unsupported response can still pass structural validation.

[Nine proposed examples](cases.json) include ordinary bug and credible regression
positives, an old-manual counterexample, a retracted version claim, explicit
enhancement, ambiguous bug/enhancement, a failure-only quote counterexample,
insufficient intent and deliberately omitted support. Reasons and acceptable
alternatives were reviewed by the implementing Codex agent, with attribution in
the file. This is AI review after exposure to #63, not independent review, human
confirmation or fresh holdout evidence. The overlap example retains bug as its
preferred expected type and enhancement as a defensible semantic alternative;
both exact agreement and semantic support must be reported. The requesting
user's confirmation of these new expectations remains pending. The twelve
previously user-confirmed #63 examples keep their original expectations.

## Frozen requests and settings

`requests.json` lists all **48 exact serialized application request hashes**,
cohorts, expectations and denominators. `synthetic-requests.json` publishes the
42 synthetic request objects. Exact bytes for all requests, including historical
diagnostics, are retained in ignored `.local/issue66/prepared/`. Historical full
inputs remain local under ADR-0003; their hashes and cutoffs are already archived.
`freeze.json` pins the proposal, candidate/preparer/test/application source,
local historical snapshot, request artifacts and all pre-existing evaluation
and case artifacts. Changing any frozen input, instruction, expectation, setting
or gate requires a new reviewed freeze and execution approval before inference.

| Cohort, per arm | Inputs | Calls across both arms |
| --- | --- | ---: |
| New development examples | All nine `cases.json` entries | 18 |
| Previously exposed synthetic sentinels | All twelve #63 `proposed-cases.json` entries | 24 |
| Exposed historical diagnostics | pytest #12219 (R48), #12223 (R40), #12249 (R26), original openings, cutoffs and full candidate catalog via `replay_case` | 6 |
| Total | 24 per arm | 48 |

Both arms use **the same installed Qwen3.5 4B**, recommended alias
`pytest-triage:qwen35-4b-ctx16k`, digest
`8da535b12863762c2403ed06956d92da4e57806a4772ba321137a2809e9a8bbe`.
Use its unchanged Q4_K_M artifact, native template, parser and tokenizer metadata
as recorded in #63's promotion verification. Context 16,384; temperature 0;
seed 42; top-k 20; top-p .8; repeat penalty 1; presence penalty 0;
`reasoning_effort: "none"`; drafting off. Temperature, effort and output cap
are in the captured application payload; the other settings are native alias
parameters and must be checked before execution. Reverify identity/settings by
metadata reads without inference. Refuse a changed or unavailable alias rather
than downloading, substituting or silently changing settings. Actual current
serving identity, endpoint reachability and residency have not been verified
in #66. The proposed route is the previously recorded private local Ollama
endpoint `http://172.17.48.1:11434/v1`. A changed address requires a new freeze;
the executor refuses redirects and proxies.

Use fixed Python `triage_issue` for synthetic inputs and public `replay_case`
for the historical inputs. Every response must flow through the real model
decoder, `generate_validated`, report construction and `TriageReport` validation.
No standalone classification parser may replace the report. No new browser,
HTTP, agent, retrieval or reply-usefulness experiment is proposed here.

One serial request at a time, paired in manifest case order: control then
candidate. Each call is capped at 20 seconds, **256 output tokens** and **65,536
response bytes**. Total ceiling **48 local calls / 12,288 output tokens**;
zero retries, repairs, warm-ups, downloads, hosted calls or fee-bearing APIs.
All attempted dispatches, including transport errors and lost responses, consume
their slots. No unused allocation transfers between cohorts or arms. This is a
quality experiment; paired fixed order, prompt cache and residency limit any
latency interpretation. Hardware/electricity costs are unmeasured.

The [bounded executor](../../../scripts/issue66_run.py) verifies the freeze,
refuses a reused run directory, checks native metadata before and after every
observation, and uses `PairedBudget` to reserve each arm/case and exact body hash
durably before dispatch. It preserves raw bounded responses, reports, traces,
failures and interruptions, with no restart or retry. It requires the approved
freeze hash on the command line; that argument is a drift guard and does not
establish user approval. Its live transport remains unverified without approved
execution. Approval of this investigation alone grants no execution permission.

## Adoption criteria declared before results

These gates are small-set engineering safeguards, not a statistical guarantee.

1. All 24 candidate slots must complete as structurally valid final reports,
   without model transport errors. Preserve failures in the denominator. The
   insufficient-intent and omitted-support cases must abstain. All twelve old
   synthetic sentinels must retain their exact expected types, including docs,
   questions, regression and null; report paired gains and losses even if a
   different aggregate score would hide them.
2. All nine new candidate outcomes must match the declared acceptable set; retain
   and separately count any preferred-expectation disagreement in the overlap
   example. Every non-null selected type **and its actual selected quote** must
   be rated supported with a concrete reason. An uncertain or unsupported quote
   fails this gate; exact copying does not count as semantic review.
3. Inspect all three historical candidate reports. R48 must no longer select an
   unsupported regression/quote; a supported broad bug or explicit abstention
   is acceptable. R40 must have a supported selected type/quote or abstain; an
   unsubstantiated enhancement quote is unacceptable. Preserve R26's supported
   classification/quote or document any loss; a new unsupported selection or
   avoidable abstention where its supporting option remains available fails.
   All three original expected types stay bug. Publish historical exact-type
   gains/losses without pooling these exposed diagnostics as fresh evidence.
4. Produce an attributed per-report review for **all 48 reports**, including
   control, candidate, failures and abstentions. Review actual type support and
   quote relevance separately as yes/no/uncertain/N/A with reasons. Human review
   by the requesting user is required for adoption under this proposal; AI
   review can assist but must be attributed and cannot silently satisfy that
   gate. There must be no paired semantic-support loss against the control on
   the 21 synthetic inputs. Publish all exact-type gains, losses, common failures
   and abstentions, not only newly successful examples. Historical taxonomy
   disagreement is distinct from unsupported inference.
5. All non-type report fields must equal the matched control, including reply,
   citations, retrieval results and missing details (ignore trace IDs only).
   Existing deterministic guardrails and static checks must pass. Verify every
   frozen archive hash. Do not change the application until all gates pass.

Retain the control if any gate fails; declare inconclusive if required evidence,
human review or execution is unavailable. A negative result is valid and must
retain all failures and abstentions. No post-result loosening or annotation
rewrite is authorized. Even a pass establishes observed support on these small,
exposed/designed cases, not semantic certification, generalization, proof of
model input preservation or physical tensor placement. A sampler redesign is a
separate experiment; do not add it to this allocation after seeing results.

## Offline reproduction

From the repository root, with the retained hash-verified snapshot present:

```bash
PYTHONPATH=src .venv/bin/python scripts/issue66_prepare.py --check
.venv/bin/pytest -q tests/test_issue66_semantic_support.py tests/test_semantic_classification.py
```

Preparation patches the public model HTTP boundary and denies real socket
connections. It captures control/candidate requests through actual report
construction, proves the only outgoing difference is the prompt suffix, and
replays the three original raw Qwen diagnostic responses with exact request
hashes and full report equality. Null responses used to capture future requests
are explicitly simulated: their report hashes are structural preparation
evidence and **not candidate predictions or quality measurements**. The same
offline audit checks the deliberately omitted informative sentence stays in the
full issue but is absent from every offered quote. No failed live semantic
comparison has been claimed; no live comparison exists yet.
