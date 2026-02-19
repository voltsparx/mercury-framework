INSTALL.md

This file explains how to build and install Mercury Framework on supported platforms.

Windows
-------
- Quick ZIP installer (no external tools required):
  - Build artifacts (on Windows machine):
    ```powershell
    .\scripts\build_windows_installer.ps1 -Version 0.3.0
    ```
  - This creates `dist\mercury-framework-0.3.0-win.zip` and `dist\install.ps1`.
  - On target machine extract the ZIP and run `install.ps1` as Administrator to extract to `%ProgramFiles%\MercuryFramework` and create a Start Menu shortcut.

- MSI installer (requires WiX Toolset):
  - Install WiX Toolset and ensure `heat.exe`, `candle.exe`, and `light.exe` are on PATH.
  - Build MSI:
    ```powershell
    .\scripts\build_msi.ps1 -Version 0.3.0
    ```
  - Result: `dist\mercury-framework-0.3.0.msi`.

macOS
-----
- Requires Xcode command line tools (`pkgbuild`, `productbuild`, `hdiutil`).
- Build `.pkg` and `.dmg` on macOS:
  ```bash
  ./scripts/build_macos_installer.sh 0.3.0
  ```
- Result: `dist/mercury-framework-0.3.0.pkg` and `dist/mercury-framework-0.3.0-mac.dmg`.

Debian/Ubuntu (.deb)
---------------------
- Run on a Debian/Ubuntu host with `dpkg-deb` and `fakeroot` installed:
  ```bash
  sudo apt update && sudo apt install -y dpkg-dev fakeroot rsync
  ./scripts/build_debian.sh 0.3.0
  ```
- Result: `dist/mercury-framework_0.3.0_all.deb`.

Arch Linux
----------
- Prepare PKGBUILD and optional `makepkg` build on Arch:
  ```bash
  ./scripts/build_arch.sh 0.3.0        # prepares PKGBUILD and source tarball
  ./scripts/build_arch.sh 0.3.0 --makepkg  # builds the package (on Arch)
  ```
- Result: PKGBUILD in `dist/arch/` and built package if `makepkg` is invoked.

Source / Release ZIP
--------------------
- A release-ready ZIP is available in `dist/mercury-framework-release.zip`. Extracting that file into a clean folder yields the repository contents excluding `.git` and common build artifacts.
- Quick start after extraction (Python 3.10+):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  python -m pip install -e .
  python run.py
  mercury --list-plugins
  ```

Notes
-----
- These installer scripts intentionally do not bundle Python. Ensure Python 3.10+ is available on target systems.
- For production-grade installers you may want to sign the MSI/PKG and run builds from CI runners with signing credentials.
