#!/usr/bin/env python3
"""Print the Master iteration loop fenced block from docs/MASTER_ITERATION_LOOP.md (stdout = paste into Cursor).

E1: le-vibe/tests/test_master_iteration_loop_fence.py
"""

from __future__ import annotations

from pathlib import Path


def _master_iteration_loop_fence(repo_root: Path) -> str:
    text = (repo_root / "docs" / "MASTER_ITERATION_LOOP.md").read_text(encoding="utf-8")
    for part in text.split("```"):
        stripped = part.lstrip()
        if stripped.startswith("You are the Lé Vibe master iteration loop"):
            return part
    raise RuntimeError("Master iteration loop fenced block not found in docs/MASTER_ITERATION_LOOP.md")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    block = _master_iteration_loop_fence(repo_root)
    print(block.rstrip())


if __name__ == "__main__":
    main()
