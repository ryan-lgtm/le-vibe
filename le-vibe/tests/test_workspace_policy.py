"""workspace-policy merge with user-settings (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.workspace_policy import get_cap_mb, load_policy, save_policy, set_workspace_cap_mb


def test_get_cap_mb_workspace_entry_beats_user_settings(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "ws"
    root.mkdir()
    (cfg / "user-settings.json").write_text(
        json.dumps({"lvibe_cap_mb_default": 80}),
        encoding="utf-8",
    )
    set_workspace_cap_mb(root, 200, config_dir=cfg)
    assert get_cap_mb(root, config_dir=cfg) == 200


def test_get_cap_mb_user_settings_over_policy_default(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "ws"
    root.mkdir()
    pol = load_policy(config_dir=cfg)
    pol["default_cap_mb"] = 40
    save_policy(pol, config_dir=cfg)
    (cfg / "user-settings.json").write_text(
        json.dumps({"lvibe_cap_mb_default": 120}),
        encoding="utf-8",
    )
    assert get_cap_mb(root, config_dir=cfg) == 120


def test_get_cap_mb_policy_when_user_settings_null(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "ws"
    root.mkdir()
    pol = load_policy(config_dir=cfg)
    pol["default_cap_mb"] = 88
    save_policy(pol, config_dir=cfg)
    (cfg / "user-settings.json").write_text(
        json.dumps({"lvibe_cap_mb_default": None}),
        encoding="utf-8",
    )
    assert get_cap_mb(root, config_dir=cfg) == 88
