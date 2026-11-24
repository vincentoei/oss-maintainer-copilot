# Small replay follow-up

Final checks: all thirty public cases replay successfully with controlled
responses (28 complete, two partial for intentionally unavailable historical CI).
The full #12204 opening also passes the controlled bounded-agent path. Ruff,
formatting and strict mypy pass; the final full suite passes **354 tests, 2
skipped**, and focused replay/runner checks pass **58 tests, 2 skipped**. The live
HTTP schema still declares a 16,000-character body limit. No provider inference
was run during the follow-up.

The #12204 opening contains 40,484 characters. Historical replay previously used
the live request model's 16,000-character body limit after verifying the opening,
so this valid historical case could not reach triage.

Replay now uses a small internal subclass with a 65,536-character body limit.
It retains the existing title/number/location validation and whitespace
normalization. Only replay constructs it, after verifying the issue's content
hash, timestamp and pinned commit. Larger openings are explicitly flagged before
any model call. The live API/Python request model still limits bodies to 16,000
characters. No truncation, validation bypass or new configuration was added.

The agreed replay seam reproduces the bug with verified 16,001- and 65,536-character
openings. Those regressions failed on the original 16,000-character validator and
now assert that the complete content reaches the model. They also prove the live
model still rejects the same bodies. A 65,537-character opening remains flagged
without a model call.

The #12263 lookup failure was transient: both the regular commit endpoint and the
exact Git commit endpoint used by replay returned the original SHA and pre-cutoff
timestamp when rechecked. The live replay artifact records the replay outcome.
The first follow-up pass then hit a commit timeout on #12281. Commit reads now
retry `TimeoutError` once with the same eight-second timeout and response-size
bound. Other errors are not retried; a second timeout flags the case before any
issue/model call. Regression tests exercise recovery and exactly two failed
attempts through `replay_case`. No changed evidence cutoff or inference retry
was introduced.

The original 90-row real-model run, 115 dispatches, 87 scores and 29 eligible cases
remain archived unchanged. The offline verifier now checks their application
source hashes against their original full inference commit
`8640bae3193086e7428093df0e0fda58c57bdab5`, instead of requiring current source to
remain identical forever. That Git commit must be available locally. Follow-up
replays use controlled responses and do not constitute updated model quality
measurements, semantic support ratings or human usefulness ratings.

[Initial replay](live-replay.json) preserves the 29 successful cases and #12281
timeout before the timeout-only retry was added. [Final replay](live-replay-after-retry.json)
records the subsequent public opening/cutoff checks and an additional controlled
agent check for #12204. [Checks](checks.json) records focused and full-suite
validation, including the initial formatting failure and its correction.
Source hashes in both live artifacts bind the implementations used.
