#!/usr/bin/env bash
# Invoked by .desktop or manually; sets PYTHONPATH for an uninstalled tree checkout.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m le_vibe.launcher "$@"
