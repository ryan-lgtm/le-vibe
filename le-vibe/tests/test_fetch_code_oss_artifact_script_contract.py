"""Contract: packaging/scripts/fetch-code-oss-artifact.sh — editor probe for CI/smoke."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_fetch_code_oss_artifact_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "fetch-code-oss-artifact.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_fetch_code_oss_artifact_documents_le_vibe_editor_path_errors() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "fetch-code-oss-artifact.sh").read_text(
        encoding="utf-8"
    )
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "LE_VIBE_EDITOR not found:" in text
    assert "LE_VIBE_EDITOR not executable:" in text
    assert "no codium found" in text
