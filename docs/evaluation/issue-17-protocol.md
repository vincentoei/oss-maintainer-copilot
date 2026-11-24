# Issue #17 thirty-case expansion protocol

Scope: issue #17 only, starting from main
`1bec247b9e13d18a265610c99f0778ef13f176bf`. Preserve all twenty existing case
files and prior evaluation artifacts against `issue-17/baseline.json`.
Add ten unedited historical pytest openings with REST/GraphQL agreement,
pre-opening commits, pinned templates and explicit review provenance. The user
explicitly delegated case review to Codex and accepted its confirmation. Record
this attribution; it is not an independent human assessment.

Keep duplicate, nonduplicate, missing-detail and ambiguous coverage. Group
confirmed duplicates and conservatively grouped uncertain family members in the
evaluation partition. Publish a family manifest and check that no recorded
member is assigned to different families/partitions. No training corpus exists
in this repository yet; an empty training partition is not proof about future
or external training data. The manifest is the exclusion list for future work.

Rerun keyword rules (K), fixed legacy RAG (F), and bounded agent (A) on the same
thirty-case catalog. Use the existing replay, cutoff checks, shared evidence
preflight and scorer. Keep all ninety rows, including flags and failures. No
replacement cases, dropped errors, outcome tuning, retrieval/prompt changes,
drafting, fine-tuning, hosted reference or model search. Preserve full openings;
comments, later labels, closures and annotation rationales never enter input.
Uncertain relationships remain unscored by the existing exact metric.

One real inference pass: at most **150 charged dispatches**, F <=30 and <=1 per
case; A <=120 and <=4 per case; K zero. Charge before dispatch and retain a durable
ledger plus bounded raw responses. No warm-ups, retries, repair or second pass.
Use selected `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, context 16384, temperature 0, seed 42, top-k 20, top-p 0.8,
repeat penalty 1, 256 output tokens, 20-second timeout, 65536 response-byte bound.
Verify serving identity/settings before inference and capture final residency.
Freeze application source and catalog hashes in results before dispatch.

Report aggregate fields, eligible denominators, partial reports/errors, tokens,
latency and sampled device GPU memory. Compare the original twenty with #16,
and show changed cases, exact scores, candidate-pool changes and new ten-case
metrics separately. Added earlier candidates can change old cases; disclose
that effect. Code changes merged since #16 and nondeterministic serving also
limit causal attribution. Do not present a 20-to-30 aggregate difference as a
paired model improvement. Preserve prior results instead of overwriting them.

Fresh reply usefulness and semantic citation support require separate explicit
review; do not inherit old ratings or infer them from case confirmation.
Generate a fresh review sheet. This expansion does not promote the agent or
change the demo workflow: retain the selected 3B and fixed legacy default.
