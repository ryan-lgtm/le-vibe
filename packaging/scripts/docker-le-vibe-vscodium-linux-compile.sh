#!/usr/bin/env bash
# STEP 14 (§7.3 / 14.e): full VSCodium linux compile inside Docker — parity with
# .github/workflows/build-le-vibe-ide.yml job linux_compile (ubuntu-22.04, same apt list,
# Node from editor/.nvmrc via nvm, Rust stable, NODE_OPTIONS --max-old-space-size=8192).
#
# This is a long-running, disk-heavy path (hours; may OOM on small machines). Prefer CI
# workflow_dispatch (vscodium_linux_compile) or a self-hosted runner when available.
# Maintainer index: docs/ci-qa-hardening.md — *Optional full Linux compile* (Runner realism; Related docs).
#
# Mutates editor/vscodium/ (§7.3 merge, icons, dev/build.sh patch) and produces
# editor/vscodium/VSCode-linux-* when successful. Restores UID/GID on editor/vscodium after
# the container exits.
#
# Requires: docker, network. editor/vscodium submodule initialized; editor/vscodium/vscode/
# should exist (run ./editor/fetch-vscode-sources.sh from the host if missing — editor/BUILD.md).
#
# Optional: LEVIBE_DOCKER_COMPILE_CARGO_VOLUME — Docker volume name mounted at /root/.cargo so
# repeat compiles reuse the Cargo registry (parity with build-le-vibe-ide.yml *Cache Cargo registry*).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — optional Docker 14.e full compile (STEP 14 after STEP 0–1).
# Pytest: le-vibe/tests/test_docker_le_vibe_vscodium_linux_compile_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"
IMAGE="${LEVIBE_COMPILE_DOCKER_IMAGE:-ubuntu:22.04}"
HOST_UID="${LEVIBE_COMPILE_HOST_UID:-$(id -u)}"
HOST_GID="${LEVIBE_COMPILE_HOST_GID:-$(id -g)}"
# Match build-le-vibe-ide.yml linux_compile env and editor/vscodium/dev/build.sh.
NVM_INSTALL_VER="${LEVIBE_DOCKER_NVM_VERSION:-v0.40.1}"
CARGO_VOL="${LEVIBE_DOCKER_COMPILE_CARGO_VOLUME:-}"

usage() {
  cat <<EOF
Usage: packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh

Bind-mounts this repository at /work in a fresh ${IMAGE} container, installs
packaging/linux-vscodium-ci-apt.pkgs, then installs nvm + Node (editor/.nvmrc) and Rust
stable, exports NODE_OPTIONS (default --max-old-space-size=8192), and runs:

  ./packaging/scripts/ci-vscodium-linux-dev-build.sh

(full upstream dev/build.sh — long). Does not set LEVIBE_VSCODIUM_PREPARE_ONLY.

Environment:
  LEVIBE_COMPILE_DOCKER_IMAGE          Base image (default: ubuntu:22.04; match linux_compile)
  LEVIBE_COMPILE_HOST_UID              chown target uid for editor/vscodium (default: \$(id -u))
  LEVIBE_COMPILE_HOST_GID              chown target gid (default: \$(id -g))
  NODE_OPTIONS                         Passed into the container (default: --max-old-space-size=8192)
  LEVIBE_DOCKER_NVM_VERSION            nvm install.sh tag (default: ${NVM_INSTALL_VER})
  LEVIBE_DOCKER_COMPILE_CARGO_VOLUME   If set, docker volume name mounted at /root/.cargo (repeat-run speed; CI *linux_compile* caches registry/git similarly).

See editor/BUILD.md (14.e), .github/workflows/build-le-vibe-ide.yml (linux_compile).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ -f "${PKGS}" ]] || {
  echo "docker-le-vibe-vscodium-linux-compile: missing ${PKGS}" >&2
  exit 1
}
[[ -f "${ROOT}/editor/vscodium/product.json" ]] || {
  echo "docker-le-vibe-vscodium-linux-compile: expected editor/vscodium/product.json — git submodule update --init editor/vscodium (editor/README.md 14.b)." >&2
  exit 1
}

if ! command -v docker >/dev/null 2>&1; then
  echo "docker-le-vibe-vscodium-linux-compile: docker not on PATH." >&2
  exit 2
fi

export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=8192}"
echo "docker-le-vibe-vscodium-linux-compile: image=${IMAGE} HOST_UID=${HOST_UID} HOST_GID=${HOST_GID} NODE_OPTIONS=${NODE_OPTIONS}"
if [[ -n "${CARGO_VOL}" ]]; then
  docker volume create "${CARGO_VOL}" >/dev/null 2>&1 || true
  echo "docker-le-vibe-vscodium-linux-compile: Cargo cache volume ${CARGO_VOL} -> /root/.cargo"
fi

DOCKER_RUN=(docker run --rm)
DOCKER_RUN+=(-e "HOST_UID=${HOST_UID}")
DOCKER_RUN+=(-e "HOST_GID=${HOST_GID}")
DOCKER_RUN+=(-e "NODE_OPTIONS=${NODE_OPTIONS}")
DOCKER_RUN+=(-e "NVM_INSTALL_VER=${NVM_INSTALL_VER}")
if [[ -n "${CARGO_VOL}" ]]; then
  DOCKER_RUN+=(-v "${CARGO_VOL}:/root/.cargo")
fi
DOCKER_RUN+=(-v "${ROOT}:/work")
DOCKER_RUN+=(-w /work)
DOCKER_RUN+=("${IMAGE}")
DOCKER_RUN+=(bash -ceu '
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
mapfile -t p < <(grep -v "^[[:space:]]*#" /work/packaging/linux-vscodium-ci-apt.pkgs | grep -v "^[[:space:]]*$")
echo "docker-le-vibe-vscodium-linux-compile: installing ${#p[@]} apt packages"
apt-get install -y "${p[@]}"

export NVM_DIR="/root/.nvm"
curl -fsSL "https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_INSTALL_VER}/install.sh" | bash
# shellcheck source=/dev/null
. "${NVM_DIR}/nvm.sh"
pushd /work/editor >/dev/null
nvm install
nvm use
popd >/dev/null
command -v node
node --version
command -v npm
npm --version

curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
# shellcheck source=/dev/null
. "${HOME}/.cargo/env"
rustc --version

cd /work
./packaging/scripts/ci-vscodium-linux-dev-build.sh
chown -R "${HOST_UID}:${HOST_GID}" /work/editor/vscodium
echo "docker-le-vibe-vscodium-linux-compile: finished — editor/vscodium ownership restored."
')
"${DOCKER_RUN[@]}"
