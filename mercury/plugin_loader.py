from __future__ import annotations

import json
from pathlib import Path


REQUIRED_MANIFEST_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "network_policy",
    "responsible_use",
}


def _default_plugins_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "mercury_plugins"


def discover_plugins(
    base_dir: str | Path | None = None,
    *,
    include_non_runnable: bool = False,
) -> list[dict]:
    """Discover plugin folders under `mercury_plugins/`.

    Returns dictionaries with keys:
    - `name`
    - `path`
    - `plugin_file`
    - `runnable`
    - `manifest`
    - `valid_manifest`
    """
    plugins_dir = Path(base_dir) if base_dir else _default_plugins_dir()
    plugins: list[dict] = []
    if not plugins_dir.is_dir():
        return plugins

    for entry in sorted(plugins_dir.iterdir()):
        if not entry.is_dir():
            continue
        manifest_path = entry / "manifest.json"
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Failed to load manifest for {entry.name}: {exc}")
            continue

        plugin_file = entry / "plugin.py"
        runnable = plugin_file.is_file()
        if not include_non_runnable and not runnable:
            continue

        plugins.append(
            {
                "name": manifest.get("name", entry.name),
                "path": str(entry),
                "plugin_file": str(plugin_file),
                "runnable": runnable,
                "manifest": manifest,
                "valid_manifest": REQUIRED_MANIFEST_FIELDS.issubset(set(manifest.keys())),
            }
        )
    return plugins


def load_manifest(plugin_path: str | Path) -> dict:
    """Load `manifest.json` for a given plugin folder."""
    manifest_file = Path(plugin_path) / "manifest.json"
    if not manifest_file.is_file():
        raise FileNotFoundError(f"Manifest not found in {plugin_path}")
    return json.loads(manifest_file.read_text(encoding="utf-8"))
