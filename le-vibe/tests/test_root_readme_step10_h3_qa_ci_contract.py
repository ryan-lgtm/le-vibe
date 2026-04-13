"""Contract: root README lists STEP 10 / H3 QA CI + smoke (Roadmap H3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step10_h3_qa_ci_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### QA CI & smoke — STEP 10 / H3" in text
    assert "Master orchestrator STEP 10" in text
    assert "ci-smoke.sh" in text
    assert "ci-editor-gate.sh" in text
    assert "ci-qa-hardening.md" in text
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
