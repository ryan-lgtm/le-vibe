const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');
const { createOllamaClient } = require('../ollama');

test('createOllamaClient default timeoutMs matches leVibeNative.ollamaTimeoutMs (task-n8-41)', () => {
  const expected = packageJson.contributes.configuration[0].properties['leVibeNative.ollamaTimeoutMs'].default;
  const client = createOllamaClient({ endpoint: 'http://127.0.0.1:11435' });
  assert.equal(client.timeoutMs, expected);
});
