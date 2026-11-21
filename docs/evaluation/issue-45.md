# Issue #45: recognize supplied feature details

[Issue #45](https://github.com/vincentoei/oss-maintainer-copilot/issues/45) fixes
the redundant requests found during #21's user validation. The original and
rendered pytest #12053 opening now produce **no missing-detail requests**, using
the same local model. This is a deterministic template-rule fix; it does not
establish an improvement in model reasoning.

Branch `fix/issue-45-feature-details` starts at `605bafb`, on top of the completed
#21 implementation because those changes are not yet on `main`. The earlier
#21 measurements remain historical artifacts. Model selection, search performance,
the full workflow comparison in #16 and second-repository support in #33 are
outside this change.

## Cause and behavior

Feature sections previously required Markdown heading markers. Pasting rendered
text lost those markers and made supplied problem/solution answers appear absent.
The use-case rule also missed “For some projects”, and the alternative rule missed
the concrete existing `--pdb`/`--pdbcls` command. These missing details became
mandatory reply selections, so changing the model alone could not correct them.

Section parsing now accepts supported plain or Markdown headings and stops at
the next supported plain heading or any Markdown heading. Empty sections, HTML
comments, empty fences and common placeholders do not supply answers. Project
usage in prose can supply a use case. Concrete current CLI, script, alias, plugin
or wrapper usage can supply an alternative; version metadata alone, negated
usage, questions and hypothetical approaches do not. Explicitly reporting no
alternatives exist answers the template's “or none” question. These remain
bounded English heuristics, with semantic limitations rather than a general
natural-language completeness classifier.

## Acceptance evidence

| Criterion | Evidence | Result and limits |
| --- | --- | --- |
| Both heading formats, correct bounds | [API regressions](../../tests/test_feature_details_api.py) | Plain empty use-case section stays missing despite an answered alternative; both heading formats recognize supplied answers |
| Original and rendered #12053 need no redundant requests | [real HTTP checks](issue-45-api.json), [final browser check](issue-45-web-final.json), [report screenshot](issue-45-web-final.png), [historical run](issue-45-results.json) | Both actual bodies return `missing_details: []`; no “Could you add” requests; historical expected set is unchanged and now matches |
| Incomplete and hypothetical answers stay missing | [API regressions](../../tests/test_feature_details_api.py) | Empty/comment/placeholder sections, untried or proposed alternatives, version-only usage, negated plugin usage and template prompts remain missing; explicit absence is accepted |
| Regression tests precede implementation | TDD through `POST /api/triage` and `POST /api/agent/triage` | Observed failures before each corresponding rule correction; 31 new parametrized cases pass. Controlled clients check report behavior only, not real-model quality |
| Preserve validation and historical provenance | [SHA-256 manifest](issue-45-provenance.json), unchanged model/agent/citation modules | All 53 recorded baseline/case files retain their hashes. Cutoffs, pinned commits, expected outcomes and review provenance are unchanged; existing rejection tests still pass |
| Same model/settings, fresh twenty-case evidence | [final real run](issue-45-results.json), [initial real run](issue-45-initial-results.json), [pre-review run](issue-45-pre-review-results.json) | Twenty real responses per run, with raw selections, field scores, reports, traces, errors and GPU sampling. Earlier runs are retained; final run follows boilerplate and negated-workaround review fixes. No prior artifacts overwritten |

Full suite: **199 passed, 2 skipped**; the two optional live checks remain skipped
in the ordinary suite. Mypy checks 27 source files successfully; Ruff lint and
format checks pass. The separate recorded real-inference checks below supply
live evidence; skipped ordinary tests are not counted as live successes.

## Unchanged model and serving settings

Windows Ollama **0.40.16** serves `pytest-triage:coder3b-ctx16k` to the WSL app
at `http://172.17.48.1:11434/v1`. This is Qwen2.5-Coder-3B-Instruct, GGUF
**Q4_K_M**, source tag `qwen2.5-coder:3b-instruct-q4_K_M`, serving manifest digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`.
Identity and alias parameters exactly match #21: context **16,384**, temperature
0, seed 42, top-k 20, top-p 0.8, repeat penalty 1.0; report output is limited to
256 tokens with JSON schema and a 20-second client timeout. The unchanged model
client SHA-256 is
`7bef4c191bd6511d123c548e7cce91013dd7aae107b82690dc69d09412d861c0`.
The final profile SHA-256 is
`5030ae943385c3d948c24a41c021ca075c55b62232f3dcf3ff0d973517e0caff`.
The [#21 manifest](issue-21-selection.json) and [setup guide](../local-model.md)
retain the source/blob identity and hardware/connectivity verification. No paid
model API is used.

## Twenty-case results

The runner verified all twenty openings, earlier catalog issues and pinned
repository evidence before real inference, then reused the public evidence
reads while revalidating each timed replay. Every case retains its opening
cutoff and repository commit in the output. The controlled integrity preflight
is not a model-quality measurement. “Completed” means a scoreable report:
19 complete reports and one partial report result from twenty real responses.

| Field | #21 selected model | #45 final run |
| --- | ---: | ---: |
| Missing-details exact agreement | 7/20 (0.350) | 8/20 (0.400) |
| Missing-details macro precision | 0.775 | 0.825 |
| Missing-details macro recall | 0.650 | 0.650 |
| Issue-type agreement | 13/20 (0.650) | 13/20 (0.650) |
| Known earlier issue retrieval recall | 0.600 | 0.600 |
| Duplicate/nonduplicate exact judgment | 0.421 | 0.421 |
| Structural citation validity | 1.000 | 1.000 |
| Type / duplicate abstention appropriateness | 0.850 / 0.950 | 0.850 / 0.950 |
| Model validation failures | 1 | 1 |
| Transport / integrity / scoring errors | 0 / 0 / 0 | 0 / 0 / 0 |

Only #12053's missing-details score changes. Its two redundant historical
requests disappear and its citation count falls with them; other cases retain
their field scores. The rendered user paste formerly produced four redundant
requests; both real HTTP and browser checks now show none. Historical retrieval
uses the verified earlier catalog, whereas the separate live numbered browser
check searches GitHub's broader current history; those candidate sets are not
interchangeable.

The known failure on #12216 remains: the model suggests `type: bug` using a quote
without an acceptable unnegated bug cue. Server validation rejects the selection,
marks the trace event as an error, abstains and returns a partial report. The
transport succeeded; this is still counted as a model validation failure.
Other representative gaps remain: #7312's duplicate is treated as related;
#12072 misses expected bug details; #12079 requests a use case already present.
These are not resolved by this focused fix.

Semantic citation support, usefulness of draft replies, unreviewed retrieved
relationships, and abstentions outside the explicitly scored fields still need
human review. Structural citation validity is not semantic correctness. All
quality observations remain provisional on the same small, previously reviewed
selection set, rather than independent generalization evidence.

## Serving and browser observations

Final serial run: mean model-call latency **842.20 ms**, median **692.99 ms**,
nearest-rank P95 **1,103.75 ms**, maximum **3,547.65 ms**. Mean end-to-end replay
latency is **932.24 ms**; warm-up is **2,755.41 ms**. Maximum input is 14,487 tokens.
Peak sampled device memory during cases is **2,740 MiB**, on the previously
verified 8,151 MiB GPU. Ollama reports the alias resident entirely in VRAM with
context 16,384. Sampling every 500 ms includes other device use and can miss
brief peaks. Warm caches, model residency and changing laptop conditions make
these observations unsuitable for claiming a speedup from the rule change.

[Real fixed-report HTTP checks](issue-45-api.json) use the verified raw opening
and the user's rendered paste. Both have real token-bearing model traces and
no redundant requests. The final [Chromium browser check](issue-45-web-final.json)
submits the rendered body through the bounded-agent form, retrieves its matching
trace and verifies the visible `Missing report details: None`, complete status,
two successful model calls and no JavaScript errors. Its trace takes 892.17 ms.
The report-only screenshot avoids republishing the contributor's complete body.
Body hashes identify the temporary inputs; bodies are not added as fixtures.

Those final checks omit the issue number to isolate detail recognition; the
expected no-number duplicate/related abstentions remain visible. The separate
[numbered live browser check](issue-45-web.json) also returns no missing details,
but takes 23,313.52 ms, including 20,970.03 ms searching 784 earlier issues.
It used the initial fix before the final boilerplate guards; it is retained as
live-search evidence, rather than evidence that retrieval became faster. The
final frozen twenty-case run supplies the numbered check on the final rules.
The broader #6–#15 bounded-agent behavior mapping remains in [#21](issue-21.md).

To reproduce after following the Windows/WSL setup guide, run in the **WSL
application environment**, using the currently verified Windows adapter address
and a new output path:

```bash
UV_CACHE_DIR=/tmp/issue-45-uv-cache uv run --locked --no-env-file \
  python -m maintainer_copilot.local_evaluation \
  --ollama-url http://172.17.48.1:11434 \
  --model pytest-triage:coder3b-ctx16k \
  --output /tmp/issue-45-new-results.json
```

GitHub access and the running Windows Ollama server are required. Rediscover the
adapter address after a network restart; do not substitute WSL localhost without
checking connectivity. Existing output paths are refused to preserve evidence.

## User-operated confirmation

After restoring the stopped application server, the user refreshed the Windows
browser and submitted the rendered #12053 report again. Their pasted report
shows complete status, `type: enhancement`, no missing details, and no redundant
detail requests. The matching trace
`7795db58-8eb5-46be-a0c3-1359ad965a4e` was independently retrieved from the local
API and is preserved in [the user-validation record](issue-45-user-validation.json).
Report fields are transcribed from the user's paste; this is not an additional
frozen historical evaluation case or human approval of the suggested relationships.

The trace records three successful real model calls totaling **1,557.49 ms**
within **27,217.07 ms** overall. The uncached earlier-issue search takes
**24,604.01 ms** for 784 results and returns five candidates to the report.
Their relevance, semantic citation support and draft usefulness still await
review; GPU memory was not sampled for this user-operated run. Search performance
and the heuristic relationship explanations remain separate from this detail fix.

## Human review of saved replies

[The human-review companion](issue-45-human-review.json) annotates the final
selected-model run without changing its raw outputs or expected outcomes. It
records source-artifact, report and draft hashes, the model identity/settings,
and the requesting user's explicit rating, verbatim reason and recording time.
These ratings apply to complete application replies from this specific run;
they do not automatically transfer to #21 comparator runs or controlled baselines.

Progress: **1 of 20 reply-usefulness reviews complete; 19 pending**. For #7312,
the user rated the exact saved reply **partly useful**: #349 is a promising
fixture-derived-parameter lead, but the explanation relies on generic word
overlap, does not explain a potential duplicate, fails to distinguish #2959's
regression, includes apparently unrelated #7012, and gives no clear next step.

The user saw paraphrases of hash-verified opening texts, the exact saved draft
and a report summary in chat. Later activity was excluded. This is a recorded
user judgment, not a claim that the reviewer independently fetched every source.
Citation support, separate relationship labels and other-field abstention
judgments remain pending; comments within the usefulness reason are preserved
without silently converting them into those additional labels. The source
results JSON retains its original pending-review fields; the companion records
the subsequent human review.

## Review

### Standards

No documented-standard violations. The reviewer verified all 53 preserved
hashes and confirmed the changes respect the glossary and historical-evaluation
ADRs. One optional Duplicated Code judgment remains: two alternative checks use
the same sentence-splitting expression. A helper can be considered if segmentation
changes; it is not a blocker for this focused correction.

### Spec

The first review found two gaps: negative/proposed `workaround is …` statements
bypassed filtering, and instruction prompts counted as answers outside the
alternatives section. Regression tests reproduced both before correction.
The second review independently checked the original counterexamples through
both APIs with plain and Markdown headings and confirmed both findings resolved.
The final real-model run, HTTP and browser artifacts were then refreshed.
Earlier [HTTP](issue-45-pre-review-api.json),
[browser](issue-45-pre-review-web.json) and
[screenshot](issue-45-pre-review-web.png) evidence is retained separately.

Final review: Standards — zero violations, one optional maintenance judgment;
Spec — zero unresolved findings.
