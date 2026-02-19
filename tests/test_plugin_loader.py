from mercury.plugin_loader import discover_plugins, load_manifest

def test_discover_example_plugin():
    plugins = discover_plugins()
    names = [p['name'] for p in plugins]
    assert 'example_simulator' in names
    assert 'incident_reporter' in names
    assert 'telemetry_snapshot' in names

def test_manifest_local_only():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'] == 'example_simulator'), None)
    assert p is not None
    manifest = load_manifest(p['path'])
    assert manifest.get('network_policy') == 'local-only'


def test_non_runnable_template_dir_not_discovered():
    plugins = discover_plugins()
    names = [p["name"] for p in plugins]
    assert "Plugin Templates" not in names
