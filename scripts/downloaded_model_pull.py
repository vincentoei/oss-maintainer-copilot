"""Pull the two preflight artifacts once, checking immutable registry identities."""

import hashlib
import json
import os
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener, urlopen

DATA = Path(__file__).resolve().parents[1] / "docs/evaluation/downloaded-models"
PLAN = json.loads((DATA / "preflight.json").read_bytes())
LOCAL = build_opener(ProxyHandler({}))


def save_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as output:
        json.dump(data, output, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())


def local_request(path, data=None, timeout=20):
    req = Request(
        PLAN["local_host"] + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"},
    )
    return LOCAL.open(req, timeout=timeout)


def local_json(path, data=None, timeout=20):
    with local_request(path, data, timeout) as response:
        return json.load(response)


def installed():
    return {row["name"]: row for row in local_json("/api/tags")["models"]}


def main():
    if local_json("/api/version")["version"] != PLAN["ollama_version"]:
        raise ValueError("Ollama version changed")
    total = 0
    for name, model in PLAN["models"].items():
        repo, tag = model["tag"].split(":")
        url = f"https://registry.ollama.ai/v2/library/{repo}/manifests/{tag}"
        with urlopen(url, timeout=20) as response:
            manifest = response.read(65537)
        if hashlib.sha256(manifest).hexdigest() != model["sha256"]:
            raise ValueError(f"Registry digest changed for {name}")
        if manifest != (DATA / "manifests" / f"{name}.json").read_bytes():
            raise ValueError(f"Saved manifest differs for {name}")
        content = json.loads(manifest)
        total += sum(layer["size"] for layer in [content["config"], *content["layers"]])
    if total != PLAN["max_manifest_payload_bytes"]:
        raise ValueError("Pull payload budget differs")
    for name, model in PLAN["models"].items():
        folder = DATA / "run" / name
        save_new(folder / "pull-reservation.json", model)
        with local_request("/api/pull", {"model": model["tag"]}, timeout=180) as stream:
            last = {}
            last_status = ""
            for line in stream:
                last = json.loads(line)
                if "error" in last:
                    save_new(folder / "pull-error.json", last)
                    raise ValueError(last["error"])
                status = last.get("status")
                if status != last_status:
                    print(name, status, flush=True)
                    last_status = status
        if last.get("status") != "success":
            raise ValueError("Pull ended without success")
        tag = installed()[model["tag"]]
        save_new(folder / "installed.json", tag)
        if tag["digest"] != model["sha256"]:
            raise ValueError("Installed identity differs")


if __name__ == "__main__":
    main()
