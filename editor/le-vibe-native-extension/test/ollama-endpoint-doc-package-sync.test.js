const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json leVibeNative.ollamaEndpoint default (task-n8-45)', () => {
  const def = packageJson.contributes.configuration[0].properties['leVibeNative.ollamaEndpoint'].default;
  assert.ok(typeof def === 'string' && def.startsWith('http'));
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(def), 'OPERATOR.md should mention ollamaEndpoint default');
  assert.ok(readme.includes(def), 'README.md should mention ollamaEndpoint default');
});
