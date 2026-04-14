"""Lé Vibe workspace ``.lvibe/`` hub — layout, gitignore hygiene, storage metering (**PRODUCT_SPEC** §5.1–5.6; **STEP 15** / **docs/PM_STAGE_MAP.md**).

Consent before creation: ``workspace_consent.resolve_lvibe_creation``; caps + policy JSON: ``workspace_policy``.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from .continue_workspace import (
    LVIBE_CONTINUE_RULE_NAME,
    PRODUCT_WELCOME_RULE_NAME,
    ensure_continue_lvibe_rules,
)
from .editor_welcome import ensure_lvibe_welcome_md
from .session_orchestrator import ensure_pm_session_artifacts
from .structured_log import append_structured_log
from .workspace_consent import resolve_lvibe_creation
from .workspace_storage import refresh_storage_metadata

LVIBE_DIR_NAME = ".lvibe"
MANIFEST_VERSION = 1


def ensure_lvibe_workflow_templates(workspace_root: Path) -> list[Path]:
    """Seed ``.lvibe/workflows/setup-workspace.md`` from package templates (idempotent)."""
    wf_dir = workspace_root / LVIBE_DIR_NAME / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent.parent / "templates" / "workflows" / "setup-workspace.md"
    dest = wf_dir / "setup-workspace.md"
    written: list[Path] = []
    if not dest.exists() and src.is_file():
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(dest)
    return written

# Skip typical editor flags so we still resolve workspace paths (e.g. codium -n .).
_EDITOR_FLAG_PREFIXES = ("-",)


def _candidate_roots_from_arg(raw: str) -> list[Path]:
    """Map one CLI token to zero or more directory roots to prepare."""
    if not raw or raw.startswith(_EDITOR_FLAG_PREFIXES):
        return []
    p = Path(raw).expanduser()
    try:
        resolved = p.resolve()
    except (OSError, RuntimeError):
        return []
    if resolved.is_dir():
        return [resolved]
    if resolved.is_file():
        return [resolved.parent]
    return []


def workspace_roots_from_editor_args(editor_args: list[str]) -> list[Path]:
    """
    Paths the launcher should treat as workspace roots for `.lvibe/` (directories,
    or parent directory when a file path is passed).
    Order preserved; duplicates removed.
    """
    seen: set[str] = set()
    out: list[Path] = []
    for raw in editor_args:
        for root in _candidate_roots_from_arg(raw):
            key = str(root)
            if key not in seen:
                seen.add(key)
                out.append(root)
    return out


def _gitignore_already_mentions_lvibe(content: str) -> bool:
    for line in content.splitlines():
        s = line.strip()
        if s == ".lvibe/" or s == ".lvibe" or s == ".lvibe/**":
            return True
        # Allow indented or negated patterns — still "listed"
        if re.match(r"^!?\.lvibe/?$", s):
            return True
    return False


def ensure_gitignore_has_lvibe(workspace_root: Path) -> bool:
    """
    If `.gitignore` exists at workspace_root, append `.lvibe/` once (idempotent).
    Returns True if an append was performed.
    """
    gi = workspace_root / ".gitignore"
    if not gi.is_file():
        return False
    try:
        content = gi.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if _gitignore_already_mentions_lvibe(content):
        return False
    try:
        with gi.open("a", encoding="utf-8") as f:
            if content and not content.endswith("\n"):
                f.write("\n")
            f.write("\n# Lé Vibe workspace hub (local agent memory; keep out of git by default)\n.lvibe/\n")
    except OSError:
        return False
    return True


def ensure_lvibe_workspace(workspace_root: Path) -> Path:
    """
    Create `.lvibe/` when absent with a minimal token-efficient layout:
    manifest, agent rules, bounded incremental memory path, RAG + chunk placeholders.

    **Consent:** product flows should call ``prepare_workspaces_for_editor_args`` (or
    ``resolve_lvibe_creation`` first). This function is used for explicit/tests/API
    callers that already granted consent.
    """
    lvibe = workspace_root / LVIBE_DIR_NAME
    lvibe.mkdir(parents=True, exist_ok=True)

    manifest = lvibe / "manifest.yaml"
    if not manifest.exists():
        manifest.write_text(
            f"# Lé Vibe workspace hub (schema v{MANIFEST_VERSION})\n"
            "version: 1\n"
            "purpose: project-local agent memory and small RAG references — prefer short pulls here over full-file churn.\n",
            encoding="utf-8",
        )

    readme = lvibe / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Lé Vibe hub\n\n"
            "This folder is the **primary project memory layer** for Lé Vibe (PRODUCT_SPEC §5): small manifests, "
            "shared RAG refs, per-agent notes, and incremental memory. Prefer **short, bounded** entries.\n\n"
            "- **`agents/<agent_id>/`** — persona + role context (`skill.md` per template).\n"
            "- **`rag/`** — shared cross-cutting chunk refs (compaction trims here **first**).\n"
            "- **`chunks/`** — legacy/sidecar refs (also trimmed early).\n"
            "- **`memory/`** — incremental snippets.\n\n"
            "**PM session:** `session-manifest.json` holds `session_steps` and `product.epics` / tasks. "
            "See `docs/SESSION_ORCHESTRATION_SPEC.md` in the Lé Vibe repo.\n",
            encoding="utf-8",
        )

    agents = lvibe / "AGENTS.md"
    if not agents.exists():
        agents.write_text(
            "# Agent rules (Lé Vibe)\n\n"
            "- Treat **`.lvibe/`** as the default place for **project memory** and **incremental context**.\n"
            "- **Prefer** recalling from `memory/` and small files here instead of re-reading large caches or whole trees.\n"
            "- **Deterministic recall order:** `session-manifest.json` → `memory/incremental.md` (tail) / `memory/workspace-scan.md` → `rag/refs/` relevant refs → only required `agents/<agent_id>/skill.md` files.\n"
            "- Avoid broad `.lvibe/**` rescans unless the ordered sources are missing or contradictory.\n"
            "- **Append** new facts as **short** bullet or YAML snippets in `memory/incremental.md` (~2 KiB per entry as a "
            "guide; summarize if growing; compaction may trim the tail under storage pressure — PRODUCT_SPEC §5.5).\n"
            "- Optional: place **chunk references** under **`rag/refs/`** (preferred) or legacy `chunks/` for RAG-style lookups.\n"
            "- **User gate (PRODUCT_SPEC §7.2):** If you lack authority for a **high-impact** decision or roles **disagree** materially, stop and surface **`USER RESPONSE REQUIRED`** with **numbered questions** (see **`.continue/rules/`** memory rule)—do not assume.\n"
            "- **Secrets (PRODUCT_SPEC §8):** Do **not** read **`.env`** / **`.env.*`** unless the user **explicitly** approves; "
            "never store secret **values** here—**references** only.\n",
            encoding="utf-8",
        )

    memory_dir = lvibe / "memory"
    memory_dir.mkdir(exist_ok=True)
    incremental = memory_dir / "incremental.md"
    if not incremental.exists():
        incremental.write_text(
            "# Incremental memory (bounded)\n\n"
            "_Append small dated snippets; avoid unbounded paste of full project history._\n"
            "_Keep each new bullet roughly **≤ ~2 KiB**; `lvibe hygiene` warns if this file grows large._\n\n",
            encoding="utf-8",
        )

    rag = lvibe / "rag"
    rag.mkdir(exist_ok=True)
    rag_refs = rag / "refs"
    rag_refs.mkdir(exist_ok=True)
    rag_readme = rag / "README.md"
    if not rag_readme.exists():
        rag_readme.write_text(
            "# Shared RAG (PRODUCT_SPEC §5.2)\n\n"
            "Cross-cutting chunk references and retrieval material **separate** from per-agent narrative. "
            "Place small YAML/Markdown files under **`refs/`**. Compaction removes oldest refs here **before** "
            "touching per-agent `skill.md` files.\n\n"
            "**Minimal ref shape (recommended):** YAML frontmatter in `.md` or keys at the top of `.yaml`:\n"
            "`title`, `path` (repo-relative), `summary`, `updated` (ISO date). "
            "`lvibe hygiene` warns when keys are missing or files are oversized.\n",
            encoding="utf-8",
        )

    chunks = lvibe / "chunks"
    chunks.mkdir(exist_ok=True)
    chunks_readme = chunks / "README.md"
    if not chunks_readme.exists():
        chunks_readme.write_text(
            "# Chunk references (legacy sibling)\n\n"
            "Optional: small sidecar files (e.g. one YAML per topic) pointing to repo paths or hashes — "
            "not monolithic dumps. Prefer new work under **`../rag/refs/`** when possible.\n",
            encoding="utf-8",
        )

    continue_rules = lvibe / "continue-rules.md"
    if not continue_rules.exists():
        continue_rules.write_text(
            "# Continue / editor context (Lé Vibe)\n\n"
            "Continue loads workspace rules from **`.continue/rules/`** (see Continue docs). Lé Vibe seeds "
            f"**`{LVIBE_CONTINUE_RULE_NAME}`** (memory) and **`{PRODUCT_WELCOME_RULE_NAME}`** (PRODUCT_SPEC §4 welcome) "
            "on first workspace open. **`WELCOME.md`** in this folder is the in-editor welcome surface.\n\n"
            "See also `AGENTS.md`.\n",
            encoding="utf-8",
        )

    ensure_pm_session_artifacts(workspace_root)
    ensure_lvibe_welcome_md(workspace_root)
    ensure_lvibe_workflow_templates(workspace_root)
    ensure_continue_lvibe_rules(workspace_root)

    return lvibe


def prepare_workspaces_for_editor_args(editor_args: list[str]) -> list[Path]:
    """
    For each workspace root: consent-gated ``.lvibe/`` (PRODUCT_SPEC §5.1), gitignore hygiene (§6),
    storage metering + compaction (§5.4–5.5). Returns roots where ``.lvibe/`` was prepared.
    """
    roots = workspace_roots_from_editor_args(editor_args)
    prepared: list[Path] = []
    for root in roots:
        ensure_gitignore_has_lvibe(root)
        if not resolve_lvibe_creation(root):
            continue
        ensure_lvibe_workspace(root)
        usage, cap = refresh_storage_metadata(root)
        append_structured_log(
            "workspace",
            "lvibe_storage",
            workspace=str(root.resolve()),
            usage_bytes=usage,
            cap_mb=cap,
        )
        if os.environ.get("LE_VIBE_VERBOSE", "").lower() in ("1", "true", "yes"):
            mb = usage / (1024 * 1024)
            print(
                f"Lé Vibe workspace memory: {mb:.2f} / {cap} MB — see `.lvibe/storage-state.json`",
                file=sys.stderr,
            )
        prepared.append(root)
    return prepared
