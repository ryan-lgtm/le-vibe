#!/usr/bin/env bash
# Build le-vibe-ide_*.deb after stage-le-vibe-ide-deb.sh (PRODUCT_SPEC §7.3).
# Requires: dpkg-buildpackage (dpkg-dev) on PATH after staging.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md; VSCode-linux-* must exist (see stage-le-vibe-ide-deb.sh errors).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
"$ROOT/packaging/scripts/stage-le-vibe-ide-deb.sh" "$@"
if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
  echo "build-le-vibe-ide-deb: dpkg-buildpackage not on PATH — install dpkg-dev (e.g. sudo apt install dpkg-dev build-essential) (§7.3 IDE .deb)." >&2
  exit 1
fi
cd "$ROOT/packaging/debian-le-vibe-ide"
exec dpkg-buildpackage -us -uc -b
