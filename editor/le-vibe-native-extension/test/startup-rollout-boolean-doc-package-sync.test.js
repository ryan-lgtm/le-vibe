const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

const BOOL_KEYS = [
  'leVibeNative.enableFirstPartyAgentSurface',
  'leVibeNative.showFirstRunWizard',
  'leVibeNative.openPanelOnStartup',
];

function assertBoolDefaultNearKey(text, key, literal) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 280);
  assert.ok(
    window.includes(`\`${literal}\``),
    `expected \`${literal}\` near ${key} (within 280 chars)`,
  );
}

test('OPERATOR and README document package.json startup/rollout boolean defaults near setting keys (task-n8-51)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const key of BOOL_KEYS) {
    const def = props[key].default;
    assert.equal(typeof def, 'boolean');
    const literal = String(def);
    for (const doc of [operator, readme]) {
      assertBoolDefaultNearKey(doc, key, literal);
    }
  }
});
