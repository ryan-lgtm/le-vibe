"""STEP C1: optional auto ``le-vibe-setup-cline`` after first-run."""

from __future__ import annotations

from pathlib import Path

from le_vibe.cline_setup_auto import maybe_auto_setup_cline_after_first_run


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
