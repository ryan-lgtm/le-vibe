#!/usr/bin/env bash
# STEP 14 (14.e): invoke upstream VSCodium dev/build.sh from the monorepo (real compile).
# Run from repository root on a Linux machine with build deps installed (see editor/vscodium/docs/howto-build.md).
# CI: build-le-vibe-ide.yml job linux_compile — not run on pull_request (too slow for default runners).
# Optional env: editor/le-vibe-overrides/build-env.sh (see build-env.sh.example) — sourced before dev/build.sh.
# Authority: editor/BUILD.md, docs/vscodium-fork-le-vibe.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT}/editor/vscodium"

[[ -f ./product.json ]] || {
  echo "ci-vscodium-linux-dev-build: expected editor/vscodium/product.json (init submodule)." >&2
  exit 1
}
[[ -x ./dev/build.sh ]] || {
  echo "ci-vscodium-linux-dev-build: dev/build.sh missing or not executable." >&2
  exit 1
}

if [[ -f "${ROOT}/editor/le-vibe-overrides/build-env.sh" ]]; then
  echo "ci-vscodium-linux-dev-build: sourcing editor/le-vibe-overrides/build-env.sh"
  set -a
  # shellcheck disable=SC1091
  . "${ROOT}/editor/le-vibe-overrides/build-env.sh"
  set +a
fi

exec ./dev/build.sh
