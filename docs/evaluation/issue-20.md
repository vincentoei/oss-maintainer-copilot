# Issue #20: capped hosted quality reference

The single OpenRouter/OpenAI GPT-4.1 pass completed on **all fifty reviewed
cases**, with **50 requests**, **81,499 input tokens**, **1,030 output tokens**
and **US$0.171238** reported inference cost. Every case passed public evidence
preflight with the same eligibility, cutoffs, pinned commits, opening hashes and
candidate pools as the saved local fixed-workflow comparison. No inference
request failed and no usage was missing. The selected local model and default
workflow are unchanged.

Hosted type agreement is **31/50**, versus **29/50** for the local fixed workflow.
There are three gains and one regression. Missing-detail and duplicate scores
remain unchanged because the reference reuses those deterministic components.
This establishes a small type-selection gap on these development cases; it does
not establish unrestricted hosted triage quality, useful replies or a promotion.

## Acceptance evidence

| Acceptance criterion | Evidence |
| --- | --- |
| Same eligible cases and cutoffs; record version, requests, tokens and cost | [Results](issue-20/run/results.json) contain 50 preflight entries and 50 scored rows. Catalog fingerprint matches the post-quality #19 run. Each row preserves cutoff, commit, opening hash and candidate numbers. The target snapshot is `gpt-4.1-2025-04-14`; OpenRouter request/response alias is `openai/gpt-4.1`, provider `OpenAI`. Published endpoint metadata names `OpenAI \| openai/gpt-4.1-2025-04-14`. The [ledger](issue-20/run/hosted-requests.jsonl) and accounting record all 50 requests, 81,499/1,030 tokens and US$0.171238 reported cost. The [offline verification](issue-20/verification.json) checks every row and recomputes all scores. |
| Stop before the separate US$5 cap is exceeded | The ledger contains a durable reservation before each dispatch. Reservations total **US$1.183980**, below the hard **US$4.999999** limit; reported and token-priced costs both total **US$0.171238**. [Focused tests](../../tests/test_hosted_evaluation.py) exhaust the monetary cap before 50 requests, observe reservation persistence at the HTTP boundary, restart clients, and cover failed/interrupted requests plus the response/halt crash window. No cap refusal was needed during this small live pass. The [protocol](issue-20-protocol.md) states the price and token-framing assumptions behind the bound. |
| Published comparisons distinguish hosted output from reviewed expected outcomes | Every results row separates `hosted_report`, `expected_outcome`, `case_review`, hosted `scores` and `local_fixed_scores`. Paired aggregates use identical successful case IDs; no expected outcome or reviewer attribution was changed. The comparison below labels model predictions separately from the confirmed annotations. Fresh semantic citation support and reply usefulness remain pending. |

OpenRouter's completion response identifies its alias, not an independently
attested upstream dated snapshot. The run preserves the advertised dated
endpoint metadata and explicitly records that verification limit. The cap
assumes the published rates and conservative framing bound continue to hold;
provider invoicing, taxes, credit purchase fees and unrelated account activity
were not audited. These limitations do not become measured zero costs or
independent version attestations.

## Freeze and reproduction

Updated main was `666f5150d3b1e1da5dd24cd851e0daf69c3f26d7`; the dedicated
branch is `feat/issue-20-hosted-quality-reference`. Reviewed implementation
`8fba053ee94af2947c2f969e6ee9f3732d51b649` and the
[source/protocol/baseline freeze](issue-20/freeze.json) were committed before
inference; the freeze commit is `6662309`. The recorded pass began
**2026-11-25 15:36:09 UTC**. All application files shared with the saved local
run match its source hashes; the hosted evaluator is the added module.

The [protocol](issue-20-protocol.md) allows one pass, one request per case,
at most fifty dispatches, temperature 0, 256 output tokens, 60-second timeout,
65,536 response bytes, no drafting, warm-up, retry, repair or model search.
Public evidence is frozen before inference. Later comments, labels, annotation
rationales and reviewer identities never enter model inputs. The credential is
kept in ignored local storage and is absent from published artifacts and Git.

Use an environment containing `OPENROUTER_API_KEY` and a fresh directory to
reproduce the workflow. This command performs a new paid pass; it does not
resume or overwrite the published one:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.hosted_evaluation --provider openrouter \
  --directory /tmp/issue20-new-run
```

Add `--preflight-only` for credential-free public evidence checks. Use
`--provider openai` with `OPENAI_API_KEY` for the direct dated-snapshot route;
that direct route has controlled-response tests but was not exercised with a
paid OpenAI credential in this run.

Audit the published results without network access, credentials or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_verify.py
```

## Paired comparison

The local column reuses the preserved #19 post-quality fixed-workflow results;
it is not a new contemporaneous local inference run. All fifty cases are paired,
with no exclusions or provider failures. Aggregate `completed` means scored
reports. Four reports in each workflow remain application-status `partial`
because historical CI is unavailable, independently of model inference success.

| Measurement | Saved local fixed workflow | Hosted reference |
| --- | ---: | ---: |
| Eligible / scored / paired cases | 50 / 50 / 50 | 50 / 50 / 50 |
| Type agreement with confirmed annotations | 29/50 | 31/50 |
| Exact missing-detail agreement | 43/50 | 43/50 |
| Detail macro precision / recall | .940 / .930 | .940 / .930 |
| Expected-earlier-issue retrieval | 6/50 | 6/50 |
| Relationship exact score | 2/47 | 2/47 |
| Structural citation validity | 50/50 | 50/50 |
| Complete / partial report status | 46 / 4 | 46 / 4 |
| Inference requests | 50 | 50 |
| Input / output tokens | 81,934 / 1,287 | 81,499 / 1,030 |
| Mean report latency, ms | 411.66 | 1,435.67 |
| Nearest-rank p50 / p95 latency, ms | 301.230 / 855.583 | 1,340.106 / 2,372.882 |
| Marginal model API cost | US$0, local Ollama | US$0.171238, OpenRouter-reported |
| Fresh usefulness / semantic support | pending | pending |

Three uncertain relationships are unscored. Relationship exactness requires
retrieval of the annotated earlier issue even for nonduplicates; 2/47 is not
binary duplicate accuracy. Structural citation validity can pass vacuously and
does not establish semantic support. Local and hosted latency reflect different
servers, transport and measurement times; hardware, electricity, network and
total operating cost are unmeasured.

## Type changes and remaining uncertainty

The [type-change artifact](issue-20/type-changes.json) retains every changed
prediction, including changes where both models disagree with the annotation.
Confirmed outcomes are the scoring reference and retain their original review
attribution, including explicitly accepted Codex delegation; they are not
uniformly independent human assessments.

| Case | Confirmed expected type | Local prediction | Hosted prediction |
| --- | --- | --- | --- |
| #10156 | docs | infrastructure | question |
| #12219 | bug | docs | abstains |
| #12223, regression | bug | bug | question |
| #12305 | question | bug | regression |
| #12308, gain | regression | bug | regression |
| #12367, gain | regression | question | regression |
| #12377, gain | docs | question | docs |

The net gain is two cases, or four percentage points. Nineteen hosted type
predictions still disagree with confirmed annotations. The known missing-detail
and duplicate-retrieval problems remain; this ticket does not tune them or
change expected outcomes. The #12083 detail annotation disagreement remains
disclosed in the baseline. Development-case exposure, unknown provider training
overlap, the constrained selection contract and single-pass variability limit
generalization. No fresh human report review was supplied, so usefulness and
semantic citation support remain explicitly unverified.

## Validation and review

[Recorded checks](issue-20/checks.json) passed lint, formatting, strict
typechecking, **17 focused hosted-reference tests**, and the full suite:
**461 passed, 2 skipped**. The skipped tests require `RUN_LIVE_REPLAY=1` for
separate public replay checks; this live pass independently verified public
evidence for all fifty cases. The first sandboxed full-suite process stalled
before producing results and was terminated; the complete suite then passed
outside the sandbox in 14.69 seconds. No unrelated source fix was needed.

The [two-axis review](issue-20-code-review.md) has zero hard Standards violations,
one optional JSON-record typing suggestion, and zero remaining Spec findings.
Regression checks were observed failing before fixing invalid-selection scoring,
cohort pairing, OpenRouter integration/price changes, interruption handling and
the durable-halt crash window. The offline audit verifies the preserved local
baseline, frozen hashes, all fifty recomputed scores and paired denominators,
and every request/response reservation and usage record. Paid inference was not
repeated after viewing results.
