#!/usr/bin/env bash
# STEP 14 (14.e): verify Debian/Ubuntu packages aligned with .github/workflows/build-le-vibe-ide.yml
# *Install Linux build dependencies* before a local dev/build.sh (PRODUCT_SPEC §7.3).
# Does not install anything — prints `sudo apt-get install ...` when something is missing.
# Also checks pkg-config modules needed by native npm addons (e.g. @vscodium/native-keymap → xkbfile).
# Optional: LEVIBE_CHECK_RUST=1 warns when rustc/cargo are absent (vscode ripgrep / native crates).
# Authority: editor/BUILD.md *When full compile fails*, build-le-vibe-ide.yml linux_compile job.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/check-linux-vscodium-build-deps.sh

From the repository root: verify host packages match CI linux_compile (build-le-vibe-ide.yml).
Exits 0 when all listed packages are installed and pkg-config sees xkbfile; otherwise 1 + remediation.

Environment:
  LEVIBE_CHECK_RUST   When set to 1, warn if rustc is not on PATH (Rust installed separately in CI).

See editor/BUILD.md (14.e), .github/workflows/build-le-vibe-ide.yml *Install Linux build dependencies*.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

# Keep in sync with build-le-vibe-ide.yml (Install Linux build dependencies).
DEBS=(
  build-essential
  pkg-config
  libx11-dev
  libxkbfile-dev
  libsecret-1-dev
  libkrb5-dev
  fakeroot
  dpkg-dev
  rpm
  jq
  librsvg2-bin
  git
  python3
  python3.11-dev
  curl
  ca-certificates
)

_pkg_ok() {
  dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q 'install ok installed$'
}

missing=()
for p in "${DEBS[@]}"; do
  if ! _pkg_ok "$p"; then
    missing+=("$p")
  fi
done

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

if [[ ${#missing[@]} -eq 0 && "${_pc_ok}" -eq 1 ]]; then
  echo "check-linux-vscodium-build-deps: OK — CI-aligned apt packages and pkg-config xkbfile present."
  exit 0
fi

echo "check-linux-vscodium-build-deps: missing Debian packages: ${missing[*]:-(none)}" >&2
echo "check-linux-vscodium-build-deps: install (Debian/Ubuntu):" >&2
echo "  sudo apt-get update && sudo apt-get install -y ${missing[*]}" >&2
echo "check-linux-vscodium-build-deps: parity: .github/workflows/build-le-vibe-ide.yml *Install Linux build dependencies* — editor/BUILD.md 14.e." >&2
exit 1
