const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('OPERATOR.md exists and documents verify + persistence pointers', () => {
  const p = path.join(__dirname, '..', 'OPERATOR.md');
  assert.ok(fs.existsSync(p));
  const text = fs.readFileSync(p, 'utf8');
  assert.ok(text.includes('npm run verify'));
  assert.ok(text.includes('storage-inventory.js'));
  assert.ok(text.includes('levibe-native-chat'));
});

test('OPERATOR.md mentions package.json discovery fields (task-n8-14)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('homepage'));
  assert.ok(text.includes('bugs'));
  assert.ok(text.includes('keywords'));
  assert.ok(text.includes('repository.directory'));
});

test('OPERATOR.md mentions publisher and license (task-n8-16)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('publisher'));
  assert.ok(text.includes('license'));
  assert.ok(text.includes('SPDX'));
});

test('OPERATOR.md documents engines.vscode / minimum editor version (task-n8-17)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('engines.vscode'));
  assert.ok(text.includes('1.85'));
  assert.ok(text.includes('VSCodium'));
});

test('OPERATOR.md cross-links README prerequisites for contributors (task-n8-19)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Prerequisites (developers)'));
});

test('OPERATOR.md states local-first Ollama default without silent cloud fallback (task-n8-22)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Local-first'));
  assert.ok(text.includes('local Ollama'));
  assert.ok(text.includes('silent'));
  assert.ok(text.toLowerCase().includes('cloud'));
});

test('OPERATOR.md documents telemetry as local-by-default with explicit opt-in only (task-n8-25)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Telemetry'));
  assert.ok(text.includes('local structured logs'));
  assert.ok(text.includes('explicitly opts in'));
});

test('OPERATOR.md bounded persistence names transcript retention settings (task-n8-28)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('leVibeNative.chatTranscriptMaxBytes'));
  assert.ok(text.includes('leVibeNative.chatTranscriptMaxMessages'));
  assert.ok(text.includes('compaction'));
});

test('OPERATOR.md documents package.json main extension entry (task-n8-31)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Extension host entry'));
  assert.ok(text.includes('./extension.js'));
  assert.ok(text.includes('main'));
});

test('OPERATOR.md documents default local Ollama URL and settings key (task-n8-34)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('http://127.0.0.1:11434'));
  assert.ok(text.includes('leVibeNative.ollamaEndpoint'));
  assert.ok(text.includes('LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT'));
});

test('OPERATOR.md documents leVibeNative.ollamaTimeoutMs and smoke timeout override (task-n8-39)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Default Ollama probe timeout'));
  assert.ok(text.includes('leVibeNative.ollamaTimeoutMs'));
  assert.ok(text.includes('LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS'));
});

test('OPERATOR.md documents default Ollama model tag and leVibeNative.ollamaModel (task-n8-43)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Default local model tag'));
  assert.ok(text.includes('mistral:latest'));
  assert.ok(text.includes('leVibeNative.ollamaModel'));
});

test('OPERATOR.md documents settings disclosure guardrail test (task-n8-55)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Settings disclosure guardrail'));
  assert.ok(text.includes('package-leVibeNative-keys-doc-inventory.test.js'));
  assert.ok(text.includes('leVibeNative.*'));
});

test('OPERATOR.md documents scripts literal umbrella guardrail test (task-n8-64)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Scripts literal umbrella'));
  assert.ok(text.includes('package-json-all-scripts-doc-literal-sync.test.js'));
});

test('OPERATOR.md documents Product track workflow path (task-n8-66)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('## Product track'));
  assert.ok(text.includes('`.lvibe/workflows/native-extension-product-track.md`'));
  assert.ok(text.includes('Epic N8'));
});

test('OPERATOR.md documents WorkspaceEdit apply + manual undo (task-n9-3)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('workspace.applyEdit'));
  assert.ok(text.includes('workspace-edit-apply.js'));
  assert.ok(text.includes('Manual check'));
});

test('OPERATOR.md documents partial selection apply command (task-n9-4)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('leVibeNative.applySelectionDemoReplace'));
  assert.ok(text.includes('selection-apply.js'));
});

test('OPERATOR.md documents edit preview stale conflict (task-n9-5)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('edit-conflict.js'));
  assert.ok(text.includes('task-n9-5'));
});

test('OPERATOR.md documents workspace plan validation (task-n10-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('workspace-plan.js'));
  assert.ok(text.includes('levibe.workspace_plan.v1'));
});

test('OPERATOR.md documents workspace plan execution + audit (task-n10-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n10-2'));
  assert.ok(text.includes('workspace-plan-exec.js'));
  assert.ok(text.includes('workspace-plan-audit.jsonl'));
});

test('OPERATOR.md documents workspace plan rollback (task-n10-3)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n10-3'));
  assert.ok(text.includes('Undo completed steps'));
  assert.ok(text.includes('workspace_plan_rollback'));
});

test('OPERATOR.md documents workspace plan dry-run (task-n10-4)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n10-4'));
  assert.ok(text.includes('Dry-run sample plan'));
  assert.ok(text.includes('workspace-plan-dry-run.js'));
});

test('OPERATOR.md documents workspace scaffold create file/folder (task-n11-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n11-1'));
  assert.ok(text.includes('workspace-fs-actions.js'));
  assert.ok(text.includes('leVibeNative.openDocumentAfterWorkspaceCreate'));
});

test('OPERATOR.md documents workspace move/rename (task-n11-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n11-2'));
  assert.ok(text.includes('moveWorkspaceEntry'));
  assert.ok(text.includes('renameFile'));
});

test('OPERATOR.md documents workspace delete + audit (task-n11-3)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n11-3'));
  assert.ok(text.includes('deleteWorkspaceEntry'));
  assert.ok(text.includes('workspace-fs-ops-audit.jsonl'));
  assert.ok(text.includes('workspace_fs_ops_audit'));
});

test('OPERATOR.md documents workspace context read guards (task-n11-4)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n11-4'));
  assert.ok(text.includes('context-file-guards.js'));
  assert.ok(text.includes('contextMaxCharsPerFile'));
});

test('OPERATOR.md documents selection to chat (task-n12-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n12-1'));
  assert.ok(text.includes('leVibeNative.askChatAboutSelection'));
  assert.ok(text.includes('selection-chat-context.js'));
});

test('OPERATOR.md documents quick action templates (task-n12-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n12-2'));
  assert.ok(text.includes('chat-quick-actions.js'));
  assert.ok(text.includes('QUICK_ACTION_TEMPLATES'));
});

test('OPERATOR.md documents E2E agentic editor release checklist + sign-off (task-n15-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n15-1'));
  assert.ok(text.includes('E2E agentic editor release checklist'));
  assert.ok(text.includes('Preview sample workspace edit'));
  assert.ok(text.includes('Accept preview'));
  assert.ok(text.includes('Apply to file'));
  assert.ok(text.includes('Run sample workspace plan'));
  assert.ok(text.includes('Cancel plan run'));
  assert.ok(text.includes('Sign-off (per release)'));
});
