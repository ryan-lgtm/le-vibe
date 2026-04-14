"""PM session manifest: seed, skill sync, session_steps, and opening_intent / skip → workspace_scan hooks.

See ``docs/SESSION_ORCHESTRATION_SPEC.md`` and ``schemas/session-manifest.v1.example.json``.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Iterator

SESSION_MANIFEST_FILENAME = "session-manifest.json"
OPENING_INTENT_ID = "opening_intent"


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
        return None
    data = load_session_manifest(lvibe_dir)
    meta = data.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        data["meta"] = meta
    if meta.get("current_step_id") != OPENING_INTENT_ID:
        return None
    nxt = resolve_next_step_after_opening_skip(data, workspace_root)
    meta["current_step_id"] = nxt
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if nxt == "workspace_scan":
        write_workspace_scan_stub(lvibe_dir, workspace_root)
    return nxt


def ensure_pm_session_artifacts(workspace_root: Path) -> None:
    """Seed ``session-manifest.json`` and sync agent skills; called during workspace prepare."""
    lvibe_dir = workspace_root / ".lvibe"
    lvibe_dir.mkdir(parents=True, exist_ok=True)
    seed_session_manifest_if_missing(lvibe_dir)
    sync_agent_skills_from_templates(lvibe_dir)
