'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const { buildSelectionContextEntry, prefillPromptForSelection } = require('../selection-chat-context.js');

test('buildSelectionContextEntry embeds path, range, and clipped excerpt (task-n12-1)', () => {
  const entry = buildSelectionContextEntry(
    'src/a.ts',
    'hello world',
    { startLine: 2, startCharacter: 0, endLine: 2, endCharacter: 11 },
    { maxCharsPerFile: 1200, maxLinesPerFile: 80 },
  );
  assert.equal(entry.path, 'src/a.ts');
  assert.ok(entry.content.includes('Editor selection'));
  assert.ok(entry.content.includes('src/a.ts'));
  assert.ok(entry.content.includes('line 3'));
  assert.ok(entry.content.includes('hello world'));
  assert.equal(entry.selectionRange.startLine, 2);
  assert.equal(entry.selectionRange.endLine, 2);
});

test('prefillPromptForSelection names line range (task-n12-1)', () => {
  assert.ok(prefillPromptForSelection('x.ts', { startLine: 0, endLine: 0 }).includes('line 1'));
  assert.ok(prefillPromptForSelection('y.ts', { startLine: 0, endLine: 2 }).includes('lines 1-3'));
});
