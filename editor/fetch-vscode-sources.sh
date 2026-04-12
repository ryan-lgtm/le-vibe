#!/usr/bin/env bash
# STEP 14 (14.b / 14.c): fetch vscode sources via upstream get_repo.sh — monorepo root entrypoint.
# Does not compile. Creates/updates editor/vscodium/vscode/ (network + git). See vscodium/docs/howto-build.md.
#
# Parity: upstream dev/build.sh exports VSCODE_QUALITY / VSCODE_LATEST / CI_BUILD (top of file) before sourcing
# get_repo.sh when SKIP_SOURCE=no — we set the same three defaults here so a standalone fetch matches that path.
# Packaging-only exports from howto-build.md *Build for CI/Downstream* (#build-ci) — SHOULD_BUILD, OS_NAME, … —
# are not required for get_repo alone; use the full upstream block there when reproducing CI packaging.
#
# Prereq: Node from editor/.nvmrc — from repo root: source editor/use-node-toolchain.sh (14.a), or (cd editor && nvm install && nvm use)
# Full local build after fetch: cd editor/vscodium && ./dev/build.sh (see editor/BUILD.md).
# shellcheck disable=SC1091
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f editor/vscodium/product.json ]] || {
  echo "fetch-vscode-sources: expected editor/vscodium (init submodule)." >&2
  exit 1
}

if ! cmp -s editor/.nvmrc editor/vscodium/.nvmrc 2>/dev/null; then
  echo "fetch-vscode-sources: editor/.nvmrc must match editor/vscodium/.nvmrc" >&2
  exit 1
fi

echo "fetch-vscode-sources: use Node $(tr -d '\r\n' < editor/.nvmrc) — e.g. source editor/use-node-toolchain.sh or (cd editor && nvm install && nvm use)"
echo "fetch-vscode-sources: sourcing get_repo.sh from editor/vscodium/ (cwd-sensitive; see BUILD.md)"

cd editor/vscodium

export VSCODE_QUALITY="${VSCODE_QUALITY:-stable}"
export VSCODE_LATEST="${VSCODE_LATEST:-no}"
export CI_BUILD="${CI_BUILD:-no}"

. ./get_repo.sh

echo "fetch-vscode-sources: done. Next: cd editor/vscodium && ./dev/build.sh — then LE_VIBE_EDITOR → VSCode-linux-*/bin/codium (editor/BUILD.md)."
