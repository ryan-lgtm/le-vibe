#!/usr/bin/env bash
set -euo pipefail
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"

if curl -fsS "http://127.0.0.1:11434/api/tags" >/dev/null 2>&1; then
  exit 0
fi

if pgrep -x ollama >/dev/null 2>&1; then
  exit 0
fi

nohup ollama serve >>"${HOME}/.ollama-serve.log" 2>&1 &
disown || true
exit 0
