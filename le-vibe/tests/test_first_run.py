"""Tests for product first-run orchestration."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe.first_run import ensure_product_first_run


def test_launcher_argparse_first_run_flags_help_mentions_logs_step6():
    """lvibe --help lists first-run flags with STEP 6 / lvibe logs (E1 onboarding)."""
    launcher = Path(__file__).resolve().parents[1] / "le_vibe" / "launcher.py"
    text = launcher.read_text(encoding="utf-8")
    assert "--skip-first-run" in text
    assert "--force-first-run" in text
    assert "lvibe logs" in text
    assert "STEP 6" in text
    assert "LE_VIBE_VERBOSE" in text


def test_first_run_skips_when_marker_and_model_decision(tmp_path: Path):
    cfg = tmp_path / "le-vibe"
    cfg.mkdir(parents=True)
    (cfg / ".first-run-complete").write_text("complete\n", encoding="utf-8")
    (cfg / "model-decision.json").write_text("{}", encoding="utf-8")
    code, msg = ensure_product_first_run(config_dir=cfg)
    assert code == 0
    assert "already" in msg.lower()


def test_first_run_bootstrap_failure_message_lists_remediation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / "le-vibe"
    cfg.mkdir(parents=True)

    def fake_bootstrap(_args):
        return (2, None)  # type: ignore

    monkeypatch.setattr("le_vibe.first_run.ensure_bootstrap", fake_bootstrap)
    code, msg = ensure_product_first_run(config_dir=cfg, yes=True)
    assert code == 2
    assert "--force-first-run" in msg
    assert "LE_VIBE_VERBOSE" in msg
    assert "lvibe --help" in msg
    assert "lvibe logs" in msg
    assert "--path-only" in msg


def test_first_run_force_removes_marker(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / "le-vibe"
    cfg.mkdir(parents=True)
    (cfg / ".first-run-complete").write_text("complete\n", encoding="utf-8")
    (cfg / "model-decision.json").write_text("{}", encoding="utf-8")

    calls: list[bool] = []

    def fake_ensure(_args):
        calls.append(True)
        return 1, None  # type: ignore

    monkeypatch.setattr("le_vibe.first_run.ensure_bootstrap", fake_ensure)
    code, _msg = ensure_product_first_run(config_dir=cfg, force=True, yes=True)
    assert calls == [True]
    assert code == 1
