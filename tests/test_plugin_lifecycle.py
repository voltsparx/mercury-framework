import os
import sys
import subprocess
from mercury.plugin_loader import discover_plugins

def run_cmd(path, args):
    env = os.environ.copy()
    env['MERCURY_SAFE'] = '1'
    p = subprocess.run([sys.executable, path] + args, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr

def test_example_plugin_lifecycle():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'] == 'example_simulator'), None)
    assert p is not None
    plugin_py = os.path.join(p['path'], 'plugin.py')

    # run setup
    rc, out, err = run_cmd(plugin_py, ['--setup'])
    assert rc == 0
    assert 'setup' in out.lower()

    # run main
    rc, out, err = run_cmd(plugin_py, ['--run'])
    assert rc == 0
    assert 'running safe example plugin' in out.lower()

    # run cleanup
    rc, out, err = run_cmd(plugin_py, ['--cleanup'])
    assert rc == 0
    assert 'cleanup' in out.lower()
