# Final fixes: two-axis review before inference

Fixed point: `8444dd647e70d94ad1d48441702939601c7b76fc`. Two fresh parallel Codex
reviewers inspected the source/test/evidence diff and subsequent working fixes.
Reviews were read-only and ran no extra suite or inference.

## Standards

Documented-standard breaches: **0**. One optional naming judgment: the shared
label-cue validator also expresses general supported-prose assertions for working
controls. Its negation and quote checks are deliberately reused; this does not
justify a new abstraction for this bounded change. No other actionable smell.
Cutoffs, glossary, Conventional Commits and metadata-only publication are retained.

## Spec

Four concrete boundary findings resolved before inference: modality inside the
matched clause; a global observation override; a separately supplied failing
reproducer following a working control; and indented working controls/negated
positive failure statements. Red assertions reproduce each and focused checks
pass. Control association covers fenced/indented code; separate failing examples
are retained. Positive failure cues reject internal negation; observed negative
operations such as `is not called` still establish the reported problem.

Final re-review: **0 outstanding actionable findings**. The #12083 unchanged
annotation disagreement remains disclosed, not forced into a passing score.
New full-suite evidence: **424 passed, 2 skipped**, lint/format/mypy pass. The
initial 12 API expectation failures are preserved separately and were resolved
by retaining no-false-acknowledgement assertions while checking the intended new
deterministic-question behavior. Model fields are still validated before and
after required-statement assembly.

The final frozen comparison and fresh attributed report review are required
next; these reviews do not claim independent human usefulness assessment.
