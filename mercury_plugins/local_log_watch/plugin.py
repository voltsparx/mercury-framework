from __future__ import annotations

from mercury.plugin_api import BasePlugin, dispatch_lifecycle
from detection.log_parser import find_suspicious_lines


class LocalLogWatchPlugin(BasePlugin):
    def setup(self) -> int:
        print("local_log_watch setup complete")
        return 0

    def run(self) -> int:
        sample_log = """
        2026-01-10 12:00:00 INFO user login ok
        2026-01-10 12:00:02 WARN reverse shell keyword found in test payload
        2026-01-10 12:00:03 INFO process start /bin/bash -c echo
        """
        matches = find_suspicious_lines(sample_log)
        if not matches:
            print("No suspicious lines found in sample log.")
            return 0
        print("Suspicious sample lines:")
        for line in matches:
            print(f" - {line.strip()}")
        return 0

    def cleanup(self) -> int:
        print("local_log_watch cleanup complete")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(LocalLogWatchPlugin()))
