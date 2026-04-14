"""PM session manifest: seed, skill sync, session_steps, and opening_intent / skip → workspace_scan hooks.

See ``docs/SESSION_ORCHESTRATION_SPEC.md`` and ``schemas/session-manifest.v1.example.json``.
"""

from __future__ import annotations

import json
import re
import shutil
import uuid
from pathlib import Path
from typing import Any, Iterator

from .structured_log import append_structured_log

SESSION_MANIFEST_FILENAME = "session-manifest.json"
OPENING_INTENT_ID = "opening_intent"
GOAL_ALIGNMENT_CHECK_KEY = "goal_alignment_check"
GOAL_ALIGNMENT_PHASES = {"start", "end"}
STOP_CONDITION_CHECK_KEY = "stop_condition_check"
RELEASE_READINESS_SUMMARY_KEY = "release_readiness_summary"
CI_EVIDENCE_SUMMARY_KEY = "ci_evidence_summary"
REMAINING_GAPS_REPORT_KEY = "remaining_gaps_report"
MILESTONE_DOD_CHECKS_KEY = "milestone_definition_of_done_checks"
MILESTONE_DEPENDENCY_VISIBILITY_KEY = "milestone_dependency_visibility"
PROGRESS_CONFIDENCE_REPORT_KEY = "progress_confidence_report"
FINAL_MILESTONE_LOCK_CRITERIA_KEY = "final_milestone_lock_criteria"
FAILURE_MODE_CATALOG_KEY = "failure_mode_catalog"
EVIDENCE_ARTIFACTS_KEY = "evidence_artifacts"
EVIDENCE_ARTIFACT_RECORDS_KEY = "evidence_artifact_records"
WORKSPACE_EVENT_SCHEMA_VERSION = "workspace_event.v1"
BLOCKER_GROUP_BASE = "base"
BLOCKER_GROUP_EVIDENCE = "evidence"
FAILURE_MODE_ALLOWED_SEVERITIES: tuple[str, ...] = ("high", "medium")
FAILURE_MODE_BLOCKER_POLICY: tuple[tuple[str, str, str], ...] = (
    ("goal_alignment_end_not_aligned", BLOCKER_GROUP_BASE, "medium"),
    ("stop_condition_not_met", BLOCKER_GROUP_BASE, "high"),
    ("blocked_tasks_present", BLOCKER_GROUP_BASE, "medium"),
    ("incomplete_tasks_present", BLOCKER_GROUP_BASE, "medium"),
    ("milestone_definition_of_done_incomplete", BLOCKER_GROUP_BASE, "medium"),
    ("milestone_dependency_missing_reference", BLOCKER_GROUP_BASE, "medium"),
    ("progress_drift_detected", BLOCKER_GROUP_BASE, "medium"),
    ("final_milestone_evidence_untraceable", BLOCKER_GROUP_EVIDENCE, "high"),
    ("final_milestone_evidence_stale", BLOCKER_GROUP_EVIDENCE, "high"),
    ("final_milestone_lock_not_satisfied", BLOCKER_GROUP_BASE, "high"),
    ("ci_failures_present", BLOCKER_GROUP_BASE, "medium"),
)
FAILURE_MODE_SEVERITY_BY_BLOCKER: dict[str, str] = {
    blocker_id: severity for blocker_id, _group, severity in FAILURE_MODE_BLOCKER_POLICY
}
RELEASE_READINESS_BASE_BLOCKER_IDS: tuple[str, ...] = tuple(
    blocker_id
    for blocker_id, group, _severity in FAILURE_MODE_BLOCKER_POLICY
    if group == BLOCKER_GROUP_BASE
)
RELEASE_READINESS_EVIDENCE_BLOCKER_IDS: tuple[str, ...] = tuple(
    blocker_id
    for blocker_id, group, _severity in FAILURE_MODE_BLOCKER_POLICY
    if group == BLOCKER_GROUP_EVIDENCE
)


def failure_mode_severity_taxonomy_diagnostics() -> dict[str, Any]:
    """Return parity diagnostics between policy-used and allowed severities."""
    allowed = set(FAILURE_MODE_ALLOWED_SEVERITIES)
    used = {severity for _blocker_id, _group, severity in FAILURE_MODE_BLOCKER_POLICY}
    unknown = sorted(used.difference(allowed))
    unused = sorted(allowed.difference(used))
    return {
        "allowed_severities": sorted(allowed),
        "used_severities": sorted(used),
        "unknown_severities": unknown,
        "unused_allowed_severities": unused,
    }
# Developer checklist for adding a new workspace event:
# 1) Add event id to WORKSPACE_EVENT_REQUIRED_FIELDS with required payload keys.
# 2) Emit the event only via _emit_workspace_event (not append_structured_log directly).
# 3) Extend test_emit_workspace_event_contract_matrix expectations as needed.
# 4) Update docs/SESSION_ORCHESTRATION_SPEC.md structured-log contract section.
WORKSPACE_EVENT_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "goal_alignment_check_noop_manifest_missing": ("phase",),
    "goal_alignment_check_noop_malformed_manifest": ("phase",),
    "goal_alignment_check_noop_invalid_manifest_shape": ("phase",),
    "goal_alignment_check_noop_invalid_phase": ("phase",),
    "session_id_repaired": ("check", "repaired_session_id"),
    "goal_alignment_check_applied": ("phase", "status"),
    "stop_condition_check_noop_manifest_missing": (),
    "stop_condition_check_noop_malformed_manifest": (),
    "stop_condition_check_noop_invalid_manifest_shape": (),
    "stop_condition_check_applied": ("completion_allowed",),
    "release_readiness_noop_manifest_missing": (),
    "release_readiness_noop_malformed_manifest": (),
    "release_readiness_noop_invalid_manifest_shape": (),
    "release_readiness_applied": ("ready", "blockers"),
    "remaining_gaps_noop_manifest_missing": (),
    "remaining_gaps_noop_malformed_manifest": (),
    "remaining_gaps_noop_invalid_manifest_shape": (),
    "remaining_gaps_applied": ("gap_count",),
    "opening_skip_noop_manifest_missing": (),
    "opening_skip_noop_malformed_manifest": (),
    "opening_skip_noop_invalid_manifest_shape": (),
    "opening_skip_noop_invalid_meta_shape": (),
    "opening_skip_applied": ("from_step", "to_step"),
}


def bundled_session_manifest_example_path() -> Path:
    """Shipped copy of the canonical example (kept in sync with ``schemas/session-manifest.v1.example.json``)."""
    return Path(__file__).resolve().parent / "assets" / "session-manifest.v1.example.json"


def session_manifest_example_source_path() -> Path:
    """
    Source for new ``.lvibe/session-manifest.json`` seeds.

    When running from a monorepo checkout, prefer the repo-root ``schemas/session-manifest.v1.example.json``
    (``SESSION_ORCHESTRATION_SPEC`` / STEP 2). Installed packages fall back to the bundled asset
    (must match the schema — see ``test_session_orchestrator.test_bundled_example_matches_repo_schema``).
    """
    here = Path(__file__).resolve()
    for d in (here.parent, *here.parents):
        cand = d / "schemas" / "session-manifest.v1.example.json"
        if cand.is_file():
            return cand
    return bundled_session_manifest_example_path()


def agent_skill_templates_dir() -> Path:
    """``le-vibe/templates/agents/`` (sibling of the ``le_vibe`` package)."""
    return Path(__file__).resolve().parent.parent / "templates" / "agents"


def seed_session_manifest_if_missing(lvibe_dir: Path) -> Path | None:
    """
    If ``.lvibe/session-manifest.json`` is absent, copy the bundled example.
    Does not overwrite an existing file (PM edits preserved).
    """
    lvibe_dir.mkdir(parents=True, exist_ok=True)
    dest = lvibe_dir / SESSION_MANIFEST_FILENAME
    if dest.exists():
        return None
    src = session_manifest_example_source_path()
    shutil.copy2(src, dest)
    return dest


def sync_agent_skills_from_templates(lvibe_dir: Path) -> list[Path]:
    """
    Copy each ``templates/agents/*.md`` into ``.lvibe/agents/<agent_id>/skill.md`` when missing
    (PRODUCT_SPEC §5.2 per-agent subtrees; ``agent_id`` is the template stem).
    """
    dest_root = lvibe_dir / "agents"
    dest_root.mkdir(parents=True, exist_ok=True)
    src_dir = agent_skill_templates_dir()
    written: list[Path] = []
    for src in sorted(src_dir.glob("*.md")):
        if src.name.lower() == "readme.md":
            continue
        agent_id = src.stem
        dest_dir = dest_root / agent_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "skill.md"
        if not dest.exists():
            shutil.copy2(src, dest)
            written.append(dest)
    return written


def load_session_manifest(lvibe_dir: Path) -> dict[str, Any]:
    """Parse ``session-manifest.json`` under ``lvibe_dir``."""
    p = lvibe_dir / SESSION_MANIFEST_FILENAME
    return json.loads(p.read_text(encoding="utf-8"))


def get_session_steps(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Ordered ``session_steps`` entries from the manifest."""
    steps = manifest.get("session_steps")
    if not isinstance(steps, list):
        return []
    return [s for s in steps if isinstance(s, dict)]


def get_step_by_id(manifest: dict[str, Any], step_id: str) -> dict[str, Any] | None:
    for s in get_session_steps(manifest):
        if s.get("id") == step_id:
            return s
    return None


def goal_alignment_checks(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Return ``meta.goal_alignment_check`` as a mutable dict.

    The value is normalized to a dict to keep malformed manifests from breaking
    orchestration helpers. Callers can safely write phase records under ``start``
    and ``end`` keys.
    """
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    checks = meta.get(GOAL_ALIGNMENT_CHECK_KEY)
    if isinstance(checks, dict):
        return checks
    checks = {}
    meta[GOAL_ALIGNMENT_CHECK_KEY] = checks
    return checks


def upsert_goal_alignment_check(
    manifest: dict[str, Any],
    *,
    phase: str,
    goal: str,
    current_milestone: str,
    final_milestone: str,
    constraints: list[str] | None = None,
    status: str = "aligned",
    evidence: list[str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """
    Write a normalized ``goal_alignment_check`` record for ``phase``.

    ``phase`` must be ``start`` or ``end`` (session boundary checks from the
    orchestration session playbook).
    """
    phase_norm = phase.strip().lower()
    if phase_norm not in GOAL_ALIGNMENT_PHASES:
        raise ValueError(f"unsupported goal alignment phase: {phase!r}")
    checks = goal_alignment_checks(manifest)
    entry = {
        "goal": goal,
        "current_milestone": current_milestone,
        "final_milestone": final_milestone,
        "constraints": list(constraints or []),
        "status": status,
        "evidence": list(evidence or []),
        "notes": notes,
    }
    checks[phase_norm] = entry
    return entry


def _upsert_runtime_evidence_artifacts(
    manifest: dict[str, Any],
    *,
    evidence: list[str] | None,
) -> None:
    """
    Refresh evidence registry + session records from runtime writes.
    """
    if not isinstance(evidence, list):
        return
    normalized = [str(item).strip() for item in evidence if str(item).strip()]
    if not normalized:
        return
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    current_session_id = str(meta.get("session_id", "")).strip()
    if not current_session_id:
        return

    registry = evidence_artifact_registry(manifest)
    registry_set = set(registry)
    for artifact_id in normalized:
        if artifact_id not in registry_set:
            registry.append(artifact_id)
            registry_set.add(artifact_id)
    meta[EVIDENCE_ARTIFACTS_KEY] = registry

    records_raw = meta.get(EVIDENCE_ARTIFACT_RECORDS_KEY)
    records: list[dict[str, str]]
    if isinstance(records_raw, list):
        records = [r for r in records_raw if isinstance(r, dict)]
    else:
        records = []

    existing_idx: dict[str, int] = {}
    for idx, record in enumerate(records):
        artifact_id = str(record.get("id", "")).strip()
        if artifact_id and artifact_id not in existing_idx:
            existing_idx[artifact_id] = idx

    for artifact_id in normalized:
        idx = existing_idx.get(artifact_id)
        if idx is None:
            records.append({"id": artifact_id, "session_id": current_session_id})
            existing_idx[artifact_id] = len(records) - 1
            continue
        records[idx] = {"id": artifact_id, "session_id": current_session_id}

    meta[EVIDENCE_ARTIFACT_RECORDS_KEY] = records


def _ensure_manifest_session_id(manifest: dict[str, Any]) -> tuple[str, bool, str]:
    """
    Ensure ``meta.session_id`` is present and non-empty.

    Returns ``(session_id, repaired, previous_raw)``.
    """
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    current = str(meta.get("session_id", "")).strip()
    if current:
        return current, False, current
    previous_raw = str(meta.get("session_id", ""))
    generated = f"runtime-{uuid.uuid4()}"
    meta["session_id"] = generated
    return generated, True, previous_raw


def _emit_workspace_event(workspace_root: Path, event: str, **fields: Any) -> None:
    """
    Emit a workspace structured-log event with ``workspace_event.v1`` contract.

    Contributor rule: pass event ids as string literals at callsites.
    Dynamic/computed ids break the static parity guard test that keeps
    ``_emit_workspace_event`` usage aligned with ``WORKSPACE_EVENT_REQUIRED_FIELDS``.
    """
    if event not in WORKSPACE_EVENT_REQUIRED_FIELDS:
        raise ValueError(f"workspace event {event!r} is not registered in WORKSPACE_EVENT_REQUIRED_FIELDS")
    required = WORKSPACE_EVENT_REQUIRED_FIELDS[event]
    missing = [k for k in required if fields.get(k) is None]
    if missing:
        raise ValueError(f"workspace event {event!r} missing required fields: {', '.join(missing)}")
    append_structured_log(
        "workspace",
        event,
        schema_version=WORKSPACE_EVENT_SCHEMA_VERSION,
        workspace=str(workspace_root.resolve()),
        **fields,
    )


def persist_goal_alignment_check(
    workspace_root: Path,
    *,
    phase: str,
    status: str,
    evidence: list[str] | None = None,
    notes: str = "",
    current_milestone: str | None = None,
) -> bool:
    """
    Persist a goal-alignment boundary record into ``.lvibe/session-manifest.json``.

    Returns ``True`` when a manifest was updated, else ``False`` (missing/malformed
    manifest or unsupported phase).
    """
    lvibe_dir = workspace_root / ".lvibe"
    path = lvibe_dir / SESSION_MANIFEST_FILENAME
    if not path.is_file():
        _emit_workspace_event(workspace_root, "goal_alignment_check_noop_manifest_missing", phase=phase)
        return False
    try:
        data = load_session_manifest(lvibe_dir)
    except (OSError, json.JSONDecodeError):
        _emit_workspace_event(workspace_root, "goal_alignment_check_noop_malformed_manifest", phase=phase)
        return False
    if not isinstance(data, dict):
        _emit_workspace_event(workspace_root, "goal_alignment_check_noop_invalid_manifest_shape", phase=phase)
        return False
    session_id, repaired, previous_raw = _ensure_manifest_session_id(data)
    if repaired:
        _emit_workspace_event(
            workspace_root,
            "session_id_repaired",
            check="goal_alignment",
            phase=phase,
            previous_session_id=previous_raw,
            repaired_session_id=session_id,
        )
    checks = goal_alignment_checks(data)
    prior = checks.get(phase)
    prior_d = prior if isinstance(prior, dict) else {}
    goal = str(prior_d.get("goal") or "Ship one orchestration task per session with evidence.")
    final_milestone = str(prior_d.get("final_milestone") or "Release-ready orchestration")
    constraints_raw = prior_d.get("constraints")
    constraints = constraints_raw if isinstance(constraints_raw, list) else []
    current = current_milestone or str(prior_d.get("current_milestone") or f"session_{phase}")
    try:
        upsert_goal_alignment_check(
            data,
            phase=phase,
            goal=goal,
            current_milestone=current,
            final_milestone=final_milestone,
            constraints=[str(c) for c in constraints],
            status=status,
            evidence=evidence or [],
            notes=notes,
        )
        _upsert_runtime_evidence_artifacts(data, evidence=evidence)
    except ValueError:
        _emit_workspace_event(workspace_root, "goal_alignment_check_noop_invalid_phase", phase=phase)
        return False
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit_workspace_event(workspace_root, "goal_alignment_check_applied", phase=phase, status=status)
    return True


def stop_condition_check(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return normalized ``meta.stop_condition_check`` map."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    check = meta.get(STOP_CONDITION_CHECK_KEY)
    if isinstance(check, dict):
        return check
    check = {}
    meta[STOP_CONDITION_CHECK_KEY] = check
    return check


def evaluate_stop_condition(
    *,
    product_goals_satisfied: bool,
    final_milestone_achieved: bool,
    current_milestone: str,
    final_milestone: str,
) -> bool:
    """
    Completion gate for session closeout.

    Strict rule: completion is allowed only when product goals are satisfied and the
    current milestone equals the final milestone.
    """
    return (
        bool(product_goals_satisfied)
        and bool(final_milestone_achieved)
        and current_milestone.strip() == final_milestone.strip()
    )


def upsert_stop_condition_check(
    manifest: dict[str, Any],
    *,
    product_goals_satisfied: bool,
    final_milestone_achieved: bool,
    current_milestone: str,
    final_milestone: str,
    evidence: list[str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """Write ``meta.stop_condition_check`` and computed ``completion_allowed``."""
    completion_allowed = evaluate_stop_condition(
        product_goals_satisfied=product_goals_satisfied,
        final_milestone_achieved=final_milestone_achieved,
        current_milestone=current_milestone,
        final_milestone=final_milestone,
    )
    entry = {
        "product_goals_satisfied": bool(product_goals_satisfied),
        "final_milestone_achieved": bool(final_milestone_achieved),
        "current_milestone": current_milestone,
        "final_milestone": final_milestone,
        "completion_allowed": completion_allowed,
        "evidence": list(evidence or []),
        "notes": notes,
    }
    check = stop_condition_check(manifest)
    check.clear()
    check.update(entry)
    return check


def persist_stop_condition_check(
    workspace_root: Path,
    *,
    product_goals_satisfied: bool,
    final_milestone_achieved: bool,
    current_milestone: str,
    final_milestone: str,
    evidence: list[str] | None = None,
    notes: str = "",
) -> bool:
    """Persist stop-condition gate state into ``.lvibe/session-manifest.json``."""
    lvibe_dir = workspace_root / ".lvibe"
    path = lvibe_dir / SESSION_MANIFEST_FILENAME
    if not path.is_file():
        _emit_workspace_event(workspace_root, "stop_condition_check_noop_manifest_missing")
        return False
    try:
        data = load_session_manifest(lvibe_dir)
    except (OSError, json.JSONDecodeError):
        _emit_workspace_event(workspace_root, "stop_condition_check_noop_malformed_manifest")
        return False
    if not isinstance(data, dict):
        _emit_workspace_event(workspace_root, "stop_condition_check_noop_invalid_manifest_shape")
        return False
    session_id, repaired, previous_raw = _ensure_manifest_session_id(data)
    if repaired:
        _emit_workspace_event(
            workspace_root,
            "session_id_repaired",
            check="stop_condition",
            previous_session_id=previous_raw,
            repaired_session_id=session_id,
        )
    check = upsert_stop_condition_check(
        data,
        product_goals_satisfied=product_goals_satisfied,
        final_milestone_achieved=final_milestone_achieved,
        current_milestone=current_milestone,
        final_milestone=final_milestone,
        evidence=evidence,
        notes=notes,
    )
    _upsert_runtime_evidence_artifacts(data, evidence=evidence)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit_workspace_event(
        workspace_root,
        "stop_condition_check_applied",
        completion_allowed=bool(check.get("completion_allowed")),
    )
    return True


def release_readiness_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Build deterministic release-readiness status from manifest checks + task states.

    Summary prioritizes shipping readiness from available session evidence:
    - goal alignment end status
    - stop condition gate
    - unresolved task counts
    """
    checks = goal_alignment_checks(manifest)
    end_check = checks.get("end") if isinstance(checks.get("end"), dict) else {}
    end_status = str(end_check.get("status", "unknown"))
    stop_check = stop_condition_check(manifest)
    completion_allowed = bool(stop_check.get("completion_allowed"))
    task_counts = {"pending": 0, "in_progress": 0, "blocked": 0, "done": 0, "other": 0}
    for _, _, task in iter_tasks_in_epic_order(manifest):
        raw = str(task.get("status", "pending")).strip().lower()
        if raw in task_counts:
            task_counts[raw] += 1
        else:
            task_counts["other"] += 1
    total_tasks = sum(task_counts.values())
    dod = milestone_definition_of_done_checks(manifest)
    deps = milestone_dependency_visibility(manifest)
    progress = progress_confidence_report(manifest)
    lock = final_milestone_lock_criteria(manifest)
    ci_summary = ci_evidence_summary(manifest)
    failure_catalog = failure_mode_catalog(manifest)
    blockers = _collect_release_readiness_base_blockers(
        end_status=end_status,
        completion_allowed=completion_allowed,
        task_counts=task_counts,
        dod=dod,
        deps=deps,
        progress=progress,
        lock=lock,
        ci_summary=ci_summary,
    )
    lock_criteria = lock.get("criteria") if isinstance(lock.get("criteria"), dict) else {}
    if (
        bool(lock_criteria.get("goal_alignment_end_evidence_present"))
        and not bool(lock_criteria.get("goal_alignment_end_evidence_traceable"))
    ) or (
        bool(lock_criteria.get("stop_condition_evidence_present"))
        and not bool(lock_criteria.get("stop_condition_evidence_traceable"))
    ):
        blockers.append(RELEASE_READINESS_EVIDENCE_BLOCKER_IDS[0])
    if (
        bool(lock_criteria.get("goal_alignment_end_evidence_present"))
        and not bool(lock_criteria.get("goal_alignment_end_evidence_fresh"))
    ) or (
        bool(lock_criteria.get("stop_condition_evidence_present"))
        and not bool(lock_criteria.get("stop_condition_evidence_fresh"))
    ):
        blockers.append(RELEASE_READINESS_EVIDENCE_BLOCKER_IDS[1])
    return {
        "ready": len(blockers) == 0,
        "goal_alignment_end_status": end_status,
        "completion_allowed": completion_allowed,
        "task_counts": task_counts,
        "total_tasks": total_tasks,
        "milestone_definition_of_done_checks": dod,
        "milestone_dependency_visibility": deps,
        "progress_confidence_report": progress,
        "final_milestone_lock_criteria": lock,
        "ci_evidence_summary": ci_summary,
        "failure_mode_catalog": failure_catalog,
        "blockers": blockers,
    }


def upsert_release_readiness_summary(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.release_readiness_summary`` from current manifest state."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    upsert_milestone_definition_of_done_checks(manifest, source=source)
    upsert_milestone_dependency_visibility(manifest, source=source)
    upsert_progress_confidence_report(manifest, source=source)
    upsert_final_milestone_lock_criteria(manifest, source=source)
    upsert_ci_evidence_summary(manifest, source=source)
    upsert_failure_mode_catalog(manifest, source=source)
    summary = release_readiness_summary(manifest)
    summary["source"] = source
    meta[RELEASE_READINESS_SUMMARY_KEY] = summary
    return summary


def persist_release_readiness_summary(
    workspace_root: Path,
    *,
    source: str = "session_manifest",
) -> bool:
    """Persist generated release-readiness summary into session manifest meta."""
    lvibe_dir = workspace_root / ".lvibe"
    path = lvibe_dir / SESSION_MANIFEST_FILENAME
    if not path.is_file():
        _emit_workspace_event(workspace_root, "release_readiness_noop_manifest_missing")
        return False
    try:
        data = load_session_manifest(lvibe_dir)
    except (OSError, json.JSONDecodeError):
        _emit_workspace_event(workspace_root, "release_readiness_noop_malformed_manifest")
        return False
    if not isinstance(data, dict):
        _emit_workspace_event(workspace_root, "release_readiness_noop_invalid_manifest_shape")
        return False
    summary = upsert_release_readiness_summary(data, source=source)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit_workspace_event(
        workspace_root,
        "release_readiness_applied",
        ready=bool(summary.get("ready")),
        blockers=list(summary.get("blockers") or []),
    )
    return True


def remaining_gaps_report(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Build explicit remaining-gaps report for milestone close readiness.

    Uses release-readiness summary as primary input and expands blockers into a
    compact report with actionable gap ids.
    """
    summary = release_readiness_summary(manifest)
    gaps = list(summary.get("blockers") or [])
    return {
        "has_gaps": len(gaps) > 0,
        "gap_count": len(gaps),
        "gaps": gaps,
        "ready": bool(summary.get("ready")),
        "completion_allowed": bool(summary.get("completion_allowed")),
    }


def upsert_remaining_gaps_report(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.remaining_gaps_report`` derived from current manifest state."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    upsert_milestone_dependency_visibility(manifest, source=source)
    upsert_progress_confidence_report(manifest, source=source)
    upsert_final_milestone_lock_criteria(manifest, source=source)
    upsert_ci_evidence_summary(manifest, source=source)
    upsert_failure_mode_catalog(manifest, source=source)
    report = remaining_gaps_report(manifest)
    report["source"] = source
    meta[REMAINING_GAPS_REPORT_KEY] = report
    return report


def persist_remaining_gaps_report(
    workspace_root: Path,
    *,
    source: str = "session_manifest",
) -> bool:
    """Persist remaining-gaps report into ``.lvibe/session-manifest.json``."""
    lvibe_dir = workspace_root / ".lvibe"
    path = lvibe_dir / SESSION_MANIFEST_FILENAME
    if not path.is_file():
        _emit_workspace_event(workspace_root, "remaining_gaps_noop_manifest_missing")
        return False
    try:
        data = load_session_manifest(lvibe_dir)
    except (OSError, json.JSONDecodeError):
        _emit_workspace_event(workspace_root, "remaining_gaps_noop_malformed_manifest")
        return False
    if not isinstance(data, dict):
        _emit_workspace_event(workspace_root, "remaining_gaps_noop_invalid_manifest_shape")
        return False
    report = upsert_remaining_gaps_report(data, source=source)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit_workspace_event(
        workspace_root,
        "remaining_gaps_applied",
        gap_count=int(report.get("gap_count", 0)),
    )
    return True


def iter_tasks_in_epic_order(
    manifest: dict[str, Any],
) -> Iterator[tuple[str, str, dict[str, Any]]]:
    """
    Yield ``(epic_id, epic_title, task)`` for each task in ``product.epics`` order,
    then task order within each epic.
    """
    product = manifest.get("product") or {}
    epics = product.get("epics") or []
    if not isinstance(epics, list):
        return
    for epic in epics:
        if not isinstance(epic, dict):
            continue
        eid = str(epic.get("id", ""))
        etitle = str(epic.get("title", ""))
        tasks = epic.get("tasks") or []
        if not isinstance(tasks, list):
            continue
        for task in tasks:
            if isinstance(task, dict):
                yield eid, etitle, task


def get_product_milestones(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Return normalized ``product.milestones`` entries.

    Formal milestone schema (Task 61):
    - ``id``
    - ``objective``
    - ``acceptance``
    - ``exit_tests``
    - ``owners``
    """
    product = manifest.get("product")
    if not isinstance(product, dict):
        return []
    raw = product.get("milestones")
    if not isinstance(raw, list):
        return []
    return [m for m in raw if isinstance(m, dict)]


def get_milestone_by_id(manifest: dict[str, Any], milestone_id: str) -> dict[str, Any] | None:
    """Lookup one milestone record by ``id``."""
    for milestone in get_product_milestones(manifest):
        if milestone.get("id") == milestone_id:
            return milestone
    return None


def milestone_definition_of_done_checks(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate per-milestone definition-of-done checks (Task 62).

    A milestone passes when required schema fields are present and non-empty:
    ``objective``, ``acceptance[]``, ``exit_tests[]``, and ``owners[]``.
    """
    milestones = get_product_milestones(manifest)
    checks: list[dict[str, Any]] = []
    for m in milestones:
        objective = str(m.get("objective", "")).strip()
        acceptance = m.get("acceptance")
        exit_tests = m.get("exit_tests")
        owners = m.get("owners")
        acceptance_ok = isinstance(acceptance, list) and len(acceptance) > 0
        exit_tests_ok = isinstance(exit_tests, list) and len(exit_tests) > 0
        owners_ok = isinstance(owners, list) and len(owners) > 0
        objective_ok = len(objective) > 0
        passed = objective_ok and acceptance_ok and exit_tests_ok and owners_ok
        checks.append(
            {
                "id": str(m.get("id", "")),
                "objective_ok": objective_ok,
                "acceptance_ok": acceptance_ok,
                "exit_tests_ok": exit_tests_ok,
                "owners_ok": owners_ok,
                "passed": passed,
            }
        )
    total = len(checks)
    passed_count = sum(1 for c in checks if bool(c.get("passed")))
    return {
        "total": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "all_passed": total > 0 and passed_count == total,
        "checks": checks,
    }


def milestone_dependency_visibility(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Report cross-milestone dependency visibility (Task 63).

    Milestones may declare ``dependencies`` as a list of milestone ids.
    This report surfaces unknown references and reverse dependents.
    """
    milestones = get_product_milestones(manifest)
    ids = {str(m.get("id", "")) for m in milestones if str(m.get("id", "")).strip()}
    dependents: dict[str, list[str]] = {mid: [] for mid in ids}
    entries: list[dict[str, Any]] = []
    missing_count = 0
    for m in milestones:
        mid = str(m.get("id", ""))
        deps_raw = m.get("dependencies")
        deps = [str(d) for d in deps_raw] if isinstance(deps_raw, list) else []
        missing = [d for d in deps if d not in ids]
        for d in deps:
            if d in dependents:
                dependents[d].append(mid)
        if missing:
            missing_count += len(missing)
        entries.append(
            {
                "id": mid,
                "dependencies": deps,
                "missing_dependencies": missing,
            }
        )
    return {
        "total": len(entries),
        "missing_count": missing_count,
        "has_missing": missing_count > 0,
        "entries": entries,
        "dependents": dependents,
    }


def upsert_milestone_dependency_visibility(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.milestone_dependency_visibility`` into manifest meta."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    vis = milestone_dependency_visibility(manifest)
    vis["source"] = source
    meta[MILESTONE_DEPENDENCY_VISIBILITY_KEY] = vis
    return vis


def progress_confidence_report(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Compute progress confidence and drift detection (Task 64).

    Confidence mixes objective completion signals:
    - done task ratio
    - milestone DoD pass ratio
    - stop-condition completion gate
    Drift is flagged when alignment claims progress but task execution lags.
    """
    stop = stop_condition_check(manifest)
    dod = milestone_definition_of_done_checks(manifest)
    checks = goal_alignment_checks(manifest)
    end_check = checks.get("end") if isinstance(checks.get("end"), dict) else {}
    end_status = str(end_check.get("status", "unknown"))

    task_counts = {"pending": 0, "in_progress": 0, "blocked": 0, "done": 0, "other": 0}
    for _, _, task in iter_tasks_in_epic_order(manifest):
        raw = str(task.get("status", "pending")).strip().lower()
        if raw in task_counts:
            task_counts[raw] += 1
        else:
            task_counts["other"] += 1
    total_tasks = sum(task_counts.values())
    done_ratio = (task_counts["done"] / total_tasks) if total_tasks > 0 else 0.0

    dod_total = int(dod.get("total", 0))
    dod_passed = int(dod.get("passed", 0))
    dod_ratio = (dod_passed / dod_total) if dod_total > 0 else 0.0
    stop_ok = bool(stop.get("completion_allowed"))
    stop_score = 1.0 if stop_ok else 0.0

    confidence = (0.5 * done_ratio) + (0.3 * dod_ratio) + (0.2 * stop_score)
    drift_detected = end_status == "aligned" and done_ratio < 0.5

    return {
        "confidence_score": round(confidence, 3),
        "task_done_ratio": round(done_ratio, 3),
        "milestone_dod_pass_ratio": round(dod_ratio, 3),
        "stop_condition_met": stop_ok,
        "drift_detected": drift_detected,
        "drift_reason": (
            "goal_alignment_end_aligned_but_task_progress_low" if drift_detected else ""
        ),
    }


def upsert_progress_confidence_report(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.progress_confidence_report`` from current manifest state."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    report = progress_confidence_report(manifest)
    report["source"] = source
    meta[PROGRESS_CONFIDENCE_REPORT_KEY] = report
    return report


def final_milestone_lock_criteria(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate final-milestone lock criteria requiring complete acceptance evidence (Task 65).
    """
    checks = goal_alignment_checks(manifest)
    end_check = checks.get("end") if isinstance(checks.get("end"), dict) else {}
    end_aligned = str(end_check.get("status", "")).strip().lower() == "aligned"
    end_evidence = end_check.get("evidence")
    end_evidence_ok = isinstance(end_evidence, list) and len(end_evidence) > 0
    end_provenance = evidence_provenance_report(manifest, end_evidence)
    end_evidence_traceable = bool(end_provenance.get("all_traceable"))
    end_evidence_fresh = bool(end_provenance.get("all_fresh"))

    stop = stop_condition_check(manifest)
    stop_ok = bool(stop.get("completion_allowed"))
    stop_evidence = stop.get("evidence")
    stop_evidence_ok = isinstance(stop_evidence, list) and len(stop_evidence) > 0
    stop_provenance = evidence_provenance_report(manifest, stop_evidence)
    stop_evidence_traceable = bool(stop_provenance.get("all_traceable"))
    stop_evidence_fresh = bool(stop_provenance.get("all_fresh"))

    dod = milestone_definition_of_done_checks(manifest)
    dod_ok = bool(dod.get("all_passed"))

    deps = milestone_dependency_visibility(manifest)
    deps_ok = int(deps.get("missing_count", 0)) == 0

    progress = progress_confidence_report(manifest)
    drift_free = not bool(progress.get("drift_detected"))

    locked = all(
        [
            end_aligned,
            end_evidence_ok,
            end_evidence_traceable,
            end_evidence_fresh,
            stop_ok,
            stop_evidence_ok,
            stop_evidence_traceable,
            stop_evidence_fresh,
            dod_ok,
            deps_ok,
            drift_free,
        ]
    )
    return {
        "locked": locked,
        "criteria": {
            "goal_alignment_end_aligned": end_aligned,
            "goal_alignment_end_evidence_present": end_evidence_ok,
            "goal_alignment_end_evidence_traceable": end_evidence_traceable,
            "goal_alignment_end_evidence_fresh": end_evidence_fresh,
            "stop_condition_met": stop_ok,
            "stop_condition_evidence_present": stop_evidence_ok,
            "stop_condition_evidence_traceable": stop_evidence_traceable,
            "stop_condition_evidence_fresh": stop_evidence_fresh,
            "milestone_definition_of_done_passed": dod_ok,
            "milestone_dependencies_resolved": deps_ok,
            "no_progress_drift": drift_free,
        },
        "evidence_provenance": {
            "goal_alignment_end": end_provenance,
            "stop_condition": stop_provenance,
        },
    }


def upsert_final_milestone_lock_criteria(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.final_milestone_lock_criteria`` into manifest meta."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    lock = final_milestone_lock_criteria(manifest)
    lock["source"] = source
    meta[FINAL_MILESTONE_LOCK_CRITERIA_KEY] = lock
    return lock


def evidence_artifact_registry(manifest: dict[str, Any]) -> list[str]:
    """Return normalized ``meta.evidence_artifacts`` identifiers."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        return []
    raw = meta.get(EVIDENCE_ARTIFACTS_KEY)
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for entry in raw:
        artifact = str(entry).strip()
        if artifact and artifact not in seen:
            seen.add(artifact)
            out.append(artifact)
    return out


def evidence_artifact_session_map(manifest: dict[str, Any]) -> dict[str, str]:
    """
    Return ``artifact_id -> session_id`` map from ``meta.evidence_artifact_records``.
    """
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        return {}
    raw = meta.get("evidence_artifact_records")
    if not isinstance(raw, list):
        return {}
    out: dict[str, str] = {}
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        artifact_id = str(entry.get("id", "")).strip()
        session_id = str(entry.get("session_id", "")).strip()
        if artifact_id and session_id:
            out[artifact_id] = session_id
    return out


def evidence_provenance_report(manifest: dict[str, Any], evidence: Any) -> dict[str, Any]:
    """
    Validate that each evidence entry maps to a registered artifact id.
    """
    registry = set(evidence_artifact_registry(manifest))
    current_session_id = ""
    meta = manifest.get("meta")
    if isinstance(meta, dict):
        current_session_id = str(meta.get("session_id", "")).strip()
    artifact_sessions = evidence_artifact_session_map(manifest)
    evidence_items = [str(item).strip() for item in evidence] if isinstance(evidence, list) else []
    traceable = [item for item in evidence_items if item and item in registry]
    untraceable = [item for item in evidence_items if item and item not in registry]
    fresh = [
        item
        for item in traceable
        if current_session_id and artifact_sessions.get(item, current_session_id) == current_session_id
    ]
    stale = [item for item in traceable if item not in fresh]
    return {
        "registry_count": len(registry),
        "provided_count": len(evidence_items),
        "traceable_count": len(traceable),
        "untraceable_count": len(untraceable),
        "fresh_count": len(fresh),
        "stale_count": len(stale),
        "current_session_id": current_session_id,
        "traceable": traceable,
        "untraceable": untraceable,
        "fresh": fresh,
        "stale": stale,
        "all_traceable": len(evidence_items) > 0 and len(untraceable) == 0,
        "all_fresh": len(evidence_items) > 0 and len(untraceable) == 0 and len(stale) == 0,
    }


def parse_ci_failure_evidence(log_text: Any) -> dict[str, Any]:
    """
    Parse CI log text into deterministic failure evidence records (Task 59).
    """
    text = str(log_text or "")
    if not text.strip():
        return {
            "has_failures": False,
            "failure_count": 0,
            "error_count": 0,
            "reported_failed_count": 0,
            "reported_error_count": 0,
            "failures": [],
        }

    failures: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        failed_match = re.match(r"^FAILED\s+(\S+)\s+-\s+(.+)$", line)
        if failed_match:
            failures.append(
                {
                    "kind": "failed",
                    "node_id": failed_match.group(1),
                    "detail": failed_match.group(2).strip(),
                }
            )
            continue
        error_match = re.match(r"^ERROR\s+(\S+)\s+-\s+(.+)$", line)
        if error_match:
            failures.append(
                {
                    "kind": "error",
                    "node_id": error_match.group(1),
                    "detail": error_match.group(2).strip(),
                }
            )

    # Pytest summary usually includes "... 2 failed, 1 error ..."; keep this when available.
    reported_failed_matches = re.findall(r"\b(\d+)\s+failed\b", text)
    reported_error_matches = re.findall(r"\b(\d+)\s+error(?:s)?\b", text)
    reported_failed_count = int(reported_failed_matches[-1]) if reported_failed_matches else 0
    reported_error_count = int(reported_error_matches[-1]) if reported_error_matches else 0

    failed_count = sum(1 for item in failures if item.get("kind") == "failed")
    error_count = sum(1 for item in failures if item.get("kind") == "error")

    return {
        "has_failures": (failed_count + error_count) > 0 or (reported_failed_count + reported_error_count) > 0,
        "failure_count": failed_count,
        "error_count": error_count,
        "reported_failed_count": reported_failed_count,
        "reported_error_count": reported_error_count,
        "failures": failures,
    }


def ci_evidence_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Aggregate CI-failure evidence from manifest meta for release gating (Task 59).
    """
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        return {
            "sources": 0,
            "has_failures": False,
            "failure_count": 0,
            "error_count": 0,
            "reported_failed_count": 0,
            "reported_error_count": 0,
            "failures": [],
        }
    raw_logs: list[str] = []
    single = meta.get("ci_failure_log")
    if isinstance(single, str) and single.strip():
        raw_logs.append(single)
    multi = meta.get("ci_failure_logs")
    if isinstance(multi, list):
        raw_logs.extend(str(item) for item in multi if str(item).strip())

    failures: list[dict[str, str]] = []
    failure_count = 0
    error_count = 0
    reported_failed_count = 0
    reported_error_count = 0
    for log in raw_logs:
        parsed = parse_ci_failure_evidence(log)
        failures.extend([entry for entry in parsed.get("failures", []) if isinstance(entry, dict)])
        failure_count += int(parsed.get("failure_count", 0))
        error_count += int(parsed.get("error_count", 0))
        reported_failed_count += int(parsed.get("reported_failed_count", 0))
        reported_error_count += int(parsed.get("reported_error_count", 0))
    return {
        "sources": len(raw_logs),
        "has_failures": (failure_count + error_count) > 0 or (reported_failed_count + reported_error_count) > 0,
        "failure_count": failure_count,
        "error_count": error_count,
        "reported_failed_count": reported_failed_count,
        "reported_error_count": reported_error_count,
        "failures": failures,
    }


def upsert_ci_evidence_summary(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.ci_evidence_summary`` into manifest meta."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    summary = ci_evidence_summary(manifest)
    summary["source"] = source
    meta[CI_EVIDENCE_SUMMARY_KEY] = summary
    return summary


def failure_mode_catalog(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Build a catalog of active failure modes from current blockers (Task 58).
    """
    blockers = list(release_readiness_summary_without_catalog(manifest).get("blockers") or [])
    modes: list[dict[str, Any]] = []
    for blocker in blockers:
        severity = FAILURE_MODE_SEVERITY_BY_BLOCKER.get(blocker, "medium")
        modes.append(
            {
                "id": blocker,
                "severity": severity,
                "status": "active",
            }
        )
    return {
        "total": len(modes),
        "active": len(modes),
        "modes": modes,
    }


def release_readiness_summary_without_catalog(manifest: dict[str, Any]) -> dict[str, Any]:
    """
    Internal helper: release readiness summary fields excluding failure catalog.
    """
    checks = goal_alignment_checks(manifest)
    end_check = checks.get("end") if isinstance(checks.get("end"), dict) else {}
    end_status = str(end_check.get("status", "unknown"))
    stop_check = stop_condition_check(manifest)
    completion_allowed = bool(stop_check.get("completion_allowed"))
    task_counts = {"pending": 0, "in_progress": 0, "blocked": 0, "done": 0, "other": 0}
    for _, _, task in iter_tasks_in_epic_order(manifest):
        raw = str(task.get("status", "pending")).strip().lower()
        if raw in task_counts:
            task_counts[raw] += 1
        else:
            task_counts["other"] += 1
    total_tasks = sum(task_counts.values())
    dod = milestone_definition_of_done_checks(manifest)
    deps = milestone_dependency_visibility(manifest)
    progress = progress_confidence_report(manifest)
    lock = final_milestone_lock_criteria(manifest)
    ci_summary = ci_evidence_summary(manifest)
    blockers = _collect_release_readiness_base_blockers(
        end_status=end_status,
        completion_allowed=completion_allowed,
        task_counts=task_counts,
        dod=dod,
        deps=deps,
        progress=progress,
        lock=lock,
        ci_summary=ci_summary,
    )
    return {
        "ready": len(blockers) == 0,
        "goal_alignment_end_status": end_status,
        "completion_allowed": completion_allowed,
        "task_counts": task_counts,
        "total_tasks": total_tasks,
        "milestone_definition_of_done_checks": dod,
        "milestone_dependency_visibility": deps,
        "progress_confidence_report": progress,
        "ci_evidence_summary": ci_summary,
        "final_milestone_lock_criteria": lock,
        "blockers": blockers,
    }


def _collect_release_readiness_base_blockers(
    *,
    end_status: str,
    completion_allowed: bool,
    task_counts: dict[str, int],
    dod: dict[str, Any],
    deps: dict[str, Any],
    progress: dict[str, Any],
    lock: dict[str, Any],
    ci_summary: dict[str, Any],
) -> list[str]:
    """Return base release-readiness blocker ids from one shared rule set."""
    blockers: list[str] = []
    if end_status != "aligned":
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[0])
    if not completion_allowed:
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[1])
    if task_counts["blocked"] > 0:
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[2])
    if task_counts["pending"] > 0 or task_counts["in_progress"] > 0:
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[3])
    if not bool(dod.get("all_passed", False)):
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[4])
    if int(deps.get("missing_count", 0)) > 0:
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[5])
    if bool(progress.get("drift_detected")):
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[6])
    if bool(ci_summary.get("has_failures")):
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[7])
    if not bool(lock.get("locked", False)):
        blockers.append(RELEASE_READINESS_BASE_BLOCKER_IDS[8])
    return blockers


def upsert_failure_mode_catalog(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.failure_mode_catalog`` into manifest meta."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    catalog = failure_mode_catalog(manifest)
    catalog["source"] = source
    meta[FAILURE_MODE_CATALOG_KEY] = catalog
    return catalog


def upsert_milestone_definition_of_done_checks(
    manifest: dict[str, Any],
    *,
    source: str = "session_manifest",
) -> dict[str, Any]:
    """Write ``meta.milestone_definition_of_done_checks`` into manifest meta."""
    meta = manifest.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        manifest["meta"] = meta
    checks = milestone_definition_of_done_checks(manifest)
    checks["source"] = source
    meta[MILESTONE_DOD_CHECKS_KEY] = checks
    return checks


def workspace_has_meaningful_files(workspace_root: Path) -> bool:
    """True if the workspace has any entry besides ``.lvibe`` (opening / skip heuristic)."""
    try:
        for child in workspace_root.iterdir():
            if child.name == ".lvibe":
                continue
            return True
    except OSError:
        return False
    return False


def resolve_next_step_after_opening_skip(
    manifest: dict[str, Any],
    workspace_root: Path,
) -> str:
    """
    After the user skips ``opening_intent``, return the next ``session_steps`` id
    per ``on_skip`` and workspace contents (``SESSION_ORCHESTRATION_SPEC`` §4).
    """
    opening = get_step_by_id(manifest, OPENING_INTENT_ID) or {}
    on_skip = str(opening.get("on_skip", "")).lower()
    nonempty = workspace_has_meaningful_files(workspace_root)
    if "workspace_scan" in on_skip and nonempty:
        return "workspace_scan"
    return "agent_bootstrap"


def write_workspace_scan_stub(lvibe_dir: Path, workspace_root: Path) -> Path | None:
    """
    Minimal workspace_scan artifact: small markdown under ``memory/`` (idempotent if file exists).
    """
    out = lvibe_dir / "memory" / "workspace-scan.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        return None
    text = (
        "# Workspace scan (stub)\n\n"
        f"Workspace root: `{workspace_root}`\n\n"
        "_Token-efficient hook: replace with stack signals and key paths per "
        "`docs/SESSION_ORCHESTRATION_SPEC.md`._\n"
    )
    out.write_text(text, encoding="utf-8")
    return out


def apply_opening_skip(
    workspace_root: Path,
    *,
    skipped_opening: bool,
) -> str | None:
    """
    If ``skipped_opening`` and ``meta.current_step_id`` is ``opening_intent``,
    advance ``meta.current_step_id``, optionally write the workspace_scan stub,
    and persist the manifest. Returns the new step id, or ``None`` if no change.
    """
    if not skipped_opening:
        return None
    lvibe_dir = workspace_root / ".lvibe"
    path = lvibe_dir / SESSION_MANIFEST_FILENAME
    if not path.is_file():
        _emit_workspace_event(workspace_root, "opening_skip_noop_manifest_missing")
        return None
    try:
        data = load_session_manifest(lvibe_dir)
    except (OSError, json.JSONDecodeError):
        _emit_workspace_event(workspace_root, "opening_skip_noop_malformed_manifest")
        return None
    if not isinstance(data, dict):
        _emit_workspace_event(workspace_root, "opening_skip_noop_invalid_manifest_shape")
        return None
    meta = data.get("meta")
    invalid_meta_shape = not isinstance(meta, dict)
    if not isinstance(meta, dict):
        meta = {}
        data["meta"] = meta
    if meta.get("current_step_id") != OPENING_INTENT_ID:
        if invalid_meta_shape:
            _emit_workspace_event(workspace_root, "opening_skip_noop_invalid_meta_shape")
        return None
    nxt = resolve_next_step_after_opening_skip(data, workspace_root)
    meta["current_step_id"] = nxt
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit_workspace_event(workspace_root, "opening_skip_applied", from_step=OPENING_INTENT_ID, to_step=nxt)
    if nxt == "workspace_scan":
        write_workspace_scan_stub(lvibe_dir, workspace_root)
    return nxt


def ensure_pm_session_artifacts(workspace_root: Path) -> None:
    """Seed ``session-manifest.json`` and sync agent skills; called during workspace prepare."""
    lvibe_dir = workspace_root / ".lvibe"
    lvibe_dir.mkdir(parents=True, exist_ok=True)
    seed_session_manifest_if_missing(lvibe_dir)
    sync_agent_skills_from_templates(lvibe_dir)
