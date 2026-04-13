"""STEP 6 (E5): ``lvibe logs`` surfaces local structured log path (no Ollama)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.structured_log import STRUCTURED_LOG_FILENAME


def test_lvibe_logs_path_only_respects_xdg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["launcher", "logs", "--path-only"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith(STRUCTURED_LOG_FILENAME)
    assert "le-vibe" in out.replace("\\", "/")


def test_lvibe_logs_tail_last_lines(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    logf = tmp_path / "le-vibe" / STRUCTURED_LOG_FILENAME
    logf.parent.mkdir(parents=True)
    lines = [json.dumps({"n": i}) for i in range(5)]
    logf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["launcher", "logs", "--tail", "2"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    assert json.loads(out[-1])["n"] == 4


def test_lvibe_logs_tail_missing_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["launcher", "logs", "-n", "5"])
    assert launcher.main() == 1
    assert "no file" in capsys.readouterr().err.lower()


def test_lvibe_logs_json_meta(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    logf = tmp_path / "le-vibe" / STRUCTURED_LOG_FILENAME
    logf.parent.mkdir(parents=True)
    logf.write_text(
        '{"ts":"2026-01-01T00:00:00+00:00","component":"launcher","event":"x"}\n'
        '{"ts":"2026-01-02T00:00:00+00:00","component":"workspace","event":"y"}\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "logs", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["lines"] == 2
    assert data["first_ts"] == "2026-01-01T00:00:00+00:00"
    assert data["last_ts"] == "2026-01-02T00:00:00+00:00"


def test_lvibe_logs_json_rejects_tail_combo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["launcher", "logs", "--json", "--tail", "1"])
    assert launcher.main() == 2
    assert "cannot" in capsys.readouterr().err.lower()
