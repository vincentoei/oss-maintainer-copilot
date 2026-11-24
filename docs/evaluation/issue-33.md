# Issue #33 acceptance evidence

Implemented on `feat/33-repository-registry` from updated main
`422876ddae78d1638b6f1980fec5a28f42932355`, scoped to
[issue #33](https://github.com/vincentoei/oss-maintainer-copilot/issues/33).
The fixed legacy selection-only path and selected Qwen2.5-Coder 3B remain the
default. Optional agent/drafting are not promoted. There is no model search,
new benchmark catalog, spending or new human quality judgment.

## Acceptance matrix

| Acceptance criterion | Evidence and limitations |
| --- | --- |
| Register/persist multiple repositories | `tests/test_repositories_api.py` exercises HTTP registration, idempotence, restart with a new Python registry, stable/canonical identity, removal, invalid/private/inaccessible entries and concurrent first registration. Real [HTTP pytest registration](issue-33/http-registration.json), [browser Ruff registration](issue-33/browser-registration.json), and identical pre/post-restart registrations in [HTTP evidence](issue-33/http-reports.json). SQLite transactions persist configuration/snapshots. Removal touches only local registry rows. |
| Explicit target selection/default compatibility | Public regressions cover selected Python/fixed/agent/source interfaces, seeded pytest default, unknown/removed selection and removal of the default across restart. Real browser reports show the active selector and report identity for both projects; real HTTP rejects Ruff's removed ID with 422. Source inspection carries its selected registration. |
| Bounded inspectable context | Prepared Ruff revision `32669b2743b45fb364aa4741b82e98443155ca3c`, three YAML forms, actual required/optional fields, labels, documentation references and explicit omissions are retained in browser registration. Generic Markdown requirements are tested through configuration/refresh; unsupported dropdowns, missing context, failed refresh, disabled issues and in-flight refresh have deterministic checks. [Limits and supported formats](../repositories.md): 12 fetches, 256 KiB each, five seconds, four preparations per process, four templates, three docs, twenty supported fields, 2,000-character passages. Ruff correctly reports limited context. |
| Generic profile without per-repository code | Ruff is registered by the ordinary browser form; it has no Python profile. Additional fixture identities `acme/widget` and `other/tool` use the same public interfaces. Pytest policy stays in the adapter; shared requests/reports/rendering consume `RepositoryContext`. Generic required-field checks only use declared requirements of an applicable form/configured Markdown template. Missing/unestablished requirements and unsupported labels abstain. Interface additions are documented. |
| Isolate all repository evidence | Fixed/agent regressions reject foreign issue evidence, mismatched source selection, foreign report citations and model-authored references. Reused issue numbers are tested across three identities and concurrent reports; cache identities include repository-bearing records/URLs. Cross-repository PR links do not authorize CI reads. Snapshot refresh cannot alter in-flight citations/traces. Existing read-only limits, untrusted-input and partial-report checks are retained. Generic lexical matches remain related, not asserted duplicates. |
| Public-interface deterministic verification | Repository registration and triage tests use existing HTTP/web/Python seams with external network/model replacements. Cover persistence/removal/default errors, refresh/failure, supplied vs absent required details, optional fields, supported citations, unsupported conventions, repository mismatch, repeated numbers, concurrency, exact vs subset form applicability, comments and duplicate headings. Existing pytest regressions remain required. Fixture shape differs from Ruff's actual forms; the real forms are independently recorded and exercised in the integrated smoke. |
| Preserve baseline and history | [Integrity record](issue-33/integrity.json): all 161 pre-existing evaluation/case files are byte-identical to starting main. The original #16 verifier passes against an extracted original commit: 150 baseline artifacts, 17 frozen source files, 60 reports/score recomputations, 79 dispatches. No prior reports, fingerprints, raw outputs or human judgments were rewritten. Historical replay still checks opening identity/hashes/timestamps and pre-cutoff commits; tests cover removing live pytest and rejecting foreign matching-hash openings. Its pinned profile bypasses live registry state. ADRs 0001/0003 remain unchanged. |
| Integrated flow and limits | Real Chromium adds Ruff, shows readiness and selection, and generates one report per repository after actual process restart, with no JavaScript errors. [Browser reports/traces](issue-33/browser-reports.json), [HTTP reports/traces](issue-33/http-reports.json), [screenshots](issue-33/browser-ruff.png), successful source inspection, explicit refresh/removal and failed-read partial report are preserved. [Protocol](issue-33-protocol.md) declares 12 dispatches; [ledger](issue-33/requests.jsonl) records **6**, including one agent action and five final selections. Zero transport failures/retries/warmups; settings stayed fixed. [Serving identity](issue-33/serving.json) matches selected digest/quantization/16K parameters. No usefulness/generalization claim follows. |
| Document reusable behavior/scope | [Setup/API/storage/refresh/formats/limits](../repositories.md), README, project brief and root glossary now describe multiple registrations and one target per report. [ADR-0004](../adr/0004-repository-context-snapshots.md) records snapshot isolation and separation from historical replay. Original pytest-first release/evaluation decisions remain explicit. |

## Live results and provenance

Five reports were produced with the real selected local model: two through the
browser, two fixed HTTP reports and one optional agent HTTP report. Pytest selects
`type: bug` in both runs. Ruff abstains on issue type in all three reports. The
fixed Ruff HTTP report requests the required blank Summary, leaves optional
Version alone, and retains an explicit source-read abstention and partial status
for `does-not-exist-issue33.rs`. Other smoke reports complete structurally.
These are synthetic openings written for this capability check, not benchmark
cases or copied contributor openings.

The browser smoke precedes a deterministic hardening change: comments and repeated
headings now abstain rather than establishing missing requirements. Its exact
application source is reconstructible by applying
[browser-source.patch](issue-33/browser-source.patch) to the starting commit;
[browser hashes](issue-33/browser-source-hashes.json) were verified after applying
it in a separate directory. The HTTP smoke uses the comments/repeated-heading hardening change;
apply [HTTP source delta](issue-33/http-source-delta.patch) next to reproduce its
[executed source hashes](issue-33/http-source-hashes.json). Subsequent review strengthened standalone source validation, unified quote checks,
excluded code examples from template headings, disclosed excess Markdown fields
and restored the Python abstention flag. Those corrections have deterministic
regressions; the preserved inference reports retain the source hashes of their
actual runs. No prompt tuning followed model outputs. Raw responses are `response-1.json` through
`response-6.json`, with dispatch hashes and transport timing. The local registry
file stays out of Git; snapshots needed for inspection are retained as JSON.

Fresh usefulness, relationship correctness, abstention quality and semantic
citation-support judgments remain **unverified: no explicit human review was
requested or supplied**. Registration and literal passage checks cannot prove
these properties. No generalization or usefulness gain is claimed. Live search
against real existing issue openings and conditional live CI on the second
repository were not exercised by this small smoke; deterministic public-interface
checks establish their repository/argument isolation, not live retrieval quality.
Ordinary opt-in historical network tests are reported separately from deterministic
successes. There is no full-repository index, private-repository support, continuous
sync or multi-user authorization in this milestone.

## Required checks

The initial full suite passed **324 tests**, with two existing opt-in live
historical tests skipped. Subsequent review added regressions for the actual
GitHub adapter transport, standalone foreign source evidence, template limits,
fenced examples and the explicit Python abstention flag. Final check totals and
review disposition follow below.


The [two-axis review](issue-33-code-review.md) found and corrected three Spec
defects and the duplicated support-validation algorithm. Re-review found zero
remaining actionable Spec defects and zero documented-standard breaches; one
profile-dispatch design heuristic remains non-blocking with its scope rationale.

Final checks after all review fixes: **332 passed, 2 skipped** (existing opt-in
network replay checks, not successes); Ruff lint/format, strict mypy and
`git diff --check` pass. [Machine-readable final checks](issue-33/checks.json).
All 161 original evaluation/case files remain unchanged; the live ledger still
contains exactly six dispatches and six preserved raw responses. No additional
inference was used for review or corrections.
