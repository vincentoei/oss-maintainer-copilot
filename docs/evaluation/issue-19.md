# Issue #19: final fifty-case comparison

The benchmark now contains **50 confirmed cases across 46 issue families**.
All fifty passed live evidence preflight. The final comparison retained and
scored all **150 case/workflow rows** using **198 inference dispatches** within
the frozen 250 cap. The selected 3B model and fixed legacy RAG remain the demo
default: the bounded agent has no paired exact-field gain and uses more resources.

## Acceptance evidence

| Acceptance criterion | Evidence and status |
| --- | --- |
| About ten new cases bring the set toward fifty, each with reviewed outcomes and complete public replay metadata | Complete on the expressly delegated basis: the user chose “Delegate case review to Codex and accept its confirmation.” [Case review](cases-forty-one-through-fifty.md) records all ten outcomes, opening-based rationales, alternatives and attribution. This is assistant review accepted by the user, not independent human assessment. [Provenance](issue-19/provenance.json) verifies nineteen distinct unedited openings against REST/GraphQL, exact title/body hashes, ten independently checked pre-opening commits and eight pinned templates. [Metadata checks](issue-19/metadata-checks.json) establish 50 unique confirmed cases, 46 families, 58 family members, candidate chronology and unchanged hashes for all 269 earlier case/evaluation files. |
| Changed or unavailable public issue content is flagged rather than silently scored | Complete for the implemented boundary. The unchanged historical replay verifies content and commits before model input. Focused tests in `tests/test_replay.py` cover changed current/earlier openings and unavailable issues; `tests/test_workflow_comparison.py::test_shared_integrity_failure_keeps_all_rows_and_dispatches_nothing` covers changed and unavailable openings across every workflow, retaining three unscored rows with zero dispatches. The actual [shared preflight](issue-19/run/results.json) verified all fifty without flags. No real changed/unavailable opening occurred during this pass; failure behavior is deterministic test evidence, not an observed live failure. |
| Final expanded results include field-level scores, latency, cost and representative failures | Complete: [results](issue-19/run/results.json) retain all reports, scores, traces, resource measurements and serving snapshots. [Comparison](issue-19/comparison.json) separates archived forty, rerun originals, new ten and final fifty, with per-case changes. [Offline verification](issue-19/verification.json) recomputes every score and accounts for all 198 request/response pairs. Tables and failure analysis below expose coverage, denominators, latency and cost limitations. Fresh reply usefulness and semantic citation support remain unverified because no fresh report ratings were supplied; case confirmation does not supply those ratings. |

## Frozen scope and reproducibility

Started from updated main `9d4bb25a31b6f7f32d748d27eec243fda68ec720` on
`feat/issue-19-fifty-cases`. Only issue #19 is addressed. The confirmed cases,
runner and [protocol](issue-19-protocol.md) were committed at
`c611f9d7f0255caccaefd8a0c9826491ca664e1a` before inference. The
[freeze](issue-19/freeze.json) records that commit and protocol/catalog/source
hashes, which match the run's independently captured hashes. No expected outcome,
prompt, retrieval rule, scoring rule or default model was tuned from these results.

Shared preflight began **2026-11-25 03:49:45 UTC**, taking **57.746 seconds**.
Every workflow used the same verified openings, candidate catalog, cutoffs,
pre-opening commits and templates. Full openings were preserved without
truncation or replacement. Later comments, labels, closures, annotations and
expected outcomes never entered model input. Full contributor bodies remain
on GitHub under ADR-0003.

Selection adds the first ten unedited substantive issues after #12328, May
22–27, 2024; seven intervening edited issues were excluded. The additions are
topical nonduplicates; the full set retains five duplicate-candidate and three
uncertain relationships. This selected, previously exposed development set is
not a random sample or evidence of repository-wide accuracy. Classification
alternatives and conservative family grouping are explicit in the case review.
No training corpus exists to audit; future/external training overlap remains
unverified. Existing families and outcomes remain intact.

Replay the catalog with controlled responses using
`python -m maintainer_copilot.replay --all`. Controlled replay is an integrity
smoke check, not model-quality measurement. To reproduce real inference, keep
Windows Ollama running and use a fresh directory, as documented in the README:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison --issue 19 \
  --ollama-url http://172.17.48.1:11434 --directory /tmp/issue-19-new-run
```

Use the current Windows host address. The command refuses existing directories
and validates preserved baseline hashes and all case confirmations before serving
preflight. Older `--issue 16`, `17` and `18` modes retain their archived catalogs.

## Field scores and resources

Model: `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, served by Windows Ollama 0.40.16. Context 16384, temperature 0, seed 42,
top-k 20, top-p 0.8 and repeat penalty 1 match the established settings.
Each dispatch retained the 256-token output cap, 20-second timeout and 65536-byte
response cap. Drafting was disabled. Initial residency was empty; no warm-up,
retry, repair or second inference pass occurred. Final residency confirms
size == size_vram == 2730345103 bytes and context 16384.

| Measurement | Keyword rules | Fixed legacy RAG | Bounded agent |
| --- | ---: | ---: | ---: |
| Catalog / eligible / scored cases | 50 / 50 / 50 | 50 / 50 / 50 | 50 / 50 / 50 |
| Complete / partial / flagged reports | 46 / 4 / 0 | 45 / 5 / 0 | 43 / 7 / 0 |
| Issue-type exact agreement | 20/50 | 24/50 | 24/50 |
| Missing-detail exact agreement | 20/50 | 20/50 | 20/50 |
| Missing-detail macro precision / recall | 0.837 / 0.610 | 0.837 / 0.610 | 0.837 / 0.610 |
| Expected-earlier-issue retrieval | 6/50 | 6/50 | 5/50 |
| Existing relationship exact score | 2/47 | 2/47 | 2/47 |
| Reports passing structural citation checks | 50/50 | 50/50 | 50/50 |
| Citation records / reports with citations | 44 / 25 | 44 / 25 | 42 / 25 |
| Issue-type abstention appropriateness | 46/50 | 45/50 | 45/50 |
| Duplicate abstention appropriateness | 47/50 | 47/50 | 45/50 |
| Inference dispatches | 0 | 50 | 148 |
| Input / output tokens | 0 / 0 | 79540 / 3068 | 199091 / 4763 |
| Model errors | 0 | 1 | 1 |
| Failed retrieval events, including unavailable historical CI | 4 | 4 | 7 |
| Mean latency (ms) | 4.51 | 754.31 | 1333.02 |
| Nearest-rank p50 / p95 latency (ms) | 4.149 / 8.913 | 591.822 / 1240.925 | 1166.908 / 1928.686 |
| Maximum latency (ms) | 9.845 | 5841.102 | 7021.750 |
| Device-wide sampled GPU peak (MiB) | 2754 | 2754 | 2754 |
| Fresh reply usefulness / semantic support | unverified | unverified | unverified |

Scores include partial/fallback reports; aggregate `completed` means scoreable,
not complete application status. Three uncertain relationships remain unscored.
The relationship metric requires retrieving the annotated earlier issue even
when its relationship is nonduplicate; **2/47 is not binary duplicate accuracy**.
Empty detail predictions receive precision one, which must be read with recall.
Half the reports per workflow have no citations and pass structural checks
vacuously. Structural success does not establish semantic support or coverage.

Four failed retrieval events per workflow are intentional historical-CI
abstentions (#12249, #12255, #12303, #12308). The agent also retains issue/source
read failures on #12081 and an issue-read failure on #12204. These events are
classified as `retrieval`, so the summary's `tool_errors` field alone misses
them. Both model workflows retain the rejected selection on #12216.

The [request ledger](issue-19/run/requests.jsonl) and
[bounded raw responses](issue-19/run/responses.jsonl) retain all 198 charged
dispatches. The agent adds **98 dispatches**, uses **2.468x** fixed-workflow
tokens and has **1.554x** its p95 latency, with **zero paired exact-field gain**
across fifty pairs. Partial reports, additional errors, token use and missing
fresh semantic/usefulness review prevent promotion under the retained gates.

Latency excludes public evidence acquisition and includes cold loading/provider
caching. Six workflow-order permutations cycle through case order. These are
measurements from one sequential laptop pass, not a stable latency distribution.
GPU samples are device-wide and include resident model memory during keyword
rows; they do not establish true peaks or per-process allocation. Marginal local
model and public GitHub API charges are **USD 0**. Hardware, electricity, network
and hosting costs were not measured; tokens/time are resource proxies, not a
measured total dollar cost.

## Comparison with the archived forty

[Per-case comparison](issue-19/comparison.json) finds **zero changed field/status
rows**, **zero report-content changes** after excluding volatile trace IDs and
**zero candidate-pool changes** across the original 120 rows. All original
forty cases remain eligible. Newly introduced openings postdate their cutoffs.
The original outcomes, raw responses, review records and prior results were
preserved byte-for-byte against the baseline manifest.

| Subset | Keyword type / details | Fixed type / details | Agent type / details |
| --- | ---: | ---: | ---: |
| Archived forty (#18) | 16/40 / 17/40 | 19/40 / 17/40 | 19/40 / 17/40 |
| Rerun original forty | 16/40 / 17/40 | 19/40 / 17/40 | 19/40 / 17/40 |
| New ten | 4/10 / 3/10 | 5/10 / 3/10 | 5/10 / 3/10 |
| Final fifty | 20/50 / 20/50 | 24/50 / 20/50 | 24/50 / 20/50 |

No annotated earlier issue is retrieved on the new ten. Their issue-type and
detail outcomes change the aggregate through sample composition, not a model
or workflow improvement. Single-label ambiguity also limits exact agreement.

## Representative failures in the additions

- **#12351:** models match the accepted bug type, while keyword rules choose
  docs. All request a minimal example despite the exact build command and fail
  to request the missing OS release. The opening already lists pluggy 1.4.0;
  later upgrade advice is not replay evidence.
- **#12352:** all choose bug rather than accepted selftests. All request the
  missing reproducer but miss the OS release. The later disclosed local patch
  does not retroactively complete the opening. Bug remains a reasonable type
  alternative, as recorded before inference.
- **#12357:** all choose bug rather than accepted question. The two environment
  requests match the expected set, but the exact-type score penalizes a
  reasonable alternative interpretation of the hook-wrapper contract.
- **#12360:** keyword rules match docs; models select bug despite the outdated
  documentation/version mismatch. All correctly request no additional details.
- **#12363:** models match enhancement, but all redundantly ask for alternatives
  already given as ReadTheDocs domain settings. Keyword rules choose docs, a
  recorded classification alternative.
- **#12366:** all match enhancement but redundantly request the solution and
  use case supplied in the problem section; only the alternative is absent.
- **#12367:** keyword rules recognize regression, while models choose enhancement.
  All omit the three reviewed environment/reproducer requests and return no
  substantive evidence-backed reply claim despite the detailed opening diagnosis.
- **#12371:** models match bug while keyword rules choose docs. All omit the
  missing package-list request and abstain on a specific reply request.
- **#12376:** all choose enhancement rather than accepted proposal, an explicitly
  defensible alternative. All redundantly request a use case despite the
  multihost-plugin example. The paired earlier #12216 is not retrieved.
- **#12377:** all match docs and no missing details, yet provide only a generic
  abstention rather than a supported explanation of the documentation defect.
  Exact field agreement does not establish reply usefulness.

No observed failure triggered changes to prompts, retrieval, scoring, expected
outcomes or model settings. New report ratings were not inferred from this
analysis or copied from previous evaluations.

## Verification and remaining review

The agreed test seams were catalog loading, historical replay and the comparison
runner. Red-before-green evidence covers the [fifty-case budget](issue-19/red-budget.txt),
[runner summary](issue-19/red-runner.txt), [catalog selection](issue-19/red-catalog-selection.txt)
and [published case coverage](issue-19/red-published-cases.txt). Focused checks
passed **87 tests**, with two opt-in live tests skipped; strict typechecking
passed. The actual fifty-case preflight supplies separate live evidence.
Final repository checks are recorded in [checks](issue-19/checks.json).

Audit without network or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file python scripts/issue19_verify.py --check-only
```

The verifier checks baseline hashes, provenance, pinned template hashes, family
membership and chronology, frozen commit/catalog/protocol/source hashes, all
150 workflow rows and scores, all 198 ledger/response records and fresh review
fingerprints. The shared audit module also preserves the forty-case verifier:
`scripts/issue18_verify.py --check-only` checks its archive without rewriting it.
The [two-axis review](issue-19-code-review.md) records Standards and Spec separately.

The [fresh blinded sheet](issue-19/run/human-review.md),
[pending ratings](issue-19/run/human-review.json) and separate
[identity key](issue-19/run/review-key.json) cover all 150 reports. Reply usefulness,
semantic citation support and unannotated retrieved relationships remain
unverified because no fresh explicit report review was supplied. Delegated
confirmation of expected outcomes does not rate generated reports. No claim
of independent human review, new model quality or total monetary cost is made.
