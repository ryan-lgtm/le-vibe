"""Pytest defaults: workspace memory consent defaults to *accept* so tests stay hermetic."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Undecided + non-interactive would skip `.lvibe/`; tests expect a prepared hub unless they override.
os.environ.setdefault("LE_VIBE_LVIBE_CONSENT", "accept")

# Global first-run + Continue preamble in launcher.main() is for real installs; tests invoke subcommands
# without pulling Ollama/bootstrap — keep prior hermetic behavior unless a test clears this.
os.environ.setdefault("LE_VIBE_SKIP_SESSION_PREAMBLE", "1")

# Ensure `import le_vibe` works when running `pytest` from monorepo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
