# Issue #17 two-axis review

Fixed point: updated main `1bec247b9e13d18a265610c99f0778ef13f176bf`.
Reviewed `git diff 1bec247b9e13d18a265610c99f0778ef13f176bf...HEAD` through
`b20a294`, including implementation `8640bae` and the completed evidence commit.
The implementation was reviewed before inference; both independent reviewers
then reviewed the final artifacts. Neither reviewer edited files or ran inference.

Standards sources: AGENTS.md, docs/agents/{issue-tracker,triage-labels,domain}.md,
GLOSSARY.md, docs/adr/0001 through 0004, docs/project-brief.md and README.md,
plus the code-review skill's full smell baseline. No CONTRIBUTING.md or
CODING_STANDARDS.md exists. The spec source was GitHub issue #17, with the user's
explicit case-review delegation and agreed replay/runner test seams.

## Standards

No documented standards violations or actionable smell findings in the full diff
through `b20a294`.

The final documentation and artifacts follow the glossary and ADRs: historical
evidence stays frozen, published case metadata excludes full issue bodies, shared
families remain together, and delegated case confirmation is distinguished from
pending report reviews. Measurements disclose eligibility, denominators,
failures and comparison limits.

Offline verification passed with writes disabled: 204 preserved files, 30 cases,
28 families, 90 workflow rows, 115 request/response pairs and 87 recomputed scores.
All 90 fresh report review records remain pending.

Tooling-enforced concerns were excluded. The pending code-review document link
is understood.

## Spec

No findings. The complete diff satisfies #17 within the authorized
delegated-review basis:

- “Ten new cases have human-confirmed outcomes and complete replay metadata,
  with issue-family partition checks”: all ten additions have explicit delegated
  confirmation, replay metadata and provenance. Offline checks validate 30 cases
  across 28 families and 35 recorded members, preserving all 204 baseline files.
- “Expanded set preserves duplicate, nonduplicate, missing-detail, ambiguous
  coverage”: verified 5 duplicate candidates, 23 nonduplicates and 2 uncertain
  relationships, with cases both containing and lacking missing details.
- “All workflows rerun on eligible cases and updated results identify changed
  cases and scores”: all ten additions passed preflight. Three workflows evaluated
  all 29 eligible cases, retaining 90 rows. Existing #12204's input-bound failure
  is consistently flagged and clearly disclosed. The comparison identifies
  #12081's agent changes and #12204's three changed rows, records candidate-pool
  changes, and separates original/new subsets.

The frozen protocol is supported by 115 charged dispatches and corresponding
bounded raw responses, below the 150 cap. Offline verification reproduced the
committed comparison and verification artifacts and recomputed all 87 available
scores without network, inference or file changes.

Fresh reply usefulness, semantic citation review and future training-corpus
checks remain explicitly unverified, as required. No scope creep identified.

Standards: 0 findings, no worst issue. Spec: 0 findings, no worst issue.

## Follow-up review

Reviewed `git diff 11fa8ff...17c32a7`: `cfc068e` (bounded verified openings),
`d7becc6` (one timeout-only commit-read retry), and `17c32a7` (final evidence).
Both reviewers worked read-only without network, inference or repeated tests.

### Standards

No findings. No documented-standard violations or actionable baseline smells.
The retry stays local, bounded to two attempts and limited to `TimeoutError`.
The committed evidence retains the initial timeout and formatting failure
alongside their successful follow-ups. Original benchmark artifacts are unchanged;
the verifier checks application hashes at the original inference commit.
Documentation distinguishes controlled replay validation from quality measurements.

### Spec

No findings. Permanent commit failure flags the case before issue/model calls.
Regressions exercise timeout recovery/exhaustion, bounded historical input and
continued live rejection. Final evidence records thirty successful controlled
replays, including two expected historical-CI partial reports, and the full
40,484-character #12204 agent input. The original failed follow-up and real-model
results remain preserved, with no new provider inference or quality ratings.
Recorded checks: 354 passed, 2 skipped; focused checks: 58 passed, 2 skipped.

Follow-up Standards: 0 findings, no worst issue. Follow-up Spec: 0 findings,
no worst issue.
