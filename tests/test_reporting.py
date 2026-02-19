from pathlib import Path

from mercury.reporting import list_reports, write_run_report


def test_write_run_report_creates_json_and_markdown(tmp_path: Path):
    result = {
        "returncode": 0,
        "stdout": "ok",
        "stderr": "",
        "timed_out": False,
        "duration_sec": 0.12,
        "mode": "subprocess",
    }
    report = write_run_report(
        report_dir=tmp_path,
        plugin_name="example_simulator",
        manifest={"version": "0.3.0", "author": "test", "network_policy": "local-only"},
        phases=["run"],
        execution=result,
        runner="subprocess",
    )
    assert report["json_path"].exists()
    assert report["md_path"].exists()

    files = list_reports(tmp_path)
    names = [f.name for f in files]
    assert any(name.endswith(".json") for name in names)
    assert any(name.endswith(".md") for name in names)

