#!/usr/bin/env bash
# STEP 14 / §7.3 — report all close-out gaps in one run (does not stop at first failure).
# Use before/after long compiles: see what is still missing for verify-step14-closeout.sh.
# Exit 0 only when every checked item passes; exit 1 if any required item fails.
#
# Pair with: packaging/scripts/verify-step14-closeout.sh [--require-stack-deb]
# Docs: docs/PM_DEB_BUILD_ITERATION.md, editor/BUILD.md (14.c)
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md
#
# After the 14.c check, prints vscode_linux_build: ready|partial|absent — packaging/scripts/probe-vscode-linux-build.sh
# (same classifier as lvibe ide-prereqs --json / verify-step14-closeout.sh --json).
# Optional --json: human lines go to stderr; one machine-readable JSON object on stdout (aligned with verify-step14-closeout.sh steps).
# Pytest contract: le-vibe/tests/test_preflight_step14_closeout_contract.py (JSON shape); verify-step14-closeout.sh — le-vibe/tests/test_verify_step14_closeout_contract.py; .gitignore: le-vibe/.pytest-verify-step14-contract.lock.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

REQUIRE_STACK_DEB=0
SKIP_GATE=0
PRINT_JSON=0

_pick_latest_valid_deb() {
  local label="$1"
  shift
  local matches=("$@")
  local sorted=()
  local cand
  mapfile -t sorted < <(printf '%s\n' "${matches[@]}" | sort -V)
  for (( idx=${#sorted[@]}-1; idx>=0; idx-- )); do
    cand="${sorted[$idx]}"
    if dpkg-deb --field "$cand" Package >/dev/null 2>&1; then
      printf '%s\n' "$cand"
      return 0
    fi
  done
  echo "[missing] no valid .deb archive for ${label} (found ${#sorted[@]} candidate file(s), all unreadable)" >&2
  return 1
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

# When --json: informational lines to stderr so stdout stays a single JSON object.
p_out() {
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    printf '%s\n' "$*" >&2
  else
    printf '%s\n' "$*"
  fi
}

usage() {
  cat <<'EOF'
Usage: packaging/scripts/preflight-step14-closeout.sh [--require-stack-deb] [--skip-gate] [--json]

Prints one line per check ([ok] / [missing]) then a summary. Exit 0 iff all checks pass.

  --require-stack-deb   Also require le-vibe_*.deb (resolve-latest-le-vibe-stack-deb.sh).
  --skip-gate           Skip ci-editor-gate.sh (faster when only checking artifacts).
  --json                Human-readable lines to stderr; one JSON summary on stdout (gate, codium,
                        ide_deb, hicolor_icon_in_deb, desktop_in_deb, stack_deb, vscode_linux_build, failures).

See packaging/scripts/verify-step14-closeout.sh for the strict single-pass verifier.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-stack-deb) REQUIRE_STACK_DEB=1 ;;
    --skip-gate) SKIP_GATE=1 ;;
    --json) PRINT_JSON=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "preflight-step14-closeout: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

failures=0
GATE_STATE="ok"
CODIUM_STATE="ok"
IDE_STATE="ok"
HICON_STATE="none"
DESKTOP_STATE="skipped"
STACK_STATE="not_required"

if [[ "$SKIP_GATE" -eq 1 ]]; then
  GATE_STATE="skipped"
  p_out "[skip] ci-editor-gate.sh (--skip-gate)"
else
  if "$ROOT/packaging/scripts/ci-editor-gate.sh" >/dev/null 2>&1; then
    p_out "[ok] ci-editor-gate.sh"
  else
    echo "[missing] ci-editor-gate.sh — run packaging/scripts/ci-editor-gate.sh for details" >&2
    GATE_STATE="missing"
    failures=$((failures + 1))
  fi
fi

set +e
# Capture verify-14c combined output; on failure relay it (partial VSCode-linux tree vs no tree).
_codium_out="$("$ROOT/editor/verify-14c-local-binary.sh" 2>&1)"
_codium_ec=$?
set -e
if [[ "${_codium_ec}" -eq 0 ]]; then
  p_out "[ok] editor/vscodium VSCode-linux-*/bin/codium (${_codium_out})"
else
  if [[ -n "${_codium_out}" ]]; then
    printf '%s\n' "${_codium_out}" >&2
  fi
  echo "[missing] VSCode-linux-*/bin/codium (14.c) — cd editor/vscodium && ./dev/build.sh (editor/BUILD.md *Partial tree* / 14.c)" >&2
  CODIUM_STATE="missing"
  failures=$((failures + 1))
fi

_vlb="$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT")"
p_out "vscode_linux_build: ${_vlb}"
_vbf=""
if [[ "${_vlb}" == "partial" ]]; then
  _vbf="$("$ROOT/packaging/scripts/print-step14-vscode-linux-bin-files.sh" "$ROOT")"
  p_out "vscode_linux_bin_files: ${_vbf}"
fi
if [[ "${_vlb}" != "ready" ]]; then
  echo "hint: packaging/scripts/build-le-vibe-debs.sh --with-ide exits before stack dpkg-buildpackage until vscode_linux_build is ready (or use --vs-build PATH with bin/codium) — docs/PM_DEB_BUILD_ITERATION.md (Failure (--with-ide))" >&2
  if [[ "${_vlb}" == "partial" ]]; then
    echo "hint: partial tree — CI tarball (linux_compile): ./packaging/scripts/print-github-linux-compile-artifact-hint.sh (browser or gh); ./packaging/scripts/trigger-le-vibe-ide-linux-compile.sh; ./packaging/scripts/download-vscodium-linux-compile-artifact.sh --install; then ./packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes (editor/BUILD.md 14.f) or finish cd editor/vscodium && ./dev/build.sh (14.c)" >&2
  fi
fi

shopt -s nullglob
ide_debs=("$ROOT"/packaging/le-vibe-ide_*.deb)
if [[ ${#ide_debs[@]} -gt 0 ]]; then
  if ! _ide_deb="$(_pick_latest_valid_deb "packaging/le-vibe-ide_*.deb" "${ide_debs[@]}")"; then
    IDE_STATE="missing"
    failures=$((failures + 1))
    DESKTOP_STATE="none"
    _ide_deb=""
  fi
fi
if [[ -n "${_ide_deb:-}" ]]; then
  p_out "[ok] packaging/le-vibe-ide_*.deb ($_ide_deb)"
  # Same payload path as verify-step14-closeout.sh (§7.3 Freedesktop icon).
  _hicon_listed="./usr/share/icons/hicolor/scalable/apps/le-vibe.svg"
  if dpkg-deb --contents "$_ide_deb" 2>/dev/null | grep -Fq "$_hicon_listed"; then
    p_out "[ok] ide .deb lists ${_hicon_listed} (hicolor — §7.3)"
    HICON_STATE="ok"
  else
    echo "[missing] ${_hicon_listed} not in dpkg-deb --contents of ${_ide_deb} — rebuild IDE .deb (packaging/debian-le-vibe-ide/debian/le-vibe-ide.install)" >&2
    HICON_STATE="missing"
    failures=$((failures + 1))
  fi
  # §7.3: only lvibe is public PATH CLI from the stack package, not the IDE .deb.
  _forbidden_public_cli=(
    "./usr/bin/lvibe"
    "./usr/bin/le-vibe"
    "./usr/bin/le-vibe-ide"
    "./usr/bin/codium"
  )
  _forbidden_hit=""
  for _forbidden in "${_forbidden_public_cli[@]}"; do
    if dpkg-deb --contents "$_ide_deb" 2>/dev/null | grep -Fq "$_forbidden"; then
      _forbidden_hit="$_forbidden"
      break
    fi
  done
  if [[ -z "$_forbidden_hit" ]]; then
    p_out "[ok] ide .deb exports no public PATH CLI payload (/usr/bin/*)"
  else
    echo "[missing] IDE .deb unexpectedly exposes public CLI path ${_forbidden_hit} — keep PATH command in stack package (`/usr/bin/lvibe`) only" >&2
    IDE_STATE="missing"
    failures=$((failures + 1))
  fi
  # Freedesktop QA on packaged le-vibe.desktop (same extraction as build-le-vibe-ide-deb.sh post-build).
  if command -v desktop-file-validate >/dev/null 2>&1; then
    _desk_tmp="$(mktemp "${TMPDIR:-/tmp}/le-vibe-desk-XXXXXXXX.desktop")"
    _ok=0
    if dpkg-deb --fsys-tarfile "$_ide_deb" | tar -xOf - "usr/share/applications/le-vibe.desktop" > "$_desk_tmp" 2>/dev/null && [[ -s "$_desk_tmp" ]]; then
      _ok=1
    elif dpkg-deb --fsys-tarfile "$_ide_deb" | tar -xOf - "./usr/share/applications/le-vibe.desktop" > "$_desk_tmp" 2>/dev/null && [[ -s "$_desk_tmp" ]]; then
      _ok=1
    fi
    if [[ "$_ok" -eq 1 ]]; then
      if desktop-file-validate "$_desk_tmp" >/dev/null 2>&1; then
        DESKTOP_STATE="ok"
        p_out "[ok] desktop-file-validate (le-vibe.desktop inside ${_ide_deb})"
      else
        desktop-file-validate "$_desk_tmp" >&2 || true
        echo "[missing] desktop-file-validate failed on le-vibe.desktop extracted from ${_ide_deb}" >&2
        DESKTOP_STATE="missing"
        failures=$((failures + 1))
      fi
    else
      echo "[missing] could not extract usr/share/applications/le-vibe.desktop from ${_ide_deb} for desktop-file-validate" >&2
      DESKTOP_STATE="missing"
      failures=$((failures + 1))
    fi
    rm -f "$_desk_tmp"
  else
    DESKTOP_STATE="skipped"
    p_out "[optional] desktop-file-validate not on PATH — skipped packaged .desktop check (install desktop-file-utils; build-le-vibe-ide-deb.sh runs this after dpkg-buildpackage)"
  fi
else
  echo "[missing] packaging/le-vibe-ide_*.deb — packaging/scripts/build-le-vibe-ide-deb.sh or build-le-vibe-debs.sh --with-ide" >&2
  IDE_STATE="missing"
  failures=$((failures + 1))
  DESKTOP_STATE="none"
fi

if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
  _stack="$("$ROOT/packaging/scripts/resolve-latest-le-vibe-stack-deb.sh" "$ROOT" || true)"
  if [[ -n "$_stack" && -f "$_stack" ]]; then
    STACK_STATE="ok"
    p_out "[ok] le-vibe_*.deb stack package ($_stack)"
  else
    echo "[missing] le-vibe_*.deb — dpkg-buildpackage at repo root or build-le-vibe-debs.sh (resolve-latest-le-vibe-stack-deb.sh)" >&2
    STACK_STATE="missing"
    failures=$((failures + 1))
  fi
else
  p_out "[optional] stack le-vibe_*.deb not required (omit --require-stack-deb for full-product gate)"
fi

_status="ok"
if [[ "$failures" -gt 0 ]]; then
  _status="error"
fi

if [[ "$PRINT_JSON" -eq 1 ]]; then
  _vj="$(json_escape "$_vlb")"
  if [[ "${_vlb}" == "partial" ]]; then
    _bj="$(json_escape "${_vbf:-}")"
    _bf_json="$(printf '"vscode_linux_bin_files":"%s"' "$_bj")"
  else
    _bf_json='"vscode_linux_bin_files":null'
  fi
  printf '{"status":"%s","failures":%d,"gate":"%s","codium":"%s","ide_deb":"%s","hicolor_icon_in_deb":"%s","desktop_in_deb":"%s","stack_deb":"%s","vscode_linux_build":"%s",%s}\n' \
    "$_status" "$failures" "$GATE_STATE" "$CODIUM_STATE" "$IDE_STATE" "$HICON_STATE" "$DESKTOP_STATE" "$STACK_STATE" "$_vj" "$_bf_json"
fi

if [[ "$failures" -eq 0 ]]; then
  p_out "preflight-step14-closeout: all checked items OK — run verify-step14-closeout.sh${REQUIRE_STACK_DEB:+ --require-stack-deb} for strict gate."
  exit 0
fi

echo "preflight-step14-closeout: $failures check(s) failed — fix items above, then re-run." >&2
exit 1
