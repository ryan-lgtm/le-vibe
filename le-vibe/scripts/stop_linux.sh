#!/usr/bin/env bash
set -euo pipefail
# Only stop if we started a user nohup serve; systemd users should: sudo systemctl stop ollama
if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet ollama 2>/dev/null; then
    echo "Ollama is managed by systemd (system). Run: sudo systemctl stop ollama"
    exit 0
  fi
  if systemctl --user is-active --quiet ollama 2>/dev/null; then
    systemctl --user stop ollama 2>/dev/null || true
    exit 0
  fi
fi
pkill -x ollama 2>/dev/null || true
echo "Stopped user ollama serve processes (if any)."
