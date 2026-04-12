# Lé Vibe IDE — default build exports (PRODUCT_SPEC §7.3).
# Sourced by packaging/scripts/ci-vscodium-linux-dev-build.sh after dev/build.sh is patched
# to honor ${VAR:-upstream defaults}, and before optional build-env.sh (local overrides).
# BINARY_NAME stays codium; public CLI for the stack remains lvibe (launcher), not a second PATH name.
set -a
export APP_NAME="Lé Vibe"
export ORG_NAME="Le Vibe"
set +a
