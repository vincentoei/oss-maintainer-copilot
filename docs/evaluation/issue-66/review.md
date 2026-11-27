# Issue #66 preparation review

Attribution: two separate Codex/AI review agents with fresh contexts, one per
axis, using the code-review skill. These are source reviews, not human ratings
or independent semantic ratings of future model reports. Neither reviewer made
network or model calls. The implementing agent aggregates their findings here.

Fixed point: `main` at `2194e338e2a82a9f54ab1ef06903944508523fa3`.
Initial reviewed commit: `1a055a5`,
`chore(evaluation): prepare semantic support investigation for #66`.
Diff command: `git diff 2194e338e2a82a9f54ab1ef06903944508523fa3...HEAD`.
Deadline/arm-definition corrections were separately verified in the working tree
before the final source freeze. Final checks and evidence files were added after
the full test suite finished.

## Standards

No hard breaches of the supplied AGENTS, domain, glossary or ADR standards were
found. Historical inputs remain local, archived expectations remain unchanged,
and synthetic examples and AI judgments are explicitly attributed.

The initial review found one executor correctness concern: socket-operation
timeouts did not enforce the protocol's total 20-second dispatch deadline.
Resolved with a serial main-thread POSIX `SIGALRM` deadline covering connection,
normal response reads and HTTP-error body reads. Metadata has a five-second
deadline. The offline probe interrupted a five-second operation after 0.030
seconds and restored the signal handler and timer state.

One possible Duplicated Code smell noted the repeated control/candidate arm
definition. Resolved by using the same `ARMS` tuple for preparation and execution.

Follow-up Standards review: both findings resolved; no remaining documented
standard breaches or baseline smells. The deadline assumes the documented
serial, main-thread POSIX execution.

## Spec

Initial finding: the report referenced `checks.json` and `review.md` before those
artifacts existed. Resolved by adding the actual check results and this review
after test/review completion; no anticipated results were used as evidence.
The Spec reviewer independently verified both files and cleared the finding in
a follow-up read-only review before the final commit.

The reviewer found no scope creep and no further concrete defect in the frozen
candidate, examples or protocol. Examples distinguish credible regression,
ordinary malfunction, outdated documentation, retracted comparisons, enhancement
ambiguity, insufficient quote support and sampler omission. All labels and null
remain offered, prior expected outcomes remain intact, and R48 is exposed
diagnostic evidence. Prompt guidance is accurately described as providing no
semantic guarantee.

The actual paired model/report comparison is explicitly **partial**: request
capture and archived-report replay are verified; new control/candidate responses,
gains/losses and attributed review of actual candidate type/quote support remain
unavailable. Human expectation confirmation and adoption review are pending.
Completing these requires separate execution authorization; they are not passing
acceptance evidence and do not justify adoption.

Summary: Standards has zero remaining findings after two corrections. Spec has
zero remaining preparation blockers after adding evidence; the live comparison
and human review requirements remain unverified for the stated authorization
and evidence reasons. The ticket is not claimed fully accepted or resolved.
