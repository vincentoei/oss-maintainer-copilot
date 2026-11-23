# Two-axis code review

Reviewed against cc44852c7db55840f233f952c411dd485a8660a8 using fresh
Standards and Spec subagents as required by the implement/code-review skills.
Initial implementation reviewed at 0b6d45b; corrections reviewed in the working tree.

## Standards

No direct AGENTS.md, glossary, ADR or Conventional Commit violations found.
A quoted [C999] could escape draft validation and fail final report validation.
Corrected by escaping rendered brackets while preserving exact citation passages;
both public-interface regressions pass. Optional heuristics: experimental assembly
adds responsibilities to triage_issue; passage input pairs might benefit from a
named type if the contract grows.

Recovery skips completed cases and rejects recovery of cases that already
dispatched inference. Review presentation originally filtered failed controls;
corrected to retain all twenty IDs and assert both arms contain the frozen set.
The present recovery succeeded for all sixteen acquisition failures.

## Spec

Injection-like text in draft quotes and paraphrased instructions were initially
accepted. Corrected validation checks both rendered fields; public regressions
cover both APIs. A/B originally differed in evidence supplied; corrected controls
use evidence_enabled and receive identical passage payloads. A capturing-client
review confirmed matching packets and 512-token limits without inference.
The initial unmatched control remains preserved and excluded from promotion.

Final controlled regressions also cover supplied/absent detail and substantive/
misleading relationships through the drafting contract at both APIs. They establish
preservation of upstream behavior with explicit draft abstention, not semantic
correctness of arbitrary generated questions. All sixty human usefulness/semantic
reviews and four-arm pilot/resource results are now recorded. No accepted real
candidate establishes the remaining free-text semantic guarantees.
No additional tuning is authorized after the final development iteration or pilot.

Summary: zero unresolved hard standards violations; experimental requirements
have documented negative results and explicit limitations; all human review gates are closed.

## Final review after explicit human pilot judgments

Fresh Standards and Spec reviewers inspected the final branch against
cc44852c7db55840f233f952c411dd485a8660a8. Standards: zero material merge blockers;
optional assembly/tuple-type heuristics remain. The reviewer verified all twenty
pilot fingerprints and 85 unique request IDs. Spec: all sixty report/draft
fingerprints independently match. Development/pilot promotion gates fail.
AC3–4 are partial for demonstrated generated-question semantics; controlled null-
draft regressions establish retained upstream behavior, not arbitrary semantic
rejection. This acknowledged negative result does not require retuning or prevent
merging the retained baseline plus evidence. Initial stale review-status wording
and ambiguous nested automatic scoring markers were corrected. All sixty human
reviews are complete; original automated/raw pending markers remain historical
state with explicit companion precedence. Final deterministic checks: 284 pass,
two ordinary live tests skipped; whole-repo Ruff/format and strict mypy pass.

Summary: Standards has zero material findings. Spec retains two disclosed partial
capability criteria (AC3–4); the failed candidate is not promoted. Merge status
is tracked in #50 before any #16 handoff.
