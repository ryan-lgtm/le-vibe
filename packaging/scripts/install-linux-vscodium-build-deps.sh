#!/usr/bin/env bash
# STEP 14 (14.e): sudo apt-get install the same set as build-le-vibe-ide.yml *Install Linux build dependencies*.
# Source of truth: packaging/linux-vscodium-ci-apt.pkgs (PRODUCT_SPEC §7.3 local full compile path).
# Requires: sudo, apt-get (Debian/Ubuntu). Run from repository root.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/install-linux-vscodium-build-deps.sh

Installs Debian packages from packaging/linux-vscodium-ci-apt.pkgs (same list as
.github/workflows/build-le-vibe-ide.yml linux_compile). Requires sudo.

On Ubuntu 24.04+, if python3.11-dev is unavailable, install python3.12-dev manually
and re-run packaging/scripts/check-linux-vscodium-build-deps.sh — see editor/BUILD.md (14.e).

See also: packaging/scripts/check-linux-vscodium-build-deps.sh (verify only).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ -f "${PKGS}" ]] || {
  echo "install-linux-vscodium-build-deps: missing ${PKGS} — restore from git." >&2
  exit 1
}

if ! command -v sudo >/dev/null 2>&1; then
  echo "install-linux-vscodium-build-deps: sudo not on PATH — run as root or install sudo." >&2
  exit 2
fi

mapfile -t _lines < <(grep -v '^[[:space:]]*#' "${PKGS}" | grep -v '^[[:space:]]*$' || true)
if [[ ${#_lines[@]} -eq 0 ]]; then
  echo "install-linux-vscodium-build-deps: no packages in ${PKGS}" >&2
  exit 1
fi

echo "install-linux-vscodium-build-deps: apt-get update + install ${#_lines[@]} packages (see ${PKGS})"
sudo apt-get update -y
sudo apt-get install -y "${_lines[@]}"
