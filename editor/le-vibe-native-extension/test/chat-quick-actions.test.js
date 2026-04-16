'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const { QUICK_ACTION_ID, QUICK_ACTION_TEMPLATES, getQuickActionTemplate } = require('../chat-quick-actions.js');

test('getQuickActionTemplate returns stable strings for each id (task-n12-2)', () => {
  assert.ok(getQuickActionTemplate(QUICK_ACTION_ID.EXPLAIN).includes('plain language'));
  assert.ok(getQuickActionTemplate(QUICK_ACTION_ID.REFACTOR_SELECTION).includes('Refactor'));
  assert.ok(getQuickActionTemplate(QUICK_ACTION_ID.GENERATE_TESTS).includes('unit tests'));
  assert.equal(getQuickActionTemplate('unknown'), '');
});

test('QUICK_ACTION_TEMPLATES has exactly three entries (task-n12-2)', () => {
  assert.equal(Object.keys(QUICK_ACTION_TEMPLATES).length, 3);
});
