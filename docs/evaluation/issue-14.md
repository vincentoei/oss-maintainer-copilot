# Issue #14: fifteen-case evaluation

All fifteen cases were replayed and scored with controlled responses and the
keyword-rule baseline after acceptance of the five new outcomes. Both methods
completed all fifteen with no replay or scoring errors. Field-level failures
below remain visible; completion does not imply correct predictions.

The requesting user explicitly delegated the five-case review to Codex and
accepted its confirmation as their own. Codex confirmed all five proposals
without changes on 2026-11-18. This is delegated assistant review accepted by
the user, not an independent human assessment. Case metadata records that
attribution and confirmation time; the scoring guard is unchanged.

See [confirmed outcomes and rationale](cases-eleven-through-fifteen.md),
[opening provenance and earlier controlled replay](issue-14-provenance.json), and
[raw scores, drafts, and errors](issue-14-results.json).

## Aggregate comparison

Each aggregate uses all completed scores. The larger keyword candidate pool
can change older cases. The previous run scored ten cases; this run scores fifteen.

| Metric | Controlled: previous ten | Controlled: fifteen | Keyword: previous ten | Keyword: fifteen |
| --- | ---: | ---: | ---: | ---: |
| cases | 10 | 15 | 10 | 15 |
| completed | 10 | 15 | 10 | 15 |
| mean candidate pool size | 1.0 | 1.0 | 10.9 | 13.6 |
| duplicate retrieval recall | 1.0 | 1.0 | 0.8 | 0.733 |
| duplicate judgment accuracy | 0.556 | 0.714 | 0.444 | 0.5 |
| issue type accuracy | 0.0 | 0.0 | 0.3 | 0.4 |
| missing details exact | 0.4 | 0.4 | 0.4 | 0.4 |
| missing details precision | 0.75 | 0.767 | 0.75 | 0.767 |
| missing details recall | 0.7 | 0.667 | 0.7 | 0.667 |
| citation validity rate | 1.0 | 1.0 | 1.0 | 1.0 |
| issue type abstention appropriateness | 0.0 | 0.0 | 0.9 | 0.867 |
| duplicate abstention appropriateness | 0.9 | 0.933 | 0.9 | 0.933 |
| mean latency ms | 1564.92 | 1761.78 | 6651.34 | 8257.17 |

## Field-level results and failures

A dash denotes the uncertain #12083 relationship. Deterministic citation validity
checks URLs/cutoffs; semantic support and generated reply usefulness remain
pending review for every newly generated report.

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
| 12197 | controlled | yes | yes | no | no | yes |
| 12201 | controlled | yes | yes | no | no | yes |
| 12203 | controlled | yes | yes | no | yes | yes |
| 12204 | controlled | yes | yes | no | yes | yes |
| 12216 | controlled | yes | yes | no | no | yes |
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
| 12197 | keyword_rule | yes | yes | no | no | yes |
| 12201 | keyword_rule | yes | yes | yes | no | yes |
| 12203 | keyword_rule | no | no | yes | yes | yes |
| 12204 | keyword_rule | no | no | yes | yes | yes |
| 12216 | keyword_rule | yes | yes | no | no | yes |

### Errors

None. Both methods scored 15 of 15 cases.

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
- #12197 controlled: issue_type, missing_details, abstention.
- #12201 controlled: issue_type, missing_details, abstention.
- #12203 controlled: issue_type, abstention.
- #12204 controlled: issue_type, abstention.
- #12216 controlled: issue_type, missing_details, abstention.
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
- #12197 keyword_rule: issue_type, missing_details, abstention.
- #12201 keyword_rule: missing_details.
- #12203 keyword_rule: duplicate_retrieval, duplicate_judgment.
- #12204 keyword_rule: duplicate_retrieval, duplicate_judgment.
- #12216 keyword_rule: issue_type, missing_details.

## Acceptance evidence

1. **Five verified and accepted cases.** Existing provenance records verified
   unedited title/body hashes, opening cutoffs, pre-cutoff commit timestamps, and
   pinned template hashes. All five expected outcomes now record confirmation
   through the requesting user's explicit delegation to Codex.
2. **Difficult topical negatives confirmed.** The case review explains why each
   of the five plausible pairs describes different behavior or symptoms.
3. **All-fifteen scoring completed.** Both methods replayed and scored all fifteen;
   the JSON preserves field scores, failures, generated drafts, and empty error
   lists. Opening hashes and cutoff-safe evidence were checked during replay.

Validation: 160 tests passed, two optional live tests skipped; typechecking,
lint, and formatting passed. The evaluator separately exercised all fifteen
cases per method against GitHub.

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
