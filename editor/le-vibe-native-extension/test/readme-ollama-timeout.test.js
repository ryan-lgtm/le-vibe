const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents default Ollama probe timeout and settings (task-n8-38)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Default Ollama probe timeout'));
  assert.ok(readme.includes('2500'));
  assert.ok(readme.includes('leVibeNative.ollamaTimeoutMs'));
  assert.ok(readme.includes('LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS'));
  assert.ok(readme.includes('OPERATOR.md'));
});
