#!/usr/bin/env bash
# Stage editor/vscodium/VSCode-linux-* for packaging/debian-le-vibe-ide (PRODUCT_SPEC §7.3).
# H1 / §7.3: not part of default ci.yml le-vibe-deb artifact (stack-only); full-product — docs/apt-repo-releases.md (IDE package); invoked by build-le-vibe-ide-deb.sh / build-le-vibe-debs.sh --with-ide.
# Full-product (stack + IDE): build-le-vibe-debs.sh --with-ide prints Full-product install on success — docs/PM_DEB_BUILD_ITERATION.md (Success output (--with-ide)); this script stages for IDE .deb only or as part of that flow.
# Requires: find (findutils); basename, rm, mkdir, cp, ln, install (coreutils).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md when editor/vscodium/ is empty.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 IDE staging before dpkg-buildpackage (STEP 14 after STEP 0–1).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STAGING="$ROOT/packaging/debian-le-vibe-ide/staging"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/stage-le-vibe-ide-deb.sh [PATH]

  PATH   Optional editor/vscodium/VSCode-linux-* directory (default: discover under editor/vscodium/).

Stages the tree into packaging/debian-le-vibe-ide/staging for dpkg-buildpackage (see packaging/debian-le-vibe-ide/README.md).

Environment:
  LEVIBE_STAGE_IDE_ASSERT_BRAND   When 1, fail if resources/app/product.json lacks Lé Vibe or linuxIconName != le-vibe.
  LEVIBE_STAGE_IDE_VERBOSE        When 1, print when §7.3 identity check passes (Lé Vibe + icon key when python3 is available).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

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
  echo "stage-le-vibe-ide-deb: no VSCode-linux-* under editor/vscodium/ — compile first per editor/BUILD.md. From repo root: packaging/scripts/ci-vscodium-linux-dev-build.sh (§7.3 merge + sync-linux-icon-assets.sh, then dev/build.sh), or packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh (Docker, full compile), or cd editor/vscodium && ./dev/build.sh after get_repo (run sync + merge yourself — BUILD.md *Linux icons*). Submodule missing: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md). CI vs maintainer bundles: docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles); packaging/debian-le-vibe-ide/README.md." >&2
  exit 1
}

VS_DIR="$(find_vsbuild "${1:-}")"
NAME="$(basename "$VS_DIR")"
BIN="$VS_DIR/bin/codium"
if [[ ! -e "$BIN" ]]; then
  echo "stage-le-vibe-ide-deb: missing $BIN (partial VSCode-linux tree — finish ./dev/build.sh per editor/BUILD.md 14.c *Partial tree*). From repo root: ./editor/print-built-codium-path.sh (diagnostics). If editor/vscodium/ is empty: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md). CI vs maintainer bundles: docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles); packaging/debian-le-vibe-ide/README.md." >&2
  exit 1
fi
if [[ ! -x "$BIN" ]]; then
  echo "stage-le-vibe-ide-deb: not executable: $BIN — fix permissions or rebuild per editor/BUILD.md (14.c); if editor/vscodium/ is empty: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md). CI vs maintainer bundles: docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles); packaging/debian-le-vibe-ide/README.md." >&2
  exit 1
fi

# §7.3 shipped identity: built Electron tree should contain merged product strings (ci-vscodium-linux-dev-build.sh before dev/build.sh).
# Set LEVIBE_STAGE_IDE_ASSERT_BRAND=1 to fail if missing; default is warn-only. LEVIBE_STAGE_IDE_VERBOSE=1 prints OK when branded.
PRODUCT_JSON="$VS_DIR/resources/app/product.json"
_assert_brand="${LEVIBE_STAGE_IDE_ASSERT_BRAND:-0}"
if [[ -f "$PRODUCT_JSON" ]]; then
  if ! grep -q 'Lé Vibe' "$PRODUCT_JSON" 2>/dev/null; then
    echo "stage-le-vibe-ide-deb: warning: $PRODUCT_JSON has no Lé Vibe strings — build likely skipped packaging/scripts/ci-vscodium-linux-dev-build.sh (product merge + icons) before dev/build.sh — editor/BUILD.md *Linux icons*" >&2
    if [[ "$_assert_brand" == "1" ]]; then
      exit 1
    fi
  else
    # §7.3 linux icon key — must match packaging/icons/hicolor/scalable/apps/le-vibe.svg (docs/brand-assets.md).
    if command -v python3 >/dev/null 2>&1; then
      if ! python3 -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); sys.exit(0 if d.get('linuxIconName')=='le-vibe' else 1)" "$PRODUCT_JSON" 2>/dev/null; then
        echo "stage-le-vibe-ide-deb: warning: $PRODUCT_JSON linuxIconName is not le-vibe — align editor/le-vibe-overrides/product-branding-merge.json before dev/build.sh (editor/BUILD.md *Linux icons*)." >&2
        if [[ "$_assert_brand" == "1" ]]; then
          exit 1
        fi
      elif [[ "${LEVIBE_STAGE_IDE_VERBOSE:-0}" == "1" ]]; then
        echo "stage-le-vibe-ide-deb: §7.3 OK — Lé Vibe + linuxIconName le-vibe in resources/app/product.json" >&2
      fi
    elif [[ "${LEVIBE_STAGE_IDE_VERBOSE:-0}" == "1" ]]; then
      echo "stage-le-vibe-ide-deb: §7.3 OK — Lé Vibe strings in resources/app/product.json (python3 absent — skipped linuxIconName check)" >&2
    fi
  fi
else
  echo "stage-le-vibe-ide-deb: warning: missing $PRODUCT_JSON — cannot verify §7.3 identity in this VSCode-linux-* tree" >&2
  if [[ "$_assert_brand" == "1" ]]; then
    exit 1
  fi
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
