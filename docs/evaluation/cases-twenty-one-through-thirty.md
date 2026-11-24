# Evaluation cases 21 through 30: issue #17

The requesting user explicitly chose “Delegate case review to Codex and accept its confirmation.” Codex reviewed the openings, paired earlier openings and relevant annotation-only maintainer discussion. All ten expected outcomes below are confirmed on that delegated basis. This is assistant review accepted by the user, not an independent human assessment. Case confirmation does not rate generated replies.

| Case | Earlier issue | Relationship | Type | Missing report details |
| --- | --- | --- | --- | --- |
| [12231](https://github.com/pytest-dev/pytest/issues/12231) | [12223](https://github.com/pytest-dev/pytest/issues/12223) | nonduplicate | type: enhancement | None |
| [12242](https://github.com/pytest-dev/pytest/issues/12242) | [12219](https://github.com/pytest-dev/pytest/issues/12219) | nonduplicate | type: question | pytest and OS versions, minimal example |
| [12249](https://github.com/pytest-dev/pytest/issues/12249) | [12197](https://github.com/pytest-dev/pytest/issues/12197) | nonduplicate | type: bug | pip list output, pytest and OS versions, minimal example |
| [12255](https://github.com/pytest-dev/pytest/issues/12255) | [12204](https://github.com/pytest-dev/pytest/issues/12204) | nonduplicate | type: enhancement | alternative solutions |
| [12263](https://github.com/pytest-dev/pytest/issues/12263) | [12219](https://github.com/pytest-dev/pytest/issues/12219) | nonduplicate | type: regression | pip list output, pytest and OS versions, minimal example |
| [12273](https://github.com/pytest-dev/pytest/issues/12273) | [12263](https://github.com/pytest-dev/pytest/issues/12263) | duplicate_candidate | type: regression | pip list output, pytest and OS versions, minimal example |
| [12278](https://github.com/pytest-dev/pytest/issues/12278) | [12263](https://github.com/pytest-dev/pytest/issues/12263) | uncertain | unknown | pip list output, pytest and OS versions, minimal example |
| [12281](https://github.com/pytest-dev/pytest/issues/12281) | [12226](https://github.com/pytest-dev/pytest/issues/12226) | nonduplicate | type: enhancement | None |
| [12287](https://github.com/pytest-dev/pytest/issues/12287) | [478](https://github.com/pytest-dev/pytest/issues/478) | nonduplicate | type: question | None |
| [12290](https://github.com/pytest-dev/pytest/issues/12290) | [12228](https://github.com/pytest-dev/pytest/issues/12228) | nonduplicate | type: enhancement | alternative solutions |

## Review rationale

- **12231 / 12223:** Separating XFAIL summary from tracebacks is different from limiting JUnit XML failure attributes. The opening states the problem, proposed control, pandas use case and the rejected workaround of dropping -rx.
- **12242 / 12219:** Custom --env option discovery is different from unittest module setup hooks. Package graph and pytest version are supplied. Windows paths do not establish an OS version. The snippet omits its file location and tree, needed for a reproducing example; checked boxes alone are not evidence. Maintainer clarification later confirms a conftest location question, used for annotation only.
- **12249 / 12197:** Warnings escaping filtering during early imports differ from log_disable not being supported in ini. The opening reports pytest 8.1.1 on Linux without an OS release or complete package list; the warning output and invocation do not include an isolated module reproducer. Bug is accepted for failure to control warnings; enhancement would also be defensible.
- **12255 / 12204:** Formatting a single ExceptionGroup nicely differs from cached session-fixture traceback growth across successive tests. Two runnable examples give the problem, solution and use case. No alternative approach is stated. Enhancement is accepted for new formatting parity; bug is also defensible. Bug-only environment details are not imposed on this request.
- **12263 / 12219:** Tornado collection fails when constructing a TestCase without runTest; omitted module setup hooks are different. The opening contrasts working 8.1.0 with the title 8.2.0. It has a traceback but no package list, OS release or runnable class reproducer.
- **12273 / 12263:** Both openings show the same pytest unittest collector constructing a subclass with runTest and raising AttributeError because that method does not exist. The maintainer explicitly links 12263 and describes an analogous downstream fix. Different downstream libraries do not change the shared pytest construction failure. No complete environment or runnable isolated class is given.
- **12278 / 12263:** The opening attributes six child processes and resource races to pytest 8.2.0 without code, package list or OS version. Collection-time construction could be relevant, but the opening does not establish the same failure as missing runTest. Do not force a core bug or regression label. Maintainer requests more context. Conservatively exclude this possible family member from training with 12263/12273, without calling it a confirmed duplicate.
- **12281 / 12226:** Matching marker keyword values differs from quote-free negation syntax. Concrete device examples, the desired syntax and nose/plugin alternatives cover the applicable feature details.
- **12287 / 478:** Doctest-induced sys.path insertion and import conflicts differ from --pyargs resolving separate namespace eggs. The opening asks whether the observed behavior is expected and supplies layout, example, package list, pytest version and macOS release. Question is accepted; bug remains a plausible interpretation of the conflict.
- **12290 / 12228:** A docs website dark theme differs from explaining TOML option shapes. Evening readability supplies the use case and a toggle supplies the proposed solution, but no alternative is stated. This is a website feature request, not a missing prose explanation.

## Provenance and partition boundary

[Provenance](issue-17/provenance.json) records REST/GraphQL agreement and unedited status for all seventeen distinct openings, exact content hashes, ten independently checked pre-cutoff commits, and both pinned templates per revision. Full issue bodies remain on GitHub under ADR-0003. The older #478 opening is a migrated Bitbucket report; GitHub records no edit and its recorded import predates the case cutoff. No original pre-migration timestamp is claimed.

[Partition manifest](issue-17/partitions.json) assigns all thirty cases to evaluation, including confirmed duplicate members and conservative uncertain groups. There are **28 families**, not thirty independent families: #12263/#12273 share the runTest failure and #12278 remains conservatively grouped with them. Earlier unrelated evidence is not automatically a family member. All earlier openings may be retrieved when they precede the current cutoff. No training corpus exists in the repository yet; future training must exclude these families, including the recorded earlier members. External/future training partition integrity remains unverified.

Comments, later labels, closure decisions, external projects and the human annotation rationale are excluded from replay input. The earlier #12263 is legitimate retrieval evidence for #12273/#12278 because it predates their cutoffs. Historical CI remains unavailable. The original twenty cases retain duplicate/nonduplicate/ambiguous coverage, and these additions add another duplicate, another ambiguous relationship, unknown type, complete reports and missing details.

[Issue #17 results and acceptance evidence](issue-17.md) record the actual workflow rerun and changed scores.
