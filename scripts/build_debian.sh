#!/usr/bin/env bash
# build_debian.sh - build a .deb package for Mercury Framework
# Run this on a Debian/Ubuntu machine with dpkg-deb available.

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
VERSION="${1:-0.3.0}"
PKG_NAME="mercury-framework"
ARCH="all"

mkdir -p "$OUT_DIR"
STAGING=$(mktemp -d)
DEBIAN_DIR="$STAGING/DEBIAN"
USR_SHARE="$STAGING/usr/share/$PKG_NAME"

mkdir -p "$DEBIAN_DIR" "$USR_SHARE"

cat > "$DEBIAN_DIR/control" <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: voltsparx <voltsparx@gmail.com>
Depends: python3
Description: Mercury Framework (safe educational scaffold)
 A plugin-driven, simulated-device educational scaffold.
EOF

# copy files
rsync -a --exclude='.git' --exclude='.venv' --exclude='dist' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.github' "$ROOT_DIR/" "$USR_SHARE/"

OUT_DEB="$OUT_DIR/${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo "Building .deb -> $OUT_DEB"
if ! command -v dpkg-deb >/dev/null 2>&1; then
  echo "dpkg-deb not found. Please run on Debian/Ubuntu or install dpkg-deb." >&2
  exit 2
fi

fakeroot dpkg-deb --build "$STAGING" "$OUT_DEB"

rm -rf "$STAGING"

echo "Debian package built: $OUT_DEB"

