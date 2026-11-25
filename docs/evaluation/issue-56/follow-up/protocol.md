# Issue #56 follow-up measurement

The requesting user asked Codex to complete the remaining reproducible code fixes
in PR #57. This is one additional, separately frozen measurement of changed source,
not a retry of the archived pass. Preserve the 323 existing case/evaluation files
in baseline.json, including both prior 120-report comparisons and their reviews.
Keep all forty cases and expected outcomes byte-identical.

Freeze the source commit, all application Python hashes, this protocol and catalog
before dispatch. Use the existing forty-case replay/comparison interfaces with
`--issue 56 --protocol docs/evaluation/issue-56/follow-up/protocol.md` and a new run
directory. The runner records this exact protocol hash. Same verified opening
identities, pinned commits, cutoff-safe candidate pools and expected outcomes;
never use annotation rationales, later labels/comments or assistant ratings as
input. Full contributor bodies remain temporary under ADR-0003.

This pass has its own **200-dispatch cap**: fixed <=40 (one/case), agent <=160
(four/case), keyword zero. Persist each charge before dispatch. Retain all 120
rows and bounded raw responses, including partials, omissions, wrong types and
validation failures. No inference warm-up, retry, repair, model search or second
pass on this frozen source. Public evidence acquisition may retry read failures.

Retain the selected `pytest-triage:coder3b-ctx16k` model, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`, Q4_K_M,
context 16384, temperature 0, seed 42, top-k 20, top-p .8, repeat penalty 1,
256 output tokens, 20-second timeout and 65536 response bytes. Verify serving
identity/settings before dispatch and final residency. Keep fixed RAG default.

Compare every field/status and resource against both archived #18 and the first
#56 pass. Expose denominators, per-case gains/regressions, abstentions, validation
errors, dispatches, tokens, latency and sampled GPU memory. These already exposed
development cases do not establish generalization. Different source, prompt,
schema and serving behavior limit causal attribution.

An offline preview finds a preserved annotation disagreement at #12083: its
accepted expected detail set requires only packages, while the opening names
Linux/macOS without their releases. The new rule asks for packages and OS/release
while recognizing the described reproducer link. Do not suppress a legitimate
question or alter the outcome to make this score exact. Report this discrepancy
and distinguish it from a missed request.

Review all new reports freshly against verified openings and pinned citations,
with exact report fingerprints, explicit Codex attribution, actual reasons,
support/partial support/abstention, redundant or missing subquestions and 0/1/2
usefulness. Group only identical claims for the same opening, with separate type
fields visible. This is unblinded assistant assessment, not independent human
validation. Preserve original pending files. No workflow promotion follows.

Independent human ratings, unavailable historical CI and overlap with a future
training corpus remain evidence limitations; do not fabricate passing results.
