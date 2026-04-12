"""Continue YAML template must use a concrete model tag (no AUTODETECT-only product config)."""

from __future__ import annotations

from pathlib import Path

from le_vibe.reporting import generate_continue_config


def test_generated_continue_config_has_no_autodetect_only(tmp_path: Path):
    p = generate_continue_config("deepseek-r1:7b", "127.0.0.1", 11435, config_dir=tmp_path)
    text = p.read_text(encoding="utf-8")
    assert "AUTODETECT" not in text
    assert "deepseek-r1:7b" in text
    assert "Lé Vibe" in text or "lé vibe" in text.lower()
