# Review of actual generated reports

Start with [reports.md](reports.md). Its 53 codes hide the model and application
method. Review the complete input, suggested type, selected quote and draft reply
for each code. Do not consult `key.json`, the run results or the scorecard while
rating. Model identities are revealed only after ratings are recorded. This is
method hiding, not a claim that the reviewer has never seen the cases or results.

Record the actual reviewer, a reason, and these four judgments per report:

| Field | Rating |
| --- | --- |
| Semantic type support | yes / no / uncertain: does the opening support the suggested type or a null abstention? |
| Quote relevance | yes / no / uncertain; use not-applicable for a justified null type/quote. Exact copying alone does not establish relevance. |
| Unsupported claims | yes / no / uncertain: does the draft assert facts not supported by its input and cited evidence? |
| Reply usefulness | 0: unhelpful or misleading; 1: safe but limited; 2: useful, relevant next action. |

Use text such as `R01: type=yes; quote=yes; unsupported=no; usefulness=1;
reason=...`. Ratings belong to that report fingerprint, not to its model or to a
different report with the same label. Do not copy expected-type confirmations or
earlier report ratings. All entries in [ratings.json](ratings.json) are pending;
they currently contain no human judgment or inferred reviewer attribution.

The twelve fresh synthetic openings appear directly in the sheet. Integration
inputs are linked from each relevant entry. Historical inputs retain their
original cutoff and hash in [request-preview.json](../request-preview.json).
The exact three retained historical openings are available locally in the ignored
`.local/issue63-review-openings.md`; contributor bodies are not republished here
under ADR-0003. Do not use later issue edits, comments or labels as opening evidence.

The full saved reports include citations and context. The sheet displays the
classification, quote, reply and citation references for assessment. Candidate
review must include its integration reports; a comparison of usefulness also
needs the matched control ratings. Missing reviews remain unresolved and cannot
pass the frozen promotion gate. No automated agreement score fills these fields.
