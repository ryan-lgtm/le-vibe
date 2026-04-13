#!/usr/bin/env bash
# STEP 14 / §7.3 close-out verifier (maintainer): require the local artifacts that docs call "done":
#   - ci-editor-gate.sh passes (same as ./editor/smoke.sh fail-fast gates),
#   - editor/vscodium/VSCode-linux-*/bin/codium exists (14.c),
#   - packaging/le-vibe-ide_*.deb exists.
# Optional: also require stack ../le-vibe_*.deb via --require-stack-deb.
# Master orchestrator: 0 -> 1 -> 14 -> 2-13 -> 15-17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

REQUIRE_STACK_DEB=0
SKIP_GATE=0

usage() {
  cat <<'EOF'
Usage: packaging/scripts/verify-step14-closeout.sh [--require-stack-deb] [--skip-gate]

Checks local STEP 14 / §7.3 readiness:
  1) packaging/scripts/ci-editor-gate.sh (unless --skip-gate),
  2) editor/verify-14c-local-binary.sh (requires VSCode-linux-*/bin/codium),
  3) packaging/le-vibe-ide_*.deb exists.

Options:
  --require-stack-deb   Also require ../le-vibe_*.deb to exist.
  --skip-gate           Skip ci-editor-gate.sh (faster local check).
  -h, --help            Show this message and exit.

See also:
  - packaging/scripts/build-le-vibe-debs.sh --with-ide
  - docs/PM_DEB_BUILD_ITERATION.md
  - docs/apt-repo-releases.md
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-stack-deb) REQUIRE_STACK_DEB=1 ;;
    --skip-gate) SKIP_GATE=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "verify-step14-closeout: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ "$SKIP_GATE" -eq 0 ]]; then
  echo "==> STEP 14 gate: ci-editor-gate.sh"
  "$ROOT/packaging/scripts/ci-editor-gate.sh"
else
  echo "==> STEP 14 gate: skipped (--skip-gate)"
fi

echo "==> STEP 14 built binary: verify-14c-local-binary.sh"
CODIUM_PATH="$("$ROOT/editor/verify-14c-local-binary.sh")"
echo "    built codium: $CODIUM_PATH"

echo "==> STEP 14 IDE package: packaging/le-vibe-ide_*.deb"
shopt -s nullglob
ide_debs=("$ROOT"/packaging/le-vibe-ide_*.deb)
if [[ ${#ide_debs[@]} -eq 0 ]]; then
  echo "verify-step14-closeout: missing packaging/le-vibe-ide_*.deb — run packaging/scripts/build-le-vibe-ide-deb.sh or build-le-vibe-debs.sh --with-ide." >&2
  exit 1
fi
echo "    ide deb: ${ide_debs[0]}"

if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
  echo "==> Stack package: ../le-vibe_*.deb (required)"
  stack_debs=("$ROOT"/../le-vibe_*.deb)
  if [[ ${#stack_debs[@]} -eq 0 ]]; then
    echo "verify-step14-closeout: missing ../le-vibe_*.deb — run dpkg-buildpackage -us -uc -b (or build-le-vibe-debs.sh)." >&2
    exit 1
  fi
  echo "    stack deb: ${stack_debs[0]}"
fi

echo "verify-step14-closeout: OK (gate + built codium + ide deb${REQUIRE_STACK_DEB:+ + stack deb})."
