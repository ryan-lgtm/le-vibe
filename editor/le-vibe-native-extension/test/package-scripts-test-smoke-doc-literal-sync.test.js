const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json scripts.test and scripts.smoke literals (task-n8-62)', () => {
  const testScript = packageJson.scripts.test;
  const smokeScript = packageJson.scripts.smoke;
  assert.equal(testScript, 'node --test ./test/*.test.js');
  assert.equal(smokeScript, 'node ./scripts/smoke-integration.js');
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const [name, text] of [
    ['OPERATOR.md', operator],
    ['README.md', readme],
  ]) {
    assert.ok(text.includes(testScript), `${name} should include scripts.test literal`);
    assert.ok(text.includes(smokeScript), `${name} should include scripts.smoke literal`);
  }
});
