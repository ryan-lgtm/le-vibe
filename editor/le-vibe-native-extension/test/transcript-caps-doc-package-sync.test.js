const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('OPERATOR and README include package.json transcript cap defaults (task-n8-47)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const maxBytes = props['leVibeNative.chatTranscriptMaxBytes'].default;
  const maxMessages = props['leVibeNative.chatTranscriptMaxMessages'].default;
  assert.ok(Number.isInteger(maxBytes) && maxBytes > 0);
  assert.ok(Number.isInteger(maxMessages) && maxMessages > 0);
  const b = String(maxBytes);
  const m = String(maxMessages);
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(b) && operator.includes(m), 'OPERATOR.md should mention transcript cap defaults');
  assert.ok(readme.includes(b) && readme.includes(m), 'README.md should mention transcript cap defaults');
});
