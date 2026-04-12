# Project Spec: le-vibe — Cross-Platform Ollama Bootstrapper with Hardware-Based Model Matching

**Product name (user-facing):** **Lé Vibe**. **Must-ship requirements** that span bootstrap, CLI, workspace **`.lvibe/`**, welcome UX, and gitignore behavior: **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)**.

**Phase 2 (Linux IDE product):** **[`spec-phase2.md`](spec-phase2.md)** (**monorepo:** **`le-vibe/`** + **`editor/`**; **§14** inventory) — **`docs/PRODUCT_SPEC.md`** wins on conflicts.

**Navigation:** [`docs/README.md`](docs/README.md) — maintainer index for **Roadmap H1–H8** (per **`PRODUCT_SPEC` §9** *Maintainer index*). **Authority roster** — [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) §9. **Acceptance / E1:** [`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md) (**§1**/**H8** + §5–§10; filename historic) and [`le-vibe/tests/`](le-vibe/tests/) (clone the **`r-vibe`** tree to run **`pytest`**). Root [`README.md`](README.md) *Tests* + [`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md) (*E1 contract tests* row) list the same contract modules. **[`SECURITY.md`](SECURITY.md)** (*Related docs*) mirrors **`docs/README`** *Product surface* (**H8** — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**, **`privacy-and-telemetry`** *E1 contract tests*). **Optional RAG chunks:** [`docs/rag/le-vibe-phase2-chunks.md`](docs/rag/le-vibe-phase2-chunks.md) (`lv-meta-overview` — **§9** / **E1**/**H8** / **§14** pointers for embeddings; not canonical — see **`spec-phase2.md`** *RAG / embeddings*). **`PRODUCT_SPEC` §10** + **`spec-phase2.md` §14** (*Honesty vs CI*): **`.github/ISSUE_TEMPLATE/`** intros (**`config.yml`** **`#`** maintainer lines; incl. optional **`rag/...`**) are **E1**-maintained — **`pytest`** does not *parse* YAML structure; **[`test_issue_template_h8_contract.py`](le-vibe/tests/test_issue_template_h8_contract.py)** locks **STEP 12** / **`config.yml`** / **H8** substring anchors only — **`spec-phase2.md` §14** *Honesty vs CI* enumerates further **`pytest`** guards (STEP 2 manifest ↔ **`schemas/`**, root / package **`README`** **E1** mapping strings, STEP 16 orchestrator fence).

**Debian package (Linux):** [`debian/le-vibe.README.Debian`](debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow, **§5** **`.lvibe/`** consent, **Phase 2** scope (**`editor/`** / Flatpak — **`spec-phase2.md` §14**), pointers to **`docs/PRODUCT_SPEC.md`** / **`docs/README.md`** (see **`PRODUCT_SPEC` §9** *Maintainer index* and **[`spec-phase2.md`](spec-phase2.md)** *Debian install*).

## Goal

Build a one-shot bootstrapper that prepares a machine for local AI-assisted coding with Ollama, automatically selects the **best compatible local model based on available hardware**, starts Ollama in the background, and provides the user with a ready-to-use **Code - OSS** + **Continue**-oriented setup for a free local vibe-coding workflow.

The bootstrapper must support:
- Windows 10/11
- macOS 14+
- Debian-based Linux distributions

The bootstrapper must:
1. Detect OS, architecture, CPU, RAM, disk, and GPU.
2. Install Ollama if missing.
3. Validate and install safe prerequisites needed to run Ollama.
4. Evaluate the machine’s practical model ceiling.
5. Automatically choose the **best available model tier the hardware can run comfortably**.
6. Prefer the newest practical DeepSeek model family available in Ollama, but fall back through lower tiers if needed.
7. Pull the selected model.
8. Start Ollama in the background on the standard local endpoint.
9. Generate and print VS Code + Continue setup instructions.
10. Print clear instructions for how to stop the Ollama service later.

---

## Core product behavior

The user runs a single command. The script:
- inspects the machine,
- installs Ollama if needed,
- determines the best-fit local model,
- downloads it,
- starts Ollama,
- confirms the API is reachable at `http://127.0.0.1:11434`,
- generates a Continue config,
- prints setup and stop instructions,
- exits only when the environment is ready.

This is a **best-fit installer**, not a fixed-model installer.

---

## Key design change

### Old behavior
“Install a 32B+ model, and if not possible, fail or degrade awkwardly.”

### New behavior
“Choose the strongest realistic local model for this machine, in descending order of capability.”

The script must never assume 32B is possible. It must instead:
- test hardware,
- determine a comfort tier,
- try higher-value models first,
- fall back safely and automatically.

---

## Model selection philosophy

The bootstrapper should choose the **best coding-capable or reasoning-capable local model that the hardware can run well enough to be useful for real-world coding workflows**.

Priority order:
1. Highest-quality practical DeepSeek model available in Ollama that fits hardware comfortably
2. Next-best smaller DeepSeek model
3. Strong coder/reasoner fallback model if DeepSeek is unavailable or impractical
4. Small autocomplete helper model as an optional companion

The model choice should optimize for:
- coding usefulness,
- multi-file edit support through local tooling,
- markdown/project-doc comprehension,
- acceptable responsiveness,
- realistic memory pressure,
- stable local operation.

---

## Hardware-aware matching requirements

Create a model selection engine that scores the machine and chooses the best-fit tier.

### Input signals
The script must detect:
- OS and version
- CPU architecture
- total RAM
- available RAM
- free disk space
- GPU vendor and model
- available VRAM if detectable
- Apple Silicon unified memory where applicable
- NVIDIA driver readiness if NVIDIA GPU is present
- whether the system appears GPU-accelerated, CPU-only, or hybrid

### Output classification
The script must classify the machine into one of these tiers:

- `tier_70b_candidate`
- `tier_32b_comfortable`
- `tier_32b_possible_but_slow`
- `tier_14b_comfortable`
- `tier_8b_comfortable`
- `tier_small_fallback_only`

The script must then choose the highest recommended available model that maps to that tier.

### Comfort definition
A model is **comfortable** if it is likely to be usable for real coding work without making the machine miserable:
- acceptable startup and generation time,
- no obvious memory thrashing,
- no dangerously high sustained system pressure,
- enough free disk for model files and runtime,
- no unreasonable CPU-only penalty unless the user explicitly allows it.

A model is **possible but slow** if it might technically run but should not be the default.

The bootstrapper should default to **comfortable**, not merely **possible**.

---

## Model fallback ladder

The script must implement a descending fallback ladder.

### Preferred family
Use the DeepSeek family first when available in Ollama.

### Example fallback chain
Try, in order, with remote validation of exact tags:

1. `deepseek-r1:70b`
2. `deepseek-r1:32b`
3. `deepseek-r1:14b`
4. `deepseek-r1:8b`
5. `deepseek-r1:7b`
6. `deepseek-r1:1.5b`

If DeepSeek tags are unavailable, impractical, or not ideal for coding UX, allow a secondary fallback family for autocomplete or coding assistance such as a Qwen coder model, but keep DeepSeek as the primary default family when feasible. Continue’s docs support exact model tags or `AUTODETECT`, and Ollama’s model library exposes DeepSeek R1 in multiple tags. [web:58][web:80][web:81]

### Selection rule
The script must:
- inspect the highest tier first,
- check if the machine qualifies comfortably,
- verify the exact tag exists,
- select that model,
- otherwise continue down the chain,
- stop at the first comfortable valid option.

If no model is comfortable, choose the strongest “small fallback” and explicitly tell the user that local capability is limited on this hardware.

---

## Supported endpoint behavior

Use Ollama’s default local API endpoint:
- host: `127.0.0.1`
- port: `11434`

Default API base:
- `http://localhost:11434`

Do not expose on non-local interfaces by default. Ollama’s local API does not require authentication on localhost. [web:90][web:85]

---

## Tech stack

Implement using:
- Python 3 as the main orchestrator
- PowerShell helpers for Windows
- Bash helpers for macOS and Linux

Optional output files:
- `output/bootstrap-report.md`
- `output/continue-config.yaml`
- `output/model-decision.json`

---

## Deliverables

```text
le-vibe/
  README.md
  bootstrap.py
  requirements.txt
  scripts/
    install_windows.ps1
    install_macos.sh
    install_linux.sh
    start_windows.ps1
    start_macos.sh
    start_linux.sh
    stop_windows.ps1
    stop_macos.sh
    stop_linux.sh
  templates/
    continue-config.yaml.j2
    report.md.j2
  output/
    bootstrap-report.md
    continue-config.yaml
    model-decision.json
```

---

## Runtime phases

### Phase 1: Detect environment
Gather:
- OS name/version
- CPU model and arch
- RAM total/free
- disk total/free
- GPU(s)
- VRAM if possible
- Ollama installed?
- Ollama running?
- port 11434 already bound?

Write findings into a structured state object.

### Phase 2: Validate prerequisites
Check:
- admin/elevation only if needed
- internet access
- package manager availability
- basic tools like `curl`, `tar`, `wget` if needed
- GPU tool availability like `nvidia-smi` when NVIDIA exists

The script may safely install lightweight helper dependencies. It must not silently replace GPU drivers.

### Phase 3: Install or update Ollama
Use official install paths by OS.
Verify:
```bash
ollama --version
```

### Phase 4: Evaluate model ceiling
Implement a scoring engine.

#### Scoring factors
- RAM score
- VRAM/GPU score
- CPU score
- disk score
- OS compatibility score

#### Example guidance
This is heuristic, not absolute:
- 70B candidate:
  - very high memory class or unusually strong local setup
- 32B comfortable:
  - ~32GB-class memory footprint available with strong GPU/unified memory support
- 32B possible but slow:
  - near threshold but likely slower than desired
- 14B comfortable:
  - good mainstream high-end laptop/desktop tier
- 8B comfortable:
  - broad fallback tier
- small fallback only:
  - constrained or CPU-only systems

The script must log:
- selected tier
- rejected higher tiers
- reasons for each rejection

### Phase 5: Discover available model tags
Use one or more of:
- `ollama search`
- known validated tags
- `ollama pull` dry-check behavior if necessary

The script must not assume every desired tag exists forever.
It must verify exact tags before selection.

### Phase 6: Choose best compatible model
Implement:
```python
choose_best_model(hardware, available_tags, user_override=None) -> ModelDecision
```

Return:
```json
{
  "selected_model": "deepseek-r1:14b",
  "selected_tier": "tier_14b_comfortable",
  "comfortable": true,
  "reason": "32B rejected due to insufficient comfortable memory headroom; 14B is the highest practical stable tier.",
  "rejected_candidates": [
    {
      "model": "deepseek-r1:32b",
      "reason": "insufficient comfortable headroom"
    }
  ]
}
```

### Phase 7: Pull selected model
Use:
```bash
ollama pull <exact-tag>
```

Then verify:
```bash
ollama list
```

### Phase 8: Start Ollama in background
Start Ollama using the default local endpoint and ensure it remains available:
- Windows: background app or managed process
- macOS: background process or app launch
- Debian Linux: prefer `systemd`, fallback to user background process

Verify:
- API responds at `http://127.0.0.1:11434`
- no duplicate processes are spawned
- process/service info is written to the report

### Phase 9: Generate Continue config
Generate a ready-to-paste config for Continue using the **exact selected model tag** (Lé Vibe **must-ship**: persist that concrete tag under `~/.config/le-vibe/locked-model.json`; do not rely on AUTODETECT as the only stored value when a tag is known — see [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)).

Use a template like:

```yaml
name: Lé Vibe (Ollama local)
version: 0.0.1
schema: v1

models:
  - name: Lé Vibe (locked local)
    provider: ollama
    model: {{ selected_model }}
    apiBase: http://localhost:11434
    roles:
      - chat
      - edit
      - apply
      - autocomplete
```

(Continue upstream still allows `AUTODETECT` in some flows; the **product** config uses one locked tag for all roles.)

### Phase 10: Print final instructions
Print:
- selected model
- why it was chosen
- local endpoint
- Continue setup steps
- exact stop/start/status commands for the OS

---

## VS Code / Continue instructions

At the end of execution, print something like:

```text
Ollama is running locally at:
http://127.0.0.1:11434

Selected model:
<exact-model-tag>

Why this model was chosen:
<plain English explanation>

To connect VS Code:
1. Install the Continue extension.
2. Open Continue config.
3. Import or paste:
   ./output/continue-config.yaml
4. Confirm apiBase is:
   http://localhost:11434
5. Choose the local model in Continue.

To stop Ollama later:
<OS-specific command>
```

---

## Required functions

Implement at minimum:

```python
detect_os() -> OSInfo
detect_hardware() -> HardwareInfo
check_prerequisites() -> list[CheckResult]
install_ollama() -> None
get_available_model_tags() -> list[str]
score_model_tier(hardware) -> TierAssessment
choose_best_model(hardware, available_tags, user_override=None) -> ModelDecision
pull_model(model_tag) -> None
is_ollama_running(host, port) -> bool
start_ollama_service(host, port) -> ServiceResult
generate_continue_config(model_tag, host, port) -> Path
generate_report(state) -> Path
print_final_instructions(state) -> None
```

---

## Safety constraints

- Do not promise a 32B model if the machine cannot run it comfortably.
- Do not install or replace GPU drivers automatically without user confirmation.
- Do not expose Ollama on public interfaces by default.
- Do not overwrite existing Continue configs without creating a backup.
- Do not kill a running Ollama instance unless the script started it or the user confirms.

---

## Reporting requirements

Generate `output/bootstrap-report.md` containing:
- detected hardware
- prerequisites and install results
- selected tier
- selected model
- rejected larger candidate models and reasons
- service status
- endpoint verification
- Continue instructions
- stop/start/status instructions

Also generate `output/model-decision.json` for machine-readable diagnostics.

---

## CLI flags

Support:
```bash
python3 bootstrap.py --dry-run
python3 bootstrap.py --force-reinstall
python3 bootstrap.py --model deepseek-r1:14b
python3 bootstrap.py --allow-slow
python3 bootstrap.py --host 127.0.0.1 --port 11434
python3 bootstrap.py --yes
python3 bootstrap.py --verbose
```

### Flag behavior
- `--model`:
  - force a user-requested model if possible
  - if not practical, explain why and fail safely unless `--allow-slow` is present
- `--allow-slow`:
  - allows choosing a “possible but slow” model tier instead of the default “comfortable only”

---

## Acceptance criteria

The project is complete when:
- it installs or validates Ollama on a supported machine,
- it evaluates hardware and chooses a model based on fit,
- it falls back automatically when a higher tier is not realistic,
- it pulls the exact selected model,
- it starts Ollama successfully,
- it verifies `http://127.0.0.1:11434`,
- it generates a Continue config using the exact installed model tag or autodetect,
- it prints clear stop instructions.

---

## Testing matrix

Test:
1. Strong machine that qualifies for 32B
2. Mid-tier machine that should fall to 14B
3. Smaller machine that should fall to 8B
4. Constrained machine that should fall to 1.5B or small fallback
5. Existing Ollama install without a model
6. Existing Ollama service already running
7. Invalid forced model override
8. Port 11434 already in use

The tests must confirm that fallback selection behaves correctly.

---

## Final instruction to Cursor

Build the complete **le-vibe** project, not pseudocode.

The script must be robust, conservative, and honest:
- pick the highest practical model,
- fall back automatically when needed,
- explain its decisions clearly,
- prioritize local usability over ambitious but slow model picks,
- leave the user with a working local coding setup.