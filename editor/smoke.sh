#!/usr/bin/env bash
# Lé Vibe IDE — local smoke (STEP 14). Same checks as build-le-vibe-ide.yml gate + bash -n + .nvmrc sync.
# Run from repository root:
#   ./editor/smoke.sh
# Authority: editor/README.md, packaging/scripts/ci-editor-gate.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${ROOT}/packaging/scripts/ci-editor-gate.sh"
