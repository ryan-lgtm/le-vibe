#!/usr/bin/env bash
# STEP 14: print comma-separated filenames in editor/vscodium/VSCode-linux-*/bin when
# vscode_linux_build is partial (same inventory as lvibe ide-prereqs --json vscode_linux_bin_files).
# Used by preflight-step14-closeout.sh and verify-step14-closeout.sh — keep logic in one place.
# Exits 0; prints nothing when not partial or Python probe fails (caller probes first).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/print-step14-vscode-linux-bin-files.sh [REPO_ROOT]

Print comma-separated filenames under editor/vscodium/VSCode-linux-*/bin when
vscode_linux_build is partial — same list as:
  lvibe ide-prereqs --json  →  field "vscode_linux_bin_files"

Prints nothing (stdout) when the tree is not partial, absent, or the Python
probe fails. Classifier: packaging/scripts/probe-vscode-linux-build.sh

See: editor/BUILD.md (*Partial tree*, 14.c / 14.f), docs/PM_DEB_BUILD_ITERATION.md
(*Partial VSCode-linux tree*). Obtain CI tarball: packaging/scripts/
print-github-linux-compile-artifact-hint.sh; maintainer:
packaging/scripts/trigger-le-vibe-ide-linux-compile.sh;
packaging/scripts/download-vscodium-linux-compile-artifact.sh --install. Recovery without
recompiling: packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh (linux_compile artifact).
EOF
  exit 0
fi

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
