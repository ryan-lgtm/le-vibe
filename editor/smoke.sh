#!/usr/bin/env bash
# Lé Vibe IDE — local smoke (STEP 14). Same checks as build-le-vibe-ide.yml / build-linux.yml (alias) gate + bash -n + .nvmrc sync.
# 14.d: does not validate Lé Vibe–visible IDE branding — editor/le-vibe-overrides/branding-staging.checklist.md;
#   docs/PRODUCT_SPEC.md §7.2 (delegates to ci-editor-gate.sh — same fast gate).
# Run from repository root:
#   ./editor/smoke.sh
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (when editor/vscodium/ is empty).
# Authority: editor/README.md, packaging/scripts/ci-editor-gate.sh
# H1 / §7.3: ci.yml le-vibe-deb is the stack .deb only; this smoke does not produce le-vibe-ide_*.deb — docs/apt-repo-releases.md (IDE package); build-le-vibe-debs.sh --with-ide.
# E1: docs/PRODUCT_SPEC.md *Prioritization* documents this path — le-vibe/tests/test_product_spec_section8.py
# (same module locks ide-ci-metadata / retention-days / permissions (contents read, actions write) / Pre-binary / editor/BUILD+VENDORING in PRODUCT_SPEC *Prioritization*).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${ROOT}/packaging/scripts/ci-editor-gate.sh"
