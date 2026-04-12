#!/usr/bin/env bash
# STEP 14 (14.e): invoke upstream VSCodium dev/build.sh from the monorepo (real compile).
# Run from repository root on a Linux machine with build deps installed (see editor/vscodium/docs/howto-build.md).
# After success: ./editor/verify-14c-local-binary.sh (14.c) or ./editor/print-built-codium-path.sh — editor/BUILD.md.
# CI: build-le-vibe-ide.yml job linux_compile — not run on pull_request (too slow for default runners).
# 14.a: active node must match editor/.nvmrc before dev/build.sh unless LEVIBE_SKIP_NODE_VERSION_CHECK=1.
# PRODUCT_SPEC §7.3: merge Lé Vibe product strings; patch dev/build.sh to honor env; source
#   editor/le-vibe-overrides/build-env.lvibe-defaults.sh, then optional build-env.sh (see build-env.sh.example).
# Authority: editor/BUILD.md, docs/vscodium-fork-le-vibe.md.
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md (requires editor/vscodium/ with product.json).
# Requires: grep, sed, mktemp, mv on PATH for §7.3 merge/patch helpers (before dev/build.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VSC="${ROOT}/editor/vscodium"
MERGE_JSON="${ROOT}/editor/le-vibe-overrides/product-branding-merge.json"
DEFAULTS_SH="${ROOT}/editor/le-vibe-overrides/build-env.lvibe-defaults.sh"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: packaging/scripts/ci-vscodium-linux-dev-build.sh

Run from the repository root. Applies §7.3 Lé Vibe layers then execs editor/vscodium/dev/build.sh:
  merge product-branding-merge.json into editor/vscodium/product.json (jq),
  sync-linux-icon-assets.sh, patch dev/build.sh for env-driven APP_NAME, optional build-env*.sh,
  optional Node vs editor/.nvmrc check (14.a).

Environment:
  LEVIBE_SKIP_NODE_VERSION_CHECK      Set to 1 to skip active node vs editor/.nvmrc check.
  LEVIBE_VSCODIUM_PREPARE_ONLY        Set to 1 to apply §7.3 merge, Linux icons, and dev/build.sh
                                      patch, then exit without running dev/build.sh (no compile).
  LEVIBE_SKIP_HOST_DEPS_CHECK         Set to 1 to skip packaging/scripts/check-linux-vscodium-build-deps.sh
                                      (Linux full compile only; CI installs apt deps before this script).

Authority: editor/BUILD.md (Linux icons, 14.e), docs/vscodium-fork-le-vibe.md.
EOF
  exit 0
fi

_lvibe_merge_vscodium_product_json() {
  [[ -f "${MERGE_JSON}" ]] || return 0
  command -v jq >/dev/null 2>&1 || {
    echo "ci-vscodium-linux-dev-build: jq required for product-branding-merge.json — install: sudo apt install jq (Debian/Ubuntu)" >&2
    exit 1
  }
  local tmp
  tmp="$(mktemp)"
  jq -s '.[0] * .[1]' "${VSC}/product.json" "${MERGE_JSON}" >"${tmp}"
  mv "${tmp}" "${VSC}/product.json"
  echo "ci-vscodium-linux-dev-build: merged editor/le-vibe-overrides/product-branding-merge.json into editor/vscodium/product.json"
}

_lvibe_sync_linux_icon_assets() {
  bash "${ROOT}/editor/le-vibe-overrides/sync-linux-icon-assets.sh"
}

_lvibe_patch_dev_build_sh_for_env_defaults() {
  local f="${VSC}/dev/build.sh"
  if grep -q 'export APP_NAME="${APP_NAME:-VSCodium}"' "${f}" 2>/dev/null; then
    return 0
  fi
  if ! grep -q '^export APP_NAME="VSCodium"$' "${f}"; then
    echo "ci-vscodium-linux-dev-build: unexpected APP_NAME line in dev/build.sh — upstream layout may have changed; update _lvibe_patch_dev_build_sh_for_env_defaults in packaging/scripts/ci-vscodium-linux-dev-build.sh (after an editor/vscodium submodule bump)." >&2
    return 1
  fi
  sed -i.bak_lvibe \
    -e 's/^export APP_NAME="VSCodium"$/export APP_NAME="${APP_NAME:-VSCodium}"/' \
    -e 's/^export ASSETS_REPOSITORY="VSCodium\/vscodium"$/export ASSETS_REPOSITORY="${ASSETS_REPOSITORY:-VSCodium\/vscodium}"/' \
    -e 's/^export BINARY_NAME="codium"$/export BINARY_NAME="${BINARY_NAME:-codium}"/' \
    -e 's/^export GH_REPO_PATH="VSCodium\/vscodium"$/export GH_REPO_PATH="${GH_REPO_PATH:-VSCodium\/vscodium}"/' \
    -e 's/^export ORG_NAME="VSCodium"$/export ORG_NAME="${ORG_NAME:-VSCodium}"/' \
    "${f}"
  echo "ci-vscodium-linux-dev-build: patched editor/vscodium/dev/build.sh so APP_NAME/ORG_NAME/etc. honor environment (§7.3)"
}

[[ -f "${VSC}/product.json" ]] || {
  echo "ci-vscodium-linux-dev-build: expected editor/vscodium/product.json — run: git submodule update --init editor/vscodium (Fresh clone 14.b: editor/README.md)." >&2
  exit 1
}
[[ -x "${VSC}/dev/build.sh" ]] || {
  echo "ci-vscodium-linux-dev-build: dev/build.sh missing or not executable under ${VSC}/ — repair editor/vscodium (Fresh clone 14.b: git submodule update --init editor/vscodium — editor/README.md)." >&2
  exit 1
}

if ! command -v grep >/dev/null 2>&1; then
  echo "ci-vscodium-linux-dev-build: grep not on PATH — install grep (e.g. sudo apt install grep) (editor/BUILD.md 14.e)." >&2
  exit 1
fi
if ! command -v sed >/dev/null 2>&1; then
  echo "ci-vscodium-linux-dev-build: sed not on PATH — install sed (e.g. sudo apt install sed) (editor/BUILD.md 14.e)." >&2
  exit 1
fi
if ! command -v mktemp >/dev/null 2>&1; then
  echo "ci-vscodium-linux-dev-build: mktemp not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.e)." >&2
  exit 1
fi
if ! command -v mv >/dev/null 2>&1; then
  echo "ci-vscodium-linux-dev-build: mv not on PATH — install coreutils (e.g. sudo apt install coreutils) (editor/BUILD.md 14.e)." >&2
  exit 1
fi

# Full compile only: fail fast before mutating editor/vscodium/ when apt packages / pkg-config
# do not match build-le-vibe-ide.yml (native-keymap, etc.). Skipped for prepare-only and non-Linux.
if [[ "${LEVIBE_VSCODIUM_PREPARE_ONLY:-}" != "1" && "${LEVIBE_SKIP_HOST_DEPS_CHECK:-}" != "1" && "$(uname -s)" == "Linux" ]]; then
  echo "ci-vscodium-linux-dev-build: Linux host dependency preflight (check-linux-vscodium-build-deps.sh)..."
  if ! "${ROOT}/packaging/scripts/check-linux-vscodium-build-deps.sh"; then
    echo "ci-vscodium-linux-dev-build: install packages from the hint above, or LEVIBE_SKIP_HOST_DEPS_CHECK=1 to continue at your own risk (editor/BUILD.md 14.e)." >&2
    exit 1
  fi
fi

_lvibe_sync_linux_icon_assets
_lvibe_merge_vscodium_product_json
_lvibe_patch_dev_build_sh_for_env_defaults

if [[ "${LEVIBE_VSCODIUM_PREPARE_ONLY:-}" == "1" ]]; then
  echo "ci-vscodium-linux-dev-build: LEVIBE_VSCODIUM_PREPARE_ONLY=1 — §7.3 product merge, Linux icons, and dev/build.sh env patch applied; not invoking dev/build.sh."
  echo "ci-vscodium-linux-dev-build: Next: ./editor/fetch-vscode-sources.sh if editor/vscodium/vscode/ is missing, then re-run without LEVIBE_VSCODIUM_PREPARE_ONLY for the compile (editor/BUILD.md 14.e)."
  exit 0
fi

cd "${VSC}"

if [[ "${LEVIBE_SKIP_NODE_VERSION_CHECK:-}" != "1" ]]; then
  _nvmrc="${ROOT}/editor/.nvmrc"
  if [[ ! -f "${_nvmrc}" ]]; then
    echo "ci-vscodium-linux-dev-build: missing ${_nvmrc} — restore from git; Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md; align pins per packaging/scripts/ci-editor-nvmrc-sync.sh (14.a)." >&2
    exit 1
  fi
  IFS= read -r _want < "${_nvmrc}" || true
  _want="${_want//$'\r'/}"
  if [[ -z "${_want}" ]]; then
    echo "ci-vscodium-linux-dev-build: empty ${_nvmrc} — set a Node version line; must match editor/vscodium/.nvmrc after a vendor bump (14.a)." >&2
    exit 1
  fi
  if ! command -v node >/dev/null 2>&1; then
    echo "ci-vscodium-linux-dev-build: node not on PATH — source editor/use-node-toolchain.sh (14.a) or install Node ${_want}" >&2
    exit 1
  fi
  _have="$(node --version | sed 's/^v//')"
  if [[ "${_want}" != "${_have}" ]]; then
    echo "ci-vscodium-linux-dev-build: active Node ${_have} != editor/.nvmrc ${_want} — run: source editor/use-node-toolchain.sh (14.a), or LEVIBE_SKIP_NODE_VERSION_CHECK=1 to override" >&2
    exit 1
  fi
fi

if [[ -f "${DEFAULTS_SH}" ]]; then
  echo "ci-vscodium-linux-dev-build: sourcing editor/le-vibe-overrides/build-env.lvibe-defaults.sh"
  set -a
  # shellcheck disable=SC1091
  . "${DEFAULTS_SH}"
  set +a
fi

if [[ -f "${ROOT}/editor/le-vibe-overrides/build-env.sh" ]]; then
  echo "ci-vscodium-linux-dev-build: sourcing editor/le-vibe-overrides/build-env.sh"
  set -a
  # shellcheck disable=SC1091
  . "${ROOT}/editor/le-vibe-overrides/build-env.sh"
  set +a
fi

exec ./dev/build.sh
