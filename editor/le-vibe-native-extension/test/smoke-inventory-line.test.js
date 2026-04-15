const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('smoke script logs canonical persisted dir via storage-inventory', () => {
  const p = path.join(__dirname, '..', 'scripts', 'smoke-integration.js');
  const src = fs.readFileSync(p, 'utf8');
  assert.ok(src.includes("require('../storage-inventory')") || src.includes('require("../storage-inventory")'));
  assert.ok(src.includes('levibeNativeChatDir'));
  assert.ok(src.includes('first-party persisted config dir'));
});
