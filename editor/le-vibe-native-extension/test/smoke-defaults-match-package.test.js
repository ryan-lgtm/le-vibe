const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('smoke-integration.js Ollama fallbacks match package.json defaults (task-n8-40)', () => {
  const script = fs.readFileSync(path.join(__dirname, '..', 'scripts', 'smoke-integration.js'), 'utf8');
  const props = packageJson.contributes.configuration[0].properties;
  const endpointDefault = props['leVibeNative.ollamaEndpoint'].default;
  const timeoutDefault = props['leVibeNative.ollamaTimeoutMs'].default;

  assert.ok(
    script.includes(`|| '${endpointDefault}'`),
    'smoke endpoint fallback must match leVibeNative.ollamaEndpoint default',
  );
  assert.ok(
    script.includes(`|| ${timeoutDefault})`),
    'smoke timeout fallback must match leVibeNative.ollamaTimeoutMs default',
  );
});
