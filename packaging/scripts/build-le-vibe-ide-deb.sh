#!/usr/bin/env bash
# Build le-vibe-ide_*.deb after stage-le-vibe-ide-deb.sh (PRODUCT_SPEC §7.3).
# H1 / §7.3: not included in default ci.yml le-vibe-deb upload (stack-only); publish beside stack .deb — docs/apt-repo-releases.md (IDE package); stack + IDE — packaging/scripts/build-le-vibe-debs.sh --with-ide.
# Full-product (stack + IDE): build-le-vibe-debs.sh --with-ide prints Full-product install on success — docs/PM_DEB_BUILD_ITERATION.md (Success output (--with-ide)); this script builds the IDE .deb only.
# Requires: dpkg-buildpackage (dpkg-dev) on PATH after staging.
# Optional: lintian on the produced .deb if installed — packaging/debian-le-vibe-ide/README.md;
#   non-fatal unless LEVIBE_IDE_LINTIAN_STRICT=1 (exit code from lintian).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md; VSCode-linux-* must exist (see stage-le-vibe-ide-deb.sh errors).
# Staging env (passed through to stage-le-vibe-ide-deb.sh): LEVIBE_STAGE_IDE_ASSERT_BRAND, LEVIBE_STAGE_IDE_VERBOSE — §7.3 product.json identity.
# Optional: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 runs ci-editor-gate.sh before staging (same §7.3 check as build-le-vibe-debs.sh --with-ide).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 le-vibe-ide .deb build after STEP 0–1.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/build-le-vibe-ide-deb.sh [PATH]

  PATH   Optional path to editor/vscodium/VSCode-linux-* (default: discover under editor/vscodium/).

Builds packaging/le-vibe-ide_*.deb via stage-le-vibe-ide-deb.sh + dpkg-buildpackage.
See packaging/debian-le-vibe-ide/README.md and docs/PM_DEB_BUILD_ITERATION.md.

Partial VSCode-linux tree (missing VSCode-linux-* or bin/codium before staging succeeds):
  docs/PM_DEB_BUILD_ITERATION.md (*Partial VSCode-linux tree*), editor/BUILD.md (Partial tree, 14.c),
  ./editor/print-built-codium-path.sh, ./editor/print-vsbuild-codium-path.sh.
After both .debs exist on the build machine: packaging/scripts/verify-step14-closeout.sh --require-stack-deb.

Environment:
  LEVIBE_EDITOR_GATE_ASSERT_BRAND   When 1, run ci-editor-gate.sh before staging (§7.3 product.json).
  LEVIBE_STAGE_IDE_ASSERT_BRAND     Fail staging if product.json lacks Lé Vibe (stage-le-vibe-ide-deb.sh).
  LEVIBE_STAGE_IDE_VERBOSE          Print when §7.3 identity check passes (staging script).
  LEVIBE_IDE_LINTIAN_STRICT         When 1, fail the script if lintian fails after build.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "${LEVIBE_EDITOR_GATE_ASSERT_BRAND:-0}" == "1" ]]; then
  echo "build-le-vibe-ide-deb: §7.3 pre-check: ci-editor-gate.sh (LEVIBE_EDITOR_GATE_ASSERT_BRAND=1)"
  LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 "$ROOT/packaging/scripts/ci-editor-gate.sh"
fi
"$ROOT/packaging/scripts/stage-le-vibe-ide-deb.sh" "$@"
if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
  echo "build-le-vibe-ide-deb: dpkg-buildpackage not on PATH — install dpkg-dev (e.g. sudo apt install dpkg-dev build-essential) (§7.3 IDE .deb)." >&2
  exit 1
fi
cd "$ROOT/packaging/debian-le-vibe-ide"
dpkg-buildpackage -us -uc -b

_latest="$(ls -t "$ROOT/packaging"/le-vibe-ide_*.deb 2>/dev/null | head -1 || true)"
if [[ -z "${_latest:-}" ]]; then
  echo "build-le-vibe-ide-deb: expected packaging/le-vibe-ide_*.deb after dpkg-buildpackage — check build log. CI vs maintainer bundles: docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles); packaging/debian-le-vibe-ide/README.md." >&2
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
    if [[ "${LEVIBE_IDE_LINTIAN_STRICT:-}" == "1" ]]; then
      exit "${_lio}"
    fi
  fi
else
  echo "build-le-vibe-ide-deb: lintian not on PATH — skipped (optional QA per packaging/debian-le-vibe-ide/README.md)." >&2
fi
