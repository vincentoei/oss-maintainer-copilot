# Issue #63 publication review

Separate Standards and Spec reviewers checked `git diff 28f3d36...HEAD` through
`dd07e86`, plus the subsequent p50 wording correction. They performed no model
calls, downloads or ratings on behalf of a human. The accepted source freeze and
measurements were not altered during publication.

## Standards

No documented-standard breaches or material correctness findings. No actionable
baseline smells.

Read-only checks confirmed frozen inputs/current source hashes, all 55 ledger
reservations against call files, 53 report fingerprints, 55,389 input / 1528
output tokens, 50 complete and three partial reports, and 53 pending human
ratings. Publication preserves ADR-0003's restriction on bulk contributor bodies
and explicitly retains unresolved review and the existing default.

One minor wording note was resolved: the latency table and acceptance summary
now identify the published percentile values as nearest-rank p50. The frozen
scorer and measurements are unchanged.

Standards: 0 remaining findings.

## Spec

No publication-blocking Spec defects found. One acceptance requirement remains
incomplete: “Collect fresh, method-hidden review sheets … with … reviewer
attribution and reasons.” All 53 actual-report ratings remain pending. Expected
type confirmations provide no independent semantic or usefulness judgment. The
report discloses this, retains 3B and leaves promotion unresolved. This blocks
full acceptance/promotion while allowing publication of measured results.

Read-only checks confirmed 53 reports, 55 reserved/executed calls, 55,389 input /
1528 output tokens; candidate fresh agreement 12/12 versus 8/12 for each control;
diagnostics 0/3 versus 3/3; and eight passing integration reports. Cohorts,
denominators, abstentions, changes, approval sequence and source/default integrity
match the specification. No scope creep or incorrect implementation was found.
Limits on usefulness, search transitions, truncation, physical residency,
cold-start timing and the small designed cohort are explicit.

The Spec reviewer's full replay hung in sandbox TestClient and was stopped;
independent artifact checks completed. The parent completed successful escalated
offline replay and clean full-history clone replay. With the retained snapshot,
the scorecard reproduces byte for byte; without it, scores/accounting are
unchanged and nine unreplayed historical report structures are listed explicitly.

Spec: 0 publication blockers; 1 disclosed pending acceptance requirement.
