# Lé Vibe Native Extension — operator quick reference

Use this sheet when validating or shipping the first-party extension (`editor/le-vibe-native-extension/`).

**Prerequisites:** **Node.js 18+** on your PATH to run **`npm run verify`** / **`npm test`** (uses `node:test`). The VS Code extension host ships its own runtime; the Node engine is for this package’s scripts and CI only. For installing or running the extension in an editor, match **`engines.vscode`** in `package.json` — currently **VS Code 1.85+** (or a compatible build such as **VSCodium** meeting the same API level). Contributor-oriented wording for the same Node and editor requirements is in **`README.md`** (*Prerequisites (developers)*).

`package.json` includes **`repository.directory`**, **`homepage`**, **`bugs`**, and **`keywords`** so tooling and registries can link to the monorepo path and issue tracker. It also declares **`publisher`** and **`license`** (SPDX string) for marketplace and CI identity.

**Extension host entry:** **`package.json`** **`main`** must be **`./extension.js`** (VS Code activation entry; required for packaging).

**Local-first:** the shipped defaults target **local Ollama** (see `leVibeNative.ollamaEndpoint`); the extension does **not** silently fall back to a cloud LLM.

**Default local Ollama URL:** **`http://127.0.0.1:11434`** — configure via **`leVibeNative.ollamaEndpoint`** (smoke’s default probe matches unless `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` is set).

**Default Ollama probe timeout:** **`2500` ms** — configure via **`leVibeNative.ollamaTimeoutMs`** (smoke override **`LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`**; same default as the smoke table below).

**Default local model tag:** **`mistral:latest`** — **`leVibeNative.ollamaModel`** (used for streaming generate requests).

**Ollama retries:** **`leVibeNative.ollamaMaxRetries`** default **`2`**, base backoff **`leVibeNative.ollamaRetryBackoffMs`** default **`400` ms** (transient `GET /api/tags` and streaming `POST /api/generate`).

**Telemetry:** defaults to **local structured logs only**; there is **no** remote telemetry unless the user **explicitly opts in**.

**Canonical user-facing name (chat UX):** **Lé Vibe Chat** — palette titles and panel copy use this name for the agent surface (per product track).

## Verify (canonical)

From this directory:

```bash
npm run verify
```

Runs **`npm test`** then **`npm run smoke`**. Green = all unit tests pass; smoke confirms non-blank panel HTML, optional `lvibe` launcher string check when the full monorepo is present, a best-effort local Ollama probe (non-fatal if Ollama is down unless strict mode is on), and prints the **canonical first-party persisted config directory** (from `storage-inventory.js`) before `smoke: done`.

### Smoke environment (optional)

| Variable | Effect |
|----------|--------|
| `LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1` | Fail smoke if Ollama is unreachable (use on a machine with Ollama). |
| `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` | Override default `http://127.0.0.1:11434`. |
| `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS` | Override Ollama probe timeout (default `2500`). |
| `LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1` | Skip `packaging/bin/lvibe` check (extension-only tree). |

## Bounded persistence

All extension-owned files live under **`~/.config/le-vibe/levibe-native-chat/`**. See **`README.md`** (section *Bounded persistence inventory*) and **`storage-inventory.js`** (`levibeNativeChatDir`, `PERSISTED_ARTIFACTS`).

Chat transcript JSONL is capped by **`leVibeNative.chatTranscriptMaxBytes`** (default **524288** bytes) and **`leVibeNative.chatTranscriptMaxMessages`** (default **200** JSONL rows) (oldest-first compaction with an explicit system stub when limits are hit — details in README).

## Product track

Workflow board: **`.lvibe/workflows/native-extension-product-track.md`** (Epic N8 — operator runbook).
