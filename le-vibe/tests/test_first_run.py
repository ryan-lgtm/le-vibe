"""Tests for product first-run orchestration."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe.first_run import ensure_product_first_run, evaluate_first_run_agent_readiness


def test_launcher_argparse_first_run_flags_help_mentions_logs_step6():
    """lvibe --help lists first-run flags with STEP 6 / lvibe logs (E1 onboarding)."""
    launcher = Path(__file__).resolve().parents[1] / "le_vibe" / "launcher.py"
    text = launcher.read_text(encoding="utf-8")
    assert "--skip-first-run" in text
    assert "--force-first-run" in text
    assert "lvibe logs" in text
    assert "Live:" in text
    assert "tail -f" in text
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
    assert "Live:" in msg
    assert "tail -f" in msg
    assert "lvibe logs --tail 50" in msg


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


def test_first_run_agent_readiness_fails_when_model_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / "le-vibe"
    cfg.mkdir(parents=True)
    (cfg / "model-decision.json").write_text('{"selected_model":"deepseek-r1:8b"}', encoding="utf-8")
    monkeypatch.setattr("le_vibe.first_run.verify_api", lambda _h, _p: True)
    monkeypatch.setattr("le_vibe.first_run.list_local_model_names", lambda _h, _p: [])
    ok, msg = evaluate_first_run_agent_readiness(config_dir=cfg)
    assert ok is False
    assert "selected model" in msg.lower()


def test_first_run_agent_readiness_ok_when_model_and_cline_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / "le-vibe"
    cfg.mkdir(parents=True)
    (cfg / "model-decision.json").write_text('{"selected_model":"deepseek-r1:8b"}', encoding="utf-8")
    monkeypatch.setattr("le_vibe.first_run.verify_api", lambda _h, _p: True)
    monkeypatch.setattr(
        "le_vibe.first_run.list_local_model_names",
        lambda _h, _p: ["deepseek-r1:8b"],
    )
    monkeypatch.setattr(
        "le_vibe.first_run.subprocess.check_output",
        lambda *_a, **_k: "saoudrizwan.claude-dev\nredhat.vscode-yaml\n",
    )
    ok, msg = evaluate_first_run_agent_readiness(config_dir=cfg)
    assert ok is True
    assert msg == "agent-ready"
