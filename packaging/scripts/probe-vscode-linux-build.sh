#!/usr/bin/env bash
# STEP 14 / §7.3: print VSCode-linux tree state for the monorepo (14.c).
# Same values as lvibe ide-prereqs --json / verify-step14-closeout.sh --json (vscode_linux_build).
# Used by preflight-step14-closeout.sh, verify-step14-closeout.sh, manual-step14-install-smoke.sh.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/probe-vscode-linux-build.sh [REPO_ROOT]

Print one line to stdout: ready | partial | absent | unknown

  ready    — editor/vscodium/VSCode-linux-*/bin/codium exists
  partial  — VSCode-linux-* exists but bin/codium missing
  absent   — no usable tree
  unknown  — Python probe failed

Same classifier as le_vibe.ide_packaging_paths.vscode_linux_build_status().
EOF
  exit 0
fi

ROOT="${1:-$DEFAULT_ROOT}"
REPO_ROOT="$ROOT" PYTHONPATH="$ROOT/le-vibe" python3 -c '
import os
from pathlib import Path
from le_vibe.ide_packaging_paths import vscode_linux_build_status
st, _ = vscode_linux_build_status(Path(os.environ["REPO_ROOT"]))
print(st)
' 2>/dev/null || echo "unknown"
