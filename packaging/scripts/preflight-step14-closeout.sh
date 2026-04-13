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
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

REQUIRE_STACK_DEB=0
SKIP_GATE=0

usage() {
  cat <<'EOF'
Usage: packaging/scripts/preflight-step14-closeout.sh [--require-stack-deb] [--skip-gate]

Prints one line per check ([ok] / [missing]) then a summary. Exit 0 iff all checks pass.

  --require-stack-deb   Also require le-vibe_*.deb (resolve-latest-le-vibe-stack-deb.sh).
  --skip-gate           Skip ci-editor-gate.sh (faster when only checking artifacts).

See packaging/scripts/verify-step14-closeout.sh for the strict single-pass verifier.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-stack-deb) REQUIRE_STACK_DEB=1 ;;
    --skip-gate) SKIP_GATE=1 ;;
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

if [[ "$SKIP_GATE" -eq 1 ]]; then
  echo "[skip] ci-editor-gate.sh (--skip-gate)"
else
  if "$ROOT/packaging/scripts/ci-editor-gate.sh" >/dev/null 2>&1; then
    echo "[ok] ci-editor-gate.sh"
  else
    echo "[missing] ci-editor-gate.sh — run packaging/scripts/ci-editor-gate.sh for details" >&2
    failures=$((failures + 1))
  fi
fi

set +e
# Capture verify-14c combined output; on failure relay it (partial VSCode-linux tree vs no tree).
_codium_out="$("$ROOT/editor/verify-14c-local-binary.sh" 2>&1)"
_codium_ec=$?
set -e
if [[ "${_codium_ec}" -eq 0 ]]; then
  echo "[ok] editor/vscodium VSCode-linux-*/bin/codium (${_codium_out})"
else
  if [[ -n "${_codium_out}" ]]; then
    printf '%s\n' "${_codium_out}" >&2
  fi
  echo "[missing] VSCode-linux-*/bin/codium (14.c) — cd editor/vscodium && ./dev/build.sh (editor/BUILD.md *Partial tree* / 14.c)" >&2
  failures=$((failures + 1))
fi

_vlb="$("$ROOT/packaging/scripts/probe-vscode-linux-build.sh" "$ROOT")"
echo "vscode_linux_build: ${_vlb}"
if [[ "${_vlb}" == "partial" ]]; then
  _bf="$("$ROOT/packaging/scripts/print-step14-vscode-linux-bin-files.sh" "$ROOT")"
  echo "vscode_linux_bin_files: ${_bf}"
fi
if [[ "${_vlb}" != "ready" ]]; then
  echo "hint: packaging/scripts/build-le-vibe-debs.sh --with-ide exits before stack dpkg-buildpackage until vscode_linux_build is ready (or use --vs-build PATH with bin/codium) — docs/PM_DEB_BUILD_ITERATION.md (Failure (--with-ide))" >&2
  if [[ "${_vlb}" == "partial" ]]; then
    echo "hint: partial tree — CI tarball (linux_compile): ./packaging/scripts/print-github-linux-compile-artifact-hint.sh (browser or gh); then ./packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes (editor/BUILD.md 14.f) or finish cd editor/vscodium && ./dev/build.sh (14.c)" >&2
  fi
fi

shopt -s nullglob
ide_debs=("$ROOT"/packaging/le-vibe-ide_*.deb)
if [[ ${#ide_debs[@]} -gt 0 ]]; then
  _ide="$(printf '%s\n' "${ide_debs[@]}" | sort -V | tail -n1)"
  echo "[ok] packaging/le-vibe-ide_*.deb ($_ide)"
else
  echo "[missing] packaging/le-vibe-ide_*.deb — packaging/scripts/build-le-vibe-ide-deb.sh or build-le-vibe-debs.sh --with-ide" >&2
  failures=$((failures + 1))
fi

if [[ "$REQUIRE_STACK_DEB" -eq 1 ]]; then
  _stack="$("$ROOT/packaging/scripts/resolve-latest-le-vibe-stack-deb.sh" "$ROOT" || true)"
  if [[ -n "$_stack" && -f "$_stack" ]]; then
    echo "[ok] le-vibe_*.deb stack package ($_stack)"
  else
    echo "[missing] le-vibe_*.deb — dpkg-buildpackage at repo root or build-le-vibe-debs.sh (resolve-latest-le-vibe-stack-deb.sh)" >&2
    failures=$((failures + 1))
  fi
else
  echo "[optional] stack le-vibe_*.deb not required (omit --require-stack-deb for full-product gate)"
fi

if [[ "$failures" -eq 0 ]]; then
  echo "preflight-step14-closeout: all checked items OK — run verify-step14-closeout.sh${REQUIRE_STACK_DEB:+ --require-stack-deb} for strict gate."
  exit 0
fi

echo "preflight-step14-closeout: $failures check(s) failed — fix items above, then re-run." >&2
exit 1
