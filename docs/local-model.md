# Local Ollama run on the Windows laptop

The recommended model is **Qwen3.5 4B Q4_K_M**, served as
`pytest-triage:qwen35-4b-ctx16k` with 16,384 context and explicit
`MODEL_REASONING_EFFORT=none`. Model suggestions remain explicitly enabled through
`MODEL_NAME`; starting the app without that setting still supports deterministic
triage with model abstentions.

The [maintainer decision](evaluation/issue-63/promotion-decision.md) accepts the
known quote-support and taxonomy tradeoffs after evaluation and an independent
AI review. This is a portfolio default, not a claim that every semantic safeguard
passed. The measured comparison and original negative promotion recommendation
are preserved. No new benchmark or model inference accompanied this change.

## Use the already installed, evaluated artifact

Use the Windows/WSL network and server setup in archived steps 1–4 below. Verify
the current Windows adapter address; `172.17.48.1` is the recorded address, not a
universal default. Ollama 0.40.16 was the measured version.

On the measured laptop, the evaluated alias already exists. In Windows PowerShell,
point the client at the verified server and copy its name:

```powershell
$env:OLLAMA_HOST = "http://172.17.48.1:11434"
$ollamaExe = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
& $ollamaExe cp triage-eval:qwen35-4b-16k-v1 pytest-triage:qwen35-4b-ctx16k
(Invoke-RestMethod "$env:OLLAMA_HOST/api/tags").models |
    Where-Object { $_.name -eq 'pytest-triage:qwen35-4b-ctx16k' } |
    Select-Object name,digest,details
& $ollamaExe show --parameters pytest-triage:qwen35-4b-ctx16k
```

The copied alias must retain digest
`8da535b12863762c2403ed06956d92da4e57806a4772ba321137a2809e9a8bbe`.
Do not overwrite a different existing destination alias. The serving name was
created and metadata-verified during promotion, without generation or download.
Copying an installed model uses [Ollama's copy operation](https://docs.ollama.com/api/copy).

If provisioning another machine, the source is `qwen3.5:4b-q4_K_M`, whose recorded
source digest is
`d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04`.
The [Qwen3.5 Modelfile](../models/pytest-triage-qwen35.Modelfile) defines the
settings for creating `pytest-triage:qwen35-4b-ctx16k`. It inherits the native
template/renderer/parser. Provisioning requires a separate download if the source
is absent; promotion did not perform one. Inspect source/artifact identity and
settings before calling a newly provisioned model equivalent to the measured one.
Do not assume a mutable source tag permanently identifies the same weights.

Expected effective parameters: `num_ctx 16384`, temperature 0, seed 42,
top-k 20, top-p 0.8, repeat penalty 1 and presence penalty 0. Qwen3.5's native
thinking default is true, so the application request setting below is essential.
Do not copy the archived 3B launch command or warm-up when validating this model.

## Start the recommended configuration

From the WSL checkout, use the verified current host address:

```sh
uv sync --locked --group dev
export MODEL_BASE_URL=http://172.17.48.1:11434/v1
export MODEL_NAME=pytest-triage:qwen35-4b-ctx16k
export MODEL_REASONING_EFFORT=none
uv run --locked --no-env-file uvicorn maintainer_copilot.web:app --host 127.0.0.1 --port 8000
```

These variables configure the launched process; restart an existing app with
these settings to switch it. Model downloads, a new inference run, and restarting
an unrelated running app were not part of the promotion's metadata verification.

Issue #63 exercised the identical artifact under its original evaluation alias
through Python, HTTP, real browser and bounded-agent final reporting. It recorded
4,276 MiB peak sampled device use, approximately 4.98 seconds for its first call
from empty residency, and 487 ms fresh nearest-rank p50 model latency. These are
measured serial-run observations, not capacity or latency guarantees. Physical
tensor residency, near-window behavior and model-driven search/inspect quality
remain limited as documented in the [report](evaluation/issue-63/report.md).

## Select 3B for lower-memory use

Keep the installed `pytest-triage:coder3b-ctx16k` alias. To select it, restart the
app using the same launch command with:

```sh
export MODEL_NAME=pytest-triage:coder3b-ctx16k
export MODEL_REASONING_EFFORT=none
```

Both arms were tested with this explicit-off setting. This is a manual model
choice, not an automatic semantic-error detector or a promise of simultaneous
GPU residency. The original [3B Modelfile](../models/pytest-triage.Modelfile)
and historical evaluation harnesses remain unchanged for reproduction.

## Archived issue #21 setup: Qwen2.5 Coder 3B

The steps below describe the original 3B setup and measurements. They remain
available to reproduce #21; the recommended configuration is the Qwen3.5 setup
above. In particular, the archived step 8 launches a real evaluation and is not
required to switch the application model.

This is the tested issue #21 setup: **Ollama on Windows; application in WSL
Ubuntu**. The selected model is `qwen2.5-coder:3b-instruct-q4_K_M`, served as
`pytest-triage:coder3b-ctx16k`. See the [measurements, limitations and acceptance
evidence](evaluation/issue-21.md) and [exact identities](evaluation/issue-21-selection.json).
No paid model API, API key or Ollama cloud model is required. Account sign-in is
not required for these local requests. Run each numbered step and check its
expected output before proceeding; the commands below label their environment.

### 1. Verify Windows hardware and tools

Use **Windows PowerShell**, not a WSL shell:

```powershell
$PSVersionTable.PSVersion
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv
```

The measured laptop has an RTX 5060 Laptop GPU, 8,151 MiB VRAM, driver 592.01
and 16,573,128,704 bytes RAM. Available memory changes; total Windows RAM and
the WSL memory limit are different quantities. If `nvidia-smi` is unavailable,
stop and inspect the Windows NVIDIA driver installation before inferring GPU fit.

The guided session installed llmfit 1.1.10 and Ollama 0.40.16 with WinGet:

```powershell
winget install --exact --id AlexsJones.llmfit --source winget
```

Expect successful installation. Reopen PowerShell after PATH changes, then check:

```powershell
llmfit --version
llmfit system --json
```

For Ollama, the separate installation step is:

```powershell
winget install --exact --id Ollama.Ollama --source winget
```

Expect successful installation. The GUI Apps screen does not need to launch any
integration. To bypass an inherited/stale PATH when checking installed versions:

```powershell
& "$env:LOCALAPPDATA\Microsoft\WinGet\Links\llmfit.exe" --version
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```

If a version differs from the recorded run, record it with new results; do not
claim the old benchmark was rerun unchanged. Consult installed `--help` before
using flags from newer documentation. Current official sources:
[llmfit installation/usage](https://github.com/AlexsJones/llmfit),
[CLI](https://github.com/AlexsJones/llmfit/blob/main/docs/cli.md),
[providers](https://github.com/AlexsJones/llmfit/blob/main/docs/providers.md),
[Ollama Windows](https://docs.ollama.com/windows).

### 2. Discover the Windows address that WSL can reach

In the **WSL application shell**:

```sh
ip -4 route show default
```

This session returned `default via 172.17.48.1 dev eth0 ...`. The `via` address
is the Windows host for this NAT setup. It can change after a WSL restart.
Do not substitute the DNS-tunneling nameserver from `/etc/resolv.conf`.

In **Windows PowerShell**:

```powershell
$wslAdapterAddress = Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.InterfaceAlias -like '*WSL*' } |
    Select-Object -First 1 -ExpandProperty IPAddress
$wslAdapterAddress
```

Expect the same address as WSL's default route. Stop if it is empty or disagrees.
The session measured one matching adapter at `172.17.48.1`.
[Microsoft's networking documentation](https://learn.microsoft.com/en-us/windows/wsl/networking)
explains the NAT/mirrored distinction. A successful Windows localhost request
does not prove WSL can use the same localhost address.

### 3. Start the Windows Ollama server

Quit the Ollama tray application first; closing its window alone may leave the
server running. Use **Windows PowerShell** and the address from step 2:

```powershell
$env:OLLAMA_HOST = "http://${wslAdapterAddress}:11434"
$env:OLLAMA_NO_CLOUD = "1"
$env:OLLAMA_NUM_PARALLEL = "1"
$env:OLLAMA_MAX_LOADED_MODELS = "1"
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

Expect `Listening on 172.17.48.1:11434` for the measured address and
`Ollama cloud disabled: true`. **Keep this terminal running.** These settings
are process-scoped. They do not change persistent user environment variables.
The selected alias sets context explicitly; the server's GPU-based default
context log is not proof of that alias's context.

If the address is already in use, quit the tray server and retry. If the address
is invalid, repeat step 2. A firewall prompt or failed cross-environment request
needs inspection; this run required no firewall change. Do not infer success
from the listener message alone. See [Ollama configuration](https://docs.ollama.com/faq).

### 4. Verify connectivity from the application environment

In **WSL**, set the address actually observed in step 2:

```sh
export OLLAMA_HOST=http://172.17.48.1:11434
python3 - <<'PY'
import json, os, urllib.request
for route in ("version", "tags", "ps"):
    with urllib.request.urlopen(os.environ["OLLAMA_HOST"] + "/api/" + route, timeout=5) as response:
        print(route, response.status, json.load(response))
PY
```

Expect HTTP 200 for all three; `/api/version` was `0.40.16`. Empty model lists
are normal before a download. Connection refused means the listener/address is
wrong or stopped; timeout can indicate binding/firewall/routing. Inspect the
actual Windows listener with `Get-NetTCPConnection -State Listen -LocalPort
11434` in another PowerShell. The tested app uses this explicit host URL, not
WSL `127.0.0.1:11434`.

### 5. Download and create the selected model

Open a **second Windows PowerShell**; leave the server terminal running. Set its
client address to the same verified adapter address:

```powershell
$env:OLLAMA_HOST = "http://172.17.48.1:11434"
$ollamaExe = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
& $ollamaExe pull qwen2.5-coder:3b-instruct-q4_K_M
```

Expect download progress, digest verification and success. Before comparing
against the recorded benchmark, inspect the source identity:

```powershell
(Invoke-RestMethod "$env:OLLAMA_HOST/api/tags").models |
    Where-Object { $_.name -eq 'qwen2.5-coder:3b-instruct-q4_K_M' } |
    Select-Object name,digest,details
```

Expected source digest:
`f72c60cabf6237b07f6e632b2c48d533cef25eda2efbd34bed21c5e9c01e6225`.
Quantization must be Q4_K_M. If the tag now resolves differently, stop treating
it as the same model and record/re-evaluate the new identity. Keep the downloaded
weights available for exact local reruns.

For this checkout, the checked-in [Modelfile](../models/pytest-triage.Modelfile)
is visible to Windows at the measured WSL path:

```powershell
$modelFile = '\\wsl.localhost\Ubuntu\home\vincentoei\projects\oss-maintainer-copilot\models\pytest-triage.Modelfile'
Test-Path $modelFile
```

Expect `True`; adjust the distro/checkout path if necessary, using WSL `wslpath
-w <absolute-Modelfile-path>` to discover it. Then create the serving alias:

```powershell
& $ollamaExe create pytest-triage:coder3b-ctx16k -f $modelFile
& $ollamaExe show --parameters pytest-triage:coder3b-ctx16k
```

Expect success, `num_ctx 16384`, temperature 0, seed 42, top-k 20, top-p 0.8 and
repeat penalty 1. These are the measured settings. The 8K setup cannot fit the
full #12204 case; its rejected request required 14,487 input tokens.

### 6. Warm the model and verify actual GPU residency

In the **second Windows PowerShell**:

```powershell
$warmup = @{
    model = 'pytest-triage:coder3b-ctx16k'
    prompt = 'Return only the JSON object {"ready":true}.'
    format = 'json'
    stream = $false
    keep_alive = '5m'
    options = @{ num_predict = 32 }
} | ConvertTo-Json -Depth 4
Invoke-RestMethod "$env:OLLAMA_HOST/api/generate" -Method Post -ContentType 'application/json' -Body $warmup -TimeoutSec 180
Invoke-RestMethod "$env:OLLAMA_HOST/api/ps" | ConvertTo-Json -Depth 8
& $ollamaExe ps
```

Expect an actual short response with `done: true`. `/api/ps` must show the alias,
Q4_K_M and `context_length: 16384`. This run reported equal `size` and
`size_vram`, confirming full GPU residency. Compare `ollama ps` and
`nvidia-smi` rather than assuming fit from model file size alone. A model-loading
failure, CPU offload or changed context must be recorded as changed serving
behavior. The first-ever application smoke timed out; warm-up is separate from
the app's 20-second per-call limit and from historical quality scoring.

### 7. Start the app in WSL

In the **WSL application shell**, from this checkout:

```sh
uv sync --locked --group dev
export MODEL_NAME=pytest-triage:coder3b-ctx16k
export MODEL_BASE_URL=http://172.17.48.1:11434/v1
uv run --locked --no-env-file uvicorn maintainer_copilot.web:app --host 127.0.0.1 --port 8000
```

Use the verified current address. Expect Uvicorn to listen on
`http://127.0.0.1:8000`. Optional authenticated public GitHub reads use the
existing `GITHUB_TOKEN`; it is not a model API key. With GitHub CLI already
authenticated, set it in this shell before starting the app with
`export GITHUB_TOKEN="$(gh auth token)"`.

Open `http://127.0.0.1:8000` in Windows. Both Windows HTTP access and real browser
submission were verified. A simple input is title `Bug: collection fails`, body
`pytest errors when collecting tests.` Expect a cited detail request, type bug,
a trace link and a real model event with usage when the provider supplies it.
The model endpoint must support JSON-schema structured outputs. Trace contents
are process-local and disappear after app restart.

For the bounded-agent smoke, use the report's optional issue/source fields.
The server offers only supplied, unused read actions, allows at most four model
calls and validates the final report. A broad earlier-issue search can hit
GitHub's 1,000-result cap; expect a partial report with an explicit abstention,
not a fabricated duplicate. The [integration record](evaluation/issue-21-integration-bounded.json)
shows both read tools and this failure, plus injection handling.

### 8. Reproduce real twenty-case evaluation in WSL

Keep Windows Ollama running. Use another **WSL shell** in the checkout:

```sh
export GITHUB_TOKEN="$(gh auth token)"
uv run --locked --no-env-file python -m maintainer_copilot.local_evaluation \
  --ollama-url http://172.17.48.1:11434 \
  --model pytest-triage:coder3b-ctx16k \
  --output /tmp/issue-21-new-results.json
```

The output path must not exist; choose a new path for every run. Expect an
integrity preflight, real warm-up, twenty progress lines and a JSON artifact
with field scores, raw model selections, reports, traces, model-error counts,
latency, identity/settings and sampled GPU memory. Integrity failures flag cases
before model input. A scoreable fallback report does not mean inference succeeded.
The controlled preflight is not included as quality evidence.

The final comparison used repeated `--model` arguments for
`pytest-triage:coder3b-ctx16k`, `pytest-triage:qwen3-4b-ctx16k` and
`pytest-triage:coder7b-ctx16k`. Comparator source tags and identical generation
settings are in the [selection manifest](evaluation/issue-21-selection.json).
Do not replace the existing #12–#15 baseline artifacts with new output.
Human review of generated replies and semantic citation support remains separate
from this deterministic field scorer.
