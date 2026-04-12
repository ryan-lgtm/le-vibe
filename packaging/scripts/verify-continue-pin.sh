#!/usr/bin/env bash
# H4: ensure packaging/continue-openvsx-version contains a single semver line (reproducible Open VSX pin).
# Run from repo root: ./packaging/scripts/verify-continue-pin.sh
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree); maintainer story: docs/continue-extension-pin.md; index: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PIN="${ROOT}/packaging/continue-openvsx-version"

if [[ ! -f "$PIN" ]]; then
  echo "verify-continue-pin: missing $PIN" >&2
  exit 1
fi

LINE="$(grep -v '^[[:space:]]*#' "$PIN" | head -1 | tr -d '[:space:]\r')"
if [[ -z "$LINE" ]]; then
  echo "verify-continue-pin: no non-comment version line in $PIN" >&2
  exit 1
fi
if [[ ! "$LINE" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$ ]]; then
  echo "verify-continue-pin: expected semver (e.g. 1.2.3), got: $LINE" >&2
  exit 1
fi

echo "verify-continue-pin: OK ($LINE)"
