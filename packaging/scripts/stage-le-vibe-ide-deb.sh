#!/usr/bin/env bash
# Stage editor/vscodium/VSCode-linux-* for packaging/debian-le-vibe-ide (PRODUCT_SPEC §7.3).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md when editor/vscodium/ is empty.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STAGING="$ROOT/packaging/debian-le-vibe-ide/staging"

find_vsbuild() {
  local arg="${1:-}"
  if [[ -n "$arg" && -d "$arg" ]]; then
    echo "$arg"
    return 0
  fi
  local d
  d="$(find "$ROOT/editor/vscodium" -maxdepth 1 -type d -name 'VSCode-linux-*' -print -quit 2>/dev/null || true)"
  if [[ -n "$d" ]]; then
    echo "$d"
    return 0
  fi
  echo "stage-le-vibe-ide-deb: no VSCode-linux-* under editor/vscodium/ — vendor sources (Fresh clone 14.b: git submodule update --init editor/vscodium — editor/README.md), fetch/build per editor/BUILD.md, then dev/build.sh." >&2
  exit 1
}

VS_DIR="$(find_vsbuild "${1:-}")"
NAME="$(basename "$VS_DIR")"
BIN="$VS_DIR/bin/codium"
if [[ ! -x "$BIN" ]]; then
  echo "stage-le-vibe-ide-deb: not executable: $BIN" >&2
  exit 1
fi

rm -rf "$STAGING"
mkdir -p "$STAGING/usr/lib/le-vibe/ide"
cp -a "$VS_DIR" "$STAGING/usr/lib/le-vibe/ide/$NAME"
mkdir -p "$STAGING/usr/lib/le-vibe/bin"
ln -sfn "../ide/$NAME/bin/codium" "$STAGING/usr/lib/le-vibe/bin/codium"

# §7.3 — Freedesktop menu + hicolor icon (not only the VSCode-linux tree under /usr/lib).
DESKTOP_SRC="$ROOT/packaging/debian-le-vibe-ide/debian/le-vibe.desktop"
ICON_SRC="$ROOT/packaging/icons/hicolor/scalable/apps/le-vibe.svg"
if [[ ! -f "$DESKTOP_SRC" ]]; then
  echo "stage-le-vibe-ide-deb: missing $DESKTOP_SRC" >&2
  exit 1
fi
if [[ ! -f "$ICON_SRC" ]]; then
  echo "stage-le-vibe-ide-deb: missing $ICON_SRC" >&2
  exit 1
fi
install -D -m0644 "$DESKTOP_SRC" "$STAGING/usr/share/applications/le-vibe.desktop"
install -D -m0644 "$ICON_SRC" "$STAGING/usr/share/icons/hicolor/scalable/apps/le-vibe.svg"
echo "stage-le-vibe-ide-deb: staged $STAGING (launcher $STAGING/usr/lib/le-vibe/bin/codium; menu $STAGING/usr/share/applications/le-vibe.desktop)"
