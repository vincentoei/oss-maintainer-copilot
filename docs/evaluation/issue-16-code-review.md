# Issue #16 two-axis review

Fixed point: updated main `2e1da92edaedc280af8af099555714e5fed25136`.
Command: `git diff 2e1da92edaedc280af8af099555714e5fed25136...HEAD`.
Implementation commits reviewed: protocol `11f9f0b`, evaluator `7d78ea7`,
corrections `7cfb226`. Separate fresh-context Standards and Spec agents reviewed
in parallel, then each checked the corrections before real inference began.
No reviewer ran inference or supplied human usefulness ratings.

## Standards

Initial review: no documented-standard breaches. Two heuristic findings:
unchecked residency dictionaries could treat two missing sizes as equal; fixed
method mappings repeat across budgets and dispatch. The first was corrected by
requiring known positive memory sizes and adding a public summary regression.
The second remains an accepted nonblocking judgment within this fixed three-arm
scope; introducing a generic dispatch framework is unnecessary for #16.

Recheck, verbatim:

> Rechecked `7cfb226`: no hard standards breach or remaining concrete defect found.
>
> The residency gate now handles missing sizes correctly. Preflight flags failed
> or partial evidence verification; bounded response capture preserves malformed
> responses before parsing; full GPU samples persist.
>
> The fixed method mappings are acceptable within this three-arm scope. Tests
> were not rerun here because the uv cache is read-only and no repository virtual
> environment exists.

The primary agent runs the checks with the existing development environment and
this checkout's `src` on `PYTHONPATH`; reviewer environment limits are not test
results. See the main evaluation report for actual verification evidence.

## Spec

Initial review identified two P2 findings against the frozen protocol: preflight
ignored source/documentation verification failures converted into partial reports;
malformed raw provider responses were discarded before measurement could retain
them. Both were reproduced with failing runner tests and corrected before any
inference. Preflight now saves and checks verification traces, and a default-off
response observer retains bounded provider bytes before parsing. No prompt,
schema, scoring rule or generation setting changed.

Recheck, verbatim:

> Both findings are resolved in `7cfb226`:
>
> - Preflight now retains its trace and flags non-OK documentation/source retrieval
>   before any arm executes, preserving identical eligibility and preventing
>   inference for affected cases.
> - The response observer captures bounded provider output before parsing,
>   retaining text, byte count, hash and truncation status even when parsing fails.
>
> GPU samples are now retained, and absent residency sizes remain unknown.
>
> No remaining concrete defects found in the reviewed correction diff. Live
> evaluation, fresh human reviews and the final acceptance evidence remain pending;
> no inference was performed during this review.

Summary at implementation freeze: Standards zero hard breaches, one accepted
nonblocking mapping heuristic; Spec two corrected defects, zero remaining code
findings. Execution results and any still-unverified human judgments are reported
separately, not converted into review passes.

## Final evidence review

Both axes reviewed evidence commit `39a4dfa` after the real run and full checks.
Standards found zero hard breaches and no new smell finding. The reviewer
independently checked the offline assertions and publication boundaries: bounded
provider outputs/reports only, without full contributor openings or serialized
inputs. The existing mapping judgment remains nonblocking.

Spec found no new findings. The reviewer reran offline verification, confirmed
candidate eligibility, execution order, prompt/input/schema comparisons and all
reported quality/resource numbers. Retaining fixed legacy follows the failed
gates; human usefulness and semantic judgments remain unverified. Neither final
review dispatched inference. The subsequent documentation-only clarification
`69f3250` exposes the 15/15/14 citation counts and nine citation-free reports per
arm; it changes no scores or artifacts.

Final totals: Standards zero hard breaches, one previously accepted nonblocking
heuristic; Spec zero outstanding defects. Human review remains sixty pending
ratings, explicitly outside these automated/code-review results.
