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
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VSC="${ROOT}/editor/vscodium"
MERGE_JSON="${ROOT}/editor/le-vibe-overrides/product-branding-merge.json"
DEFAULTS_SH="${ROOT}/editor/le-vibe-overrides/build-env.lvibe-defaults.sh"

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
    echo "ci-vscodium-linux-dev-build: unexpected APP_NAME line in dev/build.sh — update packaging/scripts/ci-vscodium-linux-dev-build.sh" >&2
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

_lvibe_sync_linux_icon_assets
_lvibe_merge_vscodium_product_json
_lvibe_patch_dev_build_sh_for_env_defaults

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
