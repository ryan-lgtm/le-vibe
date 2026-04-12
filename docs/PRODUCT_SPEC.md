# Lé Vibe — Product specification (must ship)

This document is the **single source of truth** for **must-ship** product requirements. Everything below is **required** for the Lé Vibe vision—not optional backlog.

**Repository:** `r-vibe` — **monorepo:** `le-vibe/` (Python stack + launcher **`.deb`**) and `editor/` (Lé Vibe IDE shell); see **`editor/README.md`**.

---

## Prioritization (north star)

**Single project, one repository (monorepo):** **Lé Vibe** = **`le-vibe/`** (Python bootstrap, launcher, stack **`.deb`**, **`.lvibe/`**) + **`editor/`** (Code - OSS–based **Lé Vibe IDE** binary). No separate “fork repo” is required for product coherence—only this tree.

**What we are optimizing for:** a **single installable Lé Vibe IDE**—branded **Code - OSS** binary (name, icons, About, desktop entry) built from **`editor/`**, not “upstream VSCodium + our scripts” as the long-term default. Roadmap **H6** — **[`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)** — is **P0**: land upstream sources under **`editor/`**, wire CI, ship artifacts from the **same** git history as the stack.

**Spine vs shell:** **`le-vibe/`** supplies hardware-aware **Ollama**, **`lvibe`**, managed lifecycle, **Continue** wiring, and **`.lvibe/`** policy. **`editor/`** supplies the desktop application. Both share **`~/.config/le-vibe/`** and **`LE_VIBE_EDITOR`** conventions documented here.

**How to sequence work:** populate **`editor/`** (submodule, subtree, or import), run **`./editor/smoke.sh`** from the repository root so the vendored-tree gate matches **`build-le-vibe-ide.yml`** (layout, upstream script syntax, **`editor/.nvmrc`** — see **`docs/ci-qa-hardening.md`** *IDE smoke*). The workflow **`build-linux.yml`** is a **`workflow_dispatch`** alias that **reuses** the same job (labels in PM docs may say “build-linux”). Then wire IDE build CI; keep **`le-vibe/`** packages and pins aligned on each release tag.

### Product and project management — in service of the IDE

Session manifests, **`.lvibe/`** epics/tasks, skill agents, and orchestration docs exist to **coordinate shipping the Lé Vibe IDE and stack as one product**—not as unrelated backlogs.

- **Design corpus (do not drift):** **`docs/PRODUCT_SPEC.md`** (this file), **`spec-phase2.md`** (Phase 2 product definition, architecture, managed Ollama, milestones), **`spec.md`** (bootstrap/tiering), **`docs/PROMPT_BUILD_LE_VIBE.md`** (orchestrator queue), **`docs/SESSION_ORCHESTRATION_SPEC.md`**, **`docs/PM_STAGE_MAP.md`**, **`docs/AI_PILOT_AND_CONTINUE.md`**, and **`schemas/session-manifest.v1.example.json`**. PM stages and lazy prompts **prioritize `editor/`** (H6) after baseline regression—see Master orchestrator **order** in **`PROMPT_BUILD_LE_VIBE.md`**.
- **Owner intent:** The **desktop editor** is the primary product surface; **`lvibe`**, Ollama, Continue, and **`.lvibe/`** implement the **local-first, honest-tier** experience defined in those specs. Material IDE choices (branding scope, update channel, bundling) use **§7.2** (**`USER RESPONSE REQUIRED`**) when specs do not uniquely decide.
- **Canonical IDE path:** **`editor/README.md`**, **`editor/BUILD.md`** (local compile entrypoint), **`editor/VENDORING.md`**, **`docs/vscodium-fork-le-vibe.md`**.

---

## 1. Official naming

| Context | Rule |
|---------|------|
| **User-facing copy** (UI, welcome, About, marketing, docs body, errors meant for humans) | Use **Lé Vibe** (capital **L**, **é** in *Lé*). |
| **ASCII identifiers** | Keep **`le-vibe`** (Debian package, directories, `~/.config/le-vibe/`), **`lvibe`** (default CLI command name), **`.lvibe/`** (workspace folder). |
| **Code / imports** | Existing Python package name `le_vibe` may remain; new public strings should say **Lé Vibe**. |

**Must ship:** Audit and update user-visible strings across launcher, man pages, `.desktop`, README, **`.github/`** (**`ci.yml`**, **`dependabot.yml`**, **`ISSUE_TEMPLATE/`** + **`config.yml`** **`#` H8** maintainer lines on reporter-facing YAML), and extension/Continue copy so **Lé Vibe** is consistent wherever Unicode is acceptable.

---

## 2. Default CLI: open the editor in a folder

**Must ship:** From any terminal, after install, the user can:

```bash
cd /path/to/project
lvibe .
```

**Behavior:**

1. **`lvibe`** is the **default, discoverable CLI** (install `lvibe` on `PATH`, e.g. `/usr/bin/lvibe`).
2. It forwards to the same launcher stack as today’s `le-vibe` (managed Ollama, first-run policy, editor spawn).
3. **`.`** (or any path) is passed to the Code OSS / VSCodium binary so the **workspace opens in that folder** (equivalent to `codium /path/to/project`).
4. **`le-vibe`** may remain as a compatibility symlink or alias to the same entrypoint—document both; **primary UX** is **`lvibe`**.

**Implementation note:** The launcher already accepts trailing `editor_args`; ensure the shell wrapper passes arguments through and document `lvibe <path>` in man page and README.

---

## 3. Model policy: default and lock to the most concrete model for hardware

**Must ship:**

1. **Hardware-aware selection** (reuse tier engine) always resolves to a **specific, concrete model tag** (not an open-ended “AUTODETECT” as the only persisted value when a tag is known).
2. **Lock** the chosen model for the product session / config so upgrades do not silently drift without user intent (persist explicit model id under `~/.config/le-vibe/`).
3. **Document** the policy: best-fit for **this** machine, honest tiering, no fake “always 70B” claims.

---

## 4. First-run / running welcome: positioning

**Must ship:** When the app is running (first launch or dedicated welcome surface), show **Welcome to Lé Vibe** and explain:

- **Lé Vibe** is an **open source** and **free** coding environment.
- It is positioned as a **local-first alternative** to **Cursor** (same general intent—AI-assisted coding—not feature parity).
- Short, honest paragraph; expandable later in docs.

**Surface:** Implement where the product actually controls UI (Continue onboarding, small extension webview, or forked editor first-run)—pick one path and ship it.

---

## 5. Workspace `.lvibe/` — RAG hub, per-agent context, consent, and storage sanity

**Naming:** The folder is always **`.lvibe/`** (ASCII), never alternate spellings in code or docs.

**Core idea:** Lé Vibe runs on **local hardware**; agent work must stay **efficient**. Heavy cost should **not** go to repeatedly re-reading huge caches or unstructured repo dumps. The agent **orchestrates** through a **structured, token-efficient** layer rooted in **`.lvibe/`**—but **only when the user agrees** to local project memory.

### 5.1 Consent: create `.lvibe/` or stay bare-bones

**Must ship:**

1. **Universal prompt (clear copy):** Before **first** use of Lé Vibe–backed memory for a workspace, the user sees a **short, honest** explanation: **what** `.lvibe/` is (local markdown + small RAG-style notes for agents, not committed by default if gitignored), **why** it helps, and that it **stays on disk** subject to a **size budget** (below).
2. **Accept:** User **accepts** → create **`.lvibe/`** and apply defaults (layout §5.3, budget §5.4).
3. **Decline:** User **declines** → **do not create** **`.lvibe/`**. Lé Vibe behaves like a **normal code editor + local model**: **no** project memory folder, **no** automatic RAG writes. Persist the opt-out for that workspace (e.g. under **`~/.config/le-vibe/`**) so the user is **not** nagged every session.
4. **Reversible:** User can **enable** Lé Vibe memory later in settings (same explanation + accept).

### 5.2 Simple folder model (product structure)

Keep the tree **easy to reason about** and **easy to cap by size**:

| Area | Role |
|------|------|
| **Per-agent subtrees** | Under **`.lvibe/agents/<agent_id>/`** — **persona + project-specific context** and **interaction history** for that role (small markdown files; bounded growth per agent). Example `agent_id`: `product_manager`, `senior_backend_engineer`, … |
| **Shared RAG / chunks** | Under **`.lvibe/rag/`** (or equivalent top-level siblings such as existing **`chunks/`**, **`memory/`**) — **cross-cutting** chunk references, manifests, and token-efficient retrieval material **separate** from per-agent narrative so compaction can target **RAG first**, then **oldest agent notes**, without mixing concerns. |

Exact filenames may evolve; the **separation** (agent-local vs shared RAG) is **must ship** for maintainability and compaction.

### 5.3 Behavior when `.lvibe/` exists (must ship)

1. **Agent default:** Rules / Continue defaults tell the primary model to **prefer** **`.lvibe/`** for recall over ad-hoc full-file churn.
2. **Continuous learning:** Append **small, bounded** entries (incremental memory) as today—never unbounded single files.
3. **Session-long learning:** Same as §5.1–5.2: **background-friendly** updates for users who are not chat-heavy, **without** exceeding the **storage budget**.

### 5.4 Storage budget (megabytes) — default and user control

**Must ship:**

1. **Global default cap:** **50 MB** per workspace **`.lvibe/`** tree (product default; document in onboarding). Users may **raise or lower** the cap in settings (megabytes; sane **min/max** enforced in implementation, e.g. 10–500 MB—exact bounds are engineering detail).
2. **Transparency:** Show **current usage vs cap** somewhere sensible (settings or status), not hidden.
3. **Enforcement:** Writes that would exceed the cap **must not** silently expand the folder—**block or compact first** (§5.5).

### 5.5 When the folder is full (compaction — product policy)

**Goal:** Stay **lean** without surprising data loss.

**Must ship (behavioral order):**

1. **Before hard failure:** Prefer **automatic compaction** over rejecting user work when possible.
2. **Compaction strategy (default):**  
   - **First:** **RAG / chunk layer** — merge or summarize **oldest** low-value chunk refs; collapse redundant entries in shared **`rag/`** / **`chunks/`** / incremental pools.  
   - **Second:** **Per-agent** folders — summarize **oldest** dated sections into shorter **rollups** (keep a one-line pointer to “archived detail” only if still needed).  
   - **Third:** **Round-robin** trim among agents if still over cap—**never** delete **`session-manifest.json`** without replacing with a minimal stub; never delete **active task** state without writing a summary elsewhere first.
3. **Optional escalation:** If compaction cannot restore headroom, **notify** the user and offer **raise cap** or **clear category** (e.g. clear one agent’s history) with confirmation.
4. **No silent infinite growth:** The **50 MB** (or user) cap is a **hard** budget for normal operation; compaction runs are **deterministic** and **logged** at operator level (not secret telemetry).

### 5.6 Relation to older “always create” behavior

Implementation must **migrate** from **unconditional** `.lvibe/` creation to **consent-gated** creation per §5.1, while preserving **gitignore** and **secrets** rules (**§6**, **§8**).

**Non-goals for excuses:** “RAG is hard” is not a reason to skip consent, caps, or a **minimal** compaction path once `.lvibe/` is enabled.

---

## 6. Git: ignore `.lvibe/` by default

**Must ship:**

- If the workspace contains a **`.gitignore` file**, ensure **`.lvibe/`** is listed (append if missing, idempotent).
- If there is **no** `.gitignore`, do **not** silently create one unless product policy explicitly adds “init repo hygiene”—**default rule:** only auto-append when `.gitignore` **exists**.

---

## 7. Runtime: master agent, subagents, and a harmonious assist

**Product intent (north star):** The **primary LLM** in the app is **lean and efficient**. It **grounds** on **`.lvibe/`** RAG (small chunks, manifests, incremental memory—not whole-repo slop) and on **task/epic** state from the **session manifest** (**`docs/SESSION_ORCHESTRATION_SPEC.md`**).

**Must ship (behavioral model):**

1. **Subagents** (skill roles: PM, Engineering, QA, **Senior Industry Advisor**, etc.) are **first-class**: their markdown definitions and negotiated outputs feed context under **`.lvibe/agents/<agent_id>/`** and shared RAG (**§5.2**) so the master agent **reuses what they “learn”** instead of re-deriving everything each turn (when **§5.1** consent is on).
2. **Invocation:** The runtime **invokes** or **simulates** subagent perspectives **when it makes sense** for the current task (task-based management, not a wall of parallel chatter)—orchestration is **selective**, not always “all agents every time.”
3. **Harmony:** Light assist and heavy “vibe-code” should both feel **coherent**: same **`.lvibe/`** layer, same **token discipline**, **fast** paths for simple asks.

### 7.1 Continue construction & **AI Pilot** (next product phases)

**Scope and intent** (full detail: **[`docs/AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md)**):

1. **“Please continue”** — User instruction to **resume construction** from current PM/session state (manifest + epics/tasks + **`.lvibe/`**), not restart from zero.
2. **AI Pilot** — User-enabled mode (e.g. **prompt command**, later UI) for **sustained**, near–real-time **auto** advancement of work with **visible** multi-role coordination; still bound by **§5**, **§8**, and consent.
3. **Self-coordinated agents** — Stages are **doc-locked**: engineers (and future in-app agents) follow **`docs/PM_STAGE_MAP.md`** so each step has a **primary PM document**—not ad hoc guessing.

**Cursor / lazy-prompt mimic today:** Repeatable **self-coordinating engineer** loop in **`docs/PROMPT_BUILD_LE_VIBE.md`**—**not** a disposable one-shot per question.

### 7.2 User gate — authority, escalation, and **USER RESPONSE REQUIRED**

The **master orchestrator** must **not** guess on **material** decisions that belong to the **user** or that **specialty subagents** cannot resolve without human product authority.

**Must ship (behavioral model):**

1. **Authority model:** The orchestrator maintains a clear sense of **what it may decide alone** (e.g. sequencing within agreed scope, trivial refactors) vs **what requires user input** (e.g. product/design direction, **major** schema or database reshapes, breaking API contracts, tradeoffs with long-lived cost).
2. **Subagent → coordinator:** Subagents **request** the coordinator when a step is **high-impact** or when **specialists disagree**. The coordinator **does not** override the user on those categories.
3. **Halt, don’t assume:** When the orchestrator **cannot** responsibly decide, it **stops automated execution** of that branch and surfaces a **user gate**—**no** silent defaults on matters listed above.
4. **USER RESPONSE REQUIRED:** The UI (or agent output in Cursor mimic) must show that exact label in **ALL CAPS** as a **banner line**, followed by **numbered questions** the user must answer to proceed.
5. **Answer format:** Instruct the user to reply by **number** (e.g. `1: …`, `2: …`). Accept explicit **non-preference** answers such as **“No preference”**, **“I don’t care”**, **“Your call”**, or **“Surprise me”** as **valid**—the orchestrator then may choose a **documented** default or escalate to **Product Manager** / **Senior Industry Advisor** role per skill files, **without** inventing user intent.
6. **Examples** of gate-worthy situations: **design** choices that affect UX or brand; **major database** or storage restructures; **persistent disagreement** among subagents on approach; legal/compliance-sensitive choices (surface to **User** / **Product Manager**).

**Detail and protocol:** **`docs/SESSION_ORCHESTRATION_SPEC.md`** (orchestration §5). Lazy prompts should mirror halt semantics (**`docs/PROMPT_BUILD_LE_VIBE.md`**).

Implementation may span Continue rules, extension hooks, and future fork UI—this section states **what** the product must achieve for **experience**, not one fixed stack.

---

## 8. Security: secrets and env files

**Must ship:**

1. **Default deny:** Do **not** read **`.env`**, **`.env.local`**, **`.env.*`**, or common secret file patterns **unless** the user **explicitly** instructs the product/agent to use them for a defined purpose.
2. **Explicit use:** When the user does instruct, **subagents and the master agent** must treat contents as **high sensitivity**—no echoing secrets into **`.lvibe/`** RAG, logs, or incremental memory; prefer **references** (“user approved reading `.env` for key X”) over **values**.
3. **Document** this policy in operator/user docs and agent skill files where relevant.

---

## 9. Relationship to existing specs

| Document | Role |
|----------|------|
| **`spec.md`** | Phase 1 bootstrap, tiering, Ollama, Continue templates. |
| **`spec-phase2.md`** | Desktop shell, managed Ollama lifecycle, Debian-first; **§14** — in-repo snapshot vs **H6**/**H7** deferrals; optional **`docs/rag/le-vibe-phase2-chunks.md`** (*RAG / embeddings* — not a second source of truth). |
| **`docs/PRODUCT_SPEC.md`** (this file) | **Must-ship product narrative + CLI + `.lvibe/` + welcome + naming**; ***Prioritization*** + ***Product and project management — in service of the IDE*** — monorepo: **`editor/`** (IDE) + **`le-vibe/`** (stack). |
| **`docs/SESSION_ORCHESTRATION_SPEC.md`** | **PM-driven session manifests**, skill agents, master orchestrator steps, epic/task iteration (same model for **this repo** and **user workspaces**). |
| **`docs/AI_PILOT_AND_CONTINUE.md`** | **Continue construction**, **AI Pilot**, visible coordination, self-coordinated agents (intent). |
| **`docs/PM_STAGE_MAP.md`** | **Orchestrator STEP → PM docs** (per-stage authority for engineers and auto-style loops). |
| **`docs/PROMPT_BUILD_LE_VIBE.md`** | **Master orchestrator** queue (STEPS **0–17**; **execution order** **0→1→14→2–13→15–17**), Roadmap H, lazy prompts for engineering |
| **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** | E1 regression evidence (**§1**/**H8**, §5–§10) ↔ **`le-vibe/tests/`**; filename **SECTION8** historic |
| **§7.2** (this file) | **USER RESPONSE REQUIRED** — halt when orchestrator cannot decide; numbered questions; accept “no preference.” |

**Maintainer index (Roadmap H):** [`README.md`](README.md) lists **H1–H8** guides (e.g. `apt-repo-releases`, `sbom-signing-audit`, `ci-qa-hardening`, `continue-extension-pin`, `brand-assets`, `flatpak-appimage`, `vscodium-fork-le-vibe`) and links back here—they **supplement** this table; **§8** still governs shipped agent/secret behavior. The **`.deb`** also ships **`/usr/share/doc/le-vibe/README.Debian`** (maintainer source: [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) with post-install steps, **§5** **`.lvibe/`** consent, **Phase 2** scope (**`spec-phase2.md` §14**, **H6**/**H7** vs this package), and pointers back to this file and [`README.md`](README.md).

Conflicts: **this file wins** for product naming and must-ship features until specs are reconciled. **Session orchestration** details live in **`SESSION_ORCHESTRATION_SPEC.md`**.

---

## 10. Success criteria (acceptance)

Regression evidence (**§1** / **H8** naming, §7, §8, §10): **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** and **`le-vibe/tests/`** — e.g. **`test_product_spec_section8.py`** (welcome, Continue rule strings, §8/§7.2), **`test_continue_workspace.py`** (`.continue/rules`, **numbered questions**), **`test_workspace_hub.py`** (`.lvibe/AGENTS.md` §7.2 strings), **`test_session_orchestrator.py`** (STEP 2 — bundled **`session-manifest`** ↔ **`schemas/`**), **`test_root_readme_ai_pilot_contract.py`** (§7.1 root **`README.md`** + *Tests* / **E1 mapping** substrings), **`test_le_vibe_readme_e1_contract.py`** (**`le-vibe/README.md`** *Tests* roster), **`test_prompt_build_orchestrator_fence.py`** (Master orchestrator fence in **`PROMPT_BUILD_LE_VIBE.md`**), **`test_issue_template_h8_contract.py`** (**H8** — **STEP 12** / **`config.yml`** anchors in **`.github/ISSUE_TEMPLATE/*.yml`**), **`test_ci_yml_submodules_contract.py`** (**H6** — **`ci.yml`** checks out **`editor/vscodium`**), **`test_editor_le_vibe_overrides_readme_contract.py`** (**H6** — **`editor/le-vibe-overrides/README.md`** **STEP 14** pointers). Full **E1** contract list — root [`README.md`](../README.md) *Tests* / **E1 mapping**; **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*. **H8** **`.github/ISSUE_TEMPLATE/`** intros (incl. **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#`** maintainer lines; optional **`docs/rag/le-vibe-phase2-chunks.md`** on forms) and **`SECURITY`** *Related docs* / **`docs/README`** *Product surface* stay human-audited under **E1** — **`pytest`** does not *parse* issue-template YAML (substring contracts only). Filename **SECTION8** is historic.

- [x] User sees **Lé Vibe** in primary UI/docs copy (with **é**) where Unicode is used.
- [x] **`lvibe .`** opens the editor with the current directory as workspace.
- [x] **Concrete model** is selected and **locked** per policy; config is inspectable.
- [x] **Welcome to Lé Vibe** copy ships with OSS/free vs Cursor positioning.
- [x] **§5 Consent & storage:** First-use **explanation + accept/decline**; **decline** → **no** **`.lvibe/`**, bare-bones editor behavior; **accept** → **`.lvibe/`** with **50 MB** default budget (user-configurable), **per-agent** subfolders + **shared RAG** layout (**§5.2**), **compaction** policy (**§5.5**), usage vs cap visible.
- [x] **`.lvibe/`** hub (when enabled): agent defaults reference it; incremental, token-efficient artifacts (**legacy paths** may exist until migration to §5.2 layout).
- [x] **§7.2 User gate:** **`USER RESPONSE REQUIRED`** (all caps) + **numbered questions** when the orchestrator must not assume; **no-preference** answers are valid delegation—see **`docs/SESSION_ORCHESTRATION_SPEC.md`** §5.1.
- [x] **`.gitignore`** contains **`.lvibe/`** when a **`.gitignore`** file exists in the project.

**After baseline implementation:** use **one** prompt only—the **Master orchestrator** in **[`docs/PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md)** (ordered work queue; you do not pick steps by hand).

---

*Last updated: product direction — all sections above are must ship.*
