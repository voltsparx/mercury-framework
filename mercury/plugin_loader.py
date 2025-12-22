import os
import json

def discover_plugins(base_dir=None):
    """
    Discover all plugins in the mercury_plugins directory.
    Returns a list of dicts with keys: name, path
    """
    if base_dir is None:
        # Default to repository root + mercury_plugins
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mercury_plugins")

    plugins = []
    if not os.path.isdir(base_dir):
        return plugins

    for name in os.listdir(base_dir):
        plugin_path = os.path.join(base_dir, name)
        if os.path.isdir(plugin_path):
            manifest_path = os.path.join(plugin_path, "manifest.json")
            if os.path.isfile(manifest_path):
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    plugin_info = {
                        "name": manifest.get("name", name),
                        "path": plugin_path,
                        "manifest": manifest
                    }
                    plugins.append(plugin_info)
                except Exception as e:
                    print(f"Failed to load manifest for {name}: {e}")
    return plugins

def load_manifest(plugin_path):
    """
    Load the manifest.json for a given plugin path.
    """
    manifest_file = os.path.join(plugin_path, "manifest.json")
    if not os.path.isfile(manifest_file):
        raise FileNotFoundError(f"Manifest not found in {plugin_path}")
    with open(manifest_file, "r", encoding="utf-8") as f:
        return json.load(f)
