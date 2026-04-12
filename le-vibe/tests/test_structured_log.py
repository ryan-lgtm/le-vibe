"""Local JSONL structured log — no third-party telemetry."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from le_vibe.structured_log import (
    STRUCTURED_LOG_FILENAME,
    append_structured_log,
    structured_log_enabled,
    structured_log_path,
)


def test_append_writes_jsonl(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("LE_VIBE_STRUCTURED_LOG", "1")
    append_structured_log("test", "hello", n=42)
    logf = tmp_path / "le-vibe" / STRUCTURED_LOG_FILENAME
    assert logf.is_file()
    line = logf.read_text(encoding="utf-8").strip().splitlines()[-1]
    row = json.loads(line)
    assert row["component"] == "test"
    assert row["event"] == "hello"
    assert row["n"] == 42
    assert "ts" in row


def test_disabled_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("LE_VIBE_STRUCTURED_LOG", "0")
    assert structured_log_enabled() is False
    append_structured_log("x", "y")
    assert not (tmp_path / "le-vibe" / STRUCTURED_LOG_FILENAME).exists()


def test_structured_log_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    p = structured_log_path()
    assert p.name == STRUCTURED_LOG_FILENAME
    assert "le-vibe" in p.parts
