"""Evaluate an explicitly configured model through the cutoff-safe replay."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from collections.abc import Collection
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from threading import Event, Thread
from time import perf_counter
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from maintainer_copilot import issue_search, model, source
from maintainer_copilot.evaluation import CaseResult, aggregate, score_report
from maintainer_copilot.replay import (
    CaseFlagged,
    CommitSource,
    GitHubCommitSource,
    HistoricalCase,
    RepositoryCommit,
    candidate_references,
    load_cases,
    replay_case,
)
from maintainer_copilot.trace import get_trace


class _ObservedModel(model.OpenAICompatibleModel):
    def __init__(self, client: model.OpenAICompatibleModel) -> None:
        super().__init__(client.base_url, client.model_name)
        self.client = client
        self.calls: list[dict[str, Any]] = []

    def generate(self, request: model.ModelRequest) -> object:
        started = perf_counter()
        call: dict[str, Any] = {}
        try:
            response = self.client.generate(request)
            if isinstance(response, model.ModelResponse):
                call.update(
                    response=response.output,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    error=response.error,
                )
            else:
                call["response"] = response
            return response
        except Exception as exc:
            call["error"] = "Model client failed."
            call["error_type"] = type(exc).__name__
            call["provider_error_type"] = (
                type(exc.__cause__).__name__ if exc.__cause__ is not None else None
            )
            if isinstance(exc.__cause__, HTTPError):
                call["provider_http_status"] = exc.__cause__.code
            raise
        finally:
            call["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            self.calls.append(call)


def evaluate_local_model(
    client: model.OpenAICompatibleModel,
    *,
    cases: Collection[HistoricalCase] | None = None,
    commit_source: CommitSource | None = None,
    issue_source: issue_search.IssueSource | None = None,
    source_reader: source.SourceReader | None = None,
    measure_gpu: bool = False,
) -> dict[str, Any]:
    """Preserve reports, responses and traces separately from baseline artifacts.

    Model responses never substitute for expected outcomes. The existing replay
    verifies every opening and commit before calling the supplied model. Search
    is limited to verified catalog openings available at each case's cutoff.
    """
    if not client.model_name:
        raise ValueError("A model name is required; no controlled-response fallback.")
    catalog = list(load_cases() if cases is None else cases)
    observed = _ObservedModel(client)
    results: list[CaseResult] = []
    records: list[dict[str, Any]] = []
    for case in catalog:
        started = perf_counter()
        first_call = len(observed.calls)
        candidate_numbers = tuple(
            reference.number for reference in candidate_references(case, catalog)
        )
        report = None
        scores = None
        error = None
        trace = None
        with _GpuMemory(measure_gpu) as gpu:
            try:
                report = replay_case(
                    case,
                    model_client=observed,
                    candidate_catalog=catalog,
                    keyword_filter=True,
                    commit_source=commit_source,
                    issue_source=issue_source,
                    source_reader=source_reader,
                )
                scores = score_report(case, report, candidate_numbers)
                trace = get_trace(report.trace_id)
            except (CaseFlagged, ValueError) as exc:
                error = str(exc)
        result = CaseResult(
            issue_number=case.issue_number,
            method="local_model",
            opening_cutoff=case.opening_cutoff.isoformat(),
            repository_commit=case.repository_commit,
            latency_ms=round((perf_counter() - started) * 1000, 3),
            candidate_pool_size=len(candidate_numbers),
            error=error,
            scores=scores,
        )
        results.append(result)
        records.append(
            {
                **asdict(result),
                "report": report.model_dump(mode="json") if report else None,
                "trace": trace.model_dump(mode="json") if trace else None,
                "model_calls": observed.calls[first_call:],
                "gpu_memory": gpu.summary(),
            }
        )
        print(
            f"{client.model_name} #{case.issue_number}: "
            f"{error or (report.status if report else 'unavailable')}",
            file=sys.stderr,
            flush=True,
        )
    return {
        "method": "local_model",
        "model_name": client.model_name,
        "model_call_count": len(observed.calls),
        "model_error_count": sum(
            event["kind"] == "model" and event["status"] != "ok"
            for record in records
            if record["trace"] is not None
            for event in record["trace"]["events"]
        ),
        "aggregate": aggregate(results),
        "cases": records,
        "methodology": (
            "Real endpoint responses through the existing fixed replay and field "
            "scorer. Keyword retrieval covers verified pre-cutoff catalog openings. "
            "Duplicate matching and missing details remain rules; the model controls "
            "type and selection of supplied reply statements. Semantic judgments "
            "remain pending. This is not the full workflow comparison in #16."
        ),
    }


class _GpuMemory:
    """Sample device-wide NVIDIA use; never substitute zero for unavailable data."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self.samples: list[float] = []
        self.error: str | None = None
        self.stopped = Event()
        self.thread: Thread | None = None

    def _sample(self) -> None:
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.used",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=3,
            )
            # This evaluation targets the laptop's single NVIDIA GPU. Fail
            # visibly rather than sum unrelated devices on another machine.
            rows = result.stdout.strip().splitlines()
            if len(rows) != 1:
                raise ValueError("GPU telemetry requires exactly one NVIDIA GPU")
            self.samples.append(float(rows[0]))
        except (OSError, ValueError, subprocess.SubprocessError):
            self.error = "NVIDIA memory telemetry unavailable."

    def _poll(self) -> None:
        while not self.stopped.wait(0.5):
            self._sample()

    def __enter__(self) -> "_GpuMemory":
        if self.enabled:
            self._sample()
            if self.error is None:
                self.thread = Thread(target=self._poll, daemon=True)
                self.thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stopped.set()
        if self.thread is not None:
            self.thread.join(timeout=4)
        if self.enabled:
            self._sample()

    def summary(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "sample_interval_ms": 500,
            "sample_count": len(self.samples),
            "initial_used_mib": self.samples[0] if self.samples else None,
            "peak_sampled_used_mib": max(self.samples) if self.samples else None,
            "error": self.error,
            "scope": (
                "Device-wide use including other processes; sampled, not true peak."
            ),
        }


class _LiveEvidenceCache:
    """Reuse public reads within one run; replay still verifies each case."""

    def __init__(self) -> None:
        self.commits: dict[str, RepositoryCommit] = {}
        self.issues: dict[int, issue_search.IssueRecord] = {}
        self.excerpts: dict[tuple[str, str, int], source.SourceExcerpt] = {}

    def get_commit(self, sha: str) -> RepositoryCommit:
        if sha not in self.commits:
            self.commits[sha] = GitHubCommitSource().get_commit(sha)
        return self.commits[sha]

    def get_issue(self, number: int) -> issue_search.IssueRecord:
        if number not in self.issues:
            self.issues[number] = issue_search.GitHubIssueSource().get_issue(number)
        return self.issues[number]

    def search_issues(
        self, query: str, created_before: datetime
    ) -> list[issue_search.IssueRecord]:
        raise CaseFlagged("Historical evaluation must not search the live index.")

    def get_excerpt(self, location: source.SourceLocation) -> source.SourceExcerpt:
        key = (location.commit, location.path, location.line)
        if key not in self.excerpts:
            self.excerpts[key] = source.PublicRepositorySource().get_excerpt(location)
        return self.excerpts[key]


def _ollama_json(url: str, payload: dict[str, object] | None = None) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=180) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError("Ollama response must be an object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", action="append", required=True)
    parser.add_argument(
        "--output", type=Path, help="New JSON artifact path; existing files are refused"
    )
    parser.add_argument(
        "--ollama-url", default=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    )
    args = parser.parse_args()
    output: Path | None = args.output
    if output is not None:
        with output.open("x", encoding="utf-8") as handle:
            handle.write('{"status": "starting"}\n')
    base = args.ollama_url.rstrip("/")
    evidence = _LiveEvidenceCache()
    catalog = load_cases()
    artifact: dict[str, Any] = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "server": _ollama_json(f"{base}/api/version"),
        "ollama_url": base,
        "python_version": platform.python_version(),
        "generation": {
            "temperature": 0,
            "max_tokens": 256,
            "response_format": "json_schema (triage selection)",
            "model_client_sha256": hashlib.sha256(
                Path(model.__file__).read_bytes()
            ).hexdigest(),
            "client_timeout_seconds": 20,
            "other_settings": "See each model's recorded parameters and serving state.",
        },
        "cost_assumptions": {
            "model_api_usd": 0,
            "scope": "Local Ollama; electricity, hardware and network costs excluded.",
        },
        "models": {},
        "integrity_preflight": [],
    }
    if output is not None:
        output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    # Acquire and verify public evidence before timing any candidate. The
    # controlled response here is solely an integrity smoke, never quality data.
    for case in catalog:
        entry: dict[str, Any] = {"issue_number": case.issue_number}
        try:
            replay_case(
                case,
                commit_source=evidence,
                issue_source=evidence,
                source_reader=evidence,
                candidate_catalog=catalog,
                keyword_filter=True,
            )
            entry["integrity"] = "passed"
        except CaseFlagged as exc:
            entry.update(integrity="flagged", error=str(exc))
        artifact["integrity_preflight"].append(entry)
        if output is not None:
            output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    for name in args.model:
        tags = _ollama_json(f"{base}/api/tags")
        identity = next(
            (item for item in tags.get("models", []) if item["name"] == name), None
        )
        if identity is None:
            raise ValueError(f"Local model is not installed under exact name {name!r}")
        info = _ollama_json(f"{base}/api/show", {"model": name})
        started = perf_counter()
        with _GpuMemory(True) as gpu:
            warmup = _ollama_json(
                f"{base}/api/generate",
                {
                    "model": name,
                    "prompt": 'Return only the JSON object {"ready":true}.',
                    "format": "json",
                    "stream": False,
                    "keep_alive": "5m",
                    "options": {"num_predict": 32},
                },
            )
        warmup_ms = round((perf_counter() - started) * 1000, 3)
        serving = _ollama_json(f"{base}/api/ps")
        result = evaluate_local_model(
            model.OpenAICompatibleModel(f"{base}/v1", name),
            cases=catalog,
            commit_source=evidence,
            issue_source=evidence,
            source_reader=evidence,
            measure_gpu=True,
        )
        result.update(
            identity=identity,
            parameters=info.get("parameters"),
            model_info=info.get("model_info"),
            template_sha256=hashlib.sha256(
                info.get("template", "").encode()
            ).hexdigest(),
            warmup={
                "latency_ms": warmup_ms,
                "response": warmup,
                "gpu_memory": gpu.summary(),
            },
            serving_before=serving,
            serving_after=_ollama_json(f"{base}/api/ps"),
        )
        artifact["models"][name] = result
        if output is not None:
            output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    if output is None:
        print(json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
