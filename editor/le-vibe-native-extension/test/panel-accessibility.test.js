const test = require('node:test');
const assert = require('node:assert/strict');
const extensionModule = require('../extension');
const { STARTUP_STATES } = require('../readiness');

test('panel and wizard HTML include accessibility baseline (task-n17-2)', () => {
  const panel = extensionModule.panelHtml('ready');
  assert.ok(panel.includes('<html lang="en">'), 'panel html lang');
  assert.ok(panel.includes('id="levibe-chat-main"'), 'panel main landmark');
  assert.ok(panel.includes('skip-link'), 'panel skip link');
  assert.ok(panel.includes('aria-label="Prompt for local Ollama'), 'prompt aria-label');
  assert.ok(panel.includes('role="status"'), 'chat status live region');
  assert.ok(panel.includes('role="log"'), 'chat log live region');
  assert.ok(panel.includes('nav aria-label='), 'states nav label');

  const wiz = extensionModule.firstRunWizardHtml(0);
  assert.ok(wiz.includes('<html lang="en">'), 'wizard html lang');
  assert.ok(wiz.includes('id="levibe-wizard-main"'), 'wizard main landmark');
  assert.ok(wiz.includes('aria-label="Next checkpoint"'), 'wizard next aria-label');
});

test('every panel data-action button has type and aria-label (task-n17-2)', () => {
  for (const state of STARTUP_STATES) {
    const html = extensionModule.panelHtml(state);
    const matches = [...html.matchAll(/<button[^>]*data-action="([^"]+)"[^>]*>/g)];
    assert.ok(matches.length > 0, `expected data-action buttons for state ${state}`);
    for (const m of matches) {
      const tag = m[0];
      assert.ok(tag.includes('type="button"'), `button ${m[1]} should have type=button`);
      assert.ok(tag.includes('aria-label='), `button ${m[1]} should have aria-label`);
    }
  }
});
