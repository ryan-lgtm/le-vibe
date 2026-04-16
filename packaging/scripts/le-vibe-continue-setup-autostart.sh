#!/usr/bin/env bash
# Roadmap G-A3: optional XDG autostart — one desktop notification when Continue wiring is still pending.
# Copy aligns with le_vibe.continue_setup_auto (next lvibe after first-run runs le-vibe-setup-continue when possible).
# Requires: mkdir, touch (coreutils) when a notification is shown; notify-send (libnotify) optional (skipped if absent).
# Idempotent: skips after ~/.continue/config.yaml is linked, or after one successful notify,
# or if the user disables via ~/.config/le-vibe/.continue-setup-autostart-disable.
# Product / trust: docs/PRODUCT_SPEC.md (first-run / Continue integration); spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — Roadmap G-A3 Continue autostart (first-run / Continue integration).
# Pytest: le-vibe/tests/test_continue_autostart_script.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

CONFIG_ROOT="${XDG_CONFIG_HOME:-$HOME/.config}"
LV_DIR="$CONFIG_ROOT/le-vibe"
SRC="${LE_VIBE_CONTINUE_YAML:-$LV_DIR/continue-config.yaml}"
MARK_DONE="$LV_DIR/.continue-setup-notify-done"
MARK_DISABLE="$LV_DIR/.continue-setup-autostart-disable"
CONTINUE_CFG="$CONFIG_ROOT/continue/config.yaml"

[[ -f "$MARK_DISABLE" ]] && exit 0

if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  exit 0
fi

[[ -f "$SRC" ]] || exit 0

if [[ -L "$CONTINUE_CFG" && -e "$CONTINUE_CFG" ]]; then
  exit 0
fi

[[ -f "$MARK_DONE" ]] && exit 0

if ! command -v notify-send >/dev/null 2>&1; then
  exit 0
fi

if ! command -v mkdir >/dev/null 2>&1; then
  echo "le-vibe-continue-setup-autostart: mkdir not on PATH — install coreutils (e.g. sudo apt install coreutils) (G-A3 autostart)." >&2
  exit 1
fi
if ! command -v touch >/dev/null 2>&1; then
  echo "le-vibe-continue-setup-autostart: touch not on PATH — install coreutils (e.g. sudo apt install coreutils) (G-A3 autostart)." >&2
  exit 1
fi

mkdir -p "$LV_DIR"
if notify-send \
  --app-name="Lé Vibe" \
  --urgency=normal \
  "Optional Continue wiring" \
  "Lé Vibe Chat is the default agent. Continue YAML sync still pending — run le-vibe-setup-continue or the next lvibe with LE_VIBE_AUTO_CONTINUE_SETUP=1."; then
  touch "$MARK_DONE"
fi
exit 0
