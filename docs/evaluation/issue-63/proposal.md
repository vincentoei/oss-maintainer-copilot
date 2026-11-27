# Issue #63 promotion evaluation proposal

Status: prepared protocol, awaiting final review/source freeze and explicit
execution approval. The requesting user confirmed all twelve proposed types
in three explicit batch replies. No #63 model calls have been made. The application
default remains Qwen2.5-Coder 3B. This proposal cannot authorize its own execution.

## Baseline and annotation

Review/publication PR #64 merged as `28f3d36`, retaining #62 and the separately
capped downloaded-model comparison plus a reviewed transport-audit correction.
That merge is this preparation's baseline. Preserve all prior artifacts;
do not rerun the fifty historical cases to create a new overall score.

`proposed-cases.json` has twelve new investigator-designed synthetic openings:
four ordinary bugs, three regressions, three questions, one documentation defect
and one deliberately insufficient report. The three batch questions sent to the
requesting user contain the complete text and proposed types. All three replies
explicitly confirmed their four proposed types; attribution is stored separately
from generated-report review. These designed observations cannot establish
unseen real-world generalization. The documentation pair shares a title and
contrasts correction of guidance with help applying correct guidance; the log
and exit-status pairs contrast longstanding failure with a verified version break.

Annotation rubric: classify a reported malfunction as bug; prefer regression
when a credible unchanged-project working-to-broken/rollback comparison supports
it. A request for help applying functioning behavior is a question. A requested
correction to published guidance is docs. Insufficient evidence/intent permits
null. These rules guide review only; they are not added to the model prompt.
Retain uncertainty rather than changing expectations to fit predictions.

## Proposed arms and settings

| Arm | Installed alias | Manifest digest |
| --- | --- | --- |
| Current-default control | `pytest-triage:coder3b-ctx16k` | `3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8` |
| Existing quality reference | `pytest-triage:coder7b-ctx16k` | `863fd25a4686b53c56c1a178816edc5ede1c859fc40233e35ad5d8a898e3f7cc` |
| Candidate | `triage-eval:qwen35-4b-16k-v1` | `8da535b12863762c2403ed06956d92da4e57806a4772ba321137a2809e9a8bbe` |

All are GGUF Q4_K_M on the existing Windows Ollama 0.40.16 / RTX 5060 Laptop
8 GB setup. Reverify rather than assume the endpoint address or free resources.
Freeze native templates/renderers/parsers, effective parameters and tokenizer
metadata from read-only inspection before execution. Keep context 16,384,
temperature 0, seed 42, top-k 20, top-p .8, repeat penalty 1 and explicit
`reasoning_effort: "none"` in all three arms. Keep the current classification
prompt, excerpt sampler, schema, retrieval and validators. Use the new opt-in
`MODEL_REASONING_EFFORT=none` application setting rather than rewriting outgoing
bytes in an evaluation adapter. Unset preserves the old payload. The control's
explicit-off field differs from the ordinary deployed 3B request; its first
charged request is its compatibility gate. Do not silently change mode if refused.

One serial model at a time, 20 seconds and at most 256 output tokens per call,
65,536 response bytes. Begin each arm with the first fresh case after unloading
the preceding runner; no model-bearing prompt may be sent to warm it. Record
the administrative unload separately and verify empty residency before the
charged cold request. Record cold loading and cache state; fixed arm order
3B → 7B → Qwen3.5 limits performance interpretation.

## Proposed request set and budget

| Cohort | Exact inputs and paths | Maximum calls |
| --- | --- | ---: |
| New synthetic quality cases | All twelve confirmed openings, fixed triage, once per arm | 36 |
| Previously exposed bug-loss diagnostics | pytest #12219, #12223, #12249, public historical replay with original cutoffs, hashes and full original candidate catalog, once per arm | 9 |
| Candidate fixed integration | `integration-inputs.json` short and 15,900-character long input, each through Python fixed triage, POST `/api/triage`, and browser submission | 6 |
| Candidate bounded-agent integration | The same short and long inputs, each through POST `/api/agent/triage`; one permitted `finish` planner choice and one final classification | 4 |
| **Total** | **Three fixed arms plus candidate-only integration** | **55** |

Ceiling: **55 local calls / 14,080 output tokens**, zero model downloads, hosted calls,
API fees, retries, repairs, substitutions, uncharged warm-ups or extensions.
Hardware/electricity costs remain unmeasured. Unused planner slots are not
transferred to other requests. The two integration inputs reuse the synthetic
exit-status bug and are not extra fresh quality observations. The long input
adds a fixed sequence of synthetic observation lines and a final sentinel; do
not infer model-side input preservation from a successful short response.

The agent integration inputs provide no issue number or source location, so
their only permitted action is `finish`; these checks cover planning-to-final
reporting and do not exercise search or inspect transitions. Existing deterministic
agent/replay tests cover tool restrictions and unrelated retrieval/detail behavior
separately. All 55 exact serialized model requests have now been captured with
simulated responses, including the actual browser form/backend. Before approval,
publish the clean runner/config revision and final reviewed input/request hashes;
reserve each actual payload hash before HTTP. Pin source evidence for
agent reads and historical diagnostics; a missing/changed opening remains a
flagged row, not a substituted input. Refuse reused directories, duplicate slots,
unknown payloads, changed identities/settings, response limits or a non-local
route. Reserve failures durably before dispatch. Halt on identity/effort or
ledger drift and publish the partial run; do not restart the allocation.

## Decision gates proposed before results

These are practical minimum gates for this small portfolio evaluation, not
statistical significance or a guarantee of production reliability:

1. All twelve candidate fresh responses must pass application validation and
   complete without transport errors. At least 10/12 must match reviewed types,
   with at least 2/3 regressions and 2/3 questions correct, and both the docs and
   null sentinels correct. Candidate total must be no lower than either control,
   and ordinary-bug agreement must be no lower than either control. Always publish
   all per-class outcomes, including any gains offset by new losses.
2. Preserve all three exposed bug-loss expectations and review the candidate's
   actual reports/quotes. Do not force their labels or change the rubric after
   inference. Unresolved semantic disagreements require a documented tradeoff;
   they cannot be hidden by the new-cohort score.
3. All candidate application integration reports must reach final classification
   within their per-call and agent limits with no exposed reasoning. Expected
   partial reports for unavailable evidence are distinguished from model failures.
   The known issue text, selected quotes, citations and bounded actions must pass
   the existing public guardrails. Record full end-to-end timing separately from
   model latency, cache use, sampled device memory and reported runner placement.
4. Produce method-hidden review sheets for all 36 fresh, nine diagnostic and eight
   integration reports, keyed to original input and report fingerprints. Ask the requesting
   user to rate semantic type support, quote relevance, reply usefulness (0/1/2)
   and unsupported claims with reasons. Do not copy earlier ratings. A promote
   recommendation requires completed candidate review (including integration), no unsupported factual
   claim, no irrelevant type quote, and no candidate reply-usefulness loss against
   matched rated controls. Unrated comparisons remain pending, not assumed wins.
5. Reject promotion or mark it inconclusive if these gates fail or essential
   evidence is unavailable. Report observed prompt counts plus the 256-token
   allowance against the window and keep truncation unknown when independent
   evidence is absent. No sampled-memory or API field proves physical placement
   of every tensor. Keep such uncertainty in the final recommendation.

Do not modify the default as part of the measured run. Publish the scorecard,
per-case changes, errors/abstentions, review attribution and decision rationale;
any actual promotion follows the reviewed decision. No new model/prompt search
is authorized by a negative result.

## Remaining preparation

The bounded runner, independent audit and 55 captured request hashes are prepared.
Separate Standards and Spec reviews found no remaining preparation blockers.
Commit the input/source/serving freeze, then obtain approval for that exact
allocation. Generated-report human review is a
separate later step after inference. No #63 inference is authorized merely by
this protocol or an approval of expected types.

## Accounting and reproduction notes

The runner reserves a hashed slot before HTTP and retains the model transport
guard in a closed state during and after temporary app shutdown. A late worker
cannot regain an unguarded model transport. Interrupted reservations remain
charged even when a report or response file is missing; the scorer marks those
observations charged-without-result and awards no agreement. Native version,
alias, template/settings and metadata are checked before and after observations.

Reported GPU placement is recomputed from the captured matching digest, 16K
context and positive equal total/GPU byte counts. This remains API-reported
placement rather than proof about physical tensors. Wall timing excludes the
sampler's exit join and metadata reads; browser integration includes browser
startup and tool verification. Native reported cache use and unknown token
counts are retained separately from latency.

The offline scorer replays fresh and public integration inputs through the
application. It also replays historical diagnostics when the retained, hashed
local snapshot is present; otherwise it explicitly identifies their quote/reply
fields as not replayed. Browser output was checked against the actual API report
at execution; offline API replay does not rerun the original browser session.

Browser tools are pinned in `browser-tools.json`. The existing Chromium needed
two small Ubuntu NSS/NSPR packages (about 1.56 MB) extracted under `/tmp` during
preparation, with no system install or model download. Their binaries are hashed
and checked before execution; a missing or changed dependency refuses the run.
