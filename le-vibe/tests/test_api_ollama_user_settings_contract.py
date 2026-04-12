"""Ollama pull path + user-settings alignment (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md §4)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from le_vibe.api import EnsureBootstrapArgs, _resolve_locked_model_policy, _write_model_decision
from le_vibe.ollama_ops import model_tag_present_locally, pull_model
from le_vibe.reporting import write_model_decision_json
from le_vibe.types import ModelDecision


def test_pull_model_passes_ollama_host_to_subprocess() -> None:
    seen: dict[str, str] = {}

    def fake_run(cmd, timeout, env):  # noqa: ANN001
        seen["env_ollama"] = env.get("OLLAMA_HOST", "")
        p = MagicMock()
        p.returncode = 0
        return p

    with patch("le_vibe.ollama_ops.subprocess.run", side_effect=fake_run):
        ok, _ = pull_model("mistral:latest", host="127.0.0.1", port=11435)
    assert ok is True
    assert seen["env_ollama"] == "127.0.0.1:11435"


def test_model_tag_present_locally() -> None:
    names = ["qwen2.5-coder:7b", "llama3:latest"]
    assert model_tag_present_locally("qwen2.5-coder:7b", names) is True
    assert model_tag_present_locally("qwen2.5-coder", names) is True
    assert model_tag_present_locally("other:1b", names) is False


def test_resolve_locked_model_policy() -> None:
    a = EnsureBootstrapArgs(model=None, locked_model_policy=None)
    assert _resolve_locked_model_policy(a) == "hardware_tier_best_fit"
    b = EnsureBootstrapArgs(model="x:y", locked_model_policy=None)
    assert _resolve_locked_model_policy(b) == "cli_override"
    c = EnsureBootstrapArgs(model=None, locked_model_policy="user_settings")
    assert _resolve_locked_model_policy(c) == "user_settings"


def test_write_model_decision_locked_policy_user_settings(tmp_path: Path) -> None:
    d = ModelDecision(
        selected_model="mistral:latest",
        selected_tier="tier_small",
        comfortable=True,
        reason="user",
        rejected_candidates=[],
    )
    write_model_decision_json(d, config_dir=tmp_path, locked_policy="user_settings")
    data = json.loads((tmp_path / "locked-model.json").read_text(encoding="utf-8"))
    assert data["policy"] == "user_settings"


def test_write_model_decision_helper_matches_explicit_policy(tmp_path: Path) -> None:
    d = ModelDecision(
        selected_model="a:b",
        selected_tier="tier_small",
        comfortable=True,
        reason="r",
        rejected_candidates=[],
    )
    args = EnsureBootstrapArgs(config_dir=tmp_path, locked_model_policy="user_settings")
    _write_model_decision(d, args)
    data = json.loads((tmp_path / "locked-model.json").read_text(encoding="utf-8"))
    assert data["policy"] == "user_settings"
