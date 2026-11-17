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
| Mean end-to-end latency | 1,855.99 ms | 1,834.33 ms |
| Replay errors | 0 | 0 |
| Draft-reply usefulness | Pending human review | Pending human review |

The one uncertain duplicate relationship is excluded from exact judgment
accuracy. Exact matching cannot establish whether a `related_issues` entry
appropriately conveys that uncertainty. The case-level output records the
observed relationship and `pending_human_review` for that judgment.

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

## Human review still needed

The saved draft replies are ready for a maintainer to rate. For each case,
record whether the reply asks for the confirmed missing details, presents the
earlier issue with suitable uncertainty, and makes only supported claims.
Mark each as useful, partly useful, or not useful, with a short reason.
Citation checks here verify structure and the pinned evidence boundary;
whether each cited passage actually supports the surrounding wording also
needs human review. The uncertain #12083 relationship likewise needs a human
judgment of the report's phrasing. No pending judgment is counted as correct.

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
