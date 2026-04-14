#!/usr/bin/env bash
# STEP 14.f / §7.3 — download vscodium-linux-build.tar.gz from a successful GitHub Actions
# **linux_compile** run (build-le-vibe-ide.yml) using curl + the REST API (no gh CLI).
# Requires GITHUB_TOKEN or GH_TOKEN with **actions:read** (repo scope on private repos).
# Authority: editor/BUILD.md (*GitHub Actions artifact*), docs/PM_DEB_BUILD_ITERATION.md.
# Pair: packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh --yes
# E1: le-vibe/tests/test_packaging_step14_help_smoke.py; packaging/scripts/ci-editor-gate.sh (bash -n).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
API="${GITHUB_API_URL:-https://api.github.com}"
RUN_ID=""
OUT_DIR=""
DO_INSTALL=0

usage() {
  cat <<'EOF'
Usage: packaging/scripts/download-vscodium-linux-compile-artifact.sh [OPTIONS]

Find the newest successful workflow run for **build-le-vibe-ide.yml** that uploaded artifact
**le-vibe-vscodium-linux-<run_id>** (job **linux_compile**), download the GitHub .zip wrapper,
extract **vscodium-linux-build.tar.gz**, and print its path.

Requires **GITHUB_TOKEN** or **GH_TOKEN** with permission to read Actions artifacts
(**actions:read**; classic PAT: **repo** on private repositories).

Options:
  --run-id ID      Use this workflow run id instead of auto-discovery (artifact must exist).
  --output-dir DIR Write extracted vscodium-linux-build.tar.gz here (default: TMPDIR or /tmp).
  --install          After download, run install-vscodium-linux-tarball-to-editor-vendor.sh --yes.
  -h, --help         Show this message and exit.

Environment:
  GITHUB_TOKEN, GH_TOKEN   GitHub API token (required).
  GITHUB_API_URL           Override API host (default https://api.github.com).

After success, vendor the tree:
  packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh /path/to/vscodium-linux-build.tar.gz --yes

Offline copy/paste (no token): packaging/scripts/print-github-linux-compile-artifact-hint.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-id) RUN_ID="${2:-}"; shift 2 ;;
    --output-dir) OUT_DIR="${2:-}"; shift 2 ;;
    --install) DO_INSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "${0##*/}: unexpected argument: $1 — use --help" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TOKEN" ]]; then
  echo "${0##*/}: set GITHUB_TOKEN or GH_TOKEN (actions:read) — see --help" >&2
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
if ! command -v unzip >/dev/null 2>&1; then
  echo "${0##*/}: unzip not on PATH — install unzip (e.g. sudo apt install unzip)" >&2
  exit 1
fi

_gh_headers() {
  curl -sS \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$@"
}

_parse_remote() {
  local url u o r
  url="$(git -C "$ROOT" remote get-url origin 2>/dev/null || true)"
  if [[ -z "$url" ]]; then
    echo "${0##*/}: could not read git remote origin" >&2
    exit 1
  fi
  # git@github.com:org/repo.git  or  https://github.com/org/repo(.git)
  if [[ "$url" =~ github\.com[:/]([^/]+)/([^/]+)$ ]]; then
    o="${BASH_REMATCH[1]}"
    r="${BASH_REMATCH[2]%.git}"
    printf '%s %s\n' "$o" "$r"
    return 0
  fi
  echo "${0##*/}: unsupported origin URL: $url" >&2
  exit 1
}

read -r OWNER REPO < <(_parse_remote)

_pick_artifact_from_run() {
  local rid="$1"
  local json
  json="$(_gh_headers "${API}/repos/${OWNER}/${REPO}/actions/runs/${rid}/artifacts?per_page=100")"
  if ! jq -e . >/dev/null 2>&1 <<<"$json"; then
    echo "${0##*/}: artifacts API error for run ${rid}" >&2
    printf '%s\n' "$json" >&2
    return 1
  fi
  jq -r '.artifacts[] | select(.name | test("^le-vibe-vscodium-linux-[0-9]+$")) | "\(.id)\t\(.name)"' <<<"$json" | head -n1
}

RESOLVED_RUN=""
ARTIFACT_ID=""
ARTIFACT_NAME=""

if [[ -n "$RUN_ID" ]]; then
  RESOLVED_RUN="$RUN_ID"
  line="$(_pick_artifact_from_run "$RUN_ID")"
  if [[ -z "$line" ]]; then
    echo "${0##*/}: run ${RUN_ID} has no le-vibe-vscodium-linux-* artifact (linux_compile may not have run or failed)." >&2
    exit 1
  fi
  ARTIFACT_ID="${line%%$'\t'*}"
  ARTIFACT_NAME="${line#*$'\t'}"
else
  runs_json="$(_gh_headers "${API}/repos/${OWNER}/${REPO}/actions/workflows/build-le-vibe-ide.yml/runs?per_page=50")"
  if ! jq -e '.workflow_runs' >/dev/null 2>&1 <<<"$runs_json"; then
    echo "${0##*/}: workflow runs API error — check token and repo access (${OWNER}/${REPO})" >&2
    printf '%s\n' "$runs_json" >&2
    exit 1
  fi
  while read -r rid; do
    [[ -z "$rid" ]] && continue
    line="$(_pick_artifact_from_run "$rid" || true)"
    if [[ -n "$line" ]]; then
      RESOLVED_RUN="$rid"
      ARTIFACT_ID="${line%%$'\t'*}"
      ARTIFACT_NAME="${line#*$'\t'}"
      break
    fi
  done < <(jq -r '.workflow_runs[] | select(.conclusion == "success") | .id' <<<"$runs_json")
  if [[ -z "$RESOLVED_RUN" || -z "$ARTIFACT_ID" ]]; then
    echo "${0##*/}: no successful run with le-vibe-vscodium-linux-* artifact found — trigger workflow_dispatch with vscodium_linux_compile, push ide-v* tag, or use --run-id" >&2
    echo "${0##*/}: hint: packaging/scripts/print-github-linux-compile-artifact-hint.sh" >&2
    exit 1
  fi
fi

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="${TMPDIR:-/tmp}"
fi
mkdir -p "$OUT_DIR"
ZIP="$(mktemp "${OUT_DIR%/}/le-vibe-vscodium-art.XXXXXX.zip")"
trap 'rm -f "${ZIP}"' EXIT

echo "${0##*/}: owner/repo=${OWNER}/${REPO} run_id=${RESOLVED_RUN} artifact=${ARTIFACT_NAME} (id=${ARTIFACT_ID})"

# Download archive (.zip); GitHub redirects to blob storage — curl -L
http_code="$(
  curl -sS -L -o "$ZIP" -w '%{http_code}' \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "${API}/repos/${OWNER}/${REPO}/actions/artifacts/${ARTIFACT_ID}/zip"
)"
if [[ "$http_code" != "200" ]]; then
  echo "${0##*/}: download failed HTTP ${http_code}" >&2
  exit 1
fi

EXTRACT="$(mktemp -d "${OUT_DIR%/}/le-vibe-vscodium-extract.XXXXXX")"
trap 'rm -f "${ZIP}"; rm -rf "${EXTRACT}"' EXIT
unzip -q -o "$ZIP" -d "$EXTRACT"

TGZ=""
if [[ -f "${EXTRACT}/vscodium-linux-build.tar.gz" ]]; then
  TGZ="${EXTRACT}/vscodium-linux-build.tar.gz"
else
  TGZ="$(find "$EXTRACT" -maxdepth 3 -name 'vscodium-linux-build.tar.gz' -type f -print -quit)"
fi
if [[ -z "$TGZ" || ! -f "$TGZ" ]]; then
  echo "${0##*/}: vscodium-linux-build.tar.gz not found inside artifact zip — layout may have changed" >&2
  find "$EXTRACT" -maxdepth 4 -type f -print >&2 || true
  exit 1
fi

FINAL="${OUT_DIR%/}/vscodium-linux-build.tar.gz"
if [[ "$TGZ" != "$FINAL" ]]; then
  cp -f "$TGZ" "$FINAL"
fi
trap - EXIT
rm -f "${ZIP}"
rm -rf "${EXTRACT}"

echo "${0##*/}: wrote ${FINAL}"

if [[ "$DO_INSTALL" -eq 1 ]]; then
  exec "${ROOT}/packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh" "$FINAL" --yes
fi
