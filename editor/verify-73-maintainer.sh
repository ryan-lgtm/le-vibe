#!/usr/bin/env bash
# §7.3 maintainer bundle (STEP 14): same gate as ./editor/smoke.sh, then lvibe ide-prereqs --json sanity.
# Does not build Electron or .deb — use packaging/scripts/build-le-vibe-debs.sh --with-ide for full-product artifacts.
# Run from repository root:
#   ./editor/verify-73-maintainer.sh
# Strict §7.3 identity (product.json + linuxIconName + sync-linux-icon-assets --check):
#   LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 ./editor/verify-73-maintainer.sh
# Authority: docs/PRODUCT_SPEC.md §7.3, editor/BUILD.md, packaging/scripts/ci-editor-gate.sh
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 maintainer gate after STEP 0–1.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/le-vibe"

if [[ "${LEVIBE_EDITOR_GATE_ASSERT_BRAND:-0}" == "1" ]]; then
  LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 "${ROOT}/packaging/scripts/ci-editor-gate.sh"
else
  "${ROOT}/packaging/scripts/ci-editor-gate.sh"
fi

python3 -m le_vibe.launcher ide-prereqs --json | python3 -c "import json,sys;d=json.load(sys.stdin);assert d.get('static_prereq_files_ok')is True,d;assert'vscodium_linux_svg_staged'in d"
echo "verify-73-maintainer: OK (gate + ide-prereqs --json)"
