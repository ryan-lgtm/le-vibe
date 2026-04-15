const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  advanceStep,
  markCheckpoint,
  completeWizard,
  saveWizardState,
  loadWizardState,
  FINAL_STEP_INDEX,
} = require('../first-run-wizard');

test('advanceStep caps at final index', () => {
  let s = { step: 0, complete: false, checkpoints: {} };
  for (let i = 0; i < 10; i += 1) {
    s = advanceStep(s);
  }
  assert.equal(s.step, FINAL_STEP_INDEX);
});

test('completeWizard sets complete and finished checkpoint', () => {
  const s = completeWizard({ step: 2, complete: false, checkpoints: { welcome: true } });
  assert.equal(s.complete, true);
  assert.equal(s.checkpoints.finished, true);
  assert.ok(s.completedAt);
});

test('save and load round-trip', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-wiz-'));
  const file = path.join(dir, 'state.json');
  const written = saveWizardState(
    completeWizard(markCheckpoint({ step: 0, complete: false, checkpoints: {} }, 'welcome')),
    file,
  );
  assert.equal(written.complete, true);
  const loaded = loadWizardState(file);
  assert.equal(loaded.complete, true);
  assert.equal(loaded.checkpoints.welcome, true);
});
