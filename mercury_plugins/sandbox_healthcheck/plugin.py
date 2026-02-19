from __future__ import annotations

import os
import platform
import sys

from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class SandboxHealthcheckPlugin(BasePlugin):
    def setup(self) -> int:
        print("sandbox_healthcheck setup complete")
        return 0

    def run(self) -> int:
        checks = {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "mercury_safe": os.environ.get("MERCURY_SAFE", "0"),
            "cwd": os.getcwd(),
            "executable": sys.executable,
        }
        print("Sandbox healthcheck:")
        for key, value in checks.items():
            print(f" - {key}: {value}")
        if checks["mercury_safe"] != "1":
            print("Warning: MERCURY_SAFE is not set.")
            return 1
        return 0

    def cleanup(self) -> int:
        print("sandbox_healthcheck cleanup complete")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(SandboxHealthcheckPlugin()))
