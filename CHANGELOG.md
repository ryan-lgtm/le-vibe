# Changelog

User-facing notes for the **Lé Vibe** bootstrap / launcher **`.deb`**. Package version is defined in **`debian/changelog`**; keep this file in sync when you cut a release so **GitHub Releases** copy can match Debian versioning.

## [Unreleased]

### Tests

- **`test_session_orchestrator.py`** — bundled **`session-manifest`** example matches **`schemas/session-manifest.v1.example.json`** (STEP 2 / PM workspace parity).
- **`test_le_vibe_readme_e1_contract.py`** — **`le-vibe/README.md`** *Tests* section keeps core **E1** module names aligned with root **`README.md`** *E1 mapping*.
- **`test_issue_template_h8_contract.py`** — **`.github/ISSUE_TEMPLATE/*.yml`** and **`config.yml`** retain **STEP 12** / **`config.yml`** / **H8** string anchors (**H8**, §1 audit assist; not a YAML parse).
- **`test_continue_workspace.py`** — **`.continue/rules`** memory file must include **numbered questions** (§7.2).
- **`test_workspace_hub.py`** — seeded **`.lvibe/AGENTS.md`** must include **numbered questions** (§7.2 alignment with Continue rules).
- **`test_product_spec_section8.py`** — §7.2 Continue rule must include **numbered questions** (with **`USER RESPONSE REQUIRED`**).
- Master orchestrator fenced block in **`docs/PROMPT_BUILD_LE_VIBE.md`** remains extractable (**STEP 16** / **`packaging/scripts/print-master-orchestrator-prompt.py`**) — [`le-vibe/tests/test_prompt_build_orchestrator_fence.py`](le-vibe/tests/test_prompt_build_orchestrator_fence.py).

### Documentation

- **`PRODUCT_SPEC` *Prioritization*:** documents **`build-linux.yml`** as a **`workflow_dispatch`** alias reusing **`build-le-vibe-ide.yml`** (STEP 14 / **H6**); **[`docs/ci-qa-hardening.md`](docs/ci-qa-hardening.md)** *Related docs* and **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md)** STEP **14** point at the same pair; **[`spec-phase2.md`](spec-phase2.md)** §14 (*Honesty vs CI*, ships table) and **[`editor/BUILD.md`](editor/BUILD.md)** aligned; root **`README.md`** *Tests* / **E1 mapping** and **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** intro cite **`test_product_spec_section8.py`** vs **`build-linux.yml`** alongside **`build-le-vibe-ide.yml`**; **[`docs/SESSION_ORCHESTRATION_SPEC.md`](docs/SESSION_ORCHESTRATION_SPEC.md)** intro names both workflows for PM ↔ IDE coordination; **[`le-vibe/README.md`](le-vibe/README.md)** *Tests* **`test_product_spec_section8.py`** line matches the same pairing.
- **E1 roster (broad sweep closure):** maintainer surfaces (**`docs/`**, **`packaging/`**, **`.github/`**, **`.desktop`**, **`README.Debian`**) defer full **`pytest`** contract meaning to root **`README.md`** *Tests* / **E1 mapping** and **`spec-phase2.md` §14** *Honesty vs CI* (not only **`test_issue_template_h8_contract.py`** / **H8**).
- **[`SECURITY.md`](SECURITY.md)** *Related docs* — **`privacy-and-telemetry`** bullet cites **E1 contract tests** row; **`spec.md`** *Acceptance / E1* — root **`README`** *Tests* + privacy table.
- **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)** — *Related documentation* table: **E1 contract tests** row (root **`README`** *Tests*, **`le-vibe/README`**, **`le-vibe/tests/`**); E1 evidence §7.1 row cites **`README`** *Tests* + **`le-vibe/README`**.
- Root **`README.md`** *Tests* — aligned with **`PRODUCT_SPEC` §10** / **`le-vibe/README`** ( **`test_workspace_hub`**, **`test_continue_workspace`**, §7.2 **numbered questions**); **`python3 -m pytest`** example.
- **`le-vibe/README.md`** *Tests* — roster matches **`PRODUCT_SPEC` §10** (**`test_workspace_hub`**, **`test_continue_workspace`**, §7.2 **numbered questions**).
- **H8 / STEP 12:** [`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md) *E1 (STEP 12)*, [`docs/README.md`](docs/README.md) *Product surface* (*E1*), [`spec-phase2.md`](spec-phase2.md) §14 *Honesty vs CI*, [`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md) *Roadmap H8* — **`.github/`** workflow / Dependabot / issue-template edits ↔ §10 checklist / docs index.
- **`docs/screenshots/README.md`**, **`docs/flatpak-appimage.md`** (H7), **`docs/vscodium-fork-le-vibe.md`** (H6) — *E1* scope paragraphs (screenshots vs §10; **SKIPPED** in-tree H7; fork CI out-of-repo); E1 evidence *H6/H7* row updated.
- **E1 evidence §7.2** — [`test_product_spec_section8.py`](le-vibe/tests/test_product_spec_section8.py) **numbered questions** assertion called out; **Roadmap H5** (*brand-assets*, E1 evidence) — **`desktop-file-validate`**, §1 **Lé Vibe**, §10 refresh.
- **`docs/continue-extension-pin.md`** (H4) — **E1 / acceptance** (`verify-continue-pin`, **`test_continue_openvsx_pin.py`**, evidence refresh); **[`docs/README.md`](docs/README.md)** table + E1 evidence *Roadmap H4* line.
- **`docs/sbom-signing-audit.md`** (H2) and **`docs/ci-qa-hardening.md`** (H3) — **E1 / acceptance** paragraphs (supply-chain / **`pytest`** vs **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)**); E1 evidence *Roadmap H1–H3* row updated.
- **`docs/PROMPT_BUILD_LE_VIBE.md`** (intro), root **`README.md`** (*Documentation index*), **`docs/apt-repo-releases.md`** (H1) — **E1 / pytest** / post-release verification pointers.
- **`spec-phase2.md` §14** (*Honesty vs CI*) — navigation line for **`docs/README`**, **`PM_STAGE_MAP` STEP 1**, **`SESSION_ORCHESTRATION_SPEC`**, **`AI_PILOT_AND_CONTINUE`** §4; **[`SECURITY.md`](SECURITY.md)** *Related docs* lists **`docs/README`** (*E1 / pytest*); **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)** *Related documentation* (*Docs index* row) tags **E1 / pytest**; E1 evidence **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** (*Phase 2 vs in-repo honesty*) updated.
- **`docs/README.md`** (*E1 / pytest*) and **`docs/PM_STAGE_MAP.md`** (*E1 STEP 1*) — cross-links to **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)**, **`le-vibe/tests/`**, **`SESSION_ORCHESTRATION_SPEC`**, and **`AI_PILOT_AND_CONTINUE`** §4.
- **`docs/SESSION_ORCHESTRATION_SPEC.md`**, **`docs/AI_PILOT_AND_CONTINUE.md`** §4, and **`spec.md`** — E1 (**§1**/**H8** + §5–§10) / **`le-vibe/tests/`** pointers for orchestration, Continue / **Please continue**, and Phase 1 navigation.
- **`le-vibe/README.md`** *Development* / **Tests** — same E1 roster + **`python3 -m pytest`** as root **`README.md`**; **`debian/le-vibe.README.Debian`** *Authority* points **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** / **`le-vibe/tests/`** for clone-based QA.
- **`PRODUCT_SPEC` §10** (regression evidence line lists **§1**/**H8** + §7–§10) and root **`README.md`** *Tests* — full **E1 mapping** roster (**`test_product_spec_section8.py`**, **`test_continue_workspace.py`** / **`test_workspace_hub.py`**, **`test_session_orchestrator.py`**, **`test_root_readme_ai_pilot_contract.py`**, **`test_le_vibe_readme_e1_contract.py`**, **`test_prompt_build_orchestrator_fence.py`**, **`test_issue_template_h8_contract.py`**, **`test_ci_yml_submodules_contract.py`**) plus **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** pointer.
- **Phase 2 / §14:** [`spec-phase2.md`](spec-phase2.md) names **`test_root_readme_ai_pilot_contract.py`**, **`test_prompt_build_orchestrator_fence.py`**, and **`test_issue_template_h8_contract.py`** as honesty guards for README §7.1, the Master orchestrator fence, and **H8** issue-template anchors; **[`SECURITY.md`](SECURITY.md)** and **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)** cross-link E1 + **`le-vibe/tests/`** for §8 posture.
- **E1 / §7.1:** Root **`README.md`** *Please continue* / **AI Pilot** copy is regression-tested by [`le-vibe/tests/test_root_readme_ai_pilot_contract.py`](le-vibe/tests/test_root_readme_ai_pilot_contract.py); **[`docs/README.md`](docs/README.md)** (*PRODUCT_SPEC_SECTION8_EVIDENCE* row) cites that test. **[`docs/screenshots/README.md`](docs/screenshots/README.md)** points accidental sensitive captures at **[`SECURITY.md`](SECURITY.md)**.
- **H8 / `.github/` (CI, Dependabot, ISSUE_TEMPLATE + config.yml # H8):** [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/) intros name **`docs/PM_STAGE_MAP` STEP 12** and **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** (E1 audit); **[`SECURITY.md`](../SECURITY.md)** *Related docs* adds **`PM_STAGE_MAP`** (§14 triage) and **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** (E1).
- **H5 / STEP 11:** [`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md) **STEP 11** *Also read* lists [`docs/screenshots/README.md`](docs/screenshots/README.md) alongside **`packaging/icons/`**; [`docs/brand-assets.md`](docs/brand-assets.md), [`docs/screenshots/README.md`](docs/screenshots/README.md), [`docs/README.md`](docs/README.md), root [`README.md`](README.md) (dedicated **H5** line, parallel to **H8** / **STEP 12** for **`.github/`**), [`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md) (*Related documentation*: **H5** + **Roadmap** → **STEP 12**), and E1 ([`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)) cross-link the same orchestrator stage.
- Product / trust alignment: **`spec-phase2.md` §14** (what **`r-vibe`** ships vs **H6** editor fork / **H7** Flatpak–style bundles) cross-linked from **`docs/PRODUCT_SPEC.md` §9**, **`debian/le-vibe.README.Debian`**, **`debian/control`**, packaging **Product / trust** headers (scripts, **`PATH`** wrappers, `.desktop` files), **`.github/`** (**`ci.yml`**, **`dependabot.yml`**, **`ISSUE_TEMPLATE` + `config.yml` `#` H8**), and **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** (E1).
- **H8 / optional RAG / `PRODUCT_SPEC` §10 honesty:** **`docs/rag/le-vibe-phase2-chunks.md`** (*RAG / embeddings*, non-canonical) and **`spec-phase2.md` §14** (*Honesty vs CI* + optional-chunk table row) aligned with **`SECURITY`** *Related docs*, **`.github/ISSUE_TEMPLATE/`** (bug / feature / documentation), **`PM_STAGE_MAP` STEP 12**, **`docs/PROMPT_BUILD_LE_VIBE.md`** intro, root **`README`**, **`privacy-and-telemetry`** *Reporting issues*, **`README.Debian`**, and packaging **`#`** headers — **E1** maintains issue-template YAML; **`pytest`** does not parse it.
- **H2 / Dependabot:** **[`.github/dependabot.yml`](.github/dependabot.yml)** header and cross-links in root **`README`**, **`docs/PROMPT_BUILD_LE_VIBE.md`**, **`docs/sbom-signing-audit.md`**, and E1 evidence align weekly **pip** / **GitHub Actions** bump PRs with **`pip-audit`**, **`CHANGELOG.md`**, and **`PRODUCT_SPEC` §8–§9**.

## [0.1.1] — 2026-04-12

### Documentation

- **`debian/le-vibe.README.Debian`** (installed as **`/usr/share/doc/le-vibe/README.Debian`**): **H6** note for full clones — after **`git submodule update --init --recursive`**, run **`./editor/smoke.sh`** from the repository root for the same layout / script-syntax checks as **`build-le-vibe-ide.yml`** (no Electron compile).

## [0.1.0] — 2026-04-11

### Added

- Debian package skeleton: Python stack under `/usr/share/le-vibe`, `le-vibe` and `le-vibe-setup-continue` on `PATH`, `.desktop`, icon, man pages.
- Managed Ollama on dedicated port **11435**, first-run flow, Continue config generation and setup scripts.
- CI: pytest, `.deb` build, `SHA256SUMS`, CycloneDX SBOM, `pip-audit`, lintian (errors fail).

### Notes

- Code - OSS / VSCodium binary is **not** bundled; install separately or set **`LE_VIBE_EDITOR`**.

<!-- When tagging, add compare links, e.g. [0.1.0]: https://github.com/org/repo/releases/tag/v0.1.0 -->
