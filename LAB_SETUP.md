Lab setup and emulator guidance for Mercury v3.0 (safe testing only)

This document explains how to prepare isolated test environments for Mercury
plugins and templates. Always get written permission before testing on any
system you do not own.

1) Local VM approach (recommended)
- Create virtual machines using VirtualBox, VMware, or cloud instances.
- Use snapshots to revert state between tests.
- Create isolated networks (host-only or internal) so the VM cannot reach the Internet.

2) Android emulator (AVD) guidance
- Install Android Studio and use `avdmanager` to create AVDs for the versions you want to test (Android 8-16).
- Use `adb` to install benign test APKs from `samples/android_template`.
- Run plugins marked `android-sim` against the emulator only.

3) macOS testing
- Use dedicated macOS hosts or cloud macOS runners where permitted. Prefer VM snapshots and isolated networks.

4) Network isolation
- Use firewall rules or container networks that restrict external access.
- For network-focused templates, restrict endpoints to `127.0.0.1` or lab-controlled hosts.

5) Consent and legal checklist
- Confirm written authorization to test the target environment.
- Document scope, start/end dates, and contact persons.
- Do not test on third-party or production systems without explicit written consent.

6) Notes
- The repository is intended for educational simulation and testing. It does not include exploit payloads.
- For reproducible research, consider using VM images and provide checksums for reviewers.
