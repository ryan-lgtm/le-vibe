"""STEP 7: optional auto ``le-vibe-setup-continue`` after first-run (happy path)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from le_vibe.continue_setup_auto import (
    _SUPPRESSED,
    continue_symlink_ok,
    maybe_auto_setup_continue_after_first_run,
)


def test_continue_symlink_ok_true_when_linked(tmp_path: Path) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    src = cfg / "continue-config.yaml"
    src.write_text("x: 1\n", encoding="utf-8")
    cont_dir = tmp_path / "continue"
    cont_dir.mkdir()
    dst = cont_dir / "config.yaml"
    dst.symlink_to(src)
    monkey_cfg = cfg
    with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(tmp_path)}, clear=False):
        assert continue_symlink_ok(monkey_cfg) is True


def test_continue_symlink_ok_false_when_missing(tmp_path: Path) -> None:
    cfg = tmp_path / "lv"
    cfg.mkdir()
    with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(tmp_path)}, clear=False):
        assert continue_symlink_ok(cfg) is False


def test_maybe_auto_skips_when_symlink_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    src = cfg / "continue-config.yaml"
    src.write_text("x: 1\n", encoding="utf-8")
    cont_dir = tmp_path / "continue"
    cont_dir.mkdir()
    (cont_dir / "config.yaml").symlink_to(src)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    run = subprocess.run
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not run")))
    maybe_auto_setup_continue_after_first_run(cfg)


def test_maybe_auto_skips_without_yaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not run")))
    maybe_auto_setup_continue_after_first_run(cfg)


def test_maybe_auto_skips_when_env_off(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    (cfg / "continue-config.yaml").write_text("x: 1\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_AUTO_CONTINUE_SETUP", "0")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not run")))
    maybe_auto_setup_continue_after_first_run(cfg)


def test_maybe_auto_skips_when_suppressed_file_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    (cfg / "continue-config.yaml").write_text("x: 1\n", encoding="utf-8")
    (cfg / _SUPPRESSED).write_text("x\n", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not run")))
    maybe_auto_setup_continue_after_first_run(cfg)


def test_maybe_auto_runs_when_which_finds_setup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    (cfg / "continue-config.yaml").write_text("x: 1\n", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    fake = tmp_path / "le-vibe-setup-continue"
    fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake.chmod(0o755)

    def _which(name: str) -> str | None:
        return str(fake) if name == "le-vibe-setup-continue" else None

    monkeypatch.setattr("le_vibe.continue_setup_auto.shutil.which", _which)

    class R:
        returncode = 0
        stderr = ""
        stdout = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())

    maybe_auto_setup_continue_after_first_run(cfg)
    assert (cfg / _SUPPRESSED).is_file() is False


def test_maybe_auto_writes_suppressed_on_failure_exit_3(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    (cfg / "continue-config.yaml").write_text("x: 1\n", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    fake = tmp_path / "le-vibe-setup-continue"
    fake.write_text("#!/bin/sh\nexit 3\n", encoding="utf-8")
    fake.chmod(0o755)

    def _which(name: str) -> str | None:
        return str(fake) if name == "le-vibe-setup-continue" else None

    monkeypatch.setattr("le_vibe.continue_setup_auto.shutil.which", _which)

    class R:
        returncode = 3
        stderr = "err"
        stdout = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())

    maybe_auto_setup_continue_after_first_run(cfg)
    assert (cfg / _SUPPRESSED).is_file()


def test_maybe_auto_no_suppressed_on_exit_4(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "le-vibe"
    cfg.mkdir()
    (cfg / "continue-config.yaml").write_text("x: 1\n", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    fake = tmp_path / "le-vibe-setup-continue"
    fake.write_text("#!/bin/sh\nexit 4\n", encoding="utf-8")
    fake.chmod(0o755)

    def _which(name: str) -> str | None:
        return str(fake) if name == "le-vibe-setup-continue" else None

    monkeypatch.setattr("le_vibe.continue_setup_auto.shutil.which", _which)

    class R:
        returncode = 4
        stderr = ""
        stdout = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R())

    maybe_auto_setup_continue_after_first_run(cfg)
    assert not (cfg / _SUPPRESSED).is_file()
