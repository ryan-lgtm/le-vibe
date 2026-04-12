#!/usr/bin/env bash
# STEP 14 (14.c): smoke Lé Vibe launcher → editor binary (no long-lived UI).
# Runs: python -m le_vibe.launcher --skip-first-run --editor <bin> -- --version
# Prereq: `ollama` on PATH (managed Ollama); see editor/BUILD.md.
# Usage from repo root:
#   LE_VIBE_EDITOR=/path/to/codium ./editor/smoke-lvibe-editor.sh
#   ./editor/smoke-lvibe-editor.sh /path/to/codium
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/le-vibe"

BIN="${1:-${LE_VIBE_EDITOR:-}}"
if [[ -z "${BIN}" ]]; then
  if [[ -x /usr/bin/codium ]]; then
    BIN=/usr/bin/codium
  else
    echo "smoke-lvibe-editor: set LE_VIBE_EDITOR or pass path to codium (built or system)." >&2
    exit 2
  fi
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "smoke-lvibe-editor: need \`ollama\` on PATH for managed Ollama (launcher)." >&2
  exit 3
fi

exec python3 -m le_vibe.launcher --skip-first-run --editor "${BIN}" -- --version
