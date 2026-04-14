#!/usr/bin/env bash
# STEP 14 (14.c): smoke Lé Vibe launcher → editor binary (no long-lived UI).
# Runs: python -m le_vibe.launcher --skip-first-run --editor <bin> -- --version
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (before fetch/build for a repo-local codium path).
# Prereq: `python3` on PATH (launcher); `ollama` on PATH (managed Ollama); see editor/BUILD.md.
# Usage from repo root:
#   LE_VIBE_EDITOR=/path/to/codium ./editor/smoke-lvibe-editor.sh
#   ./editor/smoke-lvibe-editor.sh /path/to/codium
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.c launcher ↔ codium smoke after STEP 0–1.
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/le-vibe"

usage() {
  cat <<'EOF'
Usage: editor/smoke-lvibe-editor.sh [PATH/TO/CODIUM]

Run the Lé Vibe launcher against an editor binary with --version (STEP 14.c — editor/BUILD.md).
PATH defaults to LE_VIBE_EDITOR, else /usr/bin/codium when present.

Requires: python3 and ollama on PATH (managed Ollama).

  -h, --help   Show this message and exit.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

BIN="${1:-${LE_VIBE_EDITOR:-}}"
if [[ -z "${BIN}" ]]; then
  if [[ -x /usr/bin/codium ]]; then
    BIN=/usr/bin/codium
  else
    echo "smoke-lvibe-editor: set LE_VIBE_EDITOR or pass path to codium (built or system). Repo build: git submodule update --init editor/vscodium (Fresh clone 14.b, editor/README.md), then editor/BUILD.md; after dev/build.sh use output of ./editor/print-built-codium-path.sh for LE_VIBE_EDITOR." >&2
    exit 2
  fi
fi

# 14.c — fail fast if the editor path is wrong (before launcher / Ollama).
if [[ "${BIN}" == */* ]]; then
  if [[ ! -f "${BIN}" || ! -x "${BIN}" ]]; then
    echo "smoke-lvibe-editor: not an executable file: ${BIN} (see ./editor/print-built-codium-path.sh after dev/build.sh). Empty editor/vscodium/: git submodule update --init editor/vscodium (Fresh clone 14.b, editor/README.md)." >&2
    exit 4
  fi
else
  if ! command -v "${BIN}" >/dev/null 2>&1; then
    echo "smoke-lvibe-editor: editor not on PATH: ${BIN}" >&2
    exit 4
  fi
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "smoke-lvibe-editor: python3 not on PATH — install Python 3 (editor/BUILD.md 14.c)." >&2
  exit 5
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "smoke-lvibe-editor: need \`ollama\` on PATH for managed Ollama (launcher)." >&2
  exit 3
fi

exec python3 -m le_vibe.launcher --skip-first-run --editor "${BIN}" -- --version
