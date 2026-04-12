#!/usr/bin/env bash
# STEP 14 (H6): editor/ vendoring detection — matches .github/workflows/build-le-vibe-ide.yml
# (and build-linux.yml, which reuses that workflow) gate.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (same as ci-qa-hardening.md Local clone).
# Run from repo root: ./packaging/scripts/ci-editor-gate.sh
# Requires: bash on PATH (for bash -n and downstream packaging/scripts).
# Exits 0 when layout is none (skip). For layout=vscodium, runs bash syntax on upstream scripts (may exit 1).
# 14.d: does not validate Lé Vibe–visible IDE branding — editor/le-vibe-overrides/branding-staging.checklist.md;
#   docs/PRODUCT_SPEC.md §7.2. Fast gate only (same story as ./editor/smoke.sh).
# Authority: editor/VENDORING.md.
# H1 / §7.3: default CI uploads le-vibe-deb (stack le-vibe .deb only); this script does not build le-vibe-ide_*.deb —
#   maintainer — packaging/scripts/build-le-vibe-ide-deb.sh / build-le-vibe-debs.sh --with-ide (docs/apt-repo-releases.md IDE package).
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
  echo "ci-editor-gate: IDE sources not vendored — try: git submodule update --init editor/vscodium (editor/README.md Fresh clone 14.b); else see editor/VENDORING.md (interim: LE_VIBE_EDITOR → VSCodium/codium)."
  exit 0
fi

if ! command -v bash >/dev/null 2>&1; then
  echo "ci-editor-gate: bash not on PATH — install bash (e.g. sudo apt install bash) (STEP 14 gate)." >&2
  exit 1
fi

echo "ci-editor-gate: upstream present (${layout}) — wire Linux build in build-le-vibe-ide.yml (build-linux alias) when ready."
bash -n "${ROOT}/editor/smoke-lvibe-editor.sh"
if [[ "${layout}" == "vscodium" ]]; then
  "${ROOT}/packaging/scripts/ci-vscodium-bash-syntax.sh"
  "${ROOT}/packaging/scripts/ci-editor-nvmrc-sync.sh"
  bash -n "${ROOT}/editor/use-node-toolchain.sh"
  bash -n "${ROOT}/editor/fetch-vscode-sources.sh"
  bash -n "${ROOT}/editor/print-built-codium-path.sh"
  bash -n "${ROOT}/editor/verify-14c-local-binary.sh"
  bash -n "${ROOT}/editor/smoke-built-codium-lvibe.sh"
  bash -n "${ROOT}/editor/print-vsbuild-codium-path.sh"
  bash -n "${ROOT}/editor/print-ci-tarball-codium-path.sh"
  bash -n "${ROOT}/packaging/scripts/ci-vscodium-linux-dev-build.sh"
fi
exit 0
