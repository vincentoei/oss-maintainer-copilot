# Issue #56: triage-quality fixes after the forty-case evaluation

Requested follow-up to [#18](https://github.com/vincentoei/oss-maintainer-copilot/issues/18)
and [PR #55](https://github.com/vincentoei/oss-maintainer-copilot/pull/55).
The fixes live on `fix/triage-report-quality`, based on PR #55's head
`abe7540de2fe0891c2aa00a4cadc67eef51a7b89`. PR #55's branch and all forty expected
outcomes remain unchanged. All **269** prior case/evaluation files are protected
by [baseline hashes](issue-56/baseline.json).

## Fixes and deterministic evidence

[Diagnosis](issue-56-diagnosis.md) records the original failing replay, minimized
causes, alternatives and red evidence. The changes recognize supplied editable
package tables, installed dependency graphs, Markdown/environment formats, named
OS releases, valid test functions, self-test commands and concrete feature answers.
Questions ask only for the missing pytest/OS half. Explicit before/after sessions
no longer cause a false version-conflict question. Empty, negated and hypothetical
evidence still leaves the relevant request missing.

Model selection uses one indexed label/quote pair. This prevents the schema from
permitting a label with another label's quote while preserving public report
fields and the existing semantic, negation and citation validation. Invalid
selections abstain with usage retained; no repair call occurs.

[Repository checks](issue-56/checks.json): **400 passed, 2 skipped**, lint,
formatting and strict typing passed. The approved replay/cutoff and comparison
interfaces exercise the actual report builder and provider adapter. Two fresh
[code-review axes](issue-56-code-review.md) have zero outstanding findings.

Review publication binds reports to their exact fingerprints, verifies 49 opening
identities/cutoffs, pre-cutoff commits, allowed URLs and pinned file hashes, then
publishes explicit semantic judgments. [Five evidence tampering checks](issue-56/review-identity-checks.json)
are rejected before publication; the valid 120-report archived review passes.
Identity validation itself makes no semantic correctness claim.

## Freeze and one-pass comparison

[Protocol](issue-56-protocol.md) and [freeze](issue-56/freeze.json) record source
commit `ac498979cc170eedfdbd8b534d1a68b554f755f4`, the unchanged forty-case catalog,
source hashes and the separately capped pass. Selected model, sampling parameters,
fixed workflow default, timeout, output and response limits are unchanged.
No inference warm-up, retry, repair, model search or second pass is permitted.

The pass began **2026-11-24 14:19:15 UTC**. All forty live evidence preflights
passed, and all **120** keyword/fixed/agent rows were retained and scored. The
[dispatch ledger](issue-56/run/requests.jsonl) and
[raw response records](issue-56/run/responses.jsonl) account for **158** charged
calls: 40 fixed and 118 agent, within the independent 200 cap. No second pass was
run. Initial/final serving snapshots confirm the selected model digest and
2730345103-byte full GPU residency at context 16384.

## Before and after

[Comparison](issue-56/comparison.json) includes every case/workflow field and
status transition plus both complete resource summaries. Same openings, expected
outcomes, cutoffs, commits and candidate pools; every prior artifact is preserved.

| Measurement (before → after) | Keyword | Fixed RAG | Bounded agent |
| --- | ---: | ---: | ---: |
| Catalog / eligible / scored | 40 / 40 / 40 | 40 / 40 / 40 | 40 / 40 / 40 |
| Type exact agreement | 16 → 18 / 40 | 19 → 21 / 40 | 19 → 22 / 40 |
| Missing-detail exact agreement | 17 → 31 / 40 | 17 → 31 / 40 | 17 → 31 / 40 |
| Detail macro precision | .887 → 1.000 | .887 → 1.000 | .887 → 1.000 |
| Detail macro recall | .600 → .775 | .600 → .775 | .600 → .775 |
| Annotated-earlier-issue retrieval | 6 → 6 / 40 | 6 → 6 / 40 | 5 → 5 / 40 |
| Relationship exact score | 2 → 2 / 37 | 2 → 2 / 37 | 2 → 2 / 37 |
| Reports passing structural citations | 40 → 40 / 40 | 40 → 40 / 40 | 40 → 40 / 40 |
| Partial reports | 4 → 4 | 5 → 5 | 7 → 7 |
| Model validation errors | 0 → 0 | 1 → 1 | 1 → 1 |
| Dispatches | 0 → 0 | 40 → 40 | 118 → 118 |
| Input tokens | 0 → 0 | 64156 → 63790 | 158765 → 158399 |
| Output tokens | 0 → 0 | 2442 → 962 | 3787 → 2307 |
| Mean latency, ms | 4.72 → 4.43 | 757.80 → 440.09 | 1378.25 → 1031.82 |
| p50 / p95 latency after, ms | 3.703 / 9.644 | 315.917 / 683.821 | 829.221 / 1670.852 |
| Device-wide sampled GPU peak, MiB | 2742 → 2742 | 2742 → 2742 | 2742 → 2742 |

Fourteen detail cases improve in every arm; **none regress**: #12072, #12189,
#12216, #12231, #12242, #12290, #12293, #12298, #12303, #12305, #12307, #12308,
#12323 and #12328. #12328 also loses the false conflicting-version follow-up.

Keyword type gains: #12303 and #12312, no regressions. Both model arms gain
#12216, #12303, #12312 and #12328. **Both regress on #12053**, choosing docs from
an incidental reference link rather than enhancement. **Fixed also regresses on
#12081**, choosing bug from example failure output rather than enhancement; the
agent keeps enhancement. Atomic pairing prevents mismatched fields, not wrong
semantic choices among mechanically valid pairs.

The #12216 pairing failure is resolved in both real-model reports. A **different
validation failure appears at #12219**: raw outputs select C1 but omit required
investigative statement C2. Existing validation correctly produces an explicit
type/draft fallback, losing the earlier useful reply. No retry or required-claim
validation weakening hides this regression. Keyword retains its useful request.

Nine cases still miss expected detail requests in every arm: #12083, #12197,
#12219, #12223, #12249, #12255, #12263, #12273 and #12278. Template applicability
remains conservative. Duplicate retrieval/judgment is unchanged and weak; the
relationship metric is not general binary duplicate accuracy. Subjective single
labels retain documented ambiguities, including bug/question and bug/selftests.

Scores include partial/fallback reports. Empty predictions receive precision
one; read that with recall. Seventeen reports per arm have no citations and pass
structural checks vacuously. Four historical-CI abstentions remain per arm;
agent additionally retains two earlier-issue and one source-read error. These
are surfaced in traces and abstentions, not replaced with current CI results.

This is a single sequential laptop pass on already exposed development cases.
Changes to parser, schema, prompt and serving behavior limit causal attribution;
latency excludes evidence acquisition and includes cold loads/caching. GPU
samples are device-wide, not process peaks. Marginal API charges are zero;
hardware/electricity/network/hosting costs are unmeasured. The agent uses 2.482×
fixed tokens and 2.443× fixed p95 for one extra exact type result; fixed remains
the default and no workflow is promoted.

## Attributed semantic and usefulness review

I reviewed the [archived 120 reports](issue-56/archived-review/review.md) in 44
disclosed same-opening/identical-claim groups and the
[new 120 reports](issue-56/candidate-review/review.md) freshly in 45 groups.
Every report retains its exact fingerprint, explicit reason, type-field result,
supported relationships, redundant/missing requests and verified citation
identities. Both sets use **Codex** attribution, `independent_human_review: false`
and `blinded: false`. Identical report claims may share a judgment; separate type
choices remain visible. No historical human ratings were copied or changed.

| Codex assessment | Archived #18 | New #56 |
| --- | ---: | ---: |
| Usefulness 0 / 1 / 2 | 70 / 29 / 21 | 54 / 17 / 49 |
| Supported / partly supported / unsupported / abstained | 36 / 15 / 6 / 63 | 63 / 6 / 0 / 51 |
| Whole redundant-field reports per arm | 7 | 0 |
| Keyword / fixed / agent rating totals, each out of 80 | 24 / 24 / 23 | 40 / 38 / 37 |

These subjective assistant ratings carry author bias and are **not independent
human quality evidence**. Whole redundant-field requests disappear, but two
**partly redundant subquestions remain in every arm**: #12298 already lists
tested pytest versions and #12300 supplies an exact pytest commit, yet each gets
the combined pytest/OS question. OS/release is still missing. These six reports
are rated partly supported rather than hidden by exact-field agreement. Generic
drafts remain unhelpful even when their empty detail set is correct; removing a
bad question does not automatically make a useful reply.

Original pending human-review files remain untouched for both passes. Independent
human ratings would be necessary to claim independent validation or workflow
promotion, neither of which this change claims. Codex cannot be its own
independent human reviewer. They are not a prerequisite for verifying these fixes.

## Acceptance evidence

| #56 criterion | Evidence / status |
| --- | --- |
| Reproduce and fix bounded report failures at approved interfaces | Complete: [diagnosis and red checks](issue-56-diagnosis.md), replay/provider regressions and [400-test repository checks](issue-56/checks.json). Actual model pass exercises the changed schema adapter. |
| Preserve cases/prior evidence and expose all deltas | Complete: [offline audit](issue-56/verification.json) verifies all 269 hashes, forty unchanged candidate pools, all 120 row identities and scores, freeze/source hashes and [every field transition](issue-56/comparison.json). Gains and regressions are described above. |
| Prevent unsupported label/quote pairing without weakening validation | Complete for pairing: controlled invalid selections abstain and real #12216 succeeds. Public report fields and citation/negation/required-claim validation remain; wrong semantic choices and #12219 omission are explicit remaining model risks. |
| Complete attributed fresh Codex report reviews | Complete on the authorized assistant basis: [archived](issue-56/archived-review/summary.json) and [new](issue-56/candidate-review/summary.json), 120 each, exact fingerprints verified. Independent human assessment remains unverified, not claimed. |
| Separately freeze and cap the new measurement | Complete: [freeze](issue-56/freeze.json), [single run](issue-56/run/results.json), [158 charged request/response pairs](issue-56/run/requests.jsonl), all 120 retained scores and pending independent review identities. No second pass. |

Two opt-in network replay tests are skipped in the deterministic suite because
`RUN_LIVE_REPLAY` is unset. The actual comparison independently verifies all forty
live openings/pins/cutoffs and runs all three real workflows, including expected
partial historical-CI reports. Unavailable historical CI cannot be reconstructed
by a current check. External/future training overlap remains unverified because
there is no training corpus; unchanged family partitions are preparation for
that future audit, not proof about unseen data.

No human check is needed to validate the scoped fixes. Full triage correctness,
independent usefulness and unseen-data performance are not established.

Run the saved audit without network or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue56_verify.py
```
