<!--
  RAG retrieval format: each chunk is separated by a line containing only: ---
  The YAML frontmatter block is optional metadata for embedding filters.
  Copy individual chunks or index this file in a vector store.
-->

---
chunk_id: lv-meta-overview
title: Lé Vibe Phase 2 — product overview
tags: [le-vibe, phase-2, ide, linux, ollama]
source: spec-phase2.md
---

# Lé Vibe (Phase 2) — overview

**Lé Vibe** is a Debian-first Linux desktop IDE built on **Code OSS** (open-source VS Code lineage), branded as a distinct product. It ships with a preconfigured **open-source agent extension** (e.g. Continue) and integrates the **le-vibe** bootstrap stack: hardware-aware **Ollama** model selection, local API at localhost, and Continue-style YAML config.

It is a **local-first, orchestrated agentic environment** with honest model tiers and minimal manual setup.

**Cross-links:** Phase 1 bootstrap (`le-vibe/`) — **`spec.md`**; authority roster — **`docs/PRODUCT_SPEC.md` §9**; E1 regression — **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** (**§1**/**H8** + §5–§10); **H8** trust surface — **`docs/README.md`** *Product surface* (**`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`ISSUE_TEMPLATE/`** + **`config.yml`** **`#` H8**); in-repo vs fork/Flatpak — **§14** in **`spec-phase2.md`** (table row *Optional RAG / embeddings chunk file* — this **`lv-meta-overview`** chunk is **not** exercised by **`pytest`**); **`SECURITY.md`** *Related docs* lists **`docs/rag/le-vibe-phase2-chunks.md`** for discoverability.

---
chunk_id: lv-feasibility-wrapper
title: Feasibility of a Code OSS–based IDE like Cursor
tags: [feasibility, vscode-oss, licensing, electron, debian]
source: spec-phase2.md
---

# Feasibility: Lé Vibe wrapper

Shipping a **branded Code OSS distribution** with custom extensions and installers is **realistic** for Linux (e.g. `.deb`). Upstream is MIT; **do not** use “VS Code” as the product name—use **Lé Vibe** and attribute “built on Code - OSS.”

Matching every feature from other agentic editors is **not** a Phase 2 goal. Ongoing cost: merging upstream security fixes and extension API updates.

---
chunk_id: lv-platform-debian
title: Platform scope — Debian-based Linux
tags: [debian, ubuntu, packaging, deb, x86_64, arm64]
source: spec-phase2.md
---

# Platform scope

- **Primary:** Debian-based distributions (Debian, Ubuntu, Mint, Pop!_OS, etc.).
- **Package:** `.deb` first; document GTK/Electron dependencies.
- **Arch:** `x86_64` first; `arm64` when Ollama and the editor base support it.
- Windows/macOS are **out of scope** for Phase 2.0.

---
chunk_id: lv-architecture-diagram
title: High-level architecture — Lé Vibe + bootstrap + Ollama
tags: [architecture, bootstrap, continue, ollama]
source: spec-phase2.md
---

# Architecture (conceptual)

The **Lé Vibe** process contains: Code OSS shell, bundled agent extension, default settings pointing at **local Ollama**, and a **native launcher/helper** that runs **le-vibe bootstrap** logic on install and on session start.

Below that sits **Ollama** at a configured host/port (default design prefers a **Lé Vibe–managed** server). Phase 1 Python code (`le-vibe/` package) should become a **library API** (`ensure_stack`, tier selection, config generation) callable from the desktop, not only from CLI.

---
chunk_id: lv-extension-choice
title: Open-source agent extension — MVP choice
tags: [continue, cline, extension, ollama, license]
source: spec-phase2.md
---

# Agent extension (MVP)

Standardize on **one** extension for v1 to limit QA: **Continue** is a strong fit (Ollama-first, chat/edit/apply). Alternatives: Cline, others—evaluate licenses and redistribution rules.

Pin a **version range** in the build; ship license notices in the repo.

---
chunk_id: lv-install-first-run
title: Install-time and first-run behavior
tags: [install, wizard, bootstrap, ollama-pull, debian]
source: spec-phase2.md
---

# Install / first run

1. Check dependencies (Python 3, curl, etc.) or ship a static helper.
2. Run Phase 1–equivalent logic: install Ollama if missing; hardware tier → model ladder → **pull model** (heavy step belongs here, not cold launch).
3. Write extension config under an XDG path (e.g. `~/.config/le-vibe/`) and wire **apiBase** + model id.
4. Install `.desktop` entry and icons.
5. Offer **advanced** options aligned with CLI: `--model`, `--allow-slow`, etc.

---
chunk_id: lv-ollama-lifecycle-core
title: Ollama lifecycle — start when app opens, stop when app closes
tags: [ollama, lifecycle, gpu, vram, sigterm, process-management]
source: spec-phase2.md §7.1
---

# Ollama lifecycle (required behavior)

**On Lé Vibe open:** start (or attach per policy) the **Lé Vibe–managed** Ollama server so the local API is available for the agent during the session.

**On Lé Vibe quit:** **stop** the Ollama process that Lé Vibe started for this product, so **GPU VRAM and RAM** used by inference are released—users can “quit the heavy app” in one action.

**Implementation:** record **PID / process group** of the spawned `ollama serve` (or use **cgroup**). On exit: **SIGTERM**, wait, then **SIGKILL** if needed. Persist `managed_pid`, `port`, `session_id` under `~/.config/le-vibe/` for crash recovery.

**Alternate design:** dedicated **port** (e.g. not 11434) so the managed server is unambiguous and teardown never affects unrelated Ollama instances.

---
chunk_id: lv-ollama-coexistence
title: Coexistence with an existing system Ollama
tags: [ollama, port-11434, conflict, attach, dedicated-port]
source: spec-phase2.md §7.2
---

# Coexistence policy

If something already listens on **11434** before Lé Vibe starts, **do not kill it blindly** (other tools may use it).

**Recommended v1 policy (A):** Lé Vibe uses a **dedicated host:port** for its managed server; extension `apiBase` matches. Stop-on-exit only terminates **that** process.

**Alternatives:** prompt for takeover; or attach-only (no stop on exit—weaker VRAM guarantee).

---
chunk_id: lv-shutdown-order
title: Shutdown ordering — agent drain then Ollama stop
tags: [shutdown, ordering, extension, sigterm]
source: spec-phase2.md §7.3
---

# Shutdown ordering

1. Stop or drain in-flight **agent/extension** requests where possible.
2. Terminate the **managed `ollama serve`** process tree.
3. Exit the **main IDE process**.

This reduces corrupted state and avoids hung GPU contexts when possible.

---
chunk_id: lv-config-paths
title: Configuration paths and single source of truth
tags: [xdg, config, model-decision.json, continue-yaml]
source: spec-phase2.md
---

# Configuration

Use **XDG**-style paths such as `~/.config/le-vibe/` for:

- `model-decision.json` (or successor) from tier logic.
- Extension config (Continue YAML) with **apiBase** and **model** id.
- Optional `managed_ollama.json` with PID/port for lifecycle.

Avoid overwriting a user’s stock VS Code profile unless they opt in; Lé Vibe should use a **distinct data dir** or profile when the Code OSS fork supports it.

---
chunk_id: lv-phase1-integration
title: Relationship to Phase 1 repository (le-vibe bootstrap)
tags: [bootstrap.py, le_vibe, python, refactor, cli]
source: spec-phase2.md
---

# Phase 1 integration

The existing **`le-vibe/`** tree provides: `bootstrap.py`, `le_vibe/` package (detect hardware, tier scoring, model ladder, `start_ollama_service`, templates, `output/`).

Phase 2 should **import** this as a library (`ensure_stack`, `ensure_ollama_managed`, etc.) from the desktop launcher. The **CLI** remains for power users.

**Change:** Phase 1 currently assumes long-running Ollama; Phase 2 adds **session-scoped start/stop** and possibly a **dedicated port**—refactor bootstrap to accept **managed mode** parameters.

---
chunk_id: lv-security-trademark
title: Security, telemetry, and trademarks
tags: [localhost, telemetry, trademark, code-oss]
source: spec-phase2.md
---

# Security and policy

- Bind Ollama to **127.0.0.1** by default; never expose on `0.0.0.0` without explicit opt-in.
- Do not silently install GPU drivers.
- **Telemetry:** default off or minimal; document clearly.
- **Trademarks:** product name **Lé Vibe**; attribute Code - OSS upstream in About.

---
chunk_id: lv-milestones
title: Phase 2 milestones (including Ollama lifecycle)
tags: [milestones, deb, continue, lifecycle]
source: spec-phase2.md
---

# Milestones (summary)

- **M1:** Code OSS spike for Debian; rebrand; `.deb` installs.
- **M2:** Bundle pinned agent extension; default config from Phase 1 templates.
- **M3:** Installer + first-run wizard calling bootstrap.
- **M4:** Fast launch when model already pulled.
- **M4b:** **Managed Ollama:** start on open, **stop on quit**; dedicated port or documented coexistence.
- **M5:** Docs, licenses, community install guide.

---
chunk_id: lv-success-criteria
title: Success criteria — Phase 2 acceptance
tags: [acceptance, ollama, debian, agent]
source: spec-phase2.md
---

# Success criteria

- Debian user completes install/first-run and can **chat with a local model** in the bundled agent UI without manual Ollama tutorials.
- **Opening** Lé Vibe brings up the managed stack; **closing** Lé Vibe **stops** the managed Ollama server and frees heavy resources (per coexistence policy).
- Model tier remains **honest** vs hardware (Phase 1 rules).

---
chunk_id: lv-in-repo-snapshot
title: Phase 2 — in-repository snapshot vs full narrative
tags: [spec-phase2, h6, h7, deb, launcher, honesty]
source: spec-phase2.md §14
---

# In-repo snapshot (honest alignment)

**`r-vibe`** ships: **`.deb`**, **`lvibe`** launcher, managed Ollama on a **dedicated port** with **stop on launcher exit**, Phase 1 bootstrap, **`.lvibe/`** per **PRODUCT_SPEC**, Continue templates/pins. **Not** in this tree: branded Code OSS binary only (**H6**), Flatpak/AppImage manifests (**H7** SKIPPED). First-run may be CLI/zenity vs full GUI wizard; **`ensure_stack()`** API is iterative. Marketing and screenshots must not claim a fork-only deliverable from this repo alone — cite **spec-phase2 §14** table.

**Roster:** **`docs/PRODUCT_SPEC.md` §9** lists **`spec-phase2.md`** with **§14** called out so this snapshot stays discoverable from the must-ship authority table.
