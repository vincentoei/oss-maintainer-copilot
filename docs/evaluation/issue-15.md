# Issue #15: twenty-case historical benchmark

All twenty confirmed cases passed replay integrity checks and were scored by both
controlled responses and the keyword-rule baseline. There are no excluded catalog
cases or replay/scoring errors. Completion does not imply correct predictions.

The five new outcomes were reviewed by Codex under the requesting user’s explicit
delegation and acceptance. This is delegated assistant review accepted by the user,
not independent human assessment. See [case review](cases-sixteen-through-twenty.md),
[provenance and integrity results](issue-15-provenance.json), and
[raw field scores, drafts and errors](issue-15-results.json).

## Aggregate field metrics

Each metric uses all completed cases; uncertain relationship judgments are excluded
from relationship accuracy rather than counted as correct. Expanding the verified
candidate catalog can change scores for existing cases. The controlled comparator
uses one paired earlier issue; keyword retrieval searches the eligible catalog.

| Metric | Controlled: fifteen | Controlled: twenty | Keyword: fifteen | Keyword: twenty |
| --- | ---: | ---: | ---: | ---: |
| cases | 15 | 20 | 15 | 20 |
| completed | 15 | 20 | 15 | 20 |
| mean_candidate_pool_size | 1.0 | 1.0 | 13.6 | 17.2 |
| duplicate_retrieval_recall | 1.0 | 0.95 | 0.733 | 0.6 |
| duplicate_judgment_accuracy | 0.714 | 0.737 | 0.5 | 0.421 |
| issue_type_accuracy | 0.0 | 0.0 | 0.4 | 0.5 |
| missing_details_exact | 0.4 | 0.35 | 0.4 | 0.35 |
| missing_details_precision | 0.767 | 0.775 | 0.767 | 0.775 |
| missing_details_recall | 0.667 | 0.65 | 0.667 | 0.65 |
| citation_validity_rate | 1.0 | 1.0 | 1.0 | 1.0 |
| issue_type_abstention_appropriateness | 0.0 | 0.0 | 0.867 | 0.9 |
| duplicate_abstention_appropriateness | 0.933 | 0.95 | 0.933 | 0.95 |
| mean_latency_ms | 1761.78 | 1568.41 | 8257.17 | 13135.85 |

## Results across every eligible case

“Pending” marks the uncertain relationship. Citation validity checks the evidence
boundary and citation wiring; semantic support remains a separate human judgment.

| Case | Method | Retrieved pair | Relationship correct | Type correct | Details exact | Citation valid |
| --- | --- | --- | --- | --- | --- | --- |
| 7312 | controlled | yes | no | no | yes | yes |
| 10156 | controlled | yes | yes | no | yes | yes |
| 12053 | controlled | yes | yes | no | no | yes |
| 12072 | controlled | yes | no | no | no | yes |
| 12079 | controlled | yes | no | no | no | yes |
| 12081 | controlled | yes | no | no | yes | yes |
| 12083 | controlled | yes | pending | no | no | yes |
| 12116 | controlled | yes | yes | no | no | yes |
| 12146 | controlled | yes | yes | no | yes | yes |
| 12189 | controlled | yes | yes | no | no | yes |
| 12197 | controlled | yes | yes | no | no | yes |
| 12201 | controlled | yes | yes | no | no | yes |
| 12203 | controlled | yes | yes | no | yes | yes |
| 12204 | controlled | yes | yes | no | yes | yes |
| 12216 | controlled | yes | yes | no | no | yes |
| 12219 | controlled | yes | yes | no | no | yes |
| 12223 | controlled | yes | yes | no | no | yes |
| 12224 | controlled | yes | yes | no | yes | yes |
| 12226 | controlled | no | no | no | no | yes |
| 12228 | controlled | yes | yes | no | no | yes |
| 7312 | keyword_rule | yes | no | yes | yes | yes |
| 10156 | keyword_rule | yes | yes | no | yes | yes |
| 12053 | keyword_rule | yes | yes | no | no | yes |
| 12072 | keyword_rule | yes | no | yes | no | yes |
| 12079 | keyword_rule | yes | no | yes | no | yes |
| 12081 | keyword_rule | yes | no | no | yes | yes |
| 12083 | keyword_rule | no | pending | no | no | yes |
| 12116 | keyword_rule | yes | yes | no | no | yes |
| 12146 | keyword_rule | no | no | no | yes | yes |
| 12189 | keyword_rule | yes | yes | no | no | yes |
| 12197 | keyword_rule | yes | yes | no | no | yes |
| 12201 | keyword_rule | yes | yes | yes | no | yes |
| 12203 | keyword_rule | no | no | yes | yes | yes |
| 12204 | keyword_rule | no | no | yes | yes | yes |
| 12216 | keyword_rule | yes | yes | no | no | yes |
| 12219 | keyword_rule | yes | yes | no | no | yes |
| 12223 | keyword_rule | no | no | yes | no | yes |
| 12224 | keyword_rule | no | no | yes | yes | yes |
| 12226 | keyword_rule | no | no | yes | no | yes |
| 12228 | keyword_rule | no | no | yes | no | yes |

## Representative failures

The JSON retains expected/observed fields and generated drafts for every case.

### controlled

- #7312 `duplicate_judgment`: expected=duplicate_candidate; observed=related_issue.
- #7312 `issue_type`: expected=type: enhancement; observed=None.
- #7312 `abstention`: observed_fields=['issue_type', 'missing_details']; duplicate_expected=False; duplicate_observed=False; issue_type_appropriate=False.
- #12053 `missing_details`: expected=[]; observed=['alternative solutions', 'real-world use case'].
- #12226 `duplicate_retrieval`: expected_issue=12197; retrieved_issues=[].

### keyword_rule

- #7312 `duplicate_judgment`: expected=duplicate_candidate; observed=related_issue.
- #10156 `issue_type`: expected=type: docs; observed=type: infrastructure.
- #12053 `missing_details`: expected=[]; observed=['alternative solutions', 'real-world use case'].
- #12083 `duplicate_retrieval`: expected_issue=7012; retrieved_issues=[].
- #12083 `abstention`: observed_fields=['draft_reply', 'missing_details']; duplicate_expected=True; duplicate_observed=False; issue_type_appropriate=True.

## Acceptance evidence

1. **Twenty reviewed cases:** five metadata files add #12219, #12223, #12224,
   #12226 and #12228. Each records public IDs, opening cutoff, commit SHA/time,
   expected outcomes, opening/pair content hashes, and delegated confirmation.
   The case review explains all five relationships and missing-detail judgments.
   Existing cases retain duplicate and uncertain judgments; the new batch adds
   topical negatives, documentation and enhancement coverage.
2. **Replay integrity:** provenance records successful live controlled replay for
   all twenty. Replay checks commit SHA/time, opening hash/time/title and earlier
   issue hash/time before model input. Nine newly acquired openings also passed
   REST/GraphQL agreement and unedited-content checks; pinned templates were read
   and hashed. No catalog case needed exclusion. Edited selection candidates
   #12269/#12270 were rejected with explicit reasons in provenance.
3. **Benchmark reporting:** both methods completed 20/20 with empty error lists.
   Aggregates above, every case’s field scores, and representative failures are
   available here and in JSON. New cases were refreshed after confirmation because
   the initial run loaded their pending status; aggregates use the unchanged
   fifteen results plus the five confirmed reruns for each method.

Validation: 165 deterministic tests passed, two optional live tests skipped.
Live controlled replay separately completed all twenty. Typechecking, lint and
format checks passed. The evaluator itself verified GitHub evidence for both methods.

## Reproduce

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.evaluation > /tmp/evaluation-new-results.json
uv run --locked --no-env-file pytest -q
uv run --locked --no-env-file mypy
uv run --locked --no-env-file ruff check .
uv run --locked --no-env-file ruff format --check .
```

## Unverified judgments and limitations

No local model was selected or called. Model selection and llmfit belong to #21
after #15 and before #16. Earlier model-quality measurements remain provisional.
Controlled responses abstain on type by design; they establish replay behavior.
The keyword baseline evaluates existing rules, not local model quality. Neither
method is a quality reference. Generated reply usefulness, semantic citation
support and other-field abstention appropriateness remain pending human review:
outcome confirmation does not establish these report-level judgments. Historical
CI is unavailable. Candidate retrieval covers only hash-verified catalog openings
preceding each cutoff, not full history; other retrieved pairs are unreviewed.
Later comments, labels, closures and fixes never enter replay input.

Public API/model fees are assumed zero; CPU, network and hosting costs are
excluded. Latencies include GitHub reads and are observational; the acquisition
and benchmark runs overlapped, so these timings do not establish performance gains.
