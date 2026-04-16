'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  normalizeCommandLine,
  commandMatchesPattern,
  evaluateTerminalCommand,
  getTerminalExecutionPolicy,
} = require('../terminal-execution-policy.js');

test('normalizeCommandLine trims and collapses whitespace', () => {
  assert.equal(normalizeCommandLine('  git   status  '), 'git status');
  assert.equal(normalizeCommandLine(''), '');
});

test('commandMatchesPattern: substring and * glob (task-n13-1)', () => {
  const line = 'npm run test -- --watch'.toLowerCase();
  assert.ok(commandMatchesPattern(line, 'npm run test'));
  assert.ok(commandMatchesPattern(line, 'NPM RUN'));
  assert.ok(!commandMatchesPattern(line, 'pnpm'));
  assert.ok(commandMatchesPattern('npm run test'.toLowerCase(), 'npm * test'));
});

test('evaluateTerminalCommand: disabled by default policy', () => {
  const r = evaluateTerminalCommand('git status', { enabled: false, allowPatterns: ['git'], denyPatterns: [] });
  assert.equal(r.ok, false);
  assert.ok(String(r.reason).includes('terminalExecutionEnabled'));
});

test('evaluateTerminalCommand: deny before allow', () => {
  const r = evaluateTerminalCommand('sudo ls', {
    enabled: true,
    allowPatterns: ['sudo'],
    denyPatterns: ['sudo '],
  });
  assert.equal(r.ok, false);
  assert.ok(String(r.reason).includes('deny'));
});

test('evaluateTerminalCommand: empty allow list when enabled blocks', () => {
  const r = evaluateTerminalCommand('git status', {
    enabled: true,
    allowPatterns: [],
    denyPatterns: [],
  });
  assert.equal(r.ok, false);
  assert.ok(String(r.reason).includes('terminalCommandAllowPatterns'));
});

test('evaluateTerminalCommand: allow match passes', () => {
  const r = evaluateTerminalCommand('git status', {
    enabled: true,
    allowPatterns: ['git status'],
    denyPatterns: [],
  });
  assert.equal(r.ok, true);
});

test('evaluateTerminalCommand: no allow match blocks', () => {
  const r = evaluateTerminalCommand('rm -f x', {
    enabled: true,
    allowPatterns: ['git status'],
    denyPatterns: [],
  });
  assert.equal(r.ok, false);
});

test('getTerminalExecutionPolicy reads leVibeNative keys (task-n13-1)', () => {
  const vscode = {
    workspace: {
      getConfiguration: () => ({
        get: (key, def) => {
          if (key === 'terminalExecutionEnabled') {
            return true;
          }
          if (key === 'terminalCommandAllowPatterns') {
            return ['npm *'];
          }
          if (key === 'terminalCommandDenyPatterns') {
            return ['sudo '];
          }
          return def;
        },
      }),
    },
  };
  const p = getTerminalExecutionPolicy(vscode);
  assert.equal(p.enabled, true);
  assert.deepEqual(p.allowPatterns, ['npm *']);
  assert.deepEqual(p.denyPatterns, ['sudo ']);
});
