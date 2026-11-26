"""Execute one approved serial comparison, or capture its metadata-only freeze."""

import json
import subprocess
from argparse import ArgumentParser
from hashlib import sha256
from urllib.request import ProxyHandler, Request, build_opener
from uuid import UUID

from downloaded_model_pull import DATA, PLAN, save_new
from downloaded_scored_prepare import (
    ALIASES,
    CACHE,
    HERE,
    REFERENCE,
    prepare,
    read,
    restore,
    with_effort,
)
from issue62_compare import HOST, LocalOnly, run_case
from issue62_prepare import PROBES

from maintainer_copilot.paired_evaluation import PairedBudget
from maintainer_copilot.replay import load_cases
from maintainer_copilot.trace import get_trace
from maintainer_copilot.workflow_comparison import ROOT

RUN = HERE / "run"
TRANSPORT = build_opener(ProxyHandler({}), LocalOnly())
LIMITS = {
    "per_arm": 56,
    "total": 168,
    "output_per_request": 256,
    "max_total_output": 43008,
    "timeout_seconds": 20,
    "response_bytes": 65536,
    "context": 16384,
    "downloads": 0,
    "warmups": 0,
    "retries": 0,
    "hosted": 0,
    "api_usd": 0,
}


def metadata(route, body=None):
    req = Request(
        HOST + route,
        data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"},
    )
    with TRANSPORT.open(req, timeout=20) as response:
        return json.load(response)


def serving():
    version = metadata("/api/version")["version"]
    if version != PLAN["ollama_version"]:
        raise ValueError("Server version drift")
    tags = {r["name"]: r for r in metadata("/api/tags")["models"]}
    identities = {REFERENCE: read(DATA / "run/host.json")["reference"]["digest"]}
    for name, model in PLAN["models"].items():
        identities[model["alias"]] = read(DATA / "run" / name / "alias.json")["tag"][
            "digest"
        ]
        if tags[model["tag"]]["digest"] != model["sha256"]:
            raise ValueError("Installed parent changed")
    arms = {}
    for alias in ALIASES:
        tag = tags[alias]
        if (
            tag["digest"] != identities[alias]
            or tag["details"]["quantization_level"] != "Q4_K_M"
        ):
            raise ValueError(f"Alias identity changed: {alias}")
        show = metadata("/api/show", {"model": alias})
        arms[alias] = {"digest": tag["digest"], "details": tag["details"]}
        for key in ("parameters", "template", "renderer", "parser", "thinking"):
            arms[alias][key] = show.get(key)
        arms[alias]["tokenizer_and_gguf_metadata_sha256"] = sha256(
            json.dumps(show["model_info"], sort_keys=True).encode()
        ).hexdigest()
    return {"version": version, "arms": arms}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def freeze():
    if prepare() != read(HERE / "requests.json"):
        raise ValueError("Requests no longer reproduce")
    if git("status", "--porcelain"):
        raise ValueError("Commit exact inputs, runner and protocol before freeze")
    save_new(
        HERE / "freeze.json",
        {
            "source_commit": git("rev-parse", "HEAD").decode().strip(),
            "request_set_sha256": sha256(
                (HERE / "requests.json").read_bytes()
            ).hexdigest(),
            "snapshot_sha256": sha256(CACHE.read_bytes()).hexdigest(),
            "scored_protocol_sha256": sha256(
                (HERE / "protocol.md").read_bytes()
            ).hexdigest(),
            "protocol_sha256": sha256(
                (DATA / "comparison.md").read_bytes()
            ).hexdigest(),
            "limits": LIMITS,
            "model_order": ALIASES,
            "reasoning_effort": "none",
            "serving": serving(),
        },
    )


class ChargedRequest:
    """Send exactly the bytes accepted by the existing durable reservation ledger."""

    def __init__(self, budget):
        self.budget = budget
        self.original = self.body = None
        self.sent = False

    def reserve(self, alias, case, body):
        self.original = body
        self.body = with_effort(body)
        self.budget.reserve(alias, case, self.body)

    def open(self, request, *, timeout):
        if (
            self.sent
            or self.body is None
            or self.original != request.data
            or timeout != 20
        ):
            raise ValueError("Unreserved or repeated transport request")
        self.sent = True
        outgoing = Request(
            request.full_url,
            data=self.body,
            headers={"Content-Type": "application/json"},
        )
        return TRANSPORT.open(outgoing, timeout=timeout)


def annotate(row, digest, residency):
    try:
        envelope = json.loads(row["raw_response"] or "null")
        choice = envelope["choices"][0]
        message = choice["message"]
        row["finish_reason"] = choice["finish_reason"]
        row["reasoning_chars"] = sum(
            len(message.get(k) or "")
            for k in ("reasoning", "thinking", "reasoning_content")
        )
        row["usage"] = envelope.get("usage")
    except (TypeError, IndexError, KeyError, ValueError):
        row.update(finish_reason=None, reasoning_chars=None, usage=None)
    usage = row["usage"] or {}
    tokens = usage.get("prompt_tokens")
    row["context_flag"] = (
        "reported_prompt_plus_allowance_exceeds_16k"
        if isinstance(tokens, int) and tokens + 256 > 16384
        else "truncation_unknown"
    )
    row["resident_after"] = residency
    row["gpu_16k"] = any(
        m["digest"] == digest
        and m["context_length"] == 16384
        and m["size"] == m["size_vram"] > 0
        for m in residency["models"]
    )
    if row["status"] == "valid" and (
        row["finish_reason"] != "stop" or row["reasoning_chars"] != 0
    ):
        row.update(
            status="validation_error",
            error="Completion did not stop cleanly with thinking disabled",
        )


def main():
    manifest = read(HERE / "freeze.json")
    source = manifest["source_commit"]
    subprocess.run(["git", "merge-base", "--is-ancestor", source, "HEAD"], check=True)
    if git("status", "--porcelain") or git(
        "diff", "--name-only", source, "HEAD"
    ).decode().splitlines() != [str((HERE / "freeze.json").relative_to(ROOT))]:
        raise ValueError("Live execution requires the clean freeze commit")
    rows = read(HERE / "requests.json")
    if (
        manifest["limits"] != LIMITS
        or list(ALIASES) != manifest["model_order"]
        or rows != prepare()
    ):
        raise ValueError("Frozen limits, arms or request reconstruction differ")
    if manifest["serving"] != serving():
        raise ValueError("Serving configuration changed")
    evidence = restore()
    catalog = load_cases()
    cases = {f"h-{c.issue_number}": c for c in catalog}
    probes = {c["id"]: c for c in read(PROBES)["cases"]}
    keys = list(cases) + list(probes)
    if keys != list(rows) or len(cases) != 50 or len(probes) != 6:
        raise ValueError("Frozen case order changed")
    RUN.mkdir()
    ledger = RUN / "reservations.jsonl"
    ledger.touch(exist_ok=False)
    budget = PairedBudget(
        ledger,
        {(a, k): d for k, r in rows.items() for a, d in r["sha256"].items()},
        per_model=LIMITS["per_arm"],
        total=LIMITS["total"],
    )
    charged_count = 0
    for alias in ALIASES:
        arm = RUN / alias.split(":")[1]
        arm.mkdir()
        if serving() != manifest["serving"]:
            raise ValueError("Identity or settings changed before arm")
        for key in keys:
            plan = rows[key]
            row = dict(
                case=key,
                alias=alias,
                expected=plan["expected"],
                status="unavailable",
                error=plan["error"],
            )
            if not plan["error"]:
                digest = manifest["serving"]["arms"][alias]["digest"]
                before = metadata("/api/ps")
                tags = {t["name"]: t["digest"] for t in metadata("/api/tags")["models"]}
                if tags.get(alias) != digest or any(
                    m["name"] == alias and m["digest"] != digest
                    for m in before["models"]
                ):
                    save_new(
                        RUN / "halt.json",
                        {
                            "reason": "Pre-dispatch identity changed",
                            "alias": alias,
                            "case": key,
                            "charged": False,
                        },
                    )
                    return
                row["resident_before"] = before
                dispatch = ChargedRequest(budget)
                run_case(row, dispatch, dispatch, cases, probes, catalog, evidence)
                if not dispatch.sent:
                    raise RuntimeError("No charged dispatch; stop comparison")
                charged_count += 1
                row["trace"] = get_trace(UUID(row["report"]["trace_id"])).model_dump(
                    mode="json"
                )
                try:
                    annotate(row, digest, metadata("/api/ps"))
                except Exception as exc:
                    save_new(arm / f"{key}.json", row)
                    save_new(
                        RUN / "halt.json",
                        {
                            "reason": f"Telemetry failed: {type(exc).__name__}",
                            "alias": alias,
                            "case": key,
                        },
                    )
                    return
            save_new(arm / f"{key}.json", row)
            halt = None
            if row["status"] == "identity_error" or any(
                m["name"] == alias
                and m["digest"] != manifest["serving"]["arms"][alias]["digest"]
                for m in row.get("resident_after", {}).get("models", [])
            ):
                halt = "Model identity changed"
            elif (
                not plan["error"]
                and charged_count == 1
                and (
                    alias != REFERENCE
                    or row["http_status"] != 200
                    or row["status"] != "valid"
                    or not row["gpu_16k"]
                )
            ):
                halt = "First charged reference request failed its compatibility gate"
            if halt:
                save_new(
                    RUN / "halt.json", {"reason": halt, "alias": alias, "case": key}
                )
                return
        if serving() != manifest["serving"]:
            raise ValueError("Serving configuration changed during arm")
    save_new(RUN / "complete.json", {"charged": charged_count})


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("action", choices=["freeze", "run"])
    if parser.parse_args().action == "freeze":
        freeze()
    else:
        main()
