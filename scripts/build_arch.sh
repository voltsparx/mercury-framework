#!/usr/bin/env bash
# build_arch.sh - prepare Arch PKGBUILD and optionally build package
# Usage: ./scripts/build_arch.sh [version] [--makepkg]
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist/arch"
VERSION="${1:-0.3.0}"
MAKEPKG=${2:-}
PKG_NAME="mercury-framework"

mkdir -p "$OUT_DIR"
SRC_TARBALL="$OUT_DIR/${PKG_NAME}-${VERSION}.tar.gz"

echo "Creating source tarball: $SRC_TARBALL"
tar --exclude='.git' --exclude='.venv' --exclude='dist' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.github' -czf "$SRC_TARBALL" -C "$ROOT_DIR" .

PKGBUILD_FILE="$OUT_DIR/PKGBUILD"
cat > "$PKGBUILD_FILE" <<PKGBUILD
pkgname=${PKG_NAME}
pkgver=${VERSION}
pkgrel=1
pkgdesc="Mercury Framework (safe educational scaffold)"
arch=(any)
url="https://example.local/mercury-framework"
license=(MIT)
depends=(python)
source=("${SRC_TARBALL##*/}")
sha256sums=('SKIP')

package() {
  mkdir -p "$pkgdir/usr/share/${PKG_NAME}"
  tar -xzf "$srcdir/${SRC_TARBALL##*/}" -C "$pkgdir/usr/share/${PKG_NAME}"
}
PKGBUILD

echo "PKGBUILD written to $PKGBUILD_FILE"

if [ "$MAKEPKG" = "--makepkg" ]; then
  if ! command -v makepkg >/dev/null 2>&1; then
    echo "makepkg not found. Run this on an Arch environment or add --makepkg when on Arch." >&2
    exit 2
  fi
  echo "Running makepkg in $OUT_DIR"
  (cd "$OUT_DIR" && makepkg -s)
fi

echo "Arch packaging artifacts prepared in: $OUT_DIR"

