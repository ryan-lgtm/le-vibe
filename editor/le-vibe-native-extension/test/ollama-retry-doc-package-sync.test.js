const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

function assertDefaultNearKey(text, key, def) {
  const idx = text.indexOf(key);
  assert.ok(idx >= 0, `expected ${key} in doc`);
  const window = text.slice(idx, idx + 220);
  // Docs use bold + code (e.g. **`2`**, **`400` ms**), not plain **2**
  assert.ok(
    window.includes(`\`${def}\``),
    `expected \`${def}\` near ${key} (within 220 chars)`,
  );
}

test('OPERATOR and README document package.json Ollama retry defaults near setting keys (task-n8-48)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const maxRetries = props['leVibeNative.ollamaMaxRetries'].default;
  const backoffMs = props['leVibeNative.ollamaRetryBackoffMs'].default;
  assert.ok(Number.isInteger(maxRetries) && maxRetries >= 0);
  assert.ok(Number.isInteger(backoffMs) && backoffMs > 0);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const doc of [operator, readme]) {
    assertDefaultNearKey(doc, 'leVibeNative.ollamaMaxRetries', String(maxRetries));
    assertDefaultNearKey(doc, 'leVibeNative.ollamaRetryBackoffMs', String(backoffMs));
  }
});
