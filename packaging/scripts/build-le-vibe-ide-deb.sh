#!/usr/bin/env bash
# Build le-vibe-ide_*.deb after stage-le-vibe-ide-deb.sh (PRODUCT_SPEC §7.3).
# Requires: dpkg-buildpackage (dpkg-dev) on PATH after staging.
# Optional: lintian on the produced .deb if installed — packaging/debian-le-vibe-ide/README.md;
#   non-fatal unless LEVIBE_IDE_LINTIAN_STRICT=1 (exit code from lintian).
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
dpkg-buildpackage -us -uc -b

_latest="$(ls -t "$ROOT/packaging"/le-vibe-ide_*.deb 2>/dev/null | head -1 || true)"
if [[ -z "${_latest:-}" ]]; then
  echo "build-le-vibe-ide-deb: expected packaging/le-vibe-ide_*.deb after dpkg-buildpackage — check build log." >&2
  exit 1
fi
if command -v lintian >/dev/null 2>&1; then
  echo "build-le-vibe-ide-deb: lintian ${_latest}" >&2
  set +e
  lintian "${_latest}"
  _lio=$?
  set -e
  if [[ "${_lio}" -ne 0 ]]; then
    echo "build-le-vibe-ide-deb: lintian exited ${_lio} — see docs/ci-qa-hardening.md; set LEVIBE_IDE_LINTIAN_STRICT=1 to fail the script on lintian." >&2
    [[ "${LEVIBE_IDE_LINTIAN_STRICT:-}" == "1" ]] && exit "${_lio}"
  fi
else
  echo "build-le-vibe-ide-deb: lintian not on PATH — skipped (optional QA per packaging/debian-le-vibe-ide/README.md)." >&2
fi
