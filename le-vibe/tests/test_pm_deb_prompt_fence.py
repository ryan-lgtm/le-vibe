"""`packaging/scripts/print-pm-deb-build-prompt.py` should keep PM deb prompt extraction stable."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_print_pm_deb_build_prompt_script_bash_syntax() -> None:
    script = Path(__file__).resolve().parents[2] / "packaging" / "scripts" / "print-pm-deb-build-prompt.py"
    assert script.is_file(), script
    subprocess.run(["python3", "-m", "py_compile", str(script)], check=True, capture_output=True)


def test_print_pm_deb_build_prompt_script_header_mentions_queue() -> None:
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "print-pm-deb-build-prompt.py").read_text(encoding="utf-8")
    assert "0 -> 1 -> 14 -> 2-13 -> 15-17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
