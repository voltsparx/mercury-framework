"""Firmware simulation template - benign example."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class FirmwareSimPlugin(BasePlugin):
    def setup(self):
        print("[firmware-sim-template] setup")
        return 0

    def run(self):
        print("[firmware-sim-template] run: benign firmware demo")
        return 0

    def cleanup(self):
        print("[firmware-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[firmware-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = FirmwareSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
