"""STEP C1: optional auto ``le-vibe-setup-cline`` after first-run."""

from __future__ import annotations

from pathlib import Path

from le_vibe.cline_setup_auto import maybe_auto_setup_cline_after_first_run, maybe_print_cline_onboarding_hint


def test_auto_setup_cline_skipped_when_disabled_by_default(tmp_path: Path, monkeypatch) -> None:
    """CP6: third-party Cline auto-install is opt-in (LE_VIBE_AUTO_CLINE_SETUP unset)."""
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    (cfg / ".first-run-complete").write_text("ok", encoding="utf-8")
    monkeypatch.delenv("LE_VIBE_AUTO_CLINE_SETUP", raising=False)
    maybe_auto_setup_cline_after_first_run(cfg)
    assert not (cfg / ".auto-cline-setup-suppressed").exists()


def test_auto_setup_cline_noop_without_first_run_complete(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    monkeypatch.setenv("LE_VIBE_AUTO_CLINE_SETUP", "1")
    monkeypatch.setattr("le_vibe.cline_setup_auto.shutil.which", lambda _name: None)
    maybe_auto_setup_cline_after_first_run(cfg)
    assert not (cfg / ".auto-cline-setup-suppressed").exists()


def test_auto_setup_cline_suppresses_on_failure(tmp_path: Path, monkeypatch) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    (cfg / ".first-run-complete").write_text("ok", encoding="utf-8")
    fake = tmp_path / "le-vibe-setup-cline"
    fake.write_text("#!/bin/sh\nexit 3\n", encoding="utf-8")
    fake.chmod(0o755)

    monkeypatch.setenv("LE_VIBE_AUTO_CLINE_SETUP", "1")
    monkeypatch.setattr(
        "le_vibe.cline_setup_auto.shutil.which",
        lambda name: str(fake) if name == "le-vibe-setup-cline" else None,
    )
    maybe_auto_setup_cline_after_first_run(cfg)
    assert (cfg / ".auto-cline-setup-suppressed").is_file()


def test_prints_onboarding_hint_once_when_auth_state_not_visible(tmp_path: Path, monkeypatch, capsys) -> None:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    (cfg / ".first-run-complete").write_text("ok\n", encoding="utf-8")
    home = tmp_path / "home"
    store = home / ".config" / "Lé Vibe" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings"
    store.mkdir(parents=True)
    (store / "cline_mcp_settings.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr("pathlib.Path.home", lambda: home)
    maybe_print_cline_onboarding_hint(cfg)
    first = capsys.readouterr().err
    assert "appears unauthenticated" in first
    maybe_print_cline_onboarding_hint(cfg)
    second = capsys.readouterr().err
    assert second == ""
