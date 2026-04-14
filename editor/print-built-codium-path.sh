#!/usr/bin/env bash
# STEP 14 (14.c): print absolute path to editor/vscodium/VSCode-linux-*/bin/codium if a local dev/build.sh output exists.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (required before product.json exists under editor/vscodium/).
# Run from repo root: ./editor/print-built-codium-path.sh
# Use: export LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)" && ./editor/smoke-lvibe-editor.sh
# For an unpacked CI tarball or any other tree, use ./editor/print-vsbuild-codium-path.sh [DIR] (14.f).
# No-op network; exits 1 if no match (build not run or different layout).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.c built codium path after STEP 0–1.
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: editor/print-built-codium-path.sh

Print absolute path to editor/vscodium/VSCode-linux-*/bin/codium after a local
dev/build.sh run (STEP 14.c — editor/BUILD.md).

Requires: git submodule editor/vscodium initialized (14.b — editor/README.md).

Partial tree (bin/codium missing): finish dev/build.sh (14.c), or obtain
linux_compile vscodium-linux-build.tar.gz — packaging/scripts/
print-github-linux-compile-artifact-hint.sh (browser Actions or gh);
packaging/scripts/trigger-le-vibe-ide-linux-compile.sh;
packaging/scripts/download-vscodium-linux-compile-artifact.sh --install; then
packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh — editor/BUILD.md 14.f.

For an unpacked CI tarball or other tree, use editor/print-vsbuild-codium-path.sh (see --help there).
EOF
  exit 0
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VSC="${ROOT}/editor/vscodium"

[[ -f "${VSC}/product.json" ]] || {
  echo "print-built-codium-path: expected editor/vscodium — run: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
  exit 1
}

exec "${ROOT}/editor/print-vsbuild-codium-path.sh" "$VSC"
