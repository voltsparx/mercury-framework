"""Forensic simulation plugin template - benign example."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class ForensicSimPlugin(BasePlugin):
    def setup(self):
        print("[forensic-sim-template] setup")
        return 0

    def run(self):
        print("[forensic-sim-template] run: benign forensic demo")
        return 0

    def cleanup(self):
        print("[forensic-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[forensic-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = ForensicSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
