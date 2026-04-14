#!/usr/bin/env bash
# Canonical local end-to-end path: prerequisites → (optional) compile fail-fast → VSCode-linux + bin/codium
# → stack + IDE .deb → STEP 14 close-out verify → optional apt install → post-install smoke.
# Does not use apt repository hosting — only local dpkg-buildpackage artifacts + sudo apt install .deb files.
# Authority: docs/PM_DEB_BUILD_ITERATION.md, editor/BUILD.md, packaging/debian-le-vibe-ide/README.md
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md; docs/PM_STAGE_MAP.md
# Pytest: le-vibe/tests/test_install_le_vibe_local_script_contract.py — verify JSON stubs:
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

DO_INSTALL=0
ASSUME_YES=0
FORCE_EDITOR_BUILD=0
SKIP_EDITOR_BUILD=0
SKIP_COMPILE_FAILFAST=0
PRINT_JSON=0
ENABLE_APT_SIM=0
SKIP_VERIFY_GATE=0
LOG_FILE=""
PREFLIGHT_ONLY=0

usage() {
  cat <<'EOF'
Usage: packaging/scripts/install-le-vibe-local.sh [options]

From a monorepo clone on a supported Linux host, orchestrate the full maintainer path:
  1) Prerequisites (Linux, editor/vscodium checkout, stack .deb build tools)
  2) Optional compile fail-fast (same ordering as linux_compile / editor/BUILD.md *CI*)
  3) Full VSCodium linux compile via ci-vscodium-linux-dev-build.sh → dev/build.sh
     (skipped when VSCode-linux-*/bin/codium already exists — resume-friendly; use --force-editor-build
     to always compile)
  4) packaging/scripts/build-le-vibe-debs.sh --with-ide
  5) packaging/scripts/verify-step14-closeout.sh --require-stack-deb
  6) With --install: sudo apt install both .deb files (stack first, then IDE — same as build-le-vibe-debs.sh)
  7) After install: packaging/scripts/manual-step14-install-smoke.sh --verify-only

Resolves the repository root from this script’s path (your cwd may be anywhere).

Options:
  --install          After building .deb files, run sudo apt install on both (requires sudo, apt-get).
  --yes              Non-interactive apt (passes -y to apt-get install).
  --force-editor-build   Always run ci-vscodium-linux-dev-build.sh even if bin/codium already exists.
  --skip-editor-build    Never compile; require editor/vscodium/VSCode-linux-*/bin/codium (14.c) already.
  --skip-compile-failfast
                     Skip ci-vscodium-bash-syntax.sh + ci-editor-nvmrc-sync.sh before the long compile.
  --apt-sim          Pass --apt-sim to verify-step14-closeout.sh (with --require-stack-deb).
  --skip-gate        Pass --skip-gate to verify-step14-closeout.sh (faster; skips ci-editor-gate.sh).
  --json             On success, print one JSON object to stdout with paths and pass/fail flags.
                     Human progress remains on stderr unless stdout is only JSON (errors still on stderr).
  --log-file PATH    Append a timestamped transcript to PATH (mkdir -p parent when possible).
  --preflight-only   Check prerequisites and print host/resource/editor-dep milestones only (no compile,
                     no .deb build, no apt install). Exits 0 when Linux + submodule + stack packaging tools +
                     VSCodium host deps pass; exits 2 if deps are missing. Combine with --json for machine-readable
                     summary. Incompatible with --install and other build/verify flags.
  -h, --help         Show this message and exit.

Environment (inherited by child scripts where applicable):
  DEB_BUILD_OPTIONS              e.g. parallel=$(nproc) for faster stack dpkg-buildpackage
  LEVIBE_SKIP_NODE_VERSION_CHECK Passed to ci-vscodium-linux-dev-build.sh
  LEVIBE_SKIP_HOST_DEPS_CHECK    Passed to ci-vscodium-linux-dev-build.sh
  LEVIBE_EDITOR_GATE_ASSERT_BRAND  Passed through build-le-vibe-debs.sh --with-ide
  LEVIBE_STAGE_IDE_ASSERT_BRAND, LEVIBE_STAGE_IDE_VERBOSE, LEVIBE_IDE_LINTIAN_STRICT — IDE staging/build
  LEVIBE_LOCAL_SKIP_COMPILE_FAILFAST=1  Same as --skip-compile-failfast

Exit codes:
  0  All requested steps succeeded.
  1  Build, verify, install, or smoke step failed.
  2  Unsupported OS, missing prerequisite tools, or invalid CLI.

Canonical full-product non-interactive install (build + sudo install + smoke):
  packaging/scripts/install-le-vibe-local.sh --install --yes

Build artifacts only (no sudo):
  packaging/scripts/install-le-vibe-local.sh

Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md

See also:
  packaging/scripts/build-le-vibe-debs.sh --help
  packaging/scripts/ci-vscodium-linux-dev-build.sh --help
  packaging/scripts/verify-step14-closeout.sh --help
  docs/PM_DEB_BUILD_ITERATION.md
  docs/LOCAL_INSTALL_ONE_SHOT.md
EOF
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\t'/\\t}"
  printf '%s' "$value"
}

log_human() {
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    printf '%s\n' "$*" >&2
  else
    printf '%s\n' "$*"
  fi
}

log_tee() {
  if [[ -n "$LOG_FILE" ]]; then
    printf '%s\n' "$*" | tee -a "$LOG_FILE" >&2
  else
    log_human "$*"
  fi
}

require_linux() {
  if [[ "$(uname -s)" != "Linux" ]]; then
    echo "install-le-vibe-local: this orchestrator supports Linux hosts only (uname: $(uname -s))." >&2
    echo "  For other platforms see editor/BUILD.md and docs/PM_DEB_BUILD_ITERATION.md." >&2
    exit 2
  fi
}

require_submodule() {
  if [[ ! -f "$ROOT/editor/vscodium/product.json" ]]; then
    echo "install-le-vibe-local: missing editor/vscodium/product.json — initialize the submodule:" >&2
    echo "  git submodule update --init editor/vscodium   # Fresh clone (14.b) — editor/README.md" >&2
    exit 2
  fi
}

warn_if_vscodium_submodule_dirty() {
  local sub="$ROOT/editor/vscodium"
  local dirty=""
  if [[ ! -e "$sub/.git" ]]; then
    return 0
  fi
  dirty="$(git -C "$sub" status --porcelain 2>/dev/null || true)"
  if [[ -n "$dirty" ]]; then
    log_tee "==> VSCodium submodule state: DIRTY (non-blocking warning)"
    log_tee "    editor/vscodium has local modifications. Builds may be non-reproducible."
    log_tee "    Before a release-quality run, clean/reset the submodule to its pinned commit."
  else
    log_tee "==> VSCodium submodule state: clean"
  fi
}

require_stack_packaging_tools() {
  local missing=()
  if ! have_cmd dpkg-buildpackage; then missing+=("dpkg-dev"); fi
  if ! have_cmd dh; then missing+=("debhelper"); fi
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "install-le-vibe-local: missing packages for .deb builds: ${missing[*]}" >&2
    echo "  Install: sudo apt install -y build-essential debhelper dpkg-dev" >&2
    exit 2
  fi
  if ! have_cmd find || ! have_cmd sort || ! have_cmd head; then
    echo "install-le-vibe-local: find, sort, and head are required (findutils, coreutils)." >&2
    exit 2
  fi
}

emit_final_json() {
  local status="$1"
  local step="$2"
  local msg="$3"
  local vlb="${4:-}"
  local codium="${5:-}"
  local stack_deb="${6:-}"
  local ide_deb="${7:-}"
  local verify_ok="${8:-false}"
  local install_done="${9:-false}"
  local smoke_ok="${10:-false}"
  sj="$(json_escape "$step")"
  mj="$(json_escape "$msg")"
  vj="$(json_escape "$vlb")"
  cj="$(json_escape "$codium")"
  stj="$(json_escape "$stack_deb")"
  idj="$(json_escape "$ide_deb")"
  printf '{\n'
  printf '  "status": "%s",\n' "$status"
  printf '  "step": "%s",\n' "$sj"
  printf '  "message": "%s",\n' "$mj"
  printf '  "vscode_linux_build": "%s",\n' "$vj"
  printf '  "codium_path": "%s",\n' "$cj"
  printf '  "stack_deb": "%s",\n' "$stj"
  printf '  "ide_deb": "%s",\n' "$idj"
  printf '  "verify_step14_closeout_passed": %s,\n' "$verify_ok"
  printf '  "install_performed": %s,\n' "$install_done"
  printf '  "post_install_smoke_passed": %s\n' "$smoke_ok"
  printf '}\n'
}

emit_preflight_json() {
  local status="$1"
  local vlb="$2"
  local edeps="$3"
  local msg="$4"
  vj="$(json_escape "$vlb")"
  ej="$(json_escape "$edeps")"
  mj="$(json_escape "$msg")"
  printf '{"mode":"preflight","status":"%s","vscode_linux_build":"%s","editor_host_deps":"%s","message":"%s"}\n' \
    "$status" "$vj" "$ej" "$mj"
}

run_preflight_only() {
  require_linux
  require_submodule
  require_stack_packaging_tools
  warn_if_vscodium_submodule_dirty

  if ! have_cmd python3; then
    echo "install-le-vibe-local: python3 is required for VSCode-linux probe — install python3." >&2
    if [[ "$PRINT_JSON" -eq 1 ]]; then
      emit_preflight_json "error" "unknown" "unknown" "python3 missing"
    fi
    exit 2
  fi

  log_tee "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  log_tee "Preflight only — no compile, no .deb build, no apt install"
  log_tee "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  log_tee "==> Host"
  log_tee "    uname: $(uname -a)"
  log_tee "    CPUs:  $(nproc)"
  if have_cmd free; then
    while IFS= read -r _ln; do log_tee "    RAM:   $_ln"; done < <(free -h 2>/dev/null | head -5 || true)
  else
    log_tee "    RAM:   (install procps for free -h)"
  fi
  log_tee "    Disk (repo + /tmp):"
  while IFS= read -r _ln; do log_tee "    $_ln"; done < <(df -Ph "$ROOT" /tmp 2>/dev/null || df -Ph 2>/dev/null | head -8 || true)

  if [[ -f "$ROOT/editor/.nvmrc" ]]; then
    local want have
    IFS= read -r want <"$ROOT/editor/.nvmrc" || true
    want="${want//$'\r'/}"
    if have_cmd node; then
      have="$(node --version 2>/dev/null | sed 's/^v//' || echo "?")"
      if [[ -n "$want" && "$have" == "$want" ]]; then
        log_tee "==> Node: OK (matches editor/.nvmrc $want)"
      else
        log_tee "==> Node: editor/.nvmrc wants ${want:-?}, active $have — run: source editor/use-node-toolchain.sh (editor/BUILD.md 14.a)"
      fi
    else
      log_tee "==> Node: not on PATH — install Node ${want:-from editor/.nvmrc} or source editor/use-node-toolchain.sh"
    fi
  fi

  local vlb
  vlb="$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT" 2>/dev/null | tr -d '\r\n' || echo unknown)"
  log_tee "==> VSCode-linux tree (compile milestone)"
  while IFS= read -r _ln; do log_tee "    $_ln"; done < <("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" --progress "$ROOT" 2>/dev/null || true)
  log_tee "    probe (ready|partial|absent|unknown): $vlb"

  log_tee "==> VSCodium Linux build dependencies (packaging/linux-vscodium-ci-apt.pkgs)"
  local edeps="ok"
  set +e
  "$ROOT/packaging/scripts/check-linux-vscodium-build-deps.sh"
  local deps_rc=$?
  set -e
  if [[ "$deps_rc" -ne 0 ]]; then
    edeps="missing"
    if [[ "$vlb" == "ready" ]]; then
      log_tee "WARN: host dependency check failed, but VSCode-linux-*/bin/codium already exists."
      log_tee "    Install deps before the next full compile: packaging/scripts/install-linux-vscodium-build-deps.sh"
      log_tee "    Or override at your risk: LEVIBE_SKIP_HOST_DEPS_CHECK=1 — editor/BUILD.md (14.e)"
      edeps="missing_tree_ready"
    else
      echo "install-le-vibe-local: VSCodium host build dependencies incomplete (vscode_linux_build: $vlb)." >&2
      echo "  Install: packaging/scripts/install-linux-vscodium-build-deps.sh" >&2
      echo "  Or print only: packaging/scripts/install-linux-vscodium-build-deps.sh --print-install-command" >&2
      echo "  Docker full compile (OOM-prone hosts): packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh" >&2
      echo "  Read: editor/BUILD.md (14.e), docs/LOCAL_INSTALL_ONE_SHOT.md" >&2
      if [[ "$PRINT_JSON" -eq 1 ]]; then
        emit_preflight_json "error" "$vlb" "$edeps" "check-linux-vscodium-build-deps.sh failed"
      fi
      exit 2
    fi
  fi

  log_tee "==> Expectations (full one-shot install)"
  log_tee "    • Editor compile (dev/build.sh): often 1–4+ hours on a capable workstation; can fail with OOM on low RAM."
  log_tee "    • Disk: plan for tens of GB under editor/vscodium/ during compile; keep >25 GB free when possible."
  log_tee "    • Partial VSCode-linux tree: editor/BUILD.md (*Partial tree*); tarball recovery: packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh"
  log_tee "    • Resume: re-run this script — existing VSCode-linux-*/bin/codium skips recompile unless --force-editor-build."

  log_tee ""
  log_tee "PASS — preflight (ready to run full install without --preflight-only)"
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    emit_preflight_json "ok" "$vlb" "$edeps" "preflight checks passed (see editor_host_deps for dep parity)"
  fi
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install) DO_INSTALL=1 ;;
    --yes) ASSUME_YES=1 ;;
    --force-editor-build) FORCE_EDITOR_BUILD=1 ;;
    --skip-editor-build) SKIP_EDITOR_BUILD=1 ;;
    --skip-compile-failfast) SKIP_COMPILE_FAILFAST=1 ;;
    --json) PRINT_JSON=1 ;;
    --apt-sim) ENABLE_APT_SIM=1 ;;
    --skip-gate) SKIP_VERIFY_GATE=1 ;;
    --log-file)
      LOG_FILE="${2:-}"
      if [[ -z "$LOG_FILE" ]]; then echo "install-le-vibe-local: --log-file needs a path" >&2; exit 2; fi
      shift
      ;;
    --preflight-only) PREFLIGHT_ONLY=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "install-le-vibe-local: unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if [[ "${LEVIBE_LOCAL_SKIP_COMPILE_FAILFAST:-}" == "1" ]]; then
  SKIP_COMPILE_FAILFAST=1
fi

if [[ "$SKIP_EDITOR_BUILD" -eq 1 && "$FORCE_EDITOR_BUILD" -eq 1 ]]; then
  echo "install-le-vibe-local: --skip-editor-build and --force-editor-build are mutually exclusive." >&2
  exit 2
fi

if [[ "$PREFLIGHT_ONLY" -eq 1 ]]; then
  if [[ "$DO_INSTALL" -eq 1 || "$FORCE_EDITOR_BUILD" -eq 1 || "$SKIP_EDITOR_BUILD" -eq 1 || "$ENABLE_APT_SIM" -eq 1 || "$SKIP_VERIFY_GATE" -eq 1 || "$SKIP_COMPILE_FAILFAST" -eq 1 ]]; then
    echo "install-le-vibe-local: --preflight-only cannot be combined with --install, --force-editor-build, --skip-editor-build, --apt-sim, --skip-gate, or --skip-compile-failfast." >&2
    exit 2
  fi
fi

if [[ "$DO_INSTALL" -eq 1 ]]; then
  if ! have_cmd sudo; then
    echo "install-le-vibe-local: --install requires sudo on PATH." >&2
    exit 2
  fi
  if ! have_cmd apt-get; then
    echo "install-le-vibe-local: --install requires apt-get (Debian/Ubuntu)." >&2
    exit 2
  fi
fi

if [[ -n "$LOG_FILE" ]]; then
  mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
  {
    echo "==== install-le-vibe-local $(date -Iseconds) ===="
    echo "root=$ROOT"
  } >>"$LOG_FILE"
fi

if [[ "$PREFLIGHT_ONLY" -eq 1 ]]; then
  run_preflight_only
fi

require_linux
require_submodule
require_stack_packaging_tools
warn_if_vscodium_submodule_dirty

PROBE_OUT="$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT" 2>/dev/null | tr -d '\r\n' || echo unknown)"

run_compile_failfast() {
  if [[ "$SKIP_COMPILE_FAILFAST" -eq 1 ]]; then
    log_tee "==> Compile fail-fast: skipped (--skip-compile-failfast)"
    return 0
  fi
  log_tee "==> Compile fail-fast: ci-vscodium-bash-syntax.sh"
  "$ROOT/packaging/scripts/ci-vscodium-bash-syntax.sh"
  log_tee "==> Compile fail-fast: ci-editor-nvmrc-sync.sh"
  "$ROOT/packaging/scripts/ci-editor-nvmrc-sync.sh"
}

run_editor_build() {
  if [[ "$SKIP_EDITOR_BUILD" -eq 1 ]]; then
    log_tee "==> Editor compile: skipped (--skip-editor-build)"
    if [[ "$PROBE_OUT" != "ready" ]]; then
      log_tee "install-le-vibe-local: --skip-editor-build requires VSCode-linux tree ready (probe: ${PROBE_OUT})." >&2
      log_tee "  Finish compile: packaging/scripts/ci-vscodium-linux-dev-build.sh — editor/BUILD.md (14.c)" >&2
      if [[ "$PRINT_JSON" -eq 1 ]]; then
        emit_final_json "error" "editor" "probe not ready with --skip-editor-build" "$PROBE_OUT" "" "" "" "false" "false" "false"
      fi
      exit 1
    fi
    return 0
  fi
  if [[ "$PROBE_OUT" == "ready" && "$FORCE_EDITOR_BUILD" -eq 0 ]]; then
    log_tee "==> Editor compile: skipped (VSCode-linux-*/bin/codium already present — use --force-editor-build to rebuild)"
    return 0
  fi
  run_compile_failfast
  log_tee "==> Editor compile: ci-vscodium-linux-dev-build.sh (→ dev/build.sh) — long-running"
  "$ROOT/packaging/scripts/ci-vscodium-linux-dev-build.sh"
}

run_editor_build

PROBE_OUT="$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT" 2>/dev/null | tr -d '\r\n' || echo unknown)"

FAIL_STEP=""
FAIL_MSG=""

verify_codium_executable() {
  log_tee "==> Verify built binary: editor/verify-14c-local-binary.sh"
  local cpath
  if ! cpath="$("$ROOT/editor/verify-14c-local-binary.sh")"; then
    FAIL_STEP="14c"
    FAIL_MSG="built codium missing or incomplete"
    return 1
  fi
  if [[ ! -x "$cpath" ]]; then
    echo "install-le-vibe-local: not executable: $cpath" >&2
    FAIL_STEP="14c"
    FAIL_MSG="bin/codium not executable"
    return 1
  fi
  log_tee "    OK: $cpath"
  printf '%s' "$cpath"
  return 0
}

CODIUM_PATH=""
if ! CODIUM_PATH="$(verify_codium_executable)"; then
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    emit_final_json "error" "${FAIL_STEP:-14c}" "$FAIL_MSG" "$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT" 2>/dev/null | tr -d '\r\n' || echo unknown)" "" "" "" "false" "false" "false"
  fi
  exit 1
fi

log_tee "==> Build .deb packages: build-le-vibe-debs.sh --with-ide"
BLD_ARGS=(--with-ide)
[[ "$DO_INSTALL" -eq 1 ]] && BLD_ARGS+=(--install)
[[ "$ASSUME_YES" -eq 1 ]] && BLD_ARGS+=(--yes)
if ! "$ROOT/packaging/scripts/build-le-vibe-debs.sh" "${BLD_ARGS[@]}"; then
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    emit_final_json "error" "deb" "build-le-vibe-debs.sh --with-ide failed" "$PROBE_OUT" "$CODIUM_PATH" "" "" "false" "false" "false"
  fi
  exit 1
fi

STACK_DEB="$("$ROOT/packaging/scripts/resolve-latest-le-vibe-stack-deb.sh" "$ROOT" || true)"
IDE_DEB="$(find "$ROOT/packaging" -maxdepth 1 -name 'le-vibe-ide_*.deb' -type f 2>/dev/null | sort -V | tail -n1 || true)"

# Explicit artifact gate before any apt install (build-le-vibe-debs --install runs inside the build step).
if [[ "$DO_INSTALL" -eq 1 ]]; then
  if [[ -z "${STACK_DEB:-}" || ! -f "$STACK_DEB" ]]; then
    echo "install-le-vibe-local: stack package .deb missing after build (expected le-vibe_*_all.deb beside clone or repo root)." >&2
    echo "  See: packaging/scripts/resolve-latest-le-vibe-stack-deb.sh — docs/PM_DEB_BUILD_ITERATION.md" >&2
    if [[ "$PRINT_JSON" -eq 1 ]]; then
      emit_final_json "error" "artifacts" "stack .deb not found after build" "$PROBE_OUT" "$CODIUM_PATH" "" "${IDE_DEB:-}" "false" "false" "false"
    fi
    exit 1
  fi
  if [[ -z "${IDE_DEB:-}" || ! -f "$IDE_DEB" ]]; then
    echo "install-le-vibe-local: IDE package .deb missing after build (expected packaging/le-vibe-ide_*_amd64.deb)." >&2
    echo "  See: packaging/scripts/build-le-vibe-debs.sh --with-ide — editor/BUILD.md (14.c)" >&2
    if [[ "$PRINT_JSON" -eq 1 ]]; then
      emit_final_json "error" "artifacts" "IDE .deb not found after build" "$PROBE_OUT" "$CODIUM_PATH" "${STACK_DEB:-}" "" "false" "false" "false"
    fi
    exit 1
  fi
fi

VERIFY_ARGS=(--require-stack-deb)
[[ "$ENABLE_APT_SIM" -eq 1 ]] && VERIFY_ARGS+=(--apt-sim)
[[ "$SKIP_VERIFY_GATE" -eq 1 ]] && VERIFY_ARGS+=(--skip-gate)

log_tee "==> STEP 14 close-out: verify-step14-closeout.sh ${VERIFY_ARGS[*]}"
if ! "$ROOT/packaging/scripts/verify-step14-closeout.sh" "${VERIFY_ARGS[@]}"; then
  if [[ "$PRINT_JSON" -eq 1 ]]; then
    emit_final_json "error" "verify" "verify-step14-closeout.sh failed" "$PROBE_OUT" "$CODIUM_PATH" "${STACK_DEB:-}" "${IDE_DEB:-}" "false" "$([[ "$DO_INSTALL" -eq 1 ]] && echo true || echo false)" "false"
  fi
  exit 1
fi

SMOKE_PASSED="false"
if [[ "$DO_INSTALL" -eq 1 ]]; then
  log_tee "==> Post-install smoke: manual-step14-install-smoke.sh --verify-only"
  if "$ROOT/packaging/scripts/manual-step14-install-smoke.sh" --verify-only; then
    SMOKE_PASSED="true"
  else
    if [[ "$PRINT_JSON" -eq 1 ]]; then
      emit_final_json "error" "smoke" "manual-step14-install-smoke.sh --verify-only failed" "$PROBE_OUT" "$CODIUM_PATH" "${STACK_DEB:-}" "${IDE_DEB:-}" "true" "true" "false"
    fi
    exit 1
  fi
else
  log_tee "==> Post-install smoke: skipped (no --install — on a target host: sudo apt install both .deb, then manual-step14-install-smoke.sh --verify-only)"
fi

log_tee ""
log_tee "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_tee "PASS — Lé Vibe local install path"
log_tee "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_tee "Built:"
log_tee "  VSCode tree + codium: $CODIUM_PATH"
log_tee "  Stack .deb:          ${STACK_DEB:-<unknown>}"
log_tee "  IDE .deb:            ${IDE_DEB:-<unknown>}"
if [[ "$DO_INSTALL" -eq 1 ]]; then
  log_tee "Installed: both packages via apt (see build-le-vibe-debs output above)."
  log_tee "Post-install smoke: $SMOKE_PASSED"
else
  log_tee "Installed: (not requested) — run with --install --yes for non-interactive sudo apt install."
fi
log_tee "STEP 14 verify: OK (verify-step14-closeout.sh --require-stack-deb)"
log_tee "Next: lvibe --help  |  codium --version  |  lvibe open-welcome"
log_tee ""

if [[ "$PRINT_JSON" -eq 1 ]]; then
  emit_final_json "ok" "done" "all steps passed" "$PROBE_OUT" "$CODIUM_PATH" "${STACK_DEB:-}" "${IDE_DEB:-}" "true" "$([[ "$DO_INSTALL" -eq 1 ]] && echo true || echo false)" "$SMOKE_PASSED"
fi

exit 0
