#!/usr/bin/env bash
# STEP 14 (14.c): after editor/vscodium/dev/build.sh — run launcher smoke against VSCode-linux-*/bin/codium from this tree.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (before toolchain / fetch / build under editor/vscodium/).
# From repo root: ./editor/smoke-built-codium-lvibe.sh
# Requires: python3 and ollama on PATH (same as smoke-lvibe-editor.sh). Exits 1 if no built codium (print-built-codium-path).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "smoke-built-codium-lvibe: python3 not on PATH — install Python 3 (editor/BUILD.md 14.c)." >&2
  exit 5
fi

export LE_VIBE_EDITOR="$("${ROOT}/editor/print-built-codium-path.sh")"
exec "${ROOT}/editor/smoke-lvibe-editor.sh"
