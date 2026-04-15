const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include every package.json scripts.* exact literal (task-n8-63)', () => {
  const scripts = packageJson.scripts;
  assert.ok(scripts && typeof scripts === 'object');
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const [name, literal] of Object.entries(scripts)) {
    assert.equal(typeof literal, 'string');
    assert.ok(literal.length > 0, `scripts.${name} must be non-empty`);
    assert.ok(operator.includes(literal), `OPERATOR.md should include scripts.${name} literal`);
    assert.ok(readme.includes(literal), `README.md should include scripts.${name} literal`);
  }
});
