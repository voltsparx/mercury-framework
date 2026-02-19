import subprocess
import sys


def test_module_launcher_lists_plugins():
    result = subprocess.run(
        [sys.executable, "-m", "mercury", "--list-plugins"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "example_simulator" in result.stdout
