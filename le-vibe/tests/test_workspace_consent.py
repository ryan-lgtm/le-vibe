"""Consent gate and policy persistence (PRODUCT_SPEC §5.1)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.workspace_hub import prepare_workspaces_for_editor_args


def test_decline_skips_lvibe_and_persists(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    proj = tmp_path / "proj"
    proj.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.chdir(proj)
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "decline")
    prepare_workspaces_for_editor_args(["."])
    assert not (proj / ".lvibe").exists()
    pol = json.loads((cfg / "workspace-policy.json").read_text(encoding="utf-8"))
    key = str(proj.resolve())
    assert pol["workspaces"][key]["consent"] == "declined"


def test_invalid_env_consent_logs_and_skips_without_folder(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    proj = tmp_path / "proj"
    proj.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.chdir(proj)
    captured: list[dict] = []

    def _cap(component: str, event: str, **fields: object) -> None:
        captured.append({"component": component, "event": event, **fields})

    monkeypatch.setattr("le_vibe.workspace_consent.append_structured_log", _cap)
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "surprise-me")
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    from le_vibe.workspace_consent import resolve_lvibe_creation

    assert resolve_lvibe_creation(proj) is False
    assert not (proj / ".lvibe").exists()
    assert any(x.get("reason") == "invalid_env_value" for x in captured)


def test_accept_creates_lvibe_and_storage_state(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    proj = tmp_path / "proj"
    proj.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.chdir(proj)
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "accept")
    prepare_workspaces_for_editor_args(["."])
    assert (proj / ".lvibe" / "storage-state.json").is_file()
    pol = json.loads((cfg / "workspace-policy.json").read_text(encoding="utf-8"))
    assert pol["workspaces"][str(proj.resolve())]["consent"] == "accepted"
