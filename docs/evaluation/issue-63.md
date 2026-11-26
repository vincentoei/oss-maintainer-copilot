# Issue #63: Qwen3.5 default-model evaluation

Status: **approved run complete; human report review pending**. Qwen3.5 matched
12/12 new synthetic expectations against 8/12 for both controls, but repeated
all three exposed bug-loss diagnostics. Keep the 3B default pending resolution
of the historical tradeoffs and semantic/usefulness review. [Full report](issue-63/report.md)
· [Offline scorecard](issue-63/scorecard.json).

| Acceptance area | Evidence / remaining limitations |
| --- | --- |
| Review and publish prior comparison | PR #64 merged as `28f3d36`, preserving frozen history. #62 resolution recorded and issue closed. Earlier measurements and expected outcomes unchanged. |
| Fresh cases and annotation rubric | All [twelve synthetic expectations](issue-63/proposed-cases.json) confirmed by the requesting user before inference. Four bugs, three regressions, three questions, one docs and one null. Rubric frozen in protocol; small designed cohort does not establish real-world generalization. |
| Frozen, approved requests and limits | [Protocol](issue-63/proposal.md), [freeze](issue-63/freeze.json), [actual user approval](issue-63/approval.json), [request hashes](issue-63/request-preview.json) and [pre-dispatch ledger](issue-63/run/reservations.jsonl). Exactly 55 calls; 1528/14,080 output tokens; no retries, repairs, warm-ups, model downloads, hosted calls or API fees. |
| Comparison and per-case changes | [Scorecard](issue-63/scorecard.json) preserves all denominators, statuses, confusion and paired changes. Fresh: candidate 12/12, controls 8/12; candidate gains three regressions and null, loses none. Exposed diagnostics: candidate 0/3 versus both controls 3/3; reported separately. No new fifty-case score. |
| Fresh human semantic/usefulness review | [Actual report sheets](issue-63/review/reports.md), fingerprints, rubric and pending attribution cover all 53 reports. Request sent to the user. **Unverified:** no actual human ratings received; no expected labels or agent inspection presented as human review. Promotion gate cannot pass yet. |
| Application and resources | Candidate passes all eight Python/API/browser/agent short/long reports, ten calls. All observations report 16K GPU placement; sampled peak candidate device use 4276 MiB. Empty-residency first-call model time 4.981 s; fresh median 487 ms. Long final prompt 4532 reported tokens. Physical tensor residency, absence of truncation, near-window behavior and model-driven search/inspect remain unverified here. Existing deterministic tests/simulations cover failure guards and unrelated behavior; no live failure was induced. |
| Preservation, tests, review and replay | [Preparation checks](issue-63/preparation-checks.json): 510 passed, two opt-in skips, Ruff/mypy and seven prior audits pass. Separate [preparation reviews](issue-63/preparation-review.md) have no remaining blockers. The new auditor reproduced all 53 full report/context objects and matched 55 charges without further inference. Final publication review is in progress; results and expected outcomes from earlier evaluations are preserved. |
| Recommendation and tradeoffs | [Decision rationale](issue-63/report.md): retain 3B for now; Qwen3.5 is a stronger classification candidate, but known historical losses and actual human review remain unresolved. Default unchanged. #63 remains open for report review and final disposition. |

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
override the later approval and measured results. Generated report ratings are
a separate step and remain pending.
