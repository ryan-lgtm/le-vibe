#!/usr/bin/env bash
# Roadmap H3: quick QA — pytest + .desktop validation. Run from repo root:
#   ./packaging/scripts/ci-smoke.sh
# Pytest step runs full le-vibe/tests/ (H8 STEP 12 anchors: test_issue_template_h8_contract.py — .github/ISSUE_TEMPLATE + config.yml).
# Full E1 contract roster (not only H8): root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI — same pointers as docs/ci-qa-hardening.md and docs/apt-repo-releases.md E1.
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); H-theme maintainer docs: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Optional RAG chunk: docs/rag/le-vibe-phase2-chunks.md (§14 table row; not pytest-gated) — SECURITY.md Related docs; same index as .github/workflows/ci.yml header.
# STEP 14 / H6: after pytest, ci-editor-gate.sh (same gate as ./editor/smoke.sh, build-le-vibe-ide.yml, build-linux.yml alias). E1: test_product_spec_section8.py — PRODUCT_SPEC *Prioritization*.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "ci-smoke: verify Continue Open VSX pin (H4)"
./packaging/scripts/verify-continue-pin.sh

echo "ci-smoke: packaging shell wrappers (bash -n)"
while IFS= read -r -d '' f; do
  bash -n "$f"
done < <(find packaging/bin -maxdepth 1 -type f -print0 2>/dev/null || true)

echo "ci-smoke: lvibe hygiene on synthetic workspace"
HYG_TMP="$(mktemp -d)"
trap 'rm -rf "${HYG_TMP}"' EXIT
export LVIBE_HYGIENE_TMP="${HYG_TMP}"
export PYTHONPATH="${ROOT}/le-vibe${PYTHONPATH:+:$PYTHONPATH}"
# §5 consent: synthetic dir only — mirror pytest default (le-vibe/tests/conftest.py) so
# ensure_lvibe_workspace matches automation intent if consent checks expand.
LE_VIBE_LVIBE_CONSENT=accept python3 -c "
import os, sys
from pathlib import Path
from le_vibe.workspace_hub import ensure_lvibe_workspace
from le_vibe.hygiene import check_lvibe_workspace
root = Path(os.environ['LVIBE_HYGIENE_TMP'])
ensure_lvibe_workspace(root)
errs, warns = check_lvibe_workspace(root)
for w in warns:
    print('warning:', w, file=sys.stderr)
if errs:
    for e in errs:
        print('error:', e, file=sys.stderr)
    sys.exit(1)
"
unset LVIBE_HYGIENE_TMP

echo "ci-smoke: pytest (le-vibe)"
cd le-vibe
python3 -m pip install -q -r requirements.txt pytest
python3 -m pytest tests/ -q
cd "$ROOT"

echo "ci-smoke: editor vendoring gate (STEP 14)"
./packaging/scripts/ci-editor-gate.sh

if command -v desktop-file-validate >/dev/null 2>&1; then
  echo "ci-smoke: desktop-file-validate"
  desktop-file-validate packaging/applications/le-vibe.desktop
  desktop-file-validate packaging/autostart/le-vibe-continue-setup.desktop
elif [[ -n "${GITHUB_ACTIONS:-}" ]]; then
  echo "ci-smoke: desktop-file-validate not found; install desktop-file-utils" >&2
  exit 1
else
  echo "ci-smoke: skipping desktop-file-validate (install desktop-file-utils for full checks)" >&2
fi

echo "ci-smoke: OK"
