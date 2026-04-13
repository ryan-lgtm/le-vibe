# STEP 14 — autonomous engineer runbook (§7.3 close-out)

**Purpose:** Give the **engineer** (human or agent) **exact manifests, manuscript pointers, and paste blocks** so work on **STEP 14 / H6 / `editor/`** runs **to completion** without waiting for the owner to **orchestrate each turn**. Incremental steps are normal; **stalling for permission is not** when §7.3 and the Master queue already define the outcome.

**Authority:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) **§7.3** (material IDE choices are fixed — **implement**), Master orchestrator in [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) (**ORDERED WORK QUEUE**, execution order **0 → 1 → 14 → 2–13 → 15–17**), [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md) (hard stops).

---

## 1. Manifests (copy paths)

| Artifact | Path | Use |
|----------|------|-----|
| **Session schema (generic)** | [`schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json) | PM epics shape; STEP 2 seeding — [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) |
| **STEP 14 close-out (seed backlog)** | [`schemas/session-manifest.step14-closeout.v1.example.json`](../schemas/session-manifest.step14-closeout.v1.example.json) | Pre-filled **product.epics** for §7.3 tasks; optional copy to **`.lvibe/session-manifest.json`** if you use workspace orchestration |
| **User settings (IDE PM track)** | [`schemas/user-settings.v1.example.json`](../schemas/user-settings.v1.example.json) | When touching IDE settings workflows — [`PM_IDE_SETTINGS_AND_WORKFLOWS.md`](PM_IDE_SETTINGS_AND_WORKFLOWS.md) |

**Optional workspace copy:**

```bash
cp schemas/session-manifest.step14-closeout.v1.example.json .lvibe/session-manifest.json
```

Engineering **does not** require `.lvibe/` to ship **`editor/`** + **`.deb`**; use the manifest when you want visible epics/tasks in the same format as STEP 2.

---

## 2. Documentation the engineer must keep hot (lean index)

| Manuscript | Role |
|------------|------|
| [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) | **STEP 14** row + **do not** artificially cap scope while §7.3 remains open |
| [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) | **STEP →** primary PM doc for IDE / `.deb`; **H1 vs §7.3 .deb bundles** (stack **`ci.yml`** **`le-vibe-deb`** vs maintainer **`--with-ide`**) + **Compile fail-fast (STEP 14, before IDE `.deb`)** — same three scripts as the *Compile fail-fast* row below |
| [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) | **`packaging/scripts/build-le-vibe-debs.sh --with-ide`**, **Full-product install**, **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (+ optional **`--apt-sim`** / **`--json`**; **`apt_sim_note`** in **`--json`** — *`--json` close-out payload*); stack **`le-vibe_*.deb`** — **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** (*Output paths*). **Ordering:** **build machine** close-out, **test host** install/smoke — [`apt-repo-releases.md`](apt-repo-releases.md) (*IDE package*). |
| [`ci-qa-hardening.md`](ci-qa-hardening.md) | **`./editor/smoke.sh`** vs **`linux_compile`** / tarball — honesty |
| [`vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md) | H6 fork, CI, packaging narrative |
| [`editor/README.md`](../editor/README.md), [`editor/BUILD.md`](../editor/BUILD.md) | Build entrypoints; if **`VSCode-linux-*/bin/codium`** is missing, see **BUILD.md** (*Partial tree*), **`./editor/print-built-codium-path.sh`**, **`./editor/print-vsbuild-codium-path.sh`**, [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) (*Partial VSCode-linux tree*), **`packaging/scripts/build-le-vibe-ide-deb.sh --help`**, [`apt-repo-releases.md`](apt-repo-releases.md) (*IDE package* — *Incomplete Linux build*). |
| **Compile fail-fast (STEP 14)** | [`ci-vscodium-bash-syntax.sh`](../packaging/scripts/ci-vscodium-bash-syntax.sh) → [`ci-editor-nvmrc-sync.sh`](../packaging/scripts/ci-editor-nvmrc-sync.sh) → [`ci-vscodium-linux-dev-build.sh`](../packaging/scripts/ci-vscodium-linux-dev-build.sh) (→ **`editor/vscodium/dev/build.sh`**) — same ordering as **`./editor/smoke.sh`** / **`build-le-vibe-ide.yml`** *linux_compile*; [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md), [`apt-repo-releases.md`](apt-repo-releases.md) (*IDE package*), [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md). |
| [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md) | **`PASTE SAME AGAIN`** until done; stops below |

### 2.1 Full-product `.deb` fail-fast (probe before stack `dpkg-buildpackage`)

**[`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh)** **`--with-ide`** runs **`packaging/scripts/probe-vscode-linux-build.sh`** first (unless you pass **`--vs-build`** to a **`VSCode-linux-*`** tree that already has **`bin/codium`**). If the probe is not **`ready`**, the script **exits before** the stack **`dpkg-buildpackage`** — do not expect a **`le-vibe_*.deb`** rebuild when **14.c** is still incomplete. See **`docs/PM_DEB_BUILD_ITERATION.md`** *Failure (`--with-ide`)*. **`packaging/scripts/preflight-step14-closeout.sh`** prints a **stderr hint** after **`vscode_linux_build:`** when not **`ready`** (same maintainer story). **`lvibe ide-prereqs --print-closeout-commands`** includes the same ordering in its status blocks.

---

## 3. Stock / canonical assets (theme = Lé Vibe IDE + stack)

Use **in-repo** sources; do not invent parallel icon paths.

| Asset | Path / note |
|-------|-------------|
| **Canonical Linux app icon (SVG)** | [`packaging/icons/hicolor/scalable/apps/le-vibe.svg`](../packaging/icons/hicolor/scalable/apps/le-vibe.svg) |
| **Brand handoff (icons, `.desktop`, diagrams)** | [`brand-assets.md`](brand-assets.md) — **Icon=le-vibe**, hicolor; optional PNG export checklist; **presentation palette** (deep purple + ruby red) for Mermaid / slides only until H6 defines UI tokens |
| **Override sync helper** | [`editor/le-vibe-overrides/sync-linux-icon-assets.sh`](../editor/le-vibe-overrides/sync-linux-icon-assets.sh) |

**Intent:** Same **Lé Vibe** mark in launcher and editor chrome where §7.3 applies; **Code - OSS / VSCodium** attribution where upstream requires — see **§1** in [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md).

---

## 4. Hard stops (only these pause the engineer)

Per [`AGENT_MODE_ORCHESTRATION.md`](AGENT_MODE_ORCHESTRATION.md):

| Token | When |
|-------|------|
| **`USER_RESPONSE_REQUIRED`** | Guardrail end — missing **product** fact **outside** §7.3, or a **tradeoff** not in spec (numbered questions). **Not** “should I continue STEP 14?” |
| **`LÉ VIBE BLOCKED`** | Secrets, credentials, **required** out-of-repo access you cannot use |
| **`SKIPPED` + reason** | Honest deferral of a **slice** (e.g. cannot compile Electron in this environment) — document per **spec-phase2** §14 / Master queue rules — **do not** silently skip |

Everything else: **`PASTE SAME AGAIN`** and keep shipping until §7.3 is **implemented and verified** or honestly deferred with **`SKIPPED`**.

---

## 5. OWNER_DIRECTIVES — autonomous STEP 14 (paste above the master loop)

Use with [`MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md) / `print-master-iteration-loop-prompt.py`. **PRODUCT** and **PROJECT** hats stay **subordinate** to **ENGINEER** for this initiative unless you explicitly switch mode.

```
OWNER_DIRECTIVES:
- Primary outcome: Close PRODUCT_SPEC §7.3 — Lé Vibe end-to-end: full v1 branding in the built IDE shell under editor/, only lvibe as the public PATH CLI for the product story, installable Debian .deb for the IDE plus stack .deb where the repo defines Full-product install.
- Execution order: docs/PROMPT_BUILD_LE_VIBE.md — first incomplete STEP in order 0 → 1 → 14 → 2–13 → 15–17. While STEP 14 is incomplete, prioritize editor/ (H6) over STEPs 2–13.
- Do not wait for the owner to orchestrate each turn. Take substantive progress every ENGINEER turn (code, tests, packaging, or verified build notes). Repaste the same orchestration prompt with CONTINUATION: PASTE SAME AGAIN until §7.3 is verified or a slice is SKIPPED with reason.
- Forbidden: doc-only or contract-only churn that substitutes for a real branded IDE build path and .deb story unless the environment truly cannot compile — then SKIPPED + reason, not fake done.
- Stock assets: use packaging/icons/hicolor/scalable/apps/le-vibe.svg and docs/brand-assets.md; keep editor/le-vibe-overrides aligned.
- Stops: only USER_RESPONSE_REQUIRED (§7.2, outside §7.3) or LÉ VIBE BLOCKED (secrets / out-of-repo).
```

---

## 6. ENGINEER single-turn header (paste after the printed master loop body)

```
MODE: ENGINEER
CONTINUATION: PASTE SAME AGAIN

First incomplete STEP per PROMPT_BUILD_LE_VIBE.md ORDERED WORK QUEUE (0 → 1 → 14 → …). Branch main at recorded sha; cd le-vibe && python3 -m pytest tests/ after Python changes.
If STEP 14: advance §7.3 — smoke (./editor/smoke.sh), branding/editor overrides, Linux build path per editor/BUILD.md, **`probe-vscode-linux-build.sh` ready** then **`build-le-vibe-debs.sh --with-ide`** (probe-before-stack **`dpkg-buildpackage`** — [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) *Failure (`--with-ide`)*; **`--vs-build`** when staging from a non-default tree), then **`verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** / **`--json`** as needed; **`apt_sim_note`** in **`--json`** — [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) *`--json` close-out payload*); stack **`le-vibe_*.deb`** discovery — **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** (*Output paths* in [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)); **Ordering:** close-out on **build machine**, install/smoke on **test host** — [`apt-repo-releases.md`](apt-repo-releases.md) (*IDE package*); else SKIPPED + reason.
End with PASTE SAME AGAIN if work remains toward §7.3.
```

---

## 7. Definition of done (STEP 14 honest)

- **§7.3** behaviors in [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) are **implemented** in **`editor/`** and packaging — not merely described in tests.
- **Installable IDE `.deb`** + stack **`.deb`** per **`PM_DEB_BUILD_ITERATION.md`** / **`build-le-vibe-debs.sh --with-ide`** when the build environment can produce them; close-out gate via **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (optional **`--apt-sim`**, **`--json`**; **`apt_sim_note`** — [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) *`--json` close-out payload*); stack path helper **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** (*Output paths*). **Ordering:** **build machine** close-out, **test host** install/smoke — [`apt-repo-releases.md`](apt-repo-releases.md) (*IDE package*).
- **Local / manual** reproducibility narrative holds — **GitHub Actions are not** the v1 completion gate.
- If something cannot be verified in-agent, **`SKIPPED` + reason** — update the honest paragraph per **spec-phase2 §14**, do not claim green.

---

*This runbook **coordinates** behavior; it does not replace [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) must-ship until engineering merges evidence.*
