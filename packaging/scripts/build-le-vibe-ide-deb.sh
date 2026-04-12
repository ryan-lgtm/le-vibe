#!/usr/bin/env bash
# Build le-vibe-ide_*.deb after stage-le-vibe-ide-deb.sh (PRODUCT_SPEC §7.3).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md; VSCode-linux-* must exist (see stage-le-vibe-ide-deb.sh errors).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
"$ROOT/packaging/scripts/stage-le-vibe-ide-deb.sh" "$@"
cd "$ROOT/packaging/debian-le-vibe-ide"
exec dpkg-buildpackage -us -uc -b
