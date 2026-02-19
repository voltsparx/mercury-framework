#!/usr/bin/env python3
"""Prepare Unix packaging artifacts for Mercury Framework.

- Creates a source tarball under `dist/`.
- Writes a PKGBUILD for Arch under `dist/arch/`.
- If `dpkg-deb` is available (Linux), builds a .deb package into `dist/`.

This script is intended to be runnable on any platform; building a .deb
requires `dpkg-deb` and rootless packaging tools available on Linux.
"""
from __future__ import annotations
import os
import tarfile
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
PKG_NAME = 'mercury-framework'
VERSION = sys.argv[1] if len(sys.argv) > 1 else '0.3.0'

OUT.mkdir(exist_ok=True)

# Create source tarball by walking the tree and adding files while excluding patterns.
SRC_TARBALL = OUT / f"{PKG_NAME}-{VERSION}.tar.gz"
print(f"Creating source tarball: {SRC_TARBALL}")
excludes = {'.git', '.venv', 'dist', '__pycache__', '.pytest_cache', '.github'}
with tarfile.open(SRC_TARBALL, 'w:gz') as tar:
    for root, dirs, files in os.walk(ROOT):
        # compute relative path from ROOT
        rel_root = os.path.relpath(root, ROOT)
        # skip excluded top-level directories
        if rel_root == '.' or not any(part in excludes for part in rel_root.split(os.sep)):
            for f in files:
                # skip files in excluded dirs
                full = os.path.join(root, f)
                rel = os.path.relpath(full, ROOT)
                # skip if any path component is excluded
                if any(part in excludes for part in rel.split(os.sep)):
                    continue
                tar.add(full, arcname=rel)

# Write PKGBUILD under dist/arch
ARCH_DIR = OUT / 'arch'
ARCH_DIR.mkdir(parents=True, exist_ok=True)
PKGBUILD = ARCH_DIR / 'PKGBUILD'
print(f"Writing PKGBUILD to: {PKGBUILD}")
PKGBUILD.write_text(f"""pkgname={PKG_NAME}
pkgver={VERSION}
pkgrel=1
pkgdesc=\"Mercury Framework (safe educational scaffold)\"
arch=(any)
url=\"https://example.local/mercury-framework\"
license=(MIT)
depends=(python)
source=("{SRC_TARBALL.name}")
sha256sums=('SKIP')

package() {{
  mkdir -p "$pkgdir/usr/share/{PKG_NAME}"
  tar -xzf "$srcdir/{SRC_TARBALL.name}" -C "$pkgdir/usr/share/{PKG_NAME}"
}}
""")

# Attempt to build a .deb if dpkg-deb exists
if shutil.which('dpkg-deb'):
    print('dpkg-deb found - attempting to build .deb (may require Linux).')
    tmp_deb = OUT / 'debbuild'
    if tmp_deb.exists():
        shutil.rmtree(tmp_deb)
    usr_share = tmp_deb / 'usr' / 'share' / PKG_NAME
    usr_share.mkdir(parents=True, exist_ok=True)
    # copy files
    shutil.copytree(ROOT, usr_share, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git', '.venv', 'dist', '__pycache__', '.pytest_cache', '.github'))
    deb_control = tmp_deb / 'DEBIAN'
    deb_control.mkdir(parents=True, exist_ok=True)
    control = deb_control / 'control'
    control.write_text(f"""Package: {PKG_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: all
Maintainer: voltsparx <voltsparx@gmail.com>
Depends: python3
Description: Mercury Framework (safe educational scaffold)
 A plugin-driven, simulated-device educational scaffold.
""")
    out_deb = OUT / f"{PKG_NAME}_{VERSION}_all.deb"
    subprocess.check_call(['dpkg-deb', '--build', str(tmp_deb), str(out_deb)])
    shutil.rmtree(tmp_deb)
    print(f"Built .deb: {out_deb}")
else:
    print('dpkg-deb not found - skipping .deb build (OK on non-Linux hosts).')

print('Prepared Unix packaging artifacts under:', OUT)

