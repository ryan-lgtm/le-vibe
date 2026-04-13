#!/usr/bin/env bash
# STEP 14: ensure editor/.nvmrc matches editor/vscodium/.nvmrc (Node pin parity).
# Requires: cmp (coreutils). No-op if VSCodium tree is absent. Run from repo root.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (needed for editor/vscodium/.nvmrc).
# Called from ci-editor-gate.sh / ./editor/smoke.sh. E1: le-vibe/tests/test_product_spec_section8.py (PRODUCT_SPEC *Prioritization*).
# E1: editor/le-vibe-overrides/README.md — le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.a pin parity before ci-vscodium-linux-dev-build (STEP 14 after STEP 0–1).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

[[ -f editor/vscodium/product.json ]] || exit 0

[[ -f editor/.nvmrc && -f editor/vscodium/.nvmrc ]] || {
  echo "ci-editor-nvmrc-sync: expected editor/.nvmrc and editor/vscodium/.nvmrc — if editor/vscodium/.nvmrc is missing: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
  exit 1
}

if ! command -v cmp >/dev/null 2>&1; then
  echo "ci-editor-nvmrc-sync: cmp not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.a)." >&2
  exit 1
fi

if ! cmp -s editor/.nvmrc editor/vscodium/.nvmrc; then
  echo "ci-editor-nvmrc-sync: editor/.nvmrc differs from editor/vscodium/.nvmrc — update editor/.nvmrc to match upstream pin after a vendor bump (14.a); see editor/README.md." >&2
  exit 1
fi

echo "ci-editor-nvmrc-sync: OK"
