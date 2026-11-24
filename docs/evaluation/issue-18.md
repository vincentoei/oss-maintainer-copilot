# Issue #18: forty reviewed evaluation cases

The catalog contains **40 confirmed cases across 37 issue families**. All forty
passed shared live preflight. The single comparison retained and scored all
**120 case/workflow rows**, including partial/fallback reports. The selected 3B
model and fixed legacy RAG remain the demo default.

## Acceptance evidence

| Acceptance criterion | Evidence and status |
| --- | --- |
| Ten new cases have human-confirmed outcomes, complete metadata, and cutoff-safe replay | Complete on the explicitly authorized delegated basis: the user chose “Delegate case review to Codex and accept its confirmation.” [Case review](cases-thirty-one-through-forty.md) records ten judgments, rationale, ambiguities and attribution. This is assistant review accepted by the user, not independent human assessment. [Provenance](issue-18/provenance.json) verifies sixteen distinct unedited openings against REST/GraphQL, title/body hashes, ten independently checked pre-cutoff commits and twelve pinned template versions. [Actual preflight](issue-18/run/results.json) verified all forty cases, including every addition; no opening was truncated or replaced. |
| The issue-family and chronology checks still pass for the expanded set | Complete for the recorded catalog: [metadata checks](issue-18/metadata-checks.json) verify 40 unique cases, 37 families and 46 members with no conflicting assignment, no recorded training overlap and only pre-cutoff candidates. [Partitions](issue-18/partitions.json) preserve existing families and conservatively group #12303/#12287 and #12307/#6682 without inventing duplicate confirmation. All 237 prior case/evaluation files match [baseline hashes](issue-18/baseline.json). Future/external training integrity remains unverified because no training corpus exists. |
| Results report updated field-level scores and newly observed failures | Complete: [results](issue-18/run/results.json) preserve all 120 reports, scores, traces and resource records. [Comparison](issue-18/comparison.json) separates archived thirty, rerun original thirty, new ten and expanded forty, with per-case score/status/candidate changes. [Offline verification](issue-18/verification.json) recomputes all 120 scores and accounts for all 158 request/response pairs. The failure analysis below covers the additions. Fresh reply usefulness and semantic citation support remain unverified because no fresh report ratings were supplied. |

## Scope and freeze

Started from updated main `48e3273ee109e9a7ff6c6b1c55a4c6882e7d4183` on
`feat/issue-18-forty-cases`; only #18 is addressed. The cases, confirmed outcomes,
runner and [protocol](issue-18-protocol.md) were committed at
`212bfecb22ab32c02e229f6d7872914123aa8d20` before inference. The
[freeze](issue-18/freeze.json) records that commit and source/protocol/catalog
hashes, independently captured by the run before dispatch. Original outcomes,
review ratings, responses and earlier results were preserved.

Shared preflight began **2026-11-24 12:39:37 UTC**, taking 99.055 seconds. Every
arm used the same verified openings, cutoffs, pinned commits, templates and
eligible candidate catalog. Later discussion, labels, closures and annotation
rationales never entered replay. Full issue bodies remain on GitHub under ADR-0003.

The earlier [controlled smoke replay](issue-18/replay.json) retained forty cases
with zero flags, 36 complete and four partial reports. It preceded requesting-user
confirmation, so its archived review-status fields correctly say `pending` for
the additions. It used controlled model responses, not real-model quality
measurement. The actual comparison uses the confirmed catalog and local inference.

## Updated scores and resources

Model: `pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`,
Q4_K_M. Initial/final run serving snapshots verify context 16384, temperature 0,
seed 42, top-k 20, top-p 0.8 and repeat penalty 1. Output was capped at 256 tokens,
timeout at 20 seconds and response bytes at 65536. Windows Ollama 0.40.16 was
reached from WSL at `172.17.48.1:11434`. Final residency confirms size == size_vram
== 2730345103 bytes and context 16384.

| Measurement | Keyword rules | Fixed legacy RAG | Bounded agent |
| --- | ---: | ---: | ---: |
| Catalog / eligible / scored cases | 40 / 40 / 40 | 40 / 40 / 40 | 40 / 40 / 40 |
| Complete / partial / flagged reports | 36 / 4 / 0 | 35 / 5 / 0 | 33 / 7 / 0 |
| Issue-type exact agreement | 16/40 | 19/40 | 19/40 |
| Missing-detail exact agreement | 17/40 | 17/40 | 17/40 |
| Missing-detail macro precision / recall | 0.887 / 0.600 | 0.887 / 0.600 | 0.887 / 0.600 |
| Expected-earlier-issue retrieval | 6/40 | 6/40 | 5/40 |
| Existing relationship exact score | 2/37 | 2/37 | 2/37 |
| Reports passing structural citation checks | 40/40 | 40/40 | 40/40 |
| Citation records / reports with citations | 33 / 19 | 33 / 19 | 31 / 19 |
| Issue-type abstention appropriateness | 36/40 | 35/40 | 35/40 |
| Duplicate abstention appropriateness | 37/40 | 37/40 | 35/40 |
| Inference dispatches | 0 | 40 | 118 |
| Input / output tokens | 0 / 0 | 64156 / 2442 | 158765 / 3787 |
| Model errors | 0 | 1 | 1 |
| Failed retrieval events, including unavailable CI | 4 | 4 | 7 |
| Mean latency (ms) | 4.72 | 757.80 | 1378.25 |
| Nearest-rank p50 / p95 latency (ms) | 3.718 / 9.199 | 642.816 / 1206.256 | 1170.576 / 1991.640 |
| Maximum latency (ms) | 23.890 | 4138.367 | 7117.849 |
| Device-wide sampled GPU peak (MiB) | 2742 | 2742 | 2742 |
| Fresh reply usefulness / semantic support | unverified | unverified | unverified |

Scores include partial/fallback reports; the aggregate's `completed` means
scoreable, not complete application status. Three uncertain relationships remain
unscored. The relationship metric requires retrieving the annotated earlier
issue even for nonduplicates; 2/37 is not general binary duplicate accuracy.
Empty detail predictions receive precision one, which must be read with recall.
Twenty-one reports per arm have no citations and pass structural checks vacuously;
40/40 does not establish semantic support or evidence coverage.

The summary's `tool_errors` counter counts events classified as `tool`; these
failed reads are classified as `retrieval`. The table exposes raw retrieval
events: four intentional historical-CI abstentions per arm, plus two issue reads
and one source read for the agent. #12216 retains its rejected model selection
in both model arms. Raw responses remain available.

The [dispatch ledger](issue-18/run/requests.jsonl) and
[bounded responses](issue-18/run/responses.jsonl) retain **158 actual calls**
within the frozen 200 cap: 40 fixed and 118 agent. No inference retry, warm-up,
repair or second pass occurred. Agent tokens were **2.441x** fixed with 78 extra
dispatches and zero paired exact-field gain across forty pairs; its p95 was
1.651x fixed. These results supply no basis to promote the agent.

Latency excludes public evidence acquisition and includes cold loads/provider
caching. Six workflow-order permutations cycle through case order. This is one
sequential laptop run, not a stable distribution. Device-wide GPU samples include
resident model memory during keyword rows and cannot establish true peaks or
process allocation. Marginal model/GitHub API charges are USD 0; hardware,
electricity, network and hosting were not measured.

## Comparison with the archived thirty

[Per-case deltas](issue-18/comparison.json) identify exactly one changed original
case across three rows: **#12204**. Its full verified opening is now eligible
after the already-merged #17 replay-limit follow-up; the archive flagged it before
dispatch. All arms now match its reviewed bug type and empty missing-detail set,
but do not retrieve annotated #12203. Keyword/fixed reports are complete; the
agent is partial after an issue-read failure and abstains on relationships. This
is a coverage change, not a model improvement. No old score or outcome changed.

All report content, statuses and field scores for the other 29 original cases
are unchanged when volatile trace IDs are excluded. Every original candidate
pool is unchanged: additions and newly introduced candidate openings postdate
those cutoffs. The agent's #12081 issue/source read failures were already present
in the archived run and are retained here.

| Subset | Keyword type / details | Fixed type / details | Agent type / details |
| --- | ---: | ---: | ---: |
| Archived thirty (#17; 29 eligible) | 12/29 / 14/29 | 16/29 / 14/29 | 16/29 / 14/29 |
| Rerun original thirty | 13/30 / 15/30 | 17/30 / 15/30 | 17/30 / 15/30 |
| New ten | 3/10 / 2/10 | 2/10 / 2/10 | 2/10 / 2/10 |
| Expanded forty | 16/40 / 17/40 | 19/40 / 17/40 | 19/40 / 17/40 |

Different denominators, subjective single-label judgments, previously exposed
development cases and provider behavior limit interpretation. Aggregate changes
do not establish a paired model improvement or generalization.

## Failures exposed by the additions

- **#12293:** all arms choose bug rather than the reviewed version regression
  and request none of the three expected environment/reproducer details.
- **#12298:** all arms identify question but miss all three expected detail
  requests; logs do not substitute for fixture/test code.
- **#12300:** all arms match bug and all three missing details, but do not
  retrieve the annotated earlier nonduplicate, as in every new case.
- **#12303:** models choose bug and keyword rules choose enhancement rather than
  regression. All arms redundantly ask for versions despite the accepted rolling
  openSUSE/pytest identification and omit the uncertain relationship abstention.
- **#12305:** all arms choose bug rather than the accepted question interpretation
  and request package/version information already supplied.
- **#12307:** all arms abstain on type and template details, missing the reviewed
  bug type and two missing environment details.
- **#12308:** all arms choose bug rather than regression and redundantly request
  the supplied package list. The minimal example request is correct; the later
  reproduction did not leak into the opening.
- **#12312:** all arms abstain on the reviewed enhancement and produce no useful
  reply claim. Matching an empty detail set does not establish reply usefulness.
- **#12323:** all arms choose bug rather than accepted selftests and omit the
  missing package list request. Review records bug as a reasonable alternative;
  exact agreement must be read with that ambiguity.
- **#12328:** keyword rules recognize regression but models choose bug. All arms
  ask for a minimal example already supplied as a complete package layout with
  tests and invocation, a redundant request on a complete report.

#12303/#12308 also retain intentional historical-CI abstentions, as do existing
#12249/#12255. No observed failure triggered a prompt, retrieval, scorer,
expected-outcome or model change. This ticket measures the expanded set.

## Verification and remaining review

[Checks](issue-18/checks.json) record lint, formatting, strict mypy and the full
suite. The agreed seams are the existing replay/cutoff interface and comparison
runner. [Red evidence](issue-18/red.txt) shows the forty-case confirmation check
failing while additions were pending; it passed after authorized confirmation.
Focused replay/comparison checks passed 70 tests with two opt-in live tests
skipped. Earlier implementation used existing checks while seam confirmation was
pending; no strict test-first sequence is claimed for that runner extension.
The actual forty-case preflight and comparison supply separate live evidence.

Run `PYTHONPATH=src .venv/bin/python scripts/issue18_verify.py` without network or
inference to verify preserved files, frozen source/catalog/protocol at `212bfec`,
provenance/template hashes, families, candidate cutoffs, all 120 rows, 158
dispatch/response records, fresh review fingerprints and recomputed scores. It
regenerates the comparison. The older `scripts/issue17_verify.py` still audits
its original thirty-case catalog and ninety rows after this expansion.

The [fresh sheet](issue-18/run/human-review.md),
[pending ratings](issue-18/run/human-review.json) and separate
[identity key](issue-18/run/review-key.json) cover all 120 reports. Reply usefulness,
semantic citation support and unannotated retrieved relationships remain
unverified because no new report ratings were supplied. No old ratings were
transferred; delegated case confirmation does not supply them. Future/external
training integrity awaits an actual training corpus. The
[two-axis review](issue-18-code-review.md) records Standards and Spec separately.
