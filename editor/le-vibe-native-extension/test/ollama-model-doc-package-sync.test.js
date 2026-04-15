const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json leVibeNative.ollamaModel default (task-n8-44)', () => {
  const def = packageJson.contributes.configuration[0].properties['leVibeNative.ollamaModel'].default;
  assert.ok(typeof def === 'string' && def.length > 0);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(def), 'OPERATOR.md should mention ollamaModel default');
  assert.ok(readme.includes(def), 'README.md should mention ollamaModel default');
});
