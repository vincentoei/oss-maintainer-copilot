# Issue #56: completion of remaining reproducible fixes

The requesting user asked Codex to finish the remaining code fixes in PR #57.
No user setup, credentials or manual execution was needed. This work continues
on `fix/triage-report-quality`; PR #55 remains unchanged.

## Fixed behavior and regression evidence

The [diagnosis](issue-56/follow-up/diagnosis.md) and individual red runs reproduce
the nine remaining missing-detail cases, partly redundant version questions,
incidental type cues and model-omitted investigative questions at the approved
replay/comparison seams. The original forty-case preview had 31 exact detail sets;
the [fixed replay checks](issue-56/follow-up/replay-checks.json) cover every expected
request, lose no previously correct detail set and reach 39 exact sets.

- Observed body failures and structured current/expected behavior establish an
  applicable template without requiring `Bug:` in the title. Hypothetical or
  negated positive failures stay excluded. Presentation-improvement requests use
  feature requirements rather than a bug checklist.
- Working controls are distinguished from failing reproducers, including fenced
  and indented examples and separately supplied failing examples. Described
  reproducer links count as supplied without asserting their execution.
- Tested pytest version lists and exact pytest commits in the version section
  suppress repeated pytest questions while preserving an absent OS/release.
- Reference URLs, template comments and fenced output are excluded as standalone
  type evidence. Exact original quotes and negation checks remain enforced.
- Required questions belong to deterministic report policy. Every untrusted
  model field is validated before required-statement assembly, then the assembled
  selection is validated again. Unknown/duplicate citations and unsupported types
  still fail; fallbacks retain vetted investigative questions. No repair call is
  added, and drafting behavior is unchanged.

The [full repository checks](issue-56/follow-up/checks.json) pass: **425 tests,
2 opt-in live tests skipped**, lint, formatting and strict mypy clean. Existing
API tests retain their no-false-acknowledgement assertions and now verify that
required questions survive model omission without a validation fallback.
[Two-axis review](issue-56/follow-up/code-review.md) has zero outstanding
actionable findings after four boundary corrections, each captured red-to-green.

## Historical preservation and measurement

All **323** prior case/evaluation files, including both earlier comparisons and
their reviews, remain protected by [baseline hashes](issue-56/follow-up/baseline.json).
The forty expected outcomes, opening identities, cutoffs, pinned commits and
candidate pools are unchanged. Full contributor bodies remain temporary.

The [protocol](issue-56/follow-up/protocol.md) and
[freeze](issue-56/follow-up/freeze.json) record source
`0035e144fe98b13aa32416b7b5dce199437215e5` before the one additional pass. It uses
the same selected model/settings and existing runner with an explicit protocol
hash and a new directory. Its independent cap is 200 charged calls. No warm-up,
retry, repair, second pass or model search is allowed for this frozen source.

## Annotation disagreement

#12083's preserved expected detail set requires only a package list. Its opening
names Linux/macOS without OS releases. The fixed report requests the missed
package list and an OS release while recognizing the described reproducer link.
The extra OS request is a real disagreement with the accepted annotation; it is
not concealed by suppressing the question or changing the outcome. This accounts
for the offline preview's 39/40 exact result despite complete expected-request
coverage. Recognizing a supplied link does not verify that its repository runs.

## Verification limits

The code fixes require no human check. Independent human ratings would require
another person and are not claimed; explicit Codex report reviews remain distinct.
Unavailable historical CI cannot be reconstructed with current CI, and a training
overlap audit needs an actual training corpus. These are evidence limitations,
not setup tasks for the requesting user. No workflow promotion or generalization
claim follows from these already exposed development cases.

## Final measured results

The live pass began **2026-11-24 15:02:15 UTC** at source `0035e14`. All forty
live opening/pin/cutoff preflights passed. All **120** rows were retained/scored,
including expected partial historical-CI reports. The
[ledger](issue-56/follow-up/run/requests.jsonl) and
[raw responses](issue-56/follow-up/run/responses.jsonl) retain **158** charged
dispatches: fixed 40, agent 118, within the independent 200 cap. No inference
retry or second pass occurred. Initial #56 and this changed-source pass together
used 316 calls under two separate 200-call caps; the earlier #18 run is preserved.

| Measurement | First #56 pass | Final live pass |
| --- | ---: | ---: |
| Keyword / fixed / agent type agreement | 18 / 21 / 22 of 40 | 19 / 24 / 24 of 40 |
| Exact detail sets, each workflow | 31/40 | 39/40 |
| Detail macro precision / recall, each | 1.000 / .775 | .988 / 1.000 |
| Model validation errors, fixed / agent | 1 / 1 | 0 / 0 |
| Partial reports, keyword / fixed / agent | 4 / 5 / 7 | 4 / 4 / 6 |
| Earlier-issue retrieval, keyword / fixed / agent | 6 / 6 / 5 of 40 | 6 / 6 / 5 of 40 |
| Relationship exact score, each | 2/37 | 2/37 |
| Structural citation validity, each | 40/40 | 40/40 |
| Fixed input / output tokens | 63790 / 962 | 66891 / 1046 |
| Agent input / output tokens | 158399 / 2307 | 161500 / 2391 |
| Fixed mean / p50 / p95 latency, ms | 440.09 / 315.917 / 683.821 | 455.33 / 322.135 / 751.563 |
| Agent mean / p50 / p95 latency, ms | 1031.82 / 829.221 / 1670.852 | 1048.43 / 841.799 / 1592.359 |
| Device-wide sampled GPU peak, MiB | 2742 | 2742 |

Eight additional detail cases become exact in every workflow: #12197, #12219,
#12223, #12249, #12255, #12263, #12273 and #12278. The ninth, #12083, now receives
its missed package request plus the disclosed OS-release question. **No previously
correct detail or type result regresses against the first #56 pass.** Fixed gains
#12053/#12081/#12189; agent gains #12053/#12189; keyword gains #12189. Both formerly
observed model type regressions are resolved. #12219 retains its vetted question
and no longer has a required-item validation fallback.

Relative to original #18, keyword type agreement improves 16→19/40, model type
agreement 19→24/40, and all workflows' detail agreement improves 17→39/40.
[Every initial-#56 transition](issue-56/follow-up/comparison-initial56.json) and
[every #18 transition](issue-56/follow-up/comparison-issue18.json) is retained.
Wrong types still exist; atomic pairing and incidental-cue filtering do not prove
general semantic correctness. Duplicate retrieval/judgment remains weak and
unchanged. Relationship scoring requires the annotated earlier issue even for
nonduplicates, so 2/37 is not general binary accuracy.

The agent still adds 78 dispatches, uses 2.412× fixed tokens and 2.119× fixed p95
without an exact-field advantage. Four historical-CI abstentions remain in each
arm; the agent retains two earlier-issue and one source-read errors. The selected
3B model and fixed RAG remain defaults. Single-run latency includes caching/cold
loads and excludes evidence acquisition; device-wide GPU samples are not process
peaks. Zero marginal API charges exclude hardware/electricity/network/hosting.
Already exposed development cases and source/prompt/schema changes limit causal
attribution and generalization.

## Final title-version wording check

Fresh review found that #12072/#12263 supply pytest identity only in their titles.
The live source still asked the combined version question for them. After that
measurement, one narrow change passes the complete opening's title/body to the
existing environment recognizer. The final source therefore differs from
`0035e14` in **pytest_profile.py only**. Its [425-test checks](issue-56/follow-up/checks.json)
record final source hashes; the separate
[424-test freeze checks](issue-56/follow-up/checks-at-inference-freeze.json) retain
the actual live source identity. No live final-source measurement is claimed.

The [six recorded-response replays](issue-56/follow-up/title-version-replay.json)
exercise both affected openings through keyword/fixed/agent replay and the real
provider adapter using the live pass's exact saved response bytes. **Zero new
dispatches** occurred. Every deterministic field score, type and status is
unchanged; the question now asks only for OS/release. This verifies wording and
integration, not what a freshly sampled model would choose after changed input.
The replay includes explicit Codex semantic review of the narrowed questions.

## Fresh attributed report review and verification

All [120 live reports](issue-56/follow-up/review/review.md) received fresh explicit
Codex review in 45 disclosed same-opening/identical-claim groups. The
[summary](issue-56/follow-up/review/summary.json) records usefulness 0/1/2 counts
28/20/72 and support/partial/abstained counts 87/6/27. Keyword/fixed/agent rating
totals are 55/55/54 out of 80. These unblinded assistant ratings carry author
bias and do not establish independent human quality or justify promotion.

The six partly supported frozen reports are exactly the title-version questions
at #12072/#12263, subsequently fixed and reviewed in the separate replay above.
#12219's generic minimal-example question overlaps its focused investigative
question; this verbosity lowers its usefulness rating even though both requests
are grounded in missing information. Generic replies to complete reports can
still be unhelpful despite correct empty detail sets. Structural citation checks
alone do not establish any of these semantic judgments.

[Offline verification](issue-56/follow-up/verification.json) checks all 323
preserved files, both source identities, forty unchanged candidate pools, all
120 row/score identities, 158 ledger/response pairs, 120 assistant fingerprints,
and six post-measurement replays. Original pending independent human-review files
remain unchanged. No additional human check is required for the scoped fixes.

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue56_followup_verify.py
```
