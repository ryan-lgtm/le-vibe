'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const {
  outlineTextFromSymbols,
  symbolKindLabel,
  OUTLINE_MAX_SYMBOL_NODES,
  OUTLINE_MAX_DEPTH,
} = require('../outline-context.js');

test('symbolKindLabel maps vscode SymbolKind numbers (task-n14-2)', () => {
  assert.equal(symbolKindLabel(11), 'Function');
  assert.equal(symbolKindLabel(4), 'Class');
});

test('outlineTextFromSymbols flattens tree with depth and node caps (task-n14-2)', () => {
  const tree = [
    {
      name: 'outer',
      kind: 11,
      children: [
        { name: 'inner', kind: 12, children: [{ name: 'deep', kind: 11, children: [] }] },
      ],
    },
  ];
  const text = outlineTextFromSymbols(tree, {
    pathLabel: 'x.ts',
    maxChars: 10000,
    maxLines: 100,
    maxNodes: 2,
    maxDepth: OUTLINE_MAX_DEPTH,
  });
  assert.ok(text.includes('outer'));
  assert.ok(text.includes('inner'));
  assert.ok(!text.includes('deep'));
});

test('outlineTextFromSymbols respects clip budget (task-n14-2)', () => {
  const many = Array.from({ length: 50 }, (_, i) => ({
    name: `fn${i}`,
    kind: 11,
    children: [],
  }));
  const text = outlineTextFromSymbols(many, {
    pathLabel: 'big.ts',
    maxChars: 120,
    maxLines: 20,
    maxNodes: OUTLINE_MAX_SYMBOL_NODES,
    maxDepth: 2,
  });
  assert.ok(text.length <= 120);
});

test('outlineTextFromSymbols handles SymbolInformation-like entries (task-n14-2)', () => {
  const flat = [
    { name: 'a', kind: 11, location: { uri: {}, range: {} } },
    { name: 'b', kind: 12, location: { uri: {}, range: {} } },
  ];
  const text = outlineTextFromSymbols(flat, {
    pathLabel: 'y.ts',
    maxChars: 5000,
    maxLines: 80,
  });
  assert.ok(text.includes('Function a'));
  assert.ok(text.includes('Variable b'));
});
