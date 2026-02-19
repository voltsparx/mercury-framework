import subprocess
import sys


def test_quickstart_flag_runs(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mercury",
            "--quickstart",
            "--no-clear",
            "--report-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Quickstart" in result.stdout
