#!/usr/bin/env bash
# STEP 14 (14.f): print absolute path to VSCode-linux-*/bin/codium under a directory tree.
# If SEARCH_ROOT is repo editor/vscodium: Fresh clone (14.b) — git submodule update --init editor/vscodium — editor/README.md (before 14.a fetch / dev/build.sh).
# Use after unpacking vscodium-linux-build.tar.gz from linux_compile, or any tree that contains VSCode-linux-*.
# Usage: ./editor/print-vsbuild-codium-path.sh [SEARCH_ROOT]
#   SEARCH_ROOT defaults to the current working directory (typical: cd to unpack dir, then run from repo with ../../editor/... or pass the unpack path).
# Example (artifact in /tmp/vs):
#   ./editor/print-vsbuild-codium-path.sh /tmp/vs
# Requires: stat and realpath (coreutils).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — 14.f VSCode-linux path resolution after STEP 0–1.
set -euo pipefail

SEARCH="${1:-.}"
if [[ ! -d "$SEARCH" ]]; then
  echo "print-vsbuild-codium-path: not a directory: $SEARCH — pass a path to an unpacked VSCode-linux-* tree or editor/vscodium (editor/BUILD.md 14.f / 14.c)." >&2
  exit 1
fi
SEARCH="$(cd "$SEARCH" && pwd)"

shopt -s nullglob
matches=("${SEARCH}"/VSCode-linux-*/bin/codium)

if [[ ${#matches[@]} -eq 0 ]]; then
  echo "print-vsbuild-codium-path: no VSCode-linux-*/bin/codium under ${SEARCH} — editor/BUILD.md 14.f (artifact) or 14.c (local build). If editor/vscodium/ is empty: git submodule update --init editor/vscodium (Fresh clone 14.b, editor/README.md)." >&2
  exit 1
fi

if ! command -v stat >/dev/null 2>&1; then
  echo "print-vsbuild-codium-path: stat not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.f)." >&2
  exit 1
fi

best="${matches[0]}"
best_mtime=$(stat -c '%Y' "$best" 2>/dev/null || echo 0)
for p in "${matches[@]}"; do
  mt=$(stat -c '%Y' "$p" 2>/dev/null || echo 0)
  if [[ "$mt" -gt "$best_mtime" ]]; then
    best=$p
    best_mtime=$mt
  fi
done

if ! command -v realpath >/dev/null 2>&1; then
  echo "print-vsbuild-codium-path: realpath not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.f)." >&2
  exit 1
fi
realpath "$best"
