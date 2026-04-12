#!/usr/bin/env bash
# Stage editor/vscodium/VSCode-linux-* for packaging/debian-le-vibe-ide (PRODUCT_SPEC §7.3).
# H1 / §7.3: not part of default ci.yml le-vibe-deb artifact (stack-only); full-product — docs/apt-repo-releases.md (IDE package); invoked by build-le-vibe-ide-deb.sh / build-le-vibe-debs.sh --with-ide.
# Requires: find (findutils); basename, rm, mkdir, cp, ln, install (coreutils).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md when editor/vscodium/ is empty.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STAGING="$ROOT/packaging/debian-le-vibe-ide/staging"

if ! command -v find >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: find not on PATH — install findutils (e.g. sudo apt install findutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v basename >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: basename not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v rm >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: rm not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v mkdir >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: mkdir not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v cp >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: cp not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v ln >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: ln not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi
if ! command -v install >/dev/null 2>&1; then
  echo "stage-le-vibe-ide-deb: install not on PATH — install coreutils (e.g. sudo apt install coreutils) (§7.3 IDE .deb staging)." >&2
  exit 1
fi

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
  echo "stage-le-vibe-ide-deb: no VSCode-linux-* under editor/vscodium/ — compile first per editor/BUILD.md. From repo root: packaging/scripts/ci-vscodium-linux-dev-build.sh (§7.3 merge + sync-linux-icon-assets.sh, then dev/build.sh), or cd editor/vscodium && ./dev/build.sh after get_repo (run sync + merge yourself — BUILD.md *Linux icons*). Submodule missing: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md). See packaging/debian-le-vibe-ide/README.md." >&2
  exit 1
}

VS_DIR="$(find_vsbuild "${1:-}")"
NAME="$(basename "$VS_DIR")"
BIN="$VS_DIR/bin/codium"
if [[ ! -x "$BIN" ]]; then
  echo "stage-le-vibe-ide-deb: not executable: $BIN — fix permissions or rebuild per editor/BUILD.md (14.c); if editor/vscodium/ is empty: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
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
  echo "stage-le-vibe-ide-deb: missing $DESKTOP_SRC — restore packaging/debian-le-vibe-ide from git (§7.3 desktop template)." >&2
  exit 1
fi
if [[ ! -f "$ICON_SRC" ]]; then
  echo "stage-le-vibe-ide-deb: missing $ICON_SRC — restore packaging/icons from git (see docs/brand-assets.md)." >&2
  exit 1
fi
install -D -m0644 "$DESKTOP_SRC" "$STAGING/usr/share/applications/le-vibe.desktop"
install -D -m0644 "$ICON_SRC" "$STAGING/usr/share/icons/hicolor/scalable/apps/le-vibe.svg"
echo "stage-le-vibe-ide-deb: staged $STAGING (launcher $STAGING/usr/lib/le-vibe/bin/codium; menu $STAGING/usr/share/applications/le-vibe.desktop)"
