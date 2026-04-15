const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const { PERSISTED_ARTIFACTS } = require('../storage-inventory');

test('README bounded persistence table mentions every PERSISTED_ARTIFACTS entry', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('## Bounded persistence inventory'));
  for (const a of PERSISTED_ARTIFACTS) {
    if (a.basename.includes('*')) {
      assert.ok(
        readme.includes('transcript-') && readme.includes('.jsonl'),
        'README should describe transcript jsonl pattern',
      );
    } else {
      assert.ok(readme.includes(a.basename), `README must mention ${a.basename}`);
    }
  }
});
