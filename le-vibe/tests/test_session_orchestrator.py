"""PM session manifest seed, agent sync, and opening_intent / skip hooks."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

import le_vibe.session_orchestrator as session_orchestrator
import workspace_event_contract_utils as workspace_event_utils
from workspace_event_contract_utils import workspace_event_static_diagnostics
from workspace_event_contract_utils import discover_workspace_event_emitter_modules
from workspace_event_contract_utils import should_exclude_workspace_event_scan_path
from workspace_event_contract_utils import WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS
from workspace_event_contract_utils import WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS
from workspace_event_contract_utils import SAFE_UPDATE_STEP_PATTERNS
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
from workspace_event_contract_utils import HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX
from workspace_event_contract_utils import assert_safe_update_step_patterns_integrity
from workspace_event_contract_utils import assert_safe_update_procedure_docstring
from le_vibe.session_orchestrator import (
    GOAL_ALIGNMENT_CHECK_KEY,
    SESSION_MANIFEST_FILENAME,
    STOP_CONDITION_CHECK_KEY,
    apply_opening_skip,
    bundled_session_manifest_example_path,
    evaluate_stop_condition,
    evidence_artifact_registry,
    evidence_artifact_session_map,
    evidence_provenance_report,
    ensure_pm_session_artifacts,
    failure_mode_catalog,
    final_milestone_lock_criteria,
    get_milestone_by_id,
    get_product_milestones,
    goal_alignment_checks,
    get_session_steps,
    iter_tasks_in_epic_order,
    load_session_manifest,
    milestone_dependency_visibility,
    milestone_definition_of_done_checks,
    progress_confidence_report,
    persist_goal_alignment_check,
    persist_remaining_gaps_report,
    persist_release_readiness_summary,
    persist_stop_condition_check,
    remaining_gaps_report,
    release_readiness_summary,
    resolve_next_step_after_opening_skip,
    seed_session_manifest_if_missing,
    session_manifest_example_source_path,
    sync_agent_skills_from_templates,
    upsert_goal_alignment_check,
    upsert_final_milestone_lock_criteria,
    upsert_failure_mode_catalog,
    upsert_milestone_dependency_visibility,
    upsert_milestone_definition_of_done_checks,
    upsert_progress_confidence_report,
    upsert_remaining_gaps_report,
    upsert_release_readiness_summary,
    upsert_stop_condition_check,
    workspace_has_meaningful_files,
)


def _expected_agent_skill_count() -> int:
    templates_dir = Path(__file__).resolve().parents[1] / "templates" / "agents"
    return len([p for p in templates_dir.glob("*.md") if p.name.lower() != "readme.md"])


# PROCEDURE_GUARD #1: safe-update step patterns satisfy shared integrity constraints.
def test_safe_update_step_patterns_integrity_guard() -> None:
    assert_safe_update_step_patterns_integrity(SAFE_UPDATE_STEP_PATTERNS)


# PROCEDURE_GUARD #2: integrity helper remains stable across repeated invocation.
def test_safe_update_step_patterns_integrity_helper_is_idempotent() -> None:
    assert_safe_update_step_patterns_integrity(SAFE_UPDATE_STEP_PATTERNS)


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
    assert len(copied) == _expected_agent_skill_count()
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
    milestones = get_product_milestones(data)
    assert milestones
    milestone = milestones[0]
    assert milestone.get("id") == "milestone-foundation"
    assert isinstance(milestone.get("acceptance"), list)
    assert isinstance(milestone.get("exit_tests"), list)
    assert isinstance(milestone.get("owners"), list)


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


def test_apply_opening_skip_noop_when_not_at_opening_emits_no_log(tmp_path: Path, monkeypatch):
    ensure_pm_session_artifacts(tmp_path)
    # First skip transitions opening_intent -> agent_bootstrap/workspace_scan.
    apply_opening_skip(tmp_path, skipped_opening=True)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None
    assert events == []


def test_apply_opening_skip_noop_when_not_skipped_emits_no_log(tmp_path: Path, monkeypatch):
    ensure_pm_session_artifacts(tmp_path)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert apply_opening_skip(tmp_path, skipped_opening=False) is None
    assert events == []


def test_apply_opening_skip_noop_on_malformed_manifest(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    (lv / SESSION_MANIFEST_FILENAME).write_text("{not-json", encoding="utf-8")
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None


def test_apply_opening_skip_logs_manifest_missing_noop(tmp_path: Path, monkeypatch):
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None
    assert events, "expected structured log event"
    component, event, fields = events[-1]
    assert component == "workspace"
    assert event == "opening_skip_noop_manifest_missing"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert fields.get("schema_version") == "workspace_event.v1"


def test_apply_opening_skip_logs_malformed_manifest_noop(tmp_path: Path, monkeypatch):
    lv = tmp_path / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    (lv / SESSION_MANIFEST_FILENAME).write_text("{not-json", encoding="utf-8")
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None
    assert events, "expected structured log event"
    component, event, fields = events[-1]
    assert component == "workspace"
    assert event == "opening_skip_noop_malformed_manifest"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert fields.get("schema_version") == "workspace_event.v1"


def test_apply_opening_skip_logs_invalid_manifest_shape_noop(tmp_path: Path, monkeypatch):
    lv = tmp_path / ".lvibe"
    lv.mkdir(parents=True, exist_ok=True)
    (lv / SESSION_MANIFEST_FILENAME).write_text('["not-a-dict"]', encoding="utf-8")
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert apply_opening_skip(tmp_path, skipped_opening=True) is None
    assert events, "expected structured log event"
    component, event, fields = events[-1]
    assert component == "workspace"
    assert event == "opening_skip_noop_invalid_manifest_shape"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert fields.get("schema_version") == "workspace_event.v1"


def test_apply_opening_skip_logs_transition_when_applied(tmp_path: Path, monkeypatch):
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    ensure_pm_session_artifacts(tmp_path)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    nxt = apply_opening_skip(tmp_path, skipped_opening=True)
    assert nxt == "workspace_scan"
    transition = [e for e in events if e[1] == "opening_skip_applied"]
    assert transition, "expected opening_skip_applied event"
    component, event, fields = transition[-1]
    assert component == "workspace"
    assert event == "opening_skip_applied"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert fields.get("from_step") == "opening_intent"
    assert fields.get("to_step") == "workspace_scan"
    assert fields.get("schema_version") == "workspace_event.v1"


def test_apply_opening_skip_repairs_non_dict_meta_and_logs_noop(tmp_path: Path, monkeypatch):
    (tmp_path / "file.txt").write_text("x", encoding="utf-8")
    ensure_pm_session_artifacts(tmp_path)
    lv = tmp_path / ".lvibe"
    manifest_path = lv / SESSION_MANIFEST_FILENAME
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["meta"] = "not-a-dict"
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    nxt = apply_opening_skip(tmp_path, skipped_opening=True)
    assert nxt is None
    updated = load_session_manifest(lv)
    assert updated.get("meta") == "not-a-dict"
    noop = [e for e in events if e[1] == "opening_skip_noop_invalid_meta_shape"]
    assert noop, "expected opening_skip_noop_invalid_meta_shape event"
    component, event, fields = noop[-1]
    assert component == "workspace"
    assert event == "opening_skip_noop_invalid_meta_shape"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert fields.get("schema_version") == "workspace_event.v1"


def test_ensure_pm_session_artifacts_idempotent(tmp_path: Path):
    ensure_pm_session_artifacts(tmp_path)
    ensure_pm_session_artifacts(tmp_path)
    lv = tmp_path / ".lvibe"
    assert (lv / SESSION_MANIFEST_FILENAME).is_file()
    assert len(list((lv / "agents").glob("*/skill.md"))) == _expected_agent_skill_count()


def test_public_package_exports_resolve_next_step_after_opening_skip():
    import le_vibe as lv

    assert lv.resolve_next_step_after_opening_skip is resolve_next_step_after_opening_skip


def test_seeded_manifest_contains_start_and_end_goal_alignment_checks(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    checks = data["meta"][GOAL_ALIGNMENT_CHECK_KEY]
    assert checks["start"]["status"] == "aligned"
    assert checks["end"]["status"] == "pending"


def test_seeded_manifest_contains_stop_condition_check(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    check = data["meta"][STOP_CONDITION_CHECK_KEY]
    assert check["completion_allowed"] is False


def test_seeded_manifest_contains_release_readiness_summary(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    summary = data["meta"]["release_readiness_summary"]
    assert summary["ready"] is False
    assert "stop_condition_not_met" in summary["blockers"]


def test_seeded_manifest_contains_remaining_gaps_report(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    report = data["meta"]["remaining_gaps_report"]
    assert report["has_gaps"] is True
    assert report["gap_count"] >= 1


def test_seeded_manifest_contains_milestone_definition_of_done_checks(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    checks = data["meta"]["milestone_definition_of_done_checks"]
    assert checks["all_passed"] is True
    assert checks["passed"] == 1


def test_seeded_manifest_contains_milestone_dependency_visibility(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    vis = data["meta"]["milestone_dependency_visibility"]
    assert vis["has_missing"] is False
    assert vis["missing_count"] == 0


def test_get_milestone_by_id_finds_formal_schema_entry(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    milestone = get_milestone_by_id(data, "milestone-foundation")
    assert milestone is not None
    assert milestone.get("objective")
    assert milestone.get("acceptance")
    assert milestone.get("exit_tests")
    assert milestone.get("owners")


def test_milestone_definition_of_done_checks_detect_missing_fields():
    manifest = {
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "",
                    "acceptance": [],
                    "exit_tests": [],
                    "owners": [],
                }
            ]
        }
    }
    checks = milestone_definition_of_done_checks(manifest)
    assert checks["all_passed"] is False
    assert checks["failed"] == 1
    entry = checks["checks"][0]
    assert entry["passed"] is False
    assert entry["objective_ok"] is False


def test_upsert_milestone_definition_of_done_checks_writes_meta():
    manifest = {
        "meta": {},
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                }
            ]
        },
    }
    checks = upsert_milestone_definition_of_done_checks(manifest, source="test")
    assert checks["source"] == "test"
    assert manifest["meta"]["milestone_definition_of_done_checks"]["all_passed"] is True


def test_milestone_dependency_visibility_reports_missing_refs():
    manifest = {
        "product": {
            "milestones": [
                {"id": "m1", "dependencies": ["m2", "m3"]},
                {"id": "m2", "dependencies": []},
            ]
        }
    }
    vis = milestone_dependency_visibility(manifest)
    assert vis["has_missing"] is True
    assert vis["missing_count"] == 1
    m1 = next(e for e in vis["entries"] if e["id"] == "m1")
    assert m1["missing_dependencies"] == ["m3"]


def test_upsert_milestone_dependency_visibility_writes_meta():
    manifest = {
        "meta": {},
        "product": {
            "milestones": [
                {"id": "m1", "dependencies": []},
            ]
        },
    }
    vis = upsert_milestone_dependency_visibility(manifest, source="test_dep")
    assert vis["source"] == "test_dep"
    assert manifest["meta"]["milestone_dependency_visibility"]["total"] == 1


def test_upsert_goal_alignment_check_writes_phase_record():
    manifest: dict[str, object] = {}
    entry = upsert_goal_alignment_check(
        manifest,
        phase="start",
        goal="Ship session task",
        current_milestone="M1",
        final_milestone="M9",
        constraints=["keep scope narrow"],
        status="aligned",
        evidence=["picked bounded task"],
        notes="session kickoff",
    )
    assert entry["goal"] == "Ship session task"
    assert entry["status"] == "aligned"
    checks = goal_alignment_checks(manifest)
    assert checks["start"]["current_milestone"] == "M1"
    assert checks["start"]["evidence"] == ["picked bounded task"]


def test_upsert_goal_alignment_check_rejects_unknown_phase():
    manifest: dict[str, object] = {}
    with pytest.raises(ValueError):
        upsert_goal_alignment_check(
            manifest,
            phase="middle",
            goal="x",
            current_milestone="y",
            final_milestone="z",
        )


def test_persist_goal_alignment_check_updates_seeded_manifest(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    ok = persist_goal_alignment_check(
        ws,
        phase="start",
        status="aligned",
        evidence=["runtime-start"],
        notes="auto",
        current_milestone="Launcher session start",
    )
    assert ok is True
    data = load_session_manifest(ws / ".lvibe")
    start = data["meta"][GOAL_ALIGNMENT_CHECK_KEY]["start"]
    assert start["current_milestone"] == "Launcher session start"
    assert start["evidence"] == ["runtime-start"]
    assert start["notes"] == "auto"
    artifacts = data["meta"]["evidence_artifacts"]
    assert "runtime-start" in artifacts
    records = data["meta"]["evidence_artifact_records"]
    runtime_record = next(r for r in records if r["id"] == "runtime-start")
    assert runtime_record["session_id"] == data["meta"]["session_id"]


def test_persist_goal_alignment_check_repairs_missing_session_id(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    lvibe = ws / ".lvibe"
    path = lvibe / SESSION_MANIFEST_FILENAME
    data = load_session_manifest(lvibe)
    data["meta"].pop("session_id", None)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    assert (
        persist_goal_alignment_check(
            ws,
            phase="start",
            status="aligned",
            evidence=["repair-session-id"],
            notes="repair",
            current_milestone="Launcher session start",
        )
        is True
    )
    updated = load_session_manifest(lvibe)
    repaired = str(updated["meta"].get("session_id", "")).strip()
    assert repaired.startswith("runtime-")
    record = next(r for r in updated["meta"]["evidence_artifact_records"] if r["id"] == "repair-session-id")
    assert record["session_id"] == repaired


def test_persist_goal_alignment_check_logs_session_id_repair(tmp_path: Path, monkeypatch):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    lvibe = ws / ".lvibe"
    path = lvibe / SESSION_MANIFEST_FILENAME
    data = load_session_manifest(lvibe)
    data["meta"]["session_id"] = "   "
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert (
        persist_goal_alignment_check(
            ws,
            phase="start",
            status="aligned",
            evidence=["runtime-start"],
            notes="auto",
            current_milestone="Launcher session start",
        )
        is True
    )
    repairs = [e for e in events if e[1] == "session_id_repaired"]
    assert repairs
    component, event, fields = repairs[-1]
    assert component == "workspace"
    assert event == "session_id_repaired"
    assert fields.get("check") == "goal_alignment"
    assert fields.get("phase") == "start"
    assert fields.get("schema_version") == "workspace_event.v1"


def test_persist_goal_alignment_check_noop_when_manifest_missing(tmp_path: Path):
    ws = tmp_path
    assert persist_goal_alignment_check(ws, phase="start", status="aligned") is False


def test_evaluate_stop_condition_requires_both_flags_and_final_milestone():
    assert (
        evaluate_stop_condition(
            product_goals_satisfied=True,
            final_milestone_achieved=True,
            current_milestone="M9",
            final_milestone="M9",
        )
        is True
    )
    assert (
        evaluate_stop_condition(
            product_goals_satisfied=True,
            final_milestone_achieved=False,
            current_milestone="M9",
            final_milestone="M9",
        )
        is False
    )
    assert (
        evaluate_stop_condition(
            product_goals_satisfied=True,
            final_milestone_achieved=True,
            current_milestone="M8",
            final_milestone="M9",
        )
        is False
    )


def test_upsert_stop_condition_check_sets_completion_allowed():
    manifest: dict[str, object] = {}
    check = upsert_stop_condition_check(
        manifest,
        product_goals_satisfied=True,
        final_milestone_achieved=True,
        current_milestone="Final",
        final_milestone="Final",
        evidence=["all tests green"],
        notes="ready",
    )
    assert check["completion_allowed"] is True
    assert check["evidence"] == ["all tests green"]


def test_persist_stop_condition_check_updates_manifest(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    ok = persist_stop_condition_check(
        ws,
        product_goals_satisfied=False,
        final_milestone_achieved=False,
        current_milestone="Session end",
        final_milestone="Final milestone pending",
        evidence=["session ended"],
        notes="pending proof",
    )
    assert ok is True
    data = load_session_manifest(ws / ".lvibe")
    check = data["meta"][STOP_CONDITION_CHECK_KEY]
    assert check["completion_allowed"] is False
    assert check["current_milestone"] == "Session end"


def test_persist_stop_condition_check_noop_when_manifest_missing(tmp_path: Path):
    assert (
        persist_stop_condition_check(
            tmp_path,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="x",
            final_milestone="y",
        )
        is False
    )


@pytest.mark.parametrize(
    ("product_goals_satisfied", "final_milestone_achieved", "current_milestone", "final_milestone"),
    [
        (False, False, "M1", "M9"),
        (True, False, "M9", "M9"),
        (False, True, "M9", "M9"),
        (True, True, "M8", "M9"),
    ],
)
def test_stop_condition_stays_false_until_all_final_conditions_are_true(
    product_goals_satisfied: bool,
    final_milestone_achieved: bool,
    current_milestone: str,
    final_milestone: str,
):
    assert (
        evaluate_stop_condition(
            product_goals_satisfied=product_goals_satisfied,
            final_milestone_achieved=final_milestone_achieved,
            current_milestone=current_milestone,
            final_milestone=final_milestone,
        )
        is False
    )


def test_stop_condition_turns_true_only_at_verified_final_milestone():
    assert (
        evaluate_stop_condition(
            product_goals_satisfied=True,
            final_milestone_achieved=True,
            current_milestone="M9",
            final_milestone="M9",
        )
        is True
    )


def test_persist_stop_condition_false_then_true_transition(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="M8",
            final_milestone="M9",
            evidence=["partial"],
            notes="not done",
        )
        is True
    )
    first = load_session_manifest(ws / ".lvibe")
    assert first["meta"][STOP_CONDITION_CHECK_KEY]["completion_allowed"] is False

    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=True,
            final_milestone_achieved=True,
            current_milestone="M9",
            final_milestone="M9",
            evidence=["all acceptance tests pass"],
            notes="final milestone verified",
        )
        is True
    )
    second = load_session_manifest(ws / ".lvibe")
    assert second["meta"][STOP_CONDITION_CHECK_KEY]["completion_allowed"] is True
    records = second["meta"]["evidence_artifact_records"]
    latest = next(r for r in records if r["id"] == "all acceptance tests pass")
    assert latest["session_id"] == second["meta"]["session_id"]


def test_persist_stop_condition_refreshes_existing_artifact_record_session(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    lvibe = ws / ".lvibe"
    path = lvibe / SESSION_MANIFEST_FILENAME
    data = load_session_manifest(lvibe)
    data["meta"]["evidence_artifacts"] = ["same-artifact"]
    data["meta"]["evidence_artifact_records"] = [{"id": "same-artifact", "session_id": "old-session"}]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="M1",
            final_milestone="M9",
            evidence=["same-artifact"],
            notes="refresh artifact session",
        )
        is True
    )

    updated = load_session_manifest(lvibe)
    record = next(r for r in updated["meta"]["evidence_artifact_records"] if r["id"] == "same-artifact")
    assert record["session_id"] == updated["meta"]["session_id"]


def test_persist_stop_condition_repairs_invalid_session_id(tmp_path: Path):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    lvibe = ws / ".lvibe"
    path = lvibe / SESSION_MANIFEST_FILENAME
    data = load_session_manifest(lvibe)
    data["meta"]["session_id"] = "   "
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="M1",
            final_milestone="M9",
            evidence=["repair-invalid-session-id"],
            notes="repair",
        )
        is True
    )
    updated = load_session_manifest(lvibe)
    repaired = str(updated["meta"].get("session_id", "")).strip()
    assert repaired.startswith("runtime-")
    record = next(
        r for r in updated["meta"]["evidence_artifact_records"] if r["id"] == "repair-invalid-session-id"
    )
    assert record["session_id"] == repaired


def test_persist_stop_condition_logs_session_id_repair(tmp_path: Path, monkeypatch):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    lvibe = ws / ".lvibe"
    path = lvibe / SESSION_MANIFEST_FILENAME
    data = load_session_manifest(lvibe)
    data["meta"].pop("session_id", None)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="M1",
            final_milestone="M9",
            evidence=["session ended"],
            notes="pending proof",
        )
        is True
    )
    repairs = [e for e in events if e[1] == "session_id_repaired"]
    assert repairs
    component, event, fields = repairs[-1]
    assert component == "workspace"
    assert event == "session_id_repaired"
    assert fields.get("check") == "stop_condition"
    assert fields.get("schema_version") == "workspace_event.v1"


def test_persist_goal_alignment_check_applied_event_includes_contract_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert (
        persist_goal_alignment_check(
            ws,
            phase="start",
            status="aligned",
            evidence=["runtime-start"],
            notes="auto",
            current_milestone="Launcher session start",
        )
        is True
    )
    applied = [e for e in events if e[1] == "goal_alignment_check_applied"]
    assert applied
    _, _, fields = applied[-1]
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(ws.resolve())
    assert fields.get("phase") == "start"
    assert fields.get("status") == "aligned"


def test_persist_stop_condition_check_applied_event_includes_contract_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    ws = tmp_path
    ensure_pm_session_artifacts(ws)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert (
        persist_stop_condition_check(
            ws,
            product_goals_satisfied=False,
            final_milestone_achieved=False,
            current_milestone="M1",
            final_milestone="M9",
            evidence=["session ended"],
            notes="pending proof",
        )
        is True
    )
    applied = [e for e in events if e[1] == "stop_condition_check_applied"]
    assert applied
    _, _, fields = applied[-1]
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(ws.resolve())
    assert "completion_allowed" in fields


def test_emit_workspace_event_enforces_required_fields(tmp_path: Path):
    with pytest.raises(ValueError):
        session_orchestrator._emit_workspace_event(tmp_path, "goal_alignment_check_applied", phase="start")


def test_emit_workspace_event_allows_noop_without_extra_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    session_orchestrator._emit_workspace_event(tmp_path, "opening_skip_noop_manifest_missing")
    assert events
    _, event, fields = events[-1]
    assert event == "opening_skip_noop_manifest_missing"
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(tmp_path.resolve())


@pytest.mark.parametrize(
    ("event", "required"),
    sorted(session_orchestrator.WORKSPACE_EVENT_REQUIRED_FIELDS.items()),
)
def test_emit_workspace_event_contract_matrix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    event: str,
    required: tuple[str, ...],
):
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, emitted_event: str, **fields: object) -> None:
        events.append((component, emitted_event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    payload = {k: f"value-{k}" for k in required}
    session_orchestrator._emit_workspace_event(tmp_path, event, **payload)
    assert events
    component, emitted_event, fields = events[-1]
    assert component == "workspace"
    assert emitted_event == event
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(tmp_path.resolve())
    for key in required:
        assert key in fields


@pytest.mark.parametrize(
    ("event", "required"),
    [
        (event, required)
        for event, required in sorted(session_orchestrator.WORKSPACE_EVENT_REQUIRED_FIELDS.items())
        if required
    ],
)
def test_emit_workspace_event_rejects_missing_required_field(
    tmp_path: Path,
    event: str,
    required: tuple[str, ...],
):
    missing_key = required[0]
    payload = {k: f"value-{k}" for k in required[1:]}
    with pytest.raises(ValueError, match=missing_key):
        session_orchestrator._emit_workspace_event(tmp_path, event, **payload)


def test_emit_workspace_event_rejects_unregistered_event(tmp_path: Path):
    with pytest.raises(ValueError, match="not registered"):
        session_orchestrator._emit_workspace_event(tmp_path, "unregistered_workspace_event")


def test_workspace_event_registry_matches_emit_callsites():
    src_path = Path(session_orchestrator.__file__).resolve()
    emitted, errors = workspace_event_static_diagnostics(src_path)
    assert not errors, "\n".join(errors)
    registered = set(session_orchestrator.WORKSPACE_EVENT_REQUIRED_FIELDS.keys())
    assert emitted == registered


def test_workspace_event_static_diagnostics_report_line_and_column(tmp_path: Path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        "def f(tmp_path, event_name):\n"
        "    _emit_workspace_event(tmp_path, event_name)\n",
        encoding="utf-8",
    )
    _, errors = workspace_event_static_diagnostics(sample)
    assert errors
    msg = errors[0]
    assert "sample.py:2:" in msg
    assert "event id must be string literal" in msg


def test_workspace_event_literal_ids_hold_repo_wide_for_emitters():
    repo_root = Path(__file__).resolve().parents[1]
    le_vibe_pkg = repo_root / "le_vibe"
    modules_with_emit_calls = discover_workspace_event_emitter_modules(le_vibe_pkg)
    assert modules_with_emit_calls, "expected at least one workspace event emitter module"
    for module in modules_with_emit_calls:
        _, errors = workspace_event_static_diagnostics(module)
        assert not errors, "\n".join(errors)


def test_workspace_event_scan_exclusion_policy_handles_generated_and_vendor_paths():
    assert should_exclude_workspace_event_scan_path(Path("le_vibe/generated/foo.py")) is True
    assert should_exclude_workspace_event_scan_path(Path("le_vibe/vendor/foo.py")) is True
    assert should_exclude_workspace_event_scan_path(Path("le_vibe/third_party/foo.py")) is True
    assert should_exclude_workspace_event_scan_path(Path("le_vibe/core/foo.py")) is False


def test_workspace_event_scan_exclusion_policy_has_rationale_per_term():
    assert set(WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS) == set(WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS.keys())
    for part, reason in WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS.items():
        assert part.strip()
        assert reason.strip()


def test_workspace_event_scan_exclusion_terms_are_reviewed_policy_surface():
    expected = {"__pycache__", "generated", "third_party", "vendor"}
    actual = set(WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS.keys())
    assert actual == expected, (
        "exclusion terms changed: update rationale map intentionally and sync "
        "SESSION_ORCHESTRATION_SPEC + contract assertions"
    )


def test_workspace_event_contract_utils_docstring_keeps_safe_update_procedure():
    doc = workspace_event_utils.__doc__ or ""
    assert "Exported helper index" in doc
    assert "workspace_event_static_diagnostics" in doc
    assert "assert_safe_update_procedure_docstring" in doc
    assert_safe_update_procedure_docstring(doc, SAFE_UPDATE_STEP_PATTERNS)


def test_governance_comment_markers_present_in_session_orchestrator_tests():
    text = Path(__file__).read_text(encoding="utf-8")
    assert "Guard #1:" in text
    assert "Guard #2:" in text
    assert "Guard #3:" in text


def test_governance_comment_markers_are_adjacent_to_target_tests():
    lines = Path(__file__).read_text(encoding="utf-8").splitlines()
    expected_pairs = (
        ("# Guard #1:", "def test_workspace_event_helper_index_symbols_have_no_duplicates"),
        ("# Guard #2:", "def test_workspace_event_helper_index_symbols_derivation_is_explicit"),
        ("# Guard #3:", "def test_workspace_event_helper_index_symbols_keep_callable_then_constant_order"),
    )
    for guard_prefix, fn_def_prefix in expected_pairs:
        fn_idx = next(
            (idx for idx, line in enumerate(lines) if line.strip().startswith(fn_def_prefix)),
            -1,
        )
        assert fn_idx >= 0, fn_def_prefix
        guard_idx = -1
        for idx in range(fn_idx - 1, -1, -1):
            stripped = lines[idx].strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                guard_idx = idx
                break
            break
        assert guard_idx >= 0, guard_prefix
        assert lines[guard_idx].strip().startswith(guard_prefix), (guard_prefix, lines[guard_idx].strip())
        # Allow one blank spacer line for readability.
        assert fn_idx - guard_idx in (1, 2), (guard_prefix, fn_def_prefix, guard_idx, fn_idx)


def test_procedure_guard_markers_are_adjacent_to_target_tests():
    lines = Path(__file__).read_text(encoding="utf-8").splitlines()
    expected_pairs = (
        ("# PROCEDURE_GUARD #1:", "def test_safe_update_step_patterns_integrity_guard"),
        ("# PROCEDURE_GUARD #2:", "def test_safe_update_step_patterns_integrity_helper_is_idempotent"),
    )
    for guard_prefix, fn_def_prefix in expected_pairs:
        fn_idx = next(
            (idx for idx, line in enumerate(lines) if line.strip().startswith(fn_def_prefix)),
            -1,
        )
        assert fn_idx >= 0, fn_def_prefix
        guard_idx = -1
        for idx in range(fn_idx - 1, -1, -1):
            stripped = lines[idx].strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                guard_idx = idx
                break
            break
        assert guard_idx >= 0, guard_prefix
        assert lines[guard_idx].strip().startswith(guard_prefix), (guard_prefix, lines[guard_idx].strip())
        assert fn_idx - guard_idx in (1, 2), (guard_prefix, fn_def_prefix, guard_idx, fn_idx)


def test_helper_index_governance_anchor_token_present():
    text = Path(__file__).read_text(encoding="utf-8")
    # Anchor prefix is shared-policy metadata and should remain tied to this governance block.
    assert HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX in text
    lines = text.splitlines()
    anchor_comment_lines = [
        line for line in lines if line.strip().startswith(HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX)
    ]
    assert len(anchor_comment_lines) == 1
    target_idx = next(
        (
            idx
            for idx, line in enumerate(lines)
            if line.strip().startswith("def test_workspace_event_contract_utils_helper_index_matches_exports")
        ),
        -1,
    )
    assert target_idx >= 0
    preceding_comment_idx = -1
    for idx in range(target_idx - 1, -1, -1):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            preceding_comment_idx = idx
            break
        # Stop when we hit non-comment code before finding a comment marker.
        break
    assert preceding_comment_idx >= 0
    assert "HELPER_INDEX_GOVERNANCE" in lines[preceding_comment_idx]


# HELPER_INDEX_GOVERNANCE: keeps exported symbol docs, ordering, and partition semantics aligned.
def test_workspace_event_contract_utils_helper_index_matches_exports():
    doc = workspace_event_utils.__doc__ or ""
    # HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX is covered via canonical symbol tuple membership.
    for name in WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS:
        assert f"- {name}" in doc
        assert hasattr(workspace_event_utils, name), name


def test_workspace_event_contract_utils_helper_index_order_is_canonical():
    doc = workspace_event_utils.__doc__ or ""
    # Order is verified against the same canonical tuple used for export-coverage checks.
    positions = [doc.index(f"- {name}") for name in WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS]
    assert positions == sorted(positions)


# Guard #1: symbol list stays collision-free.
def test_workspace_event_helper_index_symbols_have_no_duplicates():
    # Duplicate detection also operates on canonical tuple membership.
    assert len(WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS) == len(set(WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS))


# Guard #2: index remains explicitly derived from callable + constant partitions.
def test_workspace_event_helper_index_symbols_derivation_is_explicit():
    # Derivation stays single-sourced: canonical tuple equals callable + constant partitions.
    assert (
        WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS
        == WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS + WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
    )


# Guard #3: category ordering remains callable section then constant section.
def test_workspace_event_helper_index_symbols_keep_callable_then_constant_order():
    callable_count = len(WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS)
    assert WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS[:callable_count] == WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS
    assert WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS[callable_count:] == WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS


def test_release_readiness_summary_ready_when_checks_and_tasks_complete():
    manifest = {
        "meta": {
            "session_id": "s1",
            "evidence_artifacts": ["acceptance.complete", "exit_tests.complete"],
            "evidence_artifact_records": [
                {"id": "acceptance.complete", "session_id": "s1"},
                {"id": "exit_tests.complete", "session_id": "s1"},
            ],
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["acceptance.complete"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["exit_tests.complete"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [
                {
                    "id": "e1",
                    "title": "t",
                    "tasks": [{"id": "a", "status": "done"}, {"id": "b", "status": "done"}],
                }
            ]
        },
    }
    summary = release_readiness_summary(manifest)
    assert summary["ready"] is True
    assert summary["total_tasks"] == 2
    assert summary["blockers"] == []


def test_upsert_release_readiness_summary_adds_meta_entry():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "pending"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {"epics": []},
    }
    summary = upsert_release_readiness_summary(manifest, source="test")
    assert summary["source"] == "test"
    assert "release_readiness_summary" in manifest["meta"]


def test_persist_release_readiness_summary_writes_manifest(tmp_path: Path):
    ensure_pm_session_artifacts(tmp_path)
    assert persist_release_readiness_summary(tmp_path, source="test_persist") is True
    data = load_session_manifest(tmp_path / ".lvibe")
    summary = data["meta"]["release_readiness_summary"]
    assert summary["source"] == "test_persist"
    assert summary["ready"] is False
    dod = data["meta"]["milestone_definition_of_done_checks"]
    assert dod["source"] == "test_persist"
    deps = data["meta"]["milestone_dependency_visibility"]
    assert deps["source"] == "test_persist"
    progress = data["meta"]["progress_confidence_report"]
    assert progress["source"] == "test_persist"
    lock = data["meta"]["final_milestone_lock_criteria"]
    assert lock["source"] == "test_persist"
    cat = data["meta"]["failure_mode_catalog"]
    assert cat["source"] == "test_persist"


def test_persist_release_readiness_summary_logs_contract_fields(tmp_path: Path, monkeypatch):
    ensure_pm_session_artifacts(tmp_path)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert persist_release_readiness_summary(tmp_path, source="test_persist") is True
    applied = [e for e in events if e[1] == "release_readiness_applied"]
    assert applied
    _, _, fields = applied[-1]
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert "ready" in fields
    assert "blockers" in fields


def test_remaining_gaps_report_tracks_release_blockers():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "pending"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {"epics": [{"id": "e", "title": "x", "tasks": [{"id": "t", "status": "pending"}]}]},
    }
    report = remaining_gaps_report(manifest)
    assert report["has_gaps"] is True
    assert "stop_condition_not_met" in report["gaps"]


def test_upsert_remaining_gaps_report_adds_meta_entry():
    manifest = {"meta": {}, "product": {"epics": []}}
    report = upsert_remaining_gaps_report(manifest, source="test_gaps")
    assert report["source"] == "test_gaps"
    assert "remaining_gaps_report" in manifest["meta"]


def test_persist_remaining_gaps_report_writes_manifest(tmp_path: Path):
    ensure_pm_session_artifacts(tmp_path)
    assert persist_remaining_gaps_report(tmp_path, source="test_persist_gaps") is True
    data = load_session_manifest(tmp_path / ".lvibe")
    report = data["meta"]["remaining_gaps_report"]
    assert report["source"] == "test_persist_gaps"
    assert report["has_gaps"] is True


def test_persist_remaining_gaps_report_logs_contract_fields(tmp_path: Path, monkeypatch):
    ensure_pm_session_artifacts(tmp_path)
    events: list[tuple[str, str, dict[str, object]]] = []

    def _fake_log(component: str, event: str, **fields: object) -> None:
        events.append((component, event, fields))

    monkeypatch.setattr("le_vibe.session_orchestrator.append_structured_log", _fake_log)
    assert persist_remaining_gaps_report(tmp_path, source="test_persist_gaps") is True
    applied = [e for e in events if e[1] == "remaining_gaps_applied"]
    assert applied
    _, _, fields = applied[-1]
    assert fields.get("schema_version") == "workspace_event.v1"
    assert fields.get("workspace") == str(tmp_path.resolve())
    assert "gap_count" in fields


def test_seeded_manifest_contains_progress_confidence_report(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    report = data["meta"]["progress_confidence_report"]
    assert "confidence_score" in report
    assert report["drift_detected"] is False


def test_seeded_manifest_contains_final_milestone_lock_criteria(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    lock = data["meta"]["final_milestone_lock_criteria"]
    assert lock["locked"] is False
    assert "criteria" in lock


def test_seeded_manifest_contains_failure_mode_catalog(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    cat = data["meta"]["failure_mode_catalog"]
    assert cat["total"] >= 1
    assert isinstance(cat["modes"], list)


def test_seeded_manifest_contains_evidence_artifact_registry(tmp_path: Path):
    lv = tmp_path / ".lvibe"
    lv.mkdir()
    seed_session_manifest_if_missing(lv)
    data = load_session_manifest(lv)
    registry = evidence_artifact_registry(data)
    assert "acceptance.complete" in registry
    assert "exit_tests.complete" in registry
    sessions = evidence_artifact_session_map(data)
    assert sessions["acceptance.complete"] == "example-local-dev"


def test_progress_confidence_report_flags_drift_when_alignment_ahead_of_execution():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "aligned"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "pending"}]}],
        },
    }
    report = progress_confidence_report(manifest)
    assert report["drift_detected"] is True
    assert report["drift_reason"] == "goal_alignment_end_aligned_but_task_progress_low"


def test_upsert_progress_confidence_report_writes_meta():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "pending"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {"milestones": [], "epics": []},
    }
    report = upsert_progress_confidence_report(manifest, source="test_progress")
    assert report["source"] == "test_progress"
    assert "progress_confidence_report" in manifest["meta"]


def test_final_milestone_lock_criteria_requires_acceptance_evidence():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["aligned"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": []},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    lock = final_milestone_lock_criteria(manifest)
    assert lock["locked"] is False
    assert lock["criteria"]["stop_condition_evidence_present"] is False


def test_final_milestone_lock_criteria_requires_traceable_evidence():
    manifest = {
        "meta": {
            "evidence_artifacts": ["acceptance.complete", "exit_tests.complete"],
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["acceptance.complete"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["unknown-artifact"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    lock = final_milestone_lock_criteria(manifest)
    assert lock["locked"] is False
    assert lock["criteria"]["stop_condition_evidence_traceable"] is False
    assert lock["evidence_provenance"]["stop_condition"]["untraceable"] == ["unknown-artifact"]


def test_evidence_provenance_report_separates_traceable_and_untraceable():
    manifest = {"meta": {"evidence_artifacts": ["a", "b"]}}
    report = evidence_provenance_report(manifest, ["a", "c"])
    assert report["traceable"] == ["a"]
    assert report["untraceable"] == ["c"]
    assert report["all_traceable"] is False


def test_evidence_provenance_report_marks_stale_when_session_differs():
    manifest = {
        "meta": {
            "session_id": "s2",
            "evidence_artifacts": ["a"],
            "evidence_artifact_records": [{"id": "a", "session_id": "s1"}],
        }
    }
    report = evidence_provenance_report(manifest, ["a"])
    assert report["traceable"] == ["a"]
    assert report["stale"] == ["a"]
    assert report["all_fresh"] is False


def test_final_milestone_lock_criteria_requires_fresh_evidence():
    manifest = {
        "meta": {
            "session_id": "s2",
            "evidence_artifacts": ["acceptance.complete", "exit_tests.complete"],
            "evidence_artifact_records": [
                {"id": "acceptance.complete", "session_id": "s2"},
                {"id": "exit_tests.complete", "session_id": "s1"},
            ],
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["acceptance.complete"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["exit_tests.complete"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    lock = final_milestone_lock_criteria(manifest)
    assert lock["locked"] is False
    assert lock["criteria"]["stop_condition_evidence_fresh"] is False
    assert lock["evidence_provenance"]["stop_condition"]["stale"] == ["exit_tests.complete"]


def test_release_readiness_summary_adds_untraceable_evidence_blocker():
    manifest = {
        "meta": {
            "evidence_artifacts": ["acceptance.complete", "exit_tests.complete"],
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["acceptance.complete"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["missing.trace"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    summary = release_readiness_summary(manifest)
    assert summary["ready"] is False
    assert "final_milestone_evidence_untraceable" in summary["blockers"]


def test_release_readiness_summary_adds_stale_evidence_blocker():
    manifest = {
        "meta": {
            "session_id": "s2",
            "evidence_artifacts": ["acceptance.complete", "exit_tests.complete"],
            "evidence_artifact_records": [
                {"id": "acceptance.complete", "session_id": "s2"},
                {"id": "exit_tests.complete", "session_id": "s1"},
            ],
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["acceptance.complete"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["exit_tests.complete"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    summary = release_readiness_summary(manifest)
    assert summary["ready"] is False
    assert "final_milestone_evidence_stale" in summary["blockers"]


def test_upsert_final_milestone_lock_criteria_writes_meta():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "aligned", "evidence": ["ok"]}},
            "stop_condition_check": {"completion_allowed": True, "evidence": ["ok"]},
        },
        "product": {
            "milestones": [
                {
                    "id": "m1",
                    "objective": "obj",
                    "acceptance": ["a"],
                    "exit_tests": ["t"],
                    "owners": ["@prod"],
                    "dependencies": [],
                }
            ],
            "epics": [{"id": "e1", "title": "x", "tasks": [{"id": "t1", "status": "done"}]}],
        },
    }
    lock = upsert_final_milestone_lock_criteria(manifest, source="test_lock")
    assert lock["source"] == "test_lock"
    assert "final_milestone_lock_criteria" in manifest["meta"]


def test_failure_mode_catalog_maps_blockers_to_entries():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "pending"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {"milestones": [], "epics": []},
    }
    cat = failure_mode_catalog(manifest)
    ids = [m["id"] for m in cat["modes"]]
    assert "stop_condition_not_met" in ids
    stop_mode = next(m for m in cat["modes"] if m["id"] == "stop_condition_not_met")
    assert stop_mode["severity"] == "high"


def test_upsert_failure_mode_catalog_writes_meta():
    manifest = {
        "meta": {
            "goal_alignment_check": {"end": {"status": "pending"}},
            "stop_condition_check": {"completion_allowed": False},
        },
        "product": {"milestones": [], "epics": []},
    }
    cat = upsert_failure_mode_catalog(manifest, source="test_failure_modes")
    assert cat["source"] == "test_failure_modes"
    assert "failure_mode_catalog" in manifest["meta"]
