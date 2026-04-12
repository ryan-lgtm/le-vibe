# le-vibe

Hardware-aware one-shot **launcher** for local vibe coding with [Ollama](https://ollama.com) and the [Continue](https://continue.dev) extension (Code - OSS / **Lé Vibe**, not Microsoft’s VS Code distribution). It detects your OS and hardware, installs Ollama if needed, **starts the Ollama API** on `127.0.0.1:11434` by default (platform script, then `ollama serve` if needed), picks a **best-fit** model from the DeepSeek R1 ladder (with Qwen coder fallbacks), pulls it, and writes a ready-to-import Continue config under `output/`.

For **Lé Vibe Phase 2** (managed Ollama on a dedicated port, configs under `~/.config/le-vibe/`), see the [repository README](../README.md).

**Authority:** Must-ship behavior — [`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md). Phase 1/2 specs — [`../spec.md`](../spec.md), [`../spec-phase2.md`](../spec-phase2.md). **Optional RAG / embeddings** (not canonical): [`../docs/rag/le-vibe-phase2-chunks.md`](../docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview`) — see **`spec-phase2.md`** *RAG / embeddings*. PM session & orchestration — [`../docs/SESSION_ORCHESTRATION_SPEC.md`](../docs/SESSION_ORCHESTRATION_SPEC.md), [`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md). Maintainer doc index (Roadmap **H1–H8**) — [`../docs/README.md`](../docs/README.md) (**`PRODUCT_SPEC` §9** *Maintainer index*).

**Trust / H8 (parent repository):** [`../SECURITY.md`](../SECURITY.md) (*Related docs* — **`docs/README`** *Product surface* / **ISSUE_TEMPLATE** optional **`rag/...`*); [`../docs/privacy-and-telemetry.md`](../docs/privacy-and-telemetry.md) (*E1 contract tests* row); [`../docs/README.md`](../docs/README.md) *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** ([`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) **`#` H8** lines; same chain as root [`README.md`](../README.md) *Documentation index & privacy*).

**Phase 2 vs this tree:** [`../spec-phase2.md`](../spec-phase2.md) **§14** — **monorepo:** **`le-vibe/`** (this package) + **[`../editor/`](../editor/)** (Lé Vibe IDE shell, **H6**); **H7** Flatpak may stay out-of-tree by policy.

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

**Tests:** From this directory, **`pytest tests/`** runs the full suite. **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](../docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** maps **§1**/**H8** + §5–§10 to modules; contract highlights include **`test_product_spec_section8.py`**, **`test_continue_workspace.py`** / **`test_workspace_hub.py`** (§7.2 — **`.continue/rules`** + **`.lvibe/AGENTS.md`**, **numbered questions**), **`test_session_orchestrator.py`** (**STEP 2** — **`session-manifest`** ↔ **`schemas/`**), **`test_root_readme_ai_pilot_contract.py`** (repo root **`README.md`** §7.1 + **E1** roster), **`test_prompt_build_orchestrator_fence.py`** (**`docs/PROMPT_BUILD_LE_VIBE.md`** orchestrator fence), **`test_issue_template_h8_contract.py`** (**H8** — **`.github/ISSUE_TEMPLATE/*.yml`**). See the [repository README](../README.md) *Tests* section for the same roster.

```bash
pip install -r requirements.txt
pip install pytest
python3 -m pytest tests/
```
