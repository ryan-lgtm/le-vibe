#!/usr/bin/env bash
# One-shot: build le-vibe (stack) and optionally le-vibe-ide .deb artifacts.
# --with-ide delegates to packaging/scripts/build-le-vibe-ide-deb.sh (stage + dpkg-buildpackage + optional lintian).
# Requires: find (findutils), sort, head (coreutils) to locate emitted *.deb files beside the repo.
# Authority: docs/PM_DEB_BUILD_ITERATION.md — PM-scoped convenience; not a v1 production gate.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md when building --with-ide and editor/vscodium/ is empty.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

WITH_IDE=0
DO_INSTALL=0
ASSUME_YES=0
VS_BUILD=""

usage() {
  cat <<'EOF'
Usage: packaging/scripts/build-le-vibe-debs.sh [options]

Build Debian binary packages from this monorepo:
  (default)        Build the le-vibe stack .deb only.
  --with-ide       Also build le-vibe-ide (requires editor/vscodium/VSCode-linux-*).
  --install        After build, sudo apt install the produced .deb files (interactive sudo).
  --yes            Non-interactive apt (adds -y for apt install).
  --vs-build PATH  Use this VSCode-linux-* directory for IDE staging (implies --with-ide).

Environment:
  DEB_BUILD_OPTIONS           Passed through to dpkg-buildpackage when set.
  LEVIBE_IDE_LINTIAN_STRICT   When set to 1, fail the IDE build if lintian fails (see packaging/scripts/build-le-vibe-ide-deb.sh).

Prerequisites (stack): debhelper, build-essential, dpkg-dev (sudo apt install build-essential debhelper).
Prerequisites (IDE):  a successful dev/build.sh under editor/vscodium (see editor/BUILD.md).
  Fresh clone (14.b): git submodule update --init editor/vscodium from repo root if editor/vscodium/ is empty — editor/README.md.

Artifacts:
  Stack:  typically ../le-vibe_*.deb (parent of repo root — standard dpkg-buildpackage).
  IDE:    packaging/le-vibe-ide_*.deb (see packaging/debian-le-vibe-ide/README.md).

EOF
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

require_stack_build_deps() {
  local missing=()
  if ! have_cmd dpkg-buildpackage; then missing+=("dpkg-dev"); fi
  if ! have_cmd dh; then missing+=("debhelper"); fi
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "build-le-vibe-debs: missing packages: ${missing[*]}" >&2
    echo "  Install: sudo apt install -y build-essential debhelper dpkg-dev" >&2
    exit 2
  fi
}

find_stack_deb() {
  # dpkg-buildpackage from repo root writes *.deb to the parent directory.
  local p
  p="$(find "$(cd "$ROOT/.." && pwd)" -maxdepth 1 -name 'le-vibe_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  # Some workflows run from a subdir; search repo root parent only.
  p="$(find "$ROOT/.." -maxdepth 1 -name 'le-vibe_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  echo ""
}

find_ide_deb() {
  local p
  p="$(find "$ROOT/packaging" -maxdepth 1 -name 'le-vibe-ide_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  echo ""
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-ide) WITH_IDE=1 ;;
    --install) DO_INSTALL=1 ;;
    --yes) ASSUME_YES=1 ;;
    --vs-build)
      VS_BUILD="${2:-}"
      if [[ -z "$VS_BUILD" ]]; then echo "build-le-vibe-debs: --vs-build needs a path" >&2; exit 2; fi
      WITH_IDE=1
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "build-le-vibe-debs: unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

require_stack_build_deps

if ! command -v find >/dev/null 2>&1; then
  echo "build-le-vibe-debs: find not on PATH — install findutils (e.g. sudo apt install findutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi
if ! command -v sort >/dev/null 2>&1; then
  echo "build-le-vibe-debs: sort not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi
if ! command -v head >/dev/null 2>&1; then
  echo "build-le-vibe-debs: head not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi

echo "==> Building stack package (le-vibe) from: $ROOT"
dpkg-buildpackage -us -uc -b

STACK_DEB="$(find_stack_deb)"
if [[ -z "$STACK_DEB" || ! -f "$STACK_DEB" ]]; then
  echo "build-le-vibe-debs: could not locate le-vibe_*.deb under $(cd "$ROOT/.." && pwd) — if dpkg-buildpackage failed, fix errors above; on success the stack .deb is emitted beside the repo directory (../le-vibe_*.deb from repo root)." >&2
else
  echo "==> Stack .deb: $STACK_DEB"
fi

IDE_DEB=""
if [[ "$WITH_IDE" -eq 1 ]]; then
  echo "==> Building IDE package (le-vibe-ide) via build-le-vibe-ide-deb.sh (stage + dpkg-buildpackage + optional lintian)"
  if [[ -n "$VS_BUILD" ]]; then
    "$ROOT/packaging/scripts/build-le-vibe-ide-deb.sh" "$VS_BUILD"
  else
    "$ROOT/packaging/scripts/build-le-vibe-ide-deb.sh"
  fi
  IDE_DEB="$(find_ide_deb)"
  if [[ -n "$IDE_DEB" && -f "$IDE_DEB" ]]; then
    echo "==> IDE .deb: $IDE_DEB"
  else
    echo "build-le-vibe-debs: could not locate le-vibe-ide_*.deb under packaging/ — if staging or dpkg-buildpackage failed, see editor/BUILD.md (14.c); empty editor/vscodium/: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
  fi
fi

if [[ "$DO_INSTALL" -eq 1 ]]; then
  if ! have_cmd sudo; then
    echo "build-le-vibe-debs: --install requires sudo" >&2
    exit 2
  fi
  if ! have_cmd apt-get; then
    echo "build-le-vibe-debs: apt-get not on PATH — --install requires apt (Debian/Ubuntu)." >&2
    exit 2
  fi
  APT_ARGS=()
  [[ "$ASSUME_YES" -eq 1 ]] && APT_ARGS+=("-y")
  if [[ -n "$STACK_DEB" && -f "$STACK_DEB" ]]; then
    echo "==> Installing: $STACK_DEB"
    sudo apt-get install "${APT_ARGS[@]}" "$STACK_DEB"
  fi
  if [[ -n "$IDE_DEB" && -f "$IDE_DEB" ]]; then
    echo "==> Installing: $IDE_DEB"
    sudo apt-get install "${APT_ARGS[@]}" "$IDE_DEB"
  fi
fi

echo "==> Done."
