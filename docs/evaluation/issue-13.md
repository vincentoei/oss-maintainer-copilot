# Issue #13: ten-case evaluation results

The existing evaluator completed both methods on all ten confirmed cases with
zero replay errors. No local model was selected or called. Expected outcomes
record user acceptance of the assistant judgments, not independent inspection.
See [the review and ambiguities](cases-six-through-ten.md),
[provenance checks](issue-13-provenance.json), and
[full per-case scores and generated drafts](issue-13-results.json).

## Aggregate comparison

Columns compare the published [issue #12 run](issue-12-results.json) (five cases)
with this run (ten). Duplicate accuracy excludes the one uncertain expected
relationship (four versus nine scored judgments); other field rates use five
versus ten cases. Precision and recall are case macro means.

| Metric | Controlled: 5 | Controlled: 10 | Keyword: 5 | Keyword: 10 |
| --- | ---: | ---: | ---: | ---: |
| completed | 5 | 10 | 5 | 10 |
| mean candidate pool size | 1.0 | 1.0 | 6.0 | 10.9 |
| duplicate retrieval recall | 1.0 | 1.0 | 0.6 | 0.8 |
| duplicate judgment accuracy | 0.5 | 0.556 | 0.25 | 0.444 |
| issue type accuracy | 0.0 | 0.0 | 0.2 | 0.3 |
| missing details exact | 0.8 | 0.4 | 0.8 | 0.4 |
| missing details precision | 1.0 | 0.75 | 1.0 | 0.75 |
| missing details recall | 0.8 | 0.7 | 0.8 | 0.7 |
| citation validity rate | 1.0 | 1.0 | 1.0 | 1.0 |
| issue type abstention appropriateness | 0.0 | 0.0 | 0.8 | 0.9 |
| duplicate abstention appropriateness | 0.8 | 0.9 | 0.8 | 0.9 |
| mean latency ms | 1737.04 | 1564.92 | 4348.95 | 6651.34 |

Controlled is a fixed-response smoke comparator that abstains on issue type;
keyword_rule uses the existing lexical retrieval, template-detail checks and
type cues. Neither is an LLM quality reference. Zero paid model calls; public
GitHub reads have no per-request fee assumed. CPU, hosting and network cost are
excluded. Latency includes repeated public network reads and is not a model
benchmark. All model quality measurements remain provisional; model selection
and llmfit stay in #21 after #15 and before #16.

## Field results for all ten cases

Each row reports whether the known earlier issue surfaced; whether its
duplicate/nonduplicate judgment matched; whether type and missing details
matched; and whether deterministic citation-boundary checks passed. A dash
marks the uncertain relationship excluded from duplicate accuracy. Human
semantic citation validity and draft usefulness are pending for this run.

| Case | Method | Retrieved | Relationship correct | Type correct | Details exact | Citation boundary valid |
| --- | --- | --- | --- | --- | --- | --- |
| 7312 | controlled | yes | no | no | yes | yes |
| 10156 | controlled | yes | yes | no | yes | yes |
| 12053 | controlled | yes | yes | no | no | yes |
| 12072 | controlled | yes | no | no | no | yes |
| 12079 | controlled | yes | no | no | no | yes |
| 12081 | controlled | yes | no | no | yes | yes |
| 12083 | controlled | yes | — | no | no | yes |
| 12116 | controlled | yes | yes | no | no | yes |
| 12146 | controlled | yes | yes | no | yes | yes |
| 12189 | controlled | yes | yes | no | no | yes |
| 7312 | keyword_rule | yes | no | yes | yes | yes |
| 10156 | keyword_rule | yes | yes | no | yes | yes |
| 12053 | keyword_rule | yes | yes | no | no | yes |
| 12072 | keyword_rule | yes | no | yes | no | yes |
| 12079 | keyword_rule | yes | no | yes | no | yes |
| 12081 | keyword_rule | yes | no | no | yes | yes |
| 12083 | keyword_rule | no | — | no | no | yes |
| 12116 | keyword_rule | yes | yes | no | no | yes |
| 12146 | keyword_rule | no | no | no | yes | yes |
| 12189 | keyword_rule | yes | yes | no | no | yes |

## Changed first-five fields

Adding cases also expands keyword retrieval for the original cases: all
distinct hash-verified openings in the catalog before each cutoff are eligible.
Controlled still supplies one chosen earlier issue per case. Compare the same
original cases below to distinguish pool changes from the larger denominator.
Other retrieved issues have no reviewed pair label and are explicitly listed
as unreviewed in the JSON; this is not full-history retrieval recall.

- #7312 controlled: no change in these fields.
- #10156 controlled: no change in these fields.
- #12081 controlled: no change in these fields.
- #12083 controlled: no change in these fields.
- #12146 controlled: no change in these fields.
- #7312 keyword_rule: no change in these fields.
- #10156 keyword_rule: no change in these fields.
- #12081 keyword_rule: no change in these fields.
- #12083 keyword_rule: no change in these fields.
- #12146 keyword_rule: no change in these fields.

## New failures and practical limits

- #12053 controlled: type `None` (expected `type: enhancement`); details `['alternative solutions', 'real-world use case']` (expected `[]`); earlier issue classified as `related_issue`.
- #12072 controlled: type `None` (expected `type: bug`); details `[]` (expected `['minimal example', 'pip list output', 'pytest and OS versions']`); earlier issue classified as `related_issue`.
- #12079 controlled: type `None` (expected `type: enhancement`); details `['alternative solutions', 'real-world use case']` (expected `['alternative solutions']`); earlier issue classified as `related_issue`.
- #12116 controlled: type `None` (expected `type: bug`); details `['pip list output']` (expected `[]`); earlier issue classified as `related_issue`.
- #12189 controlled: type `None` (expected `type: question`); details `[]` (expected `['pytest and OS versions']`); earlier issue classified as `related_issue`.
- #12053 keyword_rule: type `type: question` (expected `type: enhancement`); details `['alternative solutions', 'real-world use case']` (expected `[]`); earlier issue classified as `related_issue`.
- #12072 keyword_rule: type `type: bug` (expected `type: bug`); details `[]` (expected `['minimal example', 'pip list output', 'pytest and OS versions']`); earlier issue classified as `related_issue`.
- #12079 keyword_rule: type `type: enhancement` (expected `type: enhancement`); details `['alternative solutions', 'real-world use case']` (expected `['alternative solutions']`); earlier issue classified as `related_issue`.
- #12116 keyword_rule: type `type: enhancement` (expected `type: bug`); details `['pip list output']` (expected `[]`); earlier issue classified as `related_issue`.
- #12189 keyword_rule: type `type: enhancement` (expected `type: question`); details `[]` (expected `['pytest and OS versions']`); earlier issue classified as `related_issue`.

Both methods put the two new duplicate candidates under related issues.
The template rules over-request alternatives for #12053 despite the opening
describing its current CLI workaround; fail to recognize #12079’s use case;
and miss absent details on #12072 and #12189. #12116’s package-list heading
also exposes a heuristic recognition failure. These are recorded results,
not fixes to the triage implementation in this issue.

Expected outcomes are confirmed, but no generated draft or semantic citation
judgment is marked reviewed. Even unchanged original controlled drafts retain
pending status in this fresh artifact; prior human assessments remain in the
issue #12 artifact. A valid citation URL and cutoff do not establish semantic
support. Historical CI and full-history search remain unverified because this
replay supplies pinned templates and a limited catalog of earlier openings.

## Reproduce and acceptance evidence

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > /tmp/evaluation-new-results.json
uv run --locked --no-env-file pytest -q
uv run --locked --no-env-file mypy
uv run --locked --no-env-file ruff check .
uv run --locked --no-env-file ruff format --check .
```

- Five new cases: metadata JSON records hashes, unedited openings, cutoff-safe
  commits and earlier issues, and human acceptance; provenance records checked
  template lines and complete controlled replay. The scorer retains its human
  confirmation guard.
- Additional coverage and ambiguity: the five new families and their explicit
  alternative judgments are documented in the case review. The original
  uncertain relationship remains an expected abstention.
- All-ten evaluation and changes: both methods completed 10/10 without errors;
  this comparison and the full JSON publish aggregates, field-level results,
  generated drafts, citation lists, failures, latency and cost assumptions.
- Automated validation: 155 tests passed, 2 live tests skipped; live controlled
  replay and scoring separately exercised all ten against public GitHub.
  Typechecking, lint and formatting passed.
