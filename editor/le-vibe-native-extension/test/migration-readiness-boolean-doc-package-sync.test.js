const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

const BOOL_KEYS = ['leVibeNative.showThirdPartyMigrationNudge', 'leVibeNative.useLiveOllamaReadiness'];

function assertBoolDefaultNearKey(text, key, literal) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 300);
  assert.ok(
    window.includes(`\`${literal}\``),
    `expected \`${literal}\` near ${key} (within 300 chars)`,
  );
}

test('OPERATOR and README document package.json migration/readiness boolean defaults near setting keys (task-n8-52)', () => {
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
