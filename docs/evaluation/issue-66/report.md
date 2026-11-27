# Issue #66: diagnosis and unadopted correction

**Decision: retain the unchanged application; the proposed correction is
inconclusive until separately approved model execution and human review.**
There is no new semantic effectiveness result. This investigation prepared an
experiment, not a semantic validator or a repaired model. The #63 recommendation
and its explicitly accepted limitations remain in effect.

Started from updated `main` at `2194e338e2a82a9f54ab1ef06903944508523fa3` on
`issue-66-semantic-support`. Work is confined to #66; no reply-usefulness work,
model search, training, download, hosted inference or production change.

## Diagnosis from saved outputs

The public path is `triage_issue` (or historical `replay_case`) →
`OpenAICompatibleModel.generate` → structured selection decode →
`generate_validated` → `TriageReport`. The model receives the complete issue and
all resolved type labels plus null, independently of label wording. It also
receives at most 16 label-independent quote options: nonempty 160-character
line chunks, uniformly subsampled when there are more than 16. A type and quote
index must abstain together. The selected index resolves to an original excerpt;
validation checks allowed labels, null pairing, exact issue-text membership,
length, schema and vetted reply citations. It does **not** check whether a quote
entails a category. The report validates citations and context ownership, not
type/quote semantic entailment.

The [offline diagnosis](diagnosis.json) reproduces each original Qwen3.5 request
hash and **complete report** from its archived raw response. It verifies the
report fingerprint against the attributed #63 review before copying that review
as prior evidence. Those prior judgments remain the independent Codex/AI review
of #63; copying them here is not a second independent rating or human review.
The implementing Codex agent also inspected the full hash-verified local opening
and every actual offered quote. Full historical openings and option sets remain
local under ADR-0003.

| Diagnostic | Type inference | Selected quote | Sampler contribution / uncertainty |
| --- | --- | --- | --- |
| R48 / pytest #12219 | Regression remains uncertain: older documented hook support and a malfunction do not demonstrate that the same affected project worked before a version change. The minimized current-version example works. Broad bug is supported. | The chosen fragment reports the hook not running; it has no version comparison, so it does not support regression. | All 16 options were inspected. None establishes a credible working-to-broken version comparison; better sampling cannot manufacture missing historical evidence. The sampler also omits some opening context, but the full opening still does not demonstrate the comparison. Whether an older affected-project reproduction would establish regression remains unknown. |
| R40 / pytest #12223 | Enhancement is defensible as a request for output-size control; bug is defensible as broken consumer interoperability. This is taxonomy ambiguity. | The chosen fragment describes parser failure; it omits the requested output control, so enhancement quote relevance remains uncertain. | The explicit request to reduce only the message attribute appears in the full opening but **is absent from all 16 offered options**. This is a real sampler omission as well as a quote-selection concern. Prompt guidance alone cannot select that omitted request. |
| R26 / pytest #12249 | Enhancement is defensible as extending normal filtering to an earlier phase; bug also fits the filtering gap. | The offered and selected chunk contains both inability to control warnings and requested suppression; the prior review supports both type and quote. | The sampler clips the sentence, but retains the operative limitation and request. It did not prevent support here. Linked CI remains unavailable; no external technical diagnosis is inferred from that absence. |

All three archived expected types remain **bug**, and the candidate's old
**0/3 versus both controls' 3/3** exact benchmark result is preserved. Semantic
defensibility of an alternative never rewrites an expected outcome. R48 is
explicitly exposed diagnostic evidence, not a new holdout. No finding isolates
model size as the cause: the observed path permits a valid but unsupported
selection, with a separate sampler limitation in R40. The proposed prompt tests
one explanation without changing the model, sampler or validator.

## Proposed correction and frozen comparison

The [protocol](protocol.md) declares the exact candidate, nine AI-reviewed new
positive/counterexamples, original expected outcomes for twelve old synthetic
cases and three diagnostics, request/settings hashes, adoption gates and cap.
The [candidate](../../../scripts/issue66_candidate.py) exists only in evaluation;
the application's prompt remains unchanged. It asks the model to verify both
whole-issue type support and selected-quote support, retain credible version
evidence for regression, distinguish extension requests, and abstain if the
sampler offers no supporting quote. This may increase abstention or lose correct
classifications; those outcomes are preserved and can reject adoption.

The public [request manifest](requests.json) freezes **48 local calls / 12,288
maximum output tokens**: 24 matched inputs per arm using the same recommended
Qwen3.5 artifact. All exact serialized requests were captured through real report
construction, with a simulated null response and real sockets denied. The audit
proves the only outgoing difference is the candidate's system-prompt suffix;
all labels and null remain offered. The sampler stress example proves the full
issue can contain decisive evidence absent from every selectable quote.

These are **structural preparation checks, not model predictions**. No new
candidate/control semantic gains, losses or abstention rates have been measured.
The proposed executor preserves raw responses, attempted-dispatch reservations,
reports and failures; current serving identity and live transport still require
verification. Human confirmation of new expectations and actual generated-report
review are pending. The gates cannot pass without that evidence. No correction
has been adopted and no negative live experiment is claimed.

## Acceptance evidence

| #66 acceptance criterion | Evidence / status |
| --- | --- |
| Diagnose public evidence-selection/validation using saved outputs; distinguish inference, quote, taxonomy and sampler issues | **Verified offline.** Three original full reports and request hashes rebuilt by `issue66_prepare.py --check`; R48/R40/R26 analysis above and attributed ratings in `diagnosis.json`. All 53 old reports also replayed by the unchanged #63 auditor, reproducing its entire scorecard exactly. |
| Bounded correction and reviewed ordinary bug/regression/ambiguous enhancement positive/counterexamples; preserve null and all labels; no lexical gating or historical answers | **Prepared.** Evaluation-only prompt suffix, nine reasoned examples with explicit implementing-AI attribution in `cases.json`, and public report test documenting the surviving semantic-validation limit. The public request audit checks every resolved label plus null in every schema. Human expectation confirmation remains pending; the examples are designed development probes. |
| Freeze exact requests, expectations, settings, criteria and cap before requesting execution approval | **Prepared and hash-frozen.** `protocol.md`, `requests.json`, `synthetic-requests.json`, `freeze.json` and local exact historical requests. Executor checks drift and uses durable pre-dispatch accounting. No new inference or downloads; the completed #63 allocation is untouched. |
| Compare unchanged control and candidate through actual public report construction; retain failures, abstentions, gains/losses and attributed type/quote inspection; expose R48 | **Partially verified, live comparison unverified.** Real public construction captures both arms and saved original diagnostics are reproduced and inspected. New model responses, paired semantic outcomes and actual candidate type/quote review do not exist because #66 authorizes no new model calls. The frozen experiment and executor prepare this step; simulation is not substituted for it. R48 remains explicitly exposed. |
| Adopt only on predeclared criteria; preserve artifacts; deterministic tests/static checks/offline audits; state guarantees accurately | **No adoption.** All 916 old evaluation/case files are hashed and preserved, #60's 50/50 type reachability and old 29/50 agreement replay unchanged, #63's original scorecard matches exactly. Deterministic/static verification and independent source review are recorded in `checks.json` and `review.md`. Semantic guarantees remain limited to structural validation; effectiveness and human review are pending. |

## Verification and limits

The new report test was run red before adding the evaluation candidate, then
green. It deliberately replays an unsupported regression selection and confirms
the exact quote reaches the final report. That test prevents presenting the
candidate as semantic enforcement. Targeted public model/API/report/budget tests
passed (54 tests). Mypy passes; the final full-suite, formatting and review
results are recorded separately in [checks.json](checks.json).

The initial sandboxed TestClient tests and #63 auditor stalled and were
interrupted. Their bounded, inference-free reruns outside the sandbox passed:
54 targeted tests and 53 complete archived reports with exact scorecard equality.
This is an environment limitation, not a model retry or reused evaluation slot.
`issue60_verify.py` also validates 434 older preserved files and all 150 archived
dispatch records without new inference. None of these historical records is a
new charge. No new actual report has been rated by a human, no live candidate
effectiveness has been established, and no generalization or semantic
certification follows from offline structural checks.
