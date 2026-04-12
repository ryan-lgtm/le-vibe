#!/usr/bin/env bash
# Lé Vibe IDE — local smoke (STEP 14). Same checks as build-le-vibe-ide.yml / build-linux.yml (alias) gate + bash -n + .nvmrc sync.
# Run from repository root:
#   ./editor/smoke.sh
# Authority: editor/README.md, packaging/scripts/ci-editor-gate.sh
# E1: docs/PRODUCT_SPEC.md *Prioritization* documents this path — le-vibe/tests/test_product_spec_section8.py
# (same module locks ide-ci-metadata / retention-days / Pre-binary / editor/BUILD+VENDORING in PRODUCT_SPEC *Prioritization*).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${ROOT}/packaging/scripts/ci-editor-gate.sh"
