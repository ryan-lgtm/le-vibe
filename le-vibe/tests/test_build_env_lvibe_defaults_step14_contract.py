"""Contract: editor/le-vibe-overrides/build-env.lvibe-defaults.sh — §7.3 default exports (STEP 14)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_build_env_lvibe_defaults_bash_syntax() -> None:
    script = _repo_root() / "editor" / "le-vibe-overrides" / "build-env.lvibe-defaults.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_build_env_lvibe_defaults_documents_7_3_and_compile_hook():
    path = _repo_root() / "editor" / "le-vibe-overrides" / "build-env.lvibe-defaults.sh"
    text = path.read_text(encoding="utf-8")
    assert text.splitlines()[0] == "# Lé Vibe IDE — default build exports (PRODUCT_SPEC §7.3)."
    assert text.splitlines()[1].startswith("# Sourced by packaging/scripts/ci-vscodium-linux-dev-build.sh")
    assert path.is_file()
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "§7.3" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "APP_NAME=" in text and "Lé Vibe" in text
    assert "ORG_NAME=" in text
    assert 'export APP_NAME="Lé Vibe"' in text
    assert 'export ORG_NAME="Le Vibe"' in text
    assert "set -a" in text
    assert "set +a" in text
    assert text.index("set -a") < text.index('export APP_NAME="Lé Vibe"')
    assert text.index('export APP_NAME="Lé Vibe"') < text.index('export ORG_NAME="Le Vibe"')
    assert text.index('export ORG_NAME="Le Vibe"') < text.index("set +a")
    assert text.count("export ") == 2
    assert text.rstrip().endswith("set +a")
    assert "codium" in text
    assert "BINARY_NAME" in text
    assert "BINARY_NAME stays codium" in text
    assert "export BINARY_NAME=" not in text
    assert "lvibe" in text
    assert "test_build_env_lvibe_defaults_step14_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
