"""`docs/MASTER_ITERATION_LOOP.md` must retain an extractable Master iteration loop fence (print-master-iteration-loop-prompt.py)."""

from __future__ import annotations

from pathlib import Path


def test_master_iteration_loop_fence_extractable():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "MASTER_ITERATION_LOOP.md").read_text(encoding="utf-8")
    fence: str | None = None
    for part in text.split("```"):
        if part.lstrip().startswith("You are the Lé Vibe master iteration loop"):
            fence = part
            break
    assert fence is not None, (
        "Master iteration loop fenced block missing — "
        "see packaging/scripts/print-master-iteration-loop-prompt.py"
    )
    assert "MODE: ENGINEER" in fence and "MODE: PRODUCT_MANAGER" in fence
    assert "MODE: PROJECT" in fence
    assert "OWNER_DIRECTIVES" in fence
    assert "AGENT_MODE_ORCHESTRATION" in fence
    assert "ORDERED WORK QUEUE" in fence or "PROMPT_BUILD_LE_VIBE" in fence
    assert "USER RESPONSE REQUIRED" in fence
    assert "LÉ VIBE SESSION COMPLETE" in fence
    assert "PM_DEB_BUILD_ITERATION.md" in fence
    assert "build-le-vibe-debs.sh --with-ide" in fence
    assert "Full-product install" in fence
    assert "le-vibe-deb" in fence
