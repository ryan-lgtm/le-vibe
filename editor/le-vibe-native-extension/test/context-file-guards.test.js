'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const ignore = require('ignore');

const {
  CONTEXT_SKIP_REASON,
  bufferLooksBinary,
  relativePosixForGitignore,
  formatContextGuardUserMessage,
} = require('../context-file-guards.js');

test('bufferLooksBinary detects null byte in prefix (task-n11-4)', () => {
  assert.equal(bufferLooksBinary(Buffer.from('hello')), false);
  assert.equal(bufferLooksBinary(Buffer.from([0x48, 0, 0x49])), true);
});

test('relativePosixForGitignore normalizes separators (task-n11-4)', () => {
  assert.equal(relativePosixForGitignore('a\\b\\c'), 'a/b/c');
});

test('formatContextGuardUserMessage is deterministic per reason (task-n11-4)', () => {
  const a = formatContextGuardUserMessage(CONTEXT_SKIP_REASON.GITIGNORE, { pathLabel: 'dist/out.js' });
  assert.ok(a.includes('dist/out.js'));
  assert.ok(a.includes('.gitignore'));

  const b = formatContextGuardUserMessage(CONTEXT_SKIP_REASON.FILE_TOO_LARGE, {
    pathLabel: 'huge.txt',
    maxChars: 1200,
    byteLength: 99999,
  });
  assert.ok(b.includes('huge.txt'));
  assert.ok(b.includes('1200'));
  assert.ok(b.includes('99999'));

  const c = formatContextGuardUserMessage(CONTEXT_SKIP_REASON.BINARY, { pathLabel: 'x.bin' });
  assert.ok(c.includes('x.bin'));
  assert.ok(c.includes('binary'));
});

test('ignore package matches .gitignore-style patterns for picker filtering (task-n11-4)', () => {
  const ig = ignore().add('*.log\nbuild/\n');
  assert.equal(ig.ignores('foo.log'), true);
  assert.equal(ig.ignores('build/x.txt'), true);
  assert.equal(ig.ignores('src/main.ts'), false);
});
