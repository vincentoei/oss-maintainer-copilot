# Project brief: Open-source Maintainer Copilot

## Goal

Build a portfolio-quality AI system that helps a human maintainer triage incoming issues in public GitHub repositories, starting with [pytest](https://github.com/pytest-dev/pytest). Follow the six learning milestones below to experience applications, observability, inference and compute, training, infrastructure, and distributed inference. Report measured quality, latency, and cost; make no claim about maintainer time saved without a real user study.

The original #1 release was **pytest-first**. Issue #33 extends it to multiple registered public GitHub repositories through one shared triage path. Pytest's issue types and template interpretation stay in its profile; other repositories use bounded generic context and optional declarative configuration. Registration needs no per-repository Python or new evaluation cases. This capability does not establish usefulness for every project.

## User workflow

A user registers a public repository, selects it, and pastes an issue into the web UI or sends its registration identity to the Python/HTTP API. The system returns a structured **triage report** for human review:

- a suggested issue type using the selected repository's supported labels (pytest retains its existing `type:*` labels);
- ranked **duplicate candidates**, with related issues distinguished from substantially matching failures or requests;
- **missing report details** based on established requirements of the applicable repository template;
- a draft maintainer reply; and
- a citation for each factual claim, or an explicit **abstention** where evidence is insufficient.

The app reads public repository material. It does not post to target repositories, change labels, edit code, or run commands from issue text. Treat issue text and retrieved material as untrusted input. Validate tool arguments, report fields, and citations.

Issue #33 extends the original pytest-first release to multiple registered public
GitHub repositories in the local single-user app. Reviewers add a URL or
owner/repo, inspect bounded prepared context, select one target repository per
report, and explicitly refresh or remove registration. The existing pytest
adapter remains usable; new repositories use a generic profile and optional
declarative configuration without per-repository Python. Missing or unsupported
context limits conclusions and produces abstentions. Access to target repositories
stays read-only. See [repository setup and limits](repositories.md).

## System shape

- **Retrieval:** use bounded passages and earlier issues from one target repository. Explicit refresh updates live context; historical evaluation applies each case's evidence cutoff.
- **Workflow:** fixed legacy RAG with the selected Qwen2.5-Coder 3B remains the demo default after #16; the agent stays optional.
- **Agent:** one bounded agent may call two read-only tools: search earlier issues and inspect a repository file at a specified commit. Inspect CI only when an issue points to a relevant commit or PR. Limit tool steps and handle tool failures explicitly.
- **Output:** validate the structured report before display. Preserve evidence links and a trace ID so a reviewer can inspect how the report was produced.
- **Models:** keep the application model interface replaceable. Use [`llmfit`](https://github.com/AlexsJones/llmfit) to shortlist models for the laptop's 8 GB GPU, then choose using task evaluation and measured serving performance. Use a stronger hosted model only as a capped **quality reference**, never as the expected answer.

## Evaluation

Start with 20 human-reviewed **evaluation cases**, then expand toward about 50 held-out cases that include duplicates, nonduplicates, missing details, and ambiguous reports. Use explicit duplicate relationships or maintainer-linked duplicates as candidate positives and manually review both positives and negatives. A missing `closed as duplicate` label is not proof of a nonduplicate.

For each historical case, expose only evidence available when the issue opened. Use an unedited issue title/body or a manually verified original; exclude cases whose opening content cannot be reconstructed reliably. Pin docs and code to a commit before the issue's **evidence cutoff**. Keep later comments, labels, closures, and duplicate decisions out of model input, while allowing them to inform human annotation. Split training and evaluation chronologically, and keep each **issue family** in one partition. [ADR-0001](adr/0001-time-frozen-historical-evaluation.md) records the decision.

Publish issue IDs, cutoffs, commit SHAs, human-reviewed **expected triage outcomes**, and content hashes. Fetch public issue text when evaluation runs and flag a case if its content hash changes. [ADR-0003](adr/0003-publish-evaluation-metadata.md) records this publication choice.

Score duplicate retrieval, issue type, applicable missing details, citation validity, abstention, and draft-reply usefulness separately. Report both aggregate results and representative failures. Compare a keyword-search and rule-check baseline, a fixed RAG workflow, and the bounded agent. Keep the agent in the final demo only if its gain justifies its added latency and cost. Run deterministic schema, citation, and retrieval-fixture checks in CI; run full model evaluations on demand.

## Learning milestones

| Guide step | Build or experiment | Evidence to publish |
| --- | --- | --- |
| 1. Applications | Python API, thin UI, pytest retrieval, two read-only tools, validated triage report | Working local demo and sample cited reports |
| 2. Observability | Trace retrieval, model calls, tool calls, failures, tokens, and timing; create the first 20 reviewed cases | Trace examples and field-level baseline results |
| 3. Inference + compute | Serve the same selected open model through Ollama and vLLM on the RTX 5060 Laptop GPU; use the same request set and record any quantization difference | Time to first token, output speed, VRAM, quality, and error measurements |
| 4. Training | Fine-tune a small model with LoRA/QLoRA for structured issue type and missing-detail predictions; serve base and adapted versions | Held-out base-versus-adapter results, including a negative result if the adapter loses |
| 5. Infrastructure | Run indexing or evaluation as a GPU-aware Ray job locally; deploy the API or worker to local Kubernetes to practise scheduling, health checks, and updates | Reproducible deployment and failure/restart demonstration |
| 6. Distributed inference | In one prepared two-GPU rental, compare single-GPU vLLM, tensor parallel vLLM, and Dynamo prefill/decode on the same issue-request mix | Throughput, latency, errors, GPU use, and cost per setup, including regressions |

Historical pytest type labels are noisy training targets, not evaluation truth. Audit samples, exclude held-out cases, and keep the base model in the working app if LoRA does not improve the held-out task. [ADR-0002](adr/0002-reviewed-weak-labels-for-training.md) records the training-data trade-off.

## Budget and release boundary

Cap the two-GPU rental at **US$10** and hosted quality-reference API use at a separate **US$5**. Prepare containers, models, scripts, and request sets locally before renting. A two-GPU Pod is a candidate for the cloud lab; verify its actual price, availability, and driver compatibility before starting. Postpone the lab if a suitable pair is unavailable within the cap. The [RunPod pricing page](https://www.runpod.io/pricing) is a planning reference, not a locked quote.

Ray's local GPU job fulfills the guide's infrastructure option. Local Kubernetes practice can use a CPU service; GPU scheduling under WSL2 is an experiment, not a prerequisite for completing the path. The portfolio has no always-on GPU deployment.

Release each milestone in a runnable state. The public repository should contain setup instructions, an architecture diagram, sample reports and traces, reproducible evaluation commands and results, benchmark methodology, and a short demo recording. The [glossary](../GLOSSARY.md) defines the domain terms used here.
