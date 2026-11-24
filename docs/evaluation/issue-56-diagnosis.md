# Issue #56 diagnosis and regression checks

Scope: follow-up fixes requested after PR #55 verification. Work begins at
`abe7540de2fe0891c2aa00a4cadc67eef51a7b89` in an isolated worktree on
`fix/triage-report-quality`; PR #55's branch is untouched. Forty expected
outcomes and all 269 prior case/evaluation files remain unchanged.

## Feedback loop

`PYTHONPATH=src pytest tests/test_triage_quality_replay.py -q` exercises the
previously approved historical replay interface. External GitHub/model boundaries
are controlled; the real report builder, repository policy, schema adapter,
quote validation and trace accounting execute. Assertions target missing or
redundant requests and validated type selection, not implementation calls.

The original unminimized package-table harness printed
`Missing details: ['pip list output']` and failed, despite supplied environment,
code and a valid editable-install table. Removing the third column from only its
header made the request disappear, isolating the rigid parser from model/replay
handling. A minimized table and editable package row became the first regression
test. After the fix the original harness prints `Missing details: []`.

[Baseline red run](issue-56/red-pr55-baseline.txt) runs the new regressions against
a pristine temporary `git archive` of PR #55's source. Per-slice red artifacts in
`issue-56/red-*.txt` record failing assertions before the corresponding fixes.
No input mutation or changed expected outcome creates the signal.

## Confirmed causes and changes

- **Package evidence:** a two-column-only header/row parser misses pip's editable
  install column and installed dependency graphs. Recognize those formats while
  requiring actual distribution rows and an installed graph marker. A full-suite
  run caught an overly broad optional third column accepting version prose;
  restrict it to a Unix/Windows editable-install path. Empty tables/prose remain
  missing. The four existing API/drafting regressions subsequently pass.
- **Environment evidence:** Markdown labels, named/rolling OS releases and pytest
  session-version syntax are missed. Normalize presentation only, recognize those
  identities and remove Python/pytest/pluggy versions before looking for an OS
  release. A generic Linux banner with only software versions remains incomplete.
  Ask only for the missing pytest or OS half, retaining the same scored field.
- **Reproducers:** valid pytest functions do not require an underscore after
  `test`. A development pytest self-test command plus an exact failing `testing/`
  node is also reproducible without copying its implementation into the opening.
- **Applicability:** explicit exception/failure titles and a reported collection
  error or observed expected-behavior mismatch can establish a bug-report template
  without a literal `Bug:` prefix. A broad `unexpected` rule was removed when the
  preview exposed an unwanted request on a confounded fixture-scope report;
  generic questions still abstain. Template choice is distinct from issue type.
- **Feature answers:** an explicitly rejected existing flag with its lost behavior
  supplies an alternative; reading documentation in low light supplies a concrete
  use case. Untried hypothetical wrappers and placeholders still remain missing.
- **Follow-up:** an older session explicitly labeled as a comparison is not
  conflicting with the current environment. Preserve clarification when a listed
  version and its unlabeled session differ.
- **Type selection:** independent label and quote enums permit the mismatched pair
  captured for #12216. The decoder now selects one explicit indexed evidence pair;
  the adapter preserves public report fields and performs the existing quote,
  label, negation, citation and required-reply validation. Invalid/bool/out-of-range
  selections abstain and retain provider usage. `regressed` and an explicit
  `warn if` feature request are supported cues, not forced classifications.

## Alternatives tested and boundaries

Initial ranked package hypotheses were header rigidity, separator/spacing, and
evidence loss after parsing. The one-variable header probe isolated rigidity;
editable rows/separators were then covered at replay. For model rejection, the
ranked causes were independent field pairing, quote truncation, and negation.
A decoder following the old supplied enums reproduced an unsupported pairing;
atomic pair selection removed it without relaxing quote validation.

The loops run in seconds and reproduce the actual call patterns, so bisection,
broad logging and temporary production instrumentation were unnecessary. No
debug instrumentation was added. One sandboxed API-test attempt stalled and was
terminated; the same checks passed outside the sandbox. The initial full-suite
failure is retained in `issue-56/checks-before-package-guard.json` and is not
reported as passing.

The deterministic development preview improves keyword missing-detail exact
agreement from 17/40 to 31/40 with no previously correct detail result regressing,
and type agreement from 16/40 to 18/40. These are development observations, not
real-model or generalization claims. A separately frozen capped pass measures
the real workflows under [the protocol](issue-56-protocol.md). The explicit
Codex report-review sidecars preserve attribution and every report fingerprint;
they do not claim independent human review or change old pending rating files.
