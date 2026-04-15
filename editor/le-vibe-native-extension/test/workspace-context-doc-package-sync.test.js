const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

const CONTEXT_KEYS = [
  'leVibeNative.contextMaxFiles',
  'leVibeNative.contextMaxCharsPerFile',
  'leVibeNative.contextMaxLinesPerFile',
  'leVibeNative.contextMaxTotalChars',
];

function assertDefaultNearKey(text, key, def) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 260);
  assert.ok(
    window.includes(`\`${def}\``),
    `expected \`${def}\` near ${key} (within 260 chars)`,
  );
}

test('OPERATOR and README document package.json workspace context defaults near setting keys (task-n8-50)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const key of CONTEXT_KEYS) {
    const def = props[key].default;
    assert.ok(Number.isInteger(def) && def > 0, `${key} default must be positive integer`);
    const literal = String(def);
    for (const doc of [operator, readme]) {
      assertDefaultNearKey(doc, key, literal);
    }
  }
});
