# Independent Codex/AI review of issue #63 generated reports

**Recommendation: retain Qwen2.5-Coder 3B as the application default for now.**
Qwen3.5 4B is the stronger fresh classification candidate, but the actual reports
fail the frozen requirement that every candidate type quote be relevant. The
review also leaves one candidate classification uncertain. The original human
review requirement remains unmet. This is a reasoned negative promotion decision
on the present evidence, not evidence that 3B is universally better.

Reviewed target: `eval/issue-63-qwen35-promotion` at
`937351fb21e805e5d414b6d2efd7ec50ec555aad`, draft PR #65, issue #63.
Review performed in a separate worktree on `review/issue-63-codex`.
Reviewer: **independent Codex/AI review, GPT-6** (the family identity supplied to
this session; the exact deployed variant is unavailable). These judgments are
not human ratings. No human report ratings have been supplied.

The [attributed ratings](codex-ratings.json) contain all 53 report codes and
original fingerprints, four judgments and concrete reasons for every report.
The original [pending human-rating file](ratings.json) is unchanged.

## Method, independence and evidence

I first read the method-hidden README and all report sheet entries, without
consulting `key.json`, the scorecard, measured report or aggregate results.
I inspected both integration inputs, the complete retained historical openings
in the original workspace's ignored `.local/issue63-review-openings.md`, and
additional anonymized report payloads for context and citations. A mechanical
script read `run/results.json` only to hash each report payload and emit it under
its sheet R code. It exposed no model aliases, row outcomes, scores or mapping
to the reviewer. Reading that container for anonymization is disclosed rather
than claiming the results file was never accessed. The report generator source
was read to locate the payload and fingerprint format. No prior ratings were
used to produce mine.

Initial ratings were saved before revealing the key or reading the proposal,
measured report, scorecard and acceptance evidence. Their unchanged file SHA-256
is `fd9592f67ab1296795a9298828a7dcc67129deb77b41d253b72bce1f254854ec`.
The saved timestamp records the phase boundary; the file was not revised after
unblinding. The user prompt already identified Qwen3.5 as the candidate and
mentioned three known historical bug disagreements. That prior exposure limits
independence: this is method hiding, not an assertion of complete ignorance of
the experiment. Similar replies and repeated inputs also make reports dependent.
The live issue and PR descriptions were read only after ratings were saved;
PR #65's head matched the requested commit at that read. No later pytest edits,
labels or comments were used as opening evidence.

The ignored snapshot was available from the original workspace and matched the
frozen snapshot SHA-256
`54659e822b11f0c37f24b056d4eace6f0dd7f600bd8d025e659503e30922b8a9`.
Each retained review opening's title/body bytes matched that snapshot. Original
opening cutoffs and content hashes are:

| pytest issue | Original cutoff | SHA-256 of title, NUL, body |
| --- | --- | --- |
| #12219 | 2024-04-16T08:22:38+00:00 | `681e48797dfaccd7ce7ff3a86bd5862656e34bfbda83da9364ae7fb8696a891b` |
| #12223 | 2024-04-17T09:00:30+00:00 | `731ee2132c277f516b51978c67bb77a578a8731a4b726346f248e7934d627e72` |
| #12249 | 2024-04-26T14:06:04+00:00 | `5c195b0eca34760f69c1fcac6dd99193ed8c68662c4a8ddc38fd44dea581fdf5` |

Contributor bodies are not republished. Citation assessment uses the frozen
report context's template fields, saved passages and original input. I did not
independently fetch template links or confirm the external technical behavior
reported by contributors. In particular, #12249's unavailable CI remains
unavailable. A correct quotation and accepted JSON are not semantic validation.

## Findings from the blinded ratings

Semantic support asks whether the input supports the category, not whether it
matches the benchmark's preferred category exactly. A malfunction can support
broad `bug` while a controlled version break makes `regression` more precise.
Thus the controls' fresh regression misses remain benchmark misses even though
I rate broad bug as supported. Conversely, a note explicitly withholding intent
and evidence supports neither bug (3B R20) nor question (7B R07). Those are
unsupported classifications, while candidate R08 correctly abstains.

| Model/cohort | Reports | Type yes / no / uncertain | Quote yes / no / uncertain / N/A | Unsupported reply claims | Usefulness counts 0 / 1 / 2 |
| --- | ---: | --- | --- | --- | --- |
| Qwen2.5-Coder 3B, matched inputs | 15 | 14 / 1 / 0 | 13 / 1 / 1 / 0 | 0 yes; 15 no | 10 / 3 / 2 |
| Qwen2.5-Coder 7B, matched inputs | 15 | 14 / 1 / 0 | 12 / 2 / 1 / 0 | 0 yes; 15 no | 10 / 3 / 2 |
| Qwen3.5 4B, matched inputs | 15 | 14 / 0 / 1 | 12 / 1 / 1 / 1 | 0 yes; 15 no | 10 / 3 / 2 |
| Qwen3.5 4B, integration | 8 | 8 / 0 / 0 | 8 / 0 / 0 / 0 | 0 yes; 8 no | 8 / 0 / 0 |

These are AI judgments, not benchmark replacements or independent statistical
samples. The eight integrations reuse the exit-status case; they are not eight
new quality observations. The candidate total is 23 reports, controls 15 each.

All 15 matched inputs have byte-identical draft replies across the three arms.
Their usefulness sums are each 7/30, with no paired losses or gains. Ten of the
twelve fresh replies in each arm give only the fallback inability statement;
I rate those 0 because a clear malfunction, documentation correction or question
receives no next action. I treat that statement as a cautious limitation rather
than an unsupported external factual claim. The incomplete note earns 1 for
appropriate restraint. Cleanup's environment/reproduction requests earn 2.

The three historical hook replies earn 2: they acknowledge the working minimal
example and ask for a failing reduction of the affected project. XML and warning
replies earn 1: environment requests are safe but generic. The hook and warning
replies ask for OS information already present in their frozen openings, and
the hook reply duplicates its generic minimal-example request. These are shared
application reply weaknesses, not candidate improvements. No report establishes
a fabricated diagnosis or fix. The eight candidate integration replies all earn
0 despite correct classifications: safe fallback is not useful triage by itself.

Candidate integration codes R04/R06/R29/R43 cover the short input and
R16/R41/R45/R52 the long input. Every selected quote supports the status/failure
mismatch, including the repeated observation in long reports. None introduces
unsupported reply facts, but none offers an investigative next step.

## The three historical disagreements

**pytest #12219 — candidate R48, controls R42/R24.** The complete opening reports
hooks not running in the affected project, invokes older support and current
documentation, and supplies a minimized example where current hooks do run.
It does not demonstrate that the same affected project worked on an older
version. Broad bug is supported; regression is plausible but **uncertain** under
the frozen credible working-to-broken comparison rubric. This is substantive
overreach beyond demonstrated version evidence, not merely a harmless synonym
for bug. It also does not prove the label false: no old-version reproduction is
available to settle that question. R48's selected fragment only says the hook
never runs. It supplies no version comparison and is **not relevant evidence for
regression**. The full opening cannot repair the selected quote's missing support.
The useful investigative reply does not cure that defect.

**pytest #12223 — candidate R40, controls R22/R53.** The frozen body includes a
small test and XML example, reports verbose message attributes that cause
consumer truncation/crashes, and asks about reducing the attribute independently
of the body. Bug is well supported as broken interoperability; enhancement is
also defensible as a request for output-size control rather than demonstrated
invalid XML. I rate enhancement support yes, a **taxonomy ambiguity**, not a
confidently wrong classification. The quote describes consumer failures without
the requested output control, so its relevance to enhancement is **uncertain**.
Selecting a failure sentence exactly does not settle that relevance. The safe
generic reply does not investigate parser limits or the requested distinction.

**pytest #12249 — candidate R26, controls R37/R30.** The opening identifies
warnings emitted during early import/rewrite, beyond normal configuration's
control, and explicitly requests suppression through normal options. Bug is
supported as a filtering gap; enhancement is defensible as extending filtering
to an earlier phase. R26's quote includes both limitation and requested
suppression, so both its type and quote receive yes. This is **taxonomy ambiguity**,
not evidence of hallucination. The controls' selected spans identify import-time
warnings but omit the broken filtering, which is why their quote ratings remain
uncertain. The generic requests repeat already supplied OS information and are
only limited help. Missing linked CI is an evidence limitation, not a model error.

All three archived bug expectations and the candidate's **0/3 versus both
controls' 3/3** remain unchanged. These are exposed diagnostics, not fresh
holdout losses. Two defensible alternatives reduce the severity of the semantic
concern; they do not erase benchmark losses, validate the regression claim or
justify rewriting annotations. No new pooled historical score is calculated.

## Frozen promotion gates and decision policy

The gates are those in [proposal.md](../proposal.md), interpreted alongside
[report.md](../report.md), [scorecard.json](../scorecard.json) and the original
[acceptance evidence](../../issue-63.md).

| Gate | Assessment after this review |
| --- | --- |
| 1: fresh validity and type thresholds, no worse than either control | **Pass.** Candidate 12/12 valid and correct; 4/4 ordinary bugs, 3/3 regressions, 3/3 questions, docs and null correct. Both controls 8/12. Four gains and no fresh losses against each. |
| 2: preserve and inspect historical losses, document tradeoff | **Review/documentation complete; residual uncertainty remains.** Two enhancement choices are defensible ambiguities; R48's regression is unestablished and its quote fails support. No annotation changed. This gate does not itself demand 3/3 exact agreement. |
| 3: bounded real application integration and guardrails | **Pass within measured scope.** Eight reports/ten calls, final classifications and bounded finish actions, no exposed reasoning; expected CI partial reports distinguished from model failures. Correct exit-status quotes, but poor usefulness. Search/inspect transitions and near-window inputs were not exercised. |
| 4: actual report review, attribution and semantic safeguards | **Does not pass.** All candidate and matched-control AI ratings now complete; no unsupported draft fact and no paired usefulness loss. However R48 has an irrelevant type quote, R40 quote relevance is unresolved, and no human ratings have been supplied. |
| 5: no promotion when gates fail or essential evidence unresolved; retain measurement uncertainty | **Requires retain or inconclusive.** This review recommends retain because a concrete quote defect exists, rather than only missing ratings. Truncation and physical tensor placement remain unverified. |

The user explicitly delegated this semantic review to Codex, authorizing these
AI ratings. That does not silently amend the frozen protocol's request for human
ratings. I propose **no decision-policy change for this retain recommendation**.
Accepting AI review in place of human review would be an explicit post-result
policy amendment requiring maintainer acceptance and a recorded rationale.
Even that amendment alone would not pass gate 4: tolerating R48's quote defect
or treating uncertain quotes as passes would separately weaken its semantic
standard. This review does not recommend doing that. The pending human file and
original scorecard decision are preserved as historical artifacts.

## Practical tradeoffs and remaining decision

Qwen3.5 earns consideration: it recognizes controlled regressions and abstains
on insufficient intent where both controls fail the preferred taxonomy. Its
fresh gains are meaningful for classification, although deliberately explicit
synthetic wording and small sample size limit generalization. Retaining 3B
accepts those known weaknesses. The larger 7B reference supplies no measured
fresh classification or reply advantage here.

The candidate's recorded fresh p50 model time is 486.687 ms versus 320.387 ms
for 3B, and empty-residency first-call time is 4.981 s versus 3.873 s. Across
observations sampled device peaks are 4276 MiB versus 2752 MiB (7B: 5368 MiB).
Those costs appear practical on the measured 8 GB laptop, but samples include
other processes and are not true peaks. Fixed arm order, differing native
artifacts and cache hits (11 fresh control calls, zero fresh candidate calls)
prevent interpreting this as an intrinsic speed comparison or capacity guarantee.

If promotion is later approved, retaining 3B as a selectable availability or
lower-memory fallback is sensible. It could not automatically protect against
valid JSON containing an unsupported type/quote: those outputs pass structural
validation. This run did not test an automatic fallback mechanism or simultaneous
residency. The recommendation is therefore **retain now**, with Qwen3.5 kept as
the leading candidate, not reject it permanently or assume fallback solves the
semantic gate. Remaining maintainer decisions are whether to accept the
historical taxonomy tradeoffs and what review policy to adopt. Human review of
the existing saved reports can proceed without more inference. Any future prompt,
quote-selection or model evaluation changes need their own scope and authorization.

## Offline verification and preservation

In this review, `scripts/issue63_results.py` replayed all 53 complete report/context
structures from saved responses using the retained hash-verified snapshot and
reconciled all 55 charges. Its stdout matched the frozen scorecard byte for byte. The initial sandboxed
audit stalled and was interrupted; the same offline auditor completed outside
the sandbox with a 60-second process limit and recorded model transport.
Separate offline assertions verified all 53 rating/key/payload fingerprints,
all 15 matched reply equalities, exact retained opening bytes and snapshot hash,
and the unchanged initial rating hash. `git diff --check` passed. The final
commit adds only this review and the attributed ratings; original pending human
ratings, source, protocol, responses, scores and annotations remain unchanged.

No application/evaluation model calls, downloads, retries, hosted calls or API
spending occurred. No application default, PR merge or issue closure was made.
This docs-only review did not rerun the full application test suite, launch a
browser, induce live timeout failures, or independently remeasure hardware.
Recorded 510-test/preparation and source-review results remain prior evidence,
not newly performed checks. The 15,900-character integration input's reported
4532 prompt tokens plus 256 allowance fit 16K; independent token preservation,
absence of truncation, near-window behavior, all-tensor physical residency and
model-driven search/inspect quality remain unverified.
