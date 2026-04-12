#!/usr/bin/env python3
"""Print the PM Debian build iteration fenced block from docs/PM_DEB_BUILD_ITERATION.md (stdout = paste into Cursor)."""

from __future__ import annotations

from pathlib import Path


def _fence(repo_root: Path) -> str:
    text = (repo_root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    for part in text.split("```"):
        stripped = part.lstrip()
        if stripped.startswith("You are the Lé Vibe **packaging / .deb build**"):
            return part
    raise RuntimeError("PM_DEB_BUILD_ITERATION.md: packaging engineer fenced block not found")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    print(_fence(repo_root).rstrip())


if __name__ == "__main__":
    main()
