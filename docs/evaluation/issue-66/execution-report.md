# Issue #66: completed semantic-support experiment

**Reject the proposed prompt correction and retain the unchanged application.**
All 48 approved local calls completed, but the candidate fails the predeclared
adoption criteria. It gains one correct abstention and loses one correct ordinary
bug classification; R48 remains unsupported and another historical quote loses
support. No application change, gate amendment or further inference follows.

The [pre-execution investigation](report.md) records diagnosis from saved outputs
before proposing the correction. Work started from updated `main` at
`2194e338e2a82a9f54ab1ef06903944508523fa3` on `issue-66-semantic-support`.
Preparation was committed at `7292553`. The requesting user then confirmed the
nine new expectations and approved the exact 48-call experiment in this
conversation. The [approval record](approval.json) identifies the unchanged
[freeze](freeze.json), SHA-256
`7754ad7a9e9c2700a7c5edafe7537258988a09ded1a9886da109556dd1bd1cd7`.
Frozen proposal status text records preparation; approval and results are
separate. No frozen input, expectation, setting, prompt, source, adoption gate or
old artifact changed after approval.

## Diagnosis and bounded correction

The real public path is `triage_issue` (or historical `replay_case`) →
`OpenAICompatibleModel.generate` → selection decode → `generate_validated` →
`TriageReport`. The whole issue and every resolved label plus null reach the
model. Independently, up to 16 nonempty 160-character line chunks are offered,
with uniform subsampling. No label requires a lexical cue. Validation checks
schema, allowed labels, paired nulls, exact quote provenance/length and vetted
citations; it does not establish semantic entailment.

The [original diagnosis](diagnosis.json) reconstructs all three saved Qwen reports
with exact request hashes and full report equality. It preserves #63's attributed
independent AI review. Full historical openings and sampler options were inspected
locally under ADR-0003. R48 lacks demonstrated working-to-broken affected-project
evidence; its hook-failure quote cannot establish regression. R40 is a defensible
bug/enhancement ambiguity, but its parser-failure quote omits the requested
control; the sampler actually omits that explicit request. R26's original quote
retains the filtering limitation and requested suppression. These are distinct
inference, selected-quote, taxonomy and sampler problems, with no model-size
attribution. All three issues are exposed diagnostics, never fresh holdout data.

The [frozen correction](protocol.md) appends evaluation-only prompt guidance
requiring whole-input and selected-quote support, credible version evidence for
regression, requested-change evidence for enhancement, and abstention when no
offered quote supports a category. It changes no sampler, validator, label list,
null behavior, retrieval or reply policy. The [nine reasoned examples](cases.json)
cover ordinary bug, genuine version break, ambiguous enhancement and their
counterexamples. AI authorship and subsequent user confirmation remain separately
attributed. No lexical restriction or historical answer was introduced.

## Execution and measured outcomes

Both arms used the same recommended installed Qwen3.5 4B Q4_K_M artifact and
native 16K settings, with explicit thinking-off requests. The executor checked
identity/settings before and after each observation. Order was serial, control
then candidate per case. No retries, repairs, warm-ups, downloads, hosted calls
or extension occurred. Every request hash was reserved durably before dispatch.
The [complete run](run/results.json), raw responses and [ledger](run/reservations.jsonl)
retain **48 valid reports from 48 calls**, with no missing reports. Historical
CI partiality is expected and separate from model errors; there are no model
transport or validation failures.

Reported usage was **34,270 input tokens and 1,258 output tokens**, below the
12,288-output-token cap. Each response stays within 256 tokens and 65,536 bytes;
each reported prompt plus allowance fits 16,384. All completions stop normally
without reasoning fields. These checks do not independently prove model-side
input preservation or physical tensor placement. No performance improvement is
claimed; order, cache and residency limit timing interpretation.

The [scorecard](scorecard.json) replays all 48 raw responses through real public
report construction, checking regenerated request hashes and full report equality.
It retains every per-case result, failure denominator, abstention and field change.

| Cohort | Control exact / acceptable | Candidate exact / acceptable |
| --- | --- | --- |
| Nine new development examples | 6/9 / 7/9 | 7/9 / 8/9 |
| Twelve exposed synthetic sentinels | 12/12 / 12/12 | 11/12 / 11/12 |
| Three exposed historical diagnostics, all expected bug | 0/3 / 0/3 | 0/3 / 0/3 |

“Acceptable” only adds the predeclared enhancement alternative for the overlapping
bug/enhancement example. Both arms select that defensible alternative; it remains
a preferred bug-expectation miss. No annotation changed and historical scores
are not pooled as fresh evidence. The earlier #63 historical **0/3 versus both
controls' 3/3** also remains unchanged.

The single exact-type **gain** is `omitted-support`: the control selects regression
with a generic observation quote; the candidate correctly abstains because the
sampler omitted the only supporting comparison. The whole input supports
regression, which does not validate the control's selected quote.

The single exact-type **loss** is `fixture-bug`: the control selects a supported
bug; the candidate selects regression with the fragment saying the same failure
also happens on the previous release. That establishes no version that worked.
Both the candidate's type and quote are unsupported, directly violating the
intended correction and losing an old sentinel.

`old-docs` remains a common expected-type failure: control selects question for a
hook malfunction, while candidate abstains despite an offered supporting bug
quote. Candidate abstentions are `old-docs`, `insufficient`, `omitted-support` and
`uncertain`; control abstentions are `insufficient` and `uncertain`. The overlap
case remains a common preferred-expectation disagreement. Nothing is omitted
because it is a failure or abstention.

In the actual historical comparisons:

- **R48 / #12219:** both select regression. The candidate changes to a clipped
  current-version/documentation quote that still establishes no affected-project
  working-to-broken comparison. Type support is uncertain; quote support fails.
- **R40 / #12223:** both select defensible enhancement with the same parser-failure
  quote. Relevance remains uncertain and the sampler still omits requested control.
- **R26 / #12249:** both select defensible enhancement, but the candidate selects
  only the fragment referring to normal config options. It omits the warnings
  referent and suppression request. The control retains a supporting available
  chunk: the candidate loses selected-quote support.

## Attributed review and adoption gates

The [48-entry review sheet](semantic-review.md) and [fingerprinted ratings](semantic-ratings.json)
rate actual whole-input type support and actual selected-quote relevance
separately, with concrete reasons. Reviewer: **implementing Codex/AI agent**, after
seeing expectations and outputs. This is not blinded, independent or human review.

Across 24 reports per arm, type support yes/no/uncertain/N/A is control
**20/1/1/2**, candidate **18/1/1/4**; quote relevance is **18/3/1/2** versus
**16/3/1/4**. Nulls receive N/A and a separate abstention-appropriateness judgment;
candidate `old-docs` is avoidable. Synthetic report-support gain is
`omitted-support`, loss is `fixture-bug`; the historical support loss is #12249.
These judgments concern dependent designed/exposed cases, not statistical
estimates or replacement expected outcomes.

The [decision](decision.json) applies every unchanged gate:

| Gate | Result |
| --- | --- |
| 1: valid reports, both null sentinels, all twelve old sentinels | **Fail.** Validity and nulls pass, but `fixture-bug` loses exact agreement: 11/12. |
| 2: all nine new acceptable outcomes and supported selections | **Fail.** `old-docs` abstains: 8/9, below required 9/9. |
| 3: repair exposed diagnostics without a support loss | **Fail.** R48 remains unsupported, R40 quote remains uncertain, R26 loses quote support. |
| 4: all actual reviews, human adoption review, no synthetic support loss | **Fail.** All 48 have attributed AI ratings; `fixture-bug` is a support loss. Human actual-report ratings remain unavailable. |
| 5: unchanged non-type fields, checks and archive preservation | **Fail under the literal frozen field rule.** `abstentions` differs for `old-docs` and `omitted-support`. All other non-type fields, including all 24 matched replies, citations, retrieval results and missing details, are identical; preservation and checks pass. |

The type-abstention bookkeeping differences are retained rather than silently
excluded after results. No gate is loosened. Human actual-report ratings remain
**unverified**: approval confirmed expectations and execution, not generated-report
quality. Missing human ratings cannot justify adoption; the observed failures
already require rejection. The valid negative result needs no policy exception,
additional inference, or demand that the user rate all reports before retaining
the application.

## Acceptance evidence and remaining uncertainty

| #66 criterion | Evidence and limits |
| --- | --- |
| Diagnose public selection/validation from saved outputs; separate inference, quote, taxonomy and sampler issues | Original three reports/request hashes and all 53 old reports reproduce; the pre-execution diagnosis and actual comparisons above separate all four mechanisms. No model-size conclusion. |
| Bounded correction and reviewed positive/counterexamples; preserve labels/null | Evaluation-only suffix, nine reasoned AI-authored examples subsequently user-confirmed in `approval.json`; all resolved labels/null remain offered without lexical gating or historical answers. |
| Freeze requests, outcomes, settings, criteria and cap before approval | Commit `7292553`, unchanged freeze, subsequent explicit approval; 48 exact reserved calls, 1,258 output tokens, zero extensions/downloads/hosted calls. |
| Compare actual public reports; preserve outcomes and attributed quote/type review; expose R48 | All 48 reports/raw responses replay exactly; scorecard retains gains, losses, abstentions and per-case outcomes; all 48 have reasoned AI ratings. R48 is exposed diagnostic evidence. Independent human report ratings remain unavailable and are not claimed. |
| Adopt only on declared criteria; negative result valid; preserve artifacts, tests/checks/audits; state guarantees | Negative result, no adoption or application change. All 916 old evaluation/case files and frozen source hashes preserved; #60/#63 old outcomes reproduce. Verification and source reviews are recorded in `execution-checks.json` and `execution-review.md`. |

The application guarantee remains structural validity and exact quote provenance;
semantic entailment requires review. Remaining unknowns are human report judgments,
out-of-sample generalization, independently proven input preservation and physical
tensor placement. The approved allocation is complete; no more inference is
authorized or needed to document this negative result.

To reproduce the complete new scorecard without inference, using the retained
hash-verified local snapshot:

```bash
PYTHONPATH=src .venv/bin/python scripts/issue66_results.py > /tmp/issue66-scorecard.json
cmp /tmp/issue66-scorecard.json docs/evaluation/issue-66/scorecard.json
```

The auditor denies real socket connections and supplies only saved model
responses. Do not rerun the executor: its allocation is complete, and its durable
run-directory and reservation guards refuse reuse.
