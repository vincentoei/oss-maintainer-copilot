# Evaluation cases 11 through 15: issue #14

Five additional pytest openings extend the catalog to fifteen distinct issue
families. All five are confirmed difficult topical negatives.
On 2026-11-18T04:47:35.478798+00:00,
Codex reviewed the five openings and their paired earlier issues and confirmed
all proposed relationships, issue types, and missing details without changes.

The requesting user explicitly delegated this review to Codex and stated,
"I'll treat your confirmation as my confirmation." The case records therefore
record confirmation accepted by the requesting user through that delegation.
This was assistant-performed review, not an independent human assessment.
Later maintainer comments corroborate context but are not the acceptance source.
The scorer's confirmation guard remains unchanged.

| Case | Earlier issue | Confirmed relationship | Type | Missing report details |
| --- | --- | --- | --- | --- |
| [12197](https://github.com/pytest-dev/pytest/issues/12197) | [12053](https://github.com/pytest-dev/pytest/issues/12053) | Nonduplicate | `type: question` | `pip list output`, `pytest and OS versions`, `minimal example` |
| [12201](https://github.com/pytest-dev/pytest/issues/12201) | [12146](https://github.com/pytest-dev/pytest/issues/12146) | Nonduplicate | `type: enhancement` | None |
| [12203](https://github.com/pytest-dev/pytest/issues/12203) | [12116](https://github.com/pytest-dev/pytest/issues/12116) | Nonduplicate | `type: bug` | `minimal example` |
| [12204](https://github.com/pytest-dev/pytest/issues/12204) | [12203](https://github.com/pytest-dev/pytest/issues/12203) | Nonduplicate | `type: bug` | None |
| [12216](https://github.com/pytest-dev/pytest/issues/12216) | [12146](https://github.com/pytest-dev/pytest/issues/12146) | Nonduplicate | `type: bug` | `pip list output`, `pytest and OS versions` |

## Confirmed rationale and resolved ambiguities

- **12197 / 12053:** Both compare command-line options with ini configuration,
  but log filtering and debugger selection are different requested behaviors.
  Question is preferred because the opening asks about an assumed configuration
  option; bug or enhancement would also be defensible descriptions of the desired
  parity. The pytest version is present; only the OS part of the combined version
  field is missing. There is no package list or standalone ini/test/command
  reproduction. This review accepts the missing-minimal-example judgment: the
  option description alone omits the exact configuration and logging test.
- **12201 / 12146:** Both concern parametrization, but platform-dependent parameter
  selection differs from a class fixture running too often for rebuilt tuples.
  The feature request supplies its Windows/POSIX path use case and describes
  skipif plus copied tests as an alternative despite the empty alternatives
  section. No additional feature-template detail is missing.
- **12203 / 12116:** Both lose log records, but the new report concerns fixture
  setup exceptions; the earlier report concerns records emitted in child
  processes. The opening does not establish that these have the same cause.
  The package list and Fedora 39/pytest 8.1.1 versions are present. Its sketch
  depends on undefined Launcher/get_ctr_log helpers, so a standalone minimal
  example remains missing. The linked plugin is context, not an additional
  fetched replay artifact.
- **12204 / 12203:** Both involve fixtures raising exceptions, but growing
  tracebacks across tests differ from lost log records. A package list, macOS
  version, and runnable example are present. The prose/package list states
  pytest 8.1.1 while the pasted run states 8.0.0 (and different pluggy versions).
  Clarifying that inconsistency would be useful, but it does not make the
  version field absent. Expected missing details are therefore empty.
- **12216 / 12146:** Both involve parametrized fixtures, but dynamically adding
  an unrequested fixture fails to invoke it, whereas the earlier fixture runs
  too often. Bug is accepted for the demonstrated runtime failure; enhancement
  or question are defensible because the opening seeks a supported way to do
  dynamic injection. pytest 8.1.1 and a runnable example are present. Package
  list and OS version are absent; only OS is missing from the combined field.

## Provenance and cutoff boundary

[Provenance](issue-14-provenance.json) records REST/GraphQL agreement for all
eight distinct issue openings, GraphQL `lastEditedAt: null`, and SHA-256 of
UTF-8 `title + NUL + body` without normalization. Metadata preserves each opening
cutoff, verification timestamp, full repository commit SHA and committer time.
Commits were selected using the latest commit before each opening and both bug
and feature templates were fetched at each pinned commit. Their requested lines
and file hashes are preserved in the provenance artifact. Contributor bodies
remain on GitHub under ADR 0003; acquisition copies are temporary only.

Every paired issue predates its case cutoff. #12203 is both a new case and an
eligible earlier issue for #12204. Shared vocabulary does not establish an issue
family: the pairwise differences above explain the five distinct new families.
Comments, later edits, labels, closures and later fixes never enter replay.
External linked projects/discussions are not fetched by this replay. Historical
CI remains unavailable. This batch adds pinned templates and verified issue
pairs, not new source/documentation fixtures.

## Annotation-only corroboration

- [12197 maintainer explanation](https://github.com/pytest-dev/pytest/issues/12197#issuecomment-2042519138)
  explains that log-disable is only a CLI option; the reporter later accepts
  addopts. This supports the question interpretation but does not override review.
- [12201 maintainer response](https://github.com/pytest-dev/pytest/issues/12201#issuecomment-2045333955)
  suggests passing a variable to parametrize, consistent with a feature request
  that has a straightforward workaround.
- [12204 maintainer diagnosis](https://github.com/pytest-dev/pytest/issues/12204#issuecomment-2081239376)
  explains repeated raising of a cached exception and notes that the symptom
  also affects ordinary exceptions. That later diagnosis is annotation only.
- No maintainer response was returned in the initial four-comment read for
  #12203 or #12216; opening-time rationale above is the basis for their confirmed outcomes.

## Scope and validation

No local model is selected or called. Model selection and llmfit belong to #21
after #15 and before #16. All earlier model-quality observations are provisional.
Controlled responses establish replay behavior; the keyword baseline measures
existing rules against the limited published catalog, not full-history recall.
Acceptance of expected outcomes is separate from semantic citation and
generated draft usefulness review; those judgments remain pending.

Live controlled replay previously completed all fifteen cases without a flagged
opening or commit. [The evaluation report](issue-14.md) and its
[raw results](issue-14-results.json) track scoring after this confirmation.
