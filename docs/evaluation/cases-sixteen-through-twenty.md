# Evaluation cases 16 through 20: issue #15

Five additional unedited pytest openings bring the catalog to twenty distinct
issue families. The requesting user explicitly chose “Delegate review to Codex
and accept its confirmation.” Codex reviewed the openings and paired earlier
issues, then confirmed all five proposed outcomes without changes. Metadata
records the confirmation time and attribution. This is assistant review accepted
by the user, not an independent human assessment. The scoring guard is unchanged.

| Case | Earlier issue | Relationship | Type | Missing report details |
| --- | --- | --- | --- | --- |
| [12219](https://github.com/pytest-dev/pytest/issues/12219) | [4064](https://github.com/pytest-dev/pytest/issues/4064) | Nonduplicate | `type: bug` | `pip list output`, `pytest and OS versions`, `minimal example` |
| [12223](https://github.com/pytest-dev/pytest/issues/12223) | [12204](https://github.com/pytest-dev/pytest/issues/12204) | Nonduplicate | `type: bug` | `pip list output`, `pytest and OS versions` |
| [12224](https://github.com/pytest-dev/pytest/issues/12224) | [10156](https://github.com/pytest-dev/pytest/issues/10156) | Nonduplicate | `type: enhancement` | None |
| [12226](https://github.com/pytest-dev/pytest/issues/12226) | [12197](https://github.com/pytest-dev/pytest/issues/12197) | Nonduplicate | `type: enhancement` | `alternative solutions` |
| [12228](https://github.com/pytest-dev/pytest/issues/12228) | [12197](https://github.com/pytest-dev/pytest/issues/12197) | Nonduplicate | `type: docs` | `alternative solutions` |

## Reviewed rationale and ambiguities

- **12219 / 4064:** A runtime setup/teardown failure in a ported suite differs
  from correcting documentation that claimed the hooks were unsupported.
  The opening includes pytest 8.1.1 and Darwin, but no OS release or package
  list. Its small example succeeds; a minimal example reproducing the failing
  behavior is still needed. The external ported suite is context, not a fetched
  replay artifact. Bug is accepted for the reported runtime failure.
- **12223 / 12204:** Oversized JUnit XML message attributes differ from traceback
  growth caused by repeated fixture exceptions. The two-line assertion example
  reproduces the large diff. pytest 8.1.1 is stated; package list and OS version
  are missing. Bug is accepted because downstream parsers truncate or crash;
  enhancement or question would also be defensible for the desired output limit.
- **12224 / 10156:** Explicit collection/session/test lifecycle APIs differ from
  documenting dynamic fixture registration. Problem, proposed API, Pyodide use
  case, and the workaround of restarting Pyodide per file are all present.
- **12226 / 12197:** Quote-free marker negation differs from availability of
  log-disable as an ini option. Bash/CI examples and proposed syntax supply the
  use case and solution. The alternatives section is empty. Showing the existing
  quoted form describes the problem; it does not state an alternative tried or
  that no workaround exists. Missing alternatives is accepted.
- **12228 / 12197:** Documenting TOML value shapes differs from adding or explaining
  an ini option. The addopts examples and proposed documentation provide a problem,
  solution and use case. Searching other projects investigates valid shapes;
  it does not resolve the documentation gap or state an alternative tried.
  Missing alternatives is accepted. The feature template applies despite the
  documentation type; no bug-only package/version requirements are imposed.

These are five different issue families, including two distinct configuration
requests paired with the same topical negative. Earlier confirmed cases retain
duplicate, nonduplicate and uncertain relationships, plus missing-detail coverage.

## Provenance and evidence boundary

[Provenance](issue-15-provenance.json) records all nine distinct issue openings:
REST/GraphQL title, body and creation-time agreement; `lastEditedAt: null`; and
SHA-256 of UTF-8 `title + NUL + body`, without normalization. Each case preserves
its public ID, cutoff, full pre-cutoff commit SHA, committer timestamp, expected
outcome, and content hashes. The latest commit returned before each opening was
independently checked against the Git commit endpoint. Bug and feature templates
were fetched at every pinned commit; their file hashes and lines are recorded.
Full contributor issue bodies remain on GitHub under ADR 0003.

Both #12269 and #12270 were rejected during selection: each was edited after
opening and no verified original was acquired. They are not benchmark cases.
Every selected earlier issue predates its case cutoff. Comments, labels,
closures, later duplicate decisions and external linked projects are excluded
from replay input. No new source/documentation fixtures were added. Historical
CI remains unavailable. Confirmation of expected outcomes does not confirm
semantic citation support or generated reply usefulness.

No local model was selected or called. Model selection and llmfit remain #21,
after #15 and before #16. Earlier model-quality measurements are provisional.
See [the twenty-case benchmark](issue-15.md) for acceptance evidence and results.
