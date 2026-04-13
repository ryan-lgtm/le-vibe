"""STEP 5 (E4): ``lvibe hygiene`` delegates to ``le_vibe.hygiene`` (no Ollama)."""

from __future__ import annotations

import sys

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
