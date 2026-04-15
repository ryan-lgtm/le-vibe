const test = require('node:test');
const assert = require('node:assert/strict');
const {
  resolveSingleSelectionForPartialApply,
  SELECTION_APPLY_LIMITATIONS_MD,
} = require('../selection-apply.js');

test('resolveSingleSelectionForPartialApply happy path single non-empty selection (task-n9-4)', () => {
  const range = { start: { line: 0, character: 0 }, end: { line: 0, character: 3 }, isEmpty: false };
  const r = resolveSingleSelectionForPartialApply({ selections: [range] });
  assert.equal(r.ok, true);
  assert.equal(r.range, range);
});

test('resolveSingleSelectionForPartialApply rejects no editor (task-n9-4)', () => {
  const r = resolveSingleSelectionForPartialApply(null);
  assert.equal(r.ok, false);
  assert.equal(r.code, 'NO_ACTIVE_EDITOR');
  assert.ok(String(r.message).includes('no active editor'));
});

test('resolveSingleSelectionForPartialApply rejects empty selection (task-n9-4)', () => {
  const r = resolveSingleSelectionForPartialApply({
    selections: [{ start: { line: 1, character: 1 }, end: { line: 1, character: 1 }, isEmpty: true }],
  });
  assert.equal(r.ok, false);
  assert.equal(r.code, 'EMPTY_SELECTION');
});

test('resolveSingleSelectionForPartialApply rejects multi-selection (task-n9-4)', () => {
  const a = { start: { line: 0, character: 0 }, end: { line: 0, character: 1 }, isEmpty: false };
  const b = { start: { line: 2, character: 0 }, end: { line: 2, character: 1 }, isEmpty: false };
  const r = resolveSingleSelectionForPartialApply({ selections: [a, b] });
  assert.equal(r.ok, false);
  assert.equal(r.code, 'MULTI_SELECTION');
  assert.ok(String(r.message).includes('one selection'));
});

test('resolveSingleSelectionForPartialApply infers empty when isEmpty omitted (task-n9-4)', () => {
  const r = resolveSingleSelectionForPartialApply({
    selections: [{ start: { line: 0, character: 5 }, end: { line: 0, character: 5 } }],
  });
  assert.equal(r.ok, false);
  assert.equal(r.code, 'EMPTY_SELECTION');
});

test('SELECTION_APPLY_LIMITATIONS_MD documents multi-cursor limitation (task-n9-4)', () => {
  assert.ok(SELECTION_APPLY_LIMITATIONS_MD.includes('multi-cursor'));
  assert.ok(SELECTION_APPLY_LIMITATIONS_MD.includes('non-empty'));
});
