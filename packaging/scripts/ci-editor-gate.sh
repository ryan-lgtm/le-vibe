#!/usr/bin/env bash
# STEP 14 (H6): editor/ vendoring detection — matches .github/workflows/build-le-vibe-ide.yml
# (and build-linux.yml, which reuses that workflow) gate.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (same as ci-qa-hardening.md Local clone).
# Run from repo root: ./packaging/scripts/ci-editor-gate.sh
# Requires: bash on PATH (for bash -n and downstream packaging/scripts).
# Exits 0 when layout is none (skip). For layout=vscodium, runs bash syntax on upstream scripts (may exit 1).
# 14.d: default path does not validate Lé Vibe–visible IDE branding — editor/le-vibe-overrides/branding-staging.checklist.md;
#   docs/PRODUCT_SPEC.md §7.2. Fast gate only (same story as ./editor/smoke.sh). Optional release QA: set
#   LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 to fail when editor/vscodium/VSCode-linux-*/resources/app/product.json exists
#   but lacks Lé Vibe strings or linuxIconName != le-vibe, or vscodium linux le-vibe.svg is missing / not canonical
#   (sync-linux-icon-assets.sh --check). Same identity story as stage-le-vibe-ide-deb.sh; pair with
#   LEVIBE_STAGE_IDE_ASSERT_BRAND=1 for .deb.
# Authority: editor/VENDORING.md.
# H1 / §7.3: default CI uploads le-vibe-deb (stack le-vibe .deb only); this script does not build le-vibe-ide_*.deb —
#   maintainer — packaging/scripts/build-le-vibe-ide-deb.sh / build-le-vibe-debs.sh --with-ide (Full-product install on success — docs/PM_DEB_BUILD_ITERATION.md; docs/apt-repo-releases.md IDE package).
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

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/ci-editor-gate.sh

Run from the repository root (same entry as ./editor/smoke.sh). Detects editor layout
(flat / vscodium / none); when upstream is present, runs bash -n on IDE/packaging helper scripts.
Exits 0 when layout=none (no vendored IDE sources).

Environment:
  LEVIBE_EDITOR_GATE_ASSERT_BRAND   When 1, fail if VSCode-linux-*/resources/app/product.json
                                    exists but lacks Lé Vibe strings or linuxIconName is not le-vibe
                                    (§7.3 identity + hicolor icon key — docs/brand-assets.md). When a
                                    VSCode-linux-* tree exists, also requires
                                    editor/vscodium/src/stable/resources/linux/le-vibe.svg present and
                                    matching packaging canonical (sync-linux-icon-assets.sh --check).

See editor/VENDORING.md, editor/README.md, .github/workflows/build-le-vibe-ide.yml.
EOF
  exit 0
fi

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

if [[ "${layout}" == "vscodium" && "${LEVIBE_EDITOR_GATE_ASSERT_BRAND:-0}" == "1" ]]; then
  if ! command -v find >/dev/null 2>&1; then
    echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 requires find on PATH (findutils)." >&2
    exit 1
  fi
  _vs="$(find "${ROOT}/editor/vscodium" -maxdepth 1 -type d -name 'VSCode-linux-*' -print -quit 2>/dev/null || true)"
  if [[ -n "${_vs}" ]]; then
    _pj="${_vs}/resources/app/product.json"
    if [[ ! -f "${_pj}" ]]; then
      echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 — missing ${_pj} (incomplete VSCode-linux-* tree)." >&2
      exit 1
    fi
    if ! grep -q 'Lé Vibe' "${_pj}" 2>/dev/null; then
      echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 — ${_pj} has no Lé Vibe strings. Run packaging/scripts/ci-vscodium-linux-dev-build.sh before dev/build.sh (editor/BUILD.md *Linux icons*)." >&2
      exit 1
    fi
    if ! command -v python3 >/dev/null 2>&1; then
      echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 requires python3 on PATH (linuxIconName check)." >&2
      exit 1
    fi
    if ! python3 -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); sys.exit(0 if d.get('linuxIconName')=='le-vibe' else 1)" "${_pj}"; then
      echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 — ${_pj} must set linuxIconName to le-vibe (editor/le-vibe-overrides/product-branding-merge.json; docs/brand-assets.md)." >&2
      exit 1
    fi
    _vsc_linux_svg="${ROOT}/editor/vscodium/src/stable/resources/linux/le-vibe.svg"
    if [[ ! -f "${_vsc_linux_svg}" ]]; then
      echo "ci-editor-gate: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 — missing ${_vsc_linux_svg} — run editor/le-vibe-overrides/sync-linux-icon-assets.sh before dev/build.sh (docs/brand-assets.md; editor/BUILD.md *Linux icons*)." >&2
      exit 1
    fi
    if ! bash "${ROOT}/editor/le-vibe-overrides/sync-linux-icon-assets.sh" --check; then
      exit 1
    fi
  fi
fi

exit 0
