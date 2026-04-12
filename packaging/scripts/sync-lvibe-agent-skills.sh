#!/usr/bin/env bash
# STEP 3 (E2): Copy missing Lé Vibe agent templates into .lvibe/agents/<id>/skill.md.
# Run from a workspace root after pulling the monorepo — idempotent (skips existing skill.md).
# Continue rules (le_vibe.continue_workspace) point Chat/Agent at .lvibe/; this refreshes skills only.
# Authority: docs/SESSION_ORCHESTRATION_SPEC.md; docs/PRODUCT_SPEC.md §5–§8.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WS="${1:-.}"
export PYTHONPATH="${ROOT}/le-vibe${PYTHONPATH:+:$PYTHONPATH}"
export LVIBE_WORKSPACE_ROOT="$(cd "$WS" && pwd)"
python3 - <<'PY'
from pathlib import Path
import os
import sys

from le_vibe.session_orchestrator import sync_agent_skills_from_templates

root = Path(os.environ["LVIBE_WORKSPACE_ROOT"])
lv = root / ".lvibe"
if not lv.is_dir():
    print(f"sync-lvibe-agent-skills: missing {lv} — run lvibe . on this workspace first.", file=sys.stderr)
    sys.exit(1)
written = sync_agent_skills_from_templates(lv)
if written:
    print(f"sync-lvibe-agent-skills: wrote {len(written)} skill.md file(s)")
    for p in written:
        print(f"  {p}")
else:
    print("sync-lvibe-agent-skills: no missing skill.md (delete a file under .lvibe/agents/*/ to force re-copy)")
PY
