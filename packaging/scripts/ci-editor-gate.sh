#!/usr/bin/env bash
# STEP 14 (H6): editor/ vendoring detection — matches .github/workflows/build-le-vibe-ide.yml
# (and build-linux.yml, which reuses that workflow) gate.
# Run from repo root: ./packaging/scripts/ci-editor-gate.sh
# Exits 0 when layout is none (skip). For layout=vscodium, runs bash syntax on upstream scripts (may exit 1).
# Authority: editor/VENDORING.md.
# E1: docs/PRODUCT_SPEC.md *Prioritization* documents ./editor/smoke.sh (this gate) — le-vibe/tests/test_product_spec_section8.py.
# E1: editor/le-vibe-overrides/README.md — le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py.
# build-le-vibe-ide.yml (build-linux alias) uploads ide-ci-metadata.txt (le_vibe_editor_docs=editor/README.md);
#   upload-artifact retention-days; permissions contents read + actions write — test_build_le_vibe_ide_workflow_contract.py;
#   GitHub Actions run Summary — Pre-binary artifact line (LE_VIBE_EDITOR pointer) — same test.
# 14.c: bash -n editor/smoke-lvibe-editor.sh (launcher ↔ LE_VIBE_EDITOR smoke; see editor/BUILD.md).
# VSCodium’s repo uses product.json + get_repo.sh (no root package.json until vscode is fetched).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

layout=none
if [[ -f editor/package.json ]]; then
  layout=flat
elif [[ -f editor/vscodium/product.json ]]; then
  layout=vscodium
fi

echo "ci-editor-gate: layout=${layout}"
if [[ "${layout}" == "none" ]]; then
  echo "ci-editor-gate: IDE sources not vendored — see editor/VENDORING.md (interim: LE_VIBE_EDITOR → VSCodium/codium)."
  exit 0
fi

echo "ci-editor-gate: upstream present (${layout}) — wire Linux build in build-le-vibe-ide.yml (build-linux alias) when ready."
bash -n "${ROOT}/editor/smoke-lvibe-editor.sh"
if [[ "${layout}" == "vscodium" ]]; then
  "${ROOT}/packaging/scripts/ci-vscodium-bash-syntax.sh"
  "${ROOT}/packaging/scripts/ci-editor-nvmrc-sync.sh"
  bash -n "${ROOT}/editor/fetch-vscode-sources.sh"
  bash -n "${ROOT}/editor/print-built-codium-path.sh"
  bash -n "${ROOT}/editor/print-vsbuild-codium-path.sh"
  bash -n "${ROOT}/packaging/scripts/ci-vscodium-linux-dev-build.sh"
fi
exit 0
