#!/usr/bin/env bash
# STEP 14.c — confirm local dev/build.sh produced VSCode-linux-*/bin/codium under editor/vscodium/.
# No network; does not start Ollama (unlike smoke-built-codium-lvibe.sh). From repo root:
#   ./editor/verify-14c-local-binary.sh
# Exit 0: prints absolute path to bin/codium on stdout (same as print-built-codium-path.sh).
# Exit 1: stderr lists upstream message plus monorepo next steps (14.a→14.c).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (before fetch/build under editor/vscodium/).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PB="${ROOT}/editor/print-built-codium-path.sh"

set +e
out="$("${PB}" 2>&1)"
ec=$?
set -e

if [[ "${ec}" -eq 0 ]]; then
  printf '%s\n' "${out}"
  exit 0
fi

printf '%s\n' "${out}" >&2
echo "verify-14c-local-binary: (14.c) No built tree yet — toolchain → fetch → compile: editor/BUILD.md (14.a use-node-toolchain.sh, 14.b fetch-vscode-sources.sh, then cd editor/vscodium && ./dev/build.sh). Full launcher smoke: ./editor/smoke-built-codium-lvibe.sh (needs ollama on PATH)." >&2
exit 1
