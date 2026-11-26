# Downloaded-model compatibility on the 8 GB laptop GPU

The RTX 5060 Laptop GPU had 8,151 MiB total and 7,883 MiB free before inference. Windows Ollama 0.40.16 served two pinned Q4_K_M artifacts on the local adapter. The two artifacts total 7,911,330,439 payload bytes across their manifest configurations and layers, before cache reuse and transport overhead. Each parent was checked against its full registry SHA-256 after the pull. Each experiment-only child alias retained the parent template, capabilities, renderer and parser. [Host snapshot](run/host.json) · [Exact artifact pins](research.md) · [Pull and settings freeze](preflight.json)

The four charged requests use one unscored synthetic opening through public fixed triage. The ordinary request matches the production JSON Schema and validator. The second request changes only the OpenAI-compatible transport field `reasoning_effort` to `"none"`. Both use 16,384 context, temperature 0, seed 42, top-k 20, top-p 0.8, repeat penalty 1, presence penalty 0, 256 output tokens and the production 20-second timeout. There is no input from the two scored cohorts. [Frozen wire hashes](requests.json)

## Gemma 4 E2B

The first request reached the 20-second deadline before the server reported a resident model. That consumed its slot and produced no response for validating JSON or measuring thinking. The next request started with 1,922 MiB sampled used and no alias yet listed, consistent with the preceding load still in progress, returned HTTP 200 after 17.16 seconds, stopped after 28 completion tokens, and passed the application's validator. It returned no exposed reasoning. The alias advertises thinking enabled by default and allows true/false; its packaged three-token speculative draft was active. This order cannot isolate thinking as the cause of the first failure. [Alias and modes](run/gemma4/alias.json) · [Ordinary call](run/gemma4/application.json) · [Explicit-off call](run/gemma4/reasoning_effort_none.json)

After the successful request, Ollama reported 16,384 context and equal GPU and total runner size (404,215,561 bytes). The 500 ms device sampler peaked at 3,276 MiB. The resident Windows process confirmed a single 16,384-token slot and showed 3,264 MiB of dedicated GPU memory plus 2,454 MiB of shared memory. Treat the Ollama ratio as its reported model-layer placement. Its byte count under-reports device use on this run. Shared allocations cannot identify which individual weights, host buffers or caches occupy them. Ollama's implementation can report equality from parsed layer placement or a file-size fallback. Physical residency of every tensor is unverified. [Windows runner counters](run/gemma4/windows-gpu.json) · [Ollama 0.40.16 memory accounting](https://github.com/ollama/ollama/blob/v0.40.16/llm/llama_server.go#L2809-L2850)

## Qwen3.5 4B

The alias also advertises thinking on by default. The ordinary, cold request returned HTTP 200 after 14.05 seconds with 1,166 characters in the separate reasoning field, an empty content string and `finish_reason: length` at all 256 completion tokens. The application correctly rejected it. With thinking explicitly disabled, the resident alias returned HTTP 200 and stopped with valid JSON in 25 tokens, zero exposed reasoning and 451 ms. Ollama reported 402 cached prompt tokens on this second request, limiting the latency comparison. Both requests showed 16,384 context and equal GPU and total runner size (3,650,124,512 bytes). Peak sampled device use was 4,270 MiB. Windows confirmed one 16K slot with 4,255 MiB dedicated and 650 MiB shared GPU memory. [Alias](run/qwen3.5/alias.json) · [Ordinary call](run/qwen3.5/application.json) · [Explicit-off call](run/qwen3.5/reasoning_effort_none.json) · [Windows counters](run/qwen3.5/windows-gpu.json)

## Eligibility and limitations

| Candidate | Ordinary application request | Explicit-off request | Proposed comparison |
|---|---|---|---|
| Gemma 4 E2B | Cold timeout; JSON and thinking behavior unobserved | Valid, stopped, no exposed reasoning, 16K GPU placement reported | Include with explicit-off |
| Qwen3.5 4B | Length limit, reasoning, empty final content | Valid, stopped, no exposed reasoning, 16K GPU placement reported | Include with explicit-off |
| Ministral 3 8B | Registry and hardware estimate only | Unmeasured | Defer; estimated weights plus 16-bit KV already exceed observed free VRAM before scratch space |

No score, semantic-support rating or reply-usefulness rating is assigned to the probe. Both primary candidates served a short text request with a 16K allocation. Long-issue tokenization, cold-start reliability, repeated latency and absence of physical memory spill remain unverified. The proposal keeps the application default and the #62 experiment intact and charges the 7B comparison to a new ledger. [Optional-candidate calculation](research.md#optional-ministral-fit-screen) · [Scored-phase proposal](comparison.md)

## Validation

Freeze commit `83c28e5` pins the downloads, settings, probe input, no-retry call caps and zero API fees. Commit `761145e` pins all four wire hashes. Independent review before inference led to recording provider bytes, surfacing pre-dispatch errors, and checking the frozen application source and aliases. All four reservations were dispatched exactly once with runner `73f4b45`. One timed out. The three provider envelopes can be fed back through the application without network access:

```sh
PYTHONPATH=src .venv/bin/python scripts/downloaded_model_verify.py
```

The four earlier #20/#59/#60 audits passed. The #62 verifier passed and its JSON scorecard recomputed byte for byte. The application suite passed 504 tests with two opt-in tests skipped. Ruff lint, format and mypy passed.
