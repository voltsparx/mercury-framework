"""Linux simulation plugin template - benign example."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class LinuxSimPlugin(BasePlugin):
    def setup(self):
        print("[linux-sim-template] setup")
        return 0

    def run(self):
        print("[linux-sim-template] run: benign linux demo")
        return 0

    def cleanup(self):
        print("[linux-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[linux-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = LinuxSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
