# Issue 59 — documentation defect or usage question?

**Keep the #60 classification contract.** On the same Qwen, a single added
instruction distinguishing correction of published guidance from help applying
it changed zero labels. The focal docs prediction survived historical agent
replay, but failed to generalize to a closely related migration-guide defect.
This supports declining this particular prompt change. It leaves the measured
50-case application agreement at 29/50.

## What the unchanged aggregate hides

The model chose bug or enhancement on 48/50 reports. Seven expected questions
and seven expected regressions became bug, accounting for 14/21 disagreements.
Of the six regressions from the old contract, four chose a type previously
unavailable for that issue and two chose an alternative already available.
Some useful quotes were omitted, some were offered and ignored, and some
openings leave the desired classification open to interpretation. The full
opening was present in every request. The [21-case diagnosis](issue-59/remaining-errors.md)
accounts for all six regressions and distinguishes those explanations.

The old-contract #20 references selected docs for pytest #12377 across all
three hosted models. The same local Qwen selected docs under #60. Neither
result establishes a general gap in model capability. #20 owns the capped
hosted reference and #60 owns reachability and validation. #59 owns this
docs/question diagnostic and permits a recorded negative result. Taxonomy-wide
policy, changing the quote sampler and model comparison are outside this ticket.

## Deterministic reproduction

Before testing a correction I replayed Qwen's saved selection through the
original public model encoder and validator. The opening hash, system prompt,
encoded data and response-schema hashes all matched the recorded request. The
docs expectation failed on aa95999: index 1 selected question from three
label/quote pairs. The paired snippet described the guide “showing how to
rewrite” a condition. Index 0 offered docs from the title and index 2 offered
removal from the obsolete API. The word “how” described the guide's content.
The #19 post-quality agent and fixed final requests also have the same three
hashes and returned the same index. On the #60 follow-up the same assertion
passes: Qwen selected docs and independent quote index 0, the title. No
evidence was repaired. The focal case has no missing report details across
the archived and new completed workflows.

Reproduce from the repo root with the existing virtual environment. The fetch
only reads public issue text. The first playback intentionally exits with
`AssertionError: type: question`; the second succeeds. The last command audits
the paired experiment offline.

```sh
tmpdir59=$(mktemp -d)
git archive aa95999 src | tar -x -C "$tmpdir59"
gh issue view 12377 --repo pytest-dev/pytest --json title,body > "$tmpdir59/opening.json"
PYTHONPATH="$tmpdir59/src" .venv/bin/python scripts/issue59_reproduce.py before "$tmpdir59/opening.json"
PYTHONPATH=src .venv/bin/python scripts/issue59_reproduce.py followup "$tmpdir59/opening.json"
PYTHONPATH=src .venv/bin/python scripts/issue59_verify.py
```

## Predeclared candidate and paired results

Commit ed5be65 froze the [protocol](issue-59/protocol.md), [two synthetic
contrast pairs](issue-59/probes.json) and evaluator before dispatch. Historical
fixed baselines reuse #60 outputs after matching all seven encoded requests.
Candidate inputs and schemas match baseline hashes; only the report system
instruction changed. Both agent arms actually chose a historical search, then
finish, then a report. The same full 50-case catalog determined eligible earlier
issues for each historical replay. Results use pre-cutoff evidence.

| Workflow and case | Expected | #60 contract | Candidate |
|---|---|---|---|
| Fixed historical 10156, 12228 | docs | enhancement | enhancement |
| Fixed historical 12189, 12287, 12298 | question | bug | bug |
| Fixed historical 12360 | docs | bug | bug |
| Fixed historical 12377 | docs | docs | docs |
| Bounded agent 12377 | docs | docs | docs |
| Contradictory guide settings, asks to reconcile | docs | docs | docs |
| Same settings, asks how to apply them | question | question | question |
| Migration page recommends removed helper, asks to update example | docs | bug | bug |
| Working migration example, asks where to invoke helper | question | question | question |

The candidate retained **1/7** historical fixed, **1/1** focal agent and **3/4**
synthetic types. Zero gains, regressions, type abstentions, or validation/model
errors in the paired sets. Synthetic intents were declared by the investigator.
Notably, the obsolete-helper probe had only two options for quoting; the model
selected the entire body including the requested text correction, then assigned
bug. Resampling quotes cannot supply more relevant evidence in that example.

[Per-case reports](issue-59/run/results.json) and adjacent per-call records
retain prompts as hashes, selected indices, token counts, and mapped quotes.
The [serving preflight](issue-59/run/serving.json) verified the pinned Ollama
model, digest, template, version and settings. Baseline used 7 dispatches
(3,155 input / 180 output tokens); candidate used 14 (13,155 / 401). Total
21/23 local calls, USD 0 model API cost, no retries or hosted requests.
The separate #60 history still contains its 100 initial and 50 extension calls.

## Acceptance and limits

| #59 criterion | Evidence |
|---|---|
| Reproducer and counterexamples before correction | Hash-matched red/green playback above, frozen matched pairs, preserved responses. The red checks the historical semantic disagreement after successful mechanical validation. |
| General bounded diagnosis | One instruction on requested action; no case-specific application logic. It failed both the historical-gain and synthetic-pair adoption requirements. |
| Before/after and guardrails | Table and offline verifier; public-boundary guardrail tests in test_semantic_classification.py cover foreign types, invalid indices/null pairs, fabricated quotes, extra fields and unknown citations. A real but irrelevant quote can still pass. |
| Preserve inputs and prior measurements | All additions since cac83fe are evaluation scripts or new #59 artifacts. No prior case, cutoff, outcome, report, hosted ledger or source was edited. Existing #60 and both #20 offline audits pass. |
| Capped, frozen, targeted inference | ed5be65 pins source, comparison, settings and cap. No broader inference occurred. |

The seven historical cases were selected for diagnosis after seeing #60.
The two synthetic pairs deliberately share vocabulary and have no independent
ratings. No fifty-case candidate score, model promotion, or fresh human
judgment of reply usefulness or semantic support follows from this comparison.
