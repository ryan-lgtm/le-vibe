const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json leVibeNative.ollamaTimeoutMs default (task-n8-46)', () => {
  const def = packageJson.contributes.configuration[0].properties['leVibeNative.ollamaTimeoutMs'].default;
  assert.ok(typeof def === 'number' && def > 0);
  const literal = String(def);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(literal), 'OPERATOR.md should mention ollamaTimeoutMs default ms value');
  assert.ok(readme.includes(literal), 'README.md should mention ollamaTimeoutMs default ms value');
});
