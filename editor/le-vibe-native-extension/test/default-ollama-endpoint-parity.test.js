const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');
const { DEFAULT_OLLAMA_HTTP_ENDPOINT } = require('../default-ollama-endpoint');

test('default-ollama-endpoint.js matches package.json leVibeNative.ollamaEndpoint default', () => {
  const props = packageJson.contributes.configuration[0].properties;
  assert.equal(props['leVibeNative.ollamaEndpoint'].default, DEFAULT_OLLAMA_HTTP_ENDPOINT);
});
