# Issue #48: diagnosis and bounded triage fixes

[Issue #48](https://github.com/vincentoei/oss-maintainer-copilot/issues/48)
started on updated `main` at `04755b8d2a8db6d6a1ccb326bee965439c2d70db`,
on `fix/issue-48-triage-failures`. The [twenty-case diagnosis](issue-48-diagnosis.md)
and [before isolation](issue-48-isolation-before.json) preceded application edits.
The original #12–#15/#21/#45 evidence, expected outcomes, case metadata and model
file remain unchanged; the [manifest](issue-48-provenance.json) verifies 72 files,
including the #45 results hash specified in the issue.

The final [real run](issue-48-results.json) removes all six redundant requests in
five targeted reports, retains substantive explanations instead of generic word
overlap, and includes three supported investigative questions. This is a bounded
application improvement, not evidence of better model reasoning. Substantial
limitations remain: known-earlier-issue retrieval and the existing relationship
score regress, four known duplicate leads remain classified as related, and many
replies still abstain without useful guidance. **Fresh human usefulness review is
pending**, so no human-quality improvement is claimed.

## Cause and changes

- Package tables now supply package information independently of an exact heading.
  Concrete path-testing, test-dependency, Bash/CI and configuration-documentation
  scenarios supply use cases. Current copied `skipif` tests supply a workaround,
  including the observed phrase “making use of the”. Empty/placeholder content and
  genuinely absent alternatives still receive requests. These are bounded English
  rules, not a general semantic completeness classifier.
- Relationship assessment requires an identified behavior or strong matching title,
  with excerpts from both reports and relevant differences where supported. Hidden
  comments and common built-in exception names cannot establish relationships.
  The fixture-derived-parameter, readouterr, custom-debugger, import-failure,
  argument-file and module-hook connections use opening evidence only. The model
  receives these vetted statements; it still does not assess full candidate bodies.
  Unsupported connections are omitted. Six suggestions replace 45, but omission
  alone is not confirmation that a relationship is irrelevant.
- Opening-supported questions compare #12146's scenarios without version/value
  confounders, clarify #12204's package/session version mismatch, and ask #12219
  for a minimized *failing* project example. Intentional version comparisons,
  negated/uncertain success, questions, and success in a different clause abstain.
  No root cause, supported API or external project behavior is invented.

The JSON `ModelSuggestion` schema is unchanged. The **meaning of required reply
IDs is strengthened**: a vetted investigative question joins missing-detail
requests. Initial real inference showed #12219's question was available but omitted;
prioritizing questions in the prompt alone still omitted it. Requiring the vetted
question corrects that application-selection failure. Public fixed/bounded API
checks verify that omission, unknown IDs and added free-text diagnoses fail
validation and yield partial reports. No failure is converted into a successful
selection. The question is optional to construct: insufficient or contradictory
evidence produces no question to require.

The submitted opening can now be cited at its own issue URL. Historical replay
verifies that opening's hash/cutoff before construction. Structural scoring permits
that verified opening while still rejecting newer/unverified URLs; self-duplicates
remain excluded. This is an added evidence source, not semantic citation approval.
Model type/quote checks, unsupported-claim rejection, four-call agent limit, tool
output limits, read-only boundaries and partial-report behavior remain in place.

Source and script hashes are in the [manifest](issue-48-provenance.json). The model
client hash covers the prompt change and generalized required-statement error;
weights and generation settings did not change. The agent implementation is
unchanged. No training, paid API, evaluation-set expansion, #16 workflow comparison
or #33 second-repository work is included.

## Final measured results

All twenty original openings, eligible catalog issues and pinned repository
artifacts passed content/cutoff verification. No changed content was silently
substituted or truncated. There were twenty real responses: 19 complete reports
and one partial report. “Completed” in the field scorer includes that partial
scoreable report and does not mean the model selection passed validation.

| Field | Preserved #45 run | Final #48 run |
| --- | ---: | ---: |
| Missing-detail exact agreement | 8/20 (0.400) | 13/20 (0.650) |
| Missing-detail macro precision | 0.825 | 1.000 |
| Missing-detail macro recall | 0.650 | 0.650 |
| Issue-type agreement | 13/20 (0.650) | 13/20 (0.650) |
| Known-earlier-issue retrieval recall | 0.600 | 0.300 |
| Existing duplicate/nonduplicate exact score | 8/19 (0.421) | 2/19 (0.105) |
| Structural citation validity | 1.000 | 1.000 |
| Type / duplicate abstention appropriateness | 0.850 / 0.950 | 0.850 / 0.950 |
| Model validation failures | 1 | 1 |
| Transport / integrity / scoring errors | 0 / 0 / 0 | 0 / 0 / 0 |
| Human usefulness | 0 useful, 5 partly, 15 not | 20 pending |

The existing retrieval metric includes curated nonduplicate pairs. Six such
previously surfaced pairs are now withheld, reducing recall and exact judgment
scores. The scorer treats `not_retrieved` as incorrect for these nonduplicate
pairs; it has **not** been changed to make these scores look better. All four
confirmed duplicate leads are still surfaced, but all four remain related rather
than duplicate candidates, as before. Relationship interpretation beyond the
original expected pairs remains pending independent review. Conservative filtering
trades coverage for fewer unsubstantiated suggestions; these numbers do not prove
that every removed suggestion was noise.

#12216 still returns an unsupported bug-label quote. Validation rejects it and
keeps a partial report and explicit abstention. The report renderer passes the
rejection through. That remains an unresolved model-choice failure.

| Case | Observed final application change | Fresh human delta |
| --- | --- | --- |
| #7312 | #349 connection explained; #2959/#7012 removed; still related, not duplicate | Pending |
| #10156 | Weak fixture-overlap suggestions removed; contribution guidance still absent | Pending |
| #12053 | Only debugger connection retained and differentiated from CLI-help request | Pending |
| #12072 | Specific import failure explained; still related; missing-detail template gap remains | Pending |
| #12079 | Supplied use case no longer requested; absent alternative still requested; model still omits #11871 in draft | Pending |
| #12081 | readouterr connection explained; documentation/source wording still general | Pending |
| #12083 | No fabricated version conflict; still abstains without targeted guidance | Pending |
| #12116 | Supplied package table no longer requested; still lacks multiprocessing contribution guidance | Pending |
| #12146 | Required same-version/same-tuple comparison included | Pending |
| #12189 | Unsubstantiated capture suggestions removed; still lacks targeted JUnit investigation | Pending |
| #12197 | Weak configuration-topic suggestions removed; supported ini behavior still unresolved | Pending |
| #12201 | Supplied path-testing use case and copied-test workaround no longer requested; otherwise abstains | Pending |
| #12203 | Generic minimal-example request retained; targeted logging example still not supplied | Pending |
| #12204 | Required conflicting pytest/pluggy version clarification included | Pending |
| #12216 | Invalid type selection still rejected; partial fallback remains | Pending |
| #12219 | Required minimized failing example request included; issue type still mismatches expected bug | Pending |
| #12223 | Generic assertion/JUnit overlap removed; requested XML change still unresolved | Pending |
| #12224 | Misleading #11871 argument-file link removed; no verified lifecycle API recommendation | Pending |
| #12226 | Bash/CI use case no longer requested; absent alternative still requested | Pending |
| #12228 | Concrete documentation use case no longer requested; alternative request retained for unchanged expected outcome, usefulness disputed | Pending |

The [review presentation](issue-48-human-review.md) contains all twenty final
replies with before replies/ratings/reasons, opening links, cutoffs, pinned commits,
relationship reasons and citations. The [fresh review record](issue-48-human-review.json)
fingerprints each exact report and draft; all new ratings are null pending explicit
review. Original ratings are not transferred. Citation support, separate
relationship labels and other-field abstention judgments remain separately pending.
The user has been asked to rate all twenty using the same rubric. **Next human
action:** provide a usefulness rating and reason for each final reply; unsure stays
pending. Only then can human improvements, unchanged failures and regressions be
reported. These development-informed twenty cases are regression evidence, not an
independent generalization test. No maintainer-time-saved claim is made.

## Serving, latency and measurement limits

Windows Ollama 0.40.16 served `pytest-triage:coder3b-ctx16k` to the WSL application
at `http://172.17.48.1:11434/v1`. WSL's default route was that Windows address;
WSL localhost was unreachable. Exact serving verification and final residency are
in [serving](issue-48-serving-required.json) and [results](issue-48-results.json).
The digest is `3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Qwen2.5-Coder-3B-Instruct Q4_K_M. Context 16,384, temperature 0, seed 42, top-k 20,
top-p 0.8, repeat penalty 1, report limit 256 tokens and client timeout 20 seconds
match the baseline. Final `/api/ps` shows context 16,384 and equal size/size_vram.

| Observation | #45 | Final #48 |
| --- | ---: | ---: |
| Mean model-call latency (ms) | 842.201 | 572.376 |
| Median / P95 / maximum model latency (ms) | 692.988 / 1,103.751 / 3,547.650 | 605.855 / 771.284 / 776.341 |
| Mean end-to-end replay latency (ms) | 932.240 | 668.050 |
| Total input / output tokens | 36,228 / 1,356 | 34,506 / 1,246 |
| Maximum input tokens | 14,487 | 14,485 |
| Peak sampled device memory (MiB) | 2,740 | 2,742 |

P95 uses nearest rank over twenty serial calls. GPU memory was sampled every
500 ms and includes other processes; it can miss brief peaks. The GPU has 8,151 MiB
and driver 592.01. Repeated runs warm caches and model residency; laptop conditions
changed, so the lower latency is **not** a causal speedup claim. Local inference
API cost is zero, excluding hardware, power and network costs.

The [initial warm-up failure](issue-48-live-failure.json) is preserved separately:
CUDA allocation failed before scored inference while Windows had about 1.1 GiB
free RAM and GPU memory appeared idle. After the user closed applications,
Windows free RAM was about 5.6 GiB and the unchanged model loaded successfully.
This is an observed recovery, not proof of the allocator's underlying cause.
[Initial results](issue-48-initial-results.json) contain no quality scores.
The [first real run](issue-48-first-inference-results.json) exposed the missed
article in #12201; the [prompt-only run](issue-48-prompt-only-results.json) corrected
that parser gap but still omitted #12219's question. Neither run's pending review
companions supplies final ratings. All raw responses and traces are retained.

## Public interfaces and verification

Final deterministic checks: **254 passed, 2 optional live tests skipped**; strict
mypy checks 29 source/test files; Ruff lint and format pass. Skips are not counted
as live successes. Regression checks reach `POST /api/triage`,
`POST /api/agent/triage`, and the public replay/scorer. Targeted failures were
observed before their fixes, including already-supplied packages/scenarios,
misleading overlap, missing next-step choices, intentional version comparisons,
negated/cross-clause evidence, generic exception overlap, hidden comments, and
required-question omission. Existing injection/tool-limit/partial tests still pass. The preserved
[archived-baseline replay](issue-48-red-before.txt) shows twenty representative
regressions failing on pristine base source; the same checks
[pass on final source](issue-48-green-after.txt). This supplements the original
red-before-fix observations, rather than claiming the final test file existed
before diagnosis.

The [real HTTP integration](issue-48-api.json) contains eight passing requests,
covering both APIs for #12116, #12146, #12219 and #12224. Each has matching trace,
real usage, report, raw model responses and call-limit assertions. The
[browser record](issue-48-web.json) and [report-only screenshot](issue-48-web.png)
show #12219's targeted question rendered unchanged, real token-bearing model calls,
one read-only issue-search tool, and no JavaScript errors. Chromium 159.0.8154.6
needed the previous evaluation's local library path after its initial missing-library
launch failure. The screenshot was inspected; it excludes the pasted full opening.

These focused API/web checks use the original verified openings and frozen
eligible catalog candidate source with real inference. They use the ordinary live
documentation source, unlike the separately pinned historical evaluation. They
are integration checks, not additional historical-quality samples or the #16
workflow comparison. Broader live GitHub search behavior is unchanged/unmeasured.

[Two-axis code review](issue-48-code-review.md) reported evidence-negation, generic-exception, hidden-comment,
cross-clause and invented-earlier-request defects. Public red-green regressions
lock down the corrections. Both reviewers verified their findings resolved. The
final required-question contract is covered by public omission/rejection checks;
no validation was bypassed. The [diagnosis](issue-48-diagnosis.md) records remaining
class-specific causes and blockers, especially template selection and missing
verified guidance for specialized requests.

## Reproduction

From the WSL application shell, keep the same Windows Ollama server running and
use a new output path for every attempt:

```bash
export GITHUB_TOKEN="$(gh auth token)"
UV_CACHE_DIR=/tmp/issue-48-uv-cache uv run --locked --no-env-file \
  python scripts/issue48_evaluate.py \
  --ollama-url http://172.17.48.1:11434 \
  --output /tmp/issue48-new-results.json \
  --serving-output /tmp/issue48-new-serving.json
UV_CACHE_DIR=/tmp/issue-48-uv-cache uv run --locked --no-env-file \
  python scripts/issue48_isolate.py --output /tmp/issue48-new-isolation.json
UV_CACHE_DIR=/tmp/issue-48-uv-cache uv run --locked --no-env-file \
  python scripts/issue48_review.py --results /tmp/issue48-new-results.json \
  --review-json /tmp/issue48-new-review.json \
  --presentation /tmp/issue48-new-review.md
```

`issue48_evaluate.py` refuses a changed digest/quantization/alias parameter set;
all runners refuse existing artifact paths. Rediscover the Windows address after a
WSL restart. For focused API/web reproduction, acquire the original public issue
records into a temporary JSON mapping keyed by number (all case and earlier-issue
numbers in the catalog), then use `issue48_serve.py --openings <temporary-file>
--calls <new-ledger> --ollama-url <verified-url>`. It verifies all content hashes and
cutoffs before serving. `issue48_api.py --openings <temporary-file> --calls
<same-ledger> --output <new-artifact>` checks both APIs. `issue48_browser.cjs
<temporary-file> <new-output-prefix>` uses `PLAYWRIGHT_MODULE`, `CHROMIUM_PATH`,
`MODEL_CALLS_PATH` and any required `LD_LIBRARY_PATH`; it produces JSON and a
report-only screenshot. Full contributor bodies remain outside the repository.
