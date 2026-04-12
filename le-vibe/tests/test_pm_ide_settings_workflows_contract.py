"""PM IDE settings & workflows — settings merge + E1 anchors (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md §4)."""

from __future__ import annotations

import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_continue_rule_workspace_context_seeded_footer_anchors():
    """Keeps Continue rules aligned with `.lvibe/.workspace-context-seeded` + setup-workflow copy."""
    from le_vibe.continue_workspace import _lvibe_continue_rule_body

    body = _lvibe_continue_rule_body()
    assert ".lvibe/.workspace-context-seeded" in body
    assert "/setup-workspace" in body
    assert ".lvibe/workflows/setup-workspace.md" in body
    assert "touch .lvibe/.workspace-context-seeded" in body


def test_user_settings_deep_merge_preserves_nested_defaults(tmp_path):
    """Disk JSON merges into ``default_user_settings()`` (nested ``model`` / ``ide``)."""
    p = tmp_path / "user-settings.json"
    p.write_text(
        json.dumps(
            {
                "model": {"override_tag": "mistral:latest", "use_recommended": False},
            }
        ),
        encoding="utf-8",
    )
    from le_vibe.user_settings import load_user_settings

    u = load_user_settings(config_dir=tmp_path)
    assert u["model"]["override_tag"] == "mistral:latest"
    assert u["model"]["use_recommended"] is False
    assert u["model"]["allow_pull_if_disk_ok"] is True
    assert u["ide"]["show_chat_commands_help"] is True


def test_default_user_settings_keys_are_subset_of_schema_example():
    """Stack defaults stay consistent with ``schemas/user-settings.v1.example.json``."""
    from le_vibe.user_settings import default_user_settings

    ex = json.loads((_repo_root() / "schemas" / "user-settings.v1.example.json").read_text(encoding="utf-8"))
    base = default_user_settings()
    assert base["schema_version"] == ex["schema_version"]
    for section in ("model", "ide"):
        for k in base[section]:
            assert k in ex[section], f"missing {section}.{k} in schema example"


def test_schema_example_documents_help_command_and_contract_tests():
    ex = json.loads((_repo_root() / "schemas" / "user-settings.v1.example.json").read_text(encoding="utf-8"))
    assert ex["ide"]["help_show_command_id"] == "leVibe.showChatCommandsHelp"
    meta = ex.get("meta") or {}
    assert "contract_tests" in meta
    assert "test_pm_ide_settings_workflows_contract.py" in meta["contract_tests"]
