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

Remaining requirements: generated-question regressions for supplied/absent detail
and substantive/misleading relationships are incomplete; semantic support cannot
be inferred from a quotation. Human usefulness/semantic judgments remain pending.
Pilot inference and resource/model evidence are recorded separately when complete.
No additional tuning is authorized after the final development iteration or pilot.

Summary: zero unresolved hard standards violations; experimental requirements
remain incomplete until the explicit review gates and acceptance evidence close.
