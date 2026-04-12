# /setup-workspace — Lé Vibe project context (chat workflow)

**Purpose:** Seed **breadth** for the orchestrator and agents before deep work. The user (or assistant) walks through these prompts in **Continue chat**. Answers should be summarized into **`.lvibe/memory/incremental.md`** and, when ready, **`session-manifest.json`** (`meta.workspace_summary`, `product.epics` drafts).

**When finished:** create an empty marker file **`.lvibe/.workspace-context-seeded`** (e.g. `touch .lvibe/.workspace-context-seeded`) so assistants stop appending the “context not seeded” notice (see **`.continue/rules/`** memory rule).

---

## Prompts (in order)

1. **Project elevator pitch**  
   *Describe this project in 1–2 sentences. What are you building and for whom?*

2. **Repository & agents**  
   *If this workspace is a git repository: do you want agents to **commit** changes here? (You remain responsible for **remote** setup, credentials, and review.)*

3. **Autonomy dial**  
   *On a scale of 1–10 (10 = highest), how comfortable are you leaving agents to execute multi-step work without asking at every micro-step?*

4. **Risk & constraints**  
   *What must not break (APIs, on-disk formats, compliance)? Any deadlines?*

5. **Docs & authority**  
   *Which manuscripts are canonical for this repo (e.g. `docs/PRODUCT_SPEC.md`, internal ADRs)? Where should agents look first?*

6. **Orchestrator direction**  
   *What is the **one** outcome you want from the next construction slice (e.g. “MVP CLI + tests”, “document public API”)?*

---

## Optional slash-style commands (same chat)

Users may type these literally; assistants treat them as **structured intents**:

| User text | Intent |
|-----------|--------|
| `/setup-workspace` | Run this workflow; capture answers in `.lvibe/`. |
| `/agent product_manager` | Prefer **product_manager** lens for the next turn (see **`.lvibe/agents/`** roles). |
| `/agent senior_backend_engineer` | Prefer backend engineering lens. |

**Mentions:** `@product_manager`, `@senior_qa_engineer`, etc. — route questions to the matching **`.lvibe/agents/<id>/skill.md`** role when clarifying.

---

## Handoff

After answers exist in `.lvibe/` and **`session-manifest.json`** reflects epics/tasks, continue with **“Please continue”** per **`docs/AI_PILOT_AND_CONTINUE.md`**.
