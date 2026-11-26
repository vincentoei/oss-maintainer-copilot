# Issue #63: Qwen3.5 default-model evaluation

Status: **prepared, awaiting execution approval**. No #63 model calls or quality
measurements have been made. The current application default remains 3B.

The user confirmed all [twelve new synthetic expectations](issue-63/proposed-cases.json)
in three explicit batch replies. They are designed diagnostic cases, not unseen
real-world generalization evidence. The [protocol](issue-63/proposal.md) proposes
three fixed-workflow arms plus candidate-only application integration, with a
maximum **55 local calls / 14,080 output tokens**, no model downloads, hosted calls,
retries or API fees. [Request preview](issue-63/request-preview.json) ·
[Read-only serving inspection](issue-63/serving-inspection.json).

| Acceptance area | Preparation evidence / outstanding work |
| --- | --- |
| Publish reviewed prior comparison | PR #64 merged as `28f3d36`, preserving frozen history; #62 resolution recorded and issue closed. Original measurements and expected outcomes unchanged. |
| Fresh cases and annotation rubric | Twelve proposed types confirmed by the requesting user before inference; rubric recorded in protocol. Four bugs, three regressions, three questions, one docs case and one null. |
| Frozen, approved requests and limits | All 55 request hashes captured without inference, including actual browser/API paths. Final committed freeze and explicit execution approval are required before dispatch. |
| Measured comparison and per-case changes | Not yet run. Three exposed bug-loss diagnostics are separate from the twelve fresh synthetic cases. No new fifty-case score is planned. |
| Human semantic/usefulness review | Not yet available: actual generated reports do not exist. The auditor can generate method-hidden sheets keyed to report fingerprints after execution. |
| Application and resource checks | Opt-in `MODEL_REASONING_EFFORT=none` reaches fixed, agent planning and agent final calls; unset preserves the previous payload. Controlled simulation covers Python, HTTP, browser and finish-to-report agent paths. Live compatibility, cold/long-input behavior and measurements await approval. Search/inspect transitions are covered by existing deterministic tests, not this integration set. |
| Preservation, checks, review and audit | [Checks](issue-63/preparation-checks.json): 510 passed, 2 opt-in skips; Ruff/mypy and seven earlier audits pass. All 53 simulated reports replayed; accounting/tamper/late-worker fault checks passed. Separate [reviews](issue-63/preparation-review.md) found no remaining blockers before freeze. |
| Promote/retain decision | Pending actual outcomes and actual human report ratings. The historical 38/50 score does not authorize promotion. |

To reproduce the request capture with simulated model responses (no model calls):

```sh
PYTHONPATH=src .venv/bin/python scripts/issue63_prepare.py
```

The preparation requires the retained, hash-verified historical snapshot and
pinned local browser tooling. It starts a temporary loopback application and
browser, and injects simulated responses at the model boundary. Source/config
and protocol must be committed cleanly before generating the separate freeze.

The live entry point refuses execution without a committed approval record
matching the exact freeze and numeric limits. After an approved run, audit its
ledger, responses, reports, placement and scores without model inference:

```sh
PYTHONPATH=src .venv/bin/python scripts/issue63_results.py
```

Cold model residency, native cache counts and sampled device memory have the
limits stated in the protocol. Neither valid JSON nor an exact quote establishes
semantic correctness. Missing data or human ratings cannot pass adoption gates.
