"""Contract: docs/AGENT_MODE_ORCHESTRATION.md keeps STEP 14 full-product close-out gate references."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_agent_mode_orchestration_lists_step14_full_product_closeout_gate():
    text = (_repo_root() / "docs" / "AGENT_MODE_ORCHESTRATION.md").read_text(encoding="utf-8")
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "le-vibe-deb" in text
