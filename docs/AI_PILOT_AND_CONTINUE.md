# Lé Vibe — Continue construction & **AI Pilot**

**Product intent:** Lé Vibe is not a one-shot chat. It supports **ongoing, self-coordinated construction** of the user’s project: the **master** model and **subagents** follow **product-management** documentation and **session manifests**, iterate **epics/tasks**, and can run in modes where work **continues** without the user restating the whole plan.

**Naming:** **Lé Vibe** in prose; paths **`le-vibe`**, **`.lvibe/`** as elsewhere.

**Canonical roster:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §9 (*Relationship to existing specs*) places this document in one table with **`PROMPT_BUILD_LE_VIBE`**, **`SESSION_ORCHESTRATION_SPEC`**, **`PM_STAGE_MAP`**, and **`PRODUCT_SPEC_SECTION8_EVIDENCE`**.

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) → **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow and **§5** workspace consent on packaged hosts (same **§7**/**§8** guards apply).

**Phase 2 vs this tree:** In-editor **AI Pilot** / rich shell UX may ship in a **fork** or future binary — **[`spec-phase2.md`](../spec-phase2.md) §14** lists what **`r-vibe`** ships today (launcher, **`.lvibe/`**, Continue rules) vs **H6**/**H7** deferrals.

---

## 1. “Please continue”

**User says:** e.g. *“Please continue”* (or equivalent).

**Meaning (product):** Resume **construction** from the **current** PM state—**session manifest** (`session_steps`, `meta.current_step_id` where implemented), **`product.epics` / tasks**, and **`.lvibe/`** RAG—without re-onboarding. The app **does not** start from zero; it **advances** the next **incomplete** epic/task or session step per **`docs/SESSION_ORCHESTRATION_SPEC.md`**.

**Engineering mimic (Cursor today):** Re-paste the **self-coordinating engineer lazy prompt** from **`docs/PROMPT_BUILD_LE_VIBE.md`** (or the Master orchestrator block). Same **authority chain**: **`docs/PRODUCT_SPEC.md`** → **`docs/SESSION_ORCHESTRATION_SPEC.md`** → queue in **`PROMPT_BUILD_LE_VIBE.md`**.

---

## 2. **AI Pilot**

**User turns on** **AI Pilot** (via **prompt command** or UI when shipped).

**Meaning (product):** A **sustained** mode where the agent **keeps working** in near–real time: **updating code**, **advancing tasks**, and **surfacing coordination** between roles (PM, Engineering, QA, **Senior Industry Advisor**, etc.) so the user can **witness** multi-agent style negotiation—not a black box.

**Guards:** **§8 secrets** and **§5** storage/consent still apply. **AI Pilot** does **not** bypass user **decline** of **`.lvibe/`** or **env** policy.

**Engineering mimic (Cursor today):** The engineer uses the **persistent loop** prompt: **multiple** queue steps per session when safe, **PASTE SAME AGAIN** until **LÉ VIBE SESSION COMPLETE**, with **explicit** “which agent hat” in messages when helpful—**simulating** visible coordination until the fork/extension provides a real transcript panel.

---

## 3. Intelligent self-coordinated “auto agents” (north star)

- **Authority is not vibes:** Each **stage** has a **primary PM document** (see **`docs/PM_STAGE_MAP.md`**). Agents **read that first**, then code.
- **Not one-shot prompts:** Lazy prompts are **repeatable loops**—same block, **continue** until done—**not** a disposable one-liner per question.
- **Task + RAG:** Work is **task-based** (manifest epics/tasks) + **small-token** **`.lvibe/`** context.

### 3.1 User gate (**USER RESPONSE REQUIRED**)

**AI Pilot** and **Continue** modes **must** respect **`docs/PRODUCT_SPEC.md` §7.2**: the orchestrator **halts** when it cannot decide without the user, prints **`USER RESPONSE REQUIRED`**, **numbered questions**, and accepts **no-preference** replies. Pilot does **not** mean “ship silently through ambiguity.”

---

## 4. Relationship to other docs

| Document | Role |
|----------|------|
| [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) | Must-ship behavior, **§7** runtime (**§7.2** user gate), **§5** `.lvibe/`, **§8** secrets |
| [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) | Manifest, **session_steps**, agents |
| [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) | **Orchestrator STEP → PM docs** (per-stage truth) |
| [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) | Master queue + **self-coordinating engineer loop** |
| [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) | E1 audit — **§1** (**H8** naming), §7 (**§7.1** / **§7.2**), §8, §10; **`le-vibe/tests/`** (e.g. **`test_continue_workspace.py`**, **`test_session_orchestrator.py`**, **`test_root_readme_ai_pilot_contract.py`**, **`test_le_vibe_readme_e1_contract.py`**, **`test_issue_template_h8_contract.py`**) |
| [`privacy-and-telemetry.md`](privacy-and-telemetry.md) | Localhost / logs; **§8**; *Related documentation* → **E1 contract tests** (root **`README`** *Tests*, **`le-vibe/tests/`**) |
| [`SECURITY.md`](../SECURITY.md) | Vulnerability reporting; *Related docs* — **`docs/README`** *Product surface* (**H8** — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**, **`privacy-and-telemetry`** *E1 contract tests*), optional **[`docs/rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings* — non-canonical; see **`spec-phase2.md`**) |

---

*This file is **scope and intent** for in-app **Continue** / **AI Pilot**; implementation may be phased (Continue rules → extension → fork UI).*
