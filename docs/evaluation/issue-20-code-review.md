# Issue #20 code review

Fixed comparison point: updated `main`,
`666f5150d3b1e1da5dd24cd851e0daf69c3f26d7`. Reviewed with
`git diff main...HEAD` in separate fresh-context Standards and Spec agents.
Implementation commits: `661bde4`, `8a07503`; targeted final correction:
`8fba053`. The originating spec is GitHub issue #20. OpenRouter support was
expressly requested and credential use authorized by the user.

## Standards

No hard documented-standard violations found. The change follows glossary
terminology, preserves the historical-evaluation ADR decisions, and commit
subjects follow Conventional Commits.

One optional judgment call: possible Primitive Obsession in the mutable JSON
accounting records shared by `HostedBudget` and `HostedModel`. Reservation,
response and halt events have different required fields and lifecycle rules;
typed variants could make those invariants easier to inspect. This is a
maintainability heuristic, not a documented breach or release blocker. The
current implementation retains the repository's inspectable JSON-ledger style;
broader accounting refactoring is outside this ticket.

No critical correctness concern remained in the final Standards review.

## Spec

The first pass found fallback reports incorrectly counted as hosted successes
and aggregates based on different cohorts. Both now have explicit failure
handling: rejected selections remain unscored, and paired aggregates include
exactly the same successful case IDs. Regression checks cover those behaviors.

The final review found a crash/concurrency window between writing a failed
response and a separate halt marker. The correction rejects reservations when
any durable record contains an accounting error. A failing-then-passing crash
regression removes the halt marker and verifies that no second dispatch occurs.

The Spec reviewer rechecked `8fba053` and reported **no remaining Spec findings**.
The implementation preserves catalog identity and cutoffs, distinguishes
predictions from confirmed annotations, and discloses OpenRouter's alias versus
upstream snapshot verification limit. Live-result publication and offline audit
follow the source freeze; they are separate evidence from this source review.

After the live pass, the Spec reviewer checked the publication against saved
artifacts and found no material corrections. Counts, costs, reservations, paired
scores, type changes, latency percentiles, report statuses and shared source
hashes match. Acceptance evidence and remaining review/version/cost limits are
stated explicitly. This final check was read-only and made no paid calls.

Final totals: Standards **0 hard violations, 1 optional maintainability finding**;
Spec **0 remaining findings**. The earlier publication findings and durable-halt
finding were fixed before paid inference.
