# PM — Debian build one-shot (packaging iteration)

**Owner:** Product / release hygiene. **Goal:** One script builds **`le-vibe`** and optionally **`le-vibe-ide`** `.deb` files with prerequisite checks, optional **`sudo apt install`**, and clear artifact paths.

**Implementation:** [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh)  
**Sibling docs:** [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md), root [`debian/`](../debian/) (stack), [`editor/BUILD.md`](../editor/BUILD.md).

**Fresh clone (14.b / STEP 14):** **`le-vibe-ide`** repacks a compiled **`VSCode-linux-*`** tree from **`editor/vscodium/`** — if that directory is empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the repository root before **`editor/BUILD.md`** fetch/build steps — same as **`editor/README.md`** *Fresh clone (14.b)*.

## Invocations (repository root)

Run these from the clone root (`cd /path/to/r-vibe`). Stack **`le-vibe_*.deb`** is emitted **beside** the repo directory (parent of the root); IDE **`le-vibe-ide_*.deb`** is under **`packaging/`** — see **`build-le-vibe-debs.sh`** **`--help`** and *Artifacts* in that usage.

| Goal | Command |
|------|---------|
| Stack **`.deb`** only | `packaging/scripts/build-le-vibe-debs.sh` |
| Stack, then **`sudo apt install`** the built **`.deb`** files | `packaging/scripts/build-le-vibe-debs.sh --install` (add **`--yes`** for non-interactive **`apt`**) |
| Stack + IDE — **Full-product install** on success — *Success output (`--with-ide`)* below | `packaging/scripts/build-le-vibe-debs.sh --with-ide` |
| **`--with-ide`** with §7.3 **`product.json`** gate (**`ci-editor-gate.sh`**) before staging | `LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-debs.sh --with-ide` |
| **`--with-ide`** using a non-default **`VSCode-linux-*`** directory | `packaging/scripts/build-le-vibe-debs.sh --vs-build /path/to/VSCode-linux-x64` |

## Releases & full-product demo (H1 / STEP 14 / §7.3)

When you have both artifacts from **`build-le-vibe-debs.sh`** (stack) and **`--with-ide`** (or **`build-le-vibe-ide-deb.sh`** alone), ship or attach **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** together for an install-and-demo that includes the branded IDE. **Checksums**, default CI artifact **`le-vibe-deb`** (stack-only), and **`SHA256SUMS`** expectations — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package* subsection, **STEP 8 / H1**). **PM stage map:** **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles* — **STEP 14** vs **STEP 8**); monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

**Success output (`--with-ide`):** When **`build-le-vibe-debs.sh`** finishes and both **`.deb`** files are found, it prints a **Full-product install** line — **`sudo apt install`** with the resolved paths (stack **`le-vibe_*_all.deb`** beside the repository directory, IDE **`le-vibe-ide_*_amd64.deb`** under **`packaging/`**), then **`/usr/share/doc/le-vibe/README.Debian`** and **`packaging/debian-le-vibe-ide/README.md`** (*Install both packages*).

**Failure (`--with-ide`):** If **`--with-ide`** is set but **`le-vibe-ide_*.deb`** is not found under **`packaging/`** after the IDE build step, **`build-le-vibe-debs.sh`** exits with status **1** — a stack-only **`.deb`** is not treated as a successful full-product run.

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

**Goal:** Keep **`build-le-vibe-debs.sh`** correct: prerequisite detection, **`dpkg-buildpackage`** for stack (repo root) and optional IDE (`--with-ide` → **`build-le-vibe-ide-deb.sh`**: stage + **`dpkg-buildpackage`** + optional **`lintian`**), **`--install`** / **`--yes`**, artifact discovery (`le-vibe_*.deb` in repo parent; `le-vibe-ide_*.deb` under **`packaging/`**). For **`--with-ide`**, document optional **`LEVIBE_STAGE_IDE_ASSERT_BRAND`** / **`LEVIBE_STAGE_IDE_VERBOSE`** (§7.3 IDE staging above; **`stage-le-vibe-ide-deb.sh`**) and optional **`LEVIBE_EDITOR_GATE_ASSERT_BRAND`** on **`ci-editor-gate.sh`** / **`editor/smoke.sh`** (same §7.3 **`.json`** check before staging). When both **`.deb`** files are produced, the script echoes **Full-product install** — align with **Success output (`--with-ide`)** above; if **`--with-ide`** but no **`le-vibe-ide_*.deb`**, exit **1** — **Failure (`--with-ide`)** above. **Do not** claim GitHub Actions is a v1 production gate.

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
