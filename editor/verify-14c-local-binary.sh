#!/usr/bin/env bash
# STEP 14.c — confirm local dev/build.sh produced VSCode-linux-*/bin/codium under editor/vscodium/.
# No network; does not start Ollama (unlike smoke-built-codium-lvibe.sh). From repo root:
#   ./editor/verify-14c-local-binary.sh
# Exit 0: prints absolute path to bin/codium on stdout (same as print-built-codium-path.sh).
# Exit 1: stderr lists upstream message plus monorepo next steps (14.a→14.c).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (before fetch/build under editor/vscodium/).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.c verify local VSCode-linux tree after STEP 0–1.
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
if [[ "${out}" == *"partial or incomplete"* ]]; then
  echo "verify-14c-local-binary: (14.c) Incomplete VSCode-linux tree — finish cd editor/vscodium && ./dev/build.sh (editor/BUILD.md 14.c). Full launcher smoke: ./editor/smoke-built-codium-lvibe.sh (needs ollama on PATH)." >&2
else
  echo "verify-14c-local-binary: (14.c) No built tree yet — toolchain → fetch → compile: editor/BUILD.md (14.a use-node-toolchain.sh, 14.b fetch-vscode-sources.sh, then cd editor/vscodium && ./dev/build.sh). Full launcher smoke: ./editor/smoke-built-codium-lvibe.sh (needs ollama on PATH)." >&2
fi
exit 1
