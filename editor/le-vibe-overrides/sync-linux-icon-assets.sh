#!/usr/bin/env bash
# Copy Lé Vibe SVG + raster into VSCodium linux resources (PRODUCT_SPEC §7.3 — icons).
# Requires: mkdir, cp (coreutils); rsvg-convert or ImageMagick convert for PNG (see stderr below).
# --check additionally: cmp, sed, mktemp (coreutils).
# Run from repo root before dev/build.sh if you are not using packaging/scripts/ci-vscodium-linux-dev-build.sh.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (required before editor/vscodium/src/... exists).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 Linux icon staging after STEP 0–1.
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VSC="${ROOT}/editor/vscodium"

CHECK=0
case "${1:-}" in
  -h | --help)
    cat <<'EOF'
Usage: editor/le-vibe-overrides/sync-linux-icon-assets.sh [--check]

Copy packaging/icons/hicolor/scalable/apps/le-vibe.svg into
editor/vscodium/src/stable/resources/linux/ and generate le-vibe.png
(rsvg-convert preferred, or ImageMagick convert). Also writes the same mark to
src/stable and src/insider .../vs/workbench/browser/media/code-icon.svg
(1024x1024 — upstream Electron convention) for §7.3 window/workbench chrome.

  --check    Read-only: exit 0 if staged linux le-vibe.svg and workbench
             code-icon.svg files match the packaging canonical; exit 1 if missing
             or different — no writes. Requires cmp, sed, mktemp (coreutils).

Requires editor/vscodium/product.json — git submodule update --init editor/vscodium
(Fresh clone 14.b: editor/README.md).

Usually invoked via packaging/scripts/ci-vscodium-linux-dev-build.sh before dev/build.sh.
See editor/BUILD.md (*Linux icons*).
EOF
    exit 0
    ;;
  --check) CHECK=1 ;;
  "") ;;
  *)
    echo "sync-linux-icon-assets: unknown argument: ${1:-} (try --help)" >&2
    exit 2
    ;;
esac

[[ -f "${VSC}/product.json" ]] || {
  echo "sync-linux-icon-assets: expected editor/vscodium/product.json — run: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
  exit 1
}
SRC_SVG="${ROOT}/packaging/icons/hicolor/scalable/apps/le-vibe.svg"
DEST="${VSC}/src/stable/resources/linux"
[[ -f "$SRC_SVG" ]] || {
  echo "sync-linux-icon-assets: missing ${SRC_SVG} — restore packaging/icons from git (see packaging/icons/hicolor and docs/brand-assets.md)." >&2
  exit 1
}

if [[ "$CHECK" -eq 1 ]]; then
  if ! command -v cmp >/dev/null 2>&1; then
    echo "sync-linux-icon-assets: --check requires cmp (coreutils)." >&2
    exit 1
  fi
  if ! command -v sed >/dev/null 2>&1; then
    echo "sync-linux-icon-assets: --check requires sed." >&2
    exit 1
  fi
  if ! command -v mktemp >/dev/null 2>&1; then
    echo "sync-linux-icon-assets: --check requires mktemp (coreutils) — e.g. sudo apt install coreutils" >&2
    exit 1
  fi
  dest_svg="${DEST}/le-vibe.svg"
  if [[ ! -f "$dest_svg" ]]; then
    echo "sync-linux-icon-assets: --check: missing ${dest_svg} — run sync without --check first (editor/BUILD.md *Linux icons*)." >&2
    exit 1
  fi
  if ! cmp -s "$SRC_SVG" "$dest_svg"; then
    echo "sync-linux-icon-assets: --check: ${dest_svg} differs from ${SRC_SVG} — run sync to refresh (docs/brand-assets.md)." >&2
    exit 1
  fi
  tmp_wb="$(mktemp)"
  sed 's/width="128" height="128"/width="1024" height="1024"/' "$SRC_SVG" >"$tmp_wb"
  for qual in stable insider; do
    dest_wb="${VSC}/src/${qual}/src/vs/workbench/browser/media/code-icon.svg"
    if [[ ! -f "$dest_wb" ]]; then
      rm -f "$tmp_wb"
      echo "sync-linux-icon-assets: --check: missing ${dest_wb} — run sync without --check first (editor/BUILD.md *Linux icons*)." >&2
      exit 1
    fi
    if ! cmp -s "$tmp_wb" "$dest_wb"; then
      rm -f "$tmp_wb"
      echo "sync-linux-icon-assets: --check: ${dest_wb} differs from packaging-derived workbench icon — run sync to refresh (docs/brand-assets.md)." >&2
      exit 1
    fi
  done
  rm -f "$tmp_wb"
  echo "sync-linux-icon-assets: --check OK (linux le-vibe.svg + workbench code-icon.svg match packaging canonical)"
  exit 0
fi

if ! command -v mkdir >/dev/null 2>&1; then
  echo "sync-linux-icon-assets: mkdir not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md §7.3 icons)." >&2
  exit 1
fi
if ! command -v cp >/dev/null 2>&1; then
  echo "sync-linux-icon-assets: cp not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md §7.3 icons)." >&2
  exit 1
fi
if ! command -v sed >/dev/null 2>&1; then
  echo "sync-linux-icon-assets: sed not on PATH — install sed (e.g. sudo apt install sed) (editor/BUILD.md §7.3 icons)." >&2
  exit 1
fi
mkdir -p "$DEST"
cp -f "$SRC_SVG" "${DEST}/le-vibe.svg"
if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w 512 -h 512 "$SRC_SVG" -o "${DEST}/le-vibe.png"
elif command -v convert >/dev/null 2>&1; then
  convert -background none "$SRC_SVG" -resize 512x512 "${DEST}/le-vibe.png"
else
  echo "sync-linux-icon-assets: install rsvg-convert or ImageMagick convert to create le-vibe.png — e.g. sudo apt install librsvg2-bin or sudo apt install imagemagick (Debian/Ubuntu)" >&2
  exit 1
fi
for qual in stable insider; do
  wb_dir="${VSC}/src/${qual}/src/vs/workbench/browser/media"
  mkdir -p "$wb_dir"
  sed 's/width="128" height="128"/width="1024" height="1024"/' "$SRC_SVG" >"${wb_dir}/code-icon.svg"
done
echo "sync-linux-icon-assets: updated ${DEST}/le-vibe.svg, le-vibe.png, and workbench code-icon.svg (stable + insider)"
