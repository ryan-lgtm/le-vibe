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

test('OPERATOR.md cross-links README issues + GitHub source (task-n27-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n27-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Issues / bugs (task-n25-1)'));
  assert.ok(text.includes('Source on GitHub (task-n26-1)'));
  assert.ok(text.includes('bugs.url'));
  assert.ok(text.includes('homepage'));
});

test('OPERATOR.md cross-links README monorepo clone (task-n29-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n29-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Monorepo clone (task-n28-1)'));
  assert.ok(text.includes('repository'));
  assert.ok(text.includes('directory'));
});

test('OPERATOR.md cross-links README SPDX license (task-n31-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n31-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('License (task-n30-1)'));
  assert.ok(text.includes('license'));
  assert.ok(text.includes('SPDX'));
});

test('OPERATOR.md cross-links README publisher (task-n33-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n33-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Publisher (task-n32-1)'));
  assert.ok(text.includes('publisher'));
});

test('OPERATOR.md cross-links README keywords (task-n35-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n35-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Keywords (task-n34-1)'));
  assert.ok(text.includes('keywords'));
});

test('OPERATOR.md cross-links README categories (task-n37-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n37-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Categories (task-n36-1)'));
  assert.ok(text.includes('categories'));
});

test('OPERATOR.md cross-links README displayName (task-n39-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n39-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Display name (task-n38-1)'));
  assert.ok(text.includes('displayName'));
});

test('OPERATOR.md cross-links README description (task-n41-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n41-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Description (task-n40-1)'));
  assert.ok(text.includes('description'));
});

test('OPERATOR.md cross-links README package name (task-n43-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n43-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Package name (task-n42-1)'));
  assert.ok(text.includes('name'));
});

test('OPERATOR.md cross-links README version (task-n45-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n45-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Version (task-n44-1)'));
  assert.ok(text.includes('version'));
});

test('OPERATOR.md cross-links README engines.vscode minimum (task-n47-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n47-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Editor API minimum (task-n46-1)'));
  assert.ok(text.includes('engines.vscode'));
});

test('OPERATOR.md cross-links README engines.node minimum (task-n49-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n49-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Node runtime minimum (task-n48-1)'));
  assert.ok(text.includes('engines.node'));
});

test('OPERATOR.md cross-links README activationEvents docs (task-n51-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n51-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation events (task-n50-1)'));
  assert.ok(text.includes('activationEvents'));
});

test('OPERATOR.md cross-links README activationEvents command example (task-n53-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n53-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation event example (task-n52-1)'));
  assert.ok(text.includes('activationEvents'));
});

test('OPERATOR.md cross-links README startup activation intent (task-n55-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n55-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Startup activation intent (task-n54-1)'));
  assert.ok(text.includes('onStartupFinished'));
});

test('OPERATOR.md cross-links README activation example lookup (task-n57-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n57-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation example lookup (task-n56-1)'));
  assert.ok(text.includes('activationEvents'));
});

test('OPERATOR.md cross-links README activation count rationale lookup (task-n59-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n59-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation count rationale lookup (task-n58-1)'));
  assert.ok(text.includes('activationEvents'));
});

test('OPERATOR.md cross-links README activation docs quick index (task-n63-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n63-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation docs quick index (task-n62-1)'));
  assert.ok(text.includes('activation'));
});

test('OPERATOR.md cross-links README activation docs sequence (task-n61-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n61-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation docs sequence (task-n60-1)'));
  assert.ok(text.includes('activation'));
});

test('OPERATOR.md cross-links README activation index next hop (task-n65-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n65-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation index next hop (task-n64-1)'));
  assert.ok(text.includes('activation'));
});

test('OPERATOR.md cross-links README quick-index sequence token (task-n67-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n67-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation docs quick index (task-n62-1)'));
  assert.ok(text.includes('Activation docs sequence (task-n60-1)'));
});

test('OPERATOR.md cross-links README activation sequence return hop (task-n69-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n69-1'));
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Activation sequence return hop (task-n68-1)'));
  assert.ok(text.includes('Activation docs quick index (task-n62-1)'));
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

test('OPERATOR.md documents regression golden fixtures (task-n15-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n15-2'));
  assert.ok(text.includes('test/fixtures/n15-2'));
  assert.ok(text.includes('n15-2-golden-regression.test.js'));
});

test('OPERATOR.md documents GitHub Actions CI for extension verify (task-n16-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('.github/workflows/le-vibe-native-extension-ci.yml'));
  assert.ok(text.includes('npm ci'));
  assert.ok(text.includes('npm run verify'));
  assert.ok(text.includes('editor/le-vibe-native-extension'));
  assert.ok(text.includes('branch protection'));
});

test('OPERATOR.md documents VSIX packaging + install (task-n16-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('vsce package'));
  assert.ok(text.includes('npm run package'));
  assert.ok(text.includes('le-vibe-native-extension-0.1.0.vsix'));
  assert.ok(text.includes('code --install-extension'));
  assert.ok(text.includes('*.vsix'));
});

test('OPERATOR.md documents CHANGELOG ships in VSIX via .vscodeignore (task-n22-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('ships in the VSIX (task-n22-1)'));
  assert.ok(text.includes('`CHANGELOG.md`'));
  assert.ok(text.includes('.vscodeignore'));
});

test('OPERATOR.md documents VSIX manual install spot-check (task-n23-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Manual spot-check (task-n23-1)'));
  assert.ok(text.includes('Lé Vibe Native Agent'));
  assert.ok(text.includes('displayName'));
});

test('OPERATOR.md documents alternate CLI for VSIX install (task-n24-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Alternate CLI (task-n24-1)'));
  assert.ok(text.includes('codium'));
  assert.ok(text.includes('--install-extension'));
});

test('OPERATOR.md documents version bump vs deb/git (task-n16-3)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('task-n16-3'));
  assert.ok(text.includes('package.json'));
  assert.ok(text.includes('debian/changelog'));
  assert.ok(text.includes('Version bump checklist'));
  assert.ok(text.includes('git tag'));
  assert.ok(text.includes('GitHub Release'));
});

test('OPERATOR.md documents command palette inventory pointer (task-n17-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Command palette inventory (task-n17-1)'));
  assert.ok(text.includes('Command palette and keyboard shortcuts (task-n17-1)'));
  assert.ok(text.includes('Keyboard Shortcuts'));
});

test('OPERATOR.md documents panel accessibility pointer (task-n17-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Panel accessibility (task-n17-2)'));
  assert.ok(text.includes('Accessibility (task-n17-2)'));
});

test('OPERATOR.md documents status bar entry (task-n17-3)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Status bar (task-n17-3)'));
  assert.ok(text.includes('status-bar-entry.js'));
  assert.ok(text.includes('leVibeNative.showStatusBarEntry'));
});

test('OPERATOR.md documents Security notes + npm audit triage (task-n18-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Security notes (task-n18-1)'));
  assert.ok(text.includes('npm audit'));
  assert.ok(text.includes('package-lock.json'));
  assert.ok(text.includes('overrides'));
  assert.ok(text.includes('github.com/ryan-lgtm/le-vibe/issues'));
});

test('OPERATOR.md documents flake hunt loop + pass count (task-n18-2)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Flake resistance (task-n18-2)'));
  assert.ok(text.includes('for i in $(seq 1 10)'));
  assert.ok(text.includes('10/10'));
  assert.ok(text.includes('Intentionally skipped tests'));
});

test('OPERATOR.md documents CHANGELOG pointer (task-n19-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('CHANGELOG (task-n19-1)'));
  assert.ok(text.includes('CHANGELOG.md'));
});
