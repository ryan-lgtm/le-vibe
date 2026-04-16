const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const packageJson = require('../package.json');
const extensionModule = require('../extension');
const { STARTUP_STATES, getStateContent } = require('../readiness');

test('manifest contributes Lé Vibe Open Agent Surface command', () => {
  const commands = packageJson.contributes && packageJson.contributes.commands;
  assert.ok(Array.isArray(commands), 'contributes.commands must be an array');
  const command = commands.find((item) => item.command === 'leVibeNative.openAgentSurface');
  assert.ok(command, 'expected leVibeNative.openAgentSurface command contribution');
  assert.equal(command.title, 'Lé Vibe: Open Agent Surface');
  assert.ok(commands.find((item) => item.command === 'leVibeNative.pickContextFile'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.clearContextFiles'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.emitOperatorHandoff'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.openThirdPartyMigrationGuide'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.applySelectionDemoReplace'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.createWorkspaceFile'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.createWorkspaceFolder'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.moveWorkspacePath'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.deleteWorkspacePath'));
});

test('manifest supports deterministic activation entrypoints', () => {
  const activationEvents = packageJson.activationEvents || [];
  assert.ok(
    activationEvents.includes('onCommand:leVibeNative.openAgentSurface'),
    'expected command activation event',
  );
  assert.ok(activationEvents.includes('onStartupFinished'), 'expected startup activation event');
  assert.ok(activationEvents.includes('onCommand:leVibeNative.pickContextFile'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.emitOperatorHandoff'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.openThirdPartyMigrationGuide'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.applySelectionDemoReplace'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.createWorkspaceFile'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.createWorkspaceFolder'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.moveWorkspacePath'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.deleteWorkspacePath'));
});

test('extension exports activate/deactivate and command constant', () => {
  assert.equal(typeof extensionModule.activate, 'function');
  assert.equal(typeof extensionModule.deactivate, 'function');
  assert.equal(extensionModule.OPEN_AGENT_SURFACE_COMMAND, 'leVibeNative.openAgentSurface');
  assert.equal(extensionModule.OPEN_THIRD_PARTY_MIGRATION_COMMAND, 'leVibeNative.openThirdPartyMigrationGuide');
  assert.equal(extensionModule.APPLY_SELECTION_DEMO_REPLACE_COMMAND, 'leVibeNative.applySelectionDemoReplace');
  assert.equal(extensionModule.CREATE_WORKSPACE_FILE_COMMAND, 'leVibeNative.createWorkspaceFile');
  assert.equal(extensionModule.CREATE_WORKSPACE_FOLDER_COMMAND, 'leVibeNative.createWorkspaceFolder');
  assert.equal(extensionModule.MOVE_WORKSPACE_PATH_COMMAND, 'leVibeNative.moveWorkspacePath');
  assert.equal(extensionModule.DELETE_WORKSPACE_PATH_COMMAND, 'leVibeNative.deleteWorkspacePath');
  assert.equal(path.basename(require.resolve('../extension')), 'extension.js');
});

test('readiness state set includes required startup states', () => {
  assert.deepEqual(STARTUP_STATES, [
    'checking',
    'ready',
    'needs_ollama',
    'needs_model',
    'needs_auth_or_setup',
  ]);
});

test('every non-ready state has actionable remediation buttons', () => {
  ['needs_ollama', 'needs_model', 'needs_auth_or_setup'].forEach((state) => {
    const content = getStateContent(state);
    assert.ok(Array.isArray(content.actions), `expected actions array for ${state}`);
    assert.ok(content.actions.length > 0, `expected at least one action for ${state}`);
  });
});

test('first-run wizard HTML is non-empty and branded', () => {
  const html = extensionModule.firstRunWizardHtml(0);
  assert.ok(html.includes('Lé Vibe Chat — Welcome'));
  assert.ok(html.includes('wizNext') || html.includes('wizFinish'));
});

test('panel HTML is never blank and includes state indicator', () => {
  STARTUP_STATES.forEach((state) => {
    const html = extensionModule.panelHtml(state);
    assert.ok(html.includes('Lé Vibe Native Startup'));
    assert.ok(html.includes(`<strong>${state}</strong>`), `expected state marker for ${state}`);
    assert.ok(html.includes('Send Prompt'));
    assert.ok(html.includes('Cancel Request'));
    assert.ok(html.includes('Retry last prompt'));
    assert.ok(html.includes('Lé Vibe Chat storage'));
    assert.ok(html.includes('View usage'));
    assert.ok(html.includes('Export transcript'));
    assert.ok(html.includes('Clear transcript'));
    assert.ok(html.includes('Add context file'));
    assert.ok(html.includes('Clear context'));
    assert.ok(html.includes('Emit handoff event'));
    assert.ok(html.includes('Third-party agent migration'));
    assert.ok(html.includes('Open migration guide'));
    assert.ok(html.includes('Edit preview (workspace)'));
    assert.ok(html.includes('Preview sample workspace edit'));
    assert.ok(html.includes('editPreviewApply'));
    assert.ok(html.includes('Workspace plan (demo)'));
    assert.ok(html.includes('Dry-run sample plan'));
    assert.ok(html.includes('Run sample workspace plan'));
    assert.ok(html.includes('cancelWorkspacePlanRun'));
    assert.ok(html.includes('undoWorkspacePlanRollback'));
    assert.ok(html.includes('Workspace scaffold (N11)'));
    assert.ok(html.includes('createWorkspaceFilePrompt'));
    assert.ok(html.includes('moveWorkspacePathPrompt'));
    assert.ok(html.includes('deleteWorkspacePathPrompt'));
  });
});
