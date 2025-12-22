import os
import subprocess
import sys
from mercury.plugin_loader import discover_plugins


def run_cmd(path, args):
    env = os.environ.copy()
    env["MERCURY_SAFE"] = "1"

    p = subprocess.run(
        [sys.executable, path] + args,
        capture_output=True,
        text=True,
        env=env,
    )
    return p.returncode, p.stdout, p.stderr


def test_example_plugin_lifecycle():
    plugins = discover_plugins()

    p = next((p for p in plugins if p["name"] == "example_simulator"), None)
    assert p is not None

    # ✅ CROSS-PLATFORM path handling
    plugin_py = os.path.join(p["path"], "plugin.py")

    assert os.path.exists(plugin_py), f"plugin.py not found at {plugin_py}"

    # ---- setup ----
    rc, out, err = run_cmd(plugin_py, ["--setup"])
    assert rc == 0, f"setup failed: {out} {err}"
    assert "setup" in out.lower()

    # ---- run ----
    rc, out, err = run_cmd(plugin_py, ["--run"])
    assert rc == 0, f"run failed: {out} {err}"
    assert "running safe example plugin" in out.lower()

    # ---- cleanup ----
    rc, out, err = run_cmd(plugin_py, ["--cleanup"])
    assert rc == 0, f"cleanup failed: {out} {err}"
    assert "cleanup" in out.lower()
