const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('le-vibe-native-extension-ci workflow exists and runs npm ci + npm run verify (task-n16-1)', () => {
  const wf = path.join(
    __dirname,
    '..',
    '..',
    '..',
    '.github',
    'workflows',
    'le-vibe-native-extension-ci.yml'
  );
  assert.ok(fs.existsSync(wf), `expected workflow at ${wf}`);
  const text = fs.readFileSync(wf, 'utf8');
  assert.ok(text.includes('npm ci'));
  assert.ok(text.includes('npm run verify'));
  assert.ok(text.includes('editor/le-vibe-native-extension'));
  assert.ok(text.includes('ubuntu-latest'));
});
