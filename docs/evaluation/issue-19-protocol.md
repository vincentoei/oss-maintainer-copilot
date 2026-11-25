# Issue #19 fifty-case final expansion protocol

Scope: issue #19 only, from updated main
`9d4bb25a31b6f7f32d748d27eec243fda68ec720`. Preserve all forty existing
cases and prior evaluation artifacts against `issue-19/baseline.json`.
Add the first ten unedited substantive historical pytest openings after #12328,
May 22–27, 2024. Verify matching REST/GraphQL text and creation times, no edits,
title/body SHA-256, independently checked pre-opening commits and both pinned
templates. Publish metadata and provenance under ADR-0003; keep temporary full
opening copies outside the repository. Later discussion is annotation only.

The requesting user explicitly chose “Delegate case review to Codex and accept
its confirmation.” Record confirmation after provenance verification and before
inference. This is assistant review accepted by the user, not independent human
assessment. Preserve ambiguous judgments. Conservatively group known follow-up
families for training exclusion, check conflicting membership and candidate
chronology. No training corpus exists; future/external training is unverified.

Use unchanged keyword rules (K), fixed legacy RAG (F) and bounded agent (A),
shared evidence preflight and existing field scoring across fifty cases.
Retain all 150 case/workflow rows, including flags and fallback/partial reports.
Changed or unavailable openings, commits or required pinned evidence are flagged
before inference and remain unscored in every arm. No truncation, replacement,
outcome tuning, prompt/retrieval/scorer changes, drafting, fine-tuning, hosted
reference or model search. Older #16/#17/#18 modes keep their archived catalogs.

One real inference pass: at most **250 charged dispatches**, F <=50 and <=1 per
case, A <=200 and <=4 per case, K zero. Charge before dispatch and preserve the
durable ledger and bounded raw responses. No inference retries, repairs,
warm-ups or second pass. Read-only evidence acquisition may retry transport
failures. Use `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, context 16384, temperature 0, seed 42, top-k 20, top-p 0.8,
repeat penalty 1, 256 output tokens, 20-second timeout and 65536 response bytes.
Verify serving identity/settings before dispatch and capture final residency.
Commit and freeze application source, protocol and confirmed catalog before
inference. Controlled replay and deterministic tests are not quality evidence.

Publish field scores with denominators, partial reports/errors, tokens, latency,
sampled GPU memory and marginal API cost with unmeasured costs explicit.
Compare archived #18 forty-case scores with rerun originals and show new ten
separately, including per-case status, score and candidate-pool changes.
Do not attribute aggregate changes to model improvement: this is a selected,
previously exposed development benchmark and one sequential laptop run.

Generate a fresh blinded report-review sheet and separate identity key without
transferring prior ratings. Reply usefulness and semantic citation support remain
unverified without fresh explicit review, separately from expected-outcome
confirmation. Keep the selected 3B model and fixed legacy demo default.
