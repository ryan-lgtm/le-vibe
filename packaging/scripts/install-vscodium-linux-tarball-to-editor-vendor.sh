#!/usr/bin/env bash
# STEP 14.f / §7.3 — unpack linux_compile vscodium-linux-build.tar.gz into editor/vscodium/
# so editor/vscodium/VSCode-linux-*/bin/codium exists (recovers partial / interrupted builds).
# Tarball discovery: print-github-linux-compile-artifact-hint.sh, trigger-le-vibe-ide-linux-compile.sh,
#   download-vscodium-linux-compile-artifact.sh --install (same family as verify-step14-closeout.sh).
# Authority: docs/PRODUCT_SPEC.md §7.3, editor/BUILD.md (*Partial tree*, *14.f*), docs/PM_DEB_BUILD_ITERATION.md.
# E1: le-vibe/tests/test_packaging_step14_help_smoke.py; packaging/scripts/ci-editor-gate.sh (bash -n).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md
# Pytest: le-vibe/tests/test_print_paths_14f_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh [OPTIONS] /path/to/vscodium-linux-build.tar.gz

Unpack a CI linux_compile artifact tarball into editor/vscodium/, replacing any existing
editor/vscodium/VSCode-linux-* directory. Use when probe-vscode-linux-build.sh reports
partial (e.g. only codium-tunnel) or to populate a clone without compiling locally.

After success, packaging/scripts/probe-vscode-linux-build.sh should print ready.

GitHub Actions wraps the tarball in a .zip — unzip first, then pass the .tar.gz path.

Obtain the tarball from CI: packaging/scripts/print-github-linux-compile-artifact-hint.sh
(browser Actions UI or gh run download); maintainer:
packaging/scripts/trigger-le-vibe-ide-linux-compile.sh;
packaging/scripts/download-vscodium-linux-compile-artifact.sh --install.

Options:
  -y, --yes     Remove existing VSCode-linux-* without prompting (required when stdin is not a TTY).
  -h, --help    Show this message and exit.

See editor/BUILD.md (*Partial tree*, *GitHub Actions artifact vscodium-linux-build.tar.gz*).
EOF
}

YES=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes) YES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) break ;;
  esac
done

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

TAR_ARG="$1"
VSC="${ROOT}/editor/vscodium"

if [[ ! -f "${VSC}/product.json" ]]; then
  echo "${0##*/}: missing ${VSC}/product.json — init submodule (editor/README.md Fresh clone 14.b)." >&2
  exit 1
fi

if ! command -v realpath >/dev/null 2>&1; then
  echo "${0##*/}: realpath not on PATH — install coreutils." >&2
  exit 1
fi
if ! command -v tar >/dev/null 2>&1; then
  echo "${0##*/}: tar not on PATH." >&2
  exit 1
fi

if [[ ! -f "$TAR_ARG" ]]; then
  echo "${0##*/}: not a regular file: $TAR_ARG" >&2
  echo "${0##*/}: obtain tarball: ${ROOT}/packaging/scripts/print-github-linux-compile-artifact-hint.sh (browser or gh); ${ROOT}/packaging/scripts/trigger-le-vibe-ide-linux-compile.sh; ${ROOT}/packaging/scripts/download-vscodium-linux-compile-artifact.sh --install" >&2
  exit 1
fi

TAR_ABS="$(realpath "$TAR_ARG")"

shopt -s nullglob
existing=("$VSC"/VSCode-linux-*)
if [[ ${#existing[@]} -gt 0 ]]; then
  if [[ "$YES" -ne 1 ]]; then
    if [[ ! -t 0 ]]; then
      echo "${0##*/}: refusing to remove VSCode-linux-* without a TTY; pass --yes" >&2
      exit 1
    fi
    echo "Will remove:" >&2
    printf '  %s\n' "${existing[@]}" >&2
    read -r -p "Continue? [y/N] " _ans || true
    case "${_ans:-}" in
      y|Y|yes|YES) ;;
      *) echo "Aborted." >&2; exit 1 ;;
    esac
  fi
  rm -rf "${existing[@]}"
fi

echo "${0##*/}: extracting $TAR_ABS -> ${VSC}/"
tar -xzf "$TAR_ABS" -C "$VSC"

st="$("${ROOT}/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT")"
echo "vscode_linux_build: ${st}"
if [[ "$st" != "ready" ]]; then
  echo "${0##*/}: expected probe ready after extract, got ${st} — check tarball layout (editor/BUILD.md 14.f)." >&2
  exit 1
fi

_codium="$("${ROOT}/editor/print-built-codium-path.sh")"
echo "${0##*/}: ok — ${_codium}"
echo "Next: packaging/scripts/build-le-vibe-ide-deb.sh or packaging/scripts/build-le-vibe-debs.sh --with-ide (docs/PM_DEB_BUILD_ITERATION.md)."
