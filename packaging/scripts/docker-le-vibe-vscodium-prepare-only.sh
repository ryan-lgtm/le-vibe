#!/usr/bin/env bash
# STEP 14 (§7.3): run LEVIBE_VSCODIUM_PREPARE_ONLY=1 inside ubuntu:22.04 with the same apt set as
# build-le-vibe-ide.yml — merge branding, sync Linux icons, patch dev/build.sh — without a host
# full compile and without host sudo for apt (Docker runs apt as root in the container).
#
# Mutates editor/vscodium/ (product.json, dev/build.sh, linux resources). Restores UID/GID on
# editor/vscodium to HOST_UID/HOST_GID (defaults: caller id) after the script so the bind mount
# is not left root-owned.
#
# Requires: docker, network (image pull + apt). Submodule editor/vscodium/ must be present.
# See editor/BUILD.md (14.e), packaging/linux-vscodium-ci-apt.pkgs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"
IMAGE="${LEVIBE_PREPARE_DOCKER_IMAGE:-ubuntu:22.04}"
HOST_UID="${LEVIBE_PREPARE_HOST_UID:-$(id -u)}"
HOST_GID="${LEVIBE_PREPARE_HOST_GID:-$(id -g)}"

usage() {
  cat <<EOF
Usage: packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh

Bind-mounts this repository at /work in a fresh ${IMAGE} container, installs every package in
packaging/linux-vscodium-ci-apt.pkgs (CI parity), then runs:

  LEVIBE_VSCODIUM_PREPARE_ONLY=1 ./packaging/scripts/ci-vscodium-linux-dev-build.sh

from the repo root. Does not compile Electron. Mutates editor/vscodium/ — reset with
git checkout -- editor/vscodium if needed.

Environment:
  LEVIBE_PREPARE_DOCKER_IMAGE   Base image (default: ubuntu:22.04)
  LEVIBE_PREPARE_HOST_UID       chown target uid for editor/vscodium (default: \$(id -u))
  LEVIBE_PREPARE_HOST_GID       chown target gid (default: \$(id -g))

See editor/BUILD.md (§7.3 prepare-only), packaging/scripts/verify-linux-vscodium-ci-apt-docker.sh.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ -f "${PKGS}" ]] || {
  echo "docker-le-vibe-vscodium-prepare-only: missing ${PKGS}" >&2
  exit 1
}
[[ -f "${ROOT}/editor/vscodium/product.json" ]] || {
  echo "docker-le-vibe-vscodium-prepare-only: expected editor/vscodium/product.json — git submodule update --init editor/vscodium (editor/README.md 14.b)." >&2
  exit 1
}

if ! command -v docker >/dev/null 2>&1; then
  echo "docker-le-vibe-vscodium-prepare-only: docker not on PATH." >&2
  exit 2
fi

echo "docker-le-vibe-vscodium-prepare-only: image=${IMAGE} HOST_UID=${HOST_UID} HOST_GID=${HOST_GID}"

docker run --rm \
  -e HOST_UID="${HOST_UID}" \
  -e HOST_GID="${HOST_GID}" \
  -v "${ROOT}:/work" \
  -w /work \
  "${IMAGE}" \
  bash -ceu '
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
mapfile -t p < <(grep -v "^[[:space:]]*#" /work/packaging/linux-vscodium-ci-apt.pkgs | grep -v "^[[:space:]]*$")
echo "docker-le-vibe-vscodium-prepare-only: installing ${#p[@]} apt packages"
apt-get install -y "${p[@]}"
LEVIBE_VSCODIUM_PREPARE_ONLY=1 ./packaging/scripts/ci-vscodium-linux-dev-build.sh
chown -R "${HOST_UID}:${HOST_GID}" /work/editor/vscodium
echo "docker-le-vibe-vscodium-prepare-only: OK — §7.3 layers applied; editor/vscodium ownership restored."
'
