# Local model comparison publication review

Reviewed the full stack from merged main `6d7fe21` through `5fc8a5e`, followed
by the response-read correction in this publication. The scope is #62's
installed-model comparison and the subsequently requested, separately capped
downloaded-model preflight and three-model comparison. Issue #63 uses this
publication as its baseline; no promotion inference is part of this review.

## Standards

No documented-standard breaches were found against AGENTS.md, the agent guides,
glossary, evaluation ADRs or project configuration. The reviewer found one P2
correctness issue: a connection reset or timeout while reading an HTTP 200 body
retained the HTTP status but lost its transport-error class, and the offline
replayer could not reproduce that charged failure.

The correction observes errors throughout the response context and reproduces a
recorded body-read failure after returning its recorded HTTP status. New public
runner/replay regressions failed before the correction, then passed for both
connection reset and timeout. They verify that the reservation exists before
dispatch and that the failed report remains in a full denominator with zero
agreement. The Standards reviewer independently repeated both fault simulations
and confirmed the P2 resolved. No further material findings remained.

## Spec

No remaining findings. The original 112-call comparison and the later approved
168-call comparison retain separate freezes and ledgers. Original case metadata,
expected outcomes, public-input hashes and earlier reports remain unchanged.
The separate protocol accounts for downloads and the four unscored preflight
calls. No candidate was promoted and no rejected prompt was added to production.

The 7B and Qwen3.5 scores of 34/50 and 38/50, seven gains and three ordinary-bug
losses, and all three 5/6 synthetic scores reproduce offline. Human semantic
support/usefulness ratings, physical residency of every tensor, independent
truncation evidence and unseen generalization remain unverified as disclosed.
The Spec reviewer independently replayed all 112 original #62 responses against
the retained public snapshot and checked exact complete report/quote equality.

The response-read correction changes no archived observation or score. Seven
offline checks pass, and the scored publication reproduces byte for byte. These
checks and review made no new model calls or downloads. Ruff lint/format and
mypy pass. The pre-correction full suite passed 504 tests with two opt-in skips;
the final publication's checks are recorded in the pull request.

Standards: 0 remaining hard findings; the P2 transport-audit issue was resolved.
Spec: 0 remaining findings.
