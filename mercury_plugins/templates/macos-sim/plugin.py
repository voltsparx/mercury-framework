"""macOS simulation plugin template - benign example."""
import sys
import os
from mercury.plugin_api import BasePlugin, dispatch_lifecycle


class MacOSSimPlugin(BasePlugin):
    def setup(self):
        print("[macos-sim-template] setup")
        return 0

    def run(self):
        print("[macos-sim-template] run: benign macOS demo")
        return 0

    def cleanup(self):
        print("[macos-sim-template] cleanup")
        return 0


if __name__ == '__main__':
    if os.environ.get('MERCURY_SAFE') != '1':
        print('[macos-sim-template] must be run via Mercury sandbox (MERCURY_SAFE=1)')
        sys.exit(1)
    plugin = MacOSSimPlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
