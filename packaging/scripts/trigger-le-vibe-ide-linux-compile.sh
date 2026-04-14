#!/usr/bin/env bash
# STEP 14.e — POST workflow_dispatch for build-le-vibe-ide.yml with vscodium_linux_compile=true
# (runs optional job linux_compile → ci-vscodium-linux-dev-build.sh → dev/build.sh).
# Uses curl + GitHub REST API (no gh CLI). Requires GITHUB_TOKEN or GH_TOKEN with **repo** scope
# (or fine-grained: Actions write + Contents read on the repository).
# Authority: .github/workflows/build-le-vibe-ide.yml, editor/BUILD.md (14.e), docs/PM_DEB_BUILD_ITERATION.md.
# Pair: packaging/scripts/download-vscodium-linux-compile-artifact.sh (after the run finishes).
# E1: le-vibe/tests/test_packaging_step14_help_smoke.py; packaging/scripts/ci-editor-gate.sh (bash -n).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md
# Pytest: le-vibe/tests/test_preflight_step14_closeout_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
API="${GITHUB_API_URL:-https://api.github.com}"
REF="${LEVIBE_WORKFLOW_DISPATCH_REF:-main}"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/trigger-le-vibe-ide-linux-compile.sh [OPTIONS]

POSTs a **workflow_dispatch** for **build-le-vibe-ide.yml** with input **vscodium_linux_compile=true**
(boolean inputs are sent as the string **"true"** per GitHub API).

Requires **GITHUB_TOKEN** or **GH_TOKEN** with permission to dispatch workflows (classic **repo** scope).

Options:
  --ref NAME   Git ref to run (branch or tag; default: main, or LEVIBE_WORKFLOW_DISPATCH_REF).
  -h, --help   Show this message and exit.

Environment:
  GITHUB_TOKEN, GH_TOKEN              Required.
  GITHUB_API_URL                      API host (default https://api.github.com).
  LEVIBE_WORKFLOW_DISPATCH_REF        Default ref when --ref not passed (default: main).

After **204**, open the repo **Actions** tab and watch **linux_compile** (long; may OOM on GitHub-hosted runners).

Then fetch the artifact: packaging/scripts/download-vscodium-linux-compile-artifact.sh
(or packaging/scripts/print-github-linux-compile-artifact-hint.sh for browser/gh).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref) REF="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "${0##*/}: unexpected argument: $1 — use --help" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TOKEN" ]]; then
  echo "${0##*/}: set GITHUB_TOKEN or GH_TOKEN (repo scope) — see --help" >&2
  exit 2
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "${0##*/}: curl not on PATH" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "${0##*/}: jq not on PATH — install jq (e.g. sudo apt install jq)" >&2
  exit 1
fi

_parse_remote() {
  local url
  url="$(git -C "$ROOT" remote get-url origin 2>/dev/null || true)"
  if [[ -z "$url" ]]; then
    echo "${0##*/}: could not read git remote origin" >&2
    exit 1
  fi
  if [[ "$url" =~ github\.com[:/]([^/]+)/([^/]+)$ ]]; then
    printf '%s %s\n' "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]%.git}"
    return 0
  fi
  echo "${0##*/}: unsupported origin URL: $url" >&2
  exit 1
}

read -r OWNER REPO < <(_parse_remote)

BODY="$(jq -n --arg ref "$REF" '{ref: $ref, inputs: {vscodium_linux_compile: "true"}}')"
TMP="$(mktemp "${TMPDIR:-/tmp}/lv-wfd.XXXXXX.json")"
trap 'rm -f "${TMP}"' EXIT

http_code="$(
  curl -sS -X POST -o "$TMP" -w '%{http_code}' \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    -H "Content-Type: application/json" \
    -d "$BODY" \
    "${API}/repos/${OWNER}/${REPO}/actions/workflows/build-le-vibe-ide.yml/dispatches"
)"

if [[ "$http_code" == "204" ]]; then
  echo "${0##*/}: workflow_dispatch accepted (HTTP 204) — ${OWNER}/${REPO} ref=${REF} vscodium_linux_compile=true"
  echo "${0##*/}: watch: https://github.com/${OWNER}/${REPO}/actions/workflows/build-le-vibe-ide.yml"
  exit 0
fi

echo "${0##*/}: workflow_dispatch failed HTTP ${http_code}" >&2
if [[ -s "$TMP" ]]; then
  cat "$TMP" >&2
fi
exit 1
