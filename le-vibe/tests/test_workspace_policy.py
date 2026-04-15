"""workspace-policy merge with user-settings (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.workspace_policy import (
    cap_mb_from_environ,
    get_cap_mb,
    load_policy,
    save_policy,
    set_workspace_cap_mb,
)


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


def test_cap_mb_from_environ_none_when_unset_or_empty(monkeypatch) -> None:
    monkeypatch.delenv("LE_VIBE_LVIBE_CAP_MB", raising=False)
    assert cap_mb_from_environ() is None
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "   ")
    assert cap_mb_from_environ() is None


def test_cap_mb_from_environ_parses_integer(monkeypatch) -> None:
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "99")
    assert cap_mb_from_environ() == 99


def test_cap_mb_from_environ_clamps_to_min_max(monkeypatch) -> None:
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "3")
    assert cap_mb_from_environ() == 10
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "99999")
    assert cap_mb_from_environ() == 500


def test_cap_mb_from_environ_invalid_returns_none(monkeypatch) -> None:
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "not-a-number")
    assert cap_mb_from_environ() is None
