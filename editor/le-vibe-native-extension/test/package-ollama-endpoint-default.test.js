const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json default leVibeNative.ollamaEndpoint matches runbook URL (task-n8-36)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const ep = props['leVibeNative.ollamaEndpoint'];
  assert.ok(ep);
  assert.equal(ep.default, 'http://127.0.0.1:11434');
});
