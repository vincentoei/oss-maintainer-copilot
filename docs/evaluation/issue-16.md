# Issue #16: fixed RAG versus bounded agent

Decision: **retain the selected 3B model and fixed legacy application as the demo
default**. The bounded agent has zero paired exact-field gain, uses 2.29 times
the tokens, and produces two additional partial reports. Its p95 latency is
1.70 times fixed RAG. These observations fail the frozen promotion gates;
pending semantic/usefulness reviews cannot reverse those failed prerequisites.
The agent remains available as the existing optional workflow.

## Scope and freeze

Started from updated main `2e1da92edaedc280af8af099555714e5fed25136` on
`feat/issue-16-workflow-comparison`. Read AGENTS.md and the
[#50 retain-baseline decision](issue-50.md). Only #16 is implemented here.
The [comparison protocol](issue-16-protocol.md) and
[baseline manifest](issue-16-baseline.json) were committed in `11f9f0b` before
implementation or evaluation. Implementation and review corrections were frozen
at `7cfb2266d75a53708bd9e71cfe1930c74d8bf24c` before inference.
All 150 preserved baseline files and all 17 captured application source files
still match their respective hashes. No catalog case, previous evaluation
artifact, model file, legacy prompt/schema, or generation setting was retuned.
The only model-client change is an optional, default-off bounded response observer.

The single real-model run began 2026-11-24 08:42:41 UTC. All twenty cases passed
shared preflight, and all sixty case/workflow rows are retained. Each workflow
uses the same opening hash, cutoff, pinned repository SHA, eligible candidate
catalog, historical CI abstention, and existing field scorer. Both model arms
use the exact selected `pytest-triage:coder3b-ctx16k` digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`.

The agent can choose less evidence; this is the workflow difference being tested.
Historical documentation/template options now pass through the agent, while its
live defaults remain unchanged. Final selection prompts match on all twenty
F/A pairs; input/schema hashes match on nineteen. The exception is #12081,
where the agent finished without inspecting the supplied source line and hence
lacked the fixed workflow's source citation. That is an observed agent decision,
not unequal eligibility or post-cutoff evidence.

## Measurements

[results.json](issue-16/results.json) preserves each report, field score, trace,
order, content/provenance hashes, model calls and GPU samples.
[requests.jsonl](issue-16/requests.jsonl) is the durable pre-dispatch ledger;
[responses.jsonl](issue-16/responses.jsonl) retains all bounded raw provider
responses, parsed selections, tokens and timings. All 79 dispatches returned
provider responses. No transport failure, retry, warm-up, repair or second pass
occurred; unused budget does not authorize more inference.

| Measurement | Keyword rules | Fixed legacy RAG | Bounded agent |
| --- | ---: | ---: | ---: |
| Eligible / scored cases | 20 / 20 | 20 / 20 | 20 / 20 |
| Complete / partial reports | 20 / 0 | 19 / 1 | 17 / 3 |
| Issue-type exact agreement | 10/20 | 13/20 | 13/20 |
| Missing-detail exact agreement | 13/20 | 13/20 | 13/20 |
| Missing-detail macro precision / recall | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.65 |
| Expected-earlier-issue retrieval | 6/20 | 6/20 | 6/20 |
| Existing relationship exact score | 2/19 | 2/19 | 2/19 |
| Reports passing structural citation checks | 20/20 | 20/20 | 20/20 |
| Citation records checked / reports with citations | 15 / 11 | 15 / 11 | 14 / 11 |
| Issue-type abstention appropriateness | 18/20 | 17/20 | 17/20 |
| Duplicate abstention appropriateness | 19/20 | 19/20 | 18/20 |
| Model/action errors | 0 | 1 | 1 |
| Retrieval errors / explicit tool errors | 0 / 0 | 0 / 0 | 2 / 0 |
| Mean workflow latency | 3.04 ms | 881.47 ms | 1445.73 ms |
| Nearest-rank p50 latency | 2.618 ms | 615.599 ms | 1184.481 ms |
| Nearest-rank p95 latency | 4.940 ms | 919.453 ms | 1564.166 ms |
| Maximum latency | 8.573 ms | 5850.547 ms | 7090.693 ms |
| Inference dispatches | 0 | 20 | 59 |
| Input / output tokens | 0 / 0 | 34506 / 1255 | 80001 / 1927 |
| Device-wide sampled peak GPU use | 2742 MiB | 2742 MiB | 2742 MiB |
| Fresh human reply usefulness | unverified | unverified | unverified |

Twenty paired case scores: zero improvements, twenty unchanged, zero regressions
on the declared exact-field composite; mean agent-minus-fixed gain **0.0**.
The composite averages issue-type, missing-detail exactness and known relationship
correctness per case. No pair is missing. The two extra agent retrieval errors
and its duplicate-abstention regression are separately visible; the composite
does not include those fields and must not hide them.

These scores include partial/fallback reports; “scored” does not mean inference
or complete triage succeeded. Relationship uncertainty remains unscored on
#12083. The existing relationship metric requires retrieving the annotated
earlier issue even for a nonduplicate expectation; 2/19 is that exact contract,
not a general binary duplicate classifier accuracy. Precision defaults to one
on empty missing-detail predictions, so 1.00 precision is not perfect recall.
Additional retrieved issues remain unreviewed.
Nine reports per arm contain no citations and therefore pass the structural
check vacuously. The 20/20 structural rate does not establish useful evidence
coverage or semantic support.

Shared public evidence acquisition took 33.217 seconds before workflow timing.
The six arm permutations cycle in case order, reducing but not eliminating order
effects. Cold loads and provider prefix/KV caching are included; no warm-up was
used. Fixed #7312 includes the initial cold load. With twenty cases the p95 is
the nineteenth sorted latency and excludes the maximum. This single sequential
run is a laptop measurement, not a stable latency distribution or independence
claim. The twenty cases were already exposed during prior development.

The model and public GitHub marginal API charge is USD 0 for every arm. Agent
input plus output tokens total 81928 versus fixed's 35761, **2.291x**, with
39 extra dispatches. Electricity, hardware, hosting and network costs were not
measured and are not assigned zero total cost. GPU samples are device-wide:
keyword-rule rows observe the model already resident from other rows rather than
the rules allocating that memory. At 500 ms resolution, samples cannot prove
true peaks or per-process attribution.

Serving snapshots in results.json record Windows Ollama 0.40.16 reached from WSL
at `172.17.48.1:11434`, the exact 3B Q4_K_M identity/template/settings and final
residency. Context is 16384; temperature 0, seed 42, top-k 20, top-p 0.8 and
repeat penalty 1. Each action/report has 256 output tokens, 20-second timeout
and 65536 response-byte bound. Final residency reports size == size_vram ==
2730345103 bytes and context 16384. The server began with no resident model.

## Representative failures

All examples can be found by issue number and method in results.json. They are
observations against the frozen expected outcomes, not proposed fixes under #16.

| Case | Preserved failure evidence |
| --- | --- |
| #7312 | All arms retrieve the expected earlier issue but classify it as related; the human-reviewed expectation is duplicate candidate. |
| #10156 | Expected type is docs; keyword rules choose infrastructure and both model workflows choose question. The annotated earlier issue is not retrieved. |
| #12072 | All arms request none of the three expected missing details. The case uses the generic historical template profile; live structured-template assumptions cannot be substituted. |
| #12083 | Expected regression is reported as bug; pip-list request is absent. The uncertain relationship remains unscored, and the expected duplicate abstention is absent. |
| #12081 | Agent searches then finishes without inspect_source. Final report records source_claims abstention and a retrieval error; fixed workflow includes the verified source. |
| #12204 | Full legacy opening is retained and model inference succeeds. Agent immediately finishes without searching, producing duplicate/related abstentions and get_issue retrieval error. The fixed workflow completes. This case was over the separate #50 drafting packet bound; that experiment's exclusion is not inherited here. |
| #12216 | Both real-model workflows return JSON selections rejected by existing validation, retaining partial reports and type abstention. Raw outputs, usage and validation-error traces are retained without retry. |

## Frozen decision gates

| Gate | Observed outcome |
| --- | --- |
| Twenty complete pairs / no additional errors | Fail: fixed has 1 partial, agent 3; two additional agent retrieval failures. |
| Paired exact-field gain >=0.05 | Fail: 0.0. |
| No field drop >0.05 / no lower structural validity | Pass for the declared type/detail/relationship/citation fields; duplicate abstention regresses separately by 0.05. |
| Agent p95 <=80 seconds and <=2x fixed | Pass: 1.564 seconds, 1.701x. |
| Agent tokens <=2x fixed | Fail: 2.291x. |
| Full GPU residency, context 16384 / sampled peak <=7680 MiB | Pass at recorded sampling resolution; final residency and 2742 MiB samples retained. |
| Fresh human usefulness gain >=0.2 and no extra unsupported claims | Unverified: no fresh explicit ratings for these outputs. |

The failed quality, completeness/error and token gates independently prevent
promotion. Keep fixed legacy as the demo workflow. Human review is still needed
to characterize actual usefulness and semantic support; no favorable human
result is inferred from exact scores, citation structure, or older ratings.

## Acceptance evidence

| Issue #16 acceptance criterion | Evidence and status |
| --- | --- |
| Same eligible cases, cutoffs, scorer and documented settings | Verified for all twenty: shared successful preflight, per-row matching opening/cutoff/commit, frozen successful and failed evidence reads, common candidate numbers, legacy score_report, serving snapshots and protocol settings. Source/cutoff and eligibility regressions run at both agreed public boundaries. Offline verification recomputes all sixty scores. |
| Field quality, citations, abstention, latency, errors, cost and representative failures | Automated measurements complete: table above, complete per-case reports/traces, 79 request/raw-response pairs, resource samples, cost scope and examples. Semantic citation support, reply usefulness, redundancy, uncertain/extra relationships and non-exact abstention judgments remain unverified because no fresh explicit human reviews were supplied for these new outputs. |
| Consider agent latency/cost against quality before keeping final demo workflow | Complete retain decision: zero paired exact-field gain, 1.701x p95, 2.291x tokens and two extra partial reports fail predeclared gates. Selected 3B and fixed legacy remain default; no promotion or UI change. This is not a claim that the legacy replies are useful. |

The shuffled [fresh reply sheet](issue-16/human-review.md), pending
[review records](issue-16/human-review.json) and separate
[identity key](issue-16/review-key.json) cover all sixty outputs with report
fingerprints. No old #48/#50 rating was transferred, and no human label was
invented. The missing human evidence limits semantic claims; it does not block
the conservative retain decision because other required gates already fail.

## Verification

[checks.json](issue-16/checks.json): Ruff lint and formatting pass, strict mypy
passes, and the full suite passes **293 tests, 2 skipped**. The skipped tests are
the existing opt-in live replay tests; this comparison separately performed the
real twenty-case preflight and all model dispatches. Focused public runner,
replay, agent and model checks ran during implementation, including red/green
regressions for the new interface, persistent budget, unavailable pinned evidence,
malformed raw response retention and missing residency metadata.

The [offline verification](issue-16/verification.json), reproduced with
`PYTHONPATH=src python scripts/issue16_verify.py`, confirms baseline/source/catalog/
protocol hashes, all sixty rows/scores, exact request-response accounting,
per-case/arm budgets, complete raw response fingerprints, GPU sample counts and
sixty fingerprint-matched pending reviews. It performs no network or inference.
The [two-axis code review](issue-16-code-review.md) records corrected findings
and the nonblocking fixed-arm mapping judgment. No runtime source changed after
the inference freeze.
