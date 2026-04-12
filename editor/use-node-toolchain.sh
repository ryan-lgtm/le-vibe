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
set -euo pipefail

EDITOR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_lev_sourced=0
[[ "${BASH_SOURCE[0]}" != "${0}" ]] && _lev_sourced=1 || true

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
  _die "missing ${EDITOR_DIR}/.nvmrc"
fi

pushd "${EDITOR_DIR}" >/dev/null
nvm install
nvm use
popd >/dev/null

if [[ "${_lev_sourced}" -eq 1 ]]; then
  echo "use-node-toolchain: Node $(node --version) ($(command -v node)) - ${EDITOR_DIR}/.nvmrc" >&2
  return 0
fi

if [[ $# -gt 0 ]]; then
  exec "$@"
fi

echo "Node $(node --version) ($(command -v node))"
