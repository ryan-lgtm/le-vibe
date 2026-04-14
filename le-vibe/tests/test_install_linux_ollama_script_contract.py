"""Contract: Linux Ollama installer is idempotent unless --force."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_linux_script_skips_reinstall_when_ollama_on_path() -> None:
    text = (_repo_root() / "le-vibe" / "scripts" / "install_linux.sh").read_text(encoding="utf-8")
    assert "command -v ollama" in text
    assert "skipping reinstall" in text
    assert "--force" in text
    assert "curl -fsSL https://ollama.com/install.sh | sh" in text


def test_install_linux_script_force_and_unknown_arg_contract() -> None:
    text = (_repo_root() / "le-vibe" / "scripts" / "install_linux.sh").read_text(encoding="utf-8")
    assert "unknown argument" in text
    assert "expected --force" in text
    assert "case \"${1:-}\"" in text
