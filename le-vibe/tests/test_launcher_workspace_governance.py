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
    monkeypatch.delenv("LE_VIBE_LVIBE_CAP_MB", raising=False)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["workspace_root"] == str(tmp_path.resolve())
    assert data["consent"] is None
    assert data["cap_mb_effective"] >= 10
    assert data["cap_mb_env_override"] is None
    assert data["usage_bytes"] == 0
    assert data["within_cap"] is True
    assert "policy_file" in data


def test_workspace_governance_json_reflects_le_vibe_lvibe_cap_mb_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "88")
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["cap_mb_effective"] == 88
    assert data["cap_mb_env_override"] == 88


def test_workspace_governance_json_declined_consent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    ws = tmp_path / "declined-ws"
    ws.mkdir()
    key = str(ws.resolve())
    (cfg / "workspace-policy.json").write_text(
        json.dumps(
            {"version": 1, "default_cap_mb": 50, "workspaces": {key: {"consent": "declined"}}},
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(ws), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["consent"] == "declined"


def test_workspace_governance_json_accepted_consent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    ws = tmp_path / "accepted-ws"
    ws.mkdir()
    key = str(ws.resolve())
    (cfg / "workspace-policy.json").write_text(
        json.dumps(
            {"version": 1, "default_cap_mb": 50, "workspaces": {key: {"consent": "accepted"}}},
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(ws), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["consent"] == "accepted"


def test_workspace_governance_human(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.delenv("LE_VIBE_LVIBE_CAP_MB", raising=False)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "STEP 15" in out
    assert "Consent: undecided" in out
    assert str(tmp_path.resolve()) in out
    assert "Cap (effective):" in out
    assert "LE_VIBE_LVIBE_CAP_MB" not in out
    assert "Usage:" in out
    assert "Within cap:" in out
    assert "storage-state.json:" in out


def test_workspace_governance_human_shows_env_cap_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "42")
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "Cap (effective): 42 MB (LE_VIBE_LVIBE_CAP_MB=42)" in out


def test_workspace_governance_human_shows_declined_consent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    ws = tmp_path / "declined-human"
    ws.mkdir()
    key = str(ws.resolve())
    (cfg / "workspace-policy.json").write_text(
        json.dumps(
            {"version": 1, "default_cap_mb": 50, "workspaces": {key: {"consent": "declined"}}},
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(ws)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "Consent: declined" in out


def test_workspace_governance_human_shows_accepted_consent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    ws = tmp_path / "accepted-human"
    ws.mkdir()
    key = str(ws.resolve())
    (cfg / "workspace-policy.json").write_text(
        json.dumps(
            {"version": 1, "default_cap_mb": 50, "workspaces": {key: {"consent": "accepted"}}},
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(ws)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "Consent: accepted" in out


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


_BAD_WS_PROBE = "lvibe-ws-governance-bad-resolve-probe"


def test_workspace_governance_bad_workspace_returns_2(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """``Path.resolve`` OSError → exit 2 (launcher._cmd_workspace_governance)."""
    _real_resolve = Path.resolve

    def _resolve(self: Path, *args: object, **kwargs: object) -> Path:
        if _BAD_WS_PROBE in str(self):
            raise OSError("simulated resolve failure")
        return _real_resolve(self, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", _resolve)
    monkeypatch.setattr(
        sys,
        "argv",
        ["launcher", "workspace-governance", "-C", f"/tmp/{_BAD_WS_PROBE}"],
    )
    assert launcher.main() == 2
    err = capsys.readouterr().err
    assert "bad --workspace" in err
    assert "simulated resolve failure" in err
