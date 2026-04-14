"""Contract: packaging/scripts/uninstall-le-vibe-local.sh supports safe cleanup."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_uninstall_le_vibe_local_script_exists_bash_syntax_executable() -> None:
    script = _root() / "packaging" / "scripts" / "uninstall-le-vibe-local.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_uninstall_le_vibe_local_script_documents_safe_options() -> None:
    text = (_root() / "packaging" / "scripts" / "uninstall-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "--purge-user-data" in text
    assert "--purge-workspace" in text
    assert "refusing to operate on root path '/'" in text
    assert "dpkg --remove --force-remove-reinstreq" in text
    assert "apt-get remove --purge" in text
    assert "OK: lvibe not on PATH" in text
