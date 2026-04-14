#!/usr/bin/env bash
# STEP 14: syntax-check VSCodium entrypoint scripts (no network, no compile).
# Requires: bash on PATH (for bash -n).
# Run from repo root. No-op if editor/vscodium is absent. Exits non-zero on bash -n failure.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (needed before this script runs meaningful checks).
# Called from ci-editor-gate.sh / ./editor/smoke.sh. E1: le-vibe/tests/test_product_spec_section8.py (PRODUCT_SPEC *Prioritization*).
# E1: editor/le-vibe-overrides/README.md — le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — fail-fast before ci-editor-nvmrc-sync / linux dev build (STEP 14 after STEP 0–1).
# Pytest: le-vibe/tests/test_ci_vscodium_bash_syntax_step14_contract.py (this script); verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/ci-vscodium-bash-syntax.sh

Run bash -n on core editor/vscodium/*.sh entrypoints (STEP 14 fail-fast gate).
No-op (exit 0) when editor/vscodium/ is absent. No network, no compile.

  -h, --help   Show this message and exit.
EOF
  exit 0
fi
if [[ $# -gt 0 ]]; then
  echo "ci-vscodium-bash-syntax: unexpected argument(s) — no args except --help (see --help)" >&2
  exit 2
fi

[[ -f editor/vscodium/product.json ]] || exit 0

if ! command -v bash >/dev/null 2>&1; then
  echo "ci-vscodium-bash-syntax: bash not on PATH — install bash (e.g. sudo apt install bash) (STEP 14 gate; editor/BUILD.md)." >&2
  exit 1
fi

# Core path toward a Linux build (upstream names; keep list short).
scripts=(
  build.sh
  build_cli.sh
  get_repo.sh
  prepare_src.sh
  prepare_vscode.sh
)

for f in "${scripts[@]}"; do
  p="editor/vscodium/${f}"
  [[ -f "$p" ]] || {
    echo "ci-vscodium-bash-syntax: missing ${p} — repair editor/vscodium (Fresh clone 14.b: git submodule update --init editor/vscodium — editor/README.md)." >&2
    exit 1
  }
  bash -n "$p"
  echo "ci-vscodium-bash-syntax: OK ${f}"
done
