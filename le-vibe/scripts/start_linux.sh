#!/usr/bin/env bash
set -euo pipefail
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"

if curl -fsS "http://${OLLAMA_HOST}/api/tags" >/dev/null 2>&1; then
  exit 0
fi

if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet ollama 2>/dev/null; then
    exit 0
  fi
  if systemctl --user is-active --quiet ollama 2>/dev/null; then
    exit 0
  fi
fi

if pgrep -x ollama >/dev/null 2>&1; then
  exit 0
fi

nohup ollama serve >>"${HOME}/.ollama-serve.log" 2>&1 &
disown || true
exit 0
