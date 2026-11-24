# Issue #56 pre-inference review

Scope: `abe7540de2fe0891c2aa00a4cadc67eef51a7b89` through the follow-up source,
including the working changes before the inference freeze. Two fresh parallel
Codex reviewers used the code-review skill's separate Standards and Spec axes.
They performed read-only reviews and no inference or extra suite runs.

## Standards

Initial findings: **2**. Outstanding after re-review: **0**.

- Hypothetical/negated documentation-reading scenarios could suppress a needed
  use-case request. Both negative examples now remain missing; asserted use cases
  still satisfy the requirement.
- Review publication computed cached opening hashes without binding them to
  historical identities. Publication now verifies openings/cutoffs/commits and
  pinned-file identities before accepting explicit semantic review decisions.
  Positive and five negative evidence checks are recorded separately.

## Spec

Initial findings: **2**; one additional preservation regression found while
narrowing the question guard. Each has a red replay assertion and a fixed check.

- Exception-name advice questions incorrectly acquired a bug checklist.
- Hyphenated explicit version comparisons still created false conflicts.
- A broad question guard suppressed existing observed-failure cues. The guard
  now applies only to newly added compound exception names; literal `error`,
  `fail` and `broken` remain supported regardless of question prefix.

Final Spec re-review and the frozen source identity are recorded with the result
report. Semantic report ratings are a separate, explicitly attributed Codex
assessment, not an independent human review or permission to promote a workflow.
