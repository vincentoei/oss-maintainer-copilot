# Issue #50 frozen experiment protocol

Protocol v1, frozen before implementation or inference on 2026-11-23.
Starting reference: cc44852c7db55840f233f952c411dd485a8660a8.
Branch: feat/issue-50-evidence-drafting. No work on #16 or #33.

## Comparisons and attribution

A: legacy selection-only selected 3B; B: structured drafting selected 3B;
C: identical frozen drafting with shortlisted 4B; D: identical with shortlisted 7B.
A/B isolates the application contract, not model quality. B/C/D use identical
serialized evidence packets, task prompt, schema and generation limits; native
chat templates and serving digests are recorded separately. A/B evidence text is
matched; the new representation and schema are intentional application factors.
Historical #48 output used 256 tokens; fresh A/B use 512 tokens. Thus #48 versus
fresh results also contain an output-budget confound and cannot isolate drafting.
Legacy default remains 256; experimental control explicitly uses 512.

## Partitions and freezes

The unchanged twenty main-catalog cases are development/regression evidence.
Iteration 1 runs fresh A/B on those twenty (40 requests). At most one development
revision and one B rerun on those twenty (20 more). Deterministic corrections
before any real run belong to iteration 1. No case-specific reply text is added.
Freeze implementation, prompts, schemas and evidence hashes after development,
before C/D or any reserved output. Pilot results can never trigger retuning.

Reserve five additional historical pytest cases outside all twenty issue families.
Their metadata-only manifest must include human-reviewed expected outcomes,
opening-content hashes, opening cutoffs, pre-cutoff repository SHAs, family
separation rationale and explicit reviewer confirmation before inference. Selection
and annotation may inspect original inputs; implementation/tuning must not use
them. Record every input/output exposure. Do not add them to the main catalog.
Changed, unavailable or over-budget content is flagged and excluded, never silently
replaced or truncated. ADRs 0001 and 0003 apply. Full contributor bodies remain
local; publish hashes, references and bounded supporting excerpts only.

## Budgets and serving

Maximum 120 inference requests, conservatively counting warm-ups too (separately
labelled), retries, failures, agent actions and live smoke checks. Reserve 20 for
one pilot pass per arm, up to 60 development, up to 12 API/web smoke calls, and
28 transport retries/warm-ups/resource probes. Unused allocations do not authorize
extra development iterations or extra pilot passes. Charge before dispatch in a
durable ledger; ambiguous interrupted dispatches remain charged. Pilot validation
failures are final; only documented transport failure allows one retry per case/arm.

Selected identities are the #21 shortlisted Qwen2.5-Coder 3B, Qwen3 4B Instruct,
and Qwen2.5-Coder 7B, Q4_K_M, context 16384, temperature 0, seed 42, top-k 20,
top-p 0.8, repeat penalty 1. Verify actual /api/tags, /api/show and /api/ps,
including template, digest, quantization, context and GPU residency, rather than
trusting alias names. Record OS/WSL route, Windows Ollama version and connectivity.
Each response: 512 tokens maximum, 20 second client timeout, 65536 response bytes.
Evidence: original complete opening at most 16000 characters, at most 12 passages,
at most 2000 characters each and 12000 combined passage characters. Reject an
oversized opening; omit over-budget passages with explicit omission metadata.
Stable passage IDs include provenance and content fingerprints. Never truncate
contributor content without flagging it. Existing agent four-call/step and read-only
tool/output limits stay fixed. No extra model call is used for validation.

Feasibility requires full GPU residency, sampled total GPU allocation <= 7680 MiB
on existing 8 GB hardware, no allocation failure, and end-to-end report p95 <= 20 s
for fixed reports (agent smoke <= 80 s). Collect per-request latency/tokens/errors,
/api/ps and nvidia-smi samples before/after each arm. Samples cannot prove peaks.
Failed loads/fallbacks are feasibility failures, never quality successes.

## Contract and validation

Opt-in drafting shares the public fixed-report and bounded-agent report paths.
Keep required existing statements. A short generated investigation identifies exact
supplied context and the gap/comparison it asks about; factual explanations identify
passage IDs and exact supporting quotes. Explicit abstention is valid. Reject unknown
IDs, false quotes, extra source references, malformed output and instruction-like
payloads. Structural validity cannot establish semantic support. All generated text
remains an unapproved draft; explicit semantic review is required for promotion.

## Human reviews and decision thresholds

Present each evaluated final reply consistently, with anonymous candidate codes
and randomized order where practical; keep the identity key separate. Preserve
exact response/report/draft fingerprints. Human usefulness rubric from #48: useful,
partly useful, not useful; question: does the reply ask for needed details and explain
relevant evidence without misleading claims? Unsure remains pending. Record verbatim
reasons. Separately review every generated factual claim for semantic support,
unsupported assertions/presuppositions in questions, redundant detail requests,
relationship quality and appropriate abstention. Review fresh A outputs too; old
ratings cannot substitute. Do not infer approval from silence or automated checks.

Map usefulness to 2/1/0. Promote B over A only with mean paired gain >= 0.4 on the
twenty development cases AND >= 0.4 on the five pilot cases, no more than one pilot
regression, zero increase in human-confirmed unsupported claims in either partition,
all deterministic safety checks passing, complete human reviews and all resource
limits passing. Choose C or D only if it also clears those A-relative gates and
beats B by >= 0.2 mean pilot points. Ties prefer B then smaller model. Missing,
failed or pending reviews prevent promotion; never drop failures from denominators.
Do not claim independent generalization from five cases used for model selection.

Record per-case improvements/unchanged/regressions, missing-detail/type/relationship
scores and abstentions separately from usefulness; validation/transport errors,
latency/tokens/GPU measurement limits separately from quality. Preserve all attempts,
prompt/schema/evidence/application hashes and traces. Report every acceptance
criterion with evidence or precise blocker. Retain the baseline if evidence is
negative or inconclusive. A blocked run is not a completed negative experiment.
No spending, model search, fine-tuning, second repository or open-ended tuning.
