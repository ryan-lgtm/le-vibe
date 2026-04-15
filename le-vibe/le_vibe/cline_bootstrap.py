"""Cline bootstrap policy seeded into workspaces.

This template forces startup context reads from `.lvibe/` before edits.
"""

from __future__ import annotations

from pathlib import Path

CLINE_BOOTSTRAP_RULE_NAME = "00-le-vibe-bootstrap.md"


def _cline_bootstrap_body() -> str:
    return (
        "# Lé Vibe Cline bootstrap policy\n\n"
        "Before making edits, read project context in this order:\n\n"
        "1. `.lvibe/session-manifest.json`\n"
        "2. `.lvibe/IDE_FIRST_REPO_CLEANUP_BACKLOG.md` (if present)\n"
        "3. Relevant `.lvibe/**/*.md` files tied to the active task scope\n\n"
        "Execution rules:\n\n"
        "- Select the active epic/task from `product.epics` in `.lvibe/session-manifest.json`.\n"
        "- Stay scoped to the delegated task; avoid unrelated refactors.\n"
        "- If blocked by missing decisions, report blocker + explicit unblock action.\n"
    )


def ensure_cline_bootstrap_rule(workspace_root: Path) -> Path:
    """Create `.clinerules/00-le-vibe-bootstrap.md` when missing (idempotent)."""
    rules_dir = workspace_root / ".clinerules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    dest = rules_dir / CLINE_BOOTSTRAP_RULE_NAME
    if not dest.exists():
        dest.write_text(_cline_bootstrap_body(), encoding="utf-8")
    return dest
