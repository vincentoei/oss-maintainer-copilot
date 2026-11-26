# Issue #60: semantic classification contract

[Issue #60](https://github.com/vincentoei/oss-maintainer-copilot/issues/60)
removes lexical restrictions from model classification. Expected-type availability
improves from **32/50 to 50/50**, but final Qwen type agreement stays **29/50**:
six gains and six regressions. This establishes a contract correction, not an
accuracy improvement or evidence for replacing the selected model.

The first implementation failed quote validation on nineteen cases. Its complete
negative result remains published alongside the corrected contract. The original
100-dispatch experiment was extended by a separately frozen 50-dispatch follow-up;
**150 local dispatches total**, no hosted calls. The follow-up was declared before
its inference, after inspecting the first candidate's failures. It is therefore
an iterative development result, not the originally planned untuned comparison.

## Acceptance evidence

| Acceptance criterion | Evidence and limits |
| --- | --- |
| Reproducible inference-free availability audit, verified openings, full denominator and flags | The actual encoder runs through `AvailabilityModel` without HTTP inference. Each phase preserves fifty `preflight` rows with cutoff, opening hash, pinned commit, offered labels, expected reachability and error flags. All fifty openings/evidence preflights passed in all three phases; zero changed/unavailable flags. Before: eighteen expected types unavailable, three additional wrong reachable selections. Final: zero unavailable, twenty-one wrong selections. The [offline verification](issue-60/verification.json) recomputes these counts. Expected labels remain reviewed annotations, not proven ground truth; no uncertainty was relabelled. |
| Every valid resolved-context type and abstention available without a lexical cue | [Model contract](../../src/maintainer_copilot/model.py) offers all context labels plus null independently of quote excerpts. [Public-boundary tests](../../tests/test_semantic_classification.py) cover all four reviewed paraphrases and a generic repository label whose cue never matches. Neither expected outcomes nor label cues select the excerpts. Availability does not count as prediction correctness. |
| Preserve label, quote, schema and citation guardrails; issue text remains untrusted | Strict structured output permits only a valid label/null, quote index/null and vetted citation IDs. Indices resolve to original issue text. Tests reject foreign labels, invented quotes, invalid/boolean indices, inconsistent null pairs, extra tool authority and unknown citations. Existing direct-client quote validation still rejects invented text. Reply statements and bounded tools remain server controlled. Semantic support is a model judgment; see the changed guarantee below. |
| Meaningful public model/triage/replay regressions and reviewed examples beyond fifty | [Four new synthetic expectations](issue-60/reviewed-examples.json) were explicitly confirmed by the requesting user: infrastructure, regression, selftests and docs. Each is exercised through fixed triage, actual bounded-agent final classification and historical replay; ambiguous null selection is covered through all three too. Existing replay tests retain misleading code/reference and injection cases. These are controlled simulated responses, not live-model generalization or human ratings of generated reports. No catalog answers were changed. |
| Frozen same-model comparison, budget, preservation, per-case outcomes and resources | [Original protocol](issue-60-protocol.md), [source freeze](issue-60/freeze.json), [follow-up protocol](issue-60-followup-protocol.md) and [follow-up freeze](issue-60/followup-freeze.json) preserve both the failed candidate and declared extension. Fifty cases per phase, fifty complete before/final pairs; [type changes](issue-60/type-changes.json) and all raw bounded outputs are retained. The audit verifies 434 prior files unchanged. Resources and remaining human review are reported below. |
| Fixed and agent policy agree; independent baseline/unrelated fields retained; checks and review | Both final classification paths use the shared model contract. All fifty final keyword-control scores equal before; missing details, duplicate candidates, related issues, documentation/source claims and CI results are equal field by field. Full suite: 499 passed, 2 opt-in live tests skipped. Ruff and mypy pass. [Checks](issue-60/checks.json) and separate [Standards/Spec reviews](issue-60/code-review.md) record evidence. No new live bounded-agent benchmark was run. |

## Contract and changed guarantee

The old encoder bound each permitted label to a quote matching a narrow lexical
cue. That prevented eighteen reviewed types from being selected. The initial
replacement allowed a label and freely generated exact quote, but the 3B model
often paraphrased the issue or copied a reply statement. Nineteen outputs were
correctly rejected; provenance validation was not relaxed to accommodate them.

The final encoder exposes all resolved-context labels and up to sixteen exact
issue excerpts of at most 160 characters, without associating labels with
excerpts. Long inputs are sampled evenly, including first and final excerpts;
the original full title/body remain present. The model selects a label and an
excerpt index. The client maps a valid index to its original quote and applies
the canonical label, exact-substring and citation validators. Invalid outputs
produce an explicit partial/failure path, not repaired predictions. Null type and
null index remain the explicit abstention form.

A valid quote now proves **provenance**, not semantic support for the label.
The former lexical/negation filter no longer gates model suggestions. A quote
may describe a negated hypothesis, a reference or code rather than the actual
problem; sampling can omit the best explanation. Those require semantic review.
The independent keyword model retains its original cue and negation checks.
Shared suggestion validation also stops imposing the lexical gate on the
experimental drafting path; this is not a drafting promotion or usefulness claim.

## Frozen experiment and results

All runs used `pytest-triage:coder3b-ctx16k`, Qwen2.5 Coder 3B Instruct,
GGUF Q4_K_M, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`.
Ollama reported version `0.40.16`, template SHA-256
`47fca52d970e517f889420240f615fa9f8f4c6e2cb062340b9dec6fe266385b5`.
Settings stayed at context 16,384, temperature 0, seed 42, top-k 20, top-p .8,
repeat penalty 1, at most 256 response tokens, 20-second timeout and 65,536
response bytes. No warm-ups, retries, repairs or model searches were used.
Each phase reserves dispatches durably before HTTP; all fifty requests in each
phase have a matching response record. Serving snapshots before and after each
phase match identity, template and settings.

| Metric (full fifty cases unless stated) | Before | Initial after: free quote | Final follow-up: indexed quote |
| --- | ---: | ---: | ---: |
| Expected labels reachable | 32/50 | 50/50 | 50/50 |
| Type agreement | 29/50 | 14/50 | 29/50 |
| Scored model reports | 50 | 31 | 50 |
| Validation/inference failures | 0 | 19 | 0 |
| Reports with null type | 6 | 19 | 0 |
| Partial reports | 4 | 21 | 4 |
| Requests | 50 | 50 | 50 |
| Input tokens | 81,934 | 76,707 | 96,216 |
| Output tokens | 1,287 | 3,061 | 1,680 |
| Mean replay latency, ms | 629.29 | 834.56 | 694.79 |
| p50 replay latency, ms (nearest rank) | 428.585 | 689.496 | 531.112 |
| p95 replay latency, ms (nearest rank) | 1,581.711 | 1,739.464 | 1,761.624 |
| Peak sampled device GPU use, MiB | 2,752 | 2,752 | 2,754 |

The first after phase has fifty recorded rows/dispatches but is correctly marked
`incomplete`: nineteen rejected responses have unscored fallbacks. Its stored
aggregate uses thirty-one successful reports; the 14/50 figure above retains the
catalog denominator. Its nineteen nulls are validation fallbacks, not evidence of
calibrated abstention. The final run's zero abstentions also does not establish
good uncertainty handling: twenty-one selected labels still disagree with the
reviewed expectations.

Before/final have fifty complete pairs. Gains: pytest #12146, #12219, #12249,
#12255, #12307, #12377. Regressions: #12189, #12228, #12278, #12298, #12328,
#12360. These identify issues in `pytest-dev/pytest`. The
[per-case table](issue-60/type-changes.json) retains expected labels, both
predictions, correctness, quotes and errors. No accepted outcome was edited.

Before/final missing-details exact agreement stays 43/50, duplicate retrieval
success stays 6/50, relationship judgment stays 2/47 evaluated relationships, and
automated citation validity stays 50/50. These are separate from semantic support
and reply usefulness. The offline audit compares the six unrelated report fields
and independent keyword scores directly, not just their aggregates.

Latency includes the frozen keyword control and model replay within each case;
it excludes evidence preflight and is not pure model latency. The first case of
each phase includes cold model loading. GPU use was sampled every 500 ms,
device-wide, including other processes; it is not a true peak or per-process
allocation. All samples reported without errors. Ollama's ending residency was
2,730,345,103 VRAM bytes at context 16,384 in all three phases. CPU/RAM, energy,
hardware ownership and total operating cost were not measured. Marginal model
API cost was US$0; local inference still consumes hardware and electricity.

## Artifacts, reproduction and limits

The three run directories preserve results, traces, request/response ledgers and
bounded raw outputs:

- [Before results](issue-60/before/results.json), source `1e4aec5`.
- [Failed initial after results](issue-60/after/results.json), source `2e3c785`.
- [Final follow-up results](issue-60/followup/results.json), source `8d52071`.

For a new experiment, check out the corresponding frozen implementation, supply
the same Ollama alias/settings and public evidence access, and use a new output
directory. The evaluator refuses an existing directory. Follow the matching
protocol and verify serving identity/settings before dispatch; historical
opening changes must be flagged. This command spends up to fifty local calls:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.classification_evaluation \
  --directory /tmp/issue60-new-comparison --phase after --ollama-url "$OLLAMA_URL"
```

Audit the saved evidence with **no network or inference**:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue60_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_verify.py
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue20_flash_verify.py
```

The older hosted auditors now check their recorded source against its frozen Git
commit, so the current implementation can evolve without changing any archived
results or source hashes. Run them from a clone containing those commits.

Fresh [reply review sheets](issue-60/review/human-review.md) hide the method and
include type/quote evidence for all 150 reports, including failed-call fallbacks.
[Usefulness ratings](issue-60/review/human-review.json) and
[semantic type/quote ratings](issue-60/review/classification-review.json) remain
pending; the [identity key](issue-60/review/review-key.json) binds each row to its
report fingerprint. Reviewers must inspect the original issue opening at its
recorded cutoff, not current comments or labels. Method hiding cannot guarantee
blindness because output style may reveal a phase. No earlier ratings were copied.

Unverified: fresh human report usefulness, semantic type/quote support and
abstention quality, held-out real-case generalization, a live agent comparison,
and production hosting/performance. Human report ratings have not been supplied;
the four confirmed synthetic expectations establish regression intent only.
The fifty historical cases were already exposed during development, and the
follow-up used observed contract failures. These limits prevent claiming an
unbiased quality improvement, even though the label-availability defect is fixed.
