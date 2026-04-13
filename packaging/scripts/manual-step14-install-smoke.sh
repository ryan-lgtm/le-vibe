#!/usr/bin/env bash
# STEP 14 / §7.3 helper: run this on an Ubuntu maintainer host after building
# stack + IDE .deb artifacts to perform a deterministic manual install smoke.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

STACK_DEB_DEFAULT="$(ls -1 "$ROOT"/../le-vibe_*.deb 2>/dev/null | sort -V | tail -n1 || true)"
IDE_DEB_DEFAULT="$(ls -1 "$ROOT"/packaging/le-vibe-ide_*.deb 2>/dev/null | sort -V | tail -n1 || true)"

STACK_DEB="${STACK_DEB:-$STACK_DEB_DEFAULT}"
IDE_DEB="${IDE_DEB:-$IDE_DEB_DEFAULT}"
RUN_VERIFY=0
PRINT_INSTALL_CMD=0
PRINT_JSON=0

usage() {
  cat <<'EOF'
Usage: packaging/scripts/manual-step14-install-smoke.sh [--verify-only] [--print-install-cmd] [--json]

Purpose:
  Print copy/paste commands for the remaining manual STEP 14 Ubuntu validation:
    1) install stack + IDE .deb pair,
    2) launch `lvibe` and IDE,
    3) run focused post-install checks.

Environment:
  STACK_DEB  Override stack package path (default: latest ../le-vibe_*.deb)
  IDE_DEB    Override IDE package path   (default: latest packaging/le-vibe-ide_*.deb)

Options:
  --verify-only   Run post-install verification checks now (no install).
  --print-install-cmd
                  Print only: sudo apt install "<stack.deb>" "<ide.deb>".
  --json          Print resolved stack/IDE deb paths + install command as JSON.
  -h, --help      Show this message and exit.
EOF
}

assert_file() {
  local path="$1"
  local label="$2"
  if [[ -z "$path" || ! -f "$path" ]]; then
    echo "manual-step14-install-smoke: missing $label ($path)" >&2
    echo "manual-step14-install-smoke: build artifacts first:" >&2
    echo "  packaging/scripts/build-le-vibe-debs.sh --with-ide" >&2
    echo "manual-step14-install-smoke: then verify close-out artifacts:" >&2
    echo "  packaging/scripts/verify-step14-closeout.sh --require-stack-deb" >&2
    exit 2
  fi
}

run_verify_only() {
  echo "==> Post-install verification (local host)"
  command -v lvibe >/dev/null 2>&1 || {
    echo "manual-step14-install-smoke: lvibe not on PATH (is stack package installed?)." >&2
    exit 1
  }
  command -v codium >/dev/null 2>&1 || {
    echo "manual-step14-install-smoke: codium not on PATH (is IDE package installed?)." >&2
    exit 1
  }
  [[ -f /usr/share/applications/le-vibe.desktop ]] || {
    echo "manual-step14-install-smoke: missing /usr/share/applications/le-vibe.desktop" >&2
    exit 1
  }
  [[ -x /usr/lib/le-vibe/bin/codium ]] || {
    echo "manual-step14-install-smoke: missing executable /usr/lib/le-vibe/bin/codium" >&2
    exit 1
  }
  [[ -f /usr/share/doc/le-vibe/README.Debian || -f /usr/share/doc/le-vibe/README.Debian.gz ]] || {
    echo "manual-step14-install-smoke: missing /usr/share/doc/le-vibe/README.Debian(.gz)" >&2
    exit 1
  }
  echo "manual-step14-install-smoke: OK (lvibe + codium + desktop + docs present)."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --verify-only) RUN_VERIFY=1 ;;
    --print-install-cmd) PRINT_INSTALL_CMD=1 ;;
    --json) PRINT_JSON=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "manual-step14-install-smoke: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ "$RUN_VERIFY" -eq 1 ]]; then
  run_verify_only
  exit 0
fi

assert_file "$STACK_DEB" "stack deb"
assert_file "$IDE_DEB" "IDE deb"

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\t'/\\t}"
  printf '%s' "$value"
}

if [[ "$PRINT_INSTALL_CMD" -eq 1 ]]; then
  printf 'sudo apt install "%s" "%s"\n' "$STACK_DEB" "$IDE_DEB"
  exit 0
fi

if [[ "$PRINT_JSON" -eq 1 ]]; then
  stack_json="$(json_escape "$STACK_DEB")"
  ide_json="$(json_escape "$IDE_DEB")"
  install_json="$(json_escape "sudo apt install \"$STACK_DEB\" \"$IDE_DEB\"")"
  printf '{\n'
  printf '  "stack_deb": "%s",\n' "$stack_json"
  printf '  "ide_deb": "%s",\n' "$ide_json"
  printf '  "install_cmd": "%s"\n' "$install_json"
  printf '}\n'
  exit 0
fi

cat <<EOF
==> STEP 14 manual Ubuntu install smoke
1) Install both packages:
   sudo apt install "$STACK_DEB" "$IDE_DEB"

2) Verify commands resolve:
   lvibe --help
   codium --version

3) Verify installed payloads:
   test -x /usr/lib/le-vibe/bin/codium
   test -f /usr/share/applications/le-vibe.desktop
   test -f /usr/share/doc/le-vibe/README.Debian || test -f /usr/share/doc/le-vibe/README.Debian.gz

4) Launch UX smoke:
   lvibe open-welcome
   codium --user-data-dir "\$(mktemp -d)" --extensions-dir "\$(mktemp -d)"

5) Optional in-script post-install verification:
   packaging/scripts/manual-step14-install-smoke.sh --verify-only
EOF
