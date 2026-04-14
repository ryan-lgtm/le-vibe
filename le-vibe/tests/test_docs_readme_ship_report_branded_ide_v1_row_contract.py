"""Contract: docs/README.md indexes SHIP_REPORT_BRANDED_IDE_V1 and doc exists."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_lists_ship_report_branded_ide_v1_row() -> None:
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`SHIP_REPORT_BRANDED_IDE_V1.md`]" in text
    assert "v1 completion report" in text.lower()


def test_ship_report_branded_ide_v1_doc_exists_and_declares_shipped() -> None:
    p = _repo_root() / "docs" / "SHIP_REPORT_BRANDED_IDE_V1.md"
    assert p.is_file()
    t = p.read_text(encoding="utf-8")
    assert "Acceptance checklist" in t
    assert "Branded Lé Vibe IDE v1" in t
    assert "is SHIPPED" in t
