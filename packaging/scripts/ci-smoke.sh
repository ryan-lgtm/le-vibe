#!/usr/bin/env bash
# Roadmap H3 / STEP 10 (docs/PM_STAGE_MAP.md): quick QA — pytest + .desktop validation. Run from repo root:
#   ./packaging/scripts/ci-smoke.sh
# Pytest step runs full le-vibe/tests/ (H8 STEP 12 anchors: test_issue_template_h8_contract.py — .github/ISSUE_TEMPLATE + config.yml).
# Full E1 contract roster (not only H8): root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI — same pointers as docs/ci-qa-hardening.md and docs/apt-repo-releases.md E1.
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); H-theme maintainer docs: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Optional RAG chunk: docs/rag/le-vibe-phase2-chunks.md (§14 table row; not pytest-gated) — SECURITY.md Related docs; same index as .github/workflows/ci.yml header.
# STEP 14 / H6: after pytest, ci-editor-gate.sh (same gate as ./editor/smoke.sh, build-le-vibe-ide.yml, build-linux.yml alias). E1: test_product_spec_section8.py — PRODUCT_SPEC *Prioritization* (ide-ci-metadata.txt, retention-days, Pre-binary artifact, editor/BUILD.md, editor/VENDORING.md); test_build_le_vibe_ide_workflow_contract.py — ide-ci-metadata + retention-days + permissions (contents read, actions write) + Summary; test_le_vibe_readme_e1_contract.py — le-vibe/README vs root E1.
# H1 — parent ci.yml job uploads artifact le-vibe-deb (stack le-vibe .deb + SBOM + SHA256SUMS only; not le-vibe-ide — STEP 14 / §7.3; maintainer full product: build-le-vibe-debs.sh --with-ide prints Full-product install — docs/PM_DEB_BUILD_ITERATION.md; docs/apt-repo-releases.md IDE package; docs/PM_STAGE_MAP.md H1 vs §7.3 .deb bundles).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — this script is STEP 10 (H3) then ci-editor-gate.sh (STEP 14 smoke).
# Fresh clone (14.b): git submodule update --init editor/vscodium when editor/vscodium/ is empty — editor/README.md; docs/ci-qa-hardening.md *Local clone (14.b)*.
# Requires: find (findutils), mktemp (coreutils), python3 on PATH.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if ! command -v find >/dev/null 2>&1; then
  echo "ci-smoke: find not on PATH — install findutils (e.g. sudo apt install findutils) (docs/ci-qa-hardening.md)." >&2
  exit 1
fi
if ! command -v mktemp >/dev/null 2>&1; then
  echo "ci-smoke: mktemp not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/ci-qa-hardening.md)." >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "ci-smoke: python3 not on PATH — install Python 3 (docs/ci-qa-hardening.md)." >&2
  exit 1
fi

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
  # §7.3 IDE .deb — same Freedesktop QA as stack launcher (STEP 14 / packaging/debian-le-vibe-ide)
  desktop-file-validate packaging/debian-le-vibe-ide/debian/le-vibe.desktop
elif [[ -n "${GITHUB_ACTIONS:-}" ]]; then
  echo "ci-smoke: desktop-file-validate not found; install desktop-file-utils" >&2
  exit 1
else
  echo "ci-smoke: skipping desktop-file-validate (install desktop-file-utils for full checks)" >&2
fi

echo "ci-smoke: OK"
