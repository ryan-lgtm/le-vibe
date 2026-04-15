const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('docs/README.md indexes first-party native extension (task-n8-10)', () => {
  const docsReadme = path.join(__dirname, '..', '..', '..', 'docs', 'README.md');
  assert.ok(fs.existsSync(docsReadme));
  const text = fs.readFileSync(docsReadme, 'utf8');
  assert.ok(
    text.includes('editor/le-vibe-native-extension/README.md'),
    'docs index should link native extension README',
  );
  assert.ok(text.includes('native-extension-product-track.md'), 'docs index should link product track');
});
