#!/usr/bin/env bash
set -euo pipefail
pkill -x ollama 2>/dev/null || true
echo "Stopped ollama processes (if any). Quit Ollama from the menu bar if it was launched as an app."
