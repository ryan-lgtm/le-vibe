#!/usr/bin/env bash
# Point Continue’s default config at Lé Vibe’s generated YAML (~/.config/le-vibe/continue-config.yaml).
# Workspace memory: Lé Vibe also seeds `.continue/rules/00-le-vibe-lvibe-memory.md` on `lvibe <dir>` (see le_vibe.continue_workspace).
# Safe to re-run; backs up an existing real file (not symlink) to config.yaml.bak once.
# Requires: mkdir, cp, ln, realpath, readlink on PATH (STEP 14.h).
# Product / trust: docs/PRODUCT_SPEC.md §5–§8 (`.lvibe/` + secrets); spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — STEP 7 H4 / 14.h Continue config symlink after STEP 0–1.
# Pytest: le-vibe/tests/test_continue_pin_bash_step14h_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

SRC="${LE_VIBE_CONTINUE_YAML:-${XDG_CONFIG_HOME:-$HOME/.config}/le-vibe/continue-config.yaml}"
DEST_ROOT="${XDG_CONFIG_HOME:-$HOME/.config}"
DEST_DIR="$DEST_ROOT/continue"
DEST="$DEST_DIR/config.yaml"

if [[ ! -f "$SRC" ]]; then
  echo "le-vibe: missing $SRC — complete first-run (launch le-vibe / lvibe) or run bootstrap with --le-vibe-product; generated config lives under ~/.config/le-vibe/ (see le-vibe/README.md; PRODUCT_SPEC §5–§8)." >&2
  exit 1
fi

if ! command -v mkdir >/dev/null 2>&1; then
  echo "sync-continue-config: mkdir not on PATH — install coreutils (e.g. sudo apt install coreutils) (STEP 14.h)." >&2
  exit 1
fi
if ! command -v cp >/dev/null 2>&1; then
  echo "sync-continue-config: cp not on PATH — install coreutils (e.g. sudo apt install coreutils) (STEP 14.h)." >&2
  exit 1
fi
if ! command -v ln >/dev/null 2>&1; then
  echo "sync-continue-config: ln not on PATH — install coreutils (e.g. sudo apt install coreutils) (STEP 14.h)." >&2
  exit 1
fi
if ! command -v realpath >/dev/null 2>&1; then
  echo "sync-continue-config: realpath not on PATH — install coreutils (e.g. sudo apt install coreutils) (STEP 14.h)." >&2
  exit 1
fi
if ! command -v readlink >/dev/null 2>&1; then
  echo "sync-continue-config: readlink not on PATH — install coreutils (e.g. sudo apt install coreutils) (STEP 14.h)." >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
if [[ -e "$DEST" && ! -L "$DEST" ]]; then
  echo "le-vibe: backing up existing $DEST to ${DEST}.bak" >&2
  cp -n "$DEST" "${DEST}.bak" || true
fi
ln -sfn "$(realpath "$SRC")" "$DEST"
echo "le-vibe: Continue reads $DEST -> $(readlink -f "$DEST" 2>/dev/null || readlink "$DEST")"
