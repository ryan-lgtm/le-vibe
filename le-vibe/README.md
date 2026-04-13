# le-vibe

Hardware-aware one-shot **launcher** for local vibe coding with [Ollama](https://ollama.com) and the [Continue](https://continue.dev) extension (Code - OSS / **Lé Vibe**, not Microsoft’s VS Code distribution). It detects your OS and hardware, installs Ollama if needed, **starts the Ollama API** on `127.0.0.1:11434` by default (platform script, then `ollama serve` if needed), picks a **best-fit** model from the DeepSeek R1 ladder (with Qwen coder fallbacks), pulls it, and writes a ready-to-import Continue config under `output/`.

For **Lé Vibe Phase 2** (managed Ollama on a dedicated port, configs under `~/.config/le-vibe/`), see the [repository README](../README.md).

**First-run (launcher):** Before the main **`lvibe …`** session, **`ensure_product_first_run`** may run once (Ollama / model bootstrap under **`~/.config/le-vibe/`**). Use **`lvibe --skip-first-run`** to open the editor without that step; **`lvibe --force-first-run`** re-runs bootstrap even when **`~/.config/le-vibe/.first-run-complete`** exists; set **`LE_VIBE_VERBOSE=1`** for more detail when bootstrap fails. On failure, **`lvibe logs`** prints the JSON Lines path and **`Live: tail -f …`** lines (**STEP 6** default); use **`lvibe logs --path-only`** for the path alone or **`lvibe logs --tail 50`** for recent **`first_run`** / **`managed_ollama`** lines (adjust N; STEP 6 — same section as *Observability* below). **`lvibe --help`** lists the same first-run / diagnostics strings (**`argparse`** on **`--skip-first-run`** / **`--force-first-run`**, **`LE_VIBE_VERBOSE`**, **`lvibe logs`** — path + **`Live: tail -f`**, **STEP 6**) — [`le_vibe/launcher.py`](le_vibe/launcher.py). After bootstrap, the launcher may print the one-time terminal **`WELCOME_BANNER`** (same first-run / **`lvibe --help`** / logs pointers) — [`le_vibe/welcome.py`](le_vibe/welcome.py); **`tests/test_product_spec_section8.py`** (`test_welcome_banner_matches_product_spec_section4`). Implementation — **`le_vibe.first_run`**; tests — **`tests/test_first_run.py`**. **§10 acceptance** (first-run vs observability) — [`../docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](../docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md) §10 table + *Last verified*.

**Authority:** Must-ship behavior — [`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md). Phase 1/2 specs — [`../spec.md`](../spec.md), [`../spec-phase2.md`](../spec-phase2.md). **Optional RAG / embeddings** (not canonical): [`../docs/rag/le-vibe-phase2-chunks.md`](../docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview`) — see **`spec-phase2.md`** *RAG / embeddings*. PM session & orchestration — [`../docs/SESSION_ORCHESTRATION_SPEC.md`](../docs/SESSION_ORCHESTRATION_SPEC.md), [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md). Maintainer doc index (Roadmap **H1–H8**) — [`../docs/README.md`](../docs/README.md) (**`PRODUCT_SPEC` §9** *Maintainer index*).

**Alternate bundles / H7 (STEP 13):** Flatpak + AppImage templates — [`../docs/flatpak-appimage.md`](../docs/flatpak-appimage.md) (`packaging/flatpak/`, `packaging/appimage/`). **`lvibe flatpak-appimage`** lists those paths from a monorepo checkout (**`--path-only doc`** / **`flatpak`** / …; **`--json`** for **`monorepo_root`**, per-file **`exists`**, **`all_present`**).

**Trust / H8 — product surface (STEP 12):** [`../SECURITY.md`](../SECURITY.md) (*Related docs* — **`docs/README`** *Product surface* / **ISSUE_TEMPLATE** optional **`rag/...`*); [`../docs/privacy-and-telemetry.md`](../docs/privacy-and-telemetry.md) (*E1 contract tests* row); [`../docs/README.md`](../docs/README.md) *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** ([`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) **`#` H8** lines; same chain as root [`README.md`](../README.md) *Documentation index & privacy*). **`lvibe product-surface`** lists those paths from a monorepo checkout (**`--path-only ci`** / **`dependabot`** / … for one file; **`--json`** for **`monorepo_root`**, per-file **`exists`**, and **`all_present`**).

**PM session (STEP 2):** Canonical manifest — [`../schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json). After **§5** consent, workspace prepare runs **`le_vibe.session_orchestrator.ensure_pm_session_artifacts`**, which seeds **`.lvibe/session-manifest.json`** from the repo **`schemas/`** file when running from a clone (**`session_manifest_example_source_path`**), otherwise from the bundled copy (kept identical by **`tests/test_session_orchestrator.py`**). Hooks: **`apply_opening_skip`** (API) / **`lvibe apply-opening-skip`** (CLI), **`resolve_next_step_after_opening_skip`**, **`iter_tasks_in_epic_order`**. Spec — [`../docs/SESSION_ORCHESTRATION_SPEC.md`](../docs/SESSION_ORCHESTRATION_SPEC.md).

**Continue (STEP 3 / E2):** **`le_vibe.continue_workspace`** writes **`.continue/rules/`** so Chat/Agent treats **`.lvibe/`** as primary memory (session manifest + **`agents/*/skill.md`**). **`lvibe continue-rules`** seeds those rules without launching the editor (idempotent). Re-sync agent skills after a Lé Vibe upgrade — **`lvibe sync-agent-skills`** from the workspace root (same behavior as [`../packaging/scripts/sync-lvibe-agent-skills.sh`](../packaging/scripts/sync-lvibe-agent-skills.sh); both idempotent).

**In-editor welcome (STEP 4 / E3):** **`le_vibe.editor_welcome`** seeds **`.lvibe/WELCOME.md`** from **`templates/lvibe-editor-welcome.md`** (**`docs/PRODUCT_SPEC.md`** §4). **`lvibe welcome`** prints the welcome file path, or **`--text`** for the full §4 copy on the terminal (no editor). **`lvibe open-welcome`** opens that file in the resolved editor (same order as the main launcher: **`LE_VIBE_EDITOR`**, then packaged IDE, then system **`codium`**) without starting Ollama. Tests — **`tests/test_editor_welcome.py`**, **`tests/test_launcher_open_welcome.py`**, **`tests/test_launcher_welcome_cmd.py`**.

**Maintainer hygiene (STEP 5 / E4):** **`lvibe hygiene`** (same as **`python3 -m le_vibe.hygiene`** or **`lvibe-hygiene`** from the stack **`.deb`**) validates **`manifest.yaml`**, **`session-manifest.json`** (**`session-manifest.v1`** vs **`schemas/session-manifest.v1.example.json`**), **`storage-state.json`** (**§5.4** / **`lvibe-storage-state.v1`** when present), chunk **`path:`** refs under **`.lvibe/chunks/`** and **`.lvibe/rag/`**, and warns on oversized **`memory/incremental.md`**. Use **`--json`** for machine-readable **`errors`** / **`warnings`** (and optional **`seed`** lines with **`--seed-missing`**). Use **`--seed-missing`** to copy a missing session manifest from the canonical example and fill missing **`agents/*/skill.md`** without overwriting existing files. See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **5**.

**Observability (STEP 6 / E5):** Local-only **JSON Lines** at **`~/.config/le-vibe/le-vibe.log.jsonl`** — **`le_vibe.structured_log`** (**`append_structured_log`**) records **`managed_ollama`**, **`first_run`**, **`launcher`**, and **`workspace`** events. Set **`LE_VIBE_STRUCTURED_LOG=0`** to disable. **`lvibe logs`** prints the path (and optional **`--tail N`**); **`lvibe logs --path-only`** is script-friendly; **`lvibe logs --json`** prints path, enabled flag, line count, and first/last **`ts`** when lines are valid JSON. Operator notes — root [`README.md`](../README.md) *Operator troubleshooting & observability*; privacy — [`../docs/privacy-and-telemetry.md`](../docs/privacy-and-telemetry.md). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **6**.

**Continue / Open VSX pin (STEP 7 / H4):** Reproducible **`continue.continue@<semver>`** — [`../packaging/continue-openvsx-version`](../packaging/continue-openvsx-version) (installed as **`/usr/share/le-vibe/continue-openvsx-version`**). **`lvibe continue-pin`** prints the pinned semver (**`--path-only`** for the file path; **`--json`** for **`pin_file`**, **`semver`**, **`openvsx_id`**); override with **`LE_VIBE_CONTINUE_PIN_FILE`** (same as [`../packaging/scripts/install-continue-extension.sh`](../packaging/scripts/install-continue-extension.sh)). Install via that script (uses **`LE_VIBE_EDITOR`**, defaulting to **`/usr/lib/le-vibe/bin/codium`** when **`le-vibe-ide`** is installed, then system **`codium`**). Verify the pin — [`../packaging/scripts/verify-continue-pin.sh`](../packaging/scripts/verify-continue-pin.sh). Maintainer spec — [`../docs/continue-extension-pin.md`](../docs/continue-extension-pin.md). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **7**.

**Release channel / checksums (STEP 8 / H1):** Publishing **`le-vibe`** **`.deb`** beyond ad-hoc copies — [`../docs/apt-repo-releases.md`](../docs/apt-repo-releases.md) (**GitHub Actions** artifact **`le-vibe-deb`** — stack **`le-vibe`** **`.deb`** only; **full product (STEP 14 / §7.3):** attach **`le-vibe-ide_*_amd64.deb`** alongside when you have it — *IDE package* subsection in that doc, **`SHA256SUMS`**; **[`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md)** *H1 vs §7.3 .deb bundles*). After extracting artifacts, **`lvibe verify-checksums -C <dir>`** runs **`sha256sum -c SHA256SUMS`** (requires **`sha256sum`** on **`PATH`**); **`--json`** prints **`directory`**, **`sha256sums_path`**, **`exit_code`**, captured **`sha256sum`** output, and **`ok`** for automation. Version source — [`../debian/changelog`](../debian/changelog); user-facing notes — [`../CHANGELOG.md`](../CHANGELOG.md). Workflow — [`../.github/workflows/ci.yml`](../.github/workflows/ci.yml). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **8**.

**Supply chain / SBOM (STEP 9 / H2):** **`pip-audit`** + CycloneDX **`le-vibe-python.cdx.json`** (in **`le-vibe-deb`** with **`SHA256SUMS`**) — [`../docs/sbom-signing-audit.md`](../docs/sbom-signing-audit.md). **`lvibe pip-audit`** runs **`pip-audit -r le-vibe/requirements.txt`** when **`pip-audit`** is installed (git clone only — the stack **`.deb`** omits **`requirements.txt`**); **`--json`** prints **`requirements_path`**, extra args, **`exit_code`**, captured stdout/stderr, and **`ok`**. Python pins — [`requirements.txt`](requirements.txt). Dependabot — [`../.github/dependabot.yml`](../.github/dependabot.yml) (**H8** index). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **9**.

**QA CI (STEP 10 / H3):** Lintian-style ordering and **Smoke QA** — [`../docs/ci-qa-hardening.md`](../docs/ci-qa-hardening.md); entrypoints [`../packaging/scripts/ci-smoke.sh`](../packaging/scripts/ci-smoke.sh) → **`pytest`**, then [`../packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh) vs **[`../editor/smoke.sh`](../editor/smoke.sh)** (**14.e / 14.f**). From any directory, **`lvibe ci-smoke`** / **`lvibe ci-editor-gate`** locate the monorepo (walk parents or **`LE_VIBE_REPO_ROOT`**) and run the same scripts; **`--json`** prints **`monorepo_root`**, script path, args, **`exit_code`**, captured stdout/stderr, and **`ok`**. Workflow — [`../.github/workflows/ci.yml`](../.github/workflows/ci.yml). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **10**.

**Brand assets (STEP 11 / H5):** Icon + screenshot handoff — [`../docs/brand-assets.md`](../docs/brand-assets.md); scalable app icon — [`../packaging/icons/hicolor/scalable/apps/le-vibe.svg`](../packaging/icons/hicolor/scalable/apps/le-vibe.svg). **`lvibe brand-paths`** prints monorepo and/or packaged **`le-vibe.svg`** paths (**`--path-only`** for one path; **`--json`** for **`monorepo_svg`**, **`packaged_svg`**, **`chosen_for_scripts`**, **`ok`**). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **11**.

**Alternate packages / Flatpak & AppImage (STEP 13 / H7):** In-tree templates — **[`../packaging/flatpak/org.le_vibe.Launcher.yml`](../packaging/flatpak/org.le_vibe.Launcher.yml)** (rough target **Flathub**), **[`../packaging/appimage/`](../packaging/appimage/)** — [`../docs/flatpak-appimage.md`](../docs/flatpak-appimage.md) (**`spec-phase2.md` §14**). **`lvibe flatpak-appimage`** exposes the same table (**`--json`** or **`--path-only`** keys). Supported baseline Linux ship remains the **`.deb`**. See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **13**.

**`.lvibe/` governance (STEP 15):** Consent before workspace memory, **50 MB** default cap (user-set), per-agent subtrees + shared **`rag/`**, compaction (**§5.5** order) — **`le_vibe.workspace_consent`**, **`workspace_policy`**, **`workspace_storage`**, **`workspace_hub`** ([`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md) §5.1–5.6). **`lvibe workspace-governance`** (**`-C` / `--workspace`**) prints consent, effective cap (including **`LE_VIBE_LVIBE_CAP_MB`**), live **`.lvibe/`** usage vs cap, and **`storage-state.json`** when present (**`--json`** for automation). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **15**.

**PM map & master orchestrator (STEP 16):** Doc-locked queue — [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md); master prompt — [`../docs/PROMPT_BUILD_LE_VIBE.md`](../docs/PROMPT_BUILD_LE_VIBE.md); extract — [`../packaging/scripts/print-master-orchestrator-prompt.py`](../packaging/scripts/print-master-orchestrator-prompt.py) (same fence as **`lvibe master-orchestrator --print`** / **`--json`**). Optional manifest hints — [`../schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json) **`meta.continue_construction_note`** / **`meta.ai_pilot_note`** ([`../docs/SESSION_ORCHESTRATION_SPEC.md`](../docs/SESSION_ORCHESTRATION_SPEC.md)).

**AI Pilot & Continue contracts (STEP 17):** Doc-first staging and mimic UX — [`../docs/AI_PILOT_AND_CONTINUE.md`](../docs/AI_PILOT_AND_CONTINUE.md); **`le_vibe.continue_workspace`** + root [`README.md`](../README.md) §7.1. **`lvibe ai-pilot-continue`** lists those paths from a monorepo checkout (**`--path-only doc`** / **`continue`** / **`readme`**; **`--json`** for **`all_present`**). See [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md) STEP **17**.

**Packaging PM track:** **[`../docs/PM_DEB_BUILD_ITERATION.md`](../docs/PM_DEB_BUILD_ITERATION.md)** — one-shot **`le-vibe`** / optional **`le-vibe-ide`** **`.deb`** via [`../packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh); lazy prompt — [`../packaging/scripts/print-pm-deb-build-prompt.py`](../packaging/scripts/print-pm-deb-build-prompt.py). **IDE settings / workflows (PM phase):** [`../docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md`](../docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md); example schema — [`../schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json); §4 contracts — **`tests/test_pm_ide_settings_workflows_contract.py`**, **`tests/test_le_vibe_settings_extension_contract.py`**, **`tests/test_user_settings.py`**, **`tests/test_workspace_policy.py`**, **`tests/test_api_ollama_user_settings_contract.py`**.

**Phase 2 vs this tree:** [`../spec-phase2.md`](../spec-phase2.md) **§14** — **monorepo:** **`le-vibe/`** (this package) + **[`../editor/`](../editor/)** (Lé Vibe IDE shell, **H6**); **H7** — **`packaging/flatpak/`** + **`packaging/appimage/`** per [`../docs/flatpak-appimage.md`](../docs/flatpak-appimage.md).

**IDE shell (H6):** **[`../editor/README.md`](../editor/README.md)** — local build **[`../editor/BUILD.md`](../editor/BUILD.md)**; upstream vendoring **[`../editor/VENDORING.md`](../editor/VENDORING.md)**; CI parity without compiling Electron — **[`../editor/smoke.sh`](../editor/smoke.sh)** from the repository root (**[`../docs/ci-qa-hardening.md`](../docs/ci-qa-hardening.md)** *IDE smoke* vs **`ci-smoke.sh`**). **`./editor/smoke.sh --help`** prints **`ci-editor-gate`** usage (arguments are forwarded). **Fresh clone (14.b):** from the monorepo root run **`git submodule update --init editor/vscodium`** when **`editor/vscodium/`** is empty — same pointer as **`editor/README.md`** *Fresh clone (14.b)*.

**Honesty (14.d):** that fast **`ci-editor-gate`** / **`./editor/smoke.sh`** path validates vendoring + scripts only — not Lé Vibe–visible IDE branding. Staging map **[`../editor/le-vibe-overrides/branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md)** — read *PRODUCT_SPEC §7.2 (read before overrides)* first ([**`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.2); **[`../editor/README.md`](../editor/README.md)** *14.c vs 14.d*; repository **[`../README.md`](../README.md)** *CI*.

**Production install (STEP 14 / §7.3):** After a full **`editor/vscodium`** compile produces **`VSCode-linux-*`**, **[`../packaging/scripts/build-le-vibe-ide-deb.sh`](../packaging/scripts/build-le-vibe-ide-deb.sh)** emits **`le-vibe-ide`** **`.deb`** under **`packaging/`** (then **`apt install`** both **`le-vibe`** and **`le-vibe-ide`** **`.deb`** files so **`lvibe`** resolves **`/usr/lib/le-vibe/bin/codium`**). **`lvibe ide-prereqs`** lists packaging paths and **`[MISSING]`** until **`VSCode-linux-*`** exists (**`--path-only vscode`** / **`branding`** / **`vsc-linux-svg`** / …; **`--json`** adds **`static_prereq_files_ok`**, **`vscodium_linux_svg_staged`**, **`vscode_linux_ready`**, and per-path **`entries`** with **`exists`** flags). Maintainer flow — **[`../packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)**; stack + IDE in one shot — **[`../packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh)** **`--with-ide`**, which prints a **Full-product install** line on success — **[`../docs/PM_DEB_BUILD_ITERATION.md`](../docs/PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); close-out gate: **`../packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (optional **`--apt-sim`**, **`--json`**; **`apt_sim_note`** — same doc *`--json` close-out payload*); releases / checksums for both **`.deb`** files — **[`../docs/apt-repo-releases.md`](../docs/apt-repo-releases.md)** (*IDE package*, *Maintainer build output*). **Ordering:** **build machine** close-out, **test host** install/smoke — same doc (*IDE package*). **Partial VSCode-linux triage** — **[`../editor/BUILD.md`](../editor/BUILD.md)** (*Partial tree*), **[`../docs/PM_DEB_BUILD_ITERATION.md`](../docs/PM_DEB_BUILD_ITERATION.md)** (*Partial VSCode-linux tree*), **`../editor/print-built-codium-path.sh`**, **`../editor/print-vsbuild-codium-path.sh`**, **`../packaging/scripts/build-le-vibe-ide-deb.sh --help`**. Owner summary — **[`../README.md`](../README.md)** *Current status*.

**Debian `.deb`:** [`../debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow, **§5** workspace consent, and **Phase 2** scope (**`docs/spec-phase2.md` §14**) on packaged Linux systems.

## Requirements

- Python 3.10+
- Windows 10/11, macOS 14+, or a Debian-based Linux (other distros often work if `curl` and Ollama’s install script succeed)
- Network access for install and model pull

## Quick start

```bash
cd le-vibe
pip install -r requirements.txt
python3 bootstrap.py
```

Non-interactive (e.g. CI):

```bash
python3 bootstrap.py --yes
```

Dry run (no install, pull, or start — still writes `output/`):

```bash
python3 bootstrap.py --dry-run
```

## CLI flags

| Flag | Purpose |
|------|---------|
| `--dry-run` | Plan only; no install, pull, or service start |
| `--force-reinstall` | Re-run the platform Ollama installer |
| `--model <tag>` | Force a model (must be sensible for hardware unless `--allow-slow`) |
| `--allow-slow` | Allow “possible but slow” tiers (e.g. 32B when the machine is borderline) |
| `--host` / `--port` | Ollama bind address (default `127.0.0.1:11434`) |
| `--le-vibe-product` | Write configs under `~/.config/le-vibe/` and use managed port **11435** (Phase 2) |
| `--yes` | Non-interactive hints for helper scripts |
| `--verbose` | Debug logging |

## Outputs

After a successful run (or `--dry-run`):

- `output/continue-config.yaml` — import into Continue (existing file is copied to `continue-config.yaml.bak`)
- `output/bootstrap-report.md` — human-readable report
- `output/model-decision.json` — machine-readable selection and rejections

## Scripts (per OS)

| Action | Linux | macOS | Windows |
|--------|-------|-------|---------|
| Install Ollama | `scripts/install_linux.sh` | `scripts/install_macos.sh` | `scripts/install_windows.ps1` |
| Start | `scripts/start_linux.sh` | `scripts/start_macos.sh` | `scripts/start_windows.ps1` |
| Stop | `scripts/stop_linux.sh` | `scripts/stop_macos.sh` | `scripts/stop_windows.ps1` |

Linux installs use the official `https://ollama.com/install.sh` script. Windows install prefers `winget` (`Ollama.Ollama`); if that fails, install manually from [ollama.com/download/windows](https://ollama.com/download/windows).

**Status checks:** `ollama list`, `curl -s http://127.0.0.1:11434/api/tags`, or `ollama --version`.

## Safety

- Does not install or replace GPU drivers without your action elsewhere.
- Binds to localhost by default; does not expose Ollama on public interfaces.
- Does not stop an already-running Ollama unless you use the stop scripts (which target user-started `ollama serve` where applicable; systemd installs may need `systemctl` — see report).

## Development

Run a dry-run to regenerate templates output:

```bash
python3 bootstrap.py --dry-run -v
```

**Tests:** From this directory, **`pytest tests/`** runs the full suite. **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](../docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** maps **§1**/**H8** + §5–§10 to modules; contract highlights include **`test_product_spec_section8.py`** (§ *Prioritization* — **`./editor/smoke.sh`** vs **`build-le-vibe-ide.yml`** / **`build-linux.yml`**; **`linux_compile`** (fail fast: **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** → **`dev/build.sh`** — **`editor/BUILD.md`** *CI*; **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** vs **`editor/.nvmrc`**, **`LEVIBE_SKIP_NODE_VERSION_CHECK`**), **`vscodium-linux-build.tar.gz`**, **`actions/cache@v4`**, **`~/.cargo`**, **`spec-phase2.md` §14**; **`ide-ci-metadata.txt`**, **`retention-days`**, **`permissions:`** **`contents: read`**, **`actions: write`**, **Pre-binary artifact**, **`editor/BUILD.md`**, **`editor/VENDORING.md`**), **`test_continue_workspace.py`** / **`test_workspace_hub.py`** (§7.2 — **`.continue/rules`** + **`.lvibe/AGENTS.md`**, **numbered questions**), **`test_session_orchestrator.py`** / **`test_session_orchestration_spec_step2_contract.py`** (**STEP 2** — **`session-manifest`** ↔ **`schemas/`**; **`SESSION_ORCHESTRATION_SPEC.md`** intro), **`test_root_readme_ai_pilot_contract.py`** (repo root **`README.md`** §7.1 + **E1** roster), **`test_prompt_build_orchestrator_fence.py`** (**`docs/PROMPT_BUILD_LE_VIBE.md`** orchestrator fence), **`test_issue_template_h8_contract.py`** (**H8** — **`.github/ISSUE_TEMPLATE/*.yml`**), **`test_ci_yml_submodules_contract.py`** (**`.github/workflows/ci.yml`** — **`submodules: recursive`** for **`ci-editor-gate`**), **`test_editor_le_vibe_overrides_readme_contract.py`** (**`editor/le-vibe-overrides/README.md`** — **H6** / **STEP 14**), **`test_build_le_vibe_ide_workflow_contract.py`** (**`build-le-vibe-ide.yml`** — **`ide-ci-metadata.txt`** **`le_vibe_editor_docs`**), **`test_editor_build_md_contract.py`** (**`editor/BUILD.md`** — STEP **14**, **`Vendoring upstream`**), **`test_editor_readme_step14_contract.py`** (**`editor/README.md`** — **14.a–14.j** vs **H6**), **`test_spec_phase2_section14_snapshot_contract.py`** (**`spec-phase2.md` §14** *Honesty vs CI* / **14.j**), **`test_continue_openvsx_pin.py`** / **`test_install_continue_extension_script.py`** (**STEP 7 / H4** — **`continue-openvsx-version`**, **`verify-continue-pin.sh`**), **`test_apt_repo_releases_doc_h1_contract.py`** / **`test_pm_stage_map_step8_contract.py`** (**STEP 8 / H1** — **`apt-repo-releases.md`**, **`le-vibe-deb`**), **`test_sbom_signing_audit_doc_h2_contract.py`** / **`test_requirements_pins.py`** / **`test_pm_stage_map_step9_contract.py`** (**STEP 9 / H2** — **`sbom-signing-audit.md`**, **`le-vibe-python.cdx.json`**), **`test_ci_qa_hardening_doc_h3_contract.py`** / **`test_ci_qa_hardening_prioritization_cargo_contract.py`** / **`test_docs_readme_ci_qa_hardening_row_contract.py`** / **`test_pm_stage_map_step10_contract.py`** (**STEP 10 / H3** — **`ci-qa-hardening.md`**, **`ci-smoke.sh`**), **`test_brand_assets_doc_h5_contract.py`** / **`test_pm_stage_map_step11_contract.py`** (**STEP 11 / H5** — **`brand-assets.md`**), **`test_pm_stage_map_step12_contract.py`** (**STEP 12 / H8** — complements **`test_issue_template_h8_contract.py`** above), **`test_flatpak_appimage_doc_h7_contract.py`** / **`test_pm_stage_map_step13_contract.py`** (**STEP 13 / H7** — **`flatpak-appimage.md`**, **SKIPPED** in-tree), **`test_workspace_consent.py`** / **`test_workspace_storage.py`** / **`test_workspace_hub.py`** / **`test_pm_stage_map_step15_contract.py`** (**STEP 15** — **`PRODUCT_SPEC` §5**), **`test_prompt_build_orchestrator_fence.py`** / **`test_pm_stage_map_step16_contract.py`** (**STEP 16** — **`PROMPT_BUILD_LE_VIBE.md`** fence), **`test_root_readme_ai_pilot_contract.py`** / **`test_privacy_and_ai_pilot_prioritization_cargo_contract.py`** / **`test_pm_stage_map_step17_contract.py`** (**STEP 17** — **`AI_PILOT_AND_CONTINUE.md`**). See the [repository README](../README.md) *Tests* section for the same roster.

```bash
pip install -r requirements.txt
pip install pytest
python3 -m pytest tests/
```
