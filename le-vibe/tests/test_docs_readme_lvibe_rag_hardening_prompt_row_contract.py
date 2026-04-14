"""Contract: docs/README.md lists LVIBE_RAG_WORKSPACE_HARDENING_PROMPT (§5 .lvibe/ engineer prompt)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_lvibe_rag_hardening_prompt_row():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`LVIBE_RAG_WORKSPACE_HARDENING_PROMPT.md`]" in text
    assert "LVIBE_RAG_WORKSPACE_HARDENING_PROMPT.md" in text
    assert ".lvibe/" in text


def test_lvibe_rag_workspace_hardening_prompt_doc_exists():
    p = _repo_root() / "docs" / "LVIBE_RAG_WORKSPACE_HARDENING_PROMPT.md"
    assert p.is_file()
    t = p.read_text(encoding="utf-8")
    assert "workspace_storage.py" in t or "workspace_storage" in t
    assert "PRODUCT_SPEC" in t
