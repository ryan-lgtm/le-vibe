# PM — IDE settings surface & workspace workflows (next phase)

**Role:** Senior product manager scope for **in-IDE** configuration (Cursor-like), **global user settings**, **`/setup-workspace`** onboarding, and **agent mention** affordances. **Engineering** implements in **`editor/`** (Code OSS / VSCodium shell), **`le-vibe/`** (launcher, policy, Continue rules), and **`schemas/`**.

**Authority:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5 (storage), §7 (orchestration), [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md), [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md) (ENGINEER / PRODUCT / PROJECT, **`OWNER_DIRECTIVES`**, continuation vs **`USER RESPONSE REQUIRED`** / **`LÉ VIBE BLOCKED`**).

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

- [x] **Settings UI** (IDE): `contributes.configuration` (or equivalent) for cap default, model override, toggles — persisted to **`user-settings.json`** or merged with existing **`~/.config/le-vibe/`** files. **Shipped:** [`editor/le-vibe-settings-extension`](../editor/le-vibe-settings-extension/) (install unpacked **Extensions → Install from Location…** until bundled in the IDE build).  
- [x] **Launcher** reads **`user_settings.load_user_settings()`** where appropriate; does not bypass **§5** consent prompts. **Shipped:** launcher logs `user_settings_loaded`; **`workspace_policy.get_cap_mb`** merges **`lvibe_cap_mb_default`** from **`user-settings.json`** after per-workspace policy cap, before global policy default — consent flow unchanged (**`workspace_consent.resolve_lvibe_creation`**).  
- [x] **Ollama**: override path respects **managed port** and **`locked-model.json`** policy; document disk check before pull. **Shipped:** ``ollama pull`` sets **``OLLAMA_HOST=<host>:<port>``** to match the launcher / ``ensure_managed_ollama``; HTTP **``/api/tags``** on that port decides skip-pull vs download; **≥ ~12 GiB** free on the config-dir volume (else refuse pull when the model is absent); **``model.allow_pull_if_disk_ok: false``** blocks download unless the tag already exists on the managed API; **``locked-model.json``** **``policy``** is **``hardware_tier_best_fit``** | **``user_settings``** (first-run override from user-settings) | **``cli_override``** (``bootstrap --model``). First-run reads **``user-settings.json``** into ``EnsureBootstrapArgs``.  
- [x] **Help panel**: static copy from PM table + link to **`setup-workspace.md`**. **Shipped:** VS Code command **`Lé Vibe: Chat Commands & Mentions Help`** (**`leVibe.showChatCommandsHelp`**) in [`editor/le-vibe-settings-extension`](../editor/le-vibe-settings-extension/) opens a webview with **`help-chat-commands.md`** + button to open **`.lvibe/workflows/setup-workspace.md`** when present; gated by **`leVibe.ide.showChatCommandsHelp`**. **`ide.help_show_command_id`** in [`schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json) documents the command id.  
- [x] **Tests**: extend **`le-vibe/tests/`** for settings merge + E1 strings if user-visible copy shifts. **Shipped:** **`tests/test_pm_ide_settings_workflows_contract.py`** (Continue **`_lvibe_continue_rule_body`** anchors vs **`.workspace-context-seeded`** / **`setup-workspace`**, **`load_user_settings`** deep merge, defaults ⊆ schema example); **`meta.contract_tests`** in [`schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json); **`le-vibe/README.md`** lists the module next to the PM IDE row; **`test_le_vibe_readme_e1_contract.py`** locks the README line.

---

## 5. Lazy repeat — PM / engineer handoff (paste)

Use when iterating **IDE settings** + **workflows** (not the Master queue 0–17 unless merged). **Single-chat** routing across hats and **`OWNER_DIRECTIVES`** — [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md) + paste entrypoint [`MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md).

**Continuation vs stop:** **`PASTE SAME AGAIN`** stays valid while substantive work remains toward **your directives**, the Master queue, another PM track, or tests/docs follow-up. **§4 every row checked** does **not** by itself require **`PM IDE SETTINGS COMPLETE`** — that line is only when you agree this **IDE-settings initiative slice** is done *and* nothing else in scope demands another turn. **Hard stops** where the agent **must not** continue without you: **`USER RESPONSE REQUIRED`** / **§7.2** (guardrails end) and **`LÉ VIBE BLOCKED`** (secrets / out-of-repo only) — same table as [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md) *Continuation vs stop*.

```
MODE: ENGINEER — PM track: IDE settings & workflows (docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md).

Implement the next unchecked row in §4 Engineer brief (if any); otherwise orient to the next obligation under OWNER_DIRECTIVES + Master queue + open PM tracks; ground schema in schemas/user-settings.v1.example.json; keep Continue rules aligned with .lvibe/.workspace-context-seeded footer; run cd le-vibe && python3 -m pytest tests/.

End one line: PASTE SAME AGAIN | PM IDE SETTINGS COMPLETE
```

---

*This document is **product scope** for a **phase** of work; it does not replace [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) must-ship until engineering merges and E1 evidence is updated.*
