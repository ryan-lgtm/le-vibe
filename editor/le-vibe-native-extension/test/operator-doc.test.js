const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('OPERATOR.md exists and documents verify + persistence pointers', () => {
  const p = path.join(__dirname, '..', 'OPERATOR.md');
  assert.ok(fs.existsSync(p));
  const text = fs.readFileSync(p, 'utf8');
  assert.ok(text.includes('npm run verify'));
  assert.ok(text.includes('storage-inventory.js'));
  assert.ok(text.includes('levibe-native-chat'));
});
