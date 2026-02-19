"""Sandbox runner helpers for plugin execution.

This module is not a hard security boundary. It adds process separation,
manifest policy checks, and optional Docker execution with `--network=none`.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Dict


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_plugin_file(plugin_path: str | Path) -> Path:
    plugin_dir = Path(plugin_path).resolve()
    plugin_file = plugin_dir / "plugin.py"
    if not plugin_file.is_file():
        raise FileNotFoundError("plugin.py not found")

    project = _project_root().resolve()
    if project not in plugin_file.parents:
        raise ValueError("Plugin path must stay inside project root")
    return plugin_file


def _run_command(cmd: list[str], *, env: dict, timeout: int, mode: str) -> Dict:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            check=False,
        )
        return {
            "mode": mode,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
            "duration_sec": round(time.monotonic() - started, 3),
            "command": cmd,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "mode": mode,
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + "\n[mercury] Plugin execution timed out.",
            "timed_out": True,
            "duration_sec": round(time.monotonic() - started, 3),
            "command": cmd,
        }
    except FileNotFoundError as exc:
        return {
            "mode": mode,
            "returncode": 127,
            "stdout": "",
            "stderr": f"[mercury] Executable not found: {exc}",
            "timed_out": False,
            "duration_sec": round(time.monotonic() - started, 3),
            "command": cmd,
        }


def run_plugin_subprocess(plugin_path: str, args: list | None = None, timeout: int = 10) -> Dict:
    """Run `plugin.py` in a subprocess with `MERCURY_SAFE=1`."""
    plugin_file = _resolve_plugin_file(plugin_path)
    arg_list = list(args or ["--run"])

    env = os.environ.copy()
    env["MERCURY_SAFE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    project_root = str(_project_root())
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{project_root}{os.pathsep}{existing}" if existing else project_root

    cmd = [sys.executable, str(plugin_file)] + arg_list
    return _run_command(cmd, env=env, timeout=timeout, mode="subprocess")


def run_plugin_docker(
    plugin_path: str,
    args: list | None = None,
    *,
    timeout: int = 20,
    image: str = "mercury-sandbox:latest",
) -> Dict:
    """Run `plugin.py` inside a Docker container with network disabled."""
    plugin_file = _resolve_plugin_file(plugin_path)
    project_root = _project_root().resolve()
    relative_plugin = plugin_file.relative_to(project_root).as_posix()
    arg_list = list(args or ["--run"])

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    mount_src = str(project_root)
    if os.name == "nt":
        mount_src = mount_src.replace("\\", "/")

    cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=64m",
        "-e",
        "MERCURY_SAFE=1",
        "-e",
        "PYTHONDONTWRITEBYTECODE=1",
        "-v",
        f"{mount_src}:/app:ro",
        "-w",
        "/app",
        image,
        "python",
        relative_plugin,
    ] + arg_list
    return _run_command(cmd, env=env, timeout=timeout, mode="docker")


def validate_manifest_local_only(manifest: Dict) -> bool:
    """Return True when manifest explicitly declares `network_policy: local-only`."""
    policy = str(manifest.get("network_policy", "")).strip().lower()
    return policy == "local-only"
