# Qwen3.5 promotion evaluation

Keep the current 3B default pending semantic review. Qwen3.5 matched all twelve
new synthetic expectations, but repeated all three exposed historical bug
losses. Its application integration passed. These results meet the fresh-type
gate, not the complete promotion gate: historical tradeoffs and actual human
type/quote/reply ratings remain unresolved.

The requesting user approved the exact 55-call allocation after confirming the
twelve expected types. [Approval](approval.json), [freeze](freeze.json) and
[protocol](proposal.md) preserve that sequence. Source `cfd21c0` was held fixed;
all requests used explicit `reasoning_effort: "none"`, 256 output tokens and the
three pinned 16K Q4_K_M artifacts. No prompt, sampler, expected outcome or model
default changed during the run. The frozen proposal retains its pre-run status
text as historical evidence; this report records the execution that followed.

## Agreement by cohort

| Model | Fresh synthetic types | Ordinary bugs | Regressions | Questions | Docs | Insufficient/null | Exposed bug-loss diagnostics |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder 3B | 8/12 | 4/4 | 0/3 | 3/3 | 1/1 | 0/1 | 3/3 |
| Qwen2.5-Coder 7B | 8/12 | 4/4 | 0/3 | 3/3 | 1/1 | 0/1 | 3/3 |
| Qwen3.5 4B | 12/12 | 4/4 | 3/3 | 3/3 | 1/1 | 1/1 | 0/3 |

Every fresh and diagnostic response passed application validation. The candidate
had one valid type abstention, correctly matching the deliberately incomplete
opening. There were zero transport failures, invalid responses or omitted rows.
Full confusion matrices and paired gains/losses are in [scorecard.json](scorecard.json).

| Fresh input | Reviewed type | 3B | 7B | Qwen3.5 |
| --- | --- | --- | --- | --- |
| log-bug | bug | bug | bug | bug |
| log-regression | regression | bug | bug | regression |
| fixture-question | question | question | question | question |
| fixture-bug | bug | bug | bug | bug |
| exit-bug | bug | bug | bug | bug |
| exit-regression | regression | bug | bug | regression |
| precedence-docs | docs | docs | docs | docs |
| precedence-question | question | question | question | question |
| teardown-regression | regression | bug | bug | regression |
| traceback-bug | bug | bug | bug | bug |
| warning-question | question | question | question | question |
| uncertain | null | bug | question | null |

Against either control, Qwen3.5 gained the three explicit rollback/version-break
regressions and the insufficient-input abstention, with no fresh losses. All
three recognized the fresh documentation/usage contrast. These cases were
designed and their labels confirmed before inference; their small size and
explicit wording do not establish generalization to unseen contributor reports.

The separate diagnostic cohort deliberately revisits the candidate's three
known historical bug losses. Both controls selected bug for all three. Qwen3.5
again selected regression for pytest #12219 and enhancement for #12223 and
#12249. These remain losses against the unchanged archived expectations; they
are not fresh holdout observations and are not pooled into a new fifty-case score.

Assistant inspection, not independent human adjudication, identifies these
specific review questions:

- **#12219:** the selected quote describes a hook never being called; the opening
  mentions pytest 8.x but also says a minimized example works. The quote does not
  itself establish an unchanged-project working-to-broken comparison. The model's
  regression suggestion needs semantic review rather than automatic acceptance.
- **#12223:** the enhancement quote describes parsers truncating or crashing.
  Whether a requested output change is an enhancement or correction to broken
  behavior must be assessed against the full opening and preserved bug rubric.
- **#12249:** the quote asks for a way to suppress warnings that cannot currently
  be controlled by configuration. That request-shaped wording can motivate an
  enhancement interpretation, but no expectation was changed after observing it.

No new model calls or prompt corrections were used to investigate these losses.

## Application and serving evidence

The candidate correctly returned bug on all eight short/long integration reports:
Python fixed triage, HTTP fixed API, actual browser form/backend, and bounded-agent
HTTP. Each agent run used exactly one permitted `finish` action followed by final
classification. All ten integration calls passed, with no exposed reasoning.
These agent inputs have no issue number/source location, so the run does not
exercise model-driven search/inspect transitions.

| Candidate integration | Short end-to-end ms | Long end-to-end ms |
| --- | ---: | ---: |
| Python fixed triage | 729.962 | 1726.143 |
| HTTP fixed API | 667.617 | 672.220 |
| Browser submission | 1679.749 | 1137.230 |
| Bounded-agent API | 907.579 | 1897.774 |

Browser times include browser startup and pinned-tool verification. Later inputs
benefited from cache state and fixed run order; these timings are not isolated
serving benchmarks. All eight integration reports completed, with explicit
field abstentions for unavailable search evidence and unsupported reply claims.
The three historical #12249 reports were partial because linked CI evidence was
unavailable; their model selections were valid and retained in the denominator.
Overall there were 50 complete and three partial reports.

| Model | Fresh median model ms | Empty-residency first-call model ms | Peak sampled device MiB across its observations |
| --- | ---: | ---: | ---: |
| 3B | 320.387 | 3873.144 | 2752 |
| 7B | 445.332 | 5213.072 | 5368 |
| Qwen3.5 | 486.687 | 4980.511 | 4276 |

The first charged call in each arm began with empty Ollama residency and zero
reported cached prompt tokens. Two separately recorded administrative unloads
preceded arm changes; no warm-up generation occurred. First-call duration
includes loading and inference; a separate native load duration is unavailable.
Native usage reported cache hits on eleven fresh calls per control and zero
fresh candidate calls. Seven candidate integration calls reported hits. Neither
cross-arm median latency nor browser timing implies an intrinsic model speed.

All observations reported the pinned digest, 16,384 context, and positive equal
total/GPU byte counts. Device memory was sampled every 500 ms and includes other
processes; it is not the true peak. These API fields do not prove physical
residency of every tensor or absence of Windows shared-memory use.

Native prompt counts ranged from 431 to 1711 for each control and 287 to 4532
for the candidate, including its planner calls. The 15,900-character long input
produced 4532 reported final-report prompt tokens; adding the 256-token allowance
gives 4788, below 16,384. This checks a bounded long application input, not a
near-window stress test. Model-side preservation of every input token and lack
of truncation remain unverified independently of the API counts and successful
classification. Native tokenizers/templates differ across the pinned artifacts.

## Accounting, replay and semantic review

The [durable ledger](run/reservations.jsonl) contains exactly 55 reservations:
15 for 3B, 15 for 7B and 25 for the candidate. All payload hashes matched their
frozen slots before HTTP. Provider usage totals were 55,389 input and **1528 /
14,080 allowed output tokens**; no response reached 256 output tokens. There
were zero retries, repairs, warm-ups, downloads, hosted calls or API fees.
Hardware and electricity costs were not measured.

The offline auditor reproduced all 53 complete report/context structures from
the saved bounded responses, including all nine diagnostic reports using the
hash-verified retained snapshot. It reconciled all 55 charges with call files,
recomputed scoring/placement, and checked unchanged unrelated fixed-report
fields. Browser execution checked the rendered report against the real API
result; offline replay exercises that report through the API, not a second
browser session. No extra model dispatch was used for verification.

The [method-hidden review pack](review/README.md) contains all 53 actual generated
reports, report fingerprints and pending reviewer fields. The requesting user
has been asked to review them. **No human ratings have yet been supplied.** The
expected-type confirmations are not semantic-support or usefulness ratings.
All three arms produced the same draft reply on each matched fixed input. Most
fresh reports used a safe fallback rather than an actionable answer; output
agreement does not establish usefulness. The eight integration reports also
used the fallback. This experiment cannot claim improved reply usefulness.

The frozen fresh classification gates pass: 12/12 total, 4/4 bugs, 3/3 regressions,
3/3 questions, docs and null correct, and no worse than either control. The full
promotion gate remains unresolved because the three historical tradeoffs and
human support/usefulness ratings are outstanding. The recommendation is to
retain 3B for now and keep Qwen3.5 as the stronger classification candidate.
No model default was changed and no further inference is authorized by this run.

Source preparation validation passed 510 tests with two opt-in live replay skips,
Ruff, mypy, seven preserved offline audits and separate Standards/Spec review.
Current publication checks and review findings are recorded in the issue's
[acceptance evidence](../issue-63.md). Earlier benchmarks and frozen source
references remain unchanged.
