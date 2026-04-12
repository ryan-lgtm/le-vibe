# Lé Vibe — session orchestration & PM-driven manifests

This document specifies the **session manifest JSON**, **SESSION STEPS**, **skill agents**, and how the **master orchestrator** uses **RAG-oriented context** so multiple agents coordinate like a modern SaaS product org.

**Cursor / build loop (same routing idea):** [`docs/MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md) — one paste-ready prompt for **ENGINEER** ↔ **PRODUCT_MANAGER** with lean manuscript pointers and **new-agent** chats (`packaging/scripts/print-master-iteration-loop-prompt.py`).

It applies in **two places**:

| Context | Where it lives | Purpose |
|---------|----------------|---------|
| **Building Lé Vibe** (this repo) | `schemas/session-manifest.v1.example.json`, `le-vibe/templates/agents/*.md` | Dogfood the same format while developing the product; CI and docs reference these paths. |
| **User workspace** | `.lvibe/session-manifest.json`, `.lvibe/agents/<agent_id>/skill.md` | Same schema and agent skills; orchestrator and Continue/agent rules read from here. |

**Master orchestrator STEP 2 (PM session):** Seed **`session-manifest.json`** from **`schemas/session-manifest.v1.example.json`** when running from a clone (**`session_manifest_example_source_path`**), else the bundled example (same JSON — must match **`schemas/`**), copy **`le-vibe/templates/agents/*.md`** into **`.lvibe/agents/<agent_id>/skill.md`**, expose **`session_steps`** / **`product.epics`** iteration, and implement **`opening_intent` → skip → `workspace_scan`** via **`apply_opening_skip`** — **`le_vibe.session_orchestrator`** (**`ensure_pm_session_artifacts`** from workspace prepare). E1: **`le-vibe/tests/test_session_orchestrator.py`**. This is separate from **STEP 14** **H6** (**`editor/`** IDE shell); **`spec-phase2.md` §14** tracks IDE binary / build branding honesty.

**Product authority:** complements **`docs/PRODUCT_SPEC.md`**. Naming: **Lé Vibe** in prose; ASCII paths under **`.lvibe/`**. **Continue / AI Pilot** intent: **`docs/AI_PILOT_AND_CONTINUE.md`**. **Per-stage PM docs:** **`docs/PM_STAGE_MAP.md`**. **Spec index (orchestrator + E1 evidence):** **`docs/PRODUCT_SPEC.md` §9** — regression mapping and tests: **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** (**§1**/**H8** + §5–§10), **`le-vibe/tests/`** (e.g. **`test_session_orchestrator.py`**, **`test_session_orchestration_spec_step2_contract.py`** (this intro + **STEP 2**), **`test_continue_workspace.py`**, **`test_le_vibe_readme_e1_contract.py`**, **`test_editor_le_vibe_overrides_readme_contract.py`**, **`test_build_le_vibe_ide_workflow_contract.py`** — **STEP 14** / **H6**).

**Maintainer index (Roadmap H1–H8):** [`README.md`](README.md) — distribution / trust / product-surface guides, named from **`PRODUCT_SPEC` §9** (*Maintainer index*).

**H8 / trust (CI, Dependabot, ISSUE_TEMPLATE/ + config.yml # H8 & reporting):** [`docs/README.md`](README.md) *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** ([`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) **`#` H8** maintainer lines), [`privacy-and-telemetry.md`](privacy-and-telemetry.md) (*E1 contract tests*), [`SECURITY.md`](../SECURITY.md) (*Related docs*, incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings* — non-canonical; **[`spec-phase2.md`](../spec-phase2.md)**); **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md) STEP 12** *E1* when editing reporter intros or workflow headers.

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow and **§5** workspace memory consent before **`.lvibe/`** on packaged hosts.

**Phase 2 vs this tree:** Session manifests and agents apply to **workspace** **`.lvibe/`** and **Continue** in this document. The **Lé Vibe IDE** desktop shell (Code OSS / **VSCodium** build, CI, packaging) is owned under **`editor/`** — **[`editor/README.md`](../editor/README.md)**, **[`editor/BUILD.md`](../editor/BUILD.md)**, **[`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)** (**H6**); **H7** templates (**`packaging/flatpak/`**, **`packaging/appimage/`**, **[`docs/flatpak-appimage.md`](flatpak-appimage.md)**) — **[`spec-phase2.md`](../spec-phase2.md) §14**. PM epics that ship the **shell** alongside the stack should treat **`editor/`** work as **P0** with **`le-vibe/`** — local **H6** smoke (no Electron compile): **`./editor/smoke.sh`** from the monorepo root; stack vs IDE CI split — **[`docs/ci-qa-hardening.md`](ci-qa-hardening.md)** (*IDE smoke*). **14.d:** [`branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md) — read *PRODUCT_SPEC §7.2 (read before overrides)* first ([**`PRODUCT_SPEC.md`**](PRODUCT_SPEC.md) §7.2); fast smoke ≠ Lé Vibe–visible IDE branding; **[`editor/README.md`](../editor/README.md)** *14.c vs 14.d*. **GitHub:** **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (pre-binary **`ide-ci-metadata.txt`** on the default **`linux` job**; optional **`linux_compile`** — not default on **`pull_request`** — runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** → **`dev/build.sh`** (fail fast — **`editor/BUILD.md`** *CI*; **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** = **`editor/.nvmrc`** — **14.a** / **14.e**; **`LEVIBE_SKIP_NODE_VERSION_CHECK`**); may upload **`vscodium-linux-build.tar.gz`** — **14.e / 14.f** when opt-in) and manual **[`build-linux.yml`](../.github/workflows/build-linux.yml)** (**`uses:`** the same workflow). **E1 (overrides doc):** [`test_editor_le_vibe_overrides_readme_contract.py`](../le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py) — [`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md) (**STEP 14** / **H6** launcher + workflow strings). **E1 (IDE workflow):** [`test_build_le_vibe_ide_workflow_contract.py`](../le-vibe/tests/test_build_le_vibe_ide_workflow_contract.py) — [`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) **`ide-ci-metadata.txt`** **`le_vibe_editor_docs`** (**`LE_VIBE_EDITOR`** pointer), **`upload-artifact`** **`retention-days`** on the metadata upload, workflow **`permissions:`** **`contents: read`**, **`actions: write`**; GitHub Actions run **Summary** **Pre-binary artifact** line mirrors the same stack story (see **[`editor/README.md`](../editor/README.md)** *CI*).

---

## 1. Why this exists

- **Product managers** design **epics** and **tasks** once; the manifest is the machine- and human-readable backlog loop.
- **Session steps** are a **fixed vocabulary** of phases (opening, bootstrap, epic iteration). PMs configure **which** steps exist and **order**, not arbitrary code.
- **Skill agents** are roles (PM, DevOps, etc.) with **markdown** definitions—portable, diffable, and LLM-friendly.
- The **orchestrator** (master) routes steps, enables/disables agents, and grounds negotiation in **`.lvibe/`** RAG material (manifest, chunks, incremental memory—not monolithic repo dumps).

---

## 2. Skill agents (defaults)

All **eight** roles are **enabled by default**. Each has a **markdown** file describing scope, responsibilities, and boundaries (modern SaaS org norms: clear ownership, escalation to PM/User, no silent scope creep).

| Agent `id` | File (template & workspace) | Role |
|------------|-------------------------------|------|
| `product_manager` | `templates/…/product-manager.md` → `.lvibe/agents/product-manager/skill.md` | Outcomes, epics, priorities, stakeholder framing. |
| `project_manager` | `…/project-manager.md` → `.lvibe/agents/project-manager/skill.md` | Sequencing, dependencies, risk, delivery cadence. |
| `senior_backend_engineer` | `…/senior-backend-engineer.md` → `.lvibe/agents/senior-backend-engineer/skill.md` | APIs, data, services, performance, security backend. |
| `senior_frontend_engineer` | `…/senior-frontend-engineer.md` → `.lvibe/agents/senior-frontend-engineer/skill.md` | UI/UX implementation, accessibility, client performance. |
| `senior_devops_engineer` | `…/senior-devops-engineer.md` → `.lvibe/agents/senior-devops-engineer/skill.md` | CI/CD, infra as code, observability, release safety. |
| `senior_qa_engineer` | `…/senior-qa-engineer.md` → `.lvibe/agents/senior-qa-engineer/skill.md` | Test strategy, quality gates, regression mindset. |
| `senior_industry_advisor` | `…/senior-industry-advisor.md` → `.lvibe/agents/senior-industry-advisor/skill.md` | Domain and product judgment: counsel for PM/PjM/Engineering leadership; vets coherence with **QA** on agentically produced outcomes; uses RAG + general domain knowledge (labeled). |
| `user` | `…/user.md` → `.lvibe/agents/user/skill.md` | Human intent, acceptance, “what good looks like”; can be automated as a stub for playbooks. |

**Paths:**

- **Templates (this repo):** `le-vibe/templates/agents/<name>.md`
- **Workspace (skill source files):** **`.lvibe/agents/<agent_id>/skill.md`** (PRODUCT_SPEC §5.2); session manifest **`skill_path`** entries point at these files (see `schemas/session-manifest.v1.example.json`).

**Storage & consent:** **`.lvibe/`** is **opt-in** after user consent (**PRODUCT_SPEC** §5.1); size budget and compaction apply per **§5.4–5.5**.

---

## 3. Session manifest JSON (`session-manifest.v1`)

**Single file** per active session configuration (iterate PM epics/tasks **and** drive session machinery).

### 3.1 Top-level shape

| Field | Type | Meaning |
|-------|------|---------|
| `schema_version` | string | e.g. `"session-manifest.v1"` |
| `meta` | object | ids, timestamps, optional `workspace_summary` / RAG pointers; optional **`continue_construction_note`** / **`ai_pilot_note`** (human hints; tie to **[`docs/AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md)** and the Master queue in **[`docs/PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md)**) |
| `session_steps` | array | Ordered **SESSION STEPS** designed by PM workflow (see §4) |
| `agents` | object | Which roles are on; paths to skill markdown |
| `product` | object | **Epics** and **tasks** (PM-owned backlog) |

### 3.2 `product.epics`

- Each **epic** has `id`, `title`, optional `description`, and `tasks[]`.
- Each **task** has `id`, `title`, `status` (`pending` \| `in_progress` \| `done` \| `blocked`), optional `assignee_agent`, `notes`, `acceptance_criteria`.

The orchestrator **iterates** epics/tasks in order unless a step overrides (e.g. “current epic only”).

### 3.3 `agents`

- `defaults.all_enabled`: boolean — default **true** (all eight on).
- `roles[]`: optional per-role overrides: `id`, `enabled`, `skill_path` (relative to `.lvibe/` or template root).

---

## 4. SESSION STEPS (PM-designed)

Steps are **declarative** entries in `session_steps[]`. Each has at least `id`, `type`, `title`.

**Standard types** (v1):

| `type` | Meaning |
|--------|---------|
| `opening_intent` | First interaction: prompt user to **describe what they want to build**; skippable. |
| `workspace_scan` | Orchestrator builds **shared context** from existing repo (for every enabled agent) when user skips opening and a workspace exists. |
| `agent_bootstrap` | Load skill markdown + RAG refs; establish negotiation protocol for the session. |
| `epic_iteration` | Walk `product.epics` / tasks; agents coordinate per task until done or blocked. |
| `continue_construction` | **Resume** from current manifest / epic state (maps to user **“Please continue”** in **`docs/AI_PILOT_AND_CONTINUE.md`**). |
| `ai_pilot` | **Sustained** coordinated mode (prompt-gated); visible multi-agent style orchestration; same guards as **PRODUCT_SPEC** §5 / §8. |
| `retrospective` | Optional close-out (optional v1). |

**Opening rule:**

- **Prompt copy:** default title like **“Describe what you want to build”**; user may **skip**.
- **If skip** and **workspace root has meaningful files**: run **workspace scan** — orchestrator summarizes purpose, stack signals, and key paths; writes compact entries for **each** agent’s context (e.g. under `.lvibe/memory/` + chunk refs) so negotiation is **grounded**, not generic.

**If skip** and **empty workspace:** fall back to minimal bootstrap + PM asks for intent later.

---

## 5. Orchestration & RAG

- Agents **do not** each ingest the whole repo blindly. They use **`.lvibe/`** (manifest, `memory/incremental.md`, `chunks/`, `AGENTS.md`) per **`docs/PRODUCT_SPEC.md` §5**.
- **Session manifest** is part of that ground truth: epics/tasks + current step index (implementation may add `meta.current_step_id` or a sidecar state file—see example JSON).
- **Negotiation:** orchestrator proposes next action from `session_steps` + current epic/task; agents respond per skill file; decisions recorded in incremental memory **in small, token-efficient** snippets.
- **Master vs subagents (product model):** The **in-app** primary model **grounds** on **`.lvibe/`** and manifest/task state; it **invokes** subagent roles **when appropriate** so their “learning” (summaries, decisions, chunk refs) is **reused**—see **`docs/PRODUCT_SPEC.md` §7**. Not every role runs on every turn; **selective** orchestration keeps latency and token use **lean**.
- **Session-long updates:** Even when the user is **not** chat-heavy, the product may **append bounded** updates to **`.lvibe/`** over an open session (**PRODUCT_SPEC** §5)—implementation must stay **safe** and **small-token**.
- **Secrets:** Do not ingest **`.env` / `.env.local`** etc. by default; follow **`docs/PRODUCT_SPEC.md` §8**. Subagent prompts must respect the same rules.

### 5.1 User gate — **USER RESPONSE REQUIRED** (coordinator authority)

When the **master orchestrator** lacks **product authority** or **clear** technical consensus among subagents on a **high-impact** decision, it **must not** proceed with assumptions (**`docs/PRODUCT_SPEC.md` §7.2**).

**Protocol (must ship in product behavior and in Cursor-style prompts):**

1. **Halt** execution of the affected epic/task/step until resolved.
2. Emit a single prominent line: **`USER RESPONSE REQUIRED`** (all capitals).
3. Below it, list **numbered questions** (1., 2., …) with **short** context each (what tradeoff, why it matters).
4. Instruct the user to answer **by number**. Accept **“No preference”**, **“I don’t care”**, **“Your call”**, **“Surprise me”**, or equivalent as **delegation** to the orchestrator + PM/Industry Advisor heuristics—not as empty permission to invent facts.
5. **Subagent disagreement:** If two or more roles conflict, the coordinator summarizes **positions** and **one** consolidated question set—no voting spam.
6. Resume only after user reply (or explicit delegation as above); record the outcome in **`.lvibe/`** incremental memory as a **short** decision stub (no essays).

**Examples** of gate triggers: major **DB** / persistence shape changes; **breaking** public API; **brand/design** forks; **security** posture changes; unresolved **multi-agent** dispute on approach.

---

## 6. Files to ship in-repo (building the app)

| Path | Role |
|------|------|
| `schemas/session-manifest.v1.example.json` | Canonical example + comments in spec |
| `le-vibe/templates/agents/*.md` | Default skill definitions (SaaS-style) |
| Workspace prepare (`le_vibe.workspace_hub` + `le_vibe.session_orchestrator`) | Seeds `.lvibe/session-manifest.json` when absent from **`schemas/session-manifest.v1.example.json`** in a monorepo checkout (`session_manifest_example_source_path`), else the bundled copy (must match — E1 `test_session_orchestrator`); copies `le-vibe/templates/agents/*.md` into `.lvibe/agents/` when missing; hooks in `session_orchestrator` for **opening_intent** skip → **workspace_scan** |

---

## 7. Success criteria (this spec)

- [x] Example JSON validates the mental model: **session_steps** + **product.epics** + **agents**.
- [x] Eight agent markdown files exist with **Lé Vibe**-aligned, SaaS-realistic defaults (including **Senior Industry Advisor**).
- [x] Opening / skip / workspace-scan behavior is documented for implementers (`le_vibe.session_orchestrator`: `resolve_next_step_after_opening_skip`, `apply_opening_skip`, `write_workspace_scan_stub`).
- [x] Same files conceptually reused under **`.lvibe/`** for end users.

---

*This spec is input to the Master orchestrator lazy prompt and to future `lvibe` / extension features.*
