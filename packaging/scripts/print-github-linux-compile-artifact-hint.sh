#!/usr/bin/env bash
# STEP 14.e / 14.f — offline hint: fetch linux_compile **vscodium-linux-build.tar.gz** from GitHub Actions.
# Does not call the network; print copy/paste commands only. Authority: editor/BUILD.md (*14.f*),
# .github/workflows/build-le-vibe-ide.yml (job linux_compile, upload-artifact).
# E1: le-vibe/tests/test_packaging_step14_help_smoke.py; packaging/scripts/ci-editor-gate.sh (bash -n).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: packaging/scripts/print-github-linux-compile-artifact-hint.sh

Print copy/paste commands to download **vscodium-linux-build.tar.gz** from CI job **linux_compile**
(workflow **build-le-vibe-ide.yml**). Artifact upload name: **le-vibe-vscodium-linux-<run_id>**
(same **run_id** appears in the GitHub Actions URL and in that artifact name).

You do **not** need the GitHub CLI: use the **Actions** tab in the browser (see body output) **or** **gh**
below. You need a **successful** **linux_compile** run (manual **workflow_dispatch** with
**vscodium_linux_compile**, **workflow_call** with that input, or push tag **ide-v***).

After download, GitHub may deliver a **.zip** wrapper — unzip to reach **vscodium-linux-build.tar.gz**,
then vendor it:

  packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes

  -h, --help   Show this message and exit.

See editor/BUILD.md (*GitHub Actions artifact vscodium-linux-build.tar.gz*), docs/PM_DEB_BUILD_ITERATION.md.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -gt 0 ]]; then
  echo "${0##*/}: unexpected argument(s) — use --help" >&2
  exit 2
fi

echo "# === CI tarball — build-le-vibe-ide.yml job linux_compile (14.e) → 14.f ==="
echo "# Artifact contains: vscodium-linux-build.tar.gz (VSCode-linux-* tree)."
echo "#"
echo "# --- A) Browser (no gh): repository → Actions → workflow \"build-le-vibe-ide\" →"
echo "#    open a run where job \"linux_compile\" succeeded → Artifacts → download"
echo "#    \"le-vibe-vscodium-linux-<run_id>\" (.zip) → unzip → vscodium-linux-build.tar.gz"
echo "#"
echo "# --- B) GitHub CLI (optional) ---"
echo "# 1) List recent runs (pick a run_id where job linux_compile succeeded):"
echo "#    gh run list -w build-le-vibe-ide.yml -L 15"
echo "#"
echo "# 2) Download (replace RUN_ID twice — same number in -n and in the artifact name):"
echo "#    gh run download RUN_ID -n le-vibe-vscodium-linux-RUN_ID -D /tmp/lv-vscodium-art"
echo "#"
echo "# --- Install tarball into editor/vscodium/ (after A or B) ---"
echo "#    packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes"
echo "#"
echo "# --- Confirm ---"
echo "#    ./packaging/scripts/probe-vscode-linux-build.sh"
