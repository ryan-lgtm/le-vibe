"""Contract: docs/README.md H3 row for ci-qa-hardening.md lists IDE smoke vs linux_compile (STEP 14.e / 14.f)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_ci_qa_hardening_row_lists_editor_smoke_and_linux_compile():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`ci-qa-hardening.md`]" in text
    assert "./editor/smoke.sh" in text
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "14.e / 14.f" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
