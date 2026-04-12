# Privacy and telemetry (Lé Vibe stack)

This document describes what **this repository** (the **`le-vibe`** Python bootstrap, launcher, and Debian packaging) does **not** collect, and points you to upstream components that have their own policies.

## Related documentation

| Topic | Location |
|-------|----------|
| **Must-ship product requirements** (naming, paths, model lock, `.lvibe/`) | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) |
| **Authority roster** (single table: `PROMPT_BUILD`, `SESSION_ORCHESTRATION_SPEC`, `PM_STAGE_MAP`, evidence, `AI_PILOT`) | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §9 |
| **Secrets / agent rules (`.env`, `.lvibe/` RAG)** — §8 | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8; root [`SECURITY.md`](../SECURITY.md); E1 audit [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) + **`le-vibe/tests/`** |
| **Docs index** (all guides; **Roadmap H1–H8** maintainer topics per **§9** *Maintainer index*; **E1 / pytest**; optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** for embeddings — **`spec-phase2.md`** *RAG / embeddings*) | [`README.md`](README.md) |
| **E1 contract tests** (§1 / **H8** naming + §5–§10; no network) | Root [`README.md`](../README.md) *Tests*; [`../le-vibe/README.md`](../le-vibe/README.md) — [`test_le_vibe_readme_e1_contract.py`](../le-vibe/tests/test_le_vibe_readme_e1_contract.py) (*Tests* roster vs root *E1 mapping*); [`../le-vibe/tests/`](../le-vibe/tests/) — [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md); [`test_product_spec_section8.py`](../le-vibe/tests/test_product_spec_section8.py) (*Prioritization* / **`ide-ci-metadata.txt`** / **`retention-days`** / **`permissions:`** **`contents: read`**, **`actions: write`** / **`editor/BUILD.md`** / **`editor/VENDORING.md`**); **H8** reporter YAML anchors — [`test_issue_template_h8_contract.py`](../le-vibe/tests/test_issue_template_h8_contract.py); **STEP 14** / **H6** — [`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md) — [`test_editor_le_vibe_overrides_readme_contract.py`](../le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py); [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) — [`test_build_le_vibe_ide_workflow_contract.py`](../le-vibe/tests/test_build_le_vibe_ide_workflow_contract.py) |
| **Brand / screenshots (Roadmap H5)** — no extra telemetry; marketing framing must stay honest vs **§14**; **§1** incl. **H8** **`.github/`** (*Naming* in **brand-assets**) | [`brand-assets.md`](brand-assets.md); [`screenshots/README.md`](screenshots/README.md); **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) STEP 11** |
| **`.deb` post-install** (paths, **§5** consent summary, authority pointers) | [`le-vibe.README.Debian`](../debian/le-vibe.README.Debian) → **`/usr/share/doc/le-vibe/README.Debian`** |
| **PM session manifest & orchestration** | [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) |
| **Structured logging** (operator troubleshooting) | Root [`README.md`](../README.md) § *Troubleshooting*; env **`LE_VIBE_STRUCTURED_LOG=0`** |
| **Security reporting** | Root [`SECURITY.md`](../SECURITY.md) |
| **Roadmap** (orchestrator **H5–H8** themes; **H8** = CI / Dependabot / **ISSUE_TEMPLATE/** + **`config.yml`** **`#` H8** / **`.github`**) | [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md); **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) STEP 12** (H8); [`README.md`](README.md) *Product surface* (**`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**, *E1 contract tests* row on this page, [`SECURITY.md`](../SECURITY.md) *Related docs*) |
| **Phase 2 narrative vs this repo** (honest scope — **H6** / **H7** deferrals) | [`spec-phase2.md`](../spec-phase2.md) §14 |
| **Release notes / dependency bumps** (cross-check with **H2** **`pip-audit`**) | Root [`CHANGELOG.md`](../CHANGELOG.md); [`sbom-signing-audit.md`](sbom-signing-audit.md) |

## Lé Vibe (this repo)

- **Network:** The bootstrap and launcher focus on **localhost** services. Managed **Ollama** binds to **`127.0.0.1`** on the dedicated port (**`11435`** by default) — see [`spec-phase2.md`](../spec-phase2.md). There is **no** Lé Vibe–owned analytics endpoint, advertising ID, or crash reporter in the Python code shipped here.
- **Config and state:** Paths are under **`~/.config/le-vibe/`** (and related XDG locations). They stay on your machine unless **you** copy or sync them elsewhere.
- **Structured logs (operator observability):** Lé Vibe may append **JSON Lines** to **`~/.config/le-vibe/le-vibe.log.jsonl`** (managed Ollama, first-run bootstrap, launcher session events). This file is **local only**—nothing is sent to a Lé Vibe–operated analytics endpoint. Disable with **`LE_VIBE_STRUCTURED_LOG=0`**. See the root **`README.md`** (troubleshooting).
- **First-run / `ollama pull`:** Model downloads talk to **Ollama** / registry endpoints as configured by **Ollama** — that traffic is **not** invented by Lé Vibe beyond invoking **`ollama`** the same way you would on the CLI.

## Continue (extension)

**Continue** is a separate product with its own license and privacy practices. Lé Vibe generates a **`continue-config.yaml`** that points **`apiBase`** at your **local** Ollama URL; it does **not** change Continue’s own telemetry or cloud features if you enable them in the extension. Read **Continue**’s documentation and settings for anything beyond local chat.

## Editor (VSCodium / Code OSS)

**VSCodium** and other **Code - OSS** builds may include update checks, marketplace calls, and extension hosts. That behavior is **upstream** of Lé Vibe. Use the editor’s settings and documentation to limit network use if you need an air-gapped workflow.

## Debian package

The **`.deb`** installs files under **`/usr/share/le-vibe`**, **`/usr/bin`**, and standard **hicolor** icon paths. It does not add a background service that exfiltrates data; **managed Ollama** runs only when **you** launch **`le-vibe`**.

## Reporting issues

If you believe a **Lé Vibe** script or packaged file violates this intent, open an issue with reproduction steps — on **GitHub**, choose **Bug report** (or **Feature request** / **Documentation**) from **`.github/ISSUE_TEMPLATE/`** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines). Template intros follow **Roadmap H8** — same **`docs/README`** *Product surface* / **`SECURITY`** *Related docs* chain as CI (**`ci.yml`**, **`dependabot.yml`**) and optional **`docs/rag/le-vibe-phase2-chunks.md`** (**`spec-phase2.md` §14**, non-canonical). For **Continue** or **VSCodium** behavior, prefer their respective projects unless the bug is clearly in our config or launcher.

For **security-sensitive** reports, see **[`SECURITY.md`](../SECURITY.md)**.

Roadmap reference: **H8** in [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).
