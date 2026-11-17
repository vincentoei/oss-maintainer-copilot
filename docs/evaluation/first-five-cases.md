# First five reviewed pytest evaluation cases

Issue [#11](https://github.com/vincentoei/oss-maintainer-copilot/issues/11)
asks for five historical evaluation cases. These case records store
issue IDs, issue-family IDs, opening cutoffs, content hashes, pinned pytest
commits, confirmed expected triage outcomes, and explicit human-review status.
Contributor issue bodies are fetched from pytest when replay runs.

## Reviewer-confirmed judgments

| Issue under review | Earlier issue | Relationship | Issue type | Missing details | Opening-content comparison |
| --- | --- | --- | --- | --- | --- |
| [#12081](https://github.com/pytest-dev/pytest/issues/12081) | [#3448](https://github.com/pytest-dev/pytest/issues/3448) | Duplicate candidate | `type: enhancement` | None | Both describe `readouterr()` consuming output that is then absent from failure reports. #12081 proposes a new copy operation. |
| [#7312](https://github.com/pytest-dev/pytest/issues/7312) | [#349](https://github.com/pytest-dev/pytest/issues/349) | Duplicate candidate | `type: enhancement` | None applicable from the 2020 generic template | Both request fixture values in parametrization; #7312 specifies a session-scoped source. |
| [#12146](https://github.com/pytest-dev/pytest/issues/12146) | [#7312](https://github.com/pytest-dev/pytest/issues/7312) | Nonduplicate | `type: bug` | None | Recreated parameter tuples cause a cached fixture to run twice; #7312 requests a new source of parameter values. |
| [#10156](https://github.com/pytest-dev/pytest/issues/10156) | [#2959](https://github.com/pytest-dev/pytest/issues/2959) | Nonduplicate | `type: docs` | None | A documentation request for dynamic fixture registration differs from an earlier bug about frozen fixture parameters. |
| [#12083](https://github.com/pytest-dev/pytest/issues/12083) | [#7012](https://github.com/pytest-dev/pytest/issues/7012) | Uncertain | `type: regression` | `pip list output` | Both involve collection arguments and duplicate tests, but the pytest 8 file-plus-directory regression differs from the older empty-argument example. |

The requesting user confirmed all five proposed relationships, issue types,
and missing-detail judgments in the implementation conversation on
2026-11-18 (Asia/Jakarta). Each JSON file records `human_review.status` as
`confirmed`, the reviewer as `requesting user`, and the UTC time when that
confirmation was recorded. The uncertain #12083 relationship is a confirmed
expected abstention: its opening evidence does not settle whether #7012 is a
duplicate.

Later comments or closure decisions can inform the annotation. For example,
post-opening discussion on #7312 points to #349, the later closure of #10156
points to #12376, and later discussion of #7012 links a fix for #12083. None
of those later records enter the replayed issue text, earlier issue text, or
model request. A label or closure reason alone never establishes a duplicate or
nonduplicate judgment.

## Provenance and replay checks

On 2026-11-17, GitHub GraphQL returned `lastEditedAt: null` for the opening
title/body of all five issues and their five distinct earlier issues. The
recorded SHA-256 is over the REST issue `title + NUL + body` without text
normalization. Each case records the REST `created_at` as its cutoff, the full
commit SHA and committer time of the latest pytest commit returned before that
cutoff, and the UTC verification time. The live replay independently checked
the public title, cutoff, hash, earlier issue content, and Git commit record.
The JSON files publish the exact values; the issue bodies are not copied here.

The [2020 generic issue template](https://github.com/pytest-dev/pytest/blob/61a6ac97054c0bd6f812642b46847c4b7cbede2a/.github/ISSUE_TEMPLATE.md)
predates the separate bug and feature templates. The #7312 replay therefore
does not cite newer template requirements. Later cases use their pinned commits
for template links. Only #12081 requests pinned capture documentation and
source evidence; the other four cases use the verified earlier issue as their
retrieval fixture. Historical CI checks remain unavailable to replay.

`python -m maintainer_copilot.replay --all` completed all five cases on
2026-11-17 with controlled model responses. No case was flagged. The model
abstained on issue type and the retrieval heuristic put the one earlier issue
for each case under related issues. These results verify replay and the evidence
boundary; they are provisional observations, not measured model quality. The
expected outcomes above are human-confirmed and separate from the controlled
report outputs. Model selection and `llmfit` belong to
[#21](https://github.com/vincentoei/oss-maintainer-copilot/issues/21) after
#15 and before #16.

## Limits of this first set

Each replay supplies one deliberately chosen earlier issue, so this set can
check the judgment on a known pair but cannot measure search recall or ranking
among many candidates. Five cases, one uncertain relationship, and only one
expected missing detail are too few for a stable quality estimate. The cases
are valid first reviewed examples and replay fixtures; quality measurements
remain provisional until the evaluation set and retrieval task expand.
