# Issue #56 triage-quality follow-up protocol

Scope: requested fixes following #18 / PR #55, based on
`abe7540de2fe0891c2aa00a4cadc67eef51a7b89`, branch `fix/triage-report-quality`.
Preserve all forty case files, expected outcomes and prior evaluation artifacts
against `issue-56/baseline.json` (269 files). Do not modify PR #55's branch.

Fix reproducible report-detail recognition and model label/quote pairing at the
existing approved replay/comparison seams. Do not tune expected outcomes or hide
historical CI abstentions. Keep the selected model, live request limits and
default fixed workflow. This is development-set feedback, not generalization.

Run one new forty-case keyword/fixed-RAG/bounded-agent comparison after freezing
the implementation commit, protocol, catalog and source hashes. Retain all 120
rows, including partial reports, failures and exclusions. Use the same verified
opening text, cutoffs, pinned commits and eligible candidate catalog as #18.
Later labels/comments, annotation rationales and review ratings never enter the
input. Public evidence can be cached after its identity/hash/cutoff verification;
full contributor bodies stay in temporary storage under ADR-0003.

Cap the new pass at **200 charged dispatches**: fixed <=40 and <=1 per case,
agent <=160 and <=4 per case, keyword zero. Persist charges before dispatch and
retain bounded raw responses. No inference warm-ups, retries, repair calls,
second pass or model search. Read-only evidence acquisition may retry failures.
Use `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, context 16384, temperature 0, seed 42, top-k 20, top-p 0.8,
repeat penalty 1, 256 output tokens, 20-second timeout, 65536 response bytes.
Verify serving identity/settings before dispatch and record final residency.

Compare every field and status against archived #18, including per-case gains
and regressions, eligible denominators, citations, abstentions, dispatches,
tokens, latency and sampled device GPU memory. No earlier result is overwritten.
Changed code/prompt/schema and serving nondeterminism limit causal attribution.
An exact-field gain is not proof of useful replies or overall model improvement.

The user requested completion of the report review. Record **Codex** as reviewer,
with the actual method and evidence; this is not independent human assessment or
a blind review. Review every archived report against its verified opening,
pinned cited material and earlier issues, retaining exact report fingerprints.
Use 2 (useful), 1 (partly useful), 0 (not useful), with an explicit reason.
Check citation support, unsupported factual claims or question presuppositions,
supplied-detail redundancy, relationships and abstention separately. A structural
citation pass cannot assign semantic support. Identical report content for the
same opening may be reviewed together with that grouping disclosed.

Review the new reports freshly with separate fingerprints after the run. Do not
transfer old human ratings or case-confirmation judgments into report ratings.
Retain original pending review files and publish sidecars here. Do not promote a
workflow on assistant ratings. Independent human report ratings remain distinct;
external/future training integrity awaits an actual training corpus. The existing
family exclusion manifest is the preparation for that future audit.
