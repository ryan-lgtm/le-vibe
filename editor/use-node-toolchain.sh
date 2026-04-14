#!/usr/bin/env bash
# STEP 14.a — Node toolchain: nvm install / nvm use from editor/.nvmrc (must match editor/vscodium/.nvmrc; see ci-editor-nvmrc-sync).
#
# From repo root, load nvm + Node in your current shell:
#   source editor/use-node-toolchain.sh
#   (prints one stderr line: active node path + version + editor/.nvmrc path — 14.a)
#
# Or run one command with that Node on PATH (subprocess):
#   ./editor/use-node-toolchain.sh node --version
#   ./editor/use-node-toolchain.sh ./editor/fetch-vscode-sources.sh
#
# Requires nvm: https://github.com/nvm-sh/nvm (default NVM_DIR=~/.nvm)
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (editor/.nvmrc tracks editor/vscodium/.nvmrc).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.a Node toolchain after STEP 0–1.
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

EDITOR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_lev_sourced=0
[[ "${BASH_SOURCE[0]}" != "${0}" ]] && _lev_sourced=1 || true

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: source editor/use-node-toolchain.sh
   or: editor/use-node-toolchain.sh [COMMAND [ARGS...]]

Load nvm and activate Node from editor/.nvmrc (STEP 14.a — must match
editor/vscodium/.nvmrc; see packaging/scripts/ci-editor-nvmrc-sync.sh).

When executed (not sourced), runs COMMAND with that Node on PATH, or prints
the active node path if COMMAND is omitted.

Requires: nvm (default NVM_DIR=~/.nvm).

  -h, --help   Show this message and exit.
EOF
  if [[ "${_lev_sourced}" -eq 1 ]]; then
    return 0
  fi
  exit 0
fi

_die() {
  echo "use-node-toolchain: $*" >&2
  if [[ "${_lev_sourced}" -eq 1 ]]; then
    return 1
  fi
  exit 1
}

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ ! -s "${NVM_DIR}/nvm.sh" ]]; then
  _die "nvm not found — install nvm or set NVM_DIR (expected ${NVM_DIR}/nvm.sh)"
fi
# shellcheck source=/dev/null
source "${NVM_DIR}/nvm.sh"

if [[ ! -f "${EDITOR_DIR}/.nvmrc" ]]; then
  _die "missing ${EDITOR_DIR}/.nvmrc — restore from git; Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md; then align pins per packaging/scripts/ci-editor-nvmrc-sync.sh (14.a)."
fi

pushd "${EDITOR_DIR}" >/dev/null
nvm install
nvm use
popd >/dev/null

if ! command -v node >/dev/null 2>&1; then
  _die "node not on PATH after nvm install/use — check nvm and editor/.nvmrc (editor/BUILD.md 14.a)."
fi

if [[ "${_lev_sourced}" -eq 1 ]]; then
  echo "use-node-toolchain: Node $(node --version) ($(command -v node)) - ${EDITOR_DIR}/.nvmrc" >&2
  return 0
fi

if [[ $# -gt 0 ]]; then
  exec "$@"
fi

echo "Node $(node --version) ($(command -v node))"
