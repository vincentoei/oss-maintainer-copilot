# Issue #20 Flash comparison review

Fixed point: completed GPT-4.1 reference commit
`61ecdde6de607ebdf7cf65ceeb06c4e5521f9f59`. Separate fresh-context Standards and
Spec agents reviewed `git diff 61ecdde...HEAD` at implementation `76f2910`.
The Spec agent then rechecked the exact-cost correction at `52fbc8d`.

The spec combines issue #20's original acceptance criteria, the user's explicit
request to try DeepSeek V4.1 Flash and GLM 5.3 Flash, and the separately frozen
[Flash protocol](issue-20-flash-protocol.md). Tests use the runner and capped
client boundaries previously approved by the user. No reviewer accessed the
credential or made paid requests.

## Standards

No documented-standard breaches or actionable baseline code smells were found.
The separate Flash adapter preserves the original evaluator and its source-freeze
audit. Keeping transport/accounting overlap with that frozen module was accepted
in the scoped review.

## Spec

One accounting precision issue was found: parsing a provider's numeric cost as a
binary float before converting to Decimal could lose the exact reported decimal
promised in the protocol. A regression test demonstrated this before the fix.
The corrected decoder uses `parse_float=Decimal`, retains the exact string and
rounds the spending bound upward in integer microdollars. The reviewer confirmed
the correction at `52fbc8d` and found no remaining Spec issues.

The review otherwise confirmed shared reservations including prior GPT-4.1,
durable failure halting, fallback exclusion, preserved expected outcomes,
disclosed reasoning settings and a common successful cohort across all four
models. Source and protocol were committed before the paid pass. Publication
evidence is audited separately after inference.

Final totals: Standards **0 findings**; Spec **0 remaining findings** after the
single precision correction. Focused checks passed **28 tests**; the complete
suite passed **472 tests, 2 skipped** after the fix. Lint, formatting and strict
typechecking passed. The original GPT-4.1 offline audit still passes unchanged.

The Spec reviewer also checked the completed publication against saved artifacts.
No material accuracy findings remained: scores, common cohort, costs,
reservations, tokens, latency, report statuses and per-case gains/regressions
match. The linked checks artifact was written before the final publication
commit. The offline auditor additionally verifies response/reservation field
identity, call attribution to each case/model, independent rate-cost arithmetic
and final halt/accounting state. No paid inference was repeated for review.
