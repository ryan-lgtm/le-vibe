# Lé Vibe Native Extension — operator quick reference

Use this sheet when validating or shipping the first-party extension (`editor/le-vibe-native-extension/`).

`package.json` includes a **`repository.directory`** field so marketplace and tooling resolve this package to its path inside the **r-vibe** monorepo.

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
| `LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1` | Skip `packaging/bin/lvibe` check (extension-only tree). |

## Bounded persistence

All extension-owned files live under **`~/.config/le-vibe/levibe-native-chat/`**. See **`README.md`** (section *Bounded persistence inventory*) and **`storage-inventory.js`** (`levibeNativeChatDir`, `PERSISTED_ARTIFACTS`).

## Product track

Workflow board: **`.lvibe/workflows/native-extension-product-track.md`** (Epic N8 — operator runbook).
