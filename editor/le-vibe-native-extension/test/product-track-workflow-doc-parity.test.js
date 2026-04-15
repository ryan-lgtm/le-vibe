const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

/** Exact path token as documented in OPERATOR + README (task-n8-66 / n8-67). */
const WORKFLOW_PATH_TOKEN = '`.lvibe/workflows/native-extension-product-track.md`';

test('OPERATOR.md and README.md both cite Product track workflow path (task-n8-67 parity)', () => {
  for (const name of ['OPERATOR.md', 'README.md']) {
    const text = fs.readFileSync(path.join(__dirname, '..', name), 'utf8');
    assert.ok(
      text.includes(WORKFLOW_PATH_TOKEN),
      `${name} should include ${WORKFLOW_PATH_TOKEN}`,
    );
  }
});
