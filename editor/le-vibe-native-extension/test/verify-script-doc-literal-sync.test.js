const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json scripts.verify literal (task-n8-61)', () => {
  const literal = packageJson.scripts.verify;
  assert.equal(literal, 'npm test && npm run smoke');
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(literal), 'OPERATOR.md should include scripts.verify literal');
  assert.ok(readme.includes(literal), 'README.md should include scripts.verify literal');
});
