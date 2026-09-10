"""Shared fixtures for Playwright E2E tests.

Each example lives in ``example/<name>.py`` and exposes an ``app``
(FastAPI) object.  This module launches uvicorn as a subprocess and
provides a ``page`` fixture wired to the running server.
"""

from __future__ import annotations

import asyncio
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "example"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _find_free_port() -> int:
    """Return a random free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def _wait_for_server(url: str, timeout: float = 10) -> None:
    """Block until the server responds with HTTP 200."""
    import urllib.request

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            r = urllib.request.urlopen(url, timeout=1.0)
            if r.status == 200:
                return
        except Exception:
            pass
        time.sleep(0.1)
    raise RuntimeError(f"Server at {url} did not become ready in {timeout}s")


@pytest.fixture
async def example_server(request):
    """Start an example app server and yield its base URL.

    Derives the example name from the test module name:
    ``tests/e2e/test_<name>.py`` → ``example/<name>.py``.

    Usage in a test::

        async def test_something(page: Page, example_server):
            await page.goto(example_server)
            ...
    """
    test_module = request.node.module
    module_name = test_module.__name__
    # tests.e2e.test_counter → counter
    example_name = module_name.split(".")[-1].removeprefix("test_")

    example_path = EXAMPLES_DIR / f"{example_name}.py"
    if not example_path.exists():
        pytest.skip(f"No example file: {example_path}")

    port = _find_free_port()
    url = f"http://127.0.0.1:{port}"

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            f"example.{example_name}:app",
            f"--port={port}",
            "--host=127.0.0.1",
            "--log-level=warning",
        ],
        cwd=str(PROJECT_ROOT),
        env={**dict(os.environ), "PYTHONPATH": str(PROJECT_ROOT)},
    )

    try:
        _wait_for_server(url)
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
