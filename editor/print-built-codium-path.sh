#!/usr/bin/env bash
# STEP 14 (14.c): print absolute path to editor/vscodium/VSCode-linux-*/bin/codium if a local dev/build.sh output exists.
# Run from repo root: ./editor/print-built-codium-path.sh
# Use: export LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)" && ./editor/smoke-lvibe-editor.sh
# For an unpacked CI tarball or any other tree, use ./editor/print-vsbuild-codium-path.sh [DIR] (14.f).
# No-op network; exits 1 if no match (build not run or different layout).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VSC="${ROOT}/editor/vscodium"

[[ -f "${VSC}/product.json" ]] || {
  echo "print-built-codium-path: expected editor/vscodium (init submodule)." >&2
  exit 1
}

exec "${ROOT}/editor/print-vsbuild-codium-path.sh" "$VSC"
