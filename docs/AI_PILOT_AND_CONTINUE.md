# Lé Vibe — Continue construction & **AI Pilot**

**STEP 17 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **Please continue** / **AI Pilot** UX vs **`PRODUCT_SPEC`** §7 (**§7.2** **`USER RESPONSE REQUIRED`**); Continue rules in **`le_vibe/continue_workspace.py`**, product copy in root **`README.md`**. **E1:** [`test_root_readme_ai_pilot_contract.py`](../le-vibe/tests/test_root_readme_ai_pilot_contract.py), [`test_privacy_and_ai_pilot_prioritization_cargo_contract.py`](../le-vibe/tests/test_privacy_and_ai_pilot_prioritization_cargo_contract.py), [`test_pm_stage_map_step17_contract.py`](../le-vibe/tests/test_pm_stage_map_step17_contract.py).

**Product intent:** Lé Vibe is not a one-shot chat. It supports **ongoing, self-coordinated construction** of the user’s project: the **master** model and **subagents** follow **product-management** documentation and **session manifests**, iterate **epics/tasks**, and can run in modes where work **continues** without the user restating the whole plan.

**Naming:** **Lé Vibe** in prose; paths **`le-vibe`**, **`.lvibe/`** as elsewhere.

**Canonical roster:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §9 (*Relationship to existing specs*) places this document in one table with **`PROMPT_BUILD_LE_VIBE`**, **`SESSION_ORCHESTRATION_SPEC`**, **`PM_STAGE_MAP`**, and **`PRODUCT_SPEC_SECTION8_EVIDENCE`**.

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) → **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow and **§5** workspace consent on packaged hosts (same **§7**/**§8** guards apply).

**Maintainer full-product `.deb` (STEP 14 / §7.3):** **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** — **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** prints **Full-product install** on success; local close-out gate: **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable close-out output); default **[`ci.yml`](../.github/workflows/ci.yml)** artifact **`le-vibe-deb`** is **stack-only** — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*); **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles*).

**Phase 2 vs this tree:** In-editor **AI Pilot** / rich **Continue** on **Code OSS** targets the **Lé Vibe IDE** under **`editor/`** (**H6** — **[`editor/README.md`](../editor/README.md)**, **[`editor/BUILD.md`](../editor/BUILD.md)**). **[`spec-phase2.md`](../spec-phase2.md) §14** lists what **`r-vibe`** ships today (launcher, **`.lvibe/`**, Continue rules, **VSCodium** submodule + IDE CI smoke) vs remaining **H6**/**H7** work.

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
| [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) | E1 audit — **§1** (**H8** naming), §7 (**§7.1** / **§7.2**), §8, §10; **`le-vibe/tests/`** (e.g. **`test_product_spec_section8.py`** (*Prioritization* — **`linux_compile`** (fail fast: **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** → **`dev/build.sh`** — **`editor/BUILD.md`** *CI*; **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** vs **`editor/.nvmrc`**, **`LEVIBE_SKIP_NODE_VERSION_CHECK`**), **`vscodium-linux-build.tar.gz`**, **`actions/cache@v4`**, **`~/.cargo`**, **`spec-phase2.md` §14**; **`ide-ci-metadata.txt`**, **`retention-days`**, **`permissions:`** **`contents: read`**, **`actions: write`**, **Pre-binary artifact**, **`editor/BUILD.md`**, **`editor/VENDORING.md`**), **`test_continue_workspace.py`**, **`test_session_orchestrator.py`**, **`test_root_readme_ai_pilot_contract.py`**, **`test_le_vibe_readme_e1_contract.py`**, **`test_issue_template_h8_contract.py`**, **`test_editor_le_vibe_overrides_readme_contract.py`**, **`test_build_le_vibe_ide_workflow_contract.py`** — **STEP 14** / **H6**, [`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md), [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)) |
| [`privacy-and-telemetry.md`](privacy-and-telemetry.md) | Localhost / logs; **§8**; *Related documentation* → **E1 contract tests** (root **`README`** *Tests*, **`le-vibe/tests/`**) |
| [`SECURITY.md`](../SECURITY.md) | Vulnerability reporting; *Related docs* — **`docs/README`** *Product surface* (**H8** — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**, **`privacy-and-telemetry`** *E1 contract tests*), optional **[`docs/rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings* — non-canonical; see **`spec-phase2.md`**) |

---

*This file is **scope and intent** for in-app **Continue** / **AI Pilot**; implementation may be phased (Continue rules → extension → fork UI).*
