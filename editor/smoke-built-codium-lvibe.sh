#!/usr/bin/env bash
# STEP 14 (14.c): after editor/vscodium/dev/build.sh — run launcher smoke against VSCode-linux-*/bin/codium from this tree.
# From repo root: ./editor/smoke-built-codium-lvibe.sh
# Requires: ollama on PATH (same as smoke-lvibe-editor.sh). Exits 1 if no built codium (print-built-codium-path).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export LE_VIBE_EDITOR="$("${ROOT}/editor/print-built-codium-path.sh")"
exec "${ROOT}/editor/smoke-lvibe-editor.sh"
