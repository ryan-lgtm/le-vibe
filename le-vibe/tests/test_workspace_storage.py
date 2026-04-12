"""Storage metering and compaction (PRODUCT_SPEC §5.4–5.5)."""

from __future__ import annotations

from pathlib import Path

from le_vibe.workspace_hub import ensure_lvibe_workspace
from le_vibe.workspace_storage import compact_lvibe_tree, refresh_storage_metadata


def test_compaction_removes_rag_refs_when_over_cap(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    refs = root / ".lvibe" / "rag" / "refs"
    fat = refs / "big.yaml"
    fat.write_bytes(b"x" * (3 * 1024 * 1024))
    actions = compact_lvibe_tree(root, cap_mb=1)
    assert any("removed" in a for a in actions)
    assert fat.exists() is False


def test_refresh_cap_from_user_settings_json(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    (cfg / "user-settings.json").write_text(
        '{"lvibe_cap_mb_default": 120}',
        encoding="utf-8",
    )
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    usage, cap = refresh_storage_metadata(root, config_dir=cfg)
    assert cap == 120
    data = (root / ".lvibe" / "storage-state.json").read_text(encoding="utf-8")
    assert "120" in data


def test_refresh_writes_storage_state_json(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    usage, cap = refresh_storage_metadata(root, config_dir=cfg)
    assert cap == 50
    assert usage > 0
    data = (root / ".lvibe" / "storage-state.json").read_text(encoding="utf-8")
    assert "usage_bytes" in data
    assert "50" in data
