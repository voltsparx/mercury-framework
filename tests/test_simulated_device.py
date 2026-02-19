from mercury.simulated_device import SimulatedDevice


def test_fake_sms_returns_list():
    device = SimulatedDevice()
    messages = device.fake_sms()
    assert isinstance(messages, list)
    assert messages


def test_device_info_mentions_simulation():
    device = SimulatedDevice()
    info = device.device_info().lower()
    assert "simulated" in info


def test_fake_camera_frame_is_simulated():
    device = SimulatedDevice()
    frame = device.fake_camera_frame()
    assert "Simulated camera frame" in frame


def test_device_profile_switch_changes_platform():
    device = SimulatedDevice()
    device.switch_profile("linux_analyst_vm")
    assert device.platform == "linux"
    assert device.profile_key == "linux_analyst_vm"


def test_device_profiles_list_is_available():
    profiles = SimulatedDevice.available_profiles()
    assert profiles
    keys = {profile.key for profile in profiles}
    assert "android_pixel_lab" in keys
    assert "windows_workstation" in keys
