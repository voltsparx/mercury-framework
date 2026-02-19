#!/usr/bin/env bash
set -euo pipefail

# build_packages.sh - build .deb and Arch .pkg.tar.zst from this repo
# Usage: ./scripts/build_packages.sh [version]

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
VERSION="${1:-3.0.0}"

mkdir -p "$OUT_DIR"

echo "Building packages for Mercury Framework v$VERSION"
#### Debian packaging (uses dpkg-deb)
DEB_DIR="$(mktemp -d)"
DEB_DIR="$OUT_DIR/deb"
PKG_NAME="mercury-framework"
ARCH="all"
mkdir -p "$DEB_DIR/DEBIAN"
cat > "$DEB_DIR/DEBIAN/control" <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: voltsparx <voltsparx@gmail.com>
Description: Mercury Framework (safe educational scaffold)
 A plugin-driven, simulated-device educational scaffold.
EOF

rsync -a --exclude='.git' --exclude='.venv' --exclude='dist' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.github' "$ROOT_DIR/" "$DEB_DIR/usr/share/$PKG_NAME/"
rsync -a --exclude='.git' --exclude='.venv' --exclude='dist' "$ROOT_DIR/" "$DEB_DIR/usr/share/$PKG_NAME/"

OUT_DEB="$OUT_DIR/${PKG_NAME}_${VERSION}_${ARCH}.deb"
dpkg-deb --build "$DEB_DIR" "$OUT_DEB"
dpkg-deb --build "$DEB_DIR" "$OUT_DIR/${PKG_NAME}_${VERSION}_${ARCH}.deb"
#### Arch package (prepare source tarball + PKGBUILD)
#### Arch package (PKGBUILD-based)
ARCH_DIR="$OUT_DIR/arch"
mkdir -p "$ARCH_DIR/$PKG_NAME-$VERSION"
echo "Preparing Arch package tree..."
rsync -a --exclude='.git' --exclude='.venv' --exclude='dist' "$ROOT_DIR/" "$ARCH_DIR/$PKG_NAME-$VERSION/$PKG_NAME"
tar --exclude='.git' --exclude='.venv' --exclude='dist' --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.github' -czf "$SRC_TARBALL" -C "$ROOT_DIR" .
cat > "$ARCH_DIR/PKGBUILD" <<'PKGBUILD'
pkgname=mercury-framework
pkgver=${pkgver}
pkgrel=1
pkgdesc="Mercury Framework (safe educational scaffold)"
arch=(any)
url="https://example.local/mercury-framework"
license=(MIT)
depends=(python)
source=("${pkgname}-${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
  mkdir -p "$pkgdir/usr/share/$pkgname"
  cp -r "$srcdir/$pkgname"/* "$pkgdir/usr/share/$pkgname/"
}
PKGBUILD

echo "Arch package stub created. To build an Arch package run inside an Arch environment:"
echo "  cd $ARCH_DIR && makepkg -s"

echo "All done. Packages available under: $OUT_DIR"


