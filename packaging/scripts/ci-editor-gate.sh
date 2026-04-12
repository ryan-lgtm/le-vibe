#!/usr/bin/env bash
# STEP 14 (H6): editor/ vendoring detection — matches .github/workflows/build-le-vibe-ide.yml gate.
# Run from repo root: ./packaging/scripts/ci-editor-gate.sh
# Exits 0 always (honest skip until editor/package.json exists). Authority: editor/VENDORING.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

layout=none
if [[ -f editor/package.json ]]; then
  layout=flat
elif [[ -f editor/vscodium/package.json ]]; then
  layout=submodule
fi

echo "ci-editor-gate: layout=${layout}"
if [[ "${layout}" == "none" ]]; then
  echo "ci-editor-gate: IDE sources not vendored — see editor/VENDORING.md (interim: LE_VIBE_EDITOR → VSCodium/codium)."
  exit 0
fi

echo "ci-editor-gate: upstream package.json present (${layout}) — wire Linux build in build-le-vibe-ide.yml when ready."
exit 0
