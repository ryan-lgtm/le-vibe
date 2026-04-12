"""Workspace-level Continue integration: `.continue/rules` so the agent treats `.lvibe/` as primary memory."""

from __future__ import annotations

from pathlib import Path

# Lexicographic first so Lé Vibe baseline loads before project-specific numbered rules.
LVIBE_CONTINUE_RULE_NAME = "00-le-vibe-lvibe-memory.md"
# PRODUCT_SPEC §4 — in-editor assistant context (paired with `.lvibe/WELCOME.md`).
PRODUCT_WELCOME_RULE_NAME = "01-le-vibe-product-welcome.md"


def _lvibe_continue_rule_body() -> str:
    return (
        "---\n"
        "name: Lé Vibe — workspace memory (.lvibe/)\n"
        "alwaysApply: true\n"
        "---\n\n"
        "This workspace uses **Lé Vibe**. Treat **`.lvibe/`** at the project root as the **primary memory "
        "and RAG layer** (not ad-hoc full-repo dumps):\n\n"
        "- **`.lvibe/session-manifest.json`** — `session_steps`, **`product.epics`** / tasks; iterate backlog per "
        "`docs/SESSION_ORCHESTRATION_SPEC.md` (in the Lé Vibe product repo). Canonical shape: "
        "**`schemas/session-manifest.v1.example.json`** (seeding prefers that file in a clone via "
        "**`session_manifest_example_source_path`** — see **`le_vibe.session_orchestrator`**).\n"
        "**Doc-first staging (§7.1):** Before large or cross-cutting edits, align with "
        "`docs/PRODUCT_SPEC.md` → `docs/SESSION_ORCHESTRATION_SPEC.md` → `docs/AI_PILOT_AND_CONTINUE.md` → "
        "`docs/PM_STAGE_MAP.md` (orchestrator STEP → primary PM doc), then the Master queue in "
        "`docs/PROMPT_BUILD_LE_VIBE.md`—**not** ad-hoc repo-wide churn. "
        "**“Please continue”** means resume from this manifest + **`.lvibe/`**; **AI Pilot** means sustained "
        "coordination with the same **§5** consent/storage and **§8** secrets rules.\n"
        "- **`.lvibe/agents/<agent_id>/skill.md`** — per-role skill markdown (PM, DevOps, engineering, etc.); "
        "templates ship in the Lé Vibe repo as **`le-vibe/templates/agents/*.md`**. Missing files are copied on "
        "workspace prepare; to pull new template text after upgrading Lé Vibe, run **`packaging/scripts/sync-lvibe-agent-skills.sh`** "
        "from the project root (or delete specific **`skill.md`** files you want replaced, then re-run).\n"
        "- **`memory/`** — incremental, **token-efficient** snippets; **`rag/refs/`** and **`chunks/`** — small references, not monolithic files.\n"
        "- **`AGENTS.md`** — project agent conventions for this repo.\n\n"
        "When recalling context, **prefer reading short files under `.lvibe/`** over rescanning the entire tree.\n\n"
        "**User gate (PRODUCT_SPEC §7.2):** Do **not** silently ship **major** design, **breaking** API/schema moves, or pick a winner when **subagent roles disagree** materially. "
        "**Halt** that branch and print exactly **`USER RESPONSE REQUIRED`** on its own line (all capitals), then **numbered questions** with short context; accept **No preference**, **I don’t care**, **Your call**, or **Surprise me** as delegation to documented defaults—not permission to invent user intent. "
        "Use **blocked** / wait states only for **secrets**, **credentials**, or **out-of-repo** dependencies—not for normal product tradeoffs.\n\n"
        "**Secrets (PRODUCT_SPEC §8):** Default **deny** on **`.env`**, **`.env.local`**, **`.env.*`**, and common secret files—do **not** read them unless the **user explicitly** instructs you for a defined purpose. "
        "Never paste secret **values** into **`.lvibe/`**, structured logs, or incremental memory; use **references** only.\n"
    )


def _product_welcome_rule_body() -> str:
    """Matches ``docs/PRODUCT_SPEC.md`` §4 for Continue Chat/Agent (short; full copy in ``.lvibe/WELCOME.md``)."""
    return (
        "---\n"
        "name: Lé Vibe — product welcome (PRODUCT_SPEC §4)\n"
        "alwaysApply: true\n"
        "---\n\n"
        "**Welcome to Lé Vibe.** Lé Vibe is an **open source** and **free** coding environment. "
        "It is a **local-first alternative** to **Cursor** (AI-assisted coding in the same spirit—not feature parity). "
        "**In-editor welcome (must ship §4):** open **`.lvibe/WELCOME.md`** now—Explorer → **`.lvibe`**, or Quick Open (**Ctrl+P** / **Cmd+P**) → **`.lvibe/WELCOME.md`**. "
        "That file is the full §4 paragraph; keep Chat/Agent answers consistent with it.\n"
    )


def ensure_continue_lvibe_rules(workspace_root: Path) -> list[Path]:
    """
    Create Continue workspace rules when missing: memory anchor (§5) and product welcome (§4).
    Returns paths **written this call** (empty if both already existed).
    """
    rules_dir = workspace_root / ".continue" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, body in (
        (LVIBE_CONTINUE_RULE_NAME, _lvibe_continue_rule_body()),
        (PRODUCT_WELCOME_RULE_NAME, _product_welcome_rule_body()),
    ):
        dest = rules_dir / name
        if not dest.exists():
            dest.write_text(body, encoding="utf-8")
            written.append(dest)
    return written


def continue_rules_dir(workspace_root: Path) -> Path:
    return workspace_root / ".continue" / "rules"
