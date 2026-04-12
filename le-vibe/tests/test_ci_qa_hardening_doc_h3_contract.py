"""Contract: docs/ci-qa-hardening.md keeps H3 QA CI story (STEP 10)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_qa_hardening_doc_lists_smoke_and_pytest():
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "ci-smoke.sh" in text
    assert "pytest" in text
    assert "ci.yml" in text
    assert "H3" in text or "Roadmap H3" in text
