# Lé Vibe

**One repository, one product (monorepo):** **`le-vibe/`** — bootstrap, **`lvibe`** launcher, managed **Ollama**, **`.lvibe/`** workspace hub, **`le-vibe`** **`.deb`**; **`editor/`** — **Lé Vibe IDE** (Code - OSS–based desktop app; vendored build per [`docs/vscodium-fork-le-vibe.md`](docs/vscodium-fork-le-vibe.md)). It is **not** “Visual Studio Code”; attribute the editor as **Code - OSS** in About and docs.

Canonical specs: **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** (must-ship product requirements), [`spec.md`](spec.md) (Phase 1 bootstrap), [`spec-phase2.md`](spec-phase2.md) (Phase 2 IDE direction, managed Ollama lifecycle, `.deb` — honest **in-repo** vs deferred scope in **§14**, **H6**/**H7**). **Optional RAG / embeddings** (not canonical): [`docs/rag/le-vibe-phase2-chunks.md`](docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview`) — see **`spec-phase2.md`** *RAG / embeddings*.

**Formal authority roster (orchestration + evidence + lazy prompts):** [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) §9.

**Phased work / lazy prompts for PM & engineering:** [`docs/PROMPT_BUILD_LE_VIBE.md`](docs/PROMPT_BUILD_LE_VIBE.md) (Master orchestrator STEPs **0–17**).

**Orchestration & regression evidence:** [`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md) (STEP → primary PM doc), [`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md) (E1 / **§1**/**H8** + §5–§10 audit; filename historic).

**Roadmap H5 (brand / screenshots):** [`docs/brand-assets.md`](docs/brand-assets.md) (**§1** naming, incl. user-visible **H8** **`.github/`** copy — *Naming (must ship)*), [`docs/screenshots/README.md`](docs/screenshots/README.md) — **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md) STEP 11**.

**Documentation index & privacy (Roadmap H8):** **[`docs/README.md`](docs/README.md)** lists maintainer guides (**Roadmap H1–H8**; **E1 / pytest** next to the formal roster; cross-linked from **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** §9 *Maintainer index*); **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)** summarizes localhost-first behavior and upstream (**Continue**, editor) policies; **[`SECURITY.md`](SECURITY.md)** covers vulnerability reporting. **[`docs/SESSION_ORCHESTRATION_SPEC.md`](docs/SESSION_ORCHESTRATION_SPEC.md)** intro documents the same **H8** trust chain (**`docs/README`** *Product surface*, **`privacy-and-telemetry`** *E1 contract tests*, **`SECURITY`** *Related docs*). **`.github/`** (per **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md) STEP 12** — *E1* when editing **[`workflows/ci.yml`](.github/workflows/ci.yml)**, **[`dependabot.yml`](.github/dependabot.yml)**, or **[`ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/)** ([`config.yml`](.github/ISSUE_TEMPLATE/config.yml) **`#` H8** maintainer lines): [`docs/README.md`](docs/README.md) *Product surface*, [`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md) §10): CI, Dependabot, issue templates (**`README.Debian`** + **`spec-phase2.md` §14** vs **H6**/**H7**; optional **`docs/rag/le-vibe-phase2-chunks.md`** on **bug**/**feature**/**documentation** intros — **`SECURITY`** *Related docs*). **`apt`** / **`.deb`:** on-disk post-install doc **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](debian/le-vibe.README.Debian)).

### Prioritization (what ships first)

**P0 — Desktop IDE:** Implement **`editor/`** — branded **Lé Vibe** Code - OSS binary (Roadmap **H6**): name, icons, About, installable artifact from **this** repo. See **[`editor/README.md`](editor/README.md)** and **[`docs/vscodium-fork-le-vibe.md`](docs/vscodium-fork-le-vibe.md)**.

**P1 — Stack:** **`lvibe`**, managed Ollama, **`le-vibe`** **`.deb`**, Continue + **`.lvibe/`** — shared config under **`~/.config/le-vibe/`**, **`LE_VIBE_EDITOR`** points at the IDE binary.

**PM / project management:** Epics, session manifests, and lazy prompts **coordinate delivery of the IDE + stack**—see **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** *Product and project management — in service of the IDE* and **[`docs/PROMPT_BUILD_LE_VIBE.md`](docs/PROMPT_BUILD_LE_VIBE.md)** (orchestrator order **0→1→14→…**).

**Interim dev:** **`editor/vscodium`** vendors **VSCodium** upstream (git submodule); a **compiled, released** Lé Vibe IDE binary is **not** automated here yet—use system **VSCodium** + **`LE_VIBE_EDITOR`**, or build locally per **`editor/README.md`**, alongside this **`le-vibe`** `.deb`.

### Monorepo layout

| Path | Contents |
|------|----------|
| **`le-vibe/`** | Python package, bootstrap, launcher, tests |
| **`editor/`** | Lé Vibe IDE — **VSCodium** at **`vscodium/`** (submodule), **`le-vibe-overrides/`** for future branding — **`docs/vscodium-fork-le-vibe.md`** |
| **`debian/`**, **`packaging/`** | Stack **`.deb`** and wrappers |

Single **git** history; release tags can cover stack + IDE drops together.

## Managed Ollama (dedicated port, §7.2-A)

Lé Vibe’s managed `ollama serve` uses a **dedicated localhost port** so quit/teardown does not kill unrelated Ollama users on the default port:

- Default **managed port:** `11435` (constant `LE_VIBE_MANAGED_OLLAMA_PORT` in `le_vibe/paths.py`).
- **State file:** `~/.config/le-vibe/managed_ollama.json` (PID, host, port, session id).
- **Continue `apiBase`** must match, e.g. `http://127.0.0.1:11435` — produced when you run bootstrap with `--le-vibe-product` (writes configs under `~/.config/le-vibe/`).

On **last-window quit**, the launcher sends **SIGTERM** to the managed process group, waits, then **SIGKILL** if needed, and removes the state file — **VRAM and RAM used by inference are released** when you exit Lé Vibe.

### Model policy (must-ship)

Lé Vibe picks a **concrete Ollama model tag** for **this machine** using the hardware **tier** ladder (RAM, VRAM, disk—honest limits, no “always 70B” marketing). The chosen tag is **persisted** as the product lock so upgrades do not silently change your default: see **`~/.config/le-vibe/locked-model.json`** (and **`model-decision.json`** for rationale). Continue’s generated YAML uses that same tag—**not** `AUTODETECT` as the only stored value when a tag is known.

### PM session manifest (workspace `.lvibe/`)

On workspace prepare (e.g. **`lvibe .`**), after **consent** for local workspace memory ([**`docs/PRODUCT_SPEC.md`**](docs/PRODUCT_SPEC.md) §5), Lé Vibe seeds **`.lvibe/session-manifest.json`** from the bundled example (same shape as **[`schemas/session-manifest.v1.example.json`](schemas/session-manifest.v1.example.json)**) when missing, and copies skill agents into **`.lvibe/agents/<agent_id>/skill.md`** from **`le-vibe/templates/agents/`** when each file is missing. The Python API exposes **`session_steps`**, **`product.epics` / tasks** iteration, and **`apply_opening_skip(...)`** for the **opening_intent → skip → workspace_scan** hook described in **[`docs/SESSION_ORCHESTRATION_SPEC.md`](docs/SESSION_ORCHESTRATION_SPEC.md)** (`le_vibe.session_orchestrator`).

**Continue (workspace):** after **`le-vibe-setup-continue`** (global **`~/.continue/config.yaml`** → Lé Vibe YAML), the assistant still needs **project** context: Lé Vibe writes **`.continue/rules/`** rules on first open—**`00-le-vibe-lvibe-memory.md`** (anchor on **`.lvibe/`**) and **`01-le-vibe-product-welcome.md`** (PRODUCT_SPEC §4 positioning for in-editor Chat/Agent)—per **[Continue rules](https://docs.continue.dev/customize/rules)**. **`le_vibe.continue_workspace`**. **In-editor welcome:** **`lvibe .`** also seeds **`.lvibe/WELCOME.md`** from **`le-vibe/templates/lvibe-editor-welcome.md`** (`le_vibe.editor_welcome`).

### Please continue & AI Pilot (§7.1)

- **Please continue** — Resume construction from the **current** PM state: **`.lvibe/session-manifest.json`** (`session_steps`, **`product.epics`** / tasks) and **`.lvibe/`** RAG—not a blank restart. Intent and guards: **[`docs/AI_PILOT_AND_CONTINUE.md`](docs/AI_PILOT_AND_CONTINUE.md)**.
- **AI Pilot** — Sustained, coordinated advancement (mimicked in Cursor by re-pasting the **self-coordinating engineer** loop in **[`docs/PROMPT_BUILD_LE_VIBE.md`](docs/PROMPT_BUILD_LE_VIBE.md)**). **§5** consent/storage and **§8** secrets still apply; doc authority per stage: **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md)**.

### User gate (§7.2)

On **material** product or architecture choices—or **unresolved disagreement** between roles—the orchestrator **halts** and shows **`USER RESPONSE REQUIRED`** (all capitals) with **numbered questions**; **No preference** / **your call** counts as delegation. Protocol: **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** §7.2, **[`docs/SESSION_ORCHESTRATION_SPEC.md`](docs/SESSION_ORCHESTRATION_SPEC.md)** §5.1. Workspace rules under **`.continue/rules/`** restate this for Continue.

### Maintainer: `.lvibe/` hygiene (`lvibe-hygiene`)

Run from the **workspace root** when **`.lvibe/`** exists (after **`lvibe .`** with **§5** consent **accept**): **`lvibe-hygiene`** (on `PATH` from the `.deb`) or **`python3 -m le_vibe.hygiene`** with **`PYTHONPATH`** set to the **`le-vibe/`** tree in development. Checks **`manifest.yaml`** sanity, **`session-manifest.json`** structure, skill paths under **`agents/`**, **`path:`** references in **`chunks/*.yaml`**, and warns if **`memory/incremental.md`** grows large. Exit code **0** = no errors (warnings may print to stderr), **1** = validation errors. Implementation: **`le_vibe.hygiene`**.

## Install (development tree)

```bash
cd le-vibe
pip install -r requirements.txt
```

**Phase 1–style bootstrap** (default Ollama port `11434`, outputs under `le-vibe/output/`):

```bash
python3 bootstrap.py --yes
```

**Lé Vibe product paths** (configs + model decision under `~/.config/le-vibe/`, managed port **11435**):

```bash
python3 bootstrap.py --yes --le-vibe-product
```

**Launcher** (starts managed Ollama, then your editor; stops Ollama on exit):

```bash
# After install — open the editor in the current folder (default CLI name: lvibe):
lvibe .

# From repo `le-vibe/` tree:
./scripts/le-vibe-launch.sh --editor codium
# or
export PYTHONPATH="$PWD"
python3 -m le_vibe.launcher --editor /path/to/code-oss
```

Set **`LE_VIBE_EDITOR`** to the Code - OSS / VSCodium binary if you do not pass `--editor`.

### First-run (production path)

On **first launch**, `le_vibe.launcher` runs **`ensure_product_first_run`** (unless `--skip-first-run`): Ollama install if needed, hardware tier, **model pull** (can take a long time), writes `~/.config/le-vibe/continue-config.yaml` and marks **`~/.config/le-vibe/.first-run-complete`**. Later launches skip that step and only start managed Ollama.

- **`LE_VIBE_ASSUME_YES`** — default `1` for non-interactive install hints; set to `0` if you need interactive Ollama installers.
- **`LE_VIBE_VERBOSE`** — set to `1` for debug logging during first-run.
- **`--force-first-run`** — re-run bootstrap even if the marker exists (launcher).
- **Continue (one command after first-run):** with VSCodium installed, run **`le-vibe-setup-continue`** (on `PATH` from the `.deb`, or `packaging/bin/le-vibe-setup-continue` in a dev tree). It runs **sync** then **extension install** with explicit exit codes:
  - **0** — success  
  - **1** — no `~/.config/le-vibe/continue-config.yaml` yet (run **`le-vibe`** first)  
  - **2** — config sync failed  
  - **3** — extension install failed (network / marketplace / id)  
  - **4** — no editor binary (`LE_VIBE_EDITOR` / `codium`)  
  - **125** — unknown CLI option (see **`--help`**)  
  - **127** — helper scripts missing, or **`--gui`** without **zenity** on `PATH`  

  Optional **desktop prompt (Roadmap G-A2):** after first-run, **`le-vibe-setup-continue --gui`** uses **Zenity** (install `zenity` or use the package `Suggests`) to confirm before syncing and installing the extension; cancel exits **0**.

  Optional **one-shot reminder (Roadmap G-A3):** the package installs **`/etc/xdg/autostart/le-vibe-continue-setup.desktop`**, which runs once per user (after `~/.config/le-vibe/continue-config.yaml` exists and **`~/.continue/config.yaml`** is not yet linked) and sends a **`notify-send`** hint if **`libnotify-bin`** is installed. Opt out permanently: **`touch ~/.config/le-vibe/.continue-setup-autostart-disable`**, or disable the entry in your session’s autostart settings.

  Advanced: run [`packaging/scripts/sync-continue-config.sh`](packaging/scripts/sync-continue-config.sh) and [`packaging/scripts/install-continue-extension.sh`](packaging/scripts/install-continue-extension.sh) separately; default extension id **`continue.continue`**. **Roadmap H4:** pin file **[`packaging/continue-openvsx-version`](packaging/continue-openvsx-version)** + validator **[`packaging/scripts/verify-continue-pin.sh`](packaging/scripts/verify-continue-pin.sh)** (also enforced by pytest + CI smoke). Override with **`LE_VIBE_CONTINUE_OPENVSX_VERSION=latest`** or **`LE_VIBE_CONTINUE_EXTENSION`** — see **[`docs/continue-extension-pin.md`](docs/continue-extension-pin.md)**.

## Python API (importable)

```python
from le_vibe import (
    EnsureBootstrapArgs,
    ensure_bootstrap,
    ensure_managed_ollama,
    ensure_product_first_run,
    stop_managed_ollama,
    le_vibe_config_dir,
    LE_VIBE_MANAGED_OLLAMA_PORT,
)

# First-run / installer (or call ensure_product_first_run() wrapper).
code, state = ensure_bootstrap(
    EnsureBootstrapArgs(
        port=LE_VIBE_MANAGED_OLLAMA_PORT,
        config_dir=le_vibe_config_dir(),
        yes=True,
        use_managed_ollama=True,
    )
)

# Each app session: start managed server only for Lé Vibe.
ok, msg, st = ensure_managed_ollama()
# On quit:
stop_managed_ollama()
```

## Debian package (skeleton)

Source layout includes `debian/` and `packaging/` for a native `.deb` build that installs the Python tree under `/usr/share/le-vibe` and `/usr/bin/le-vibe`. The **Code - OSS / Electron build is not bundled** in this v0 skeleton; point `LE_VIBE_EDITOR` at an upstream build or replace the stub in CI.

Editor check for CI/smoke [`packaging/scripts/fetch-code-oss-artifact.sh`](packaging/scripts/fetch-code-oss-artifact.sh): **exits 0** if **`/usr/bin/codium`** is executable or **`codium`** is on `PATH`; otherwise prints install hints and exits 1. The launcher defaults to **`/usr/bin/codium`** when that file exists (override with **`LE_VIBE_EDITOR`**).

```bash
# From repository root (with build tools: debhelper, dpkg-dev, fakeroot)
dpkg-buildpackage -us -uc -b
```

After install, **`man le-vibe`** and **`man le-vibe-setup-continue`** document the launcher and Continue setup (both ship in the `.deb`).

**Flatpak / AppImage (Roadmap H7):** Optional alternate bundles are **not** built in this repo by default; they need their own manifest pipeline (sandbox permissions, Ollama on the host, editor side-by-side). Maintainer outline: **[`docs/flatpak-appimage.md`](docs/flatpak-appimage.md)**.

## CI

On **GitHub**, pushes and PRs to `main` / `master` run [`.github/workflows/ci.yml`](.github/workflows/ci.yml): **[`packaging/scripts/ci-smoke.sh`](packaging/scripts/ci-smoke.sh)** (full **`le-vibe/tests/`** **`pytest`**, incl. **`test_issue_template_h8_contract.py`** for **H8** / **STEP 12**, + **`desktop-file-validate`**), **`dpkg-buildpackage`**, **lintian** (**fails on policy errors**), supply-chain steps, and upload of the built **`.deb`** and related artifacts. You can also run the workflow **manually** (**Actions → CI → Run workflow**). Overlapping runs on the same branch cancel in progress (concurrency). The job **times out after 30 minutes** to avoid stuck runners.

**Lé Vibe IDE (Roadmap H6, STEP 14):** the **stack** job above does **not** compile the **Electron** editor. **[`build-le-vibe-ide.yml`](.github/workflows/build-le-vibe-ide.yml)** (and optional manual **[`build-linux.yml`](.github/workflows/build-linux.yml)**) check out **`editor/vscodium`**, run layout/metadata smoke and script syntax checks, and upload small **metadata** artifacts. **Local parity:** from the repo root, **`./editor/smoke.sh`** runs the same gate when the submodule is present—see **`editor/README.md`** and **`docs/ci-qa-hardening.md`**.

**Lintian:** CI uses **`lintian --fail-on error`** so **errors** block the job; **warnings** (e.g. maintainer placeholder) still print but do not fail until you raise **`--fail-on`** or fix the tags.

**Roadmap H3:** Smoke script (**`verify-continue-pin`**, **`bash -n`** on **`packaging/bin`**, synthetic **`lvibe-hygiene`**, full **`pytest`** suite, **`.desktop`**), CI **lintian** flags, and why full GUI E2E is not in default CI: **[`docs/ci-qa-hardening.md`](docs/ci-qa-hardening.md)**.

**Dependabot:** [`.github/dependabot.yml`](.github/dependabot.yml) opens weekly PRs to bump **GitHub Actions** versions and **`le-vibe/requirements.txt`** (pip). Header comments point at **`docs/PRODUCT_SPEC.md` §8–§9**, **`CHANGELOG.md`**, **`docs/sbom-signing-audit.md`** (H2 follow-up after merges), and **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1 contract tests* — same as **`ci.yml`**).

**Supply chain (Roadmap H2):** **`le-vibe/requirements.txt`** uses **pinned** versions (`==`) for reproducible SBOMs; CI runs **`pip-audit -r requirements.txt`** (fails on known vulnerabilities) and generates **CycloneDX** **`le-vibe-python.cdx.json`**. Optional **`.deb`** / repo signing and key handling: **[`docs/sbom-signing-audit.md`](docs/sbom-signing-audit.md)**.

**Releases & apt (Roadmap H1):** CI uploads artifact **`le-vibe-deb`** with **`*.deb`**, **`le-vibe-python.cdx.json`** (SBOM), and **`SHA256SUMS`** covering both; the workflow runs **`sha256sum -c SHA256SUMS`** before upload. Maintainers: bump **`debian/changelog`**, promote **[`CHANGELOG.md`](CHANGELOG.md)** **`[Unreleased]`** into a dated section when tagging, and publish **GitHub Releases** / optional apt per **[`docs/apt-repo-releases.md`](docs/apt-repo-releases.md)** (checksum signing, **reprepro** / **aptly**).

## Tests

**E1 mapping:** **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** ties **§1** / **H8** naming + §5–§10 to implementation and tests. Notable contracts: **`test_product_spec_section8.py`** (§4 welcome, §7.2 / §8 Continue rule body), **`test_continue_workspace.py`** / **`test_workspace_hub.py`** (§7.2 — **`.continue/rules`** + **`.lvibe/AGENTS.md`**, **numbered questions**), **`test_session_orchestrator.py`** (**STEP 2** — bundled **`session-manifest`** example ↔ **`schemas/`**, PM workspace hooks), **`test_root_readme_ai_pilot_contract.py`** (§7.1 copy in this file + **E1** roster strings below), **`test_le_vibe_readme_e1_contract.py`** ([**`le-vibe/README.md`**](le-vibe/README.md) *Tests* roster vs this section), **`test_prompt_build_orchestrator_fence.py`** (pasteable Master orchestrator block in **`docs/PROMPT_BUILD_LE_VIBE.md`**), **`test_issue_template_h8_contract.py`** (**H8** — **STEP 12** / **`config.yml`** in **`.github/ISSUE_TEMPLATE/*.yml`**). See also **[`le-vibe/README.md`](le-vibe/README.md)** *Tests*.

```bash
cd le-vibe
pip install -r requirements.txt
pip install pytest
python3 -m pytest tests/
```

## Operator troubleshooting & observability

- **Structured log (local only):** **`~/.config/le-vibe/le-vibe.log.jsonl`** — append-only **JSON Lines** with UTC **`ts`**, **`component`** (`managed_ollama`, `first_run`, `launcher`), **`event`**, and context fields. Used for operator debugging; **nothing is sent to a Lé Vibe–hosted telemetry endpoint**. Set **`LE_VIBE_STRUCTURED_LOG=0`** to disable logging entirely.
- **Managed Ollama fails (launcher exit 6):** Port **`11435`** may already be in use by another process; stop it or pass **`lvibe --port N`**. Ensure **`ollama`** is on **`PATH`** (`which ollama`).
- **First-run / bootstrap fails:** Use **`LE_VIBE_VERBOSE=1`** with **`lvibe`** for more logging; fix Ollama install, disk space, or network for **`ollama pull`**, then **`lvibe --force-first-run`**.
- **Editor fails to start (exit 127):** Set **`LE_VIBE_EDITOR`** to your Code OSS / VSCodium binary or install **`codium`** where the launcher expects it.

## Known limitations

- **Product name:** **Lé Vibe** is **not** “Visual Studio Code”; it is a separate product; the editor is **Code - OSS** / **VSCodium**–class tooling.
- **Bundled IDE:** There is **no** prebuilt **Lé Vibe–branded** Electron release from this repo yet; **VSCodium** sources live under **`editor/vscodium/`**. For daily use, install **VSCodium** (or set **`LE_VIBE_EDITOR`**).
- **First run:** Model **download** and Ollama install can take a long time and need disk space; cold starts after that should be faster.
- **Continue / marketplace:** Extension id and Open VSX availability can vary by editor version; use **`LE_VIBE_CONTINUE_EXTENSION`** if install fails.
- **Icon / brand (Roadmap H5):** Shipped **`hicolor`** SVG (see **[`docs/brand-assets.md`](docs/brand-assets.md)**); optional PNG exports and **`docs/screenshots/`** conventions in **[`docs/screenshots/README.md`](docs/screenshots/README.md)**.

## Release / QA checklist (go / no-go)

Use this before calling a build “production-ready” (adapt to your process):

1. **Automated:** `cd le-vibe && python3 -m pytest tests/` — all green; `dpkg-buildpackage -us -uc -b` at repo root succeeds; CI workflow passes on `main`.
2. **Package contents:** `.deb` installs `le-vibe`, `/usr/bin/le-vibe`, app `.desktop`, optional **`/etc/xdg/autostart/le-vibe-continue-setup.desktop`**, icon, scripts under `/usr/share/le-vibe/scripts/`, and **`/usr/share/doc/le-vibe/README.Debian`** (post-install steps, **§5** `.lvibe/` consent, authority doc paths in the upstream tree).
3. **Clean VM** (Debian/Ubuntu): install `.deb`, install **codium**, run **`le-vibe`** from the app menu or CLI; complete **first-run**; run **`le-vibe-setup-continue`** (optionally **`--gui`** with Zenity — Roadmap **G-A2**); confirm the one-shot **desktop notification** or autostart behavior if **`libnotify-bin`** is present (**G-A3**); send **one Continue chat** to the local model.
4. **Lifecycle:** Quit the editor; confirm managed Ollama **stops** (e.g. `~/.config/le-vibe/managed_ollama.json` removed or process gone; port **11435** not serving your session).
5. **Sign-off:** Product accepts residual **lintian** warnings (if any) or files issues to clear them before GA.

## License

The Lé Vibe bootstrap and packaging in this repository are licensed under the **MIT License** — see [`LICENSE`](LICENSE). Third-party components (Ollama, VSCodium, Continue, upstream editor) have their own licenses.

## Trademark / safety

- Default Ollama bind: **localhost**; no public bind without explicit opt-in.
- `ollama pull` is **not** captured silently — progress streams on the TTY (see `ollama_ops.pull_model`).
