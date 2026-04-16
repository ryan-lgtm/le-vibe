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
  assert.equal(command.category, 'Lé Vibe Chat');
  assert.equal(command.title, 'Open Agent Surface');
  assert.ok(commands.find((item) => item.command === 'leVibeNative.pickContextFile'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.startNewChatSession'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.restoreRecentPrompt'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.clearContextFiles'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.emitOperatorHandoff'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.openThirdPartyMigrationGuide'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.applySelectionDemoReplace'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.createWorkspaceFile'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.createWorkspaceFolder'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.moveWorkspacePath'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.deleteWorkspacePath'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.askChatAboutSelection'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.runCommandInIntegratedTerminal'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.clearTerminalSessionAllow'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.addContextAtFile'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.addContextAtFolder'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.addCurrentFileOutlineToContext'));
  assert.ok(commands.find((item) => item.command === 'leVibeNative.packageRunbookDiagnostics'));
});

test('manifest supports deterministic activation entrypoints', () => {
  const activationEvents = packageJson.activationEvents || [];
  assert.ok(
    activationEvents.includes('onCommand:leVibeNative.openAgentSurface'),
    'expected command activation event',
  );
  assert.ok(activationEvents.includes('onStartupFinished'), 'expected startup activation event');
  assert.ok(activationEvents.includes('onCommand:leVibeNative.pickContextFile'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.startNewChatSession'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.restoreRecentPrompt'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.emitOperatorHandoff'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.openThirdPartyMigrationGuide'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.applySelectionDemoReplace'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.createWorkspaceFile'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.createWorkspaceFolder'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.moveWorkspacePath'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.deleteWorkspacePath'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.runCommandInIntegratedTerminal'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.clearTerminalSessionAllow'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.addContextAtFile'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.addContextAtFolder'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.addCurrentFileOutlineToContext'));
  assert.ok(activationEvents.includes('onCommand:leVibeNative.packageRunbookDiagnostics'));
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
  assert.equal(extensionModule.ASK_CHAT_ABOUT_SELECTION_COMMAND, 'leVibeNative.askChatAboutSelection');
  assert.equal(extensionModule.RUN_COMMAND_IN_INTEGRATED_TERMINAL_COMMAND, 'leVibeNative.runCommandInIntegratedTerminal');
  assert.equal(extensionModule.CLEAR_TERMINAL_SESSION_ALLOW_COMMAND, 'leVibeNative.clearTerminalSessionAllow');
  assert.equal(extensionModule.ADD_CONTEXT_AT_FILE_COMMAND, 'leVibeNative.addContextAtFile');
  assert.equal(extensionModule.ADD_CONTEXT_AT_FOLDER_COMMAND, 'leVibeNative.addContextAtFolder');
  assert.equal(extensionModule.ADD_CURRENT_FILE_OUTLINE_COMMAND, 'leVibeNative.addCurrentFileOutlineToContext');
  assert.equal(extensionModule.PACKAGE_RUNBOOK_DIAGNOSTICS_COMMAND, 'leVibeNative.packageRunbookDiagnostics');
  assert.equal(extensionModule.START_NEW_CHAT_SESSION_COMMAND, 'leVibeNative.startNewChatSession');
  assert.equal(extensionModule.RESTORE_RECENT_PROMPT_COMMAND, 'leVibeNative.restoreRecentPrompt');
  assert.equal(typeof extensionModule.buildSelectionAssistQuickFixes, 'function');
  assert.equal(path.basename(require.resolve('../extension')), 'extension.js');
});

test('buildSelectionAssistQuickFixes returns selection fallback quick-fix actions when inline is disabled (task-cp4-3)', () => {
  const fakeVscode = {
    workspace: {
      getConfiguration() {
        return { get() { return false; } };
      },
      getWorkspaceFolder() {
        return { uri: { toString() { return 'file:///ws'; } } };
      },
    },
    CodeActionKind: { QuickFix: 'quickfix' },
    CodeAction: class {
      constructor(title, kind) {
        this.title = title;
        this.kind = kind;
        this.command = null;
      }
    },
  };
  const out = extensionModule.buildSelectionAssistQuickFixes(
    fakeVscode,
    { uri: { scheme: 'file' } },
    { isEmpty: false },
  );
  assert.equal(Array.isArray(out), true);
  assert.equal(out.length >= 3, true);
  assert.equal(out[0].command.command, 'leVibeNative.askChatAboutSelection');
});

test('buildSelectionAssistQuickFixes returns empty when inline is enabled (task-cp4-3)', () => {
  const fakeVscode = {
    workspace: {
      getConfiguration() {
        return { get() { return true; } };
      },
      getWorkspaceFolder() {
        return { uri: { toString() { return 'file:///ws'; } } };
      },
    },
    CodeActionKind: { QuickFix: 'quickfix' },
    CodeAction: class {
      constructor(title, kind) {
        this.title = title;
        this.kind = kind;
        this.command = null;
      }
    },
  };
  const out = extensionModule.buildSelectionAssistQuickFixes(
    fakeVscode,
    { uri: { scheme: 'file' } },
    { isEmpty: false },
  );
  assert.deepEqual(out, []);
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
    assert.ok(html.includes('MAX_COMPOSER_ROWS = 12'));
    assert.ok(html.includes("if (event.shiftKey)"));
    assert.ok(html.includes("appendLine('User: ' + trimmed)"));
    assert.ok(html.includes("appendLine('Assistant:')"));
    assert.ok(html.includes('background: #2f3338;'));
    assert.ok(html.includes('New chat'));
    assert.ok(html.includes('Restore recent…'));
    assert.ok(html.includes('Lé Vibe Chat storage'));
    assert.ok(html.includes('View usage'));
    assert.ok(html.includes('Export transcript'));
    assert.ok(html.includes('Clear transcript'));
    assert.ok(html.includes('Add context file'));
    assert.ok(html.includes('.gitignore'));
    assert.ok(html.includes('Clear context'));
    assert.ok(html.includes('Emit handoff event'));
    assert.ok(html.includes('Third-party agent migration'));
    assert.ok(html.includes('Open migration guide'));
    assert.ok(html.includes('Edit preview (workspace)'));
    assert.ok(html.includes('Preview sample workspace edit'));
    assert.ok(html.includes('Validate proposal JSON'));
    assert.ok(html.includes('editProposalInput'));
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
    assert.ok(html.includes('quickActionExplain'));
    assert.ok(html.includes('task-n12-2'));
    assert.ok(html.includes('Terminal execution (N13)'));
    assert.ok(html.includes('runCommandInIntegratedTerminalPrompt'));
    assert.ok(html.includes('addContextAtFile'));
    assert.ok(html.includes('addContextAtFolder'));
    assert.ok(html.includes('addCurrentFileOutline'));
  });
});
