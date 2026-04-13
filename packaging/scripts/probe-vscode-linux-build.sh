#!/usr/bin/env bash
# STEP 14 / §7.3: print VSCode-linux tree state for the monorepo (14.c).
# Same values as lvibe ide-prereqs --json / verify-step14-closeout.sh --json (vscode_linux_build).
# Used by preflight-step14-closeout.sh, verify-step14-closeout.sh, manual-step14-install-smoke.sh,
# build-le-vibe-debs.sh (--with-ide probe). Pair with print-step14-vscode-linux-bin-files.sh when partial.
#
# Default stdout is a single word (ready|partial|absent|unknown) for scripts that parse it.
# Use --progress for a weighted % toward bin/codium; use --json for machine-readable milestones.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PY="${SCRIPT_DIR}/probe_vscode_linux_build.py"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/probe-vscode-linux-build.sh [REPO_ROOT]
       packaging/scripts/probe-vscode-linux-build.sh [--progress|--json] [REPO_ROOT]

Print default stdout: one line — ready | partial | absent | unknown

  ready    — editor/vscodium/VSCode-linux-*/bin/codium exists
  partial  — VSCode-linux-* exists but bin/codium missing
  absent   — no usable tree
  unknown  — Python probe failed

  --progress  Print milestone checklist + compile_gate_pct (0–100) toward bin/codium.
              This is the Linux compile / tarball slice only — not .deb builds; see
              preflight-step14-closeout.sh for a fuller gap list.
  --json      Print JSON (vscode_linux_build, compile_gate_pct, milestones, paths).

When partial: packaging/scripts/print-step14-vscode-linux-bin-files.sh [REPO_ROOT]
prints bin/ filenames (same as lvibe ide-prereqs --json field vscode_linux_bin_files).

Same classifier as le_vibe.ide_packaging_paths.vscode_linux_build_status().
EOF
  exit 0
fi

ROOT="$DEFAULT_ROOT"
EXTRA=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --progress|--json)
      EXTRA+=("$1")
      shift
      ;;
    *)
      ROOT="$1"
      shift
      ;;
  esac
done

export REPO_ROOT="$ROOT"
cd "$ROOT"
if [[ ${#EXTRA[@]} -gt 0 ]]; then
  REPO_ROOT="$ROOT" PYTHONPATH="${ROOT}/le-vibe" python3 "$PY" "${EXTRA[@]}" "$ROOT" 2>/dev/null || {
    echo "unknown"
    exit 0
  }
else
  REPO_ROOT="$ROOT" PYTHONPATH="${ROOT}/le-vibe" python3 "$PY" "$ROOT" 2>/dev/null || echo "unknown"
fi
