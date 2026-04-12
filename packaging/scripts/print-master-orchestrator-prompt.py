#!/usr/bin/env python3
"""Print the Master orchestrator fenced block from docs/PROMPT_BUILD_LE_VIBE.md (stdout = paste into Cursor).

Product / scope: docs/PRODUCT_SPEC.md §9; spec-phase2.md §14 (H6/H7 vs in-repo queue; STEP 14 E1 — editor/le-vibe-overrides/README.md + test_editor_le_vibe_overrides_readme_contract.py; ide-ci-metadata / build-le-vibe-ide.yml + test_build_le_vibe_ide_workflow_contract.py; PRODUCT_SPEC *Prioritization* + test_product_spec_section8.py / le-vibe/README vs root + test_le_vibe_readme_e1_contract.py).
STEP 16 guard: le-vibe/tests/test_prompt_build_orchestrator_fence.py (stdout must match the fenced block).
Full E1 roster: project root README.md Tests / E1 mapping; spec-phase2.md §14 Honesty vs CI (ci.yml, dependabot.yml, packaging/bin).
"""

from __future__ import annotations

from pathlib import Path


def _master_orchestrator_fence(repo_root: Path) -> str:
    text = (repo_root / "docs" / "PROMPT_BUILD_LE_VIBE.md").read_text(encoding="utf-8")
    for part in text.split("```"):
        stripped = part.lstrip()
        if stripped.startswith("You are the senior engineer for Lé Vibe"):
            return part
    raise RuntimeError("Master orchestrator fenced block not found in docs/PROMPT_BUILD_LE_VIBE.md")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    block = _master_orchestrator_fence(repo_root)
    print(block.rstrip())


if __name__ == "__main__":
    main()
