# PM — IDE settings surface & workspace workflows (next phase)

**Role:** Senior product manager scope for **in-IDE** configuration (Cursor-like), **global user settings**, **`/setup-workspace`** onboarding, and **agent mention** affordances. **Engineering** implements in **`editor/`** (Code OSS / VSCodium shell), **`le-vibe/`** (launcher, policy, Continue rules), and **`schemas/`**.

**Authority:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5 (storage), §7 (orchestration), [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md).

---

## 1. Product goal

Deliver a **discoverable settings area** (IDE + stack) where users can:

| Setting | Behavior |
|---------|----------|
| **`.lvibe/` size cap** | Same numeric range as first-run workspace consent (**10–500 MB**, default **50 MB**). Global default may live in **`~/.config/le-vibe/user-settings.json`**; per-workspace overrides remain in **`workspace-policy.json`** when the user changes cap at consent time. |
| **Model** | **Recommended** (hardware-tier lock in **`locked-model.json`**) vs **override tag** (e.g. `mistral:latest`). Optional **pull if disk OK** — surface honest disk checks before pulling a larger model. |
| **New workspace defaults** | Toggle hints for first open (welcome, workflow pointers). |
| **Help — mentions & commands** | In-settings help listing **`/setup-workspace`**, **`/agent <role_id>`**, and **`@<role>`** patterns mapped to **`.lvibe/agents/<id>/skill.md`**. |

**Schema (example):** [`schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json)  
**Loader (stack):** [`le-vibe/le_vibe/user_settings.py`](../le-vibe/le_vibe/user_settings.py) — merge with workspace policy in future IDE milestones.

---

## 2. `/setup-workspace` narrative (chat workflow)

**Template:** [`le-vibe/templates/workflows/setup-workspace.md`](../le-vibe/templates/workflows/setup-workspace.md) → copied to **`.lvibe/workflows/setup-workspace.md`** on workspace prepare.

**Story arc (questions):**

1. **Elevator pitch** — 1–2 sentences: what we are building and for whom.  
2. **Git & commits** — if `git` present: may agents commit? (User owns remotes and credentials.)  
3. **Autonomy dial** — 1–10 openness to multi-step agent execution.  
4. **Constraints** — must-not-break surfaces, compliance, deadlines.  
5. **Canonical docs** — which manuscripts are authoritative for this repo.  
6. **Next slice** — single orchestrator outcome for the construction pass.

**Completion marker:** empty file **`.lvibe/.workspace-context-seeded`**. Until present, Continue rules ask assistants to append a **short footer** (see **`.continue/rules/`** memory rule).

---

## 3. Unseeded workspace notice (agents)

If **`.lvibe/`** exists but **`.lvibe/.workspace-context-seeded`** does **not**, every assistant reply ends with a **single** Lé Vibe notice pointing to **`/setup-workspace`** and the workflow file — implemented in **`le_vibe.continue_workspace`** (Continue workspace rules).

---

## 4. Engineer brief (acceptance)

- [ ] **Settings UI** (IDE): `contributes.configuration` (or equivalent) for cap default, model override, toggles — persisted to **`user-settings.json`** or merged with existing **`~/.config/le-vibe/`** files.  
- [ ] **Launcher** reads **`user_settings.load_user_settings()`** where appropriate; does not bypass **§5** consent prompts.  
- [ ] **Ollama**: override path respects **managed port** and **`locked-model.json`** policy; document disk check before pull.  
- [ ] **Help panel**: static copy from PM table + link to **`setup-workspace.md`**.  
- [ ] **Tests**: extend **`le-vibe/tests/`** for settings merge + E1 strings if user-visible copy shifts.

---

## 5. Lazy repeat — PM / engineer handoff (paste)

Use when iterating **IDE settings** + **workflows** (not the Master queue 0–17 unless merged).

```
MODE: ENGINEER — PM track: IDE settings & workflows (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md).

Implement the next unchecked row in §4 Engineer brief; ground schema in schemas/user-settings.v1.example.json; keep Continue rules aligned with .lvibe/.workspace-context-seeded footer; run cd le-vibe && python3 -m pytest tests/.

End one line: PASTE SAME AGAIN | PM IDE SETTINGS COMPLETE
```

---

*This document is **product scope** for a **phase** of work; it does not replace [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) must-ship until engineering merges and E1 evidence is updated.*
