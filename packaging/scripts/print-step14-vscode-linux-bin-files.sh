#!/usr/bin/env bash
# STEP 14: print comma-separated filenames in editor/vscodium/VSCode-linux-*/bin when
# vscode_linux_build is partial (same inventory as lvibe ide-prereqs --json vscode_linux_bin_files).
# Used by preflight-step14-closeout.sh and verify-step14-closeout.sh — keep logic in one place.
# Exits 0; prints nothing when not partial or Python probe fails (caller probes first).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ROOT="${1:-$DEFAULT_ROOT}"

REPO_ROOT="$ROOT" PYTHONPATH="$ROOT/le-vibe" python3 -c '
import os
from pathlib import Path
from le_vibe.ide_packaging_paths import vscode_linux_build_status, vscode_linux_bin_filenames

root = Path(os.environ["REPO_ROOT"])
st, vs = vscode_linux_build_status(root)
if st != "partial" or vs is None:
    raise SystemExit(0)
names = vscode_linux_bin_filenames(vs) or []
print(", ".join(names))
' 2>/dev/null || true
