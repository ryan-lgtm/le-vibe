const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents default Ollama model tag and leVibeNative.ollamaModel (task-n8-43)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Default local model tag'));
  assert.ok(readme.includes('mistral:latest'));
  assert.ok(readme.includes('leVibeNative.ollamaModel'));
  assert.ok(readme.includes('OPERATOR.md'));
});
