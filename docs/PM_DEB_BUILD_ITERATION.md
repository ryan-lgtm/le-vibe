# PM — Debian build one-shot (packaging iteration)

**Owner:** Product / release hygiene. **Goal:** One script builds **`le-vibe`** and optionally **`le-vibe-ide`** `.deb` files with prerequisite checks, optional **`sudo apt install`**, and clear artifact paths.

**Implementation:** [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh)  
**Sibling docs:** [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md), root [`debian/`](../debian/) (stack), [`editor/BUILD.md`](../editor/BUILD.md), **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](../docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** (E1 audit / *Last verified* when packaging or release copy shifts), **[`docs/apt-repo-releases.md`](../docs/apt-repo-releases.md)** (H1 / STEP 8 — *Related docs* lists **[`CHANGELOG.md`](../CHANGELOG.md)**, **`PRODUCT_SPEC_SECTION8_EVIDENCE.md`**, **`PM_DEB_BUILD_ITERATION.md`**, **`PM_STAGE_MAP.md`** next to **`ci-qa-hardening.md`**; **`ci-qa-hardening.md`** *Related docs* row → **[`editor/README.md`](../editor/README.md)** (*Full Linux compile* / **H3** maintainer index)).

**Master orchestrator:** **`build-le-vibe-debs.sh --with-ide`** is the one-shot **full-product** path for **STEP 14** / **§7.3** in queue order **0 → 1 → 14 → 2–13 → 15–17** — not “after everything else.” **Preflight (optional):** **`packaging/scripts/preflight-step14-closeout.sh --require-stack-deb`** or **`lvibe ide-prereqs --print-closeout-commands`** — *Preflight (all gaps)* below; **close-out gate:** **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable success output; **`apt_sim_note`** — *`--json` close-out payload* below). See **[`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md)** (*ORDERED WORK QUEUE*, *Rolling iteration — prefer continuation*) and **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** *Execution order* / **STEP 16** (same pointer as **[`editor/README.md`](../editor/README.md)** *Master orchestrator order*, **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)**).

**Release checklist (H1):** After you bump **`debian/changelog`** / **[`CHANGELOG.md`](../CHANGELOG.md)** (same **`x.y.z`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *Dual changelog discipline*) and want a **stack-only** GitHub Release (artifact **`le-vibe-deb`**, **`gh release create`**, **`SHA256SUMS`** verify) — follow **[`apt-repo-releases.md`](apt-repo-releases.md)** *Checklist — stack-only GitHub Release*. When you **`gh release create`** with **both** **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *Checklist — full-product GitHub Release* (*Combined drop* / **`SHA256SUMS`**); build both with **`build-le-vibe-debs.sh --with-ide`**, optionally run **`preflight-step14-closeout.sh --require-stack-deb`** or **`lvibe ide-prereqs --print-closeout-commands`**, then **`verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable success output; **`apt_sim_note`** — *`--json` close-out payload* below) — *Success output (`--with-ide`)* below.

**Stack vs IDE changelogs:** Root **`debian/changelog`** versions **`le-vibe_*_all.deb`**; **[`packaging/debian-le-vibe-ide/debian/changelog`](../packaging/debian-le-vibe-ide/debian/changelog)** versions **`le-vibe-ide_*_amd64.deb`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *IDE `le-vibe-ide` changelog* (same **H1** *Tagging discipline* story as stack **`v…`** vs **`ide-v*`**).

**`dpkg-parsechangelog` (IDE):** From the repository root, **`dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog`** prints the top **`le-vibe-ide`** package version — same **`dpkg-dev`** tool as **`dpkg-parsechangelog -S Version -l debian/changelog`** for the stack (*Publishing* below). Use it when verifying a full-product drop before **`--with-ide`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *Checklist — full-product GitHub Release* step **2**.

**Fresh clone (14.b / STEP 14):** **`le-vibe-ide`** repacks a compiled **`VSCode-linux-*`** tree from **`editor/vscodium/`** — if that directory is empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the repository root before **`editor/BUILD.md`** fetch/build steps — same as **`editor/README.md`** *Fresh clone (14.b)*.

**Compile fail-fast (STEP 14, same as `./editor/smoke.sh` / `build-le-vibe-ide.yml` *linux_compile*):** **`packaging/scripts/ci-vscodium-bash-syntax.sh`** → **`packaging/scripts/ci-editor-nvmrc-sync.sh`** → **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** (→ **`editor/vscodium/dev/build.sh`**) — **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md)** *Prioritization*; **[`editor/BUILD.md`](../editor/BUILD.md)** (*CI*); **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*).

## Invocations (repository root)

**Working directory:** **`build-le-vibe-debs.sh`** resolves the monorepo root from the script path and **`cd`s there** before **`dpkg-buildpackage`** — you can invoke it **from any cwd** (absolute path to the script, or a relative path from where you are). Examples below still spell **`packaging/scripts/...`** as if **`cd /path/to/r-vibe`** for consistency with **`--help`**.

Stack **`le-vibe_*.deb`** is emitted **beside** the repo directory (parent of the root); IDE **`le-vibe-ide_*.deb`** is under **`packaging/`** — see **`build-le-vibe-debs.sh`** **`--help`** and *Artifacts* in that usage.

| Goal | Command |
|------|---------|
| Stack **`.deb`** only | `packaging/scripts/build-le-vibe-debs.sh` |
| Stack, then **`sudo apt install`** the built **`.deb`** files | `packaging/scripts/build-le-vibe-debs.sh --install` (add **`--yes`** for non-interactive **`apt`**) |
| Stack + IDE — **Full-product install** on success — *Success output (`--with-ide`)* below | `packaging/scripts/build-le-vibe-debs.sh --with-ide` |
| **`--with-ide`** with §7.3 **`product.json`** gate (**`ci-editor-gate.sh`**) before staging | `LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-debs.sh --with-ide` |
| **`--with-ide`** using a non-default **`VSCode-linux-*`** directory | `packaging/scripts/build-le-vibe-debs.sh --vs-build /path/to/VSCode-linux-x64` |
| Faster stack **`dpkg-buildpackage`** (parallel **debhelper**) | `DEB_BUILD_OPTIONS=parallel=$(nproc) packaging/scripts/build-le-vibe-debs.sh` — passed through to **`dpkg-buildpackage`** (**`--help`** *Environment*: **`DEB_BUILD_OPTIONS`**) |

**Quick version check (repo root):** Before iterating on **`dpkg-buildpackage`**, read the top stanza versions with **`dpkg-parsechangelog -S Version -l debian/changelog`** (stack) and, for a full-product **`--with-ide`** drop, **`dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog`** — same commands as **`apt-repo-releases.md`** *Before a stack tag / Release* and *Checklist — full-product GitHub Release* step **2**; see **`Stack vs IDE changelogs`** and **`dpkg-parsechangelog` (IDE)** above.

### Output paths (from repo root)

| Artifact | Where it lands |
|----------|----------------|
| Stack **`le-vibe_*_all.deb`** | **Parent of the clone** — `../le-vibe_*_all.deb` (standard **`dpkg-buildpackage`** output from the repo root) |
| IDE **`le-vibe-ide_*_amd64.deb`** | **`packaging/le-vibe-ide_*.deb`** (sibling Debian source under **`packaging/debian-le-vibe-ide/`**) |

Implementation: **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** prints the newest matching path (parent of the clone, then **repo root**). **`verify-step14-closeout.sh --require-stack-deb`**, **`build-le-vibe-debs.sh`** (**`find_stack_deb`**), and **`manual-step14-install-smoke.sh`** (default **`STACK_DEB`**) all use it. **`build-le-vibe-debs.sh`** uses the same resolution when printing **Full-product install**.

**Preflight (all gaps):** **`packaging/scripts/preflight-step14-closeout.sh`** prints **`[ok]`** / **`[missing]`** for **`ci-editor-gate.sh`**, **14.c** **`editor/vscodium/VSCode-linux-*/bin/codium`**, **`packaging/le-vibe-ide_*.deb`**, and (with **`--require-stack-deb`**) stack **`le-vibe_*.deb`** — run before **`verify-step14-closeout.sh`** when iterating long **`dev/build.sh`** compiles so every blocker is visible at once.

**Full-product install** echoes **absolute** paths when both exist — *Success output (`--with-ide`)* below.

**Script help:** `packaging/scripts/build-le-vibe-debs.sh --help` (alias **`-h`**) prints flags, environments, artifact paths, exit codes, and H1 publishing pointers — same text as in [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh).

**Release folder (H1):** **Combined** drops match *Checklist — full-product GitHub Release* step **3** — copy the **`le-vibe-deb`** tree (**`le-vibe_*_all.deb`**, **`le-vibe-python.cdx.json`**, **`SHA256SUMS`**) **and** **`le-vibe-ide_*_amd64.deb`** into **one** folder, **regenerate** **`SHA256SUMS`**, then **`sha256sum -c`** / **`lvibe verify-checksums`**. Same *Minimum directory layout (readiness gate)* — stack-only three files vs **rewrite** after the second **`.deb`** — **[`apt-repo-releases.md`](apt-repo-releases.md)**.

**Publishing (STEP 8 / H1):** **`SHA256SUMS`**, **`debian/changelog`** ↔ **`CHANGELOG.md`**, and **stack-only** **`ci.yml`** **`le-vibe-deb`** vs **Stack + IDE** attach — **[`apt-repo-releases.md`](apt-repo-releases.md)** *Pre-publish artifact checklist* (**Checklist shorthand** — three lines for stack-only vs one **`--with-ide`** run vs CI+IDE **Combined drop**; same story as *Releases & full-product demo* below). **Before a stack tag / GitHub Release:** **`dpkg-parsechangelog -S Version -l debian/changelog`** should match **`CHANGELOG.md`** and the intended **`v…`** tag — same doc *Versioned changelog*. **Combined drop:** if you download the CI stack artifact and build **`le-vibe-ide`** in a **separate** step, put every shipped **`*.deb`** / SBOM in **one** directory and **regenerate** **`SHA256SUMS`** — the CI manifest is **not** valid after you add the second **`*.deb`** — same doc *Pre-publish* table row **Combined drop**. The **`ci.yml`** artifact **`le-vibe-deb`** downloads as a **`.zip`** — unzip before **`sha256sum -c SHA256SUMS`** or **`lvibe verify-checksums -C …`** — *GitHub Releases + checksums* (**H1 quick pointer** to the release checklists before **`gh release create`**) in the same doc. **`ide-v*`** git tags drive optional **`linux_compile`** CI — they do **not** replace bumping **`debian/changelog`** for the stack **`.deb`** — *Tagging discipline* in the same doc. **Stack `v…` release tags** (aligned with **`dpkg -l`**) vs **`ide-v*`** compile-only tags — *Stack release tags vs `ide-v`* (*publishing*) in the same doc.

### Exit codes (`build-le-vibe-debs.sh`)

| Code | Meaning |
|------|---------|
| **0** | Success — stack **`le-vibe_*.deb`** built; with **`--with-ide`**, both stack and **`packaging/le-vibe-ide_*.deb`** were found (see *Failure (`--with-ide`)* below). |
| **1** | **`--with-ide`** set but the IDE build failed or **`le-vibe-ide_*.deb`** was not found under **`packaging/`** after the IDE step — see *Failure (`--with-ide`)* below. |
| **2** | User or environment error: missing **`dpkg-buildpackage`** / **`debhelper`** (install line printed), unknown option, **`--vs-build`** without a path, missing **`find`** / **`sort`** / **`head`**, or **`--install`** without **`sudo`** / **`apt-get`**. |

Same table is summarized in **`packaging/scripts/build-le-vibe-debs.sh`** **`--help`** under **Exit codes**.

## Releases & full-product demo (H1 / STEP 14 / §7.3)

When you have both artifacts from **`build-le-vibe-debs.sh`** (stack) and **`--with-ide`** (or **`build-le-vibe-ide-deb.sh`** alone), ship or attach **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** together for an install-and-demo that includes the branded IDE. **Checksums**, default CI artifact **`le-vibe-deb`** (stack-only), and **`SHA256SUMS`** expectations — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package* subsection, **STEP 8 / H1**). Regenerate **`SHA256SUMS`** over **every** shipped **`*.deb`** / SBOM when combining paths (stack beside repo, IDE under **`packaging/`**) — same doc *Pre-publish artifact checklist* (**Integrity**). **PM stage map:** **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles* — **STEP 14** vs **STEP 8**); monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

**Success output (`--with-ide`):** When **`build-le-vibe-debs.sh`** finishes and both **`.deb`** files are found, it prints a **Full-product install** line — **`sudo apt install`** with the resolved paths (stack **`le-vibe_*_all.deb`** beside the repository directory, IDE **`le-vibe-ide_*_amd64.deb`** under **`packaging/`**), then **`/usr/share/doc/le-vibe/README.Debian`** and **`packaging/debian-le-vibe-ide/README.md`** (*Install both packages*), plus the local close-out check **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (gate + built **`codium`** + both **`.deb`** artifacts; add **`--apt-sim`** when you want explicit **`apt-get -s install`** dependency simulation on this host; add **`--json`** for machine-readable success output; **`apt_sim_note`** — *`--json` close-out payload* below). For the remaining manual Ubuntu install/launch smoke, use **`packaging/scripts/manual-step14-install-smoke.sh`** (or **`--print-install-cmd`** for an exact install command line, **`--json`** for machine-readable paths/install command plus **`vscode_linux_build`** — same field as **`lvibe ide-prereqs --json`** for the clone). Run close-out on the **build machine** where the **`.deb`** files were produced; run **`sudo apt install`** and the smoke helper on a **test host** — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*), **`packaging/debian-le-vibe-ide/README.md`** (*Install both packages*).

**`--json` close-out payload:** **`verify-step14-closeout.sh --json`** includes **`vscode_linux_build`** (`"ready"` on success — same invariant as **`lvibe ide-prereqs --json`** after **14.c** passes), **`codium_path`**, **`ide_deb`**, **`apt_sim_note`** — `not_requested` (default), `ran` (with **`--require-stack-deb`** + **`--apt-sim`**), or `requested_without_stack_requirement` (**`--apt-sim`** without **`--require-stack-deb`**), alongside **`apt_sim_requested`** / **`apt_sim_ran`**.

**Failure (`--with-ide`):** If **`--with-ide`** is set but **`le-vibe-ide_*.deb`** is not found under **`packaging/`** after the IDE build step, **`build-le-vibe-debs.sh`** exits with status **1** — a stack-only **`.deb`** is not treated as a successful full-product run.

**Partial VSCode-linux tree:** If **`editor/vscodium/VSCode-linux-*`** exists but **`bin/codium`** is missing (e.g. only **`codium-tunnel`** after an interrupted compile), **`packaging/scripts/stage-le-vibe-ide-deb.sh`** and **`./editor/print-built-codium-path.sh`** fail with an explicit hint — finish **`dev/build.sh`** per **`editor/BUILD.md`** (*Partial tree*, **14.c**). **`./editor/print-vsbuild-codium-path.sh`** helps when the tree lives outside **`editor/vscodium/`**; **`packaging/scripts/build-le-vibe-ide-deb.sh --help`** lists the same triage and **`verify-step14-closeout.sh --require-stack-deb`** for full close-out after both **`.deb`**s exist. Same maintainer story — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package* — *Incomplete Linux build*); **`packaging/debian-le-vibe-ide/README.md`** (*Build steps*).

### §7.3 IDE staging — Lé Vibe identity in the built tree

The **`le-vibe-ide`** package repacks **`editor/vscodium/VSCode-linux-*`**. That directory should be produced after **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** (merge **`product-branding-merge.json`**, **`sync-linux-icon-assets.sh`**, env defaults) **before** **`dev/build.sh`** — not a bare upstream compile — see **`editor/BUILD.md`** *Linux icons*.

**[`packaging/scripts/stage-le-vibe-ide-deb.sh`](../packaging/scripts/stage-le-vibe-ide-deb.sh)** warns if **`resources/app/product.json`** lacks **Lé Vibe** strings. Optional environment (inherited by **`build-le-vibe-ide-deb.sh`** and **`build-le-vibe-debs.sh --with-ide`**):

- **`LEVIBE_STAGE_IDE_ASSERT_BRAND=1`** — fail staging when identity is missing (use for release or demo drops).
- **`LEVIBE_STAGE_IDE_VERBOSE=1`** — print a line when the check passes.

**Pre-staging gate (optional):** **`LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 ./editor/smoke.sh`** (same as **`./packaging/scripts/ci-editor-gate.sh`**) fails if a **`VSCode-linux-*`** tree exists under **`editor/vscodium/`** but **`resources/app/product.json`** is missing or lacks **Lé Vibe** — run before **`build-le-vibe-ide-deb.sh`** / **`build-le-vibe-debs.sh --with-ide`** when you want the fast layout gate to enforce §7.3 identity without building **`.deb`**s yet — **[`editor/BUILD.md`](../editor/BUILD.md)** (*Debian package for the Lé Vibe IDE*). **One-shot:** **`LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-debs.sh --with-ide`** runs **`ci-editor-gate.sh`** automatically before **`build-le-vibe-ide-deb.sh`** (same check). **IDE-only:** **`LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-ide-deb.sh`** runs the same gate before **`stage-le-vibe-ide-deb.sh`**.

## Lazy repeat — paste into Cursor (engineer)

**Print stdout (repo root):** `python3 packaging/scripts/print-pm-deb-build-prompt.py`

```
You are the Lé Vibe **packaging / .deb build** engineer for this monorepo. **MODE: ENGINEER.**

**Authority:** [`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) (this file) → [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh) → [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md) → [`editor/BUILD.md`](../editor/BUILD.md).

**CI vs maintainer .deb bundles:** Default **`ci.yml`** artifact **`le-vibe-deb`** is **stack-only**; **`--with-ide`** adds **`le-vibe-ide_*_amd64.deb`** for full-product drops — **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles* — **STEP 14** vs **STEP 8**); monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

**Goal:** Keep **`build-le-vibe-debs.sh`** correct: prerequisite detection, **`dpkg-buildpackage`** for stack (repo root) and optional IDE (`--with-ide` → **`build-le-vibe-ide-deb.sh`**: stage + **`dpkg-buildpackage`** + optional **`lintian`**), **`--install`** / **`--yes`**, artifact discovery (**`resolve-latest-le-vibe-stack-deb.sh`** for **`le-vibe_*.deb`**; **`le-vibe-ide_*.deb`** under **`packaging/`**). For **`--with-ide`**, document optional **`LEVIBE_STAGE_IDE_ASSERT_BRAND`** / **`LEVIBE_STAGE_IDE_VERBOSE`** (§7.3 IDE staging above; **`stage-le-vibe-ide-deb.sh`**) and optional **`LEVIBE_EDITOR_GATE_ASSERT_BRAND`** on **`ci-editor-gate.sh`** / **`editor/smoke.sh`** (same §7.3 **`.json`** check before staging). When both **`.deb`** files are produced, the script echoes **Full-product install** — align with **Success output (`--with-ide`)** above; if **`--with-ide`** but no **`le-vibe-ide_*.deb`**, exit **1** — **Failure (`--with-ide`)** above. **Exit codes:** **0** success; **1** **`--with-ide`** without IDE **`.deb`** or IDE build failed; **2** missing stack tools / bad flags / **`--install`** prerequisites — *Exit codes (`build-le-vibe-debs.sh`)* above and **`--help`**. **H1 publishing:** CI **`le-vibe-deb`** is a **`.zip`** — unzip before verify; **`lvibe verify-checksums`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *GitHub Releases + checksums*; **stack `v…` vs `ide-v*`** — same doc *Stack release tags vs `ide-v`* (*publishing*). **Do not** claim GitHub Actions is a v1 production gate.

**After shell edits:** `bash -n packaging/scripts/build-le-vibe-debs.sh` and `cd le-vibe && python3 -m pytest tests/test_build_le_vibe_debs_script_contract.py` (or full **`pytest`**).

**Git:** After a **milestone** change to the script or this doc, `git add`, `git commit`, `git push` per [`docs/PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) **Git checkpoints**.

End with exactly **one** last line, nothing after:
- PASTE SAME AGAIN — substantive packaging work remains or tests not run
- LÉ VIBE PACKAGING COMPLETE — script + doc aligned; bash -n + pytest green
```

## Engineer acceptance (checklist)

- [ ] Script exits **2** with a clear **`apt install`** line when `dpkg-buildpackage` / `debhelper` is missing.
- [ ] Default run produces **`le-vibe_*.deb`** (parent of repo root) without IDE artifacts.
- [ ] `--with-ide` requires **`VSCode-linux-*`** (or **`--vs-build`**) per **`build-le-vibe-ide-deb.sh`** / **`stage-le-vibe-ide-deb.sh`** errors; if the IDE **`.deb`** is still missing under **`packaging/`**, **`build-le-vibe-debs.sh`** exits **1** (not stack-only success).
- [ ] `--install` uses **`sudo`** only for install, not for compile.
- [ ] **`print-pm-deb-build-prompt.py`** stdout matches the fenced block above (E1 contract).
