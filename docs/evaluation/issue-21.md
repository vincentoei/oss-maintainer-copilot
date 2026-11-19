# Issue #21: local model selection and serving

Selected **Qwen2.5-Coder-3B-Instruct, GGUF Q4_K_M, 16,384-token context**, served
by Windows Ollama 0.40.16 to the WSL application. The 3B and 4B candidates both
matched 13/20 reviewed issue types; the 3B model used less GPU memory and had
lower observed latency. These results establish a measured local selection,
not independent semantic review or generalization beyond this small selection set.
The full workflow comparison remains #16; second-repository support remains #33.

## Acceptance evidence

| Issue #21 criterion | Evidence | Result and limits |
| --- | --- | --- |
| Recorded llmfit shortlist fits the 8 GB GPU; task and serving measurements select the model | [llmfit output](issue-21-llmfit.json), [three-model results](issue-21-results.json), [selection manifest](issue-21-selection.json) | Three explicit Q4_K_M candidates fit and were measured on all twenty cases; selection uses quality, latency and actual GPU use |
| Selected model serves the existing API and web report; quality, latency, errors and GPU memory are recorded | [final integration](issue-21-integration-bounded.json), [browser evidence](issue-21-web.json), [screenshot](issue-21-web.png), field metrics below | Real fixed reports complete; bounded report preserves source/docs but is partial on the broad search; one selected-model historical response fails validation |
| Reproducible local run records model version/quantization without a paid API | [Windows/WSL run guide](../local-model.md), [Modelfile](../../models/pytest-triage.Modelfile), exact digests below | Local API, cloud disabled, no model API key; rediscover the current WSL adapter address after a network restart |

Started from updated `main` at `6c37e0e` on branch
`feat/issue-21-local-ollama`. Read AGENTS.md, the issue specifications #6–#16/#33,
the glossary, ADRs 0001–0003 and all four reviewed case batches before changing
the evaluation. Existing case metadata and baseline artifacts are unchanged.

## Verified environment and connectivity

| Measurement | Observed value | Verification |
| --- | --- | --- |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU | Host-access `nvidia-smi`; Windows llmfit; Ollama startup |
| VRAM | 8,151 MiB total | `nvidia-smi`; Ollama reported 8.0 GiB total and 6.9 GiB available at discovery |
| NVIDIA driver | 592.01 | `nvidia-smi`; Ollama used CUDA, compute capability 12.0 |
| CPU | Intel Core Ultra 7 255HX, 20 reported cores | Windows llmfit `system --json` |
| Windows physical RAM | 16,573,128,704 bytes, about 15.44 GiB | `Get-CimInstance Win32_ComputerSystem` |
| Available Windows RAM | About 1.8–2.2 GiB during setup | llmfit and `Win32_OperatingSystem.FreePhysicalMemory`; transient, distinct from total RAM |
| WSL memory limit | 12,249,832 KiB | `/proc/meminfo`; distinct from Windows physical RAM |
| OS | Windows 11 Home Single Language; WSL2 Linux x86_64 | Windows CIM; kernel `6.6.87.2-microsoft-standard-WSL2` |
| Windows PowerShell / WinGet | 5.1.26100.9818 / 1.29.380 | Direct executable version checks |
| llmfit / Ollama | 1.1.10 / 0.40.16 | Executables; Ollama API independently agrees |
| WSL Python / uv | 3.12.3 / 0.11.14 | Executable version checks |
| Browser verification | Playwright 1.65.1; Chromium 159.0.8154.6 | Actual browser process and package metadata |

Ollama runs on **Windows**, from `%LOCALAPPDATA%\Programs\Ollama`, with model
storage under `%USERPROFILE%\.ollama\models`. The application runs in **WSL**.
Initially Windows `127.0.0.1:11434` worked while WSL localhost refused the
connection. Windows confirmed Ollama listened only on loopback. WSL's measured
default gateway and Windows WSL adapter both resolved to `172.17.48.1`.

After the user quit the tray app and started Ollama bound specifically to that
adapter, WSL `/api/version`, `/api/tags` and `/api/ps` all returned HTTP 200.
No firewall change was made. Windows also returned HTTP 200 from the WSL app at
`http://127.0.0.1:8000`. `MODEL_BASE_URL` is explicitly
`http://172.17.48.1:11434/v1`; WSL localhost is not assumed to reach Windows.
The user-started server sets `OLLAMA_NO_CLOUD=1`, `OLLAMA_NUM_PARALLEL=1` and
`OLLAMA_MAX_LOADED_MODELS=1`. Startup logs confirmed cloud was disabled and the
Intel integrated GPU was excluded. Server defaults do not replace each alias's
verified 16K context.

## llmfit shortlist and selected identity

Read the current official [installation/usage](https://github.com/AlexsJones/llmfit),
[CLI](https://github.com/AlexsJones/llmfit/blob/main/docs/cli.md) and
[provider](https://github.com/AlexsJones/llmfit/blob/main/docs/providers.md)
documentation, then checked installed 1.1.10 help before choosing flags.
Default recommendations pooled 7.96 GiB NVIDIA and 2 GiB Intel memory. That is
unsuitable for this NVIDIA-only Ollama run; subsequent probes explicitly use
`--memory 7.96G`. Some initial recommendations were AWQ/GPTQ/vLLM or third-party
variants rather than corresponding Ollama GGUF artifacts; they were not selected.

| Upstream candidate / explicit Ollama tag | Q4_K_M, 16K estimated minimum VRAM, llmfit-reported GB | Observed GPU fit |
| --- | ---: | --- |
| Qwen/Qwen2.5-Coder-3B-Instruct / `qwen2.5-coder:3b-instruct-q4_K_M` | 2.85 | Fully GPU resident |
| Qwen/Qwen3-4B-Instruct-2507 / `qwen3:4b-instruct-2507-q4_K_M` | 5.08 | Fully GPU resident |
| Qwen/Qwen2.5-Coder-7B-Instruct / `qwen2.5-coder:7b-instruct-q4_K_M` | 5.79 | Fully GPU resident |

The raw artifact preserves the original 8K probes and exact 16K `plan --quant
Q4_K_M` outputs. Those estimates are separate from measured inference; llmfit's
preferred Q8_0/Q6_K quantizations were not substituted for downloaded Q4_K_M
weights. The explicit Qwen3 **Instruct-2507** tag avoids accidentally using the
unqualified `qwen3:4b` thinking variant.

Selected source manifest digest:
`f72c60cabf6237b07f6e632b2c48d533cef25eda2efbd34bed21c5e9c01e6225`.
Selected GGUF blob SHA-256:
`4a188102020e9c9530b687fd6400f775c45e90a0d7baafe65bd0a36963fbb7ba`.
Serving alias: `pytest-triage:coder3b-ctx16k`, manifest digest
`3831e8788ccb3dbe0a6510820b4c4807c7179ca34065d4aef9cc92c44c7fdad8`.
It is the 3.1B-parameter qwen2 family model, not an unspecified `latest` tag.
The selection manifest records every comparator's source/alias digests,
parameters and prompt-template hash.

All candidates use `num_ctx=16384`, temperature 0, seed 42, top-k 20, top-p 0.8
and repeat penalty 1.0. Report selection requests at most 256 output tokens,
uses JSON-schema output and retains the existing 20-second client timeout.
`/api/ps` confirms context 16,384 and equal resident size/VRAM size for each
model. This is evidence of full GPU residency, not CPU offload. The client source
hash is recorded with the final run. Backend/hardware nondeterminism and future
mutable registry tags prevent promising byte-identical responses.
The Windows CLI also recreated the checked-in Modelfile under a temporary alias;
[reproduction evidence](issue-21-reproduction.json) confirms its manifest digest
exactly matches the measured serving alias.

## Final twenty-case measurements

[The final run](issue-21-results.json) contains **60 real model calls and
responses**, twenty per candidate. Each model has 20 scoreable reports, zero
integrity/scoring errors, zero transport errors, and one rejected model selection.
“Completed” in the field scorer means scoreable; it does not imply successful
inference or a correct report. The runner separately records model-call errors,
raw selections, reports and traces so fallback output cannot hide a failure.

| Measurement | Coder 3B, selected | Qwen3 4B Instruct | Coder 7B |
| --- | ---: | ---: | ---: |
| Correct issue type | 13/20 | 13/20 | 12/20 |
| Model validation failures | 1 | 1 | 1 |
| Mean model-call latency, ms | 1,141.21 | 1,275.02 | 1,659.66 |
| Median model-call latency, ms | 695.58 | 994.47 | 1,376.74 |
| P95 model-call latency, ms, nearest rank | 1,132.40 | 1,806.53 | 2,171.81 |
| Real warm-up/load response, ms | 4,379.68 | 4,037.81 | 7,389.53 |
| Peak sampled device memory during cases, MiB | 2,740 | 5,002 | 5,356 |
| Maximum input tokens | 14,487 | 14,487 | 14,487 |

Case #12204 is the longest: selected-model end-to-end replay time was 9,568.38
ms. Mean selected-model replay latency was 1,237.56 ms. The runner first acquires
public evidence with a controlled integrity smoke, then reuses those reads while
revalidating every case before real inference. Timed cases therefore use warm
retrieval caches. Downloads were finished for the final run. These are serial,
observational laptop timings, not a controlled throughput/thermal benchmark.
Warm-up is a real short response before timing cases; it is not a quality case.
The 500 ms `nvidia-smi` sampler includes other device use and can miss brief peaks.
Warm-up samples can include the previously loaded model; the table uses case
windows after warm-up. CPU, electricity and network costs are excluded; model
API fees and public GitHub per-request fees are assumed zero.

| Selected report field | Result | Interpretation |
| --- | ---: | --- |
| Known earlier issue retrieval recall | 0.600 | Limited verified catalog, not full-history recall |
| Duplicate/nonduplicate exact judgment | 0.421 | Uncertain #12083 excluded; other retrieved relationships remain unreviewed |
| Issue type exact agreement | 0.650 | Human-confirmed outcomes; 7 incorrect/unknown results |
| Missing-details exact / precision / recall | 0.350 / 0.775 / 0.650 | Existing template rules, not model extraction |
| Structural citation validity | 1.000 | Boundary/wiring check; semantic support remains pending |
| Type / duplicate abstention appropriateness | 0.850 / 0.950 | Other-field judgments still require review |
| Generated reply usefulness | Pending | No invented numeric or model-judge score |

Duplicate retrieval/matching and missing-detail detection remain rule-based.
The model chooses a type and supplied reply statements. The unchanged #15
keyword baseline has type agreement 0.500 and the same retrieval, detail and
structural-citation metrics. This reference is not the three-workflow comparison
requested in #16. Earlier quality observations remain provisional; initial
controlled replays never become real-model quality evidence.

## Representative failures and preserved diagnostics

- **#10156:** selected question instead of docs; the opening's question-like
  wording competes with its documentation request.
- **#12189:** selected bug instead of question, quoting XML `errors="0"` /
  `failures="0"`. A literal cue can pass mechanical validation without providing
  a sound semantic reason for a bug label.
- **#12216:** chose bug with an enhancement quote option. The unchanged validator
  rejected the mismatch; the report is partial and type is unknown.
- **#12146/#12197:** abstained despite non-null expected types. The conservative
  lexical evidence boundary can prevent an otherwise plausible classification.
- **#12053:** requests already-present alternatives/use-case details. This is an
  existing rule failure retained in the scores, not attributed to the model.
- **#7312/#12083:** existing retrieval/judgment weaknesses remain. The uncertain
  #12083 pair is not converted into an exact-match win.

Preserved [3B](issue-21-coder3b-initial.json) and
[4B](issue-21-qwen3-4b-initial.json) initial runs each had 19 model errors and
only 1/20 correct types. Models supplied short label names or quotes that did
not satisfy the server's existing cue rule. A
[schema/regex prompt attempt](issue-21-qwen3-4b-schema.json) still had 18 errors.
The final client supplies mechanically valid, exact opening-text quote options
and constrains label/quote/citation values; it still asks the model to choose
semantically, and the server retains all original validation. Independent enums
do not guarantee a matching label/quote pair, as #12216 demonstrates.

An [8K diagnostic](issue-21-provider-error.json) returned HTTP 400 for #12204;
the server reported a 14,487-token request. No text was truncated or case
reannotated. The 16K final run obtains an actual response for that case from
every model. The [first API smoke](issue-21-api-initial.json) hit the 20-second
timeout; a [native diagnostic](issue-21-serving-initial.json) and
[warm retry](issue-21-api-warm.json) preserve subsequent behavior rather than
erasing the startup failure. Prompt/format refinements were informed by this
selection set, so its scores are not an untouched held-out generalization result.

## Integrity and focused integration against #6–#15

[Provenance](issue-21-provenance.json) records opening/candidate hashes, commit
timestamps, unchanged case-metadata hashes, pinned templates, prior artifact
hashes, and original transient read failures plus successful retries. All twenty
openings and every eligible catalog candidate passed hash/time checks. All 27
pinned templates were read; bug/feature hashes match reviewed template content.
Only hash-verified pre-cutoff openings, pinned docs/source and original issue
text enter historical requests. No expected outcomes, post-cutoff comments,
labels, closures, fixes or live CI results enter those requests. Contributor
bodies remain temporary acquisitions, not a new bulk publication.

| Issue behavior | Real evidence and bounded checks | Failure/gap |
| --- | --- | --- |
| #6 validated type and cited reply | Complete fixed API report/cited draft; rejected #12216 remains visible | Type agreement 13/20; semantic reply review pending |
| #7 two read tools, bounds, validation/injection | [Final agent run](issue-21-integration-bounded.json) reads source, attempts search, then finishes within four model calls; injection run uses finish plus final selection without fabricated reply/citation | Broad search exceeds GitHub's 1,000-result window, so the tool-assisted report is partial; no claim of an overall workflow advantage |
| #8 linked CI only | API/browser show 36 completed results for an explicit commit, including conflicting `codecov/patch` success/failure with separate citations; unlinked input has no CI retrieval event | Synthetic integration input checks wiring, not historical CI or a causal diagnosis |
| #9 traces and recovery | API/browser trace links, selected identity, token usage, timing/errors verified; failed search retains source/docs and cited reply | Process-local traces; no external tracing service or cross-worker persistence |
| #10–#11 frozen replay/reviewed outcomes | Twenty cases verify openings/commits before inference, preserving confirmed reviews and uncertain relationship | Published catalog and pinned evidence only |
| #12 independent field scoring | Existing scorer reused; raw selections, failures, latency and GPU samples | Semantic support, reply usefulness and other-field abstention review pending |
| #13–#15 all twenty cases | Each candidate has twenty real responses and scores; zero final integrity exclusions | Small selection set; outcome confirmation does not review generated reports |

[Initial agent traces](issue-21-integration.json) show string issue numbers
rejected before reads. A [typed-schema rerun](issue-21-integration-final.json)
read source but exhausted the step limit on repeated actions. The final decoder
is offered only exact unused actions/arguments already permitted by the server.
Server-side validation, output caps and step bounds remain unchanged.
Deterministic tests cover malicious/invalid output and dependency failures beyond
these real smokes; they are not additional quality cases.

The browser used the actual form/backend without response interception. All ten
DOM/API assertions passed, with no JavaScript errors. Windows also reached the
WSL app. [Browser JSON](issue-21-web.json) and the screenshot retain the exact
report/trace. No human is being credited with this check.

## Reproduce and review

Follow [the local run guide](../local-model.md) for exact Windows PowerShell and
WSL commands, expected results, troubleshooting and a new-path evaluation run.
The CLI refuses to overwrite an existing output artifact and checkpoints after
each completed model. Existing baseline artifacts are never its outputs.

Generated draft usefulness, semantic citation support, other-field abstention
appropriateness and other retrieved relationships await human review. Inspect
each selected-model case's `scores`, `report`, `model_calls` and `trace` in the
final JSON, follow citations, and record a separate reviewed rating/support
judgment. Leave expected outcomes and baseline artifacts intact. Codex cannot
supply an independent human judgment. Laptop reboot/restart behavior and
materially different memory/thermal conditions have not been retested.

Validation: the full deterministic suite passed **168 tests**, with two optional
live tests skipped. The separate real evaluation and HTTP/browser runs above
were executed, not inferred from those tests. Mypy, Ruff lint, Ruff format check,
JSON/link validation and unchanged-baseline hash checks passed.
