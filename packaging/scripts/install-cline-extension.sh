#!/usr/bin/env bash
# Install the Cline extension and companion Red Hat YAML extension into VSCodium / Code - OSS (Open VSX).
# Deterministic behavior: retries extension installs with bounded attempts and explicit remediation.
# Default pins: packaging/cline-openvsx-version (Cline) + packaging/vscode-yaml-openvsx-version (redhat.vscode-yaml).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIN_DEFAULT="${SCRIPT_DIR}/../cline-openvsx-version"
PIN_FILE="${LE_VIBE_CLINE_PIN_FILE:-$PIN_DEFAULT}"
YAML_PIN_DEFAULT="${SCRIPT_DIR}/../vscode-yaml-openvsx-version"
YAML_PIN_FILE="${LE_VIBE_VSCODE_YAML_PIN_FILE:-$YAML_PIN_DEFAULT}"

if [[ -n "${LE_VIBE_EDITOR:-}" ]]; then
  BIN="${LE_VIBE_EDITOR}"
elif [[ -x /usr/lib/le-vibe/bin/codium ]]; then
  BIN="/usr/lib/le-vibe/bin/codium"
elif [[ -x /usr/bin/codium ]]; then
  BIN="/usr/bin/codium"
else
  BIN="codium"
fi

# Open VSX default extension ids.
EXT_ID="${LE_VIBE_CLINE_EXTENSION:-saoudrizwan.claude-dev}"
YAML_EXT_ID="${LE_VIBE_VSCODE_YAML_EXTENSION:-redhat.vscode-yaml}"
DISALLOWED_EXT_ID="${LE_VIBE_DISALLOWED_CONTINUE_EXTENSION:-continue.continue}"

_read_pin_line() {
  local f="$1"
  if [[ ! -f "$f" ]]; then
    echo ""
    return 0
  fi
  if ! command -v awk >/dev/null 2>&1; then
    echo "install-cline-extension: awk not on PATH — install gawk/mawk (e.g. sudo apt install gawk)." >&2
    exit 1
  fi
  awk 'NF && $1 !~ /^#/ {gsub(/[[:space:]\r]/, "", $0); print; exit}' "$f"
}

if [[ -v LE_VIBE_CLINE_OPENVSX_VERSION ]]; then
  VER="${LE_VIBE_CLINE_OPENVSX_VERSION}"
else
  VER="$(_read_pin_line "$PIN_FILE")"
fi

REF="$EXT_ID"
if [[ -n "$VER" && "$VER" != "latest" ]]; then
  REF="${EXT_ID}@${VER}"
fi

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
  echo "le-vibe: no editor binary found (set LE_VIBE_EDITOR). Skipping extension installs (Cline + YAML)." >&2
  exit 0
fi

install_with_retry() {
  local ref="$1"
  local label="$2"
  local attempts="${LE_VIBE_CLINE_INSTALL_ATTEMPTS:-3}"
  local sleep_s="${LE_VIBE_CLINE_INSTALL_RETRY_SLEEP_SEC:-2}"
  local n=1
  while (( n <= attempts )); do
    if "$BIN" --install-extension "$ref"; then
      return 0
    fi
    if (( n == attempts )); then
      echo "install-cline-extension: ${label} extension install failed after ${attempts} attempts (${ref})." >&2
      return 1
    fi
    echo "install-cline-extension: retry ${n}/${attempts} failed for ${label}; sleeping ${sleep_s}s before retry." >&2
    sleep "$sleep_s"
    ((n++))
  done
}

cleanup_disallowed_continue_state() {
  local ext_id="$1"
  local listed
  local line
  local found=0
  listed="$("$BIN" --list-extensions 2>/dev/null | tr '[:upper:]' '[:lower:]' || true)"
  while IFS= read -r line; do
    if [[ "$line" == "$ext_id" ]]; then
      found=1
      break
    fi
  done <<< "$listed"
  if [[ "$found" -eq 1 ]]; then
    echo "install-cline-extension: uninstalling disallowed extension ${ext_id}." >&2
    if ! "$BIN" --uninstall-extension "$ext_id"; then
      echo "install-cline-extension: failed to uninstall disallowed extension ${ext_id}." >&2
      echo "  Remediation: ${BIN} --uninstall-extension ${ext_id}" >&2
      return 1
    fi
  fi

  local ext_dir=""
  for ext_dir in \
    "${HOME}/.vscode-oss/extensions" \
    "${HOME}/.vscode/extensions" \
    "${HOME}/.config/VSCodium/extensions"
  do
    [[ -d "$ext_dir" ]] || continue
    rm -rf "${ext_dir}/${ext_id}-"*
  done
}

if [[ "${LE_VIBE_CLEANUP_CONTINUE_STATE:-1}" != "0" ]]; then
  cleanup_disallowed_continue_state "$DISALLOWED_EXT_ID"
fi

install_with_retry "$REF" "Cline"
install_with_retry "$YAML_REF" "YAML"
