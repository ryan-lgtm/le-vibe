"""Guard `docs/PROMPT_BUILD_LE_VIBE.md` Master orchestrator fence — stale PM pastes often say 'seven agents' or wrong § refs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _master_orchestrator_fence() -> str:
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PROMPT_BUILD_LE_VIBE.md").read_text(encoding="utf-8")
    parts = text.split("```")
    for part in parts:
        stripped = part.lstrip()
        if stripped.startswith("You are the senior engineer for Lé Vibe"):
            return part
    raise AssertionError("Master orchestrator fenced block not found in docs/PROMPT_BUILD_LE_VIBE.md")


def test_master_fence_requires_eight_agents_not_seven():
    block = _master_orchestrator_fence()
    assert "eight agents in le-vibe/templates/agents/" in block
    assert "seven agents" not in block


def test_master_fence_step1_regression_is_section10_acceptance():
    block = _master_orchestrator_fence()
    assert "STEP 1 — E1: Regression proof for §10 acceptance" in block


def test_master_fence_step0_covers_product_spec_through_section8():
    block = _master_orchestrator_fence()
    assert "secrets §8" in block
    assert "§10 acceptance" in block


def test_master_fence_step14_linux_compile_fail_fast_before_dev_build():
    """STEP 14.e: optional linux_compile runs bash-n/nvmrc gates before compile wrapper → dev/build.sh (see build-le-vibe-ide.yml)."""
    block = _master_orchestrator_fence()
    assert "STEP 14 — H6" in block
    assert "§7.3" in block
    assert "§7.3 close-out" in block
    assert "Debian `.deb` for the IDE" in block
    assert "GitHub Actions are not" in block
    assert "fail fast" in block
    assert "ci-vscodium-bash-syntax.sh" in block
    assert "ci-editor-nvmrc-sync.sh" in block
    assert "ci-vscodium-linux-dev-build.sh" in block
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in block


def test_print_master_orchestrator_script_matches_fence():
    root = Path(__file__).resolve().parents[2]
    script = root / "packaging" / "scripts" / "print-master-orchestrator-prompt.py"
    r = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(root),
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip() == _master_orchestrator_fence().rstrip()
