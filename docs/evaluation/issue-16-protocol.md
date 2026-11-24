# Issue #16 frozen workflow comparison

Frozen before implementation and inference, 2026-11-24. Starting main:
`2e1da92edaedc280af8af099555714e5fed25136`. Scope: #16 only.
The baseline manifest preserves all existing evaluation artifacts, twenty catalog
cases and model files. The #50 negative decision stands: selected 3B and legacy
selection-only application; no drafting, model search, fine-tuning or prompt tuning.

## Arms and evidence

K: existing KeywordRuleModel with fixed retrieval. F: existing legacy
OpenAICompatibleModel with fixed retrieval. A: existing legacy
OpenAICompatibleAgent with its three action decisions and final report selection.
All use replay_case, the same verified opening, pre-cutoff candidate catalog,
pinned documentation/source/template, unavailable historical CI and score_report.
Agent read decisions may select less evidence; that is the experimental factor.
Historical options must be threaded through the agent without changing live defaults.
No expected outcomes, later labels/comments or relationship annotations enter input.

Preflight verifies every case and its entire eligible candidate pool once into a
shared in-memory cache. An integrity failure flags that case in all arms. Keep
twenty rows per arm, including flags/errors; no replacements or silent truncation.
Use full legacy openings, including #12204; context rejection remains an error.
No #50 passage-packet/drafting opt-in. Do not reuse old outputs or human ratings.
Freeze application source hashes in the run artifact before dispatch.

## Inference budget and execution

One pass only: at most **100 actual inference dispatches** (20 F + at most 80 A).
K has zero inference. F <=1 per case; A <=4 per case; 256 output tokens per
dispatch, 20 second client timeout, 65536 response bytes. No warm-ups, retries,
smoke inference, revision or second pass. Failed and interrupted dispatches count.
Durable locked/fsynced pre-dispatch ledger; a started output directory is never
resumed or overwritten. Failure-only fallback reports are scored but not successes.
Persist each completed case before starting the next. Metadata/resource HTTP reads
are not inference and may be repeated. No endpoint availability implies no inference.

Cycle through the six permutations of K/F/A in issue-number order to reduce order
bias (twenty cannot balance six exactly). Acquire evidence before timing. Latency
covers workflow and cache reads, not initial public evidence acquisition; report
acquisition separately. No forced unload or warm-up; cold loads are included.
Record order, raw responses, prompt/input/schema hashes, report, trace, errors,
tokens (unknown stays null), GPU samples and serving snapshots. Store full contributor
openings only locally, following ADR-0003; public artifacts contain hashes and
bounded report/model excerpts. Do not publish full serialized prompts/inputs.

## Serving and costs

Exact alias `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Qwen2.5-Coder 3.1B Q4_K_M. Verify /api/tags and /api/show against preserved
issue-48-serving-review.json: context 16384, temperature 0, seed 42, top-k 20,
top-p 0.8, repeat penalty 1. Capture actual template hash and server version;
changed identity/settings blocks inference. Capture /api/ps before/after the run
and device-wide 500 ms GPU samples per workflow. Residency/peak limitations must
be disclosed. No generation settings are changed to make the comparison succeed.

Local model and public GitHub marginal API charge: USD 0. Report model dispatches,
input/output tokens, elapsed time and sampled GPU memory as resource proxies.
Hardware, hosting, electricity and network costs are unmeasured, not zero.
K's model token use is exactly zero; missing provider usage for F/A stays unknown.

## Scores, failures and decision

Use existing exact field metrics unchanged: issue type, missing-detail exactness,
precision/recall, retrieval, relationship, structural citations and abstention.
Report denominators, partial reports, model/action/tool errors, flagged cases,
mean and nearest-rank p50/p95 latency, and representative per-field failures.
Relationship uncertainty stays unscored; additional retrieved issues and semantic
citation support remain unreviewed. Do not present structural validity as semantics.
For paired quality, average type correctness, missing-detail exactness and known
relationship correctness per case. Compare the same scoreable cases only; also
report twenty-case coverage and missing pairs so dropped failures cannot win.
Human usefulness uses fresh blinded 2/1/0 reviews (useful/partly/not useful), with
verbatim reasons, semantic support, redundancy, relationship and abstention notes.
Prepare a shuffled review sheet and separate identity key with report fingerprints;
pending or absent reviews cannot count as human quality gains.

Keep fixed legacy as the demo default unless A satisfies ALL: twenty complete
paired reports, no additional partial/model/tool errors, structural validity no
lower, mean paired exact-field gain >=0.05 and no field accuracy drop >0.05;
complete fresh human reviews with mean usefulness gain >=0.2 and no increase in
unsupported claims; p95 latency <=80 s AND <=2x F; total known input+output tokens
<=2x F; verified full GPU residency and sampled memory <=7680 MiB. Otherwise
retain fixed legacy and explain failed/pending gates. These are conservative demo
selection gates on an already exposed development set, not generalization claims.
No production promotion or UI changes are needed when fixed remains selected.

## Verification seams

The user approved both public boundaries: historical replay (cutoffs and pinned
evidence across workflows) and comparison runner/CLI (durable budget, shared
eligibility, failure accounting, paired summaries). Controlled endpoint tests
establish behavior only. Run focused tests/typechecks during implementation, full
suite at completion, and separate Standards/Spec reviews before final delivery.
