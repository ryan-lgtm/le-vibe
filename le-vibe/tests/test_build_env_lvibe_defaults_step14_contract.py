"""Contract: editor/le-vibe-overrides/build-env.lvibe-defaults.sh — §7.3 default exports (STEP 14)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_build_env_lvibe_defaults_documents_7_3_and_compile_hook():
    path = _repo_root() / "editor" / "le-vibe-overrides" / "build-env.lvibe-defaults.sh"
    text = path.read_text(encoding="utf-8")
    assert path.is_file()
    assert "§7.3" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "APP_NAME=" in text and "Lé Vibe" in text
    assert "ORG_NAME=" in text
    assert "codium" in text
