"""Environment and framework diagnostics."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import shutil
import sys

from .metadata import PROJECT_NAME, PROJECT_VERSION_TAG
from .plugin_loader import REQUIRED_MANIFEST_FIELDS, discover_plugins
from .reporting import ensure_report_dir


def _check_report_dir(report_dir: str | Path) -> tuple[bool, str]:
    try:
        path = ensure_report_dir(report_dir)
        probe = path / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True, str(path)
    except Exception as exc:
        return False, str(exc)


def collect_diagnostics(report_dir: str = "reports") -> dict:
    plugins = discover_plugins(include_non_runnable=True)
    runnable = [p for p in plugins if p.get("runnable")]
    invalid_manifests = []
    for plugin in plugins:
        manifest = plugin.get("manifest", {})
        missing = sorted(REQUIRED_MANIFEST_FIELDS.difference(set(manifest.keys())))
        if missing:
            invalid_manifests.append(
                {
                    "plugin": plugin.get("name"),
                    "missing_manifest_fields": missing,
                }
            )

    report_ok, report_info = _check_report_dir(report_dir)
    docker_path = shutil.which("docker")
    python_ok = sys.version_info >= (3, 10)
    overall_ok = python_ok and report_ok and not invalid_manifests

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": {
            "name": PROJECT_NAME,
            "version": PROJECT_VERSION_TAG,
        },
        "checks": {
            "python_version_ok": python_ok,
            "docker_available": bool(docker_path),
            "report_dir_writable": report_ok,
            "manifest_validation_ok": not invalid_manifests,
        },
        "environment": {
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "docker_path": docker_path or "",
            "report_dir": report_info,
        },
        "plugins": {
            "total": len(plugins),
            "runnable": len(runnable),
            "invalid_manifests": invalid_manifests,
        },
        "overall_ok": overall_ok,
    }


def write_diagnostics_report(report_dir: str = "reports") -> Path:
    payload = collect_diagnostics(report_dir=report_dir)
    out_dir = ensure_report_dir(report_dir)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"{stamp}_diagnostics.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    return path
