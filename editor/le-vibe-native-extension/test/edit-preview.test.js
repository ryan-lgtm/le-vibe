const test = require('node:test');
const assert = require('node:assert/strict');
const { buildUnifiedDiff, canApplyAfterPreview, reducePreviewUiState } = require('../edit-preview.js');

test('buildUnifiedDiff emits markers and +/- lines for changed files (task-n9-2)', () => {
  const d = buildUnifiedDiff('a\nb\n', 'a\nx\n', 'demo.txt');
  assert.ok(d.includes('--- demo.txt'));
  assert.ok(d.includes('+++ demo.txt'));
  assert.ok(d.includes('-b'));
  assert.ok(d.includes('+x'));
});

test('buildUnifiedDiff no changes (task-n9-2)', () => {
  const d = buildUnifiedDiff('same', 'same', 'f');
  assert.ok(d.includes('no changes'));
});

test('canApplyAfterPreview blocks apply without preview when required (task-n9-2)', () => {
  const r = canApplyAfterPreview({
    requireEditPreviewBeforeApply: true,
    previewShown: false,
    userAcceptedPreview: true,
  });
  assert.equal(r.ok, false);
});

test('canApplyAfterPreview blocks apply without accept when required (task-n9-2)', () => {
  const r = canApplyAfterPreview({
    requireEditPreviewBeforeApply: true,
    previewShown: true,
    userAcceptedPreview: false,
  });
  assert.equal(r.ok, false);
  assert.ok(String(r.reason).includes('Accept'));
});

test('canApplyAfterPreview allows apply after accept when required (task-n9-2)', () => {
  const r = canApplyAfterPreview({
    requireEditPreviewBeforeApply: true,
    previewShown: true,
    userAcceptedPreview: true,
  });
  assert.equal(r.ok, true);
});

test('canApplyAfterPreview allows apply without accept when preview not required (task-n9-2)', () => {
  const r = canApplyAfterPreview({
    requireEditPreviewBeforeApply: false,
    previewShown: true,
    userAcceptedPreview: false,
  });
  assert.equal(r.ok, true);
});

test('reducePreviewUiState enforces preview-required default path (task-cp2-2)', () => {
  const shown = reducePreviewUiState(
    { requireEditPreviewBeforeApply: true, hasSession: false, userAcceptedPreview: false },
    'preview_shown',
  );
  assert.equal(shown.hasSession, true);
  assert.equal(shown.userAcceptedPreview, false);
  assert.equal(shown.applyEnabled, false);

  const accepted = reducePreviewUiState(
    { requireEditPreviewBeforeApply: true, hasSession: shown.hasSession, userAcceptedPreview: shown.userAcceptedPreview },
    'accept',
  );
  assert.equal(accepted.applyEnabled, true);
  assert.equal(accepted.userAcceptedPreview, true);
});

test('reducePreviewUiState reject clears session + disables apply (task-cp2-2)', () => {
  const rejected = reducePreviewUiState(
    { requireEditPreviewBeforeApply: true, hasSession: true, userAcceptedPreview: true },
    'reject',
  );
  assert.equal(rejected.hasSession, false);
  assert.equal(rejected.userAcceptedPreview, false);
  assert.equal(rejected.applyEnabled, false);
});

test('reducePreviewUiState cannot accept without active preview (task-cp2-2)', () => {
  const accepted = reducePreviewUiState(
    { requireEditPreviewBeforeApply: true, hasSession: false, userAcceptedPreview: false },
    'accept',
  );
  assert.equal(accepted.hasSession, false);
  assert.equal(accepted.applyEnabled, false);
});
