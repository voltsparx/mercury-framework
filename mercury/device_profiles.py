"""Built-in simulated device profiles for labs and training demos."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    label: str
    platform: str
    model: str
    os_version: str
    locale: str
    timezone: str
    carrier: str
    battery_pct: int


DEFAULT_PROFILE = "android_pixel_lab"


PROFILES: dict[str, DeviceProfile] = {
    "android_pixel_lab": DeviceProfile(
        key="android_pixel_lab",
        label="Android Pixel Lab",
        platform="android",
        model="Pixel 8 Simulator",
        os_version="Android 15 (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="LabCell",
        battery_pct=84,
    ),
    "android_legacy_avd": DeviceProfile(
        key="android_legacy_avd",
        label="Android Legacy AVD",
        platform="android",
        model="Nexus 5X Emulator",
        os_version="Android 9 (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="LegacyLab",
        battery_pct=61,
    ),
    "windows_workstation": DeviceProfile(
        key="windows_workstation",
        label="Windows Workstation",
        platform="windows",
        model="Windows 11 Pro VM",
        os_version="Windows 11 23H2 (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="Ethernet-Lab",
        battery_pct=100,
    ),
    "linux_analyst_vm": DeviceProfile(
        key="linux_analyst_vm",
        label="Linux Analyst VM",
        platform="linux",
        model="Ubuntu 24.04 VM",
        os_version="Ubuntu 24.04 LTS (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="LabBridge",
        battery_pct=100,
    ),
    "macos_research_vm": DeviceProfile(
        key="macos_research_vm",
        label="macOS Research VM",
        platform="macos",
        model="macOS Sonoma VM",
        os_version="macOS 14 (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="Wi-Fi Lab",
        battery_pct=76,
    ),
    "iot_gateway_lab": DeviceProfile(
        key="iot_gateway_lab",
        label="IoT Gateway Lab",
        platform="iot",
        model="Edge Gateway Rev B",
        os_version="Embedded Linux 6.x (simulated)",
        locale="en-US",
        timezone="UTC",
        carrier="LabMesh",
        battery_pct=100,
    ),
}


def get_profile(profile_key: str) -> DeviceProfile:
    if profile_key not in PROFILES:
        available = ", ".join(sorted(PROFILES.keys()))
        raise ValueError(f"Unknown profile '{profile_key}'. Available: {available}")
    return PROFILES[profile_key]


def list_profiles() -> list[DeviceProfile]:
    return [PROFILES[key] for key in sorted(PROFILES.keys())]


def profile_keys() -> list[str]:
    return sorted(PROFILES.keys())
