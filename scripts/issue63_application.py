"""Exercise real Python, HTTP, browser and bounded-agent report entry points."""

import json
import os
import socket
import subprocess
import tempfile
import threading
import time
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
from urllib.request import ProxyHandler, Request, build_opener

import uvicorn

from maintainer_copilot import IssueUnderReview, triage_issue
from maintainer_copilot.model import OpenAICompatibleModel
from maintainer_copilot.triage import TriageReport
from maintainer_copilot.web import app
from maintainer_copilot.workflow_comparison import ROOT

HERE = ROOT / "docs/evaluation/issue-63"
CANDIDATE = "triage-eval:qwen35-4b-16k-v1"


def read(path):
    return json.loads(path.read_bytes())


def browser_package():
    tools = read(HERE / "browser-tools.json")
    package = Path(tools["playwright_package"])
    if (
        sha256((package / "package.json").read_bytes()).hexdigest()
        != tools["playwright_package_sha256"]
        or sha256(Path(tools["chromium_executable"]).read_bytes()).hexdigest()
        != tools["chromium_sha256"]
        or subprocess.check_output(["node", "--version"], text=True).strip()
        != tools["node_version"]
    ):
        raise ValueError("Pinned browser tooling changed")
    for name, hashed in tools["libraries_sha256"].items():
        if sha256(Path(name).read_bytes()).hexdigest() != hashed:
            raise ValueError("Pinned browser dependency changed")
    return package


@contextmanager
def application(base, on_close=None):
    with tempfile.TemporaryDirectory(prefix="issue63-registry-") as directory:
        with patch.dict(
            os.environ,
            {
                "MODEL_NAME": CANDIDATE,
                "MODEL_BASE_URL": base + "/v1",
                "MODEL_REASONING_EFFORT": "none",
                "MODEL_DRAFTING": "0",
                "REPOSITORY_REGISTRY_PATH": str(Path(directory) / "registry.sqlite3"),
            },
        ):
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
            server = uvicorn.Server(
                uvicorn.Config(
                    app,
                    log_level="error",
                    lifespan="off",
                    access_log=False,
                )
            )
            thread = threading.Thread(
                target=server.run,
                kwargs={"sockets": [sock]},
                daemon=True,
            )
            thread.start()
            deadline = time.monotonic() + 10
            try:
                while not server.started:
                    if not thread.is_alive() or time.monotonic() > deadline:
                        raise RuntimeError("Temporary application failed to start")
                    time.sleep(0.02)
                yield f"http://127.0.0.1:{port}"
            finally:
                if on_close is not None:
                    on_close()
                server.should_exit = True
                thread.join(timeout=10)
                sock.close()
                if thread.is_alive():
                    raise RuntimeError(
                        "Application shutdown incomplete; transport closed"
                    )


def integration(kind, opening, url):
    payload = {key: opening[key] for key in ("title", "body")}
    if kind == "python":
        return triage_issue(
            IssueUnderReview(**payload),
            model_client=OpenAICompatibleModel.from_environment(),
        )
    if kind == "browser":
        environment = os.environ.copy()
        libraries = read(HERE / "browser-tools.json")["library_path"]
        previous = environment.get("LD_LIBRARY_PATH", "")
        environment["LD_LIBRARY_PATH"] = libraries + (
            ":" + previous if previous else ""
        )
        try:
            result = subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts/issue63_browser.cjs"),
                    str(browser_package()),
                    url,
                    read(HERE / "browser-tools.json")["chromium_executable"],
                ],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=45,
                check=True,
                env=environment,
            )
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("Browser integration failed: " + exc.stderr) from exc
        return TriageReport.model_validate_json(result.stdout)
    route = "/api/agent/triage" if kind == "agent" else "/api/triage"
    request = Request(
        url + route,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with build_opener(ProxyHandler({})).open(request, timeout=45) as response:
        return TriageReport.model_validate_json(response.read(1048576))
