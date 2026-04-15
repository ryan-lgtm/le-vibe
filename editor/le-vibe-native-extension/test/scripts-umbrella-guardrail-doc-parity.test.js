const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

const STEM = 'Scripts literal umbrella';
const TEST_FILE = 'package-json-all-scripts-doc-literal-sync.test.js';

test('OPERATOR and README document scripts umbrella guardrail test (task-n8-64)', () => {
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const [name, text] of [
    ['OPERATOR.md', operator],
    ['README.md', readme],
  ]) {
    assert.ok(text.includes(STEM), `${name} should include "${STEM}"`);
    assert.ok(text.includes(TEST_FILE), `${name} should reference ${TEST_FILE}`);
  }
});
