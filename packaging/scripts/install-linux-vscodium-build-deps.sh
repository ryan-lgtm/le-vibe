#!/usr/bin/env bash
# STEP 14 (14.e): apt-get install the same set as build-le-vibe-ide.yml *Install Linux build dependencies*.
# Source of truth: packaging/linux-vscodium-ci-apt.pkgs (PRODUCT_SPEC §7.3 local full compile path).
# Requires: apt-get (Debian/Ubuntu). Run as root (e.g. Docker) or with sudo on PATH. Run from repository root.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.e install linux_compile deps (STEP 14 after STEP 0–1).
# Pytest: le-vibe/tests/test_check_linux_vscodium_build_deps_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/install-linux-vscodium-build-deps.sh [--print-install-command]

Installs Debian packages from packaging/linux-vscodium-ci-apt.pkgs (same list as
.github/workflows/build-le-vibe-ide.yml linux_compile).

Runs apt-get directly when already root (EUID 0); otherwise uses sudo.

Options:
  --print-install-command  Print the apt command and exit (no install). Helpful on hosts
                           where sudo requires an interactive password prompt.

On Ubuntu 24.04+, if python3.11-dev is unavailable, install python3.12-dev manually
and re-run packaging/scripts/check-linux-vscodium-build-deps.sh — see editor/BUILD.md (14.e).

See also: packaging/scripts/check-linux-vscodium-build-deps.sh (verify only).
EOF
}

PRINT_INSTALL_COMMAND=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --print-install-command) PRINT_INSTALL_COMMAND=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "install-linux-vscodium-build-deps: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

[[ -f "${PKGS}" ]] || {
  echo "install-linux-vscodium-build-deps: missing ${PKGS} — restore from git." >&2
  exit 1
}

_apt() {
  if [[ "${EUID:-0}" -eq 0 ]]; then
    "$@"
  else
    if ! command -v sudo >/dev/null 2>&1; then
      echo "install-linux-vscodium-build-deps: not root and sudo not on PATH — re-run as root or install sudo." >&2
      exit 2
    fi
    if ! sudo -n true >/dev/null 2>&1; then
      echo "install-linux-vscodium-build-deps: sudo requires an interactive password on this host." >&2
      echo "install-linux-vscodium-build-deps: run this command manually in an interactive terminal:" >&2
      echo "  sudo apt-get update && sudo apt-get install -y ${_lines[*]}" >&2
      exit 2
    fi
    sudo "$@"
  fi
}

mapfile -t _lines < <(grep -v '^[[:space:]]*#' "${PKGS}" | grep -v '^[[:space:]]*$' || true)
if [[ ${#_lines[@]} -eq 0 ]]; then
  echo "install-linux-vscodium-build-deps: no packages in ${PKGS}" >&2
  exit 1
fi

echo "install-linux-vscodium-build-deps: apt-get update + install ${#_lines[@]} packages (see ${PKGS#"${ROOT}/"})"
if [[ "$PRINT_INSTALL_COMMAND" -eq 1 ]]; then
  if [[ "${EUID:-0}" -eq 0 ]]; then
    echo "apt-get update && apt-get install -y ${_lines[*]}"
  else
    echo "sudo apt-get update && sudo apt-get install -y ${_lines[*]}"
  fi
  exit 0
fi
_apt apt-get update -y
_apt apt-get install -y "${_lines[@]}"
