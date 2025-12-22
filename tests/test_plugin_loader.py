from mercury.plugin_loader import discover_plugins, load_manifest

def test_discover_example_plugin():
    plugins = discover_plugins()
    # example_simulator should be discoverable
    names = [p['name'] for p in plugins]
    assert 'example_simulator' in names

def test_manifest_local_only():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'] == 'example_simulator'), None)
    assert p is not None
    manifest = load_manifest(p['path'])
    assert manifest.get('network_policy') == 'local-only'
