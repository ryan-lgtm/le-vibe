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

test('OPERATOR.md mentions package.json discovery fields (task-n8-14)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('homepage'));
  assert.ok(text.includes('bugs'));
  assert.ok(text.includes('keywords'));
  assert.ok(text.includes('repository.directory'));
});

test('OPERATOR.md mentions publisher and license (task-n8-16)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('publisher'));
  assert.ok(text.includes('license'));
  assert.ok(text.includes('SPDX'));
});

test('OPERATOR.md documents engines.vscode / minimum editor version (task-n8-17)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('engines.vscode'));
  assert.ok(text.includes('1.85'));
  assert.ok(text.includes('VSCodium'));
});

test('OPERATOR.md cross-links README prerequisites for contributors (task-n8-19)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('README.md'));
  assert.ok(text.includes('Prerequisites (developers)'));
});

test('OPERATOR.md states local-first Ollama default without silent cloud fallback (task-n8-22)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(text.includes('Local-first'));
  assert.ok(text.includes('local Ollama'));
  assert.ok(text.includes('silent'));
  assert.ok(text.toLowerCase().includes('cloud'));
});
