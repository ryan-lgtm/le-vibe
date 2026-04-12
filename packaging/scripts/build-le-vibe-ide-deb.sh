#!/usr/bin/env bash
# Build le-vibe-ide_*.deb after stage-le-vibe-ide-deb.sh (PRODUCT_SPEC §7.3).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
"$ROOT/packaging/scripts/stage-le-vibe-ide-deb.sh" "$@"
cd "$ROOT/packaging/debian-le-vibe-ide"
exec dpkg-buildpackage -us -uc -b
