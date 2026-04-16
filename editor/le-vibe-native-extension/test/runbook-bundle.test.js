'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  tailTextFileLines,
  collectLeVibeNativeSettingsInspect,
  writeRunbookBundle,
  defaultRunbookBundleDir,
} = require('../runbook-bundle');

test('tailTextFileLines returns last N lines', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'rb-'));
  const p = path.join(dir, 't.txt');
  fs.writeFileSync(p, 'a\nb\nc\nd\ne\n', 'utf8');
  const out = tailTextFileLines(p, 2);
  assert.ok(out.includes('d'));
  assert.ok(out.includes('e'));
  assert.ok(!out.includes('a'));
});

test('collectLeVibeNativeSettingsInspect reads inspect map', () => {
  const vscode = {
    workspace: {
      getConfiguration() {
        return {
          inspect(key) {
            return {
              defaultValue: 'def',
              globalValue: 'g',
              workspaceValue: undefined,
              workspaceFolderValue: undefined,
            };
          },
        };
      },
    },
  };
  const snap = collectLeVibeNativeSettingsInspect(vscode);
  assert.equal(snap['leVibeNative.ollamaEndpoint'].global, 'g');
});

test('writeRunbookBundle writes expected files (task-cp5-2)', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'rb-bundle-'));
  const outDir = path.join(dir, 'out');
  const levibeDir = path.join(dir, 'levibe');
  fs.mkdirSync(levibeDir, { recursive: true });
  fs.writeFileSync(
    path.join(levibeDir, 'orchestrator-events.jsonl'),
    `${JSON.stringify({ x: 1 })}\n${JSON.stringify({ x: 2 })}\n`,
    'utf8',
  );

  const vscode = {
    workspace: {
      getConfiguration() {
        return {
          inspect(key) {
            return { defaultValue: null, globalValue: null, workspaceValue: null, workspaceFolderValue: null };
          },
        };
      },
    },
  };

  const { files, outDir: got } = writeRunbookBundle({
    vscode,
    workspaceFolderUri: 'file:///tmp/ws',
    outDir,
    levibeDir,
  });
  assert.equal(got, outDir);
  assert.ok(files.includes('leVibeNative-settings.json'));
  assert.ok(files.includes('README-runbook.txt'));
  assert.ok(fs.existsSync(path.join(outDir, 'README-runbook.txt')));
  const readme = fs.readFileSync(path.join(outDir, 'README-runbook.txt'), 'utf8');
  assert.ok(readme.includes(outDir));
  assert.ok(readme.includes('Local-only'));
});

test('defaultRunbookBundleDir ends with runbook- prefix', () => {
  const d = defaultRunbookBundleDir('2026-04-15T12-00-00-000Z');
  assert.ok(d.includes('runbook-bundles'));
  assert.ok(path.basename(d).startsWith('runbook-2026'));
});
