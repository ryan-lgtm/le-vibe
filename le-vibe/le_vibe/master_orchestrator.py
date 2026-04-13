"""STEP 16: extract the Master orchestrator fenced block from ``docs/PROMPT_BUILD_LE_VIBE.md``."""

from __future__ import annotations

from pathlib import Path


def extract_master_orchestrator_fence(repo_root: Path) -> str | None:
    """
    Return the fenced block whose first line starts with **You are the senior engineer for Lé Vibe**,
    or ``None`` if the file is missing or the fence is absent.
    """
    path = repo_root / "docs" / "PROMPT_BUILD_LE_VIBE.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for part in text.split("```"):
        if part.lstrip().startswith("You are the senior engineer for Lé Vibe"):
            return part.rstrip()
    return None
