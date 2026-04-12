#!/usr/bin/env bash
# STEP 14.f — unpack a linux_compile artifact (vscodium-linux-build.tar.gz) to a temp dir and print
# the absolute path to VSCode-linux-*/bin/codium (same layout as print-vsbuild-codium-path.sh).
#
# From repo root:
#   LE_VIBE_EDITOR="$(./editor/print-ci-tarball-codium-path.sh ~/Downloads/vscodium-linux-build.tar.gz)"
#
# Requires: tar, mktemp. Does not leave the tarball extracted in your cwd (temp dir removed after).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[[ $# -eq 1 ]] || {
  echo "usage: ${0##*/} /path/to/vscodium-linux-build.tar.gz" >&2
  exit 2
}

TAR="$(realpath "$1")"
[[ -f "$TAR" ]] || {
  echo "${0##*/}: not a file: $TAR" >&2
  exit 1
}

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/le-vibe-ci-artifact.XXXXXX")"
cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

tar -xzf "${TAR}" -C "${WORKDIR}"
exec "${ROOT}/editor/print-vsbuild-codium-path.sh" "${WORKDIR}"
