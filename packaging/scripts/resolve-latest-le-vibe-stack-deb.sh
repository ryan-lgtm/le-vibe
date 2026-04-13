#!/usr/bin/env bash
# Single source of truth: newest le-vibe_*.deb beside the monorepo ($ROOT/..) or under $ROOT.
# Used by packaging/scripts/verify-step14-closeout.sh (--require-stack-deb),
# packaging/scripts/manual-step14-install-smoke.sh (default STACK_DEB),
# packaging/scripts/build-le-vibe-debs.sh (find_stack_deb).
# Authority: docs/PM_DEB_BUILD_ITERATION.md *Output paths (from repo root)*.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/resolve-latest-le-vibe-stack-deb.sh [--help] [ROOT]

Print the absolute path of the newest matching le-vibe_*.deb found:
  - beside the clone: $ROOT/../le-vibe_*.deb
  - or under the repo root: $ROOT/le-vibe_*.deb

If none exist, prints nothing (stdout empty) and exits 0.

ROOT defaults to the monorepo root (two levels above this script).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

ROOT="${1:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

shopt -s nullglob
cands=("$ROOT"/../le-vibe_*.deb "$ROOT"/le-vibe_*.deb)
shopt -u nullglob
if [[ ${#cands[@]} -eq 0 ]]; then
  exit 0
fi
printf '%s\n' "${cands[@]}" | sort -V | tail -n1
