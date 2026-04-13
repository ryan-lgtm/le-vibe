"""Pytest defaults: workspace memory consent defaults to *accept* so tests stay hermetic."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Undecided + non-interactive would skip `.lvibe/`; tests expect a prepared hub unless they override.
os.environ.setdefault("LE_VIBE_LVIBE_CONSENT", "accept")

# Ensure `import le_vibe` works when running `pytest` from monorepo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
