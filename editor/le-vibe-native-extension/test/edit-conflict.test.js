const test = require('node:test');
const assert = require('node:assert/strict');
const {
  EDIT_PREVIEW_STALE_CONFLICT_MESSAGE,
  EDIT_PREVIEW_FILE_MISSING_MESSAGE,
  EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE,
  buildPreviewRevision,
  assertContentMatchesRevision,
  checkDiskContentMatchesRevision,
  sha256Utf8,
} = require('../edit-conflict.js');

test('buildPreviewRevision + assertContentMatchesRevision ok when unchanged (task-n9-5)', () => {
  const before = 'alpha\n';
  const rev = buildPreviewRevision(before, { mtime: 100, size: 6 });
  assert.equal(rev.contentSha256, sha256Utf8(before));
  assert.equal(rev.mtimeMs, 100);
  assert.equal(rev.sizeBytes, 6);
  const r = assertContentMatchesRevision(before, rev);
  assert.equal(r.ok, true);
});

test('assertContentMatchesRevision stale when file edited (task-n9-5)', () => {
  const rev = buildPreviewRevision('same');
  const r = assertContentMatchesRevision('different', rev);
  assert.equal(r.ok, false);
  assert.equal(r.panelMessage, EDIT_PREVIEW_STALE_CONFLICT_MESSAGE);
});

test('checkDiskContentMatchesRevision stale when readFile returns new bytes (task-n9-5)', async () => {
  const rev = buildPreviewRevision('v1', { mtime: 10, size: 2 });
  const vscode = {
    workspace: {
      fs: {
        stat: async () => ({ mtime: 10, size: 2 }),
        readFile: async () => Buffer.from('v2', 'utf8'),
      },
    },
  };
  const uri = {};
  const r = await checkDiskContentMatchesRevision(vscode, uri, rev);
  assert.equal(r.ok, false);
  assert.equal(r.panelMessage, EDIT_PREVIEW_STALE_CONFLICT_MESSAGE);
});

test('checkDiskContentMatchesRevision missing file (task-n9-5)', async () => {
  const rev = buildPreviewRevision('x', { mtime: 10, size: 1 });
  const vscode = {
    workspace: {
      fs: {
        stat: async () => {
          throw new Error('ENOENT');
        },
        readFile: async () => {
          throw new Error('ENOENT');
        },
      },
    },
  };
  const r = await checkDiskContentMatchesRevision(vscode, {}, rev);
  assert.equal(r.ok, false);
  assert.equal(r.panelMessage, EDIT_PREVIEW_FILE_MISSING_MESSAGE);
});

test('checkDiskContentMatchesRevision ok when disk matches revision (task-n9-5)', async () => {
  const body = 'unchanged\n';
  const rev = buildPreviewRevision(body, { mtime: 99, size: body.length });
  const vscode = {
    workspace: {
      fs: {
        stat: async () => ({ mtime: 99, size: body.length }),
        readFile: async () => Buffer.from(body, 'utf8'),
      },
    },
  };
  const r = await checkDiskContentMatchesRevision(vscode, {}, rev);
  assert.equal(r.ok, true);
});

test('checkDiskContentMatchesRevision blocks when mtime drifts (task-cp2-4)', async () => {
  const rev = buildPreviewRevision('same', { mtime: 50, size: 4 });
  const vscode = {
    workspace: {
      fs: {
        stat: async () => ({ mtime: 51, size: 4 }),
        readFile: async () => Buffer.from('same', 'utf8'),
      },
    },
  };
  const r = await checkDiskContentMatchesRevision(vscode, {}, rev);
  assert.equal(r.ok, false);
  assert.equal(r.panelMessage, EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE);
});

test('checkDiskContentMatchesRevision blocks when size drifts (task-cp2-4)', async () => {
  const rev = buildPreviewRevision('same', { mtime: 50, size: 4 });
  const vscode = {
    workspace: {
      fs: {
        stat: async () => ({ mtime: 50, size: 5 }),
        readFile: async () => Buffer.from('same', 'utf8'),
      },
    },
  };
  const r = await checkDiskContentMatchesRevision(vscode, {}, rev);
  assert.equal(r.ok, false);
  assert.equal(r.panelMessage, EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE);
});
