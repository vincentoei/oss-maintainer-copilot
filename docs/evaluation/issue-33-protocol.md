# Issue #33 integrated smoke protocol

Declared before live registration or inference. Base main is
422876ddae78d1638b6f1980fec5a28f42932355. This is a capability/isolation smoke
check, not a benchmark or a quality comparison. No evaluation cases are added.

Use pytest's bundled profile plus `astral-sh/ruff`, selected because its YAML
issue forms and Rust-project documentation differ from pytest's Markdown
bug/feature templates. Register Ruff using the ordinary repository endpoint or
web form; no Ruff Python profile or shared-module edit is permitted.

Maximum **12 inference dispatches total**, counting failed dispatches, action
choices, final selections, retries and browser checks. Charge before dispatch in
an append-only local ledger; retain raw bounded responses, reports, traces and
failures separately from earlier evaluations. No warmups, automatic retries,
model search or tuning. Fixed selection-only legacy remains the default. Agent
smoke, if run, uses the same context and the existing four-call cap. Stop when
the budget is consumed; skipped checks remain unverified.

Use only selected `pytest-triage:coder3b-ctx16k` (Qwen2.5-Coder 3B Instruct,
Q4_K_M), temperature 0, existing seed 42/top-k 20/top-p 0.8/repeat penalty 1,
16384 context. Capture serving identity/settings before dispatch; reject a
mismatched alias rather than substituting another model. Final selection stays
256 tokens, 20-second timeout, 65536 response bytes; agent actions 256 tokens.
Keep all settings fixed across repositories/interfaces. Capture environment and
source hashes separately. No paid inference or spending is authorized here.

Through actual localhost HTTP: register, inspect prepared context, restart the
server using the same local SQLite file, list/select both repositories, and
create fixed reports. Through the existing browser: add/select the second
repository, create a report for each target, inspect the active identity,
report, citations, readiness and trace. Demonstrate limited context or a failed
source read. Include source inspection with registration identity and explicit
refresh/removal if feasible. Use synthetic user-authored issue openings rather
than bulk republishing contributor issue bodies (ADR-0003).

Verify repository identities and revisions in reports/traces/citations, bounded
model calls, rendering and error visibility. Successful registration, syntactic
citations or transport do not prove relevance, semantic support, usefulness or
generalization. All new report usefulness/semantic judgments remain **pending
explicit human review**. Preserve failures and disclose missing environment
capabilities precisely; do not label a skipped live check a success.
