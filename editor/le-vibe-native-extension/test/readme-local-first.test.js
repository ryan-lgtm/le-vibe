const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents local-first Ollama default without silent cloud fallback (task-n8-23)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Local-first'));
  assert.ok(readme.includes('local Ollama'));
  assert.ok(readme.includes('silent'));
  assert.ok(readme.toLowerCase().includes('cloud'));
  assert.ok(readme.includes('OPERATOR.md'));
});
