# Issue #14: fifteen-case evaluation

The existing evaluator was run on all fifteen cases with controlled responses and
the keyword-rule baseline. Five new expected outcomes remain pending human
confirmation. They replay successfully, but the unchanged scorer rejects them:
`case needs a confirmed human review before scoring`. Thus these are **ten scored
cases plus five explicit errors per method**, not fifteen confirmed-case scores.

See [case proposals and ambiguities](cases-eleven-through-fifteen.md),
[provenance and all-fifteen controlled replay](issue-14-provenance.json), and
[raw scores, drafts, and errors](issue-14-results.json).

## Aggregate comparison

Each new aggregate uses only completed scores. The larger keyword candidate pool
can change older cases even while the new outcomes remain unconfirmed. Rates
below must not be described as quality on fifteen human-confirmed cases.

| Metric | Controlled: previous ten | Controlled: expanded catalog | Keyword: previous ten | Keyword: expanded catalog |
| --- | ---: | ---: | ---: | ---: |
| cases | 10 | 15 | 10 | 15 |
| completed | 10 | 10 | 10 | 10 |
| mean candidate pool size | 1.0 | 1.0 | 10.9 | 13.6 |
| duplicate retrieval recall | 1.0 | 1.0 | 0.8 | 0.8 |
| duplicate judgment accuracy | 0.556 | 0.556 | 0.444 | 0.444 |
| issue type accuracy | 0.0 | 0.0 | 0.3 | 0.3 |
| missing details exact | 0.4 | 0.4 | 0.4 | 0.4 |
| missing details precision | 0.75 | 0.75 | 0.75 | 0.75 |
| missing details recall | 0.7 | 0.7 | 0.7 | 0.7 |
| citation validity rate | 1.0 | 1.0 | 1.0 | 1.0 |
| issue type abstention appropriateness | 0.0 | 0.0 | 0.9 | 0.9 |
| duplicate abstention appropriateness | 0.9 | 0.9 | 0.9 | 0.9 |
| mean latency ms | 1564.92 | 2249.34 | 6651.34 | 7907.4 |

## Field-level results and failures

A dash denotes the uncertain #12083 relationship. Pending cases have no scores.
Deterministic citation validity checks URLs/cutoffs; semantic support and generated
reply usefulness remain pending human review for every newly generated report.

| Case | Method | Retrieved | Relationship correct | Type correct | Details exact | Citation boundary |
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
| 12197 | controlled | pending | pending | pending | pending | pending |
| 12201 | controlled | pending | pending | pending | pending | pending |
| 12203 | controlled | pending | pending | pending | pending | pending |
| 12204 | controlled | pending | pending | pending | pending | pending |
| 12216 | controlled | pending | pending | pending | pending | pending |
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
| 12197 | keyword_rule | pending | pending | pending | pending | pending |
| 12201 | keyword_rule | pending | pending | pending | pending | pending |
| 12203 | keyword_rule | pending | pending | pending | pending | pending |
| 12204 | keyword_rule | pending | pending | pending | pending | pending |
| 12216 | keyword_rule | pending | pending | pending | pending | pending |

### Errors

- #12197 controlled: case needs a confirmed human review before scoring.
- #12201 controlled: case needs a confirmed human review before scoring.
- #12203 controlled: case needs a confirmed human review before scoring.
- #12204 controlled: case needs a confirmed human review before scoring.
- #12216 controlled: case needs a confirmed human review before scoring.
- #12197 keyword_rule: case needs a confirmed human review before scoring.
- #12201 keyword_rule: case needs a confirmed human review before scoring.
- #12203 keyword_rule: case needs a confirmed human review before scoring.
- #12204 keyword_rule: case needs a confirmed human review before scoring.
- #12216 keyword_rule: case needs a confirmed human review before scoring.

### Scored failures

- #7312 controlled: duplicate_judgment, issue_type, abstention.
- #10156 controlled: issue_type, abstention.
- #12053 controlled: issue_type, missing_details, abstention.
- #12072 controlled: duplicate_judgment, issue_type, missing_details, abstention.
- #12079 controlled: duplicate_judgment, issue_type, missing_details, abstention.
- #12081 controlled: duplicate_judgment, issue_type, abstention.
- #12083 controlled: issue_type, missing_details, abstention.
- #12116 controlled: issue_type, missing_details, abstention.
- #12146 controlled: issue_type, abstention.
- #12189 controlled: issue_type, missing_details, abstention.
- #7312 keyword_rule: duplicate_judgment.
- #10156 keyword_rule: issue_type.
- #12053 keyword_rule: issue_type, missing_details.
- #12072 keyword_rule: duplicate_judgment, missing_details.
- #12079 keyword_rule: duplicate_judgment, missing_details.
- #12081 keyword_rule: duplicate_judgment, issue_type.
- #12083 keyword_rule: duplicate_retrieval, issue_type, missing_details, abstention.
- #12116 keyword_rule: issue_type, missing_details.
- #12146 keyword_rule: duplicate_retrieval, duplicate_judgment, issue_type, abstention.
- #12189 keyword_rule: issue_type, missing_details.

## Acceptance evidence

1. **Five new verified cases: partial.** Metadata and provenance record verified
   unedited title/body hashes, opening cutoffs, pre-cutoff commit timestamps, and
   pinned template hashes. Human-confirmed outcomes remain unverified because the
   requesting user has not yet accepted the five proposals. All records remain
   pending; no reviewer identity or confirmation time is invented.
2. **Difficult topical negatives: prepared.** The case review explains the
   differences for each of five plausible pairs. These are proposed nonduplicate
   judgments awaiting acceptance, not model-derived expected outcomes.
3. **All-fifteen scoring: partial.** Both methods attempted all fifteen; the JSON
   preserves all field scores and errors. All-fifteen controlled replay completed
   successfully, but five cases per method are unscored until human confirmation.
   After confirmation, record the reviewer/time, retain the guard, rerun evaluation
   on all fifteen, and replace this report with confirmed-case field results.

## Reproduce and limitations

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > /tmp/evaluation-new-results.json
uv run --locked --no-env-file pytest -q
uv run --locked --no-env-file mypy
uv run --locked --no-env-file ruff check .
uv run --locked --no-env-file ruff format --check .
```

No local model was selected or called. Model selection and llmfit remain #21
after #15 and before #16; all earlier model-quality observations are provisional.
Controlled responses abstain on type by design and are smoke checks. The keyword
baseline uses existing lexical retrieval, template checks and cue rules. Neither
is a quality reference. Public API/model fees are assumed zero; CPU, network and
hosting cost are excluded. Latency includes network reads. Candidate pools are
limited to verified catalog openings preceding each cutoff, not full history.
Other retrieved pairs remain unreviewed. Later annotations never enter model
input; historical CI is unavailable. Expected-outcome confirmation does not
confirm generated reply usefulness or semantic citation support.
