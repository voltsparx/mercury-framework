"""Android simulation plugin template - do not include any exploit code.

This template demonstrates where authors could add emulator-only scripts
or instrumentation logic for testing and detection training.
"""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class AndroidSimPlugin(BasePlugin):
    def setup(self):
        print("[android-sim-template] setup: ensure emulator is running (author must ensure this)")
        return 0

    def run(self):
        print("[android-sim-template] run: demonstrating safe emulator-only actions")
        # placeholder: instrumentation / benign checks only
        return 0

    def cleanup(self):
        print("[android-sim-template] cleanup: done")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[android-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = AndroidSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
