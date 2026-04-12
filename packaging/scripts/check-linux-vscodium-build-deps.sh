#!/usr/bin/env bash
# STEP 14 (14.e): verify Debian/Ubuntu packages aligned with packaging/linux-vscodium-ci-apt.pkgs
# (same as .github/workflows/build-le-vibe-ide.yml *Install Linux build dependencies*).
# Does not install anything — prints `sudo apt-get install ...` when something is missing.
# Also checks pkg-config modules needed by native npm addons (e.g. @vscodium/native-keymap → xkbfile).
# Optional: LEVIBE_CHECK_RUST=1 warns when rustc/cargo are absent (vscode ripgrep / native crates).
# Authority: editor/BUILD.md *When full compile fails*, build-le-vibe-ide.yml linux_compile job.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS_FILE="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/check-linux-vscodium-build-deps.sh

From the repository root: verify host packages match packaging/linux-vscodium-ci-apt.pkgs
(build-le-vibe-ide.yml linux_compile). Exits 0 when all listed packages are installed and
pkg-config sees xkbfile; otherwise 1 + remediation.

Environment:
  LEVIBE_CHECK_RUST   When set to 1, warn if rustc is not on PATH (Rust installed separately in CI).

See editor/BUILD.md (14.e), packaging/scripts/install-linux-vscodium-build-deps.sh.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ -f "${PKGS_FILE}" ]] || {
  echo "check-linux-vscodium-build-deps: missing ${PKGS_FILE} — restore from git." >&2
  exit 1
}

# Python headers: CI uses python3.11-dev from the pkgs file; Ubuntu 24.04+ often has python3.12-dev
# only — accept any one of python3.{11,12,13,14}-dev or meta python3-dev (skip those lines below).
DEBS=()
while IFS= read -r line || [[ -n "${line}" ]]; do
  line="${line//$'\r'/}"
  [[ "${line}" =~ ^[[:space:]]*# ]] && continue
  [[ -z "${line// }" ]] && continue
  if [[ "${line}" =~ ^python3(\.[0-9]+)?-dev$ ]] || [[ "${line}" == "python3-dev" ]]; then
    continue
  fi
  DEBS+=("${line}")
done < "${PKGS_FILE}"

_pkg_ok() {
  dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q 'install ok installed$'
}

_python_dev_headers_ok() {
  local p
  for p in python3.11-dev python3.12-dev python3.13-dev python3.14-dev python3-dev; do
    if _pkg_ok "$p"; then
      return 0
    fi
  done
  return 1
}

missing=()
for p in "${DEBS[@]}"; do
  if ! _pkg_ok "$p"; then
    missing+=("$p")
  fi
done

_pydev_ok=1
if ! _python_dev_headers_ok; then
  echo "check-linux-vscodium-build-deps: no python3.*-dev (or python3-dev) — CI pkgs list includes python3.11-dev; on Ubuntu 24.04 use python3.12-dev or run install-linux-vscodium-build-deps.sh." >&2
  _pydev_ok=0
fi

_pc_ok=1
if ! command -v pkg-config >/dev/null 2>&1; then
  echo "check-linux-vscodium-build-deps: pkg-config not on PATH — install pkg-config (listed in CI set)." >&2
  _pc_ok=0
elif ! pkg-config --exists xkbfile 2>/dev/null; then
  echo "check-linux-vscodium-build-deps: pkg-config cannot find module xkbfile — usually fixed by libxkbfile-dev." >&2
  _pc_ok=0
fi

if [[ "${LEVIBE_CHECK_RUST:-0}" == "1" ]] && ! command -v rustc >/dev/null 2>&1; then
  echo "check-linux-vscodium-build-deps: warning: rustc not on PATH — CI linux_compile installs Rust via dtolnay/rust-toolchain; local builds may need: curl https://sh.rustup.rs -sSf | sh -s -- -y" >&2
fi

if [[ ${#missing[@]} -eq 0 && "${_pc_ok}" -eq 1 && "${_pydev_ok}" -eq 1 ]]; then
  echo "check-linux-vscodium-build-deps: OK — ${PKGS_FILE#"${ROOT}/"} satisfied and pkg-config xkbfile present."
  exit 0
fi

echo "check-linux-vscodium-build-deps: missing Debian packages: ${missing[*]:-(none)}" >&2
echo "check-linux-vscodium-build-deps: install (Debian/Ubuntu):" >&2
echo "  ./packaging/scripts/install-linux-vscodium-build-deps.sh" >&2
echo "  # or: sudo apt-get update && sudo apt-get install -y ${missing[*]}" >&2
if [[ "${_pydev_ok}" -eq 0 ]]; then
  echo "  # also: sudo apt-get install -y python3.11-dev   # ubuntu-22.04 / CI pkgs, or python3.12-dev on 24.04+" >&2
fi
echo "check-linux-vscodium-build-deps: parity: packaging/linux-vscodium-ci-apt.pkgs — editor/BUILD.md 14.e." >&2
exit 1
