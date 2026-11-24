# Issue #17: thirty reviewed evaluation cases

The catalog now contains **30 reviewed cases across 28 issue families**. All ten
new cases passed live replay preflight. The single comparison retained all
90 case/workflow rows: **29 eligible cases per workflow**, with existing #12204
flagged consistently because its opening exceeds the current 16,000-character
application limit. No opening was truncated and no replacement case was used.
The fixed legacy workflow and selected 3B model remain the demo default.

The [small replay follow-up](issue-17/follow-up/README.md) restores replay of the
full #12204 opening while keeping live request limits unchanged. The recorded
model comparison below remains the original pre-fix run with 29 eligible cases;
its scores and dispatch records have not been replaced by controlled replays.

## Acceptance evidence

| Acceptance criterion | Evidence and status |
| --- | --- |
| Ten new cases have human-confirmed outcomes and complete replay metadata, with issue-family partition checks | Complete on the explicitly authorized delegated basis: the user chose “Delegate case review to Codex and accept its confirmation.” [Case review](cases-twenty-one-through-thirty.md) records all ten judgments and ambiguities; each JSON case names that attribution and its confirmation time. This is assistant review accepted by the user, not independent human assessment. [Provenance](issue-17/provenance.json) verifies seventeen distinct opening versions against REST/GraphQL, unedited status, exact hashes, ten pre-cutoff commits and both pinned templates per revision. [Partition manifest](issue-17/partitions.json) and [metadata checks](issue-17/metadata-checks.json) cover 28 families/35 members with no conflicting family assignment or recorded training overlap. Future/external training data remains unverified because no training corpus exists yet. |
| Expanded set preserves duplicate, nonduplicate, missing-detail and ambiguous coverage | Complete: 5 duplicate-candidate, 23 nonduplicate and 2 uncertain relationships; cases with and without missing details. New cases add one duplicate candidate, eight nonduplicates and one uncertain relationship. #12263/#12273 share a failure; #12278 is conservatively grouped with them for training exclusion while retaining uncertain scoring. Catalog coverage and shared-family assertions pass through the agreed replay seam. |
| All workflows rerun on eligible cases and updated results identify changed cases and scores | Complete for all 29 eligible cases, including every addition: keyword rules, fixed legacy RAG and bounded agent. [Run results](issue-17/run/results.json) preserve all 90 rows, preflight flags, reports, scores and traces. [Comparison](issue-17/comparison.json) separates previous twenty, rerun original twenty, new ten and expanded thirty, with per-field before/after values and candidate changes. [Offline verification](issue-17/verification.json) recomputes all 87 available scores and accounts for all 115 request/response pairs. #12204 is explicitly unverified as a successful replay under current main; its three flagged rows have no model dispatch or score. |

## Reproducible scope and freeze

Started from updated main `1bec247b9e13d18a265610c99f0778ef13f176bf`, branch
`feat/issue-17-thirty-cases`; only #17 is addressed. The implementation, ten cases,
review attribution and [protocol](issue-17-protocol.md) were committed at
`8640bae` before inference. All 204 original evaluation/case files still match
[baseline hashes](issue-17/baseline.json). No previous expected outcome, result,
raw response, human rating or protocol was rewritten.

The shared preflight began **2026-11-24 11:16:42 UTC**, taking 49.337 seconds.
The run froze the 30-case catalog and all 21 application source hashes before
inference; verification checks those files at the original `8640bae` freeze. The
runner adds an explicit `--issue 17` mode and thirty-case budget; default
`--issue 16` selects the original twenty cases. Legacy prompts, retrieval,
scoring, template rules and generation settings were not tuned for the additions.

Every workflow uses the same verified opening, cutoff, pinned commit, eligible
candidate catalog and historical CI abstention. Shared failures stay shared;
agent choices can consume less evidence. Later comments were consulted only for
annotation, never passed as replay evidence. Full issue bodies remain on GitHub.
The run preserves full openings and does not bypass application validation.
The current input bound was introduced before this branch; #16's earlier run
could score #12204, but the present application rejects that opening.

## Updated measurements

The selected model is `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`, Q4_K_M.
[Serving precheck](issue-17/serving-before.json) and run serving snapshots verify
16K context, temperature 0, seed 42, top-k 20, top-p 0.8 and repeat penalty 1.
Output is capped at 256 tokens, client timeout 20 seconds, response bound 65536
bytes. Windows Ollama 0.40.16 was reached from WSL at `172.17.48.1:11434`.
The server began without a resident model; final residency confirms context
16384 and size == size_vram == 2730345103 bytes.

| Measurement | Keyword rules | Fixed legacy RAG | Bounded agent |
| --- | ---: | ---: | ---: |
| Catalog / eligible / scored cases | 30 / 29 / 29 | 30 / 29 / 29 | 30 / 29 / 29 |
| Complete / partial / flagged rows | 27 / 2 / 1 | 26 / 3 / 1 | 25 / 4 / 1 |
| Issue-type exact agreement | 12/29 | 16/29 | 16/29 |
| Missing-detail exact agreement | 14/29 | 14/29 | 14/29 |
| Missing-detail macro precision / recall | 0.937 / 0.586 | 0.937 / 0.586 | 0.937 / 0.586 |
| Expected-earlier-issue retrieval | 6/29 | 6/29 | 5/29 |
| Existing relationship exact score | 2/27 | 2/27 | 2/27 |
| Reports passing structural citation checks | 29/29 | 29/29 | 29/29 |
| Citation records / reports with citations | 20 / 13 | 20 / 13 | 18 / 13 |
| Issue-type abstention appropriateness | 27/29 | 26/29 | 26/29 |
| Duplicate abstention appropriateness | 27/29 | 27/29 | 26/29 |
| Inference dispatches | 0 | 29 | 86 |
| Input / output tokens | 0 / 0 | 36511 / 1794 | 95474 / 2777 |
| Model errors | 0 | 1 | 1 |
| Mean latency (ms) | 3.43 | 736.39 | 1152.55 |
| Nearest-rank p50 / p95 latency (ms) | 3.105 / 7.630 | 601.867 / 1916.519 | 1090.433 / 2049.266 |
| Maximum latency (ms) | 8.959 | 4042.087 | 2568.419 |
| Device-wide sampled GPU peak (MiB) | 2742 | 2742 | 2742 |
| Fresh human reply usefulness / semantic support | unverified | unverified | unverified |

Scores include partial/fallback reports. The aggregate's `completed` field means
scoreable reports, not complete application status; the table separates them.
The two uncertain relationships remain unscored. The existing relationship
metric requires retrieving the annotated earlier issue even for nonduplicates;
2/27 is not general binary duplicate accuracy. Missing-detail precision uses one
for empty predictions; it must be read with recall. Sixteen reports per workflow
have no citations and pass structural citation checks vacuously; 29/29 does not
establish semantic support or useful evidence coverage.

Latency means and quantiles use all thirty retained rows, including the flagged
row's near-zero workflow timing. Public evidence acquisition is excluded. The
six workflow order permutations cycle in case order; cold loads/provider caching
are included, with no warm-up. This is one sequential laptop run, not a stable
latency distribution. GPU samples are device-wide and cannot establish true
peaks or per-process allocation; keyword rows observe the model resident from
other rows. Marginal local model/GitHub API charges are USD 0; hardware,
electricity, network and hosting costs were not measured.

The [durable dispatch ledger](issue-17/run/requests.jsonl) and
[bounded raw responses](issue-17/run/responses.jsonl) preserve **115 actual
calls**, within the frozen 150 cap: 29 fixed and 86 agent. Every dispatch has a
provider response, usage and raw-response fingerprint. There was no retry,
repair, warm-up or second inference pass. Agent tokens total 98251 versus fixed
38305 (**2.565x**), with 57 extra calls and zero paired exact-field gain across
29 pairs. Its p95 is 1.069x fixed. The expansion supplies no basis to promote it.

## Changes on the original twenty

[Per-case comparison](issue-17/comparison.json) identifies **two changed cases
across four workflow rows**:

- **#12204, all three workflows:** previously scored, now excluded in shared
  preflight by the current application body bound. Its scores are null, and no
  inference was dispatched. The original expected outcome and opening hash remain
  unchanged. The follow-up fixes the historical replay limit separately; the
  archived comparison retains its original exclusion.
- **#12081, bounded agent:** previously retrieved #3448, now finishes without
  searching or inspecting source. The report loses the earlier-issue citation and
  adds duplicate/related abstentions. Expected-earlier retrieval changes true to
  false; duplicate-abstention appropriateness changes true to false. The exact
  relationship judgment remains false in both runs. Fixed and keyword scores are
  unchanged for this case.

All other original-case field scores are unchanged. Adding the paired earlier
issue #478 introduces one additional eligible candidate to every original case;
the comparison records that change even when field scores stay the same. Code
merged between #16 and this branch, eligible-pool differences and provider
behavior prevent attributing the #12081 change solely to case expansion.

| Subset | Keyword type / details | Fixed type / details | Agent type / details |
| --- | ---: | ---: | ---: |
| Previous twenty (#16) | 10/20 / 13/20 | 13/20 / 13/20 | 13/20 / 13/20 |
| Rerun original twenty (19 eligible) | 9/19 / 12/19 | 12/19 / 12/19 | 12/19 / 12/19 |
| New ten | 3/10 / 2/10 | 4/10 / 2/10 | 4/10 / 2/10 |
| Expanded thirty (29 eligible) | 12/29 / 14/29 | 16/29 / 14/29 | 16/29 / 14/29 |

These are distinct denominators, not a paired improvement claim. On the nineteen
mutually eligible original cases, exact type/detail/relationship correctness
remains unchanged. The changed eligibility and retrieval/abstention behavior are
reported separately rather than hidden by the exact-field composite.

## Failures exposed by the additions

- **#12231:** the reviewed feature opening explicitly supplies an alternative
  (dropping `-rx`), but all arms still request alternative solutions.
- **#12242:** the supplied package graph is not recognized; all arms request a
  package list and suggest bug rather than the reviewed question type.
- **#12249:** all arms suggest deprecation rather than the reviewed bug type and
  request none of the three expected missing details.
- **#12255:** all arms suggest bug rather than the reviewed enhancement and omit
  the expected alternatives request. It is a hard topical negative against
  #12204's growing cached traceback.
- **#12263/#12273:** all arms suggest bug rather than regression and fail to
  request the expected environment/reproducer details. The #12273 duplicate is
  not retrieved despite the earlier opening being eligible.
- **#12278:** all arms abstain on type, matching the reviewed unknown type, but
  omit missing environment/reproducer requests and the expected uncertain
  duplicate abstention.
- **#12287:** all arms choose bug rather than the accepted question interpretation;
  the review records that type ambiguity explicitly.
- **#12290:** the model arms correctly choose enhancement but request a real-world
  use case already supplied by evening readability. Keyword rules choose docs.

Both #12249 and #12255 contain linked PRs. Historical CI is intentionally
unavailable, producing partial status for every workflow on those cases. These
are retained abstentions, not live CI lookups or transport failures. Existing
#12216 still produces rejected model selections in both model arms, with raw
responses retained. No failure triggered prompt, retrieval or expected-outcome
changes after the run.

## Verification and remaining review

[Checks](issue-17/checks.json) record Ruff lint/formatting, strict mypy and the
full suite: **349 passed, 2 skipped**. The existing opt-in live replay tests are
skipped; this task separately performed all thirty live preflights and the real
three-workflow run. The first full suite attempt stalled in the sandbox and was
terminated; [that attempt](issue-17/checks-sandbox-attempt.json) is not counted as
a passing check. The successful full run was outside the sandbox. Focused
replay/evaluation/runner tests ran during the red/green changes.

Run `PYTHONPATH=src .venv/bin/python scripts/issue17_verify.py` without network or
inference to check all 204 preserved files, catalog/protocol hashes and application
hashes at the original `8640bae` inference commit (which must be present in Git),
provenance links/template hashes, family assignments, candidate cutoffs, ninety
rows, 115 dispatch/response records and 87 recomputed scores. It also regenerates
the before/after comparison from preserved artifacts.

The [fresh review sheet](issue-17/run/human-review.md),
[pending records](issue-17/run/human-review.json) and separate
[identity key](issue-17/run/review-key.json) cover all ninety rows with report
fingerprints: 87 available reports and three flagged/unavailable rows. Semantic
citation support, fresh reply usefulness and unannotated retrieved relationships
remain unverified because no fresh report ratings were supplied. Case review
was authorized separately and does not supply those ratings. No old ratings
were transferred. Future/external training partition integrity also awaits an
actual training corpus. The [two-axis code review](issue-17-code-review.md)
records Standards and Spec findings separately.
