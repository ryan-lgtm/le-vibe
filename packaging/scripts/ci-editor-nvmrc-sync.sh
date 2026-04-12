#!/usr/bin/env bash
# STEP 14: ensure editor/.nvmrc matches editor/vscodium/.nvmrc (Node pin parity).
# No-op if VSCodium tree is absent. Run from repo root.
# Called from ci-editor-gate.sh / ./editor/smoke.sh. E1: le-vibe/tests/test_product_spec_section8.py (PRODUCT_SPEC *Prioritization*).
# E1: editor/le-vibe-overrides/README.md — le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

[[ -f editor/vscodium/product.json ]] || exit 0

[[ -f editor/.nvmrc && -f editor/vscodium/.nvmrc ]] || {
  echo "ci-editor-nvmrc-sync: expected editor/.nvmrc and editor/vscodium/.nvmrc" >&2
  exit 1
}

if ! cmp -s editor/.nvmrc editor/vscodium/.nvmrc; then
  echo "ci-editor-nvmrc-sync: editor/.nvmrc must match editor/vscodium/.nvmrc (see editor/README.md)" >&2
  exit 1
fi

echo "ci-editor-nvmrc-sync: OK"
