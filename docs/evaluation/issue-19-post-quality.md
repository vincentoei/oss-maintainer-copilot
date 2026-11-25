# Issue #19: fifty cases after merged triage-quality fixes

PR #57 merged into main at `9678b7285a651c5802337c88bee7c8c540de9507`, resolving
#56 before this update to PR #58. The new fifty-case pass measures that merged
implementation, including its final title-version wording change. All fifty
cases passed evidence preflight; all **150 rows** were retained and scored using
**198 charged dispatches**. Exact missing-detail agreement improves from
**20/50 to 43/50** in every workflow. The two model workflows retain identical
field scores, so the fixed workflow remains the default.

The two model workflows regress on **#12377**, selecting question instead of
the accepted docs type. That regression and all remaining disagreements are
retained. No expected outcome, prompt or triage heuristic was changed from
these results. This pass does not establish independent human quality or
generalization beyond the selected development cases.

## Acceptance and preservation evidence

| Requirement | Evidence |
| --- | --- |
| Approximately fifty cases with reviewed outcomes and complete public replay metadata | The same [ten additions](cases-forty-one-through-fifty.md) and forty original cases remain confirmed under the user's expressly accepted Codex delegation. This is assistant review accepted by the user, not independent human assessment. Opening hashes, cutoffs, pinned commits, expected outcomes and family IDs are unchanged. [Verification](issue-19/post-quality/verification.json) checks all 50 cases, 46 families, 58 family members and unchanged candidate pools. |
| Changed or unavailable public content flagged rather than silently scored | Shared preflight verified all fifty against GitHub before inference. Changed/unavailable-opening regression tests retain unscored rows and make zero dispatches. No such live flag occurred in this pass. The supplied-baseline CLI test rejects altered artifacts before provider access or run-directory creation. |
| Final expanded comparison includes field scores, latency, cost and representative failures | [Results](issue-19/post-quality/run/results.json) retain reports, scores, traces, identity/settings and resources. [Original-fifty comparison](issue-19/post-quality/comparison-original-fifty.json) records every before/after row, transition and original-forty/new-ten subset. [Prior-quality comparison](issue-19/post-quality/comparison-quality-forty.json) compares the forty-case subset with #56's final recorded live pass. Scores, resources, remaining errors and the new regression appear below. |
| Preserve prior work while sequencing #56/#57 before #19 | [Baseline](issue-19/post-quality/baseline.json) protects **395 prior case/evaluation files** byte-for-byte, including original #19 and both #56 passes/reviews. Original measurements remain archived in [issue-19.md](issue-19.md). Both #56 audits still pass using their archived catalogs and source commits. No prior rating or response was transferred into this new run. |

## Freeze and reproduction

The user authorized this separate comparison after #57 merged. The
[protocol](issue-19/post-quality/protocol.md), baseline, integration and evaluator
were committed at **`ee0e7c6e33c0ec2b696035612c606a1e7c61984c`** before inference.
The [freeze](issue-19/post-quality/freeze.json) matches the run's independent
source, protocol and catalog hashes. The catalog hash is identical to the first
fifty-case run: `924b506c662b51e50743f19aaa26df947230a53a09bb23789742542474daf4d7`.

Shared evidence preflight began **2026-11-25 04:26:58 UTC**, taking **47.467 s**.
All workflows used the same full verified openings, pre-opening commits,
templates, cutoffs and eligible candidates. Later discussion, expected outcomes,
annotations and review ratings never entered model inputs. Full contributor
bodies remain on GitHub; published artifacts retain metadata and bounded outputs.

Use a fresh output directory and the current Windows host address:

```sh
GITHUB_TOKEN="$(gh auth token)" uv run --locked --no-env-file \
  python -m maintainer_copilot.workflow_comparison --issue 19 \
  --ollama-url http://172.17.48.1:11434 \
  --baseline docs/evaluation/issue-19/post-quality/baseline.json \
  --protocol docs/evaluation/issue-19/post-quality/protocol.md \
  --directory /tmp/issue-19-post-quality-new-run
```

The command validates the preservation manifest and confirmed catalog before
provider access. It refuses existing directories. One pass was allowed for this
source freeze: fixed <=50, agent <=200, total <=250 charged calls. Actual calls
were fixed **50**, agent **148**, keyword **0**. No warm-up, retry, repair,
second pass or model search occurred. The original fifty-case pass has a separate
freeze and ledger; its 198 calls and results remain unchanged.

Selected model: `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M, Windows Ollama 0.40.16. Settings remain context 16384, temperature 0,
seed 42, top-k 20, top-p 0.8, repeat penalty 1, 256 output tokens, 20-second
timeout and 65536 response bytes. Initial residency was empty. Final residency
confirms size == size_vram == 2730345103 bytes and context 16384.

## Scores and resources

K = keyword rules; F = fixed RAG; A = bounded agent. All denominators include
scoreable partial/fallback reports. Aggregate `completed` means scoreable,
not complete application status.

| Measurement | K | F | A |
| --- | ---: | ---: | ---: |
| Catalog / eligible / scored | 50 / 50 / 50 | 50 / 50 / 50 | 50 / 50 / 50 |
| Complete / partial / flagged | 46 / 4 / 0 | 46 / 4 / 0 | 44 / 6 / 0 |
| Type agreement, original fifty → merged fixes | 20/50 → 24/50 | 24/50 → 29/50 | 24/50 → 29/50 |
| Exact details, original fifty → merged fixes | 20/50 → 43/50 | 20/50 → 43/50 | 20/50 → 43/50 |
| Detail macro precision / recall | .940 / .930 | .940 / .930 | .940 / .930 |
| Expected-earlier-issue retrieval | 6/50 | 6/50 | 5/50 |
| Relationship exact score | 2/47 | 2/47 | 2/47 |
| Structural citation checks | 50/50 | 50/50 | 50/50 |
| Citation records / reports with citations | 71 / 36 | 71 / 36 | 69 / 36 |
| Model errors, original fifty → merged fixes | 0 → 0 | 1 → 0 | 1 → 0 |
| Failed retrieval events, including historical CI | 4 | 4 | 7 |
| Dispatches | 0 | 50 | 148 |
| Input / output tokens | 0 / 0 | 81934 / 1287 | 201485 / 2982 |
| Mean latency, ms | 5.11 | 411.66 | 1005.01 |
| Nearest-rank p50 / p95 latency, ms | 4.422 / 9.928 | 301.230 / 855.583 | 810.594 / 1698.677 |
| Maximum latency, ms | 13.170 | 3366.692 | 6066.951 |
| Device-wide sampled GPU peak, MiB | 2754 | 2754 | 2754 |
| Fresh reply usefulness / semantic support | pending | pending | pending |

Three uncertain relationships are unscored. Relationship exact scoring requires
retrieving the annotated earlier issue even for nonduplicates; **2/47 is not
binary duplicate accuracy**. Empty predictions receive detail precision one.
Fourteen reports per workflow have no citations and pass structural checks
vacuously; those checks do not prove semantic support.

Four partial reports per arm retain unavailable historical CI. The agent also
retains the established earlier-issue/source read failures at #12081/#12204.
#12216 no longer has a model-selection validation error. Atomic label/quote
pairing prevents mismatches without guaranteeing the selected pair is the
correct semantic classification, as the #12377 regression demonstrates.

| Subset | K type / details | F type / details | A type / details |
| --- | ---: | ---: | ---: |
| Earlier #19 original forty | 16/40 / 17/40 | 19/40 / 17/40 | 19/40 / 17/40 |
| #56 final recorded live forty | 19/40 / 39/40 | 24/40 / 39/40 | 24/40 / 39/40 |
| This pass: original forty | 19/40 / 39/40 | 24/40 / 39/40 | 24/40 / 39/40 |
| Earlier #19 new ten | 4/10 / 3/10 | 5/10 / 3/10 | 5/10 / 3/10 |
| This pass: new ten | 5/10 / 4/10 | 5/10 / 4/10 | 5/10 / 4/10 |

All field scores, statuses and candidate pools on the original forty match #56's
recorded live pass. Its source `0035e14` preceded the final title-version wording
change; this pass measures the actual merged wording rather than claiming its
old results were rerun unchanged. Reports can differ in narrowed questions even
when their field scores remain equal. The direct fifty-to-fifty comparison
contains **87 changed field/status rows**, including the two explicit type
regressions at #12377. No previously correct exact detail set regresses.

The agent has zero paired field-score gain across fifty pairs, **98** additional
dispatches, **2.457x** fixed tokens and **1.985x** fixed p95 latency. Partial-report,
paired-gain, token and fresh-review gates prevent promotion. The selected 3B and
fixed workflow remain defaults.

Latency excludes evidence acquisition, includes cold loading/caching, and comes
from one sequential laptop pass with six cycling workflow orders. Changed
source, schema/prompt and provider behavior limit causal attribution. Sampled
GPU memory is device-wide and cannot establish true peaks or per-process use.
Marginal local-model and public-GitHub API cost is **USD 0**; hardware,
electricity, network and hosting were not measured. Tokens and time are resource
proxies, not a measured total operating cost.

## Remaining errors and regression

- **#12083:** the accepted annotation expects packages only; the report also
  asks for missing OS releases. This disclosed annotation disagreement remains
  the original forty's sole exact-detail mismatch. The outcome was preserved.
- **#12351:** all ask for a minimal example instead of the reviewed missing OS
  release; the opening already supplies a build command. Models match bug;
  keyword rules choose docs. No later pluggy advice enters replay.
- **#12352:** all request the reproducer but omit the reviewed missing OS release.
  Bug differs from accepted selftests, with ambiguity recorded before inference.
- **#12357:** the detail requests match; all choose bug rather than the accepted
  question interpretation of the wrapper contract.
- **#12360:** both models now match docs rather than bug; all retain the correct
  empty detail set. This type gain is offset by #12377 among the new ten.
- **#12363:** all still ask for alternatives already supplied in the ReadTheDocs
  settings discussion. Models match enhancement; keyword rules choose docs.
- **#12366:** the redundant use-case question is removed, but all still request
  the solution already demonstrated in the problem section. Only an alternative
  is absent. Exact details remain wrong despite improved wording.
- **#12367:** all omit the three reviewed environment/reproducer requests.
  Models now choose question rather than their previous enhancement; neither
  matches the accepted regression. Keyword rules recognize regression.
- **#12371:** keyword type changes to bug, matching the models and expected
  outcome. Every workflow still omits the missing package-list request.
- **#12376:** the redundant use-case question is removed and exact details now
  match. All choose enhancement rather than accepted proposal, a recorded
  reasonable alternative. No annotated earlier issue is retrieved.
- **#12377 regression:** both models change from correct docs to question.
  Keyword rules retain docs. All retain the correct empty detail set and generic
  abstention reply. Mechanical quote support is insufficient to establish the
  right issue type. The regression is recorded in verification, without rerun
  or outcome tuning.

None of the additions retrieves its annotated earlier issue. Duplicate retrieval
and relationship quality remain weak. Correct empty detail sets and structurally
valid citations do not establish useful replies. No independent human rating
or promotion claim follows from this table.

## Verification and review limits

Audit all source/catalog/protocol/baseline hashes, 395 preserved files, candidate
chronology, 150 recomputed scores, 198 request/response pairs and 150 fresh review
fingerprints without network or inference:

```sh
PYTHONPATH=src uv run --locked --no-env-file \
  python scripts/issue19_post_quality_verify.py --check-only
```

Original `issue19_verify.py --check-only` and `issue18_verify.py --check-only`
still audit their archived results. #56's two verifiers now select the recorded
forty-case catalog and validate the original final-wording commit, preserving
their artifact bytes as source evolves. The [red CLI evidence](issue-19/post-quality/red-custom-baseline.txt)
and archived-audit red outputs document the integration checks before fixes.
Focused replay/provider checks passed 80 tests, with strict typechecking clean.
Final checks and two-axis review are recorded separately with this update.

The fresh [blinded sheet](issue-19/post-quality/run/human-review.md),
[pending ratings](issue-19/post-quality/run/human-review.json) and separate
[identity key](issue-19/post-quality/run/review-key.json) cover this pass's 150
reports. #56's Codex reviews remain attached to their original fingerprints;
no ratings were transferred. Fresh reply usefulness and semantic citation support
remain unverified because no explicit new report ratings were supplied. Future
training overlap awaits an actual corpus. No human setup or manual execution
is required for this scoped integration and measurement.
