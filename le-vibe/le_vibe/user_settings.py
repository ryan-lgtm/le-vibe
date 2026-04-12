"""Optional global user settings under ``~/.config/le-vibe/user-settings.json`` (**docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md**)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import le_vibe_config_dir
from .workspace_policy import DEFAULT_CAP_MB, clamp_cap_mb

USER_SETTINGS_FILENAME = "user-settings.json"


def default_user_settings() -> dict[str, Any]:
    return {
        "schema_version": "user-settings.v1",
        "lvibe_cap_mb_default": None,
        "model": {
            "use_recommended": True,
            "override_tag": None,
            "allow_pull_if_disk_ok": True,
        },
        "ide": {
            "show_chat_commands_help": True,
            "show_new_workspace_hints": True,
        },
    }


def load_user_settings(*, config_dir: Path | None = None) -> dict[str, Any]:
    """Load merged user settings; missing file → defaults only."""
    base = default_user_settings()
    p = (config_dir or le_vibe_config_dir()) / USER_SETTINGS_FILENAME
    if not p.is_file():
        return base
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return base
    if not isinstance(raw, dict):
        return base
    merged = _deep_merge(base, raw)
    cap = merged.get("lvibe_cap_mb_default")
    if cap is not None:
        merged["lvibe_cap_mb_default"] = clamp_cap_mb(cap)
    return merged


def _deep_merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def effective_default_cap_mb(settings: dict[str, Any] | None) -> int:
    """Cap MB for new workspaces when policy does not override (PRODUCT_SPEC §5)."""
    if settings is None:
        return DEFAULT_CAP_MB
    raw = settings.get("lvibe_cap_mb_default")
    if raw is None:
        return DEFAULT_CAP_MB
    return clamp_cap_mb(raw)
