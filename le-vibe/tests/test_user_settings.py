"""Optional ~/.config/le-vibe/user-settings.json (PM_IDE_SETTINGS_AND_WORKFLOWS.md)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.user_settings import (
    default_user_settings,
    effective_default_cap_mb,
    load_user_settings,
)


def test_default_user_settings_shape():
    d = default_user_settings()
    assert d["schema_version"] == "user-settings.v1"
    assert d["model"]["use_recommended"] is True


def test_load_user_settings_merge(tmp_path: Path):
    p = tmp_path / "user-settings.json"
    p.write_text(
        json.dumps(
            {
                "lvibe_cap_mb_default": 120,
                "model": {"override_tag": "mistral:latest", "use_recommended": False},
            }
        ),
        encoding="utf-8",
    )
    raw = load_user_settings(config_dir=tmp_path)
    assert raw["model"]["override_tag"] == "mistral:latest"
    assert raw["model"]["use_recommended"] is False
    assert raw["lvibe_cap_mb_default"] == 120


def test_effective_default_cap_mb():
    assert effective_default_cap_mb(None) == 50
    assert effective_default_cap_mb({"lvibe_cap_mb_default": 80}) == 80
