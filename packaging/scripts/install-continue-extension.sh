#!/usr/bin/env bash
# Install the Continue extension into VSCodium / Code - OSS (Open VSX identifier).
# Default: pinned Open VSX version from packaging/continue-openvsx-version (Roadmap H4).
# Run after the editor binary exists. Non-fatal if marketplace is unreachable.
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); H4: docs/continue-extension-pin.md; index: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIN_DEFAULT="${SCRIPT_DIR}/../continue-openvsx-version"
PIN_FILE="${LE_VIBE_CONTINUE_PIN_FILE:-$PIN_DEFAULT}"
BIN="${LE_VIBE_EDITOR:-codium}"
# Open VSX default: continue.continue — override if your marketplace uses another id.
EXT_ID="${LE_VIBE_CONTINUE_EXTENSION:-continue.continue}"

# LE_VIBE_CONTINUE_OPENVSX_VERSION: unset → read pin file; "latest" or empty → no @version; else explicit semver.
if [[ -v LE_VIBE_CONTINUE_OPENVSX_VERSION ]]; then
  VER="${LE_VIBE_CONTINUE_OPENVSX_VERSION}"
else
  VER=""
  if [[ -f "$PIN_FILE" ]]; then
    VER="$(grep -v '^[[:space:]]*#' "$PIN_FILE" | head -1 | tr -d '[:space:]\r')"
  fi
fi

REF="$EXT_ID"
if [[ -n "$VER" && "$VER" != "latest" ]]; then
  REF="${EXT_ID}@${VER}"
fi

if ! command -v "$BIN" >/dev/null 2>&1; then
  echo "le-vibe: no editor binary found (set LE_VIBE_EDITOR). Skipping Continue install." >&2
  exit 0
fi
exec "$BIN" --install-extension "$REF" "$@"
