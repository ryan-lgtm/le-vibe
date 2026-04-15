#!/usr/bin/env bash
# Install the Continue extension and the companion Red Hat YAML extension into VSCodium / Code - OSS (Open VSX).
# When reading pin files (default): requires grep, head, tr on PATH (same as verify-continue-pin.sh).
# Default pins: packaging/continue-openvsx-version (Continue) + packaging/vscode-yaml-openvsx-version (redhat.vscode-yaml; STEP 7 — docs/PM_STAGE_MAP.md).
# Run after the editor binary exists. Exits non-zero if either marketplace install fails when the editor binary exists.
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); H4: docs/continue-extension-pin.md; index: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — STEP 7 H4 / 14.h Continue install after STEP 0–1.
# Pytest: le-vibe/tests/test_install_continue_extension_script.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIN_DEFAULT="${SCRIPT_DIR}/../continue-openvsx-version"
PIN_FILE="${LE_VIBE_CONTINUE_PIN_FILE:-$PIN_DEFAULT}"
YAML_PIN_DEFAULT="${SCRIPT_DIR}/../vscode-yaml-openvsx-version"
YAML_PIN_FILE="${LE_VIBE_VSCODE_YAML_PIN_FILE:-$YAML_PIN_DEFAULT}"
# Match le_vibe.launcher _default_editor (14.g): prefer packaged Lé Vibe IDE before VSCodium.
if [[ -n "${LE_VIBE_EDITOR:-}" ]]; then
  BIN="${LE_VIBE_EDITOR}"
elif [[ -x /usr/lib/le-vibe/bin/codium ]]; then
  BIN="/usr/lib/le-vibe/bin/codium"
elif [[ -x /usr/bin/codium ]]; then
  BIN="/usr/bin/codium"
else
  BIN="codium"
fi
# Open VSX default: continue.continue — override if your marketplace uses another id.
EXT_ID="${LE_VIBE_CONTINUE_EXTENSION:-continue.continue}"
YAML_EXT_ID="${LE_VIBE_VSCODE_YAML_EXTENSION:-redhat.vscode-yaml}"

_read_pin_line() {
  # Args: path to pin file → prints first non-comment semver line or empty.
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo ""
    return 0
  fi
  if ! command -v grep >/dev/null 2>&1; then
    echo "install-continue-extension: grep not on PATH — install grep (e.g. sudo apt install grep) (docs/continue-extension-pin.md)." >&2
    exit 1
  fi
  if ! command -v head >/dev/null 2>&1; then
    echo "install-continue-extension: head not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/continue-extension-pin.md)." >&2
    exit 1
  fi
  if ! command -v tr >/dev/null 2>&1; then
    echo "install-continue-extension: tr not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/continue-extension-pin.md)." >&2
    exit 1
  fi
  grep -v '^[[:space:]]*#' "$f" | head -1 | tr -d '[:space:]\r'
}

# LE_VIBE_CONTINUE_OPENVSX_VERSION: unset → read pin file; "latest" or empty → no @version; else explicit semver.
if [[ -v LE_VIBE_CONTINUE_OPENVSX_VERSION ]]; then
  VER="${LE_VIBE_CONTINUE_OPENVSX_VERSION}"
else
  VER="$(_read_pin_line "$PIN_FILE")"
fi

REF="$EXT_ID"
if [[ -n "$VER" && "$VER" != "latest" ]]; then
  REF="${EXT_ID}@${VER}"
fi

# LE_VIBE_VSCODE_YAML_OPENVSX_VERSION: same semantics as Continue (unset → pin file).
if [[ -v LE_VIBE_VSCODE_YAML_OPENVSX_VERSION ]]; then
  YAML_VER="${LE_VIBE_VSCODE_YAML_OPENVSX_VERSION}"
else
  YAML_VER="$(_read_pin_line "$YAML_PIN_FILE")"
fi

YAML_REF="$YAML_EXT_ID"
if [[ -n "$YAML_VER" && "$YAML_VER" != "latest" ]]; then
  YAML_REF="${YAML_EXT_ID}@${YAML_VER}"
fi

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "le-vibe: no editor binary found (set LE_VIBE_EDITOR). Skipping extension installs (Continue + YAML)." >&2
  exit 0
fi

if ! "$BIN" --install-extension "$REF" "$@"; then
  echo "install-continue-extension: Continue extension install failed (continue.continue)." >&2
  exit 1
fi

if ! "$BIN" --install-extension "$YAML_REF"; then
  echo "install-continue-extension: YAML extension install failed (${YAML_EXT_ID})." >&2
  exit 1
fi
