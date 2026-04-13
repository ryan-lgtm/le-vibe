#!/usr/bin/env bash
# H4 / STEP 7: ensure packaging/continue-openvsx-version contains a single semver line (reproducible Open VSX pin).
# Requires: grep, head, tr on PATH (STEP 14.h maintainer gate).
# Run from repo root: ./packaging/scripts/verify-continue-pin.sh
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); maintainer story: docs/continue-extension-pin.md; index: docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — STEP 7 H4 / 14.h Open VSX pin check after STEP 0–1.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PIN="${ROOT}/packaging/continue-openvsx-version"

if [[ ! -f "$PIN" ]]; then
  echo "verify-continue-pin: missing $PIN — restore packaging/continue-openvsx-version from git (H4 pin; see docs/continue-extension-pin.md)." >&2
  exit 1
fi

if ! command -v grep >/dev/null 2>&1; then
  echo "verify-continue-pin: grep not on PATH — install grep (e.g. sudo apt install grep) (docs/continue-extension-pin.md)." >&2
  exit 1
fi
if ! command -v head >/dev/null 2>&1; then
  echo "verify-continue-pin: head not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/continue-extension-pin.md)." >&2
  exit 1
fi
if ! command -v tr >/dev/null 2>&1; then
  echo "verify-continue-pin: tr not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/continue-extension-pin.md)." >&2
  exit 1
fi

LINE="$(grep -v '^[[:space:]]*#' "$PIN" | head -1 | tr -d '[:space:]\r')"
if [[ -z "$LINE" ]]; then
  echo "verify-continue-pin: no non-comment version line in $PIN — add one semver line (e.g. 1.2.3); see docs/continue-extension-pin.md." >&2
  exit 1
fi
if [[ ! "$LINE" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$ ]]; then
  echo "verify-continue-pin: expected semver (e.g. 1.2.3), got: $LINE — see docs/continue-extension-pin.md" >&2
  exit 1
fi

echo "verify-continue-pin: OK ($LINE)"
