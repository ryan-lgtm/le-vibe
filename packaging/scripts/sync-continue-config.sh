#!/usr/bin/env bash
# Point Continue’s default config at Lé Vibe’s generated YAML (~/.config/le-vibe/continue-config.yaml).
# Workspace memory: Lé Vibe also seeds `.continue/rules/00-le-vibe-lvibe-memory.md` on `lvibe <dir>` (see le_vibe.continue_workspace).
# Safe to re-run; backs up an existing real file (not symlink) to config.yaml.bak once.
# Product / trust: docs/PRODUCT_SPEC.md §5–§8 (`.lvibe/` + secrets); spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
set -euo pipefail

SRC="${LE_VIBE_CONTINUE_YAML:-${XDG_CONFIG_HOME:-$HOME/.config}/le-vibe/continue-config.yaml}"
DEST_ROOT="${XDG_CONFIG_HOME:-$HOME/.config}"
DEST_DIR="$DEST_ROOT/continue"
DEST="$DEST_DIR/config.yaml"

if [[ ! -f "$SRC" ]]; then
  echo "le-vibe: missing $SRC — complete first-run (launch le-vibe) or run bootstrap with --le-vibe-product (see README)." >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
if [[ -e "$DEST" && ! -L "$DEST" ]]; then
  echo "le-vibe: backing up existing $DEST to ${DEST}.bak" >&2
  cp -n "$DEST" "${DEST}.bak" || true
fi
ln -sfn "$(realpath "$SRC")" "$DEST"
echo "le-vibe: Continue reads $DEST -> $(readlink -f "$DEST" 2>/dev/null || readlink "$DEST")"
