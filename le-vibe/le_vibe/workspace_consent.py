"""Consent gate for creating ``.lvibe/`` (PRODUCT_SPEC §5.1)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .structured_log import append_structured_log
from .workspace_policy import (
    get_consent,
    set_consent,
    workspace_key,
)

_CONSENT_BANNER = """\
Lé Vibe — local workspace memory (`.lvibe/`)

This optional folder holds small markdown + RAG-style notes for AI agents on your disk.
It stays local, is listed in `.gitignore` when a `.gitignore` exists, and is capped by a
per-workspace size budget (default 50 MB; configurable).

"""


def _env_consent_override() -> str | None:
    raw = os.environ.get("LE_VIBE_LVIBE_CONSENT", "").strip().lower()
    if not raw:
        return None
    if raw in ("accept", "accepted", "yes", "y", "1", "true"):
        return "accept"
    if raw in ("decline", "declined", "no", "n", "0", "false"):
        return "decline"
    return None


def resolve_lvibe_creation(
    workspace_root: Path,
    *,
    config_dir: Path | None = None,
) -> bool:
    """
    Return True if the launcher may create ``.lvibe/`` for this workspace.

    Persists **accept** and **decline** when the user (or ``LE_VIBE_LVIBE_CONSENT``) decides.
    If undecided and stdin is not a TTY, does **not** create and does **not** persist (user
    can be prompted on a later interactive launch).
    """
    key = workspace_key(workspace_root)
    existing = get_consent(workspace_root, config_dir=config_dir)
    if existing == "declined":
        append_structured_log("workspace", "lvibe_consent_skip", workspace=key, reason="stored_decline")
        return False
    if existing == "accepted":
        return True

    env = _env_consent_override()
    if env == "accept":
        set_consent(workspace_root, "accepted", config_dir=config_dir)
        append_structured_log("workspace", "lvibe_consent", workspace=key, decision="accept", source="env")
        return True
    if env == "decline":
        set_consent(workspace_root, "declined", config_dir=config_dir)
        append_structured_log("workspace", "lvibe_consent", workspace=key, decision="decline", source="env")
        return False

    if sys.stdin.isatty():
        print(_CONSENT_BANNER, file=sys.stderr, end="")
        try:
            line = input("Enable Lé Vibe workspace memory for this folder? [y/N]: ")
        except EOFError:
            line = ""
        ok = line.strip().lower() in ("y", "yes")
        if ok:
            set_consent(workspace_root, "accepted", config_dir=config_dir)
            append_structured_log("workspace", "lvibe_consent", workspace=key, decision="accept", source="prompt")
            return True
        set_consent(workspace_root, "declined", config_dir=config_dir)
        append_structured_log("workspace", "lvibe_consent", workspace=key, decision="decline", source="prompt")
        return False

    append_structured_log(
        "workspace",
        "lvibe_consent_skip",
        workspace=key,
        reason="non_interactive_undecided",
    )
    return False
