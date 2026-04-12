#!/usr/bin/env bash
# P3: Lé Vibe does not rebuild Code - OSS here; CI/smoke uses an existing editor (VSCodium).
# Exit 0 when a suitable binary is present so pipelines can "check then proceed".
# Product / trust: docs/PRODUCT_SPEC.md §8–§9; spec-phase2.md §14 (H6/H7 vs in-tree; STEP 14 E1 — editor/le-vibe-overrides/README.md + le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); docs/README.md (§9 Maintainer index; H8 — .github/ (ci.yml, dependabot.yml, ISSUE_TEMPLATE + config.yml # H8); SECURITY; privacy-and-telemetry E1).
# Full E1 pytest roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
set -euo pipefail
BIN="${LE_VIBE_EDITOR:-/usr/bin/codium}"
if [ -x "$BIN" ]; then
  echo "le-vibe: editor binary present: $BIN"
  exit 0
fi
if command -v codium >/dev/null 2>&1; then
  echo "le-vibe: editor on PATH: $(command -v codium)"
  exit 0
fi
echo "le-vibe: no codium found — install VSCodium (package name varies) or set LE_VIBE_EDITOR." >&2
echo "See README.md (Debian / upstream editor)." >&2
exit 1
