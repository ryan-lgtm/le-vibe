# Agent mode orchestration — one prompt, three hats, manuscript-grounded

**Purpose:** Define how a **single** paste-ready prompt (see [`MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md)) routes **senior engineering**, **product**, and **project** work without splitting into unrelated one-offs. **Your goals and directives** (optional **`OWNER_DIRECTIVES:`** prefix in chat) steer **PRODUCT** and **PROJECT** behavior; **ENGINEER** implements against [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md), the Master queue in [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md), and [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md).

**Authority:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §7.2 (**`USER RESPONSE REQUIRED`**) — the **only** “hard stop” where the agent **must not** continue implementation or prioritization without you: when **guardrails end** (missing product fact, unresolved tradeoff not in spec, or you must choose). **Secrets / credentials / required out-of-repo access** → **`LÉ VIBE BLOCKED`**. Everything else keeps moving with **`PASTE SAME AGAIN`** when substantive work remains toward your objectives or the in-repo queue.

**Not a hard stop:** Finishing a **subsidiary** checklist (e.g. §4 of [`PM_IDE_SETTINGS_AND_WORKFLOWS.md`](PM_IDE_SETTINGS_AND_WORKFLOWS.md)) does **not** by itself forbid continuation — re-paste the same orchestration prompt; the agent orients to **what is next** under **OWNER_DIRECTIVES** + Master queue + PM tracks.

---

## The three modes (one agent, explicit hat per turn)

| Mode | Hat | Does | Typical manuscript |
|------|-----|------|-------------------|
| **ENGINEER** | Senior engineer | Ships code, tests, packaging; advances **first incomplete** Master **STEP** in execution order **0 → 1 → 14 → 2–13 → 15–17**; runs **`cd le-vibe && python3 -m pytest tests/`** after Python changes. | [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) (STEP row), [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) |
| **PRODUCT** | Product manager | Prioritizes, sequences, reshapes backlog; outputs **Priorities** + **Engineer brief** with acceptance hints; voice grounded in [`le-vibe/templates/agents/product-manager.md`](../le-vibe/templates/agents/product-manager.md); epic shape in [`schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json). **Steered by `OWNER_DIRECTIVES`** when you provide them. | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md), [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) |
| **PROJECT** | Project / program | Cross-cutting orchestration: which **track** (Master queue vs PM iteration tracks e.g. [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) — maintainer **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** / **Full-product install** + close-out gate **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable close-out output; **`apt_sim_note`** — [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) (*`--json` close-out payload*)) vs default **`ci.yml`** **`le-vibe-deb`** stack-only; [`PM_IDE_SETTINGS_AND_WORKFLOWS.md`](PM_IDE_SETTINGS_AND_WORKFLOWS.md)), milestones, doc alignment, “what we call done this initiative” — **without** replacing PRODUCT prioritization or ENGINEER implementation unless you ask for a doc-only edit. **Steered by `OWNER_DIRECTIVES`.** | [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) (queue + Roadmap H), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md), initiative-specific PM docs |

**`MODE: AUTO`** (default in the paste block): pick **one** hat this turn using **`CONTINUATION:`** — if you ask for prioritization / sequencing / epic order → **PRODUCT**; if you give an engineer-ready brief or “continue shipping” → **ENGINEER**; if you ask which track to run or how initiatives stack → **PROJECT**.

---

## Owner directives (steer PRODUCT and PROJECT)

Optional prefix in the **same** chat as the orchestration prompt:

```
OWNER_DIRECTIVES:
- <goal 1>
- <goal 2>
- <non-goals or constraints>
```

If **`OWNER_DIRECTIVES`** is absent, **PRODUCT** / **PROJECT** still align to **PRODUCT_SPEC** + Master queue + open PM tracks — they do not invent conflicting product intent.

---

## Manuscript index (lean retrieval — cite path + §, do not dump whole files)

| Manuscript | Use |
|------------|-----|
| [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) | Must-ship, §7.2 / §7.3, §8 |
| [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) | Master **ORDERED WORK QUEUE** (STEPS **0–17**) |
| [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) | **STEP →** primary PM doc |
| [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) | Manifests, orchestration |
| [`schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json) | JSON shape for PM epics/tasks |
| [`schemas/session-manifest.step14-closeout.v1.example.json`](../schemas/session-manifest.step14-closeout.v1.example.json) + [`STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md`](STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md) | **STEP 14 / §7.3** — pre-filled epics + **`OWNER_DIRECTIVES`** / ENGINEER paste blocks (no owner-per-turn orchestration) |
| [`schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json) | IDE / stack user-settings (PM IDE track) |
| PM iteration tracks | [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) (**`build-le-vibe-debs.sh --with-ide`**, **Full-product install**, **`verify-step14-closeout.sh --require-stack-deb`** + optional **`--apt-sim`** / **`--json`** (**`apt_sim_note`** — *`--json` close-out payload*); **`le-vibe-deb`** = stack-only in default CI; **Partial VSCode-linux** — [`editor/BUILD.md`](../editor/BUILD.md) (*Partial tree*), *Partial VSCode-linux tree* in same doc, **`./editor/print-built-codium-path.sh`**, **`./editor/print-vsbuild-codium-path.sh`**, **`./packaging/scripts/build-le-vibe-ide-deb.sh --help`**), [`PM_IDE_SETTINGS_AND_WORKFLOWS.md`](PM_IDE_SETTINGS_AND_WORKFLOWS.md) |

---

## Continuation vs stop (end-of-message lines)

| Line | Meaning |
|------|---------|
| **`PASTE SAME AGAIN`** | Substantive work this turn **and** more work remains toward **OWNER_DIRECTIVES** + in-repo obligations (queue, tests, deb when touched), **or** a clear handoff follow-up. |
| **`LÉ VIBE SESSION COMPLETE`** | You and the agent agree the **current initiative scope** + applicable queue obligations are satisfied; tests green. |
| **`LÉ VIBE BLOCKED`** | Secrets / credentials / required out-of-repo only. |
| **`USER RESPONSE REQUIRED`** | **Cannot** continue without you — guardrails end; §7.2 numbered questions. |

**Never** use **`PASTE SAME AGAIN`** for plans-only, questions-only, or idle status (same as [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) Master orchestrator).

---

## Single paste entrypoint

**Print stdout:** `python3 packaging/scripts/print-master-iteration-loop-prompt.py` — body lives in [`MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md) (fenced block). Same block for every turn; vary **`MODE:`**, **`OWNER_DIRECTIVES:`**, and **`CONTINUATION:`** only.

**Template pointer:** [`le-vibe/templates/master-iteration-loop.md`](../le-vibe/templates/master-iteration-loop.md).

---

*This document **coordinates** lazy prompts; it does not replace [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) must-ship until engineering merges evidence.*
