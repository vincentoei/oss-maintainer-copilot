# Issue 59 targeted selection experiment

Application baseline cac83fe on the stacked #20/#60 branch. #59 covers
documentation defects versus requests for usage help. The wider 21-error
inventory is descriptive only. No broader classifier change or 50-case rerun.

Use the #60 follow-up fixed predictions for pytest 10156, 12189, 12228, 12287,
12298, 12360, 12377 (all four docs disagreements or focal docs case, plus three
distinct support questions). Require the reconstructed prompt, schema and input
hashes to match before sending the one candidate on any historical fixed case.
Run both arms on the actual bounded-agent historical replay of 12377 with the
full original candidate catalog. Use four short synthetic fixed-triage probes
as two matched pairs in both arms. The probe texts and intended types in
probes.json are investigator-designed diagnostic hypotheses without independent
review. Score them separately. Never send the intended types to the provider.

One predeclared candidate adds this trusted instruction to report selection only:

> If the requested change is to correct or complete published instructions, classify the report as documentation. If the reporter wants help applying the instructions to their own situation, classify it as a question. A question can point out a documentation defect, and a usage question can cite documentation.

Retain the #60 indexed excerpts, schema, sources, abstention and validators.
No decoder, planner or evidence changes. Same Qwen digest, template, Ollama
version and parameters as the #60 follow-up freeze; 256 tokens, temperature 0,
20 seconds, 65536 response bytes. Read-only identity checks, no warm-up.
At most 23 local dispatches: 7 historical candidate, 8 synthetic, at most
4 per agent run in two arms. Charge before dispatch, no retries, repairs,
replacement cases, budget extensions or alternative prompts. Local model API
cost cap USD 0; hardware and electricity unmeasured. Use fresh run directories.
The freeze commit pins the runner, texts, candidate, catalog and application.

Retain this candidate only if it gains historical fixed agreement without a
paired regression, returns docs on both focal paths, and gets both sides of
both synthetic contrasts right. An incomplete or mixed result warrants leaving
the application at #60. This targeted set cannot establish a new 50-case score,
generalization, independent semantic support, or usefulness.
