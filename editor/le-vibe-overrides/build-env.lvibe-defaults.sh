# Lé Vibe IDE — default build exports (PRODUCT_SPEC §7.3).
# Sourced by packaging/scripts/ci-vscodium-linux-dev-build.sh after dev/build.sh is patched
# to honor ${VAR:-upstream defaults}, and before optional build-env.sh (local overrides).
# BINARY_NAME stays codium; public CLI for the stack remains lvibe (launcher), not a second PATH name.
# Master orchestrator: 0 → 1 → 14 → 2–13 → 15–17 — docs/PROMPT_BUILD_LE_VIBE.md (ORDERED WORK QUEUE, Rolling iteration); docs/PM_STAGE_MAP.md (Execution order / STEP 16) — §7.3 default branding exports after STEP 0–1.
# Pytest: le-vibe/tests/test_build_env_lvibe_defaults_step14_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -a
export APP_NAME="Lé Vibe"
export ORG_NAME="Le Vibe"
set +a
