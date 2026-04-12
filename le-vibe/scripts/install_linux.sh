#!/usr/bin/env bash
set -euo pipefail
# Official Ollama install — https://github.com/ollama/ollama
if [[ "${BOOTSTRAP_YES:-}" == "1" ]]; then
  export DEBIAN_FRONTEND=noninteractive
fi
curl -fsSL https://ollama.com/install.sh | sh
