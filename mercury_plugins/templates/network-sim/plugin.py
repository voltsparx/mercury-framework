"""Network simulation plugin template - benign example (local-only)."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class NetworkSimPlugin(BasePlugin):
    def setup(self):
        print("[network-sim-template] setup")
        return 0

    def run(self):
        print("[network-sim-template] run: benign local network demo")
        return 0

    def cleanup(self):
        print("[network-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[network-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = NetworkSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
