const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('CHANGELOG.md exists with Keep a Changelog header and [0.1.0] section (task-n19-1)', () => {
  const p = path.join(__dirname, '..', 'CHANGELOG.md');
  assert.ok(fs.existsSync(p), 'CHANGELOG.md must exist at extension package root');
  const text = fs.readFileSync(p, 'utf8');
  assert.ok(text.includes('# Changelog'), 'expected top-level # Changelog');
  assert.ok(text.includes('## [0.1.0]'), 'expected ## [0.1.0] section');
  assert.ok(
    text.includes('native-extension-product-track.md'),
    'expected pointer to product track for full epic history',
  );
});
