# Issue #18 forty-case expansion protocol

Scope: issue #18 only, from updated main
`48e3273ee109e9a7ff6c6b1c55a4c6882e7d4183`. Preserve the thirty existing
cases and all prior evaluation artifacts against `issue-18/baseline.json`.
Add ten historical pytest openings from May 7–15, 2024. Verify identical
REST/GraphQL opening content, no edits, exact title/body hashes, independently
checked pre-opening repository commits and both pinned templates. Publish only
metadata and provenance under ADR-0003. Later discussion is annotation only.

The requesting user explicitly delegated case review to Codex and accepted its
confirmation before comparison. Record this attribution in the case review;
this is assistant review accepted by the user, not independent human assessment.
Preserve ambiguity and group possible duplicate/follow-up families conservatively
for exclusion from future training. Check every recorded family member for
conflicting assignment and every candidate against its case cutoff. No training
corpus currently exists; external/future training integrity remains unverified.

Use unchanged keyword rules (K), fixed legacy RAG (F) and bounded agent (A),
shared replay preflight and existing field scorer on the same forty-case catalog.
Retain all 120 rows, including failures and exclusions. Preserve full openings;
no truncation, replacement cases, outcome tuning, retrieval/prompt changes,
drafting, fine-tuning, hosted reference or model search. Older #16/#17 modes
retain their archived catalogs. The #17 comparison remains as recorded before
its oversized-opening follow-up; successful replay of #12204 now changes its
eligibility and must be disclosed in comparisons with that archive.

One real inference pass: at most **200 charged dispatches**, F <=40 and <=1 per
case, A <=160 and <=4 per case, K zero. Charge before dispatch and retain the
durable ledger and bounded raw responses. No inference retries, repair, warm-up
or second pass. Read-only evidence acquisition may retry transport failures.
Use `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, context 16384, temperature 0, seed 42, top-k 20, top-p 0.8,
repeat penalty 1, 256 output tokens, 20-second timeout, 65536 response bytes.
Verify serving identity/settings before dispatch and capture final residency.
Freeze application source, protocol and catalog hashes before inference.

Report field scores with denominators, partial reports/errors, tokens, latency
and sampled device GPU memory. Compare #17's thirty cases with their rerun,
show per-case score/status/candidate-pool changes and report the ten additions
separately. Candidate additions, changed #12204 eligibility and nondeterministic
serving prevent attributing aggregate differences to model improvement.

Create a fresh report-review sheet without transferring previous ratings.
Semantic citation support and reply usefulness remain unverified without fresh
explicit review, separately from confirmation of expected outcomes. Keep the
selected 3B model and fixed legacy demo workflow unchanged.
