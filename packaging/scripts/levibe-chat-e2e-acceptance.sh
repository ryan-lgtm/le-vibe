#!/usr/bin/env bash
# CP6 single entrypoint from monorepo root: extension automated acceptance (task-cp6-1).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXT="${ROOT}/editor/le-vibe-native-extension"
cd "${EXT}"
exec npm run e2e-acceptance
