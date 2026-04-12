# Phase 2 Spec: Lé Vibe — Desktop IDE & Local Agent Stack

## Purpose of this document

**Must-ship product requirements** (naming, default CLI **`lvibe`**, workspace **`.lvibe/`**, welcome copy, model lock policy) live in **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** and override this file where they differ.

**Section numbering:** In **`docs/PRODUCT_SPEC.md`**, **§7** is runtime harmony (**§7.1** Continue / AI Pilot, **§7.2** user gate / **`USER RESPONSE REQUIRED`**). In **this file**, **§7** is **Phase 2 launch and managed-Ollama lifecycle** (§7.1–7.3, plus coexistence). The numbers are **not** interchangeable—cite the file when debugging or cross-linking.

Phase 1 (`spec.md`, `le-vibe/` bootstrap) defines **machine preparation**: detect hardware, install/launch Ollama, pick a model, emit Continue-oriented config. Phase 2 defines **the product shell** around that stack: a installable desktop application named **Lé Vibe** that feels comparable in *intent* to Cursor—an IDE tuned for local, agentic coding—but built on **open components**, **Ollama**, and the Phase 1 bootstrap logic.

This spec is intentionally **Debian-based Linux first**; other OSes are out of scope until Phase 2.1+.

**Product prioritization:** **One monorepo (`r-vibe`):** **`le-vibe/`** (stack) + **`editor/`** (Lé Vibe IDE shell). **Roadmap H6** — **`docs/vscodium-fork-le-vibe.md`** — is **P0** work under **`editor/`**, not a second repository.

### Monorepo layout (`r-vibe`)

This repository ships the **bootstrap + launcher + `.deb`**, **managed Ollama** (dedicated port), **Continue** integration, **`.lvibe/`** workspace memory, and—via **`editor/`**—the **branded Code OSS / Electron** application per **`docs/PRODUCT_SPEC.md`**. **Flatpak / AppImage** top-level manifests are **SKIPPED** by policy — **`docs/flatpak-appimage.md`** (**H7**).

| Ships in **this** repo | Notes |
|------------------------|--------|
| **`lvibe`**, first-run, structured logs, CI `.deb` + SBOM + lintian | **`le-vibe/`** + **`debian/`** |
| Workspace **`.lvibe/`**, PM manifests, Continue rules, **§7.2** user-gate copy | |
| **Lé Vibe IDE** (H6) | **`editor/vscodium`** (**VSCodium** submodule), **`editor/le-vibe-overrides/`** — see **`editor/README.md`**, **`editor/BUILD.md`**, **`editor/VENDORING.md`**. Interim gate (no Electron compile): **`./editor/smoke.sh`** — same checks as **`build-le-vibe-ide.yml`** / manual **`build-linux.yml`** alias (**`docs/ci-qa-hardening.md`** *IDE smoke*; **`docs/PRODUCT_SPEC.md`** *Prioritization* — *How to sequence work*) |
| Consumer Flatpak/AppImage | **H7** — optional; not required in-tree |

**Navigation:** [`docs/README.md`](docs/README.md) — maintainer index for **Roadmap H1–H8** (named from **`PRODUCT_SPEC` §9** *Maintainer index*). **Phase 1** Ollama bootstrap (`le-vibe/` package) — [`spec.md`](spec.md). Must-ship conflicts and the **authority roster** — [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) §9.

**RAG / embeddings:** optional chunk bundle [`docs/rag/le-vibe-phase2-chunks.md`](docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview`) mirrors **§9**, **E1** (**§1**/**H8** + §5–§10), **H8** **`.github/`**, **§14** for retrieval pipelines — not a second source of truth; see [`docs/README.md`](docs/README.md). **[`SECURITY.md`](SECURITY.md)** *Related docs* lists the same file for discoverability alongside **E1** / trust docs (still non-canonical).

**Debian install:** [`debian/le-vibe.README.Debian`](debian/le-vibe.README.Debian) is shipped as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow, **§5** **`.lvibe/`** consent, **§14** scope (see **Authority** in that file), pointers to **`docs/PRODUCT_SPEC.md`** and the docs index (**§9** *Maintainer index*).

---

## 1. How realistic is a “Cursor-like” VS Code wrapper?

### What Cursor (and similar products) generally do

- Ship a **desktop shell** (often Electron-based) that embeds or closely integrates **Visual Studio Code’s open-source core** (the `vscode` repository / Code - OSS lineage), not the proprietary Microsoft distribution of “VS Code” from `code.visualstudio.com`.
- Add **custom extensions**, **branding**, **update channels**, **telemetry defaults**, and **first-run flows** so the product is a cohesive “AI IDE.”

### Feasibility: **high for a focused MVP**, with caveats

| Aspect | Realism | Notes |
|--------|---------|--------|
| **Embedding Code OSS / VSCodium-style base** | High | Many projects build on `microsoft/vscode` OSS; license is MIT with trademark constraints—**branding must not imply official Microsoft/VS Code endorsement**. “Lé Vibe” as distinct product name helps. |
| **Shipping a branded, updatable Linux app** | High | `.deb`, AppImage, or Flatpak; CI builds are well-trodden. |
| **Pre-installing an open-source AI extension** | High | Continue, Cline, Roo Code, etc.—must verify license compatibility and embedding rules per extension. |
| **Deep IDE integration rivaling Cursor** | Medium–long term | Cursor adds proprietary UI, models, and sync; matching *parity* is not required for Phase 2. **Goal:** solid **local Ollama + one strong agent UX**, not feature parity. |
| **Maintenance burden** | Medium | Tracking upstream VS Code releases, security patches, and extension API drift is ongoing work—plan for a small release train. |

**Bottom line:** Building a **Linux desktop app** that is “VS Code–compatible + our bootstrap + our defaults” is **realistic**. Calling it a full Cursor clone is not the goal; **“local-first vibe coding IDE”** is.

---

## 2. Product definition: Lé Vibe (application)

### 2.1 One-liner

**Lé Vibe** is a downloadable **Linux desktop IDE** (Code OSS–based) branded and preconfigured so that, on first install and on every launch, the user gets a **working local agentic coding environment** powered by **Ollama** and an **open-source extension**, without manual terminal setup. The default terminal entrypoint is **`lvibe`** (see **`docs/PRODUCT_SPEC.md`** §2).

### 2.2 User-facing promises

1. **Install once** — Ollama (if missing), model selection aligned with hardware, and agent extension + settings are applied as part of installation (or first-run wizard).
2. **Launch anytime** — Starting Lé Vibe **starts** its managed Ollama stack (or attaches per policy in **this document’s §7.2** — Ollama coexistence / dedicated port; **not** **`docs/PRODUCT_SPEC.md` §7.2** user gate) so the API is reachable for the session.
3. **Quit releases resources** — Closing Lé Vibe **stops** the Ollama instance that this app started (§7.1), so heavy GPU/RAM use does not persist after exit.
4. **Agent-ready** — Chat, edit, and apply-style flows work against the **chosen local model** with minimal configuration exposure.
5. **Honest about hardware** — Model tier matches machine capability (reuse Phase 1 tier engine); no fake “always 70B” marketing.

### 2.3 Non-goals (Phase 2)

- Windows / macOS installers (defer to Phase 2.x).
- Hosted models or accounts as a requirement.
- Proprietary cloud backends as default.
- Full duplication of Cursor’s unique product features (rules engine parity, etc.) unless an open extension provides them.

---

## 3. Platform scope

- **Primary:** **Debian-based Linux** (Debian, Ubuntu, Linux Mint, Pop!_OS, etc.).
- **Package format (initial):** `.deb` repository or single-file `.deb` install; document dependencies (`libgtk`, etc.) per Code OSS / Electron norms.
- **Architecture:** `x86_64` first; `arm64` when upstream base and Ollama support align.

---

## 4. High-level architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Lé Vibe (desktop)                                       │
│  ├── Code OSS shell (branded, update channel)            │
│  ├── Bundled or pinned: open-source “agent” extension    │
│  ├── Workspace defaults (Continue/Cline config, etc.)    │
│  └── Native helper / launcher hook (start/stop Ollama)     │
└──────────────────────────┬──────────────────────────────┘
                           │ on install & on each launch
                           ▼
┌─────────────────────────────────────────────────────────┐
│  le-vibe bootstrap logic (Python or thin Rust wrapper)   │
│  ├── Ensure Ollama binary + service                     │
│  ├── Tier + model selection (reuse Phase 1)              │
│  ├── Sync extension config (apiBase, model id)           │
│  └── Logs / health for optional UI surfacing             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                    Ollama @ 127.0.0.1:11434
```

### 4.1 “Wrapper” meaning here

- **Not** a minimal webview around vscode.dev alone.
- **Yes** a **custom distribution** of the open-source editor with:
  - **Lé Vibe** name, icons, and about dialog.
  - **Pre-installed** extension(s) and **default settings** pointing at local Ollama.
  - **Lifecycle hooks** that run the bootstrap/ensure step before or as the editor process starts.

---

## 5. Open-source agent extension (choice)

Phase 2 should **standardize on one** primary extension for MVP to reduce QA surface:

| Candidate | Role | Considerations |
|-----------|------|------------------|
| **Continue** | Chat + edit + apply; Ollama-first | Very aligned with Phase 1 templates; verify embedding/redistribution terms. |
| **Cline** | Agentic tasks | Strong UX; check license and config automation. |
| **Others** | Alternatives | Evaluate later as “optional packs.” |

**Spec requirement:** Pick **one** for v1; document license file in repo; pin a **version range** for reproducible builds.

---

## 6. Install-time behavior (first run)

1. **Dependency check** — Python 3 / curl / minimal tools as needed (or ship a static helper).
2. **Invoke Phase 1 logic** (or embedded equivalent):
   - Install Ollama if absent (official script or `.deb` dependency).
   - Score hardware → tier → model ladder → pull model.
   - Write **extension config** into the user config path Lé Vibe owns (e.g. `~/.config/LeVibe/...` symlinked or copied into extension expectations).
3. **Register desktop entry** — `.desktop` file, icon, MIME if applicable.
4. **Optional:** “Repair” command re-runs bootstrap without full reinstall.

**UX:** Wizard with **one primary path** (“Get started”) and **advanced** (override model, `--allow-slow`, etc.) mirroring CLI flags from Phase 1.

---

## 7. Launch-time behavior (every app start)

1. **Fast path:** HTTP probe `http://127.0.0.1:11434/api/tags` (or configured host/port).
2. If down *or not owned by this session:* run **ensure-Ollama** for **Lé Vibe’s managed instance** only (see §7.1).
3. **Optional refresh:** Re-evaluate model if hardware changed significantly (debounced; not every launch—e.g. weekly or on version bump).
4. **Start Code OSS** main window with extension already enabled and config paths resolved.

**Performance:** Launch must not block the UI for multi-minute pulls; **pull belongs to install/first-run**, not cold start—unless a pending update flag exists.

### 7.1 Ollama lifecycle tied to the Lé Vibe desktop app (required)

**Goal:** When the user **closes** Lé Vibe, **Ollama must stop** so GPU VRAM, CPU, and RAM used by inference are **released**—the user can “quit the heavy app” in one action. When they **open** Lé Vibe, **Ollama starts** (if not already running **for this session**).

| Event | Required behavior |
|--------|-------------------|
| **Lé Vibe process starts** | Start (or attach to) the **Lé Vibe–managed** Ollama server process; API available before or as the editor becomes usable for agent features. |
| **Lé Vibe process exits** (last window closed, quit from menu, SIGTERM from session) | **Stop** the Ollama instance that Lé Vibe started for this product—not necessarily every `ollama` on the machine (see §7.2). |

**Rationale:** A long-running `ollama serve` with loaded models can dominate VRAM and confuse users who think they “closed the IDE.” Tying start/stop to the desktop app matches user expectations for a **heavy local workload**.

**Implementation sketch (Linux):**

- **Preferred:** Lé Vibe launches a **child process** or **cgroup-scoped** `ollama serve` whose **PID (or process group) is recorded** by a small native helper or the main launcher. On exit, send **SIGTERM** to that tree, then **SIGKILL** after a timeout if needed.
- **Alternate:** Dedicated **socket/port** or **`OLLAMA_HOST`** for Lé Vibe only (e.g. `127.0.0.1:11435`) so stopping that listener never collides with a user’s separate Ollama install—extension `apiBase` must match.
- **State file:** Persist `managed_pid`, `managed_port`, and `session_id` under `~/.config/le-vibe/` for crash recovery and “orphan” detection on next launch.

### 7.2 Coexistence with a user-installed Ollama

- If **port 11434** is already serving **before** Lé Vibe starts, the app must **not** blindly kill it (another IDE or CLI may be using it).
- **Policy options (pick one for v1 and document):**
  - **A — Dedicated port (recommended):** Lé Vibe always uses **`127.0.0.1:<le-vibe-port>`** for its managed server; first-run writes that into the bundled extension config. Stopping on exit only affects that process.
  - **B — Takeover with consent:** Detect existing listener; prompt “Use existing Ollama” vs “Restart under Lé Vibe (may disrupt other apps).”
  - **C — Attach-only:** If something already listens, **do not spawn**; also **do not stop** on exit (weaker guarantee for VRAM release).

**VRAM guarantee** is only strict under **A** or a takeover that replaces the process with one we own.

### 7.3 Shutdown ordering

1. Extension / agent **stops issuing requests** (optional: brief drain).
2. **Terminate managed `ollama serve`** (SIGTERM → wait → SIGKILL).
3. **Exit** the Code OSS / Electron main process.

---


## 8. Configuration & file locations

- **Single source of truth** for “which model” should align between:
  - Phase 1 `model-decision.json` (or successor).
  - Extension YAML/JSON consumed by Continue (or chosen agent).
- **Namespacing:** Prefer `~/.config/le-vibe/` or XDG-compliant paths so we don’t clobber a user’s stock VS Code profile unless they opt in.

---

## 9. Relationship to Phase 1 (`le-vibe/`)

| Phase 1 | Phase 2 usage |
|---------|----------------|
| `bootstrap.py` | Called from installer postinst and/or Lé Vibe launcher wrapper |
| Tier / model ladder | Unchanged semantics; optionally expose in GUI |
| `output/continue-config.yaml` | Template for writing into extension config dir |
| Scripts `start_*.sh` | Reuse or fold into a single `le-vibe-ensure` binary |

**Refactor expectation:** Extract **library API** from `bootstrap.py` so the desktop app calls `ensure_stack()` without shelling to CLI only—CLI remains for power users.

---

## 10. Security & policy

- **Localhost-only** Ollama by default; no accidental `0.0.0.0` exposure.
- **No silent GPU driver installs** (inherit Phase 1 safety).
- **Telemetry:** Lé Vibe should document what (if anything) is sent; default **off** or minimal for OSS norms.
- **Trademarks:** Do not use “VS Code” in product name; use “built on Code - OSS” style attribution in About.

---

## 11. Milestones (suggested)

| Milestone | Deliverable |
|-----------|-------------|
| **P2-M1** | Technical spike: Code OSS build for Debian, rebrand string + icon, `.deb` installs |
| **P2-M2** | Bundle Continue (or chosen) extension; ship default `config.yaml` from Phase 1 templates |
| **P2-M3** | Installer runs embedded bootstrap; first-run wizard |
| **P2-M4** | Launcher ensures Ollama; cold start &lt; N seconds when model already pulled |
| **P2-M4b** | **Managed Ollama lifecycle:** start on app open, **SIGTERM on app quit**; dedicated port or documented coexistence policy (§7.1–7.2) |
| **P2-M5** | Docs: build from source, license notices, community install guide |

---

## 12. Open questions

1. **Exact OSS base:** Track `vscode` upstream vs VSCodium patches—legal/rebuild complexity tradeoff.
2. **Auto-updates:** In-app vs apt repository for Lé Vibe itself.
3. **Multiple extensions:** Whether to allow a “plugin marketplace” toggle or stay single-extension for v1.
4. **Sandboxing:** Flatpak vs native `.deb` for dependency isolation.
5. **Default port for managed Ollama:** `11434` vs dedicated **Lé Vibe port** (§7.2-A) for clean stop-on-exit.

---

## 13. Success criteria (Phase 2)

- A Debian user can install Lé Vibe, complete first-run, and **chat with a local model** in the preinstalled agent UI **without running manual Ollama tutorials**.
- Relaunching Lé Vibe **starts** its managed Ollama path without manual `ollama serve`; **quitting Lé Vibe stops** that managed server so VRAM is freed (per §7.1).
- Phase 1 bootstrap rules remain **honest** about model size vs hardware.

---

## 14. In-repository snapshot (honest alignment)

This section states what **`r-vibe`** ships **today** versus the **full Phase 2 narrative** above (§2–7, milestones §11). **`docs/PRODUCT_SPEC.md`** wins on must-ship naming, **`.lvibe/`**, and **§7.2** user gate; this file’s **§7** is managed-Ollama lifecycle only.

**Must-ship roster:** The **`spec-phase2.md`** row in **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) §9** explicitly cites **§14** — use it when jumping from **PRODUCT_SPEC** to this table.

| Phase 2 theme | In this repo now | Gap / deferral |
|---------------|------------------|----------------|
| **Linux `.deb` + bootstrap** | Yes — `debian/`, `dpkg-buildpackage`, `le-vibe` package, maintainer **`README.Debian`** path | None material for Debian-first scope. |
| **Managed Ollama start/stop** | Yes — dedicated port, state under `~/.config/le-vibe/`, **`stop_managed_ollama`** when the **launcher** exits after the editor (`le_vibe/launcher.py`, `managed_ollama.py`) | Tied to **`lvibe`** process, not a separate branded IDE binary (**H6**). |
| **Single “Lé Vibe IDE” shell (Code OSS + branding)** | **`editor/vscodium`** — **VSCodium** git submodule; **`editor/le-vibe-overrides/`** — placeholder for Lé Vibe–only layers; IDE **CI** (layout gate, **`bash -n`**, **`.nvmrc`** sync, PR paths); **`./editor/smoke.sh`** — same gate locally. **`LE_VIBE_EDITOR`** still points at **VSCodium**/system until a **Lé Vibe–branded** binary exists | **Branding** wired into the build (icons, About, product name — **§7.2** where material), automated **get_repo**/**build**, **Linux** artifacts — **H6** — `docs/vscodium-fork-le-vibe.md`, **`editor/README.md`**, **`editor/BUILD.md`**, **`editor/VENDORING.md`** |
| **Flatpak / AppImage** | **No** manifests in-tree | **H7** — `docs/flatpak-appimage.md` (**SKIPPED** here by policy). |
| **Install-time wizard / embedded extension** | Partial — first-run and Continue config follow Phase 1 + docs; **pin** story in `docs/continue-extension-pin.md` | Full graphical wizard and **redistributing** a pinned VSIX inside the **`editor/`** build are **not** claimed here until implemented. |
| **`ensure_stack()` library API** | Incremental — CLI and launcher call Python modules; full thin-wrapper API is ongoing | Matches §9 *refactor expectation* as iterative work, not a single drop. |
| **Optional RAG / embeddings chunk file** | **Yes** — [`docs/rag/le-vibe-phase2-chunks.md`](docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview`) for retrieval pipelines | **Not** exercised by **`pytest`**; **not** a second source of truth — mirrors **§9** / **E1** / **H8** / **§14** for humans and vector indexes only; see *RAG / embeddings* at the top of this file and **[`SECURITY.md`](SECURITY.md)** *Related docs*. |

**Honesty vs CI:** In-repo **pytest** locks parts of this table that would otherwise drift silently — e.g. root **`README.md`** §7.1 (*Please continue* / **AI Pilot**) and *Tests* / **E1 mapping** substrings via **`le-vibe/tests/test_root_readme_ai_pilot_contract.py`**; **`le-vibe/README.md`** *Tests* roster vs root via **`le-vibe/tests/test_le_vibe_readme_e1_contract.py`**; bundled **session-manifest** example ↔ **`schemas/`** via **`le-vibe/tests/test_session_orchestrator.py`** (STEP 2); the pasteable Master orchestrator block in **`docs/PROMPT_BUILD_LE_VIBE.md`** via **`le-vibe/tests/test_prompt_build_orchestrator_fence.py`**; **H8** **STEP 12** / **`config.yml`** string anchors in **`.github/ISSUE_TEMPLATE/*.yml`** via **`le-vibe/tests/test_issue_template_h8_contract.py`** (not a YAML schema parse); **`docs/PRODUCT_SPEC.md`** *Prioritization* (**`./editor/smoke.sh`**, **`build-le-vibe-ide.yml`**, **`build-linux.yml`**) via **`le-vibe/tests/test_product_spec_section8.py`**; **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** checkout (**`submodules: recursive`** for **`editor/vscodium`**) via **`le-vibe/tests/test_ci_yml_submodules_contract.py`**; **`editor/le-vibe-overrides/README.md`** (**STEP 14** / **H6** pointers) via **`le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py`**. Broader **§1** (naming + user-visible **H8** **`.github/`** copy per **[`PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)**) + §5–§10 coverage lives in **`le-vibe/tests/`** and **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** (E1). Optional **`rag/...`** lines on forms and full parity of **`SECURITY`** *Related docs* / root **`README`** *Documentation index & privacy* copy remain **E1**-maintained when reporter-facing YAML or trust docs change. Navigation: **[`docs/README.md`](docs/README.md)** (*E1 / pytest*; *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **`config.yml`**, **`privacy-and-telemetry`** *E1 contract tests*), **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md)** (**STEP 1** / **STEP 12** — H8: CI / Dependabot / **ISSUE_TEMPLATE** + **`config.yml`** **`#` H8**), **[`SECURITY.md`](SECURITY.md)** (*Related docs* mirrors the same **H8** pointers), plus intros in **`SESSION_ORCHESTRATION_SPEC`** / **`AI_PILOT_AND_CONTINUE`** §4. **H6**/**H7** handoff docs (**`flatpak-appimage`**, **`vscodium-fork-le-vibe`**) add **H8** / **`.github/`** comparability notes and define their own *E1* scope (no fork/Flatpak **`pytest`** in this tree).

**Success criteria §13:** A Debian user can install the **`.deb`**, run **`lvibe`**, get managed Ollama + local model path per policy, and use **Continue** with generated config. The **Lé Vibe IDE** installable binary is produced from **`editor/`** in the **same** repository when **H6 build and release** work completes (the **VSCodium** tree may already live under **`editor/vscodium/`** before that).

---

*This document is the Phase 2 product direction; implementation tasks should be broken into issues per milestone.*
