#!/usr/bin/env bash
# STEP 14 (14.f): print absolute path to VSCode-linux-*/bin/codium under a directory tree.
# Use after unpacking vscodium-linux-build.tar.gz from linux_compile, or any tree that contains VSCode-linux-*.
# Usage: ./editor/print-vsbuild-codium-path.sh [SEARCH_ROOT]
#   SEARCH_ROOT defaults to the current working directory (typical: cd to unpack dir, then run from repo with ../../editor/... or pass the unpack path).
# Example (artifact in /tmp/vs):
#   ./editor/print-vsbuild-codium-path.sh /tmp/vs
set -euo pipefail

SEARCH="${1:-.}"
SEARCH="$(cd "$SEARCH" && pwd)"

shopt -s nullglob
matches=("${SEARCH}"/VSCode-linux-*/bin/codium)

if [[ ${#matches[@]} -eq 0 ]]; then
  echo "print-vsbuild-codium-path: no VSCode-linux-*/bin/codium under ${SEARCH} — extract vscodium-linux-build.tar.gz or point at editor/vscodium after dev/build.sh (editor/BUILD.md 14.f)." >&2
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

realpath "$best"
