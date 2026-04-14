"""STEP 5 (E4): ``lvibe hygiene`` delegates to ``le_vibe.hygiene`` (no Ollama)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.workspace_hub import ensure_lvibe_workspace


def test_lvibe_hygiene_ok_on_prepared_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ensure_lvibe_workspace(tmp_path)
    monkeypatch.setattr(sys, "argv", ["launcher", "hygiene", "-w", str(tmp_path)])
    assert launcher.main() == 0


def test_lvibe_hygiene_fails_without_lvibe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "hygiene", "-w", str(tmp_path)])
    assert launcher.main() == 1


def test_lvibe_append_incremental_fact_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from le_vibe.workspace_hub import ensure_lvibe_workspace

    ensure_lvibe_workspace(tmp_path)
    inc = tmp_path / ".lvibe" / "memory" / "incremental.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "launcher",
            "append-incremental-fact",
            "-C",
            str(tmp_path),
            "--text",
            "cli fact",
            "--idempotent-id",
            "cli1",
        ],
    )
    assert launcher.main() == 0
    assert "cli fact" in inc.read_text(encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "launcher",
            "append-incremental-fact",
            "-C",
            str(tmp_path),
            "--text",
            "dup",
            "--idempotent-id",
            "cli1",
        ],
    )
    assert launcher.main() == 0
    assert inc.read_text(encoding="utf-8").count("cli fact") == 1
