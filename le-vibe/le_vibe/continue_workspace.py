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
        "- **`.lvibe/session-manifest.json`** — `session_steps`, **`product.epics`** / tasks; Python walks tasks in epic order via **`iter_tasks_in_epic_order`** "
        "(`le_vibe.session_orchestrator`). Iterate backlog per **`docs/SESSION_ORCHESTRATION_SPEC.md`** (Lé Vibe product repo). "
        "Canonical shape: **`schemas/session-manifest.v1.example.json`** (seeding prefers that file in a clone via "
        "**`session_manifest_example_source_path`** — see **`le_vibe.session_orchestrator`**).\n"
        "**Doc-first staging (§7.1):** Before large or cross-cutting edits, align with "
        "`docs/PRODUCT_SPEC.md` → `docs/SESSION_ORCHESTRATION_SPEC.md` → `docs/AI_PILOT_AND_CONTINUE.md` → "
        "`docs/PM_STAGE_MAP.md` (orchestrator STEP → primary PM doc), then the Master queue in "
        "`docs/PROMPT_BUILD_LE_VIBE.md`—**not** ad-hoc repo-wide churn. "
        "**“Please continue”** means resume from this manifest + **`.lvibe/`**; **AI Pilot** means sustained "
        "coordination with the same **§5** consent/storage and **§8** secrets rules.\n"
        "- **`.lvibe/agents/<agent_id>/skill.md`** — per-role skill markdown (PM, DevOps, engineering, etc.); "
        "templates ship in the Lé Vibe repo as **`le-vibe/templates/agents/*.md`**. Missing files are copied on "
        "workspace prepare; to pull new template text after upgrading Lé Vibe, run **`lvibe sync-agent-skills`** "
        "(or **`packaging/scripts/sync-lvibe-agent-skills.sh`** from a monorepo clone — same behavior; or delete specific "
        "**`skill.md`** files you want replaced, then re-run).\n"
        "- **`memory/`** — incremental, **token-efficient** snippets; **`rag/refs/`** and **`chunks/`** — small references, not monolithic files.\n"
        "- **`AGENTS.md`** — project agent conventions for this repo.\n\n"
        "When recalling context, **prefer reading short files under `.lvibe/`** over rescanning the entire tree.\n"
        "**Deterministic recall order (token-efficient):**\n"
        "1. `.lvibe/session-manifest.json` (current step + active epic/task)\n"
        "2. `.lvibe/memory/incremental.md` tail and `.lvibe/memory/workspace-scan.md` when present\n"
        "3. `.lvibe/rag/refs/` small refs for path-specific evidence\n"
        "4. `.lvibe/agents/<agent_id>/skill.md` only for the roles needed this turn\n"
        "Avoid broad `.lvibe/**` rescans unless these sources are missing or contradictory.\n\n"
        "**User gate (PRODUCT_SPEC §7.2):** Do **not** silently ship **major** design, **breaking** API/schema moves, or pick a winner when **subagent roles disagree** materially. "
        "**Halt** that branch and print exactly **`USER RESPONSE REQUIRED`** on its own line (all capitals), then **numbered questions** with short context; accept **No preference**, **I don’t care**, **Your call**, or **Surprise me** as delegation to documented defaults—not permission to invent user intent. "
        "Use this canonical output shape when a gate is triggered:\n\n"
        "USER RESPONSE REQUIRED\n"
        "1. <decision question + why it matters>\n"
        "2. <decision question + tradeoff>\n\n"
        "Ask the user to reply by number (`1: ...`, `2: ...`) before resuming.\n\n"
        "Use **blocked** / wait states only for **secrets**, **credentials**, or **out-of-repo** dependencies—not for normal product tradeoffs.\n\n"
        "**Secrets (PRODUCT_SPEC §8):** Default **deny** on **`.env`**, **`.env.local`**, **`.env.*`**, and common secret files—do **not** read them unless the **user explicitly** instructs you for a defined purpose. "
        "Never paste secret **values** into **`.lvibe/`**, structured logs, or incremental memory; use **references** only.\n\n"
        "**Chat commands & mentions:** Users may type **`/setup-workspace`** to walk the onboarding Q&A (see **`.lvibe/workflows/setup-workspace.md`**). "
        "They may use **`/agent <role_id>`** (e.g. **`/agent @prod`**) or mentions like **`@sme`**, **`@props`**, **`@prod`**, **`@be-eng`**, "
        "**`@fe-eng`**, **`@do-eng`**, **`@marketing`**, **`@cs`**, **`@rev`** to steer which "
        "**.lvibe/agents/<id>/skill.md** lens applies for the next clarification—stay within **§5** consent and **§8** secrets.\n\n"
        "**Workspace context seeding:** If **`.lvibe/`** exists but **`.lvibe/.workspace-context-seeded`** does **not**, treat project context as **incomplete**. "
        "Append **at the end** of **every** assistant reply one short **Lé Vibe** notice: that context is not fully seeded, point to **`.lvibe/workflows/setup-workspace.md`**, "
        "and say the user can run **`/setup-workspace`** and run **`touch .lvibe/.workspace-context-seeded`** when finished. "
        "If **`.workspace-context-seeded`** is present or **`.lvibe/`** is absent (declined consent), do **not** append this notice.\n"
    )


def _product_welcome_rule_body() -> str:
    """Matches ``docs/PRODUCT_SPEC.md`` §4 for Continue Chat/Agent (short; full copy in ``.lvibe/WELCOME.md``)."""
    return (
        "---\n"
        "name: Lé Vibe — product welcome (PRODUCT_SPEC §4)\n"
        "alwaysApply: true\n"
        "---\n\n"
        "**Welcome to Lé Vibe.** Lé Vibe is an **open source** and **free** coding environment. "
        "Your primary agent runs on your hardware, and an Operator can coordinate specialist agents around your project memory in **`.lvibe/`**. "
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
