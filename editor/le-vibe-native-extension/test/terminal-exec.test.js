'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { runCommandInVisibleTerminal, clearTerminalSessionAllow, LEVIBE_CHAT_TERMINAL_NAME } = require('../terminal-exec.js');

function makeVscodeMock(overrides = {}) {
  const sendTextCalls = [];
  const created = [];
  const cfg = {
    terminalExecutionEnabled: true,
    terminalCommandAllowPatterns: ['git *'],
    terminalCommandDenyPatterns: [],
    terminalSkipBatchConfirmation: false,
    ...overrides.config,
  };
  const mock = {
    workspace: {
      getConfiguration: () => ({
        get: (key, def) => (key in cfg ? cfg[key] : def),
      }),
      workspaceFolders: overrides.workspaceFolders !== undefined ? overrides.workspaceFolders : [{ uri: { fsPath: '/tmp/levibe-ws' } }],
    },
    window: {
      terminals: overrides.terminals !== undefined ? overrides.terminals : [],
      showWarningMessage: overrides.showWarningMessage || (async () => 'Run in integrated terminal'),
      createTerminal: (opts) => {
        const t = {
          name: opts.name,
          cwd: opts.cwd,
          show: () => {},
          sendText: (text, execute) => {
            sendTextCalls.push({ text, execute });
          },
        };
        created.push(t);
        mock.window.terminals = [...mock.window.terminals, t];
        return t;
      },
    },
    env: {},
  };
  mock._sendTextCalls = sendTextCalls;
  mock._createdTerminals = created;
  mock._exitSubs = [];
  if (overrides.onDidEndTerminalShellExecution === 'track') {
    mock.window.onDidEndTerminalShellExecution = (fn) => {
      mock._exitSubs.push(fn);
      return { dispose: () => {} };
    };
  }
  return mock;
}

test('runCommandInVisibleTerminal: policy block shows warning and does not sendText (task-n13-2)', async () => {
  clearTerminalSessionAllow();
  const vscode = makeVscodeMock({
    config: { terminalExecutionEnabled: false },
  });
  let warned = false;
  vscode.window.showWarningMessage = async () => {
    warned = true;
    return undefined;
  };
  const r = await runCommandInVisibleTerminal(vscode, 'git status', {});
  assert.equal(r.ok, false);
  assert.ok(warned);
  assert.equal(vscode._sendTextCalls.length, 0);
});

test('runCommandInVisibleTerminal: confirm then visible terminal sendText (task-n13-2)', async () => {
  clearTerminalSessionAllow();
  const vscode = makeVscodeMock({});
  const r = await runCommandInVisibleTerminal(vscode, 'git status', {});
  assert.equal(r.ok, true);
  assert.equal(vscode._sendTextCalls.length, 1);
  assert.equal(vscode._sendTextCalls[0].text, 'git status');
  assert.equal(vscode._sendTextCalls[0].execute, true);
  assert.equal(vscode._createdTerminals.length, 1);
  assert.equal(vscode._createdTerminals[0].name, LEVIBE_CHAT_TERMINAL_NAME);
});

test('runCommandInVisibleTerminal: cancel does not sendText', async () => {
  clearTerminalSessionAllow();
  const vscode = makeVscodeMock({});
  vscode.window.showWarningMessage = async () => 'Cancel';
  const r = await runCommandInVisibleTerminal(vscode, 'git status', {});
  assert.equal(r.ok, false);
  assert.equal(r.reason, 'cancelled');
  assert.equal(vscode._sendTextCalls.length, 0);
});

test('runCommandInVisibleTerminal: terminalSkipBatchConfirmation skips modal', async () => {
  clearTerminalSessionAllow();
  const vscode = makeVscodeMock({ config: { terminalSkipBatchConfirmation: true } });
  let modalCalls = 0;
  vscode.window.showWarningMessage = async () => {
    modalCalls += 1;
    return 'Run in integrated terminal';
  };
  const r = await runCommandInVisibleTerminal(vscode, 'git status', {});
  assert.equal(r.ok, true);
  assert.equal(modalCalls, 0);
  assert.equal(vscode._sendTextCalls.length, 1);
});

test('runCommandInVisibleTerminal: session skip after flag skips second modal', async () => {
  clearTerminalSessionAllow();
  const vscode = makeVscodeMock({});
  let modalCalls = 0;
  vscode.window.showWarningMessage = async () => {
    modalCalls += 1;
    return 'Run and skip further prompts (this session)';
  };
  const r1 = await runCommandInVisibleTerminal(vscode, 'git status', {});
  assert.equal(r1.ok, true);
  assert.equal(modalCalls, 1);
  const r2 = await runCommandInVisibleTerminal(vscode, 'git diff', {});
  assert.equal(r2.ok, true);
  assert.equal(modalCalls, 1);
  assert.equal(vscode._sendTextCalls.length, 2);
  clearTerminalSessionAllow();
});

test('runCommandInVisibleTerminal: appends audit sent line with cwd (task-n13-3)', async () => {
  clearTerminalSessionAllow();
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tex-audit-'));
  const auditPath = path.join(dir, 'terminal-command-audit.jsonl');
  const vscode = makeVscodeMock({});
  const r = await runCommandInVisibleTerminal(vscode, 'git status', { auditPath });
  assert.equal(r.ok, true);
  const raw = fs.readFileSync(auditPath, 'utf8').trim();
  const row = JSON.parse(raw.split('\n')[0]);
  assert.equal(row.phase, 'sent');
  assert.equal(row.cwd, '/tmp/levibe-ws');
  assert.equal(row.command_line, 'git status');
  assert.equal(row.exit_code, null);
  assert.ok(row.audit_id);
});

test('runCommandInVisibleTerminal: shell_ended audit when onDidEndTerminalShellExecution matches (task-n13-3)', async () => {
  clearTerminalSessionAllow();
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tex-audit-'));
  const auditPath = path.join(dir, 'terminal-command-audit.jsonl');
  const vscode = makeVscodeMock({ onDidEndTerminalShellExecution: 'track' });
  const r = await runCommandInVisibleTerminal(vscode, 'git status', { auditPath });
  assert.equal(r.ok, true);
  assert.equal(vscode._exitSubs.length, 1);
  const term = vscode._createdTerminals[0];
  vscode._exitSubs[0]({
    terminal: term,
    exitCode: 0,
    execution: { commandLine: 'git status' },
  });
  const lines = fs.readFileSync(auditPath, 'utf8').trim().split('\n');
  assert.equal(lines.length, 2);
  const ended = JSON.parse(lines[1]);
  assert.equal(ended.phase, 'shell_ended');
  assert.equal(ended.exit_code, 0);
  assert.equal(JSON.parse(lines[0]).audit_id, ended.audit_id);
});
