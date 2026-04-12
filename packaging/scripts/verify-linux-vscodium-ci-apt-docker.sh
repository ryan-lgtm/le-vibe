#!/usr/bin/env bash
# STEP 14 (14.e): verify packaging/linux-vscodium-ci-apt.pkgs installs on ubuntu:22.04 (linux_compile runner)
# without needing sudo on the host — uses Docker. PRODUCT_SPEC §7.3 CI parity for native npm / pkg-config.
# Requires: docker on PATH, network for image pull + apt.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKGS="${ROOT}/packaging/linux-vscodium-ci-apt.pkgs"
IMAGE="${LEVIBE_VERIFY_APT_DOCKER_IMAGE:-ubuntu:22.04}"

usage() {
  cat <<EOF
Usage: packaging/scripts/verify-linux-vscodium-ci-apt-docker.sh

Mounts this repo read-only at /src in a fresh ${IMAGE} container, runs apt-get install
for every package in packaging/linux-vscodium-ci-apt.pkgs, then checks pkg-config xkbfile
and python3.11 -c (matches CI linux_compile base image).

Environment:
  LEVIBE_VERIFY_APT_DOCKER_IMAGE   Override image (default: ubuntu:22.04).

See editor/BUILD.md (14.e), packaging/scripts/install-linux-vscodium-build-deps.sh.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ -f "${PKGS}" ]] || {
  echo "verify-linux-vscodium-ci-apt-docker: missing ${PKGS}" >&2
  exit 1
}

if ! command -v docker >/dev/null 2>&1; then
  echo "verify-linux-vscodium-ci-apt-docker: docker not on PATH — install Docker or use install-linux-vscodium-build-deps.sh on the host." >&2
  exit 2
fi

echo "verify-linux-vscodium-ci-apt-docker: using image ${IMAGE} (LEVIBE_VERIFY_APT_DOCKER_IMAGE)"

docker run --rm -v "${ROOT}:/src:ro" "${IMAGE}" bash -ceu '
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
mapfile -t p < <(grep -v "^[[:space:]]*#" /src/packaging/linux-vscodium-ci-apt.pkgs | grep -v "^[[:space:]]*$")
echo "verify-linux-vscodium-ci-apt-docker: installing ${#p[@]} packages"
apt-get install -y "${p[@]}"
pkg-config --exists xkbfile
python3.11 -c "import sys; print(sys.version)"
echo "verify-linux-vscodium-ci-apt-docker: OK — linux-vscodium-ci-apt.pkgs satisfied on CI base image."
'
