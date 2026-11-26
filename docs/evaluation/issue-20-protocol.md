# Issue #20: separately capped hosted quality reference

The reference is `gpt-4.1-2025-04-14`, a hosted quality candidate compared with
the selected local 3B model. Its greater capability is a hypothesis to measure,
not a quality result. Use the same fifty confirmed cases and candidate pools as
the [post-quality fifty-case comparison](issue-19-post-quality.md), whose
fixed-workflow output is the paired comparator. Preserve those artifacts and
all expected outcomes. No default-model promotion, agent experiment, prompt
tuning, new annotation, training, or additional ticket is in scope.

## Cases and inference

Before creating a run directory, require an exact match of the complete catalog
fingerprint, confirmed review status, opening cutoffs/hashes, repository commits
and candidate lists against the completed local comparison. Acquire public
evidence using the existing replay and freeze successful reads and failures
before inference. Changed/unavailable evidence remains flagged and unscored;
retain every case and expose its prior and current eligibility. Never replace
a flagged case or silently change the paired denominator. No live issue search,
later comments, labels, expected outcomes or reviewer annotations enter prompts.

One fixed-workflow pass, at most fifty hosted requests and one per case. Reuse
the current selection-only prompt and scorer, temperature 0, maximum 256 output
tokens, 60-second transport timeout and 65,536 response bytes. The hosted JSON
schema adds explicit integer/null typing and forbids extra properties to meet
OpenAI's strict structured-output contract. No inference retry, warm-up, repair,
model search, continuation of a started directory, or drafting. Record the exact
requested and returned model snapshot, token usage, sanitized failure types,
output, response and input fingerprints, report and trace.

The `--provider openrouter` route uses `OPENROUTER_API_KEY` and
`https://openrouter.ai/api/v1`. It requests `openai/gpt-4.1`, pins provider
`openai`, disables fallbacks and transforms, requires parameter support, and
sets routing maximum prices to US$2/US$8 per million input/output tokens.
Before creating a directory, read the public
[endpoint metadata](https://openrouter.ai/api/v1/models/openai/gpt-4.1/endpoints),
require its OpenAI endpoint name to identify `gpt-4.1-2025-04-14`, and reject
prices above the frozen rates. Preserve that metadata, requested alias, returned
model/provider and request ID. OpenRouter's completion alias does not independently
attest the upstream dated snapshot; disclose this version-verification limit.

## Independent monetary cap

Use only the standard text Chat Completions endpoint. Rates checked on
2026-11-25: input US$2/million and output US$8/million tokens, from the
[official model page](https://developers.openai.com/api/docs/models/gpt-4.1).
The [structured-output guide](https://developers.openai.com/api/docs/guides/structured-outputs)
documents the strict schema contract. Cached input receives no discount in
accounting; reported cost is a conservative token-price estimate, not an invoice.
OpenRouter additionally supplies `usage.cost`; retain its reported account charge,
rounded upward to integer microdollars, separately from the token-price estimate.
Missing, invalid or over-reservation cost halts OpenRouter inference. The
[usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)
and [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
documentation describe those fields and routing restrictions. Credit purchase
fees and taxes are outside the inference cap.
No tools, service-tier surcharge, batch mode or other billable API is requested.

Before dispatch, lock and fsync a reservation to `hosted-requests.jsonl`.
Reserve one input token per byte of the **entire serialized HTTP payload**,
plus 4,096 tokens for framing/schema expansion, and all 256 output tokens.
Byte-level text tokenization bounds visible input tokens by input byte count;
the extra framing allowance is a conservative assumption, not an API guarantee.
Check returned usage against both bounds; halt if usage, model identity or
transport is uncertain. Retain all reservations without refund, including HTTP
errors, timeouts, malformed envelopes, interrupted calls and successful calls.
An outstanding reservation also prevents dispatch after restart or concurrent
use. A new directory is required for the evaluator; this is not a resume feature.

The sum of reservations may never exceed **4,999,999 microdollars
(US$4.999999)**, separate from local inference accounting. Exact integer
arithmetic avoids rounding at the cap. Refuse requests before dispatch if the
next reservation would exceed it or repeat a case. Unknown usage/cost stays
null; record known costs separately and preserve the worst-case reservation.
The cap depends on the recorded provider rates and framing bound. Recheck
pricing before a later run. Taxes and unrelated account activity are outside
this workflow's model-API cap. An account/project spending limit is useful
additional protection but is not claimed to have been configured here.

## Publication and interpretation

Publish the reference's `results.json` and request ledger without credentials or
bulk contributor bodies. Each row separates `hosted_report`, `expected_outcome`,
`case_review`, `local_fixed_scores` and hosted `scores`. Confirmed annotations
retain their original reviewer attribution, including accepted Codex delegation;
they are not uniformly independent human assessment. A hosted prediction never
becomes an expected triage outcome. Report field denominators and failed calls;
fallback reports must not be described as successful hosted inference.
Rejected selections and failed requests retain fallback reports but receive no
hosted score. Publish paired hosted and local aggregates over exactly the same
successful case IDs, alongside full-catalog aggregates and each exclusion reason.

Missing-detail detection and duplicate retrieval remain deterministic components
of the fixed workflow. This comparison measures model selection of supplied
type evidence and reply statements, not unrestricted hosted triage. Field scores
do not establish semantic citation support or useful replies; fresh report
ratings remain pending. Development-case exposure, provider training overlap,
single-pass variability and source changes limit generalization and causal
attribution. A preflight or simulated endpoint response supplies no model-quality
evidence.

## Commands

Use a fresh directory for each command. The preflight performs public reads but
does not require an API key or make paid calls:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.hosted_evaluation --preflight-only \
  --directory /tmp/issue20-preflight-new
```

For the single paid pass, expose `OPENAI_API_KEY` through the environment and
run the same command without `--preflight-only`, with a fresh directory.
Alternatively expose `OPENROUTER_API_KEY` and add `--provider openrouter`.
The repository's ignored `.local/issue20.env` may hold that variable locally;
load it into the process environment before running the command.
Missing credentials cause failure before directory creation or provider access.
Never put a credential in a tracked file, command argument or published artifact.
