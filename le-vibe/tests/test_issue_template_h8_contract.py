"""E1: .github/ISSUE_TEMPLATE reporter YAML keeps H8 / STEP 12 + config.yml pointers (PRODUCT_SPEC §1, STEP 12)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_issue_template_forms_document_step12_and_config_anchor():
    root = _repo_root()
    tmpl = root / ".github" / "ISSUE_TEMPLATE"
    for name in ("bug_report.yml", "feature_request.yml", "documentation.yml"):
        text = (tmpl / name).read_text(encoding="utf-8")
        assert "STEP 12" in text, name
        assert "PM_STAGE_MAP" in text, name
        assert "ISSUE_TEMPLATE" in text, name
        assert "config.yml" in text, name
        assert "H8" in text, name


def test_issue_template_config_has_h8_maintainer_comment():
    root = _repo_root()
    text = (root / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(encoding="utf-8")
    assert "H8" in text
    assert "STEP 12" in text
    assert "docs/README.md" in text
