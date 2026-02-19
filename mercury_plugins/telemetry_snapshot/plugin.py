from __future__ import annotations

from datetime import datetime, timezone
import json

from mercury.plugin_api import BasePlugin, dispatch_lifecycle
from mercury.simulated_device import SimulatedDevice
from mercury.simulated_sensors import sensor_readings
from mercury.simulated_storage import storage_listing


class TelemetrySnapshotPlugin(BasePlugin):
    def setup(self) -> int:
        print("telemetry_snapshot setup complete")
        return 0

    def run(self) -> int:
        device = SimulatedDevice(profile_key="android_pixel_lab")
        payload = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "device": device.snapshot(),
            "sensors": sensor_readings(),
            "storage_preview": storage_listing()[:5],
        }
        print(json.dumps(payload, indent=2))
        return 0

    def cleanup(self) -> int:
        print("telemetry_snapshot cleanup complete")
        return 0


if __name__ == "__main__":
    raise SystemExit(dispatch_lifecycle(TelemetrySnapshotPlugin()))
