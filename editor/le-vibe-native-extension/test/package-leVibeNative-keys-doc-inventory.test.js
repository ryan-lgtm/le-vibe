const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR.md + README.md mention every leVibeNative.* contributes key (task-n8-54)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const keys = Object.keys(props).filter((k) => k.startsWith('leVibeNative.'));
  assert.ok(keys.length > 0);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  const combined = `${operator}\n${readme}`;
  for (const key of keys) {
    assert.ok(
      combined.includes(key),
      `Add ${key} to OPERATOR.md and/or README.md (operator + developer disclosure)`,
    );
  }
});
