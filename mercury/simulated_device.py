"""Simulated device stubs for educational testing.

All functions return fake data and explicitly warn the user. These are intended
for use in emulators and isolated labs only.
"""
from __future__ import annotations

import datetime
from typing import List

from .device_profiles import DEFAULT_PROFILE, DeviceProfile, get_profile, list_profiles


class SimulatedDevice:
    """Stateful simulated device with switchable built-in profiles."""

    def __init__(self, profile_key: str = DEFAULT_PROFILE):
        self.profile_key = ""
        self.profile: DeviceProfile = get_profile(DEFAULT_PROFILE)
        self.device_id = "mercury-sim-0001"
        self.model = self.profile.model
        self.os_version = self.profile.os_version
        self.platform = self.profile.platform
        self.locale = self.profile.locale
        self.timezone = self.profile.timezone
        self.carrier = self.profile.carrier
        self.battery_pct = self.profile.battery_pct
        self.switch_profile(profile_key)

    def switch_profile(self, profile_key: str) -> None:
        profile = get_profile(profile_key)
        self.profile = profile
        self.profile_key = profile.key
        self.model = profile.model
        self.os_version = profile.os_version
        self.platform = profile.platform
        self.locale = profile.locale
        self.timezone = profile.timezone
        self.carrier = profile.carrier
        self.battery_pct = profile.battery_pct
        self.device_id = f"mercury-{profile.key}"

    @staticmethod
    def available_profiles() -> list[DeviceProfile]:
        return list_profiles()

    def snapshot(self) -> dict:
        return {
            "profile_key": self.profile_key,
            "device_id": self.device_id,
            "platform": self.platform,
            "model": self.model,
            "os_version": self.os_version,
            "locale": self.locale,
            "timezone": self.timezone,
            "carrier": self.carrier,
            "battery_pct": self.battery_pct,
            "simulated": True,
        }

    def device_info(self) -> str:
        data = self.snapshot()
        return (
            f"Profile: {data['profile_key']}\n"
            f"Device ID: {data['device_id']}\n"
            f"Platform: {data['platform']}\n"
            f"Model: {data['model']}\n"
            f"OS Version: {data['os_version']}\n"
            f"Locale: {data['locale']}\n"
            f"Timezone: {data['timezone']}\n"
            f"Carrier: {data['carrier']}\n"
            f"Battery: {data['battery_pct']}%\n"
            "Note: This is a simulated device. No real device data is accessed."
        )

    def fake_sms(self) -> List[str]:
        """Return fake SMS message strings."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        if self.platform in {"windows", "linux", "macos"}:
            return [
                f"{now} - SOC: Endpoint check-in for {self.model} (simulated)",
                f"{now} - Analyst: Please export training logs (simulated)",
            ]
        if self.platform == "iot":
            return [
                f"{now} - Gateway: Sensor heartbeat received (simulated)",
                f"{now} - Ops: Firmware staging window at 03:00 UTC (simulated)",
            ]
        return [
            f"{now} - Alice: Hey, this is a test message (simulated)",
            f"{now} - Bob: Reminder: meeting at 10:00 (simulated)",
        ]

    def fake_gallery(self) -> List[str]:
        """Return fake gallery entries."""
        base = self.platform.replace(" ", "_")
        return [
            f"{base}_IMG_0001_simulated.jpg",
            f"{base}_IMG_0002_simulated.png",
            f"{base}_capture_simulated.jpg",
        ]

    def fake_camera_frame(self) -> str:
        """Return an ASCII camera frame for demo purposes."""
        return (
            "+----------------------+\n"
            "|   /////////*****    |\n"
            "|   |||||||||||||||    |\n"
            "|   *****///////    |\n"
            "+----------------------+\n"
            "(Simulated camera frame - no real camera used)"
        )
