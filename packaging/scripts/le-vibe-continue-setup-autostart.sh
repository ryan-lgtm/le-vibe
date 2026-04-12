#!/usr/bin/env bash
# Roadmap G-A3: optional XDG autostart — one desktop notification to run Continue setup.
# Idempotent: skips after ~/.continue/config.yaml is linked, or after one successful notify,
# or if the user disables via ~/.config/le-vibe/.continue-setup-autostart-disable.
# Product / trust: docs/PRODUCT_SPEC.md (first-run / Continue integration); spec-phase2.md §14 (H6/H7 vs in-tree); docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
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

mkdir -p "$LV_DIR"
if notify-send \
  --app-name="Lé Vibe" \
  --urgency=normal \
  "Continue setup" \
  "Wire the Continue extension: run le-vibe-setup-continue in a terminal (add --gui for a Zenity dialog)."; then
  touch "$MARK_DONE"
fi
exit 0
