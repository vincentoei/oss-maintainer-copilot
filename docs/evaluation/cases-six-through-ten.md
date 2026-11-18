# Evaluation cases 6 through 10: issue #13

These five additional pytest case records extend the first five with debugger
configuration, plugin API incompatibility, argument-file test selection,
child-process logging, and JUnit output when capture is disabled. Contributor
bodies remain on GitHub, following ADR 0003. No local model is selected.
Model selection and llmfit belong to #21 after #15 and before #16; all earlier
model-quality measurements remain provisional.

## Confirmed outcome review

Review status: **confirmed** on 2026-11-18. The assistant reviewed the public
issue openings and retained all five proposed judgments, including the
ambiguities below. The requesting user explicitly accepted the assistant
decisions as their own outcomes. This records user acceptance, not an
independent human inspection of the openings. Each JSON record now has
`human_review.status: confirmed`; the scorer's pending-annotation guard is unchanged.

For #12072 and #12189, `pytest and OS versions` is the existing combined
scoring field: only the OS version is missing; the pytest version is supplied.
This confirmation covers expected outcomes, not generated reply usefulness or
semantic citation judgments.

| Case | Earlier issue | Relationship | Type | Missing report details |
| --- | --- | --- | --- | --- |
| [12053](https://github.com/pytest-dev/pytest/issues/12053) | [8655](https://github.com/pytest-dev/pytest/issues/8655) | Nonduplicate | `type: enhancement` | None |
| [12072](https://github.com/pytest-dev/pytest/issues/12072) | [12066](https://github.com/pytest-dev/pytest/issues/12066) | Duplicate candidate | `type: bug` | `pip list output`, `pytest and OS versions`, `minimal example` |
| [12079](https://github.com/pytest-dev/pytest/issues/12079) | [11871](https://github.com/pytest-dev/pytest/issues/11871) | Duplicate candidate | `type: enhancement` | `alternative solutions` |
| [12116](https://github.com/pytest-dev/pytest/issues/12116) | [12081](https://github.com/pytest-dev/pytest/issues/12081) | Nonduplicate | `type: bug` | None |
| [12189](https://github.com/pytest-dev/pytest/issues/12189) | [12081](https://github.com/pytest-dev/pytest/issues/12081) | Nonduplicate | `type: question` | `pytest and OS versions` |

## Judgment rationale and ambiguity

- **12053:** Adding a persistent debugger class setting differs from correcting
  the help text explaining when the debugger starts (8655). The opening already
  describes the long CLI invocation as the current workaround, so no additional
  alternative detail is expected. The request also asks whether configuration
  is possible; enhancement is preferred because it proposes a concrete new
  ini option. An evaluator should not mistake this for a debugger runtime bug.
- **12072:** Both openings show the same flaky plugin import of the removed
  private `call_runtest_hook`. A duplicate candidate is justified independently
  of later labels or closure. Bug versus regression/backward compatibility is
  debatable: a private plugin API dependency does not establish a supported
  pytest compatibility guarantee. Confirmed type is bug. The traceback is useful
  evidence but is not a standalone minimal example; the OS and installed package
  versions remain absent. The pytest version is in the title.
- **12079:** Both openings request file-based selection in place of positional
  arguments. Node IDs from collect-only and optional stdin broaden 11871's
  files/directories request, so duplicate candidate is a judgment about shared
  requested behavior, not identical API details. The alternatives section is
  empty; the real-world goal (finding interdependent tests) is explicit.
- **12116:** Logging from child processes differs from consuming captured
  stdout/stderr using readouterr (12081). The opening has package/OS versions,
  a runnable reproduction, and a queue-handler workaround. Bug versus
  enhancement is ambiguous because the author also offers to implement support;
  bug is retained for the demonstrated missing records. The opening calls the
  processes spawned, while its code uses the platform-default Pool context;
  no claim about an explicit spawn start method is established.
- **12189:** The opening asks for configuration help and uses `-s`, disabling
  capture. It does not call readouterr, so 12081 is related capture context,
  not the same failure/request. Question versus bug remains an annotation
  judgment; a demonstrated defect is not established. A Windows path is not an
  OS version. Package versions and a runnable reproduction are present.

## Provenance and evidence boundary

Verification on 2026-11-18 used GitHub REST issue title/body/created_at and
GraphQL `lastEditedAt: null` for all nine distinct openings in this batch
(including earlier issues). SHA-256 covers UTF-8 `title + NUL + body` without
normalization. Each record stores its exact hash, issue-opening cutoff,
verification timestamp, and the full SHA/committer time returned by the commit
API's latest commit before that cutoff. Both bug and feature templates were
read at each pinned commit; their requested details match the existing profile
(lines 13–16 for bugs, 13/16/19/21 for features).

Earlier candidates all predate the issue under review. Their current comments,
labels, closure states, and later resolution are not replay evidence. The new
cases use verified issue pairs and pinned templates, with no added source/docs
retrieval fixture or historical CI. The existing first-five capture fixture
continues to use pinned documentation and source. The keyword baseline's
candidate pool grows with the catalog, so original cases must also be rerun;
this is still a limited catalog search, not full-history retrieval recall.

The edited comparison issues 12045, 12063, 12067, and 6945 were excluded; their
current text cannot be treated as a verified original. All five new families
are distinct from the first five. The original uncertain 12083 relationship
remains an expected abstention; ambiguity in this batch's type/detail judgments
is recorded above rather than silently treated as objective truth.

## Later human discussion (annotation only)

These comments corroborate the historical outcome but do not replace review
of the expected opening-time judgments above:

- 12053: [maintainer workaround](https://github.com/pytest-dev/pytest/issues/12053#issuecomment-1975196137)
  uses addopts, and the reporter acknowledges it. This strengthens the alternative
  question classification; the proposed enhancement type describes the opening's
  explicit new ini-option request rather than its eventual resolution.
- 12072: [corrected duplicate decision](https://github.com/pytest-dev/pytest/issues/12072#issuecomment-1976585201)
  identifies 12066 and explains the private API dependency. The first closure
  pointed to 12069, then another maintainer corrected it; a closure alone would
  have supplied the wrong annotation.
- 12079: [maintainer confirmation](https://github.com/pytest-dev/pytest/issues/12079#issuecomment-1978683528)
  closes this as covered by the accepted 11871 request.
- 12116: [maintainer discussion](https://github.com/pytest-dev/pytest/issues/12116#issuecomment-1995703367)
  treats general multiprocessing support as potentially plugin work. The proposed
  bug type describes the reported symptom; enhancement or question are defensible
  alternatives given this limitation. It does not establish the requested feature
  was already supported.
- 12189: [maintainer explanation](https://github.com/pytest-dev/pytest/issues/12189#issuecomment-5048499343)
  confirms that disabling capture leaves nothing for JUnit output, consistent with
  the proposed question classification. The later current-main verification is
  annotation context only, never evidence at the opening cutoff.

[The provenance artifact](issue-13-provenance.json) preserves the edit-history
check, pinned template hashes and requested lines, and the successful controlled
replay status for each of the ten cases. Its pending review statuses describe
that smoke run, before human confirmation.
