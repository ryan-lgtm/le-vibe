"""Contract: packaging/bin/* sh stubs require python3 on PATH before exec."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_packaging_bin_sh_launchers_syntax_and_python3_guard() -> None:
    root = _repo_root()
    for rel, needle in (
        ("packaging/bin/le-vibe", "le-vibe: python3 not on PATH"),
        ("packaging/bin/lvibe", "lvibe: python3 not on PATH"),
        ("packaging/bin/lvibe-hygiene", "lvibe-hygiene: python3 not on PATH"),
    ):
        script = root / rel
        assert script.is_file(), script
        subprocess.run(["sh", "-n", str(script)], check=True, capture_output=True)
        text = script.read_text(encoding="utf-8")
        assert needle in text
        assert "Requires: python3 on PATH" in text
