#!/usr/bin/env bash
# §7.3 maintainer bundle (STEP 14): same gate as ./editor/smoke.sh, then lvibe ide-prereqs --json sanity.
# Does not build Electron or .deb — use packaging/scripts/build-le-vibe-debs.sh --with-ide for full-product artifacts.
# Run from repository root:
#   ./editor/verify-73-maintainer.sh
# Strict §7.3 identity (product.json + linuxIconName + sync-linux-icon-assets --check):
#   LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 ./editor/verify-73-maintainer.sh
# Authority: docs/PRODUCT_SPEC.md §7.3, editor/BUILD.md, packaging/scripts/ci-editor-gate.sh
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 maintainer gate after STEP 0–1.
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/le-vibe"

usage() {
  cat <<'EOF'
Usage: editor/verify-73-maintainer.sh

Run packaging/scripts/ci-editor-gate.sh then lvibe ide-prereqs --json checks
(STEP 14 / §7.3 maintainer gate — does not build Electron or .deb).
After stack + IDE .deb artifacts exist: packaging/scripts/preflight-step14-closeout.sh --require-stack-deb;
packaging/scripts/verify-step14-closeout.sh --require-stack-deb (see docs/PM_DEB_BUILD_ITERATION.md).

Environment:
  LEVIBE_EDITOR_GATE_ASSERT_BRAND=1   Strict §7.3 branding (same as ci-editor-gate). That path runs
                                     packaging/scripts/ci-editor-gate.sh, which may invoke
                                     sync-linux-icon-assets.sh --check — needs cmp, sed, mktemp on PATH
                                     (editor/BUILD.md *Linux icons*, docs/brand-assets.md).

  -h, --help   Show this message and exit.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -gt 0 ]]; then
  echo "verify-73-maintainer: unexpected argument(s) — run with no args (see --help)" >&2
  exit 2
fi

if [[ "${LEVIBE_EDITOR_GATE_ASSERT_BRAND:-0}" == "1" ]]; then
  LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 "${ROOT}/packaging/scripts/ci-editor-gate.sh"
else
  "${ROOT}/packaging/scripts/ci-editor-gate.sh"
fi

python3 -m le_vibe.launcher ide-prereqs --json | python3 -c "import json,sys;d=json.load(sys.stdin);assert d.get('static_prereq_files_ok')is True,d;assert'vscodium_linux_svg_staged'in d"
echo "verify-73-maintainer: OK (gate + ide-prereqs --json)"
