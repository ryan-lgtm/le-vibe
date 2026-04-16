'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  terminalCommandAuditPath,
  buildTerminalCommandAuditSent,
  buildTerminalCommandAuditEnded,
  appendTerminalCommandAudit,
} = require('../terminal-command-audit.js');

test('buildTerminalCommandAuditSent includes cwd and null exit_code (task-n13-3)', () => {
  const e = buildTerminalCommandAuditSent({
    auditId: 'a1',
    workspaceUri: 'file:///proj',
    cwd: '/proj',
    commandLine: 'git status',
  });
  assert.equal(e.contract_version, 'lvibe.terminal_command_audit.v1');
  assert.equal(e.phase, 'sent');
  assert.equal(e.cwd, '/proj');
  assert.equal(e.command_line, 'git status');
  assert.equal(e.exit_code, null);
  assert.ok(e.timestamp_iso);
});

test('appendTerminalCommandAudit writes JSONL under temp dir (task-n13-3)', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tca-'));
  const p = path.join(dir, 'terminal-command-audit.jsonl');
  appendTerminalCommandAudit(p, buildTerminalCommandAuditSent({
    auditId: 'x',
    workspaceUri: null,
    cwd: '/tmp',
    commandLine: 'echo hi',
  }));
  const line = fs.readFileSync(p, 'utf8').trim();
  const row = JSON.parse(line);
  assert.equal(row.command_line, 'echo hi');
  assert.equal(row.cwd, '/tmp');
});

test('terminalCommandAuditPath lives under levibeNativeChatDir', () => {
  const p = terminalCommandAuditPath();
  assert.ok(p.endsWith('terminal-command-audit.jsonl'));
});
