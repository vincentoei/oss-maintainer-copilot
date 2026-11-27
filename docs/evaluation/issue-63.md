# Issue #63: Qwen3.5 default-model evaluation

Status: **evaluation complete; maintainer accepts promotion with known gaps**.
Qwen3.5 matched 12/12 new synthetic expectations against 8/12 for both controls,
while retaining the three exposed diagnostic disagreements. The original gates
were not all passed. After [independent AI review](issue-63/review/codex-review.md),
the maintainer explicitly accepted the tradeoff and selected Qwen3.5 as the
recommended local configuration. [Decision and policy exception](issue-63/promotion-decision.md)
· [Original evaluation report](issue-63/report.md) · [Scorecard](issue-63/scorecard.json).

| Acceptance area | Evidence / remaining limitations |
| --- | --- |
| Review and publish prior comparison | PR #64 merged as `28f3d36`, preserving frozen history. #62 resolution recorded and issue closed. Earlier measurements and expected outcomes unchanged. |
| Fresh cases and annotation rubric | All [twelve synthetic expectations](issue-63/proposed-cases.json) confirmed by the requesting user before inference. Four bugs, three regressions, three questions, one docs and one null. Rubric frozen in protocol; small designed cohort does not establish real-world generalization. |
| Frozen, approved requests and limits | [Protocol](issue-63/proposal.md), [freeze](issue-63/freeze.json), [actual user approval](issue-63/approval.json), [request hashes](issue-63/request-preview.json) and [pre-dispatch ledger](issue-63/run/reservations.jsonl). Exactly 55 calls; 1528/14,080 output tokens; no retries, repairs, warm-ups, model downloads, hosted calls or API fees. |
| Comparison and per-case changes | [Scorecard](issue-63/scorecard.json) preserves all denominators, statuses, confusion and paired changes. Fresh: candidate 12/12, controls 8/12; candidate gains three regressions and null, loses none. Exposed diagnostics: candidate 0/3 versus both controls 3/3; reported separately. No new fifty-case score. |
| Fresh human semantic/usefulness review | [Actual report sheets](issue-63/review/reports.md), fingerprints, rubric and pending attribution cover all 53 reports. All 53 [Codex/AI ratings](issue-63/review/codex-ratings.json) now have actual attribution, report fingerprints and reasons. **Unverified:** independent human ratings remain unavailable. The frozen human-review/semantic gate remains unpassed; the maintainer accepts this as an explicit policy exception, not a passing gate. |
| Application and resources | Candidate passes all eight Python/API/browser/agent short/long reports, ten calls. All observations report 16K GPU placement; sampled peak candidate device use 4276 MiB. Empty-residency first-call model time 4.981 s; fresh nearest-rank p50 487 ms. Long final prompt 4532 reported tokens. Physical tensor residency, absence of truncation, near-window behavior and model-driven search/inspect remain unverified here. Existing deterministic tests/simulations cover failure guards and unrelated behavior; no live failure was induced. |
| Preservation, tests, review and replay | [Preparation checks](issue-63/preparation-checks.json): 510 passed, two opt-in skips, Ruff/mypy and seven prior audits pass. Separate [preparation reviews](issue-63/preparation-review.md) have no remaining blockers. The new auditor reproduced all 53 full report/context objects and matched 55 charges without further inference. [Publication checks](issue-63/publication-checks.json) include byte-exact clean-clone replay; [final Standards/Spec review](issue-63/publication-review.md) has zero publication blockers and identifies the pending human review. Earlier artifacts are unchanged. |
| Recommendation and tradeoffs | The original measured report and AI review recommend retain under the frozen gates. The later [maintainer decision](issue-63/promotion-decision.md) promotes the recommended local setup despite disclosed gaps. README/current launch settings select Qwen3.5; 3B remains a manual lower-memory choice. Library opt-in behavior and benchmark defaults stay unchanged. Resolution is ready for publication; merge/closure are not yet recorded. |

Audit saved responses, reports, accounting, placement and scores without inference:

```sh
PYTHONPATH=src .venv/bin/python scripts/issue63_results.py
```

With the retained hash-verified local diagnostic snapshot, this reproduces
`issue-63/scorecard.json` byte for byte. Without that private snapshot, the auditor
still verifies raw response/accounting/scoring but explicitly lists the nine
historical report structures it could not replay. Contributor openings are not
republished in bulk under ADR-0003.

The runner refuses to reuse the existing allocation. The pre-run source and
proposal are frozen historical evidence; their pending-status wording does not
override the later approval and measured results. Actual AI report ratings are now published separately; independent human
ratings remain pending. The later maintainer decision does not alter the original
protocol, its failed promotion safeguards or measured results.
