"""Reporting helpers for plugin executions and console workflows."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_report_dir(report_dir: str | Path = "reports") -> Path:
    path = Path(report_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip())
    cleaned = cleaned.strip("-")
    return cleaned or "report"


def build_run_report(
    *,
    plugin_name: str,
    manifest: dict[str, Any],
    phases: list[str],
    execution: dict[str, Any],
    runner: str,
) -> dict[str, Any]:
    return {
        "generated_at": _utc_iso(),
        "plugin": {
            "name": plugin_name,
            "version": manifest.get("version"),
            "author": manifest.get("author"),
            "network_policy": manifest.get("network_policy"),
        },
        "execution": {
            "runner": runner,
            "phases": phases,
            "returncode": execution.get("returncode"),
            "timed_out": execution.get("timed_out", False),
            "duration_sec": execution.get("duration_sec"),
            "mode": execution.get("mode", runner),
            "command": execution.get("command"),
        },
        "output": {
            "stdout": execution.get("stdout", ""),
            "stderr": execution.get("stderr", ""),
        },
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    plugin = payload.get("plugin", {})
    execution = payload.get("execution", {})
    output = payload.get("output", {})

    lines = [
        "# Mercury Plugin Run Report",
        "",
        f"- Generated: `{payload.get('generated_at')}`",
        f"- Plugin: `{plugin.get('name')}`",
        f"- Version: `{plugin.get('version')}`",
        f"- Author: `{plugin.get('author')}`",
        f"- Runner: `{execution.get('runner')}`",
        f"- Phases: `{','.join(execution.get('phases', []))}`",
        f"- Return code: `{execution.get('returncode')}`",
        f"- Timed out: `{execution.get('timed_out')}`",
        f"- Duration (sec): `{execution.get('duration_sec')}`",
        "",
        "## Stdout",
        "```text",
        str(output.get("stdout", "")).strip(),
        "```",
        "",
        "## Stderr",
        "```text",
        str(output.get("stderr", "")).strip(),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_run_report(
    *,
    report_dir: str | Path = "reports",
    plugin_name: str,
    manifest: dict[str, Any],
    phases: list[str],
    execution: dict[str, Any],
    runner: str,
) -> dict[str, Any]:
    out_dir = ensure_report_dir(report_dir)
    slug = sanitize_slug(plugin_name)
    stamp = _utc_timestamp()
    json_path = out_dir / f"{stamp}_{slug}.json"
    md_path = out_dir / f"{stamp}_{slug}.md"

    report = build_run_report(
        plugin_name=plugin_name,
        manifest=manifest,
        phases=phases,
        execution=execution,
        runner=runner,
    )
    _write_json(json_path, report)
    _write_markdown(md_path, report)
    return {"json_path": json_path, "md_path": md_path, "report": report}


def list_reports(report_dir: str | Path = "reports", limit: int = 20) -> list[Path]:
    path = Path(report_dir)
    if not path.exists():
        return []
    reports = sorted(path.glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    return reports[:limit]
