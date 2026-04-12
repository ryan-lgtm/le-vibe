"""Pytest defaults: workspace memory consent defaults to *accept* so tests stay hermetic."""

from __future__ import annotations

import os

# Undecided + non-interactive would skip `.lvibe/`; tests expect a prepared hub unless they override.
os.environ.setdefault("LE_VIBE_LVIBE_CONSENT", "accept")
