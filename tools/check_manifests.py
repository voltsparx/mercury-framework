import os
import json
import sys
from mercury.plugin_loader import discover_plugins

def validate_manifest(plugin_path):
    manifest_path = os.path.join(plugin_path, "manifest.json")
    if not os.path.exists(manifest_path):
        return False, "Missing manifest.json"
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except Exception as e:
        return False, f"Invalid JSON: {e}"

    required_keys = ["name", "version", "description", "author", "network_policy", "responsible_use"]
    for key in required_keys:
        if key not in manifest:
            return False, f"Missing '{key}' in manifest"
    return True, None

def main():
    plugins = discover_plugins(include_non_runnable=True)
    all_valid = True
    for p in plugins:
        valid, error = validate_manifest(p["path"])
        if not valid:
            all_valid = False
            print(f"Manifest validation failed for {p['name']}: {error}")
    if all_valid:
        print("All plugin manifests validated.")
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
