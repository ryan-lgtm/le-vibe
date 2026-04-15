const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

const { isFirstPartyAgentSurfaceEnabled } = require('../feature-flags');

function makeVscodeConfig(values) {
  return {
    workspace: {
      getConfiguration() {
        return {
          get(key, fallback) {
            return key in values ? values[key] : fallback;
          },
        };
      },
    },
  };
}

test('package.json registers enableFirstPartyAgentSurface default true', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const entry = props['leVibeNative.enableFirstPartyAgentSurface'];
  assert.equal(entry.type, 'boolean');
  assert.equal(entry.default, true);
});

test('isFirstPartyAgentSurfaceEnabled respects config', () => {
  assert.equal(isFirstPartyAgentSurfaceEnabled(makeVscodeConfig({ enableFirstPartyAgentSurface: true })), true);
  assert.equal(isFirstPartyAgentSurfaceEnabled(makeVscodeConfig({ enableFirstPartyAgentSurface: false })), false);
  assert.equal(isFirstPartyAgentSurfaceEnabled(makeVscodeConfig({})), true);
});
