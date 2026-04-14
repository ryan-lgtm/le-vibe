# Lé Vibe

<p align="center">
  <img src="packaging/icons/hicolor/scalable/apps/le-vibe.svg" alt="Lé Vibe logo" width="120" />
</p>

**Lé Vibe** is an open-source, **local-first** coding environment: a **Code OSS–class desktop editor**, the [**Continue**](https://continue.dev) assistant, and [**Ollama**](https://ollama.com) on your own machine—so you get serious AI help without handing your workflow to a hosted IDE or cloud inference by default.

You open a project, chat and edit with Continue, and run models locally. The product is **not** Microsoft Visual Studio Code; the editor lineage is **Code - OSS** / **VSCodium**–style tooling with Lé Vibe branding when you build the full IDE from this repository.

---

## Install the editor / IDE

### Linux

**Supported today (one-shot from source):** **Debian and derivatives** that use **`apt`** and **`dpkg`** (e.g. **Ubuntu**, **Linux Mint**, **Pop!_OS**, **elementary**). The canonical path compiles the Lé Vibe editor, builds **`le-vibe`** + **`le-vibe-ide`** packages, and can install them locally—see **[`docs/LOCAL_INSTALL_ONE_SHOT.md`](docs/LOCAL_INSTALL_ONE_SHOT.md)** for time, disk, and troubleshooting.

1. **Clone** the repository **with submodules** (the editor sources live under `editor/vscodium/`):

   ```bash
   git clone --recurse-submodules <your-r-vibe-repo-url>
   cd r-vibe
   ```

   If you already cloned without submodules:

   ```bash
   git submodule update --init editor/vscodium
   ```

2. **Full local install (one command)** — build, verify, and (optionally) install both `.deb` packages:

   ```bash
   ./packaging/scripts/install-le-vibe-local.sh --preflight-only    # checks only; no compile
   ./packaging/scripts/install-le-vibe-local.sh                     # build .debs + STEP 14 verify
   ./packaging/scripts/install-le-vibe-local.sh --install --yes     # same + sudo apt install + smoke
   ```

   Deeper detail, expectations, and ship checklist notes: **[`docs/LOCAL_INSTALL_ONE_SHOT.md`](docs/LOCAL_INSTALL_ONE_SHOT.md)** · **[`docs/SHIP_REPORT_LOCAL_INSTALL.md`](docs/SHIP_REPORT_LOCAL_INSTALL.md)**.

**Other Linux distributions** (Fedora, RHEL, Arch, openSUSE, etc.): there is **no** single maintained one-shot installer in this repo yet—the scripted path above assumes **Debian-style** packaging. You can still build from source using **[`editor/BUILD.md`](editor/BUILD.md)** and the packaging notes under **`packaging/debian-le-vibe-ide/`**, or run the Debian-oriented flow inside a **container/VM** that provides `apt`.

### macOS

**Coming soon.** The maintained build and packaging paths in this repository target **Linux** first. On macOS you can explore **[`editor/BUILD.md`](editor/BUILD.md)** and upstream VSCodium docs for local development, but there is no supported one-command Lé Vibe IDE install yet.

### Windows

**Coming soon.** There is no supported Windows installer or documented end-to-end compile path for the Lé Vibe IDE shell in this repository yet.

---

## How the agents work

Lé Vibe uses an operator-led orchestration model: the operator agent sets goals and constraints, then specialized subagents collaborate to deliver implementation, review, and validation. For higher-risk work, subagents are expected to debate alternatives with evidence and converge on the best path before code lands.

- User-friendly overview and orchestrator behavior: [`docs/AGENT_MODE_ORCHESTRATION.md`](docs/AGENT_MODE_ORCHESTRATION.md)
- Repeatable 70-session hardening backlog (one session per task): [`docs/AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md`](docs/AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md)
- Canonical loop prompt entrypoint: [`docs/MASTER_ITERATION_LOOP.md`](docs/MASTER_ITERATION_LOOP.md)

If you want to run iterative engineering sessions, use the copy/paste prompt in the session playbook and increment session numbers sequentially.

---

## Documentation & project depth

- **Maintainer / engineering index:** [`docs/README.md`](docs/README.md) — roadmap docs, packaging, CI, trust.
- **Full narrative formerly on this page** (orchestration, CI, E1 test anchors): [`docs/MONOREPO_DEVELOPER_REFERENCE.md`](docs/MONOREPO_DEVELOPER_REFERENCE.md).
- **Product spec:** [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md) · **Stage map:** [`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md).

---

## License

The Lé Vibe bootstrap and packaging in this repository are licensed under the **MIT License** — see [`LICENSE`](LICENSE). Third-party components (Ollama, VSCodium, Continue, upstream editor) have their own licenses.

**Security:** [`SECURITY.md`](SECURITY.md).
