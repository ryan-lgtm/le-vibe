"""Append-only incremental memory (PRODUCT_SPEC §5.3)."""

from __future__ import annotations

import pytest

from le_vibe.workspace_hub import ensure_lvibe_workspace
from le_vibe.workspace_incremental_sync import append_incremental_fact


def test_append_incremental_fact_writes_and_idempotent(tmp_path: Path) -> None:
    ensure_lvibe_workspace(tmp_path)
    did1, p = append_incremental_fact(tmp_path, "first fact", idempotent_id="k1")
    assert did1 is True
    did2, p2 = append_incremental_fact(tmp_path, "ignored", idempotent_id="k1")
    assert did2 is False
    assert p == p2
    text = p.read_text(encoding="utf-8")
    assert "first fact" in text
    assert "ignored" not in text


def test_append_incremental_fact_without_idempotent_appends_twice(tmp_path: Path) -> None:
    ensure_lvibe_workspace(tmp_path)
    append_incremental_fact(tmp_path, "a")
    append_incremental_fact(tmp_path, "b")
    t = (tmp_path / ".lvibe" / "memory" / "incremental.md").read_text(encoding="utf-8")
    assert t.count("— a") >= 1
    assert t.count("— b") >= 1


def test_append_incremental_fact_missing_file_raises(tmp_path: Path) -> None:
    (tmp_path / ".lvibe").mkdir()
    (tmp_path / ".lvibe" / "memory").mkdir()
    with pytest.raises(FileNotFoundError):
        append_incremental_fact(tmp_path, "nope")
