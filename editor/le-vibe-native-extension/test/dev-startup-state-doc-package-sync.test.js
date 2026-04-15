const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

const KEY = 'leVibeNative.devStartupState';

function assertStringDefaultNearKey(text, key, literal) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 320);
  assert.ok(
    window.includes(`\`${literal}\``),
    `expected \`${literal}\` near ${key} (within 320 chars)`,
  );
}

test('OPERATOR and README document package.json devStartupState default near setting key (task-n8-53)', () => {
  const def = packageJson.contributes.configuration[0].properties[KEY].default;
  assert.equal(typeof def, 'string');
  assert.ok(def.length > 0);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const doc of [operator, readme]) {
    assertStringDefaultNearKey(doc, KEY, def);
  }
});
