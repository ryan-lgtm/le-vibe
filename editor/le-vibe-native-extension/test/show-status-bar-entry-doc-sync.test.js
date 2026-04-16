const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

function assertBoolDefaultNearKey(text, key, literal) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 320);
  assert.ok(
    window.includes(`\`${literal}\``),
    `expected \`${literal}\` near ${key} (within 320 chars)`,
  );
}

test('OPERATOR and README document leVibeNative.showStatusBarEntry default near key (task-n17-3)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const def = props['leVibeNative.showStatusBarEntry'].default;
  assert.equal(def, false);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const doc of [operator, readme]) {
    assertBoolDefaultNearKey(doc, 'leVibeNative.showStatusBarEntry', 'false');
  }
});
