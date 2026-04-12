"""Tests for concrete model lock persistence."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.reporting import write_locked_model_json, write_model_decision_json
from le_vibe.types import ModelDecision


def test_write_model_decision_writes_locked_json(tmp_path: Path):
    d = ModelDecision(
        selected_model="deepseek-r1:8b",
        selected_tier="tier_8b",
        comfortable=True,
        reason="test",
        rejected_candidates=[],
    )
    write_model_decision_json(d, config_dir=tmp_path)
    lock_path = tmp_path / "locked-model.json"
    assert lock_path.is_file()
    data = json.loads(lock_path.read_text(encoding="utf-8"))
    assert data["ollama_model"] == "deepseek-r1:8b"
    assert data["policy"] == "hardware_tier_best_fit"


def test_write_locked_model_json_explicit(tmp_path: Path):
    write_locked_model_json("qwen2.5-coder:7b", reason_excerpt="x", config_dir=tmp_path)
    data = json.loads((tmp_path / "locked-model.json").read_text(encoding="utf-8"))
    assert data["ollama_model"] == "qwen2.5-coder:7b"


def test_empty_selected_model_skips_lock(tmp_path: Path):
    d = ModelDecision(
        selected_model="",
        selected_tier="tier_small",
        comfortable=False,
        reason="none",
        rejected_candidates=[],
    )
    write_model_decision_json(d, config_dir=tmp_path)
    assert not (tmp_path / "locked-model.json").exists()
