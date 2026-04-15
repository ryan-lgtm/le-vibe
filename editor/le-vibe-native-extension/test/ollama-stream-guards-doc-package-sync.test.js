const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

function assertDefaultNearKey(text, key, def) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 240);
  assert.ok(
    window.includes(`\`${def}\``),
    `expected \`${def}\` near ${key} (within 240 chars)`,
  );
}

test('OPERATOR and README document package.json Ollama stream guard defaults near setting keys (task-n8-49)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const stallMs = props['leVibeNative.ollamaStreamStallMs'].default;
  const maxMs = props['leVibeNative.ollamaStreamMaxMs'].default;
  assert.ok(Number.isInteger(stallMs) && stallMs > 0);
  assert.ok(Number.isInteger(maxMs) && maxMs > 0);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const doc of [operator, readme]) {
    assertDefaultNearKey(doc, 'leVibeNative.ollamaStreamStallMs', String(stallMs));
    assertDefaultNearKey(doc, 'leVibeNative.ollamaStreamMaxMs', String(maxMs));
  }
});
