#!/usr/bin/env bash
# STEP 14.f — unpack a linux_compile artifact (vscodium-linux-build.tar.gz) to a temp dir and print
# the absolute path to VSCode-linux-*/bin/codium (same layout as print-vsbuild-codium-path.sh).
#
# GitHub Actions serves workflow artifacts as a .zip download; unzip first — the archive contains
# vscodium-linux-build.tar.gz (see editor/BUILD.md *14.f*).
# Local tree instead of this tarball: Fresh clone (14.b) — git submodule update --init editor/vscodium — editor/README.md, then editor/BUILD.md (14.a→14.c).
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
  echo "${0##*/}: not a file: $TAR — pass the path to vscodium-linux-build.tar.gz from CI (editor/BUILD.md 14.f)." >&2
  exit 1
}

_lc="${TAR,,}"
if [[ "${_lc}" == *.zip ]]; then
  echo "${0##*/}: received a .zip — GitHub Actions wraps \`vscodium-linux-build.tar.gz\` inside the download; unzip first, then pass the \`.tar.gz\` path (see editor/BUILD.md *14.f*)." >&2
  exit 2
fi

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/le-vibe-ci-artifact.XXXXXX")"
cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

tar -xzf "${TAR}" -C "${WORKDIR}"
exec "${ROOT}/editor/print-vsbuild-codium-path.sh" "${WORKDIR}"
