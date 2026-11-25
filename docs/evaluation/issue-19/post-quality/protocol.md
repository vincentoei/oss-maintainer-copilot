# Issue #19 comparison after merged quality fixes

The user explicitly authorized finishing #56 through PR #57 before updating
PR #58. PR #57 merged to main at `9678b7285a651c5802337c88bee7c8c540de9507`;
#56 is closed. Issue #19 integrates that main without rewriting either source
history. Preserve all fifty confirmed cases, expected outcomes and earlier
evaluation artifacts against `baseline.json` (395 protected files).
The original fifty-case run remains in `../run/` and is the earlier baseline;
this is a new source/protocol freeze and a separate comparison directory.

Measure the actual merged quality fixes, including the final title-version
wording change that #56 only checked with saved responses after its live freeze.
No additional triage heuristic, model prompt/schema, expected outcome, retrieval
or scoring change is in scope. Integration only extends archived catalog
selection and the baseline-manifest CLI guard. The #16/#17/#18/#56 catalogs stay
at 20/30/40/40; #19 uses the same fifty confirmed cases and candidate pools.

Freeze and commit source, catalog, this protocol and the baseline manifest
before inference. Confirm preservation and selected serving identity/settings
before dispatch. Use shared live evidence preflight for all three workflows;
changed/unavailable openings, pinned commits or required evidence are flagged
before inference and retain unscored rows. Do not replace, truncate or drop cases.
Later discussion, reviews, labels and expected outcomes remain outside inputs.

One pass on this new frozen source: at most **250 charged dispatches**. Keyword
rules use zero; fixed RAG <=50 (one per case); bounded agent <=200 (four per
case). Retain every row, raw bounded response and durable pre-dispatch charge.
No warm-up, inference retry, repair, second pass or model search. Read-only
evidence acquisition may retry transport failures before inference.

Use unchanged `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, context 16384, temperature 0, seed 42, top-k 20, top-p 0.8,
repeat penalty 1, 256 output tokens, 20-second timeout, 65536 response bytes.
No drafting or model/default-workflow promotion.

Report the original fifty and the new fifty side by side, with per-case
score/status/candidate changes and all failures/regressions. Separate the
original forty from the ten additions; compare the forty with #56's final
recorded live source while disclosing its post-measurement wording distinction.
Report field denominators, latency, tokens, dispatches, sampled GPU residency
and marginal API cost with unmeasured costs explicit. Keep uncertainty and the
#12083 annotation disagreement visible. Do not tune expected outcomes.

Generate fresh blinded report-review artifacts without transferring ratings.
Prior Codex report reviews apply to their fingerprinted reports, not this new
pass. New usefulness/semantic support remains pending without explicit review;
accepted case confirmation remains unchanged. Single-run timing, development
case exposure, annotation alternatives and source/prompt/schema changes limit
causal attribution and generalization. Future training overlap remains unverified.
