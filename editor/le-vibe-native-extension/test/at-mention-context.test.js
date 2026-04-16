'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const ignore = require('ignore');

const {
  sliceToCap,
  parentFolderPrefixes,
  uniqueFolderCandidatesFromFiles,
  FILE_PICKER_MAX_SCAN_URIS,
  FOLDER_QUICKPICK_MAX_CANDIDATES,
  pickAtFileContext,
  pickAtFolderContext,
} = require('../at-mention-context.js');

test('sliceToCap enforces max length (task-n14-1)', () => {
  assert.deepEqual(sliceToCap([1, 2, 3, 4], 2), [1, 2]);
  assert.deepEqual(sliceToCap([1], 0), []);
});

test('parentFolderPrefixes extracts ancestor dirs (task-n14-1)', () => {
  assert.deepEqual(parentFolderPrefixes('a/b/c.ts'), ['a', 'a/b']);
  assert.deepEqual(parentFolderPrefixes('root.ts'), []);
});

test('uniqueFolderCandidatesFromFiles respects folder cap (task-n14-1)', () => {
  const ig = ignore();
  const files = [];
  for (let i = 0; i < 500; i += 1) {
    files.push(`d${i}/f.txt`);
  }
  const folders = uniqueFolderCandidatesFromFiles(files, ig);
  assert.ok(folders.length <= FOLDER_QUICKPICK_MAX_CANDIDATES);
  assert.ok(folders.includes(''));
});

test('FILE_PICKER_MAX_SCAN_URIS is strict and documented in module (task-n14-1)', () => {
  assert.equal(typeof FILE_PICKER_MAX_SCAN_URIS, 'number');
  assert.ok(FILE_PICKER_MAX_SCAN_URIS > 0);
  assert.ok(FILE_PICKER_MAX_SCAN_URIS <= 500);
});

test('uniqueFolderCandidatesFromFiles drops gitignored folder prefixes (task-n14-1)', () => {
  const ig = ignore();
  ig.add('secret/');
  const folders = uniqueFolderCandidatesFromFiles(['secret/file.ts', 'ok/other.ts'], ig);
  assert.ok(!folders.includes('secret'));
  assert.ok(folders.includes('ok'));
});

test('pickAtFileContext returns visible skip message without workspace (task-cp1-3)', async () => {
  const vscode = {
    workspace: {
      workspaceFolders: [],
    },
    window: {
      showWarningMessage: async () => {},
      showInformationMessage: async () => {},
    },
  };
  const result = await pickAtFileContext(vscode, () => ({ maxCharsPerFile: 1200, maxLinesPerFile: 80 }));
  assert.ok(result && typeof result.skipMessage === 'string');
  assert.ok(result.skipMessage.includes('skipped @file'));
});

test('pickAtFolderContext returns visible skip message without workspace (task-cp1-3)', async () => {
  const vscode = {
    workspace: {
      workspaceFolders: [],
    },
    window: {
      showWarningMessage: async () => {},
      showInformationMessage: async () => {},
    },
  };
  const result = await pickAtFolderContext(vscode, () => ({ maxCharsPerFile: 1200, maxLinesPerFile: 80 }));
  assert.ok(result && typeof result.skipMessage === 'string');
  assert.ok(result.skipMessage.includes('skipped @folder'));
});
