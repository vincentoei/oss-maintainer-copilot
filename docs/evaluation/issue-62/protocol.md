# Proposed local model comparison under the #60 contract

**Awaiting review.** This is a proposal for [#62](https://github.com/vincentoei/oss-maintainer-copilot/issues/62).
Preparation has a zero-dispatch budget. The requesting user reviews the six
exact openings and proposed types, and separately authorizes the experiment.
Record their actual decision, revisions and scope before freezing the run.
Each pair shares its title. The bodies describe intentionally different issue
openings. These synthetic requests never join the historical catalog.
[Proposed contrasts](proposed-contrasts.json)

## Two local arms

Use the fixed report workflow at merged application source
`6d7fe21174153d1cb9812ac9d8cee9e12814795d`. Repeat the 3B control to measure
agreement and run-to-run drift from #60. Test whether a larger instruction-tuned
checkpoint in the same coder family can better use version comparisons and the
reporter's requested action while retaining correct bug and enhancement calls.
The two trained checkpoints differ in more than parameter count. Lower or
unchanged agreement, label switching without a net gain, and greater operating
cost are all plausible. [Upstream 7B model card](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)

| Installed Ollama alias | Parent model | Manifest digest |
|---|---|---|
| `pytest-triage:coder3b-ctx16k` | Qwen2.5-Coder-3B-Instruct Q4_K_M | `3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8` |
| `pytest-triage:coder7b-ctx16k` | Qwen2.5-Coder-7B-Instruct Q4_K_M | `863fd25a4686b53c56c1a178816edc5ede1c859fc40233e35ad5d8a898e3f7cc` |

Read-only host inspection on 2026-11-26 found Windows Ollama 0.40.16 with
both GGUF aliases installed, no resident models, and identical template
fingerprint `47fca52d970e517f889420240f615fa9f8f4c6e2cb062340b9dec6fe266385b5`
(repo JSON fingerprint). Both aliases specify 16,384 context, temperature 0,
seed 42, top-k 20, top-p 0.8 and repeat penalty 1. One RTX 5060 Laptop GPU,
8,151 MiB total, 7,883 MiB free at inspection, NVIDIA driver 592.01. The WSL
client saw six logical CPUs and about 11 GiB RAM. Free VRAM is transient.
The 7B alias occupies 4,683,087,275 bytes on disk. In #21 the 7B reached
5,356 MiB sampled device use with 12/20 correct to the 3B's 13/20 under an
earlier workflow. Those measurements support feasibility only. Qwen3 4B
Instruct-2507 is also installed but would change model family/template and
training specialization together. Select only 7B as the alternative. No
hosted arm or backend comparison. [Earlier hardware measurements](../issue-21.md)

## Requests and approval limits

- Historical cohort: all 50 cases from #60's follow-up, in ascending pytest
  issue number. Catalog fingerprint `924b506c662b51e50743f19aaa26df947230a53a09bb23789742542474daf4d7`.
  Verify original title/body hashes, opened-at cutoffs, pinned commits, and
  earlier candidate numbers through public replay with the same full catalog
  and keyword filtering. Compare encoded prompt, input, schema and token-limit
  hashes/values to the archived #60 requests. Snapshot reads and failures for
  both arms. Flag differences; skip both dispatches for that case. Keep all 50
  rows and disclose the reason for any missing pair.
- Fresh cohort: six user-reviewed openings in file order, fixed triage with
  no issue number and empty documentation topics. Inputs contain only the
  opening and normal application fields. Exclude pair IDs, review status,
  proposed types and rationale from the payload. Resolve any edits before the
  freeze. Do not pool these results with the historical scores.
- Use only #60's system instruction, label/null schema, full opening, indexed
  exact excerpts, vetted reply citations and existing validators. Never add
  the rejected #59 instruction. Keep model-native template, options and model
  identity verified at both ends of each arm. The application HTTP bodies for
  each case must be identical after excluding the model alias.
- One serial pass per alias, 3B then 7B, historical then fresh. Max 56 calls
  per model, **112 total** including failures, one per arm/case. At most 256
  output tokens each (28,672 combined maximum), 20-second timeout, 65,536-byte
  response limit. No warm-ups, retries, repairs, replacements or model search.
  Record cold load and residency; arm order limits timing comparisons. Assert
  no context truncation where telemetry allows; disclose unverified cases.
- **Downloads: 0 models, 0 weight bytes. Hosted calls: 0. Maximum model API
  cost: US$0.** Existing hardware/electricity costs are unmeasured. Public
  GitHub metadata and pinned repository evidence may be read. Stop if identity,
  settings or the local-only serving route cannot be verified.
- Before dispatch commit the reviewed input manifest, clean runner revision,
  protocol and hashes, both model identities/settings, drift flags, and numeric
  caps. Use a new #62 run directory and ledger with exclusive creation; lock
  and fsync one reservation keyed by arm/case before each HTTP request. Refuse
  duplicates, unlisted inputs, over-budget and reused directories. Interrupted
  or ambiguous calls consume their slot; preserve partial results. Never use
  an earlier ledger or reset the budget by starting a second run.

## What the types mean for this comparison

A reproducible malfunction supports bug. A credible working-to-broken
comparison can support the more specific regression type. A version in a
title alone is weak evidence. An author can describe a failure while asking
how to configure their own project. A question-shaped sentence can ask for a
correction to published guidance. Look at the requested action and what the
opening actually establishes. These distinctions help review the evaluation;
the model receives the unmodified #60 instructions.

For historical pytest #12197 the setting appears ineffective and the opening
leaves intent debatable. #12278 reports a temporal association but lacks
attribution; its accepted type is null. #12360 contrasts runtime behavior
and published guidance, with docs accepted. Keep those expectations and
uncertainty as recorded. Later labels/comments and old hosted outputs are
excluded from selection. [All prior disagreements](../issue-59/remaining-errors.md)

## Scoring, resources and decision

Publish per-case expected/predicted types, selected quote/index, provider
status, validation/transport error, eligibility flag and both arms' outcomes.
Separate valid null abstentions from rejected or missing responses. For each
cohort show correct / full planned denominator, eligible count, common valid
pairs, a per-arm confusion matrix including expected null and distinct
failure/unavailable columns, then gains and regressions on common valid pairs.
Failed or skipped rows never earn agreement. Show changes involving failures
as separate availability/validity transitions. Report the three focal class
confusions and both members correct per fresh pair, with small denominators
visible. Compare the new control to the archived 29/50 as a drift check only.

Record per-call wall time, input/output tokens, p50/p95 nearest-rank latency,
first-call loading effects, observed GPU peaks and residency/offload using
available telemetry. Report missing samples explicitly. Preserve raw bounded
responses, paired hashes, model versions and resource limits. Separate
human semantic quote-support and reply usefulness from automated agreement.
Fresh ratings need actual reviewers and remain pending.

Define an observed historical gain as more gains than regressions on paired
valid decisions and more correct over the full 50. Report fresh results
separately even if contradictory. A one-case gain on exposed issues is weak
evidence. Mixed signals, substantial validation loss or resource penalties
can support retaining the 3B. No automatic promotion, claim of population
accuracy or prompt revision follows. Any taxonomy intervention needs its own
approval and same-model control. vLLM remains a separate #22 investigation.
