# Issue #50: bounded drafting experiment

Decision: **retain the working legacy application/model**. The frozen candidate
fails validation in every development and reserved report. Do not adopt it or
tune again under this issue. This is a negative application-contract result,
not proof about inherent model quality. **Issue #50 remains incomplete pending
explicit human reply/semantic reviews and the limitations below; it is not merged.**

Started from updated main cc44852c7db55840f233f952c411dd485a8660a8 on
feat/issue-50-evidence-drafting. The [protocol](issue-50-protocol.md) was committed
at 09feeec and [published before implementation](https://github.com/vincentoei/oss-maintainer-copilot/issues/50#issuecomment-7107246114).
All original artifacts and twenty catalog cases remain byte-identical under the
[baseline manifest](issue-50-baseline.json). No #16 or #33 implementation occurred.

## Execution and stopping

Two development iterations; **85/120 actual inference dispatches**, including
failures: 20 initial unmatched control, 19 corrected control, 19 candidate, four
API smoke calls, twenty pilot calls and three live-browser calls. Zero warm-ups/retries of model outputs.
One oversized opening (#12204) received no inference in either corrected arm;
its explicit partial report remains in each twenty-case denominator.

[Deviations](issue-50-deviations.md) explain reallocation of development requests:
the first control lacked passage inputs. It remains observational evidence and
cannot establish promotion. Corrected control initially flagged sixteen acquisition
failures without inference. Authenticated acquisition recovered only those cases,
retaining all failures and avoiding repeated outputs. The runner charges before
dispatch with a locked/fsynced ledger and stops at sixty development requests or
120 total. Recovery is rejected if a flagged case already dispatched inference.

Pilot expectations/family separation received [explicit human confirmation](issue-50-pilot-review.md)
before inference. The [manifest](issue-50-pilot.json) freezes original hashes,
cutoffs, pre-cutoff revisions and uncertain earlier-issue judgments. All five
originals and commits were verified again before one pass per arm. No pilot output
was used for tuning; input exposure for selection/annotation is recorded. These
cases cannot subsequently be described as unseen.

## Results

[Summary and per-case field evidence](issue-50/summary.json), [request ledger](issue-50/requests.jsonl),
raw responses, reports and traces are retained in issue-50/. Failure reports are
scoreable reports, not validated model successes.

| Measurement | Corrected A: legacy 3B | B: drafting 3B |
| --- | ---: | ---: |
| Development cases / actual responses | 20 / 19 | 20 / 19 |
| Partial reports | 2 | 20 |
| Issue-type exact agreement | 0.60 | 0.00 |
| Missing-detail exact agreement | 0.65 | 0.65 |
| Existing relationship exact score | 2/19 | 2/19 |
| Structural citation validity | 1.00 | 1.00 |
| End-to-end p95 | 7.378 s | 3.644 s |
| Input / output tokens | 26193 / 1192 | 21619 / 2527 |
| Peak sampled GPU memory | 2740 MiB | 2742 MiB |
| Human usefulness / semantic support | pending | pending |

The frozen drafting schema admits generic type strings; unlike the legacy path,
its prompt does not provide enumerated type-evidence options. Models return labels
such as "bug", "Feature Request", or "Documentation Request" rather than complete
pytest labels, and sometimes confuse E passage IDs with C reply-statement IDs.
Validation rejects these responses and preserves partial reports. No response was
replaced with a better-looking retry. This is a concrete application/schema failure;
changing model size did not rescue this frozen implementation.

| Reserved pilot | Legacy 3B | Drafting 3B | Drafting 4B | Drafting 7B |
| --- | ---: | ---: | ---: | ---: |
| Cases / responses | 5/5 | 5/5 | 5/5 | 5/5 |
| Partial reports | 0 | 5 | 5 | 5 |
| End-to-end p95 | 0.938 s | 1.974 s | 5.894 s | 6.488 s |
| Peak sampled GPU use | 2742 MiB | 2742 MiB | 5002 MiB | 5356 MiB |
| Input / output tokens | 6253/270 | 5295/492 | 5295/522 | 5295/272 |

All sampled pilot residencies verify context 16384 and size == size_vram.
Serving records retain actual alias digests, templates, quantization and parameters;
alias FROM blobs match the preserved shortlisted GGUF hashes. Windows Ollama
0.40.16 serves WSL at 172.17.48.1:11434. Temperature 0, seed 42, top-k 20,
top-p 0.8, repeat penalty 1 and 512 output tokens are common. Both pilot resource
thresholds pass at sampled resolution; 500 ms device-wide samples cannot prove
true peaks and include other processes. Cold loads are included; no warm-ups used.

[Pilot hash checks](issue-50/pilot-matching.json) show identical prompts, schemas
and serialized inputs for B/C/D on every case. A/B packet evidence matches except
an empty-packet representation on #11906: A omits the optional field while B/C/D
serialize an empty list. Both contain no passages and receive the same full opening.
CRLF paragraphs exceed the passage bound and are explicitly omitted. This is a
disclosed representation limitation, not a silently truncated opening. Fresh A
also uses 512 rather than #48's 256 tokens; comparisons to #48 are confounded.

No fresh usefulness scores, unsupported-claim counts, improved/unchanged/regressed
ratings, relationship judgments or semantic approvals have been assigned.
[Forty development replies](issue-50/human-review.md) and
[twenty pilot replies](issue-50/pilot-human-review.md) use anonymous shuffled codes,
matching fingerprints and separate identity keys. Their JSON companions remain
pending. Requesting user was explicitly asked to review both sets; pilot expectation
confirmation does not approve generated replies.

## Acceptance evidence

| #50 criterion | Evidence and status |
| --- | --- |
| Freeze protocol and limits | Protocol commit/publication precede implementation. Same-model A/B measures application effects; frozen B/C/D isolates model serving identity with identical task inputs. Schedule deviation disclosed. |
| Preserve baseline/boundaries | Baseline manifest passes; main catalog untouched. Metadata-only pilot, verified cutoffs/hashes/commits, recorded selection exposure. #12204 over-budget opening flagged rather than truncated. |
| Structured drafting on both interfaces | Opt-in MODEL_DRAFTING=1 or drafting model/agent classes. Exact context quotes/IDs, extractive factual explanations, generated questions or explicit null. Legacy is default and rollback. Structural validity is not semantic proof. |
| Public regressions and safety | 276 tests pass, two ordinary live tests skipped; Ruff and strict mypy pass. Public regressions cover empty choices, null abstention, unknown IDs, false quotes, source references, malformed output, injection/paraphrases/quoted injection and citation-marker escaping. Existing #48 supplied-detail/relationship tests remain passing. New generated-question redundancy/relationship semantic regressions remain incomplete; limited lexical rejection does not prove semantic support. Read-only tools, four-call cap, tool bounds, 20 s timeout/65536-byte response and partial reports retained; experimental output limit increases to 512 as predeclared. |
| Same 3B then frozen 3B/4B/7B | Corrected 3B control/candidate precede pilot; preserved serving snapshots and blobs confirm identities/settings/residency. B/C/D input/prompt/schema hashes match. A empty-packet and schedule confounders disclosed. |
| Preserve outputs and explicit reviews | Real responses/reports/traces/errors, schema/prompt/input/evidence hashes and serving records preserved. Pilot expectations explicitly reviewed. **Sixty fresh usefulness/semantic reviews pending**; no labels or reasons invented/transferred. |
| Per-case quality/resources | summary.json contains per-case field comparisons and pending human fields; raw artifacts preserve tokens/errors/latency/GPU. Unsupported claims, human regressions, separate relationships and other-field abstention remain unverified pending human review. Five pilot cases are not independent generalization proof. |
| API/web and retain/adopt decision | Four counted real calls through both HTTP interfaces yield HTTP 200 partial reports with bounded traces. Browser renders both a preserved genuine response and a fresh browser-triggered real response/trace with no JS errors. The fresh check used three model calls, displayed the partial report, and retained its failed selection; successful rendering is not successful drafting. Threshold promotion cannot pass with failed candidates/incomplete human evidence: retain baseline. No merge or #16 handoff yet. |

## Required next human actions and limits

Review R01–R40 and P01–P20 with fresh usefulness ratings/reasons and separate semantic,
redundancy, relationship and abstention judgments; unsure stays pending.
The experiment cannot claim usefulness improvement without those reviews.
The [fresh browser check](issue-50/web-live.json) passed display/trace checks; its
model selection still failed. A pre-startup navigation failure dispatched no inference
and is preserved separately. No further prompt/schema/rule tuning is
permitted here. A future repair requires a separately scoped issue, even if every
candidate reply is unhelpful. Keep the current runnable baseline for eventual #16;
do not begin #16 or #33 within this work.

[Two-axis review](issue-50-code-review.md) documents corrected findings and remaining
requirements. To inspect the experimental behavior, set MODEL_DRAFTING=1 on the
existing server; omit it to retain the legacy default. The experimental path is
not promoted by this branch.
