"""PM session manifest seed, agent sync, and opening_intent / skip hooks."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.session_orchestrator import (
    SESSION_MANIFEST_FILENAME,
    apply_opening_skip,
    bundled_session_manifest_example_path,
    ensure_pm_session_artifacts,
    get_session_steps,
    iter_tasks_in_epic_order,
    load_session_manifest,
    resolve_next_step_after_opening_skip,
    seed_session_manifest_if_missing,
    session_manifest_example_source_path,
    sync_agent_skills_from_templates,
    workspace_has_meaningful_files,
)


def test_bundled_example_matches_repo_schema():
    bundled = bundled_session_manifest_example_path()
    assert bundled.is_file()
    repo_root = Path(__file__).resolve().parents[2]
    canonical = repo_root / "schemas" / "session-manifest.v1.example.json"
    assert canonical.is_file()
    assert json.loads(bundled.read_text(encoding="utf-8")) == json.loads(
        canonical.read_text(encoding="utf-8")
    )


def test_session_manifest_example_source_prefers_repo_schemas():
    repo_root = Path(__file__).resolve().parents[2]
    src = session_manifest_example_source_path()
    assert src == repo_root / "schemas" / "session-manifest.v1.example.json"
    assert json.loads(src.read_text(encoding="utf-8")) == json.loads(
        bundled_session_manifest_example_path().read_text(encoding="utf-8")
    )


def test_seed_and_sync_creates_manifest_and_agents(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    assert (lv / SESSION_MANIFEST_FILENAME).is_file()
    copied = sync_agent_skills_from_templates(lv)
    assert len(copied) == 8
    assert all(p.name == "skill.md" for p in copied)


def test_seed_idempotent(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    p = seed_session_manifest_if_missing(lv)
    assert p is not None
    assert seed_session_manifest_if_missing(lv) is None


def test_load_manifest_steps_and_tasks(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    steps = get_session_steps(data)
    assert [s["id"] for s in steps][:2] == ["opening_intent", "workspace_scan"]
    tasks = list(iter_tasks_in_epic_order(data))
    assert len(tasks) == 1
    eid, etitle, task = tasks[0]
    assert eid == "epic-example-001"
    assert task.get("id") == "task-example-001"


def test_workspace_nonempty_heuristic(tmp_path: Path):
    assert workspace_has_meaningful_files(tmp_path) is False
    (tmp_path / ".lvibe").mkdir()
    assert workspace_has_meaningful_files(tmp_path) is False
    (tmp_path / "src").mkdir()
    assert workspace_has_meaningful_files(tmp_path) is True


def test_resolve_skip_nonempty_vs_empty(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    assert resolve_next_step_after_opening_skip(data, tmp_path) == "agent_bootstrap"
    (tmp_path / "go.mod").write_text("module x\n", encoding="utf-8")
    assert resolve_next_step_after_opening_skip(data, tmp_path) == "workspace_scan"


def test_apply_opening_skip_advances_manifest(tmp_path: Path):
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    ensure_pm_session_artifacts(tmp_path)
    lv = tmp_path / ".lvibe"
    assert (lv / SESSION_MANIFEST_FILENAME).is_file()
    nxt = apply_opening_skip(tmp_path, skipped_opening=True)
    assert nxt == "workspace_scan"
    data = load_session_manifest(lv)
    assert data["meta"]["current_step_id"] == "workspace_scan"
    assert (lv / "memory" / "workspace-scan.md").is_file()


def test_apply_opening_skip_noop_when_not_at_opening(tmp_path: Path):
    ensure_pm_session_artifacts(tmp_path)
    apply_opening_skip(tmp_path, skipped_opening=True)
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None


def test_ensure_pm_session_artifacts_idempotent(tmp_path: Path):
    ensure_pm_session_artifacts(tmp_path)
    ensure_pm_session_artifacts(tmp_path)
    lv = tmp_path / ".lvibe"
    assert (lv / SESSION_MANIFEST_FILENAME).is_file()
    assert len(list((lv / "agents").glob("*/skill.md"))) == 8
