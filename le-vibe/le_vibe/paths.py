"""XDG and Lé Vibe product paths."""

from __future__ import annotations

import os
from pathlib import Path

# Dedicated listen port for Lé Vibe–managed Ollama (spec-phase2 §7.2-A); avoids clashing with 11434.
LE_VIBE_MANAGED_OLLAMA_PORT: int = 11435


def le_vibe_config_dir() -> Path:
    """Return `~/.config/le-vibe/` (XDG_CONFIG_HOME respected)."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    d = base / "le-vibe"
    d.mkdir(parents=True, exist_ok=True)
    return d


def managed_ollama_state_path() -> Path:
    return le_vibe_config_dir() / "managed_ollama.json"
