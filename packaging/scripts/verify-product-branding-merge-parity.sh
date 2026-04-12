#!/usr/bin/env bash
# STEP 14 (§7.3): read-only check that jq-merge of editor/vscodium/product.json with
# editor/le-vibe-overrides/product-branding-merge.json yields expected v1 Lé Vibe product
# strings (same merge as packaging/scripts/ci-vscodium-linux-dev-build.sh).
#
# Does not write to editor/vscodium/ — use before or after prepare/compile when debugging branding.
# Requires: jq. See editor/le-vibe-overrides/product-branding-merge.json, docs/brand-assets.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="${ROOT}/editor/vscodium/product.json"
MERGE="${ROOT}/editor/le-vibe-overrides/product-branding-merge.json"

usage() {
  cat <<'EOF'
Usage: packaging/scripts/verify-product-branding-merge-parity.sh

Runs jq -s '.[0] * .[1]' on editor/vscodium/product.json and product-branding-merge.json in a
temporary file, then asserts .product.nameShort/nameLong/linuxIconName match §7.3 v1 branding.
Read-only; exits 0 on success, 1 on assertion failure, 2 if jq missing or inputs missing.

See packaging/scripts/ci-vscodium-linux-dev-build.sh (_lvibe_merge_vscodium_product_json).
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "verify-product-branding-merge-parity: jq not on PATH — install jq (e.g. sudo apt install jq)." >&2
  exit 2
fi
[[ -f "$SRC" ]] || {
  echo "verify-product-branding-merge-parity: missing ${SRC} — git submodule update --init editor/vscodium (editor/README.md 14.b)." >&2
  exit 2
}
[[ -f "$MERGE" ]] || {
  echo "verify-product-branding-merge-parity: missing ${MERGE}" >&2
  exit 2
}

tmp="$(mktemp)"
trap 'rm -f "${tmp}"' EXIT
jq -s '.[0] * .[1]' "$SRC" "$MERGE" >"${tmp}"

if ! jq -e \
  '.product
    | type == "object"
    and .nameShort == "Lé Vibe"
    and .nameLong == "Lé Vibe"
    and .linuxIconName == "le-vibe"' \
  "${tmp}" >/dev/null; then
  echo "verify-product-branding-merge-parity: merged product block does not match §7.3 v1 — inspect ${MERGE} and upstream ${SRC} (jq object merge)." >&2
  jq '.product' "${tmp}" >&2 || true
  exit 1
fi

echo "verify-product-branding-merge-parity: OK — merged .product matches Lé Vibe / le-vibe (read-only)."
