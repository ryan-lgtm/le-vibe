"""Storage metering and compaction (PRODUCT_SPEC §5.4–5.5)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.workspace_hub import ensure_lvibe_workspace
from le_vibe.workspace_storage import compact_lvibe_tree, lvibe_tree_usage_bytes, refresh_storage_metadata


def test_compaction_preserves_rag_readme_when_trimming_refs(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    readme = root / ".lvibe" / "rag" / "README.md"
    assert readme.is_file()
    fat = root / ".lvibe" / "rag" / "refs" / "big.yaml"
    fat.write_bytes(b"x" * (3 * 1024 * 1024))
    compact_lvibe_tree(root, cap_mb=1)
    assert readme.is_file()
    assert not fat.exists()


def test_compaction_removes_stray_large_file_under_rag(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    stray = root / ".lvibe" / "rag" / "fat.bin"
    stray.write_bytes(b"z" * (3 * 1024 * 1024))
    compact_lvibe_tree(root, cap_mb=1)
    assert not stray.exists()


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
    payload = json.loads(data)
    assert payload["compaction_actions_count"] == 0
    assert payload["compaction_warning"] is False
    assert payload["last_compaction_at"] is None
    assert payload["storage_pressure_state"] == "ok"


def test_refresh_records_compaction_metadata_when_over_cap(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setattr("le_vibe.workspace_policy.le_vibe_config_dir", lambda: cfg)
    monkeypatch.setenv("LE_VIBE_LVIBE_CAP_MB", "10")
    root = tmp_path / "w"
    root.mkdir()
    ensure_lvibe_workspace(root)
    fat = root / ".lvibe" / "rag" / "refs" / "big.yaml"
    fat.parent.mkdir(parents=True, exist_ok=True)
    fat.write_bytes(b"x" * (15 * 1024 * 1024))

    refresh_storage_metadata(root, config_dir=cfg)

    payload = json.loads((root / ".lvibe" / "storage-state.json").read_text(encoding="utf-8"))
    assert payload["compaction_actions_count"] >= 1
    assert payload["compaction_warning"] in (True, False)
    assert isinstance(payload["last_compaction_at"], str)
    assert payload["last_compaction_at"]
    assert payload["storage_pressure_state"] in ("ok", "near_cap", "over_cap")


def test_write_storage_state_reports_near_cap_pressure(tmp_path: Path) -> None:
    from le_vibe.workspace_storage import write_storage_state

    root = tmp_path / "w"
    lv = root / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    write_storage_state(root, cap_mb=10, usage_bytes=9 * 1024 * 1024)
    payload = json.loads((lv / "storage-state.json").read_text(encoding="utf-8"))
    assert payload["storage_pressure_state"] == "near_cap"


def test_write_storage_state_exact_cap_is_near_cap_not_over(tmp_path: Path) -> None:
    from le_vibe.workspace_storage import write_storage_state

    root = tmp_path / "w"
    lv = root / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    cap_bytes = 10 * 1024 * 1024
    write_storage_state(root, cap_mb=10, usage_bytes=cap_bytes)
    payload = json.loads((lv / "storage-state.json").read_text(encoding="utf-8"))
    assert payload["storage_pressure_state"] == "near_cap"


def test_write_storage_state_one_byte_over_cap_is_over_cap(tmp_path: Path) -> None:
    from le_vibe.workspace_storage import write_storage_state

    root = tmp_path / "w"
    lv = root / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    cap_bytes = 10 * 1024 * 1024
    write_storage_state(root, cap_mb=10, usage_bytes=cap_bytes + 1)
    payload = json.loads((lv / "storage-state.json").read_text(encoding="utf-8"))
    assert payload["storage_pressure_state"] == "over_cap"


def test_write_storage_state_zero_cap_reports_over_cap(tmp_path: Path) -> None:
    from le_vibe.workspace_storage import write_storage_state

    root = tmp_path / "w"
    lv = root / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    write_storage_state(root, cap_mb=0, usage_bytes=0)
    payload = json.loads((lv / "storage-state.json").read_text(encoding="utf-8"))
    assert payload["storage_pressure_state"] == "over_cap"


def test_lvibe_tree_usage_bytes_zero_without_dot_lvibe(tmp_path: Path) -> None:
    assert lvibe_tree_usage_bytes(tmp_path) == 0


def test_lvibe_tree_usage_bytes_sums_files(tmp_path: Path) -> None:
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    (lv / "x.txt").write_bytes(b"abc")
    assert lvibe_tree_usage_bytes(tmp_path) == 3
