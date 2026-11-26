# Issue #60: classification contract before/after

Freeze before inference. Compare the unchanged selected Qwen2.5 Coder 3B
Q4_K_M model (`pytest-triage:coder3b-ctx16k`, digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`)
on exactly the same fifty confirmed cases, candidate pools and historical cutoffs.
Read-only serving preflight verifies Ollama version, template, identity and
settings. Context 16384, temperature 0, seed 42, top-k 20, top-p .8,
repeat penalty 1; 256 response tokens, 20 s timeout, 65536 response bytes.

One before pass and one after pass, at most **100 model dispatches** total:
50 per phase, one per eligible case. No warm-up, retry, repair, model switch,
hosted inference, tuning from after-run results or case replacement. Freeze each
phase's source before dispatch. An existing output directory is refused and a
durable fsynced request ledger charges failures before HTTP. Preserve prior
catalogs, annotations, evaluations and hosted accounting byte-for-byte.

Acquire verified public openings and pinned repository evidence before inference,
record every changed/unavailable flag, and freeze shared reads and failures.
Use the actual encoder with an HTTP-free capture adapter to audit offered labels
before real inference. Expected outcomes are used only afterward for audit and
scoring. Report unreachable expected labels separately from model errors and
wrong selections, keeping all fifty rows and the same denominator. Uncertainty
is preserved and annotation discrepancies are disclosed rather than tuned away.

Retain request/response hashes, bounded raw outputs, reports, traces, token use,
latency and GPU telemetry/residency, recording unavailable measurements explicitly.
Keep keyword-rule reports separate; their field results must remain unchanged.
Field aggregates on successful model reports exclude failed-call fallbacks and
state their denominators; compare complete pairs separately from full catalogs.
No perfect score, model promotion or improvement is required.

The after contract permits semantic selection from valid repository labels with
a genuine bounded issue-text quote, or explicit abstention. It preserves schema,
label allowlists, exact quote provenance, citation-ID validation, bounded tools
and read-only behavior. A lexical cue no longer proves or gates classification;
semantic fit of the type/quote remains a model judgment requiring human review.
Document the changed guarantee and misleading/negated-text limitations.

Regression tests use the agreed public model/triage and historical replay seams.
Four new synthetic examples were presented for user review before implementation;
the user explicitly answered "Confirm all four proposed types." Preserve the
original texts and attribution separately from generated model reports. These
are user-confirmed synthetic expectations, not fresh historical cases or a blinded
generalization test. Fresh generated-report
usefulness/semantic ratings also remain pending; never transfer old ratings.

Generate fresh review artifacts for the 100 measured reports. Publish per-case
gains, regressions, failures/abstentions, resource changes and limitations. These
already exposed development cases do not establish generalization; independently
reviewed new examples are separate evidence. The local model has zero marginal
API fees; electricity, hardware and total operating costs are not measured.
