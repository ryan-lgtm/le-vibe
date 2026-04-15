const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

const INVENTORY_TEST = 'package-leVibeNative-keys-doc-inventory.test.js';
const STEM = 'Settings disclosure guardrail';

test('OPERATOR and README both document settings disclosure guardrail + inventory test (task-n8-57)', () => {
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const [name, text] of [
    ['OPERATOR.md', operator],
    ['README.md', readme],
  ]) {
    assert.ok(text.includes(STEM), `${name} should include "${STEM}"`);
    assert.ok(text.includes(INVENTORY_TEST), `${name} should reference ${INVENTORY_TEST}`);
  }
});
