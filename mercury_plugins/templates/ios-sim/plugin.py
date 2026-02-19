"""iOS simulation plugin template - benign example."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class IOSSimPlugin(BasePlugin):
    def setup(self):
        print("[ios-sim-template] setup")
        return 0

    def run(self):
        print("[ios-sim-template] run: benign iOS demo")
        return 0

    def cleanup(self):
        print("[ios-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[ios-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = IOSSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
