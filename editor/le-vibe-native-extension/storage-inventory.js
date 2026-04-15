'use strict';

const path = require('node:path');
const os = require('node:os');

/**
 * Single canonical directory for first-party Lé Vibe Native Chat persisted files (task-n8-2).
 * Keep in sync with `chat-transcript.js` / `first-run-wizard.js` / `operator-handoff.js` / `third-party-migration.js`.
 */
function levibeNativeChatDir() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'levibe-native-chat');
}

/**
 * Known artifacts (basename → purpose). Does not include per-workspace transcript files (`transcript-*.jsonl`).
 */
const PERSISTED_ARTIFACTS = Object.freeze([
  { basename: 'first-run-wizard.json', purpose: 'First-run wizard checkpoints (schema first_run_wizard.v1).' },
  { basename: 'operator-handoff-audit.jsonl', purpose: 'Append-only operator handoff events (lvibe.operator_handoff.v1).' },
  { basename: 'third-party-migration-state.json', purpose: 'Third-party migration status (third_party_migration.v1).' },
  { basename: 'third-party-migration-audit.jsonl', purpose: 'Append-only migration actions (lvibe.third_party_migration.v1).' },
  { basename: 'transcript-*.jsonl', purpose: 'Per-workspace bounded chat JSONL (hash suffix); not a single fixed file.' },
]);

module.exports = {
  levibeNativeChatDir,
  PERSISTED_ARTIFACTS,
};
