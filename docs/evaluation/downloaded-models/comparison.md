# Proposed scored comparison against the #62 local 7B reference

The objective is paired agreement on bug versus regression, question versus defect and documentation defect versus usage question. Treat each candidate as an Ollama serving configuration including its tokenizer, native renderer/parser and any draft model. A small shared opening tests transport compatibility. It has no confirmed type and contributes zero scored rows. [Artifact research](research.md) · [Preflight freeze](preflight.json)

**Proposal for approval.** Run the installed Qwen2.5-Coder 7B reference, Gemma 4 E2B and Qwen3.5 4B serially with `reasoning_effort: "none"` on every request. Both candidates passed the explicit-off gate, and neither produced validated JSON on its single ordinary probe. These measurements establish configuration compatibility on one opening. The 7B has no explicit-off preflight result; its first scored request doubles as its compatibility check and consumes its normal slot. Zero scored requests have been sent. [Observed compatibility and limitations](preflight.md)

| Scored alias | Frozen local manifest SHA-256 |
|---|---|
| `pytest-triage:coder7b-ctx16k` | `863fd25a4686b53c56c1a178816edc5ede1c859fc40233e35ad5d8a898e3f7cc` |
| `triage-eval:gemma4-e2b-16k-v1` | `94d69e727168d1101645f07c651f7677776c48859760fa28ea93d753ccbb92c6` |
| `triage-eval:qwen35-4b-16k-v1` | `8da535b12863762c2403ed06956d92da4e57806a4772ba321137a2809e9a8bbe` |

## Cases and controls

Use the same 50 exposed historical pytest openings and six separately reported, previously reviewed synthetic contrasts. All 56 have already been used in #62. There is no new holdout in this proposal. Use the original expected types, including null, the same opening cutoffs, candidate pools, source snapshots and citation IDs. Reverify inputs before dispatch and keep every changed, missing or ineligible row in the published denominator. The #62 7B scored 34/50 and 5/6. Repeat its installed 7B alias as a contemporaneous reference and record type-level drift. [#62 inputs](../issue-62/preparation.json) · [#62 reference](../issue-62.md)

Use the same issue text, system message, JSON Schema, indexed quotes and application validators in every arm. Prohibit free-text repair, new prompt instructions and fallback classifications. Compare normalized request bytes across arms, pinning every permitted difference. The explicit-off field is an evaluation-only addition to all three requests. The archived 7B scores provide context for drift.

Measure tokenizer-specific context use. Freeze the template and tokenizer for each alias. Where exact local counting is supported, check rendered input length plus the 256-token allowance against 16,384 before dispatch. Flag overflows, truncation evidence and unknown truncation status. A successful short probe establishes the allocated window, not preservation of every long opening. In particular the longest #62 prompt used 14,970 input tokens on the 7B tokenizer.

A candidate qualifies in a mode only when the same preflight request receives HTTP 200 from the pinned alias, finishes with `stop`, passes the production validator and shows Ollama-reported full GPU residency at 16,384 (`size_vram == size > 0` for the matching digest). The explicit-off arm also requires zero exposed reasoning characters. If the first charged reference response rejects the field, fails the contract, exposes reasoning or fails the 16K residency check, halt and report the partial run. Never switch modes mid-run. Preflight runs the ordinary request first and the explicit-off request second; cold load and cache state can affect the difference.

## Limits and execution

At most three arms, one serial pass of 56 per arm. With the reference and both candidates the ceiling is **168 local calls and 43,008 output tokens**. With one eligible candidate the ceiling drops to **112 calls and 28,672 output tokens**. If neither qualifies, stop. The ceiling includes failed, interrupted and timed-out attempts. Zero warm-ups, retries, repairs, downloads, hosted calls or API fees in the scored phase. Ministral has no scored allocation. Hardware and electricity costs are unmeasured.

Before any scored call, obtain approval for the selected mode and arms, commit the runner, immutable local alias digests and effective parameters, Ollama version, per-case request hashes, expected types, cohort order and numeric limits. Use a new output directory and durable, exclusive per-arm/case reservations written before dispatch. Keep the #62 freeze, reservations, raw outputs and scores available for offline verification. Run the reference first, then eligible candidates in Gemma/Qwen order; record cold loads and interpret latency in light of the fixed order. One GPU, serial text-only requests, 16,384 context, temperature 0, seed 42, top-k 20, top-p 0.8, repeat penalty 1, 256 output tokens, 20-second application timeout and 65,536 response bytes. Check served manifest, GPU residency and version across arms. Halt on identity changes. Preserve charged calls, including failures, on interruption.

## Decision and evidence

Report correct/full denominator, eligible/common-valid counts, per-class confusion including null, paired gains and losses by issue, valid abstentions and validation/transport/truncation failures separately. Report both members correct for each synthetic pair. Report end-to-end and model-call p50/p95, cold call, token usage, termination reason, GPU samples and residency. Record exposed reasoning length when available. Separate native-template tokenization and serving effects from claims about checkpoint quality. Human quote-support and reply-usefulness ratings require actual reviewers.

Call an observed historical gain only when the candidate beats the contemporaneous reference on the full 50 and has more paired gains than losses on common valid decisions. Also report any net loss of bugs, questions, regressions or enhancements, and conflicting synthetic results. The exposed cohorts, single pass and lack of new human ratings limit promotion decisions. The experiment supplies evidence for a later default decision.
