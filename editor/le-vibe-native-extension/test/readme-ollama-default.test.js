const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents default Ollama URL and leVibeNative.ollamaEndpoint (task-n8-35)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Default local Ollama URL'));
  assert.ok(readme.includes('http://127.0.0.1:11434'));
  assert.ok(readme.includes('leVibeNative.ollamaEndpoint'));
  assert.ok(readme.includes('LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT'));
  assert.ok(readme.includes('OPERATOR.md'));
});
