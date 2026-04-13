#!/usr/bin/env bash
# STEP 14 / §7.3 close-out verifier (maintainer): require the local artifacts that docs call "done":
#   - ci-editor-gate.sh passes (same as ./editor/smoke.sh fail-fast gates),
#   - editor/vscodium/VSCode-linux-*/bin/codium exists (14.c),
#   - packaging/le-vibe-ide_*.deb exists.
# Optional: also require stack le-vibe_*.deb (parent of clone, then repo root) via --require-stack-deb.
# When multiple matching artifacts exist, pick the newest version-like filename.
# Master orchestrator: 0 -> 1 -> 14 -> 2-13 -> 15-17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

REQUIRE_STACK_DEB=0
SKIP_GATE=0
ENABLE_APT_SIM=0
PRINT_JSON=0

log_note() {
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    printf '%s\n' "$*" >&2
  else
    printf '%s\n' "$*"
  fi
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\t'/\\t}"
  printf '%s' "$value"
}

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

assert_deb_file_contains() {
  local deb_path="$1"
  local internal_path="$2"
  local needle="$3"
  local content
  content="$(dpkg-deb --fsys-tarfile "$deb_path" | tar -xOf - "$internal_path" 2>/dev/null || true)"
  if [[ -z "$content" ]]; then
    echo "verify-step14-closeout: $deb_path missing payload file: $internal_path" >&2
    exit 1
  fi
  if ! grep -Fq "$needle" <<<"$content"; then
    echo "verify-step14-closeout: $deb_path payload $internal_path missing expected text: $needle" >&2
    exit 1
  fi
}

assert_deb_path_is_executable() {
  local deb_path="$1"
  local internal_path="$2"
  local line
  line="$(dpkg-deb --contents "$deb_path" | grep -F " $internal_path" || true)"
  if [[ -z "$line" ]]; then
    echo "verify-step14-closeout: $deb_path missing payload path: $internal_path" >&2
    exit 1
  fi
  # `dpkg-deb --contents` starts each line with file mode bits.
  # Launcher paths may be executable files (`-rwx...`) or symlinks (`lrwx...`).
  if [[ "${line:0:1}" != "-" && "${line:0:1}" != "l" ]]; then
    echo "verify-step14-closeout: $deb_path path is not an executable file/symlink: $internal_path ($line)" >&2
    exit 1
  fi
}

assert_apt_simulated_install() {
  local stack_deb="$1"
  local ide_deb="$2"
  local apt_output
  if ! command -v apt-get >/dev/null 2>&1; then
    echo "verify-step14-closeout: apt-get not found on PATH (cannot simulate install)." >&2
    exit 2
  fi
  if ! apt_output="$(apt-get -s install "$stack_deb" "$ide_deb" 2>&1)"; then
    echo "verify-step14-closeout: apt simulation failed for stack+IDE deb pair." >&2
    echo "verify-step14-closeout: apt-get -s output follows:" >&2
    printf '%s\n' "$apt_output" >&2
    echo "verify-step14-closeout: this usually indicates host apt state issues (held/broken packages), not .deb payload drift." >&2
    exit 1
  fi
}

usage() {
  cat <<'EOF'
Usage: packaging/scripts/verify-step14-closeout.sh [--require-stack-deb] [--apt-sim] [--skip-gate] [--json]

Checks local STEP 14 / §7.3 readiness:
  1) packaging/scripts/ci-editor-gate.sh (unless --skip-gate),
  2) editor/verify-14c-local-binary.sh (requires VSCode-linux-*/bin/codium),
  3) packaging/le-vibe-ide_*.deb exists and passes content checks:
     - launcher payload paths exist (`le-vibe.desktop`, `/usr/lib/le-vibe/bin/codium`),
     - desktop content contains `Name=Lé Vibe` and `Exec=/usr/lib/le-vibe/bin/codium %F`,
     - package metadata is `Package: le-vibe-ide`, `Architecture: amd64`.

Options:
  --require-stack-deb   Also require le-vibe_*.deb (search repo parent then repo root) and verify:
                        - `/usr/bin/lvibe` exists and is executable (or symlink),
                        - README.Debian(.gz) doc payload exists,
                        - metadata is `Package: le-vibe`, `Architecture: all`.
  --apt-sim             When used with --require-stack-deb, run:
                        `apt-get -s install <stack.deb> <ide.deb>`.
  --skip-gate           Skip ci-editor-gate.sh (faster local check).
  --json                Emit machine-readable summary JSON on success.
  -h, --help            Show this message and exit.

JSON success (--json) includes:
  status, codium_path, ide_deb, stack_deb_required, stack_deb (null when
  not required), apt_sim_requested, apt_sim_ran, apt_sim_note
  (not_requested | ran | requested_without_stack_requirement).

See also:
  - packaging/scripts/build-le-vibe-debs.sh --with-ide
  - docs/PM_DEB_BUILD_ITERATION.md
  - docs/apt-repo-releases.md (*IDE package*) — ordering: run this verifier on the
    build machine; copy .debs to a test host for sudo apt install + smoke
    (packaging/scripts/manual-step14-install-smoke.sh).
  - Partial VSCode-linux tree (missing VSCode-linux-*/bin/codium before this script
    reaches step 2): docs/PM_DEB_BUILD_ITERATION.md (*Partial VSCode-linux tree*),
    editor/BUILD.md (*Partial tree*, 14.c), editor/print-vsbuild-codium-path.sh,
    editor/print-built-codium-path.sh.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-stack-deb) REQUIRE_STACK_DEB=1 ;;
    --apt-sim) ENABLE_APT_SIM=1 ;;
    --skip-gate) SKIP_GATE=1 ;;
    --json) PRINT_JSON=1 ;;
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
  log_note "==> STEP 14 gate: ci-editor-gate.sh"
  "$ROOT/packaging/scripts/ci-editor-gate.sh"
else
  log_note "==> STEP 14 gate: skipped (--skip-gate)"
fi

log_note "==> STEP 14 built binary: verify-14c-local-binary.sh"
CODIUM_PATH="$("$ROOT/editor/verify-14c-local-binary.sh")"
log_note "    built codium: $CODIUM_PATH"

log_note "==> STEP 14 IDE package: packaging/le-vibe-ide_*.deb"
shopt -s nullglob
ide_debs=("$ROOT"/packaging/le-vibe-ide_*.deb)
if [[ ${#ide_debs[@]} -eq 0 ]]; then
  echo "verify-step14-closeout: missing packaging/le-vibe-ide_*.deb — run packaging/scripts/build-le-vibe-ide-deb.sh or build-le-vibe-debs.sh --with-ide." >&2
  exit 1
fi
ide_deb_latest="$(pick_latest_match "packaging/le-vibe-ide_*.deb" "${ide_debs[@]}")"
log_note "    ide deb: $ide_deb_latest"
log_note "    ide deb payload check: /usr/share/applications/le-vibe.desktop + /usr/lib/le-vibe/bin/codium"
assert_deb_contains "$ide_deb_latest" "./usr/share/applications/le-vibe.desktop"
assert_deb_contains "$ide_deb_latest" "./usr/lib/le-vibe/bin/codium"
assert_deb_path_is_executable "$ide_deb_latest" "./usr/lib/le-vibe/bin/codium"
log_note "    ide desktop check: Name=Lé Vibe + Exec=/usr/lib/le-vibe/bin/codium %F"
assert_deb_file_contains "$ide_deb_latest" "./usr/share/applications/le-vibe.desktop" "Name=Lé Vibe"
assert_deb_file_contains "$ide_deb_latest" "./usr/share/applications/le-vibe.desktop" "Exec=/usr/lib/le-vibe/bin/codium %F"
log_note "    ide deb metadata check: Package=le-vibe-ide, Architecture=amd64"
assert_deb_field_equals "$ide_deb_latest" "Package" "le-vibe-ide"
assert_deb_field_equals "$ide_deb_latest" "Architecture" "amd64"

if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
  log_note "==> Stack package: le-vibe_*.deb (required; resolve-latest-le-vibe-stack-deb.sh)"
  stack_deb_latest="$("$ROOT/packaging/scripts/resolve-latest-le-vibe-stack-deb.sh" "$ROOT")"
  if [[ -z "$stack_deb_latest" ]]; then
    echo "verify-step14-closeout: missing le-vibe_*.deb — dpkg-buildpackage emits ../le-vibe_*.deb beside the clone; or copy into repo root; run dpkg-buildpackage -us -uc -b (or build-le-vibe-debs.sh)." >&2
    exit 1
  fi
  log_note "    stack deb: $stack_deb_latest"
  log_note "    stack deb payload check: /usr/bin/lvibe + /usr/share/doc/le-vibe/README.Debian(.gz)"
  assert_deb_contains "$stack_deb_latest" "./usr/bin/lvibe"
  assert_deb_path_is_executable "$stack_deb_latest" "./usr/bin/lvibe"
  assert_deb_contains_any \
    "$stack_deb_latest" \
    "./usr/share/doc/le-vibe/README.Debian" \
    "./usr/share/doc/le-vibe/README.Debian.gz"
  log_note "    stack deb metadata check: Package=le-vibe, Architecture=all"
  assert_deb_field_equals "$stack_deb_latest" "Package" "le-vibe"
  assert_deb_field_equals "$stack_deb_latest" "Architecture" "all"
  if [[ "$ENABLE_APT_SIM" -eq 1 ]]; then
    log_note "    apt simulation check: apt-get -s install <stack.deb> <ide.deb>"
    assert_apt_simulated_install "$stack_deb_latest" "$ide_deb_latest"
  else
    log_note "    apt simulation check: skipped (use --apt-sim)"
  fi
fi

if [[ "$PRINT_JSON" -eq 1 ]]; then
  codium_json="$(json_escape "$CODIUM_PATH")"
  ide_json="$(json_escape "$ide_deb_latest")"
  stack_json=""
  apt_sim_note="not_requested"
  if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
    stack_json="$(json_escape "$stack_deb_latest")"
    if [[ "$ENABLE_APT_SIM" -eq 1 ]]; then
      apt_sim_note="ran"
    fi
  elif [[ "$ENABLE_APT_SIM" -eq 1 ]]; then
    apt_sim_note="requested_without_stack_requirement"
  fi
  printf '{\n'
  printf '  "status": "ok",\n'
  printf '  "codium_path": "%s",\n' "$codium_json"
  printf '  "ide_deb": "%s",\n' "$ide_json"
  printf '  "stack_deb_required": %s,\n' "$([[ "$REQUIRE_STACK_DEB" -eq 1 ]] && echo "true" || echo "false")"
  printf '  "stack_deb": %s,\n' "$([[ "$REQUIRE_STACK_DEB" -eq 1 ]] && printf '"%s"' "$stack_json" || echo "null")"
  printf '  "apt_sim_requested": %s,\n' "$([[ "$ENABLE_APT_SIM" -eq 1 ]] && echo "true" || echo "false")"
  printf '  "apt_sim_ran": %s,\n' "$([[ "$REQUIRE_STACK_DEB" -eq 1 && "$ENABLE_APT_SIM" -eq 1 ]] && echo "true" || echo "false")"
  printf '  "apt_sim_note": "%s"\n' "$apt_sim_note"
  printf '}\n'
else
  echo "verify-step14-closeout: OK (gate + built codium + ide deb${REQUIRE_STACK_DEB:+ + stack deb})."
fi
