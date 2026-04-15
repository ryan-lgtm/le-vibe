'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { validateWorkspaceRelativeCreatePath, DEFAULT_DENIED_SEGMENTS } = require('../workspace-fs-actions.js');

test('validateWorkspaceRelativeCreatePath rejects traversal (task-n11-1)', () => {
  const a = validateWorkspaceRelativeCreatePath('../outside.txt');
  assert.equal(a.ok, false);
  assert.ok(String(a.userMessage).includes('..'));

  const b = validateWorkspaceRelativeCreatePath('foo/../../etc/passwd');
  assert.equal(b.ok, false);

  const c = validateWorkspaceRelativeCreatePath('/abs/path.txt');
  assert.equal(c.ok, false);
});

test('validateWorkspaceRelativeCreatePath rejects denied segments (task-n11-1)', () => {
  assert.equal(validateWorkspaceRelativeCreatePath('.git/config').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('src/.git/hooks/x').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('node_modules/pkg/index.js').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('.ssh/known_hosts').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('x/.env').ok, false);
});

test('validateWorkspaceRelativeCreatePath accepts safe nested paths (task-n11-1)', () => {
  const r = validateWorkspaceRelativeCreatePath('notes/demo.md');
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.equal(r.normalizedRelative, 'notes/demo.md');
  }
});

test('validateWorkspaceRelativeCreatePath empty rejects (task-n11-1)', () => {
  assert.equal(validateWorkspaceRelativeCreatePath('').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('   ').ok, false);
});

test('DEFAULT_DENIED_SEGMENTS includes expected roots (task-n11-1)', () => {
  assert.ok(DEFAULT_DENIED_SEGMENTS.has('.git'));
  assert.ok(DEFAULT_DENIED_SEGMENTS.has('node_modules'));
});
