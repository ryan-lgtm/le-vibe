"""STEP 15: ``lvibe workspace-governance`` JSON + human output contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.workspace_hub import ensure_lvibe_workspace
from le_vibe.workspace_storage import refresh_storage_metadata


def test_workspace_governance_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["workspace_root"] == str(tmp_path.resolve())
    assert data["consent"] is None
    assert data["cap_mb_effective"] >= 10
    assert data["usage_bytes"] == 0
    assert data["within_cap"] is True
    assert "policy_file" in data


def test_workspace_governance_human(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "STEP 15" in out
    assert "Consent:" in out
    assert str(tmp_path.resolve()) in out


def test_workspace_governance_json_promotes_storage_health_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    ws = tmp_path / "w"
    ws.mkdir()
    ensure_lvibe_workspace(ws)
    refresh_storage_metadata(ws, config_dir=cfg)

    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "--workspace", str(ws), "--json"])
    assert launcher.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["storage_pressure_state"] in ("ok", "near_cap", "over_cap")
    assert "last_compaction_at" in payload
    assert "compaction_actions_count" in payload


def test_workspace_governance_json_compaction_fields_reflect_storage_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "10")
    ws = tmp_path / "w"
    ws.mkdir()
    ensure_lvibe_workspace(ws)
    fat = ws / ".lvibe" / "rag" / "refs" / "big.yaml"
    fat.parent.mkdir(parents=True, exist_ok=True)
    fat.write_bytes(b"x" * (15 * 1024 * 1024))
    refresh_storage_metadata(ws, config_dir=cfg)

    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "--workspace", str(ws), "--json"])
    assert launcher.main() == 0
    payload = json.loads(capsys.readouterr().out)
    state = payload["storage_state"]
    assert isinstance(state, dict)
    assert payload["storage_pressure_state"] == state.get("storage_pressure_state")
    assert payload["last_compaction_at"] == state.get("last_compaction_at")
    assert payload["compaction_actions_count"] == state.get("compaction_actions_count")
