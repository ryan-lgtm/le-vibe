#!/usr/bin/env bash
set -euo pipefail
# Official Ollama install — https://github.com/ollama/ollama
FORCE=0
case "${1:-}" in
  --force) FORCE=1 ;;
  "" ) ;;
  *)
    echo "install_linux.sh: unknown argument: ${1:-} (expected --force)" >&2
    exit 2
    ;;
esac

if [[ "$FORCE" -ne 1 ]] && command -v ollama >/dev/null 2>&1; then
  echo "install_linux.sh: ollama already available on PATH at $(command -v ollama); skipping reinstall."
  exit 0
fi

if [[ "${BOOTSTRAP_YES:-}" == "1" ]]; then
  export DEBIAN_FRONTEND=noninteractive
fi
curl -fsSL https://ollama.com/install.sh | sh
