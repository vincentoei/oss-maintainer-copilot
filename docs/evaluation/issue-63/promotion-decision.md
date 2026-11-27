# Maintainer decision: recommend Qwen3.5 4B

After the comparison and independent AI review, the requesting maintainer agreed
to promote Qwen3.5 4B as the recommended local model configuration. The recorded
response was: “Okay i agree with your recommendation, so what should we do now?”
This followed an explicit recommendation to accept the known unsupported
regression quote and remaining uncertainty, preserve the failed gate result,
and keep 3B selectable for lower-memory use. [Machine-readable record](promotion-decision.json).

This is an explicit **post-result maintainer policy exception**, not a passing
result under the frozen promotion gates. The [original report](report.md),
[protocol](proposal.md), [scorecard](scorecard.json), [negative AI recommendation](review/codex-review.md)
and pending human ratings remain unchanged. The AI review is attributed to its
actual Codex reviewer; it is not represented as human review.

## Why accept the tradeoff

The candidate matched 12/12 user-confirmed fresh synthetic expectations against
8/12 for both controls, including explicit regressions and an appropriate null
abstention. The separately exposed historical benchmark also favored it overall,
but is not fresh generalization evidence. All eight bounded candidate application
checks passed on the tested laptop, and its measured resource use is practical
for this portfolio setup.

The independent review found two historical enhancement choices defensible
taxonomy ambiguities. R48's regression classification is still uncertain and
its quote does not establish a version break; R40's enhancement quote relevance
is uncertain. Those defects are accepted as known limitations of the selected
default, not repaired or relabeled by this decision. The incumbent also has
known classification and quote-support failures. The choice favors the observed
aggregate tradeoff rather than treating the current default as error-free.

Matched draft replies were identical across models, with no usefulness gain.
No claim of better reply usefulness, statistical generalization, semantic
certification or complete physical tensor residency follows from promotion.
Actual independent human report ratings remain unavailable. The maintainer
accepts the attributed AI review as decision input despite that gap; the
original human-review gate remains unpassed.

## What changes

The current README example and [local setup guide](../../local-model.md) select
`pytest-triage:qwen35-4b-ctx16k` with `MODEL_REASONING_EFFORT=none`. The new
[Qwen3.5 Modelfile](../../../models/pytest-triage-qwen35.Modelfile) records 16K,
Q4_K_M and the measured decoding parameters. Model use remains explicitly
configured with `MODEL_NAME`; the library's unconfigured abstention behavior
and historical evaluation harnesses are preserved.

The serving alias was copied from the already-installed
`triage-eval:qwen35-4b-16k-v1`, without downloads or model generation. Read-only
metadata verification established the same digest:

`8da535b12863762c2403ed06956d92da4e57806a4772ba321137a2809e9a8bbe`

Native template, renderer, parser, thinking configuration and GGUF/tokenizer
metadata match. Effective parameter names/values match; `/api/show` displayed
them in a different order for the copied alias. Thinking is disabled by the
application request setting, not by changing the native template.

The existing 55-call allocation remains complete. No new inference under the
copied name or new full benchmark was performed; the integration evidence is
for the identical artifact under its original evaluation alias. An existing
application process must be restarted with the documented settings; no running
app was restarted during this configuration change.

## Reversal and follow-up

`pytest-triage:coder3b-ctx16k` remains selectable by changing `MODEL_NAME` and
restarting the app. It is a lower-memory alternative, not an automatic semantic
fallback. Structurally valid but unsupported outputs do not trigger a model
switch, and simultaneous model residency was not tested.

Follow-up [#66](https://github.com/vincentoei/oss-maintainer-copilot/issues/66)
investigates evidence support for classifications and quotes;
[#67](https://github.com/vincentoei/oss-maintainer-copilot/issues/67) addresses
the shared reply-usefulness limitations. Preserve this decision and all
old scores when evaluating corrections. New model/prompt experiments require
their own reviewed cases and bounded execution approval; promotion authorizes
no additional benchmark calls or model downloads.
