const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');
const { createOllamaClient } = require('../ollama');

test('createOllamaClient default model matches leVibeNative.ollamaModel (task-n8-42)', () => {
  const expected = packageJson.contributes.configuration[0].properties['leVibeNative.ollamaModel'].default;
  const client = createOllamaClient({ endpoint: 'http://127.0.0.1:11434' });
  assert.equal(client.model, expected);
});
