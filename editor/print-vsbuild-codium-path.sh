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
# Pytest: le-vibe/tests/test_editor_smoke_sh_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: editor/print-vsbuild-codium-path.sh [SEARCH_ROOT]

Print absolute path to VSCode-linux-*/bin/codium under SEARCH_ROOT (default: .).
SEARCH_ROOT may be editor/vscodium, an unpacked linux_compile tarball tree, or any
directory containing VSCode-linux-* (STEP 14 — editor/BUILD.md 14.f / 14.c).

  -h, --help   Show this message and exit.

Exits 1 if no matching codium binary exists (partial build — see editor/BUILD.md *Partial tree*).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

SEARCH="${1:-.}"
if [[ ! -d "$SEARCH" ]]; then
  echo "print-vsbuild-codium-path: not a directory: $SEARCH — pass a path to an unpacked VSCode-linux-* tree or editor/vscodium (editor/BUILD.md 14.f / 14.c)." >&2
  exit 1
fi
SEARCH="$(cd "$SEARCH" && pwd)"

shopt -s nullglob
matches=("${SEARCH}"/VSCode-linux-*/bin/codium)

if [[ ${#matches[@]} -eq 0 ]]; then
  for treeroot in "${SEARCH}"/VSCode-linux-*/; do
    [[ -d "$treeroot" ]] || continue
    bindir="${treeroot}bin"
    if [[ -d "$bindir" ]] && [[ ! -e "$bindir/codium" ]]; then
      listing=""
      if command -v ls >/dev/null 2>&1; then
        listing="$(ls -1 "$bindir" 2>/dev/null | tr '\n' ' ')"
      fi
      echo "print-vsbuild-codium-path: ${treeroot} has bin/ but bin/codium is missing (partial or incomplete build)." >&2
      if [[ -n "$listing" ]]; then
        echo "print-vsbuild-codium-path: ${bindir} contains: ${listing}" >&2
      fi
      echo "print-vsbuild-codium-path: rerun: cd editor/vscodium && ./dev/build.sh (editor/BUILD.md 14.c), or unpack a full vscodium-linux-build.tar.gz artifact (14.f)." >&2
      echo "print-vsbuild-codium-path: CI tarball (browser or gh): packaging/scripts/print-github-linux-compile-artifact-hint.sh" >&2
      echo "print-vsbuild-codium-path: maintainer CI: packaging/scripts/trigger-le-vibe-ide-linux-compile.sh; packaging/scripts/download-vscodium-linux-compile-artifact.sh --install" >&2
      echo "print-vsbuild-codium-path: monorepo: packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes (replaces partial VSCode-linux-* under editor/vscodium/)" >&2
      exit 1
    fi
  done
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
