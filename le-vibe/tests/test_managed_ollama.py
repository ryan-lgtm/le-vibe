"""Tests for managed Ollama lifecycle helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe.managed_ollama import (
    ManagedOllamaState,
    ensure_managed_ollama,
    stop_managed_ollama,
)


def test_managed_state_roundtrip():
    s = ManagedOllamaState(
        pid=12345,
        host="127.0.0.1",
        port=11435,
        session_id="s1",
        started_at_unix=1.5,
    )
    d = s.to_json()
    assert ManagedOllamaState.from_json(d).pid == 12345


def test_stop_no_state(tmp_path: Path):
    p = tmp_path / "managed_ollama.json"
    ok, msg = stop_managed_ollama(state_path=p)
    assert ok is True
    assert "nothing to stop" in msg


def test_ensure_without_ollama_binary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("le_vibe.managed_ollama.shutil.which", lambda _name: None)
    p = tmp_path / "managed_ollama.json"
    ok, msg, st = ensure_managed_ollama(state_path=p, host="127.0.0.1", port=11499)
    assert ok is False
    assert "PATH" in msg
    assert st is None
