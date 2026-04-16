const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('monorepo root README links native extension docs (task-n8-9)', () => {
  const rootReadme = path.join(__dirname, '..', '..', '..', 'README.md');
  assert.ok(fs.existsSync(rootReadme), 'expected repo root README.md');
  const text = fs.readFileSync(rootReadme, 'utf8');
  assert.ok(
    text.includes('editor/le-vibe-native-extension/README.md'),
    'root README should link first-party extension README',
  );
  assert.ok(text.includes('editor/le-vibe-native-extension/OPERATOR.md'), 'root README should link OPERATOR.md');
  assert.ok(
    text.includes('.lvibe/workflows/native-extension-product-track.md'),
    'root README should link native extension product track',
  );
});

test('monorepo root README links native extension CHANGELOG (task-n20-1)', () => {
  const rootReadme = path.join(__dirname, '..', '..', '..', 'README.md');
  const text = fs.readFileSync(rootReadme, 'utf8');
  assert.ok(
    text.includes('editor/le-vibe-native-extension/CHANGELOG.md'),
    'root README should link extension CHANGELOG for semver release notes',
  );
});
