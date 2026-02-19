#!/usr/bin/env bash
# build_macos_installer.sh - create a macOS .pkg and .dmg for Mercury Framework
# Run this on macOS. Requires `pkgbuild` and `productbuild` (Xcode command line tools) and `hdiutil`.

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
VERSION="${1:-0.3.0}"
PKG_NAME="mercury-framework"
STAGING=$(mktemp -d)

mkdir -p "$OUT_DIR"

# Copy repository to staging, exclude VCS and build artifacts
rsync -a --exclude='.git' --exclude='.venv' --exclude='dist' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.github' "$ROOT_DIR/" "$STAGING/$PKG_NAME"

PKG_ROOT="$STAGING/$PKG_NAME"
PKG_IDENTIFIER="org.mercury.framework"
PKG_OUTPUT="$OUT_DIR/${PKG_NAME}-${VERSION}.pkg"

if ! command -v pkgbuild >/dev/null 2>&1; then
  echo "pkgbuild not found. Install Xcode command line tools (xcode-select --install)." >&2
  exit 2
fi

echo "Building component package: $PKG_OUTPUT"
# Install location: /Applications/Mercury Framework
pkgbuild --root "$PKG_ROOT" --identifier "$PKG_IDENTIFIER" --version "$VERSION" --install-location "/Applications/Mercury Framework" "$PKG_OUTPUT"

# Create a user-friendly product archive (not signed)
PRODUCT_PKG="$OUT_DIR/${PKG_NAME}-${VERSION}-product.pkg"
productbuild --package "$PKG_OUTPUT" "$PRODUCT_PKG" || echo "productbuild failed; continuing with component pkg"

# Create a DMG containing the product pkg (or component if product failed)
DMG_OUTPUT="$OUT_DIR/${PKG_NAME}-${VERSION}-mac.dmg"
echo "Creating DMG: $DMG_OUTPUT"
# create a temporary folder to hold the PKG
DMG_CONTENTS="$STAGING/dmg"
mkdir -p "$DMG_CONTENTS"
cp "$PRODUCT_PKG" "$DMG_CONTENTS/" 2>/dev/null || cp "$PKG_OUTPUT" "$DMG_CONTENTS/"
# create dmg using hdiutil
hdiutil create -volname "Mercury Framework" -srcfolder "$DMG_CONTENTS" -ov -format UDZO "$DMG_OUTPUT"

# Cleanup
rm -rf "$STAGING"

echo "macOS installer created: $DMG_OUTPUT (and PKG: $PKG_OUTPUT)"

