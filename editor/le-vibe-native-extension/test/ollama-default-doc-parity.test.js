const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('OPERATOR and README share default Ollama URL stem (task-n8-35)', () => {
  const shared = '**`http://127.0.0.1:11434`** —';
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(shared));
  assert.ok(readme.includes(shared));
});
