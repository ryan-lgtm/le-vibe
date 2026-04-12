# PM — Debian build one-shot (packaging iteration)

**Owner:** Product / release hygiene. **Goal:** One script builds **`le-vibe`** and optionally **`le-vibe-ide`** `.deb` files with prerequisite checks, optional **`sudo apt install`**, and clear artifact paths.

**Implementation:** [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh)  
**Sibling docs:** [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md), root [`debian/`](../debian/) (stack), [`editor/BUILD.md`](../editor/BUILD.md).

**Fresh clone (14.b / STEP 14):** **`le-vibe-ide`** repacks a compiled **`VSCode-linux-*`** tree from **`editor/vscodium/`** — if that directory is empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the repository root before **`editor/BUILD.md`** fetch/build steps — same as **`editor/README.md`** *Fresh clone (14.b)*.

## Releases & full-product demo (H1 / STEP 14 / §7.3)

When you have both artifacts from **`build-le-vibe-debs.sh`** (stack) and **`--with-ide`** (or **`build-le-vibe-ide-deb.sh`** alone), ship or attach **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** together for an install-and-demo that includes the branded IDE. **Checksums**, default CI artifact **`le-vibe-deb`** (stack-only), and **`SHA256SUMS`** expectations — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package* subsection, **STEP 8 / H1**). **PM stage map:** **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles* — **STEP 14** vs **STEP 8**); monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

## Lazy repeat — paste into Cursor (engineer)

**Print stdout (repo root):** `python3 packaging/scripts/print-pm-deb-build-prompt.py`

```
You are the Lé Vibe **packaging / .deb build** engineer for this monorepo. **MODE: ENGINEER.**

**Authority:** [`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) (this file) → [`packaging/scripts/build-le-vibe-debs.sh`](../packaging/scripts/build-le-vibe-debs.sh) → [`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md) → [`editor/BUILD.md`](../editor/BUILD.md).

**CI vs maintainer .deb bundles:** Default **`ci.yml`** artifact **`le-vibe-deb`** is **stack-only**; **`--with-ide`** adds **`le-vibe-ide_*_amd64.deb`** for full-product drops — **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles* — **STEP 14** vs **STEP 8**); monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

**Goal:** Keep **`build-le-vibe-debs.sh`** correct: prerequisite detection, **`dpkg-buildpackage`** for stack (repo root) and optional IDE (`--with-ide` → **`build-le-vibe-ide-deb.sh`**: stage + **`dpkg-buildpackage`** + optional **`lintian`**), **`--install`** / **`--yes`**, artifact discovery (`le-vibe_*.deb` in repo parent; `le-vibe-ide_*.deb` under **`packaging/`**). **Do not** claim GitHub Actions is a v1 production gate.

**After shell edits:** `bash -n packaging/scripts/build-le-vibe-debs.sh` and `cd le-vibe && python3 -m pytest tests/test_build_le_vibe_debs_script_contract.py` (or full **`pytest`**).

**Git:** After a **milestone** change to the script or this doc, `git add`, `git commit`, `git push` per [`docs/PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) **Git checkpoints**.

End with exactly **one** last line, nothing after:
- PASTE SAME AGAIN — substantive packaging work remains or tests not run
- LÉ VIBE PACKAGING COMPLETE — script + doc aligned; bash -n + pytest green
```

## Engineer acceptance (checklist)

- [ ] Script exits **2** with a clear **`apt install`** line when `dpkg-buildpackage` / `debhelper` is missing.
- [ ] Default run produces **`le-vibe_*.deb`** (parent of repo root) without IDE artifacts.
- [ ] `--with-ide` requires **`VSCode-linux-*`** (or **`--vs-build`**) per **`build-le-vibe-ide-deb.sh`** / **`stage-le-vibe-ide-deb.sh`** errors.
- [ ] `--install` uses **`sudo`** only for install, not for compile.
- [ ] **`print-pm-deb-build-prompt.py`** stdout matches the fenced block above (E1 contract).
