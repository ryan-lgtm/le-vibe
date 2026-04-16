# Changelog

All notable changes to **Lé Vibe Native Agent** / **Lé Vibe Chat** in this package are documented here. Versions follow **`package.json`** semver. Epic-level delivery history lives in the monorepo product track (see below).

## [Unreleased]

### Added

- Milestone EPIC A (chat surface shell): the panel now uses a dedicated tabbed workspace (`Chat`, `Settings`, `Logs`, `Tools`) so the main conversation feed stays focused while startup/remediation controls, diagnostics, and operational actions live in separate surfaces.
- Keyboard-accessible tab navigation with WAI-ARIA roles (`tablist`, `tab`, `tabpanel`) and arrow/home/end support for panel switching.
- Milestone EPIC B (composer interaction model): chat composer now supports `Enter` to send, `Shift+Enter` for newline, immediate clear-on-send, local user echo in the timeline, and auto-grow up to 12 visible rows.
- Composer visual refresh for dark-theme chat ergonomics with high-contrast foreground and reduced friction for longer prompt drafting.

### Fixed

- Default **`leVibeNative.ollamaEndpoint`** aligns with **`lvibe`** managed Ollama (**`http://127.0.0.1:11435`**, see `LE_VIBE_MANAGED_OLLAMA_PORT`). The previous default (`11434`) targeted a different listener than the launcher, which commonly produced **404** on **`POST /api/generate`** (wrong daemon and/or model not present there). User-visible diagnostics now hint when Ollama returns **404** (missing model vs endpoint mismatch).
- When the user has **not** overridden **`leVibeNative.ollamaEndpoint`**, the extension reads **`~/.config/le-vibe/managed_ollama.json`** (written by **`lvibe`**) and uses that **`host:port`** so readiness and chat track the managed Ollama instance even on older VSIX defaults or stale editor settings.
- Chat now retries once with an installed local model tag when Ollama returns **HTTP 404** for the configured model (common model-missing case on an otherwise healthy endpoint).
- Added command **`leVibeNative.openOllamaLogging`** and panel button **Ollama Logging** to open a live tail terminal for Ollama logs (`~/.ollama/logs/server.log`, `~/.ollama-serve.log`, `journalctl -u ollama`, fallback to `~/.config/le-vibe/le-vibe.log.jsonl`).
- Streaming requests no longer inherit the short health-probe timeout; stream HTTP timeout now floors to a higher value (`>= 15s` and aligned with stream stall guard) to avoid premature **`OLLAMA_TIMEOUT`** while local models warm/load.
- Robust model resolution: when **`leVibeNative.ollamaModel`** is not explicitly set, the extension now prefers launcher lock file **`~/.config/le-vibe/locked-model.json`** (`ollama_model`), then installed model inventory on the active endpoint, before falling back to static defaults.

## [0.1.0] - 2026-04-15

### Added

- First-party **Lé Vibe Chat** VS Code extension: deterministic readiness panel and agent surface (no blank/gray startup), local-first **Ollama** integration with streaming chat, cancel, and retries.
- Bounded chat transcript persistence under `~/.config/le-vibe/levibe-native-chat/` with user-visible caps and export/clear.
- Agentic editor flows: structured **edit proposals**, unified **diff preview**, **Accept / Reject / Apply**, stale-file conflict detection, **WorkspaceEdit** apply with undo-friendly transactions.
- **Composer-style** validated workspace plans (progress, cancel, rollback, dry-run) and guarded workspace file ops (create/move/delete with confirmation and audit where required).
- **Copilot-like** affordances: selection → chat, quick actions, optional **@file** / **@folder** / outline context (bounded caps).
- **Terminal execution** policy (off by default), visible integrated terminal runs, command audit JSONL when enabled.
- Operator handoff contract, third-party migration guide, feature-flag rollout, CI **`npm run verify`**, VSIX packaging path, optional status bar entry, accessibility and flake-resistance notes in **`OPERATOR.md`**.

### Notes

- Full epic/task history (N0–N18+): **`.lvibe/workflows/native-extension-product-track.md`** in the monorepo.
