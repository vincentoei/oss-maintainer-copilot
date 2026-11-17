# Issue #12: first field-level scores and keyword-rule baseline

These are provisional results for the five human-confirmed cases from
[the first case review](first-five-cases.md). The exact per-case fields, draft
replies, latency, errors, cutoff, and pinned commit are in
[the results JSON](issue-12-results.json). This run used public GitHub content
on 2026-11-18 with an authenticated read-only API credential. No local model
was selected or called.

## Methods

`controlled` is the existing smoke replay: it supplies the one verified earlier
issue to the lexical matching rules and uses a fixed model response that
abstains on issue type. It is not a quality reference.

`keyword_rule` uses the same opening issue text, verified earlier issue, pinned
pytest commit, template rules, and lexical match logic. It first filters the
earlier issue by the generated keyword query and then selects a type from
literal issue-text cues. It includes every available citation-backed reply
statement. Neither method reads later comments, labels, or closure decisions.
Both run through `replay_case`, which rejects changed issue content and a
post-cutoff or mismatched commit before scoring.

Each case contains **one chosen earlier issue**. The retrieval rate below is
whether that known issue surfaced from the pair fixture; it does not estimate
search recall or ranking over pytest's full issue history. Both methods use the
same report implementation for missing details and citations. Network reads
are repeated for each method, so wall-clock latency includes GitHub and raw
source fetches and is sensitive to network conditions. Both methods made zero
paid model calls. Public GitHub reads were assumed to have no per-request
dollar charge; CPU, network, and hosting costs were excluded. Anonymous GitHub
API rate limits can interrupt a run; the checked-in run completed with zero
errors using the existing GitHub CLI credential.

## Aggregate results

| Field | Controlled smoke replay | Keyword-rule baseline |
| --- | ---: | ---: |
| Completed / attempted | 5 / 5 | 5 / 5 |
| Known earlier issue surfaced | 5 / 5 | 3 / 5 |
| Confirmed duplicate/nonduplicate judgment | 2 / 4 | 1 / 4 |
| Issue type exact match | 0 / 5 | 1 / 5 |
| Missing details exact match | 4 / 5 | 4 / 5 |
| Missing details precision / recall (case macro) | 1.0 / 0.8 | 1.0 / 0.8 |
| Deterministic citation validity | 5 / 5 cases | 5 / 5 cases |
| Appropriate issue-type abstention | 0 / 5 | 4 / 5 |
| Appropriate duplicate abstention | 4 / 5 | 4 / 5 |
| Mean end-to-end latency | 1,764.90 ms | 2,625.06 ms |
| Replay errors | 0 | 0 |
| Draft-reply usefulness (human confirmed) | 5 partly useful | 3 partly useful, 2 not useful |

The one uncertain duplicate relationship is excluded from exact judgment
accuracy. The confirmed expected abstention for #12083 is scored separately:
neither method explicitly abstained on `duplicate_candidates`, so both score
4/5 on duplicate abstention. Exact matching cannot establish whether a
`related_issues` entry adequately conveys uncertainty; the requesting user
confirmed the recorded judgment for that case.

## Representative failures

- #12081 and #7312 are confirmed duplicate candidates, but both methods place
  their earlier issue under related issues. The keyword baseline also labels
  #12081 `type: docs` instead of the confirmed `type: enhancement`.
- #12083 needs `pip list output`; neither method asks for it. The keyword
  query also misses the known earlier issue #7012 and guesses `type: bug`
  instead of `type: regression`.
- #10156 is a documentation request, but the keyword baseline guesses
  `type: infrastructure`. The controlled response abstains on all five known
  issue types by design.

## Human-confirmed draft review

The requesting user confirmed all ten saved reply ratings and reasons on
2026-11-18 (Asia/Jakarta), along with the citation-support checks and
uncertainty judgments. The JSON records the confirmation time, a rating and
reason for every draft, each citation's claim and support judgment, and
missing-detail request checks. The saved drafts and deterministic scores did
not change.

The review fetched all nine distinct issue opening titles/bodies and matched
their stored SHA-256 hashes. It checked the two pinned capture passages and
the pinned bug template. Only opening content and pinned files were used;
later comments and resolutions were excluded. Issue citations have null saved
passages, so their opening bodies were inspected directly. All 12 citation
occurrences were checked: eight support their limited claims and four only
partly support them. The two uncited fallback replies have no citation-support
judgment to pass.

| Case | Method | Usefulness | Reason and uncertainty judgment |
| --- | --- | --- | --- |
| #7312 | controlled | partly useful | Relevant #349 link, but no duplicate-candidate explanation; the unspecified negated condition is unsupported as a distinction. |
| #7312 | keyword_rule | partly useful | Same reply: relevant link, unsupported negation, and insufficient explanation of the expected duplicate candidate. |
| #10156 | controlled | partly useful | Relevant #2959 background and appropriate caution, but no explanation of the documentation request versus frozen-parameter bug. |
| #10156 | keyword_rule | partly useful | Same reply: supported cautious relevance, but generic tokens do not explain the nonduplicate distinction. |
| #12081 | controlled | partly useful | Relevant #3448 and supported capture references, but unsupported negation and no explanation of the shared output-loss behavior or duplicate candidate. |
| #12081 | keyword_rule | partly useful | Same reply: valid documentation/source claims, but the source sentence merely says a line exists and the relationship explanation is inadequate. |
| #12083 | controlled | partly useful | Relevant #7012 and supported caution, but missing `pip list output` request and explicit duplicate abstention; differing reproductions are unexplained. |
| #12083 | keyword_rule | not useful | Generic fallback; no `pip list output` request, #7012 discussion, or explicit duplicate abstention. |
| #12146 | controlled | partly useful | Relevant #7312 and supported caution, but no explanation of fixture-derived parameter values versus repeated fixture execution. |
| #12146 | keyword_rule | not useful | Generic fallback without case-specific evidence or the expected nonduplicate distinction. |

For #7312 and #12081, the earlier openings support shared requested behavior;
the claim that one report negates a shared condition does not identify a
substantive contradiction. For #10156 and #12146, the cautious relationship
claims are supported, but explaining the actual distinction would make the
replies more useful. The #12081 documentation supports access to captured
stdout/stderr, and source line 935 exists as claimed; neither draft explains
the buffer-reset behavior using that source.

For #12083, both reports fail the expected request and explicit duplicate
abstention. The controlled wording that the same failure is not established
is a supported caution, but does not explicitly state that whether #7012 is a
duplicate remains uncertain or explain the pytest 8 file-plus-directory
regression versus the earlier pytest 5.4.1 empty-argument example. Its saved
abstention fields omit `duplicate_candidates`. The keyword fallback abstains
on the draft generally, which also does not meet the duplicate-specific
expectation. Neither reply is fully useful. The pinned
[bug template](https://github.com/pytest-dev/pytest/blob/03e54712dd123138aa4c1035a027e17d0dd9a86c/.github/ISSUE_TEMPLATE/1_bug_report.md#L14)
requests `pip list` output; version information in #12083 does not supply it.

The requesting user confirmed these assessments. The #12083 missing-detail
and duplicate-abstention failures remain recorded as failures.

## Reproduce

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > docs/evaluation/issue-12-results.json
uv run --locked --no-env-file pytest -q tests/test_evaluation.py tests/test_replay.py
```

The evaluation command performs live public reads and records errors if a
case's provenance cannot be verified. CI runs the deterministic scorer and
citation tests without network access. The five-case estimates and controlled
responses are provisional. Model selection and `llmfit` belong to #21 after
#15 and before #16.

The command above regenerates raw scores and would overwrite the recorded
review additions. To compare a new run while retaining this review, redirect
its output to a separate file; the ratings apply only to these saved drafts.
