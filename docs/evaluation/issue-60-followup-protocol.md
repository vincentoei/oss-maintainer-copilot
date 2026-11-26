# Issue #60: quote-selection contract correction

The original frozen before/after comparison is complete and remains unchanged:
100 dispatches, 29/50 correct types before and 14/50 after, with 19 after responses
rejected by validation. The direct quote-generation interface asked the selected
3B model to copy exact text; observed outputs paraphrased the issue or copied
reply statements instead. This is a negative contract result, not a justification
to relax quote provenance, repair outputs or alter expected outcomes.

The authorized implementation continues with one separately frozen contract
correction and **at most 50 additional local dispatches**, one per original case.
Total disclosed issue #60 inference budget is now **150**. Do not rerun either
original phase. Keep the same Qwen model, quantization, 16K context, seed and all
serving settings. Retain temperature 0, 256 output tokens, 20-second timeout,
65,536 response bytes, no warm-ups, retries, repairs or subsequent model search.

Offer all resolved repository labels plus null independently of quote selection.
Offer up to sixteen exact issue excerpts, each at most 160 characters, extracted
without using labels, expected outcomes or lexical cues. Include the opening and
sample long inputs evenly through the final excerpt; the complete original title
and body remain in the input. The model selects a quote index, and the client
maps it to the original excerpt before the existing provenance/label/citation
validator. Reject out-of-range, boolean or malformed indices and inconsistent
null pairs. Never substitute a quote or label after an invalid response.

This bounds extra context and guarantees copied provenance for valid indices;
it does not guarantee that a sampled excerpt semantically supports a type.
Sampling can omit the best explanatory passage. Keep those semantic limitations,
negation, uncertainty and usefulness judgments explicit. Do not couple particular
labels to particular excerpts or add per-case heuristics.

Reuse the user-confirmed synthetic expectations, add regression coverage for
independent label/quote selection and invalid indices, and complete review and
checks before this pass. Reacquire and verify the same fifty public openings and
pinned evidence; flag changes, preserve every row, and compare identical complete
pairs separately from the full fifty-case denominator. Verify exact identity,
version, template and settings against the first pass before dispatch.

Publish the original failure and this follow-up side by side. Preserve all prior
artifacts, source freezes, annotations and reviews. This follow-up is a declared
extension made before new inference, not a reinterpretation of the first pass's
no-tuning protocol. Stop after the fifty-case follow-up and report regressions or
remaining failures honestly; fresh report ratings remain pending.
