# Changelog

All notable changes to **Lé Vibe Native Agent** / **Lé Vibe Chat** in this package are documented here. Versions follow **`package.json`** semver. Epic-level delivery history lives in the monorepo product track (see below).

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
