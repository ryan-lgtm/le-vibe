#!/usr/bin/env bash
# STEP 14 (14.b / 14.c): fetch vscode sources via upstream get_repo.sh — monorepo root entrypoint.
# Does not compile. Creates/updates editor/vscodium/vscode/ (network + git). See vscodium/docs/howto-build.md.
#
# Parity: upstream dev/build.sh exports VSCODE_QUALITY / VSCODE_LATEST / CI_BUILD (top of file) before sourcing
# get_repo.sh when SKIP_SOURCE=no — we set the same three defaults here so a standalone fetch matches that path.
# Packaging-only exports from howto-build.md *Build for CI/Downstream* (#build-ci) — SHOULD_BUILD, OS_NAME, … —
# are not required for get_repo alone; use the full upstream block there when reproducing CI packaging.
#
# Prereq: cmp and tr (coreutils), Node from editor/.nvmrc — from repo root: source editor/use-node-toolchain.sh (14.a), or (cd editor && nvm install && nvm use)
# Full local build after fetch: cd editor/vscodium && ./dev/build.sh (see editor/BUILD.md).
# Fresh clone (14.b): git submodule update --init editor/vscodium from repo root when editor/vscodium/ is empty — editor/README.md.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.b get_repo / vscode fetch after STEP 0–1.
# shellcheck disable=SC1091
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f editor/vscodium/product.json ]] || {
  echo "fetch-vscode-sources: expected editor/vscodium/ — run: git submodule update --init editor/vscodium (editor/README.md Fresh clone 14.b)." >&2
  exit 1
}

if ! command -v cmp >/dev/null 2>&1; then
  echo "fetch-vscode-sources: cmp not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.a)." >&2
  exit 1
fi
if ! command -v tr >/dev/null 2>&1; then
  echo "fetch-vscode-sources: tr not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.a)." >&2
  exit 1
fi

if ! cmp -s editor/.nvmrc editor/vscodium/.nvmrc 2>/dev/null; then
  echo "fetch-vscode-sources: editor/.nvmrc differs from editor/vscodium/.nvmrc — update editor/.nvmrc to match upstream pin after a vendor bump (14.a); see editor/README.md." >&2
  exit 1
fi

echo "fetch-vscode-sources: use Node $(tr -d '\r\n' < editor/.nvmrc) — e.g. source editor/use-node-toolchain.sh or (cd editor && nvm install && nvm use)"
echo "fetch-vscode-sources: sourcing get_repo.sh from editor/vscodium/ (cwd-sensitive; see BUILD.md)"

cd editor/vscodium

export VSCODE_QUALITY="${VSCODE_QUALITY:-stable}"
export VSCODE_LATEST="${VSCODE_LATEST:-no}"
export CI_BUILD="${CI_BUILD:-no}"

# Upstream get_repo.sh begins with [[ -z "${RELEASE_VERSION}" ]] before assigning; with bash -u,
# expanding unset RELEASE_VERSION aborts. Relax -u only for this source (matches dev/build.sh sourcing).
set +u
# shellcheck disable=SC1091
. ./get_repo.sh
set -u

echo "fetch-vscode-sources: done. Next: cd editor/vscodium && ./dev/build.sh — then LE_VIBE_EDITOR → VSCode-linux-*/bin/codium (editor/BUILD.md)."
