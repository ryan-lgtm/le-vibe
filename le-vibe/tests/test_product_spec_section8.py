"""Contract tests for docs/PRODUCT_SPEC.md — welcome §4, launcher copy, §8 secrets strings in rules, § Prioritization editor smoke."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.continue_workspace import _lvibe_continue_rule_body
from le_vibe.welcome import WELCOME_BANNER
from le_vibe.workspace_hub import LVIBE_DIR_NAME


def test_welcome_banner_matches_product_spec_section4():
    assert "Welcome to Lé Vibe" in WELCOME_BANNER
    assert "Cursor" in WELCOME_BANNER
    assert "open source" in WELCOME_BANNER.lower() or "free" in WELCOME_BANNER.lower()


def test_lvibe_workspace_dir_name():
    assert LVIBE_DIR_NAME == ".lvibe"


def test_launcher_user_facing_description_uses_le_vibe_name():
    p = Path(launcher.__file__).read_text(encoding="utf-8")
    assert "Lé Vibe" in p


@pytest.mark.parametrize(
    "rel",
    [
        "templates/continue-config.yaml.j2",
        "templates/lvibe-editor-welcome.md",
    ],
)
def test_continue_template_lists_product_name(rel: str):
    root = Path(__file__).resolve().parents[1]
    text = (root / rel).read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "AUTODETECT" not in text


def test_lvibe_editor_welcome_template_section4_positioning():
    root = Path(__file__).resolve().parents[1]
    text = (root / "templates" / "lvibe-editor-welcome.md").read_text(encoding="utf-8")
    assert "Welcome to Lé Vibe" in text
    assert "open source" in text.lower()
    assert "Cursor" in text


def test_continue_memory_rule_documents_secrets_policy_section8():
    body = _lvibe_continue_rule_body()
    assert "PRODUCT_SPEC §8" in body
    assert ".env.local" in body or ".env.*" in body
    assert "Never paste secret" in body


def test_continue_memory_rule_documents_user_gate_section72():
    body = _lvibe_continue_rule_body()
    assert "PRODUCT_SPEC §7.2" in body
    assert "USER RESPONSE REQUIRED" in body
    assert "numbered questions" in body


def test_workspace_hub_agents_seed_documents_secrets_section8():
    p = Path(__file__).resolve().parents[1] / "le_vibe" / "workspace_hub.py"
    text = p.read_text(encoding="utf-8")
    assert "PRODUCT_SPEC §8" in text
    assert ".env" in text


def test_workspace_policy_reflects_product_spec_section5_defaults():
    p = Path(__file__).resolve().parents[1] / "le_vibe" / "workspace_policy.py"
    text = p.read_text(encoding="utf-8")
    assert "DEFAULT_CAP_MB = 50" in text
    assert "workspace-policy.json" in text


def test_product_spec_prioritization_sequences_editor_smoke_before_full_ide_ci():
    """§ Prioritization — vendoring gate for editor/ (H6 / STEP 14) stays documented."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    assert "**How to sequence work:**" in text
    assert "./editor/smoke.sh" in text
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs" in text
    assert "retention-days" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "actions: write" in text
    assert "Pre-binary artifact" in text
    assert "editor/BUILD.md" in text
    assert "editor/VENDORING.md" in text
