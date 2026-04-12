#!/usr/bin/env bash
# Copy Lé Vibe SVG + raster into VSCodium linux resources (PRODUCT_SPEC §7.3 — icons).
# Run from repo root before dev/build.sh if you are not using packaging/scripts/ci-vscodium-linux-dev-build.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC_SVG="${ROOT}/packaging/icons/hicolor/scalable/apps/le-vibe.svg"
DEST="${ROOT}/editor/vscodium/src/stable/resources/linux"
[[ -f "$SRC_SVG" ]] || {
  echo "sync-linux-icon-assets: missing ${SRC_SVG}" >&2
  exit 1
}
mkdir -p "$DEST"
cp -f "$SRC_SVG" "${DEST}/le-vibe.svg"
if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w 512 -h 512 "$SRC_SVG" -o "${DEST}/le-vibe.png"
elif command -v convert >/dev/null 2>&1; then
  convert -background none "$SRC_SVG" -resize 512x512 "${DEST}/le-vibe.png"
else
  echo "sync-linux-icon-assets: install rsvg-convert (librsvg2-bin) or ImageMagick convert to create le-vibe.png" >&2
  exit 1
fi
echo "sync-linux-icon-assets: updated ${DEST}/le-vibe.svg and le-vibe.png"
