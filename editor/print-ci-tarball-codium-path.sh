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
  echo "usage: ${0##*/} /path/to/vscodium-linux-build.tar.gz — exactly one argument (editor/BUILD.md 14.f)." >&2
  exit 2
}

ARG="$1"
if [[ ! -f "$ARG" ]]; then
  echo "${0##*/}: not a regular file: $ARG — pass the path to vscodium-linux-build.tar.gz from CI (editor/BUILD.md 14.f)." >&2
  exit 1
fi
TAR="$(realpath "$ARG")"

if ! command -v tar >/dev/null 2>&1; then
  echo "${0##*/}: tar not on PATH — install: sudo apt install tar (Debian/Ubuntu)" >&2
  exit 1
fi

_lc="${TAR,,}"
if [[ "${_lc}" == *.zip ]]; then
  echo "${0##*/}: received a .zip — GitHub Actions wraps \`vscodium-linux-build.tar.gz\` inside the download; unzip first, then pass the \`.tar.gz\` path (see editor/BUILD.md *14.f*)." >&2
  exit 2
fi

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/le-vibe-ci-artifact.XXXXXX")" || {
  echo "${0##*/}: mktemp failed — check TMPDIR is writable and not full (editor/BUILD.md 14.f)." >&2
  exit 1
}
cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

if ! tar -xzf "${TAR}" -C "${WORKDIR}"; then
  echo "${0##*/}: tar extract failed — $TAR may be corrupt or not a .tar.gz from linux_compile (editor/BUILD.md 14.f)." >&2
  exit 1
fi
exec "${ROOT}/editor/print-vsbuild-codium-path.sh" "${WORKDIR}"
