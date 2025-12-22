"""Example safe plugin for Mercury framework.

This plugin demonstrates safe, local-only behavior.
"""

import os
import sys
import socket

from mercury.plugin_api import BasePlugin, dispatch_lifecycle


def demo_local_connect(host="127.0.0.1", port=9001):
    """Attempt a safe local connection."""
    try:
        s = socket.create_connection((host, port), timeout=1)
        with s:
            s.sendall(b"hello from example_simulator\n")
            resp = s.recv(1024)
            print("[example_simulator] received:", resp.decode(errors="ignore").strip())
    except Exception as e:
        print("[example_simulator] local connect failed (expected if no server):", e)


class ExamplePlugin(BasePlugin):
    def setup(self):
        print("[example_simulator] setup (no-op)")
        return 0

    def run(self):
        print("[example_simulator] running safe example plugin")
        # Print simulated device info if available
        try:
            from mercury.simulated_device import SimulatedDevice
            device = SimulatedDevice()
            print(device.device_info())
        except ImportError:
            print("[example_simulator] no simulated device available")
        # Demonstrate local-only network behavior
        demo_local_connect()
        return 0

    def cleanup(self):
        print("[example_simulator] cleanup (no-op)")
        return 0


if __name__ == "__main__":
    # Safety check: must run inside Mercury sandbox
    if os.environ.get("MERCURY_SAFE") != "1":
        print("[example_simulator] must be run via Mercury sandbox (MERCURY_SAFE=1)")
        sys.exit(1)

    plugin = ExamplePlugin()
    rc = dispatch_lifecycle(plugin)
    sys.exit(rc)
