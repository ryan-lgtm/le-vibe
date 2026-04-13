#!/usr/bin/env bash
# STEP 14 / §7.3 close-out verifier (maintainer): require the local artifacts that docs call "done":
#   - ci-editor-gate.sh passes (same as ./editor/smoke.sh fail-fast gates),
#   - editor/vscodium/VSCode-linux-*/bin/codium exists (14.c),
#   - packaging/le-vibe-ide_*.deb exists.
# Optional: also require stack ../le-vibe_*.deb via --require-stack-deb.
# When multiple matching artifacts exist, pick the newest version-like filename.
# Master orchestrator: 0 -> 1 -> 14 -> 2-13 -> 15-17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

REQUIRE_STACK_DEB=0
SKIP_GATE=0

pick_latest_match() {
  local label="$1"
  shift
  local matches=("$@")
  if [[ ${#matches[@]} -eq 0 ]]; then
    echo "verify-step14-closeout: internal error: no matches for $label" >&2
    exit 1
  fi
  local sorted=()
  mapfile -t sorted < <(printf '%s\n' "${matches[@]}" | sort -V)
  local idx=$(( ${#sorted[@]} - 1 ))
  printf '%s\n' "${sorted[$idx]}"
}

assert_deb_contains() {
  local deb_path="$1"
  local needle="$2"
  local contents
  contents="$(dpkg-deb --contents "$deb_path")"
  if ! grep -Fq "$needle" <<<"$contents"; then
    echo "verify-step14-closeout: $deb_path missing expected payload entry: $needle" >&2
    exit 1
  fi
}

assert_deb_contains_any() {
  local deb_path="$1"
  shift
  local contents
  contents="$(dpkg-deb --contents "$deb_path")"
  local needle
  for needle in "$@"; do
    if grep -Fq "$needle" <<<"$contents"; then
      return 0
    fi
  done
  echo "verify-step14-closeout: $deb_path missing expected payload entries (any of): $*" >&2
  exit 1
}

assert_deb_field_equals() {
  local deb_path="$1"
  local field="$2"
  local expected="$3"
  local actual
  actual="$(dpkg-deb --field "$deb_path" "$field" | tr -d '\r')"
  if [[ "$actual" != "$expected" ]]; then
    echo "verify-step14-closeout: $deb_path field $field expected '$expected' but got '$actual'" >&2
    exit 1
  fi
}

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
ide_deb_latest="$(pick_latest_match "packaging/le-vibe-ide_*.deb" "${ide_debs[@]}")"
echo "    ide deb: $ide_deb_latest"
echo "    ide deb payload check: /usr/share/applications/le-vibe.desktop + /usr/lib/le-vibe/bin/codium"
assert_deb_contains "$ide_deb_latest" "./usr/share/applications/le-vibe.desktop"
assert_deb_contains "$ide_deb_latest" "./usr/lib/le-vibe/bin/codium"
echo "    ide deb metadata check: Package=le-vibe-ide, Architecture=amd64"
assert_deb_field_equals "$ide_deb_latest" "Package" "le-vibe-ide"
assert_deb_field_equals "$ide_deb_latest" "Architecture" "amd64"

if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
  echo "==> Stack package: ../le-vibe_*.deb (required)"
  stack_debs=("$ROOT"/../le-vibe_*.deb)
  if [[ ${#stack_debs[@]} -eq 0 ]]; then
    echo "verify-step14-closeout: missing ../le-vibe_*.deb — run dpkg-buildpackage -us -uc -b (or build-le-vibe-debs.sh)." >&2
    exit 1
  fi
  stack_deb_latest="$(pick_latest_match "../le-vibe_*.deb" "${stack_debs[@]}")"
  echo "    stack deb: $stack_deb_latest"
  echo "    stack deb payload check: /usr/bin/lvibe + /usr/share/doc/le-vibe/README.Debian(.gz)"
  assert_deb_contains "$stack_deb_latest" "./usr/bin/lvibe"
  assert_deb_contains_any \
    "$stack_deb_latest" \
    "./usr/share/doc/le-vibe/README.Debian" \
    "./usr/share/doc/le-vibe/README.Debian.gz"
  echo "    stack deb metadata check: Package=le-vibe, Architecture=all"
  assert_deb_field_equals "$stack_deb_latest" "Package" "le-vibe"
  assert_deb_field_equals "$stack_deb_latest" "Architecture" "all"
fi

echo "verify-step14-closeout: OK (gate + built codium + ide deb${REQUIRE_STACK_DEB:+ + stack deb})."
