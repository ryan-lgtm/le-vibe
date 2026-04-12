# Lé Vibe — releases, checksums, and apt hosting (Roadmap H1)

**STEP 8 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H1** row links here, **`debian/changelog`**, **`CHANGELOG.md`**, and **`.github/workflows/ci.yml`** artifact **`le-vibe-deb`**.

**CI vs IDE bundle:** Default **`ci.yml`** **`le-vibe-deb`** contains the **stack** **`le-vibe`** **`.deb`** + SBOM + **`SHA256SUMS`** — **not** **`le-vibe-ide_*_amd64.deb`** (**§7.3**). Full-product releases attach both — *IDE package* below; monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

This document is for **maintainers** who publish the **`.deb`** beyond ad-hoc copies: **GitHub Actions** artifacts, **checksum files**, **GitHub Releases**, and optional **apt** repositories.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9 — agent/secrets policy and the orchestration roster. **Roadmap H1** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md); see also [`sbom-signing-audit.md`](sbom-signing-audit.md) (**H2**).

**E1 / acceptance:** After changing launcher or packaging behavior, re-verify **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** and run **`cd le-vibe && python3 -m pytest tests/`** (full suite — **H8** / **STEP 12** via **`test_issue_template_h8_contract.py`**; see root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **`spec-phase2.md` §14** *Honesty vs CI* for the rest) in a source tree — same bar as CI (**[`ci-qa-hardening.md`](ci-qa-hardening.md)**). **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)**, **[`.github/dependabot.yml`](../.github/dependabot.yml)**, and **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines) sit in the same **H8** index as **`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1 contract tests* — workflow and Dependabot headers record that chain alongside **§14** scope (**H2** bump PRs → **`sbom-signing-audit.md`** follow-up). **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) in the same **H8** index — refresh when trust or **`SECURITY`** copy shifts.

**Install UX:** Each **`.deb`** ships **`/usr/share/doc/le-vibe/README.Debian`** (source [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) — post-install steps, **§5** **`.lvibe/`** workspace consent, pointers to **`PRODUCT_SPEC`** / the docs index, and an on-disk **Phase 2 scope** line (**`docs/spec-phase2.md` §14**, **H6**/**H7** vs this package). Mention it in **GitHub Releases** copy when you publish binaries so users land on the same authority chain as the source tree. **Release/marketing copy** should stay aligned with **[`spec-phase2.md`](../spec-phase2.md) §14** — **`editor/`** (**H6**) and optional **H7** bundles ship per policy; stack **`le-vibe`** **`.deb`** may publish separately from IDE artifacts until unified releases exist.

## Versioned changelog

Package version and per-release notes live in **`debian/changelog`** (Debian policy format). For **GitHub Releases** body text, also update the root **[`CHANGELOG.md`](../CHANGELOG.md)** (Keep a Changelog style) so users see the same story without reading Debian policy formatting. Between tags, **`[Unreleased]`** may hold **Documentation** / trust-alignment bullets (e.g. **`spec-phase2.md` §14** cross-links) — fold them into a dated **`[x.y.z]`** section when you bump **`debian/changelog`**.

Bump before tagging a release, for example:

```bash
cd /path/to/r-vibe
dch -v 0.1.1 "Describe user-visible changes."
# edit the entry if needed, then build
dpkg-buildpackage -us -uc -b
```

The first line (`le-vibe (0.1.1) unstable; urgency=…`) must match the version users see after **`apt install`** / **`dpkg -l le-vibe`**.

## CI artifacts (what ships from each green run)

Workflow **`.github/workflows/ci.yml`** uploads a single artifact bundle **`le-vibe-deb`** containing:

| File | Role |
|------|------|
| **`le-vibe_<version>_all.deb`** | Installable package |
| **`SHA256SUMS`** | **`sha256sum`** lines for **each** `*.deb` **and** **`le-vibe-python.cdx.json`** (CycloneDX SBOM from **`pip-audit` / `cyclonedx-bom`** — see **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)**) |
| **`le-vibe-python.cdx.json`** | Python dependency SBOM for supply-chain review |

CI runs **`sha256sum -c SHA256SUMS`** after generating the manifest so a corrupted or mismatched tree fails the job.

### IDE package (`le-vibe-ide`, STEP 14 / §7.3)

Default **`ci.yml`** artifacts ship the **stack** **`le-vibe`** **`.deb`** only. The **Lé Vibe IDE** is a **sibling** Debian source under **`packaging/debian-le-vibe-ide/`**: after **`editor/vscodium/VSCode-linux-*`** exists, run **`packaging/scripts/build-le-vibe-ide-deb.sh`** (or **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** with the stack — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)**). Full story — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)**, **[`editor/BUILD.md`](../editor/BUILD.md)**.

**Maintainer build output:** Successful **`build-le-vibe-debs.sh --with-ide`** prints a **Full-product install** line (**`sudo apt install`** with both resolved **`.deb`** paths) — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*). Installing both from one directory (or equivalent) — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** (*Install both packages*).

For a **release** that demos the **full** stack + branded editor, attach **`le-vibe-ide_*_amd64.deb`** alongside **`le-vibe_*_all.deb`** when both exist; add both **`*.deb`** lines to **`SHA256SUMS`** and run **`sha256sum -c SHA256SUMS`** before publishing.

## GitHub Releases + checksums

When you cut a **release** (tag + GitHub Release):

1. Pick a **green** workflow run on **`main`** / **`master`** (or build locally with **`dpkg-buildpackage -us -uc -b`** and regenerate checksums as below).
2. Download artifact **`le-vibe-deb`** (ZIP from **Actions → workflow run → Artifacts**), or use the **`gh`** CLI:  
   `gh run download <run-id> -n le-vibe-deb -D ./release-dir`
3. Attach to the GitHub Release: **`*.deb`**, **`SHA256SUMS`**, and optionally **`le-vibe-python.cdx.json`** (already listed in **`SHA256SUMS`**).
4. Paste **`CHANGELOG.md`** section for that version into the Release description.

**Verify before install** (run inside the directory that contains **`SHA256SUMS`** and the files named on the right-hand side of each line — typically the extracted artifact folder):

```bash
sha256sum -c SHA256SUMS
```

Then install the **`.deb`**:

```bash
sudo apt install ./le-vibe_*_all.deb
```

(`apt install ./file.deb` resolves dependencies from configured apt sources.)

**Manual checksums** (e.g. local build without SBOM path):

```bash
sha256sum le-vibe_*_all.deb le-vibe-python.cdx.json > SHA256SUMS
sha256sum -c SHA256SUMS
```

Optional: sign **`SHA256SUMS`** with **`gpg --clearsign`** and publish **`SHA256SUMS.asc`**; users verify with **`gpg --verify`**. Key handling is described in **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)**.

## Private or team apt repo (overview)

Hosting a real **apt** repository usually means: a web root (or object storage) with **`Packages`**, **`Release`**, and **`InRelease`** (or **`Release.gpg`**), plus a **pool/** of **`*.deb`** files. Two common toolchains:

### reprepro

- One-off imports: **`reprepro includedeb suite /path/to/package.deb`**
- Typical layout: a single directory holding **`conf/distributions`**, **`conf/options`**, **`db/`**, **`dists/`**, **`pool/`**
- Signing: set **`SignWith: default`** (or a key id) in **`conf/distributions`** so **`Release`** is signed; clients need your **GPG** key in **`apt-key`** / **`signed-by=`** (modern apt prefers a keyring file under **`/etc/apt/trusted.gpg.d/`** or **`Signed-By`** in the source line)

See **`man reprepro`** and Debian wiki “LocalAPTRepository” for full examples.

### aptly

- **`aptly repo create -distribution=…`** then **`aptly repo add …`**, **`aptly publish repo …`**
- Publishes a **`public/`** tree you sync to HTTPS; supports signing on publish

See **`https://www.aptly.info/`** for CLI details.

### Client snippet (after you publish)

Users add something like:

```text
deb [signed-by=/usr/share/keyrings/le-vibe-archive-keyring.gpg] https://releases.example.com/le-vibe/apt stable main
```

Exact **`signed-by`** and URL depend on how you host keys and the repository. Do not ship private keys in this repo; use CI secrets or offline signing.

## What stays in this repository

- **Source:** `debian/`, `packaging/`, CI that builds, verifies checksums, and uploads artifacts.
- **Not required in-tree:** full **reprepro**/**aptly** config for your domain — that is org-specific (DNS, TLS, signing keys, mirror layout).

For product positioning and **`editor/`** / IDE shell notes, see **`README.md`** and **`docs/vscodium-fork-le-vibe.md`**.

## Related docs

| Doc | Role |
|-----|------|
| [`ci-qa-hardening.md`](ci-qa-hardening.md) | Smoke script, **lintian**, CI step order (H3) |
| [`sbom-signing-audit.md`](sbom-signing-audit.md) | **`pip-audit`**, CycloneDX SBOM next to **`.deb`** (H2) |
| [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Canonical workflow; artifact bundle **`le-vibe-deb`** |
