const test = require('node:test');
const assert = require('node:assert/strict');

const {
  STARTUP_STATES,
  STATE_CONTENT,
  getConfiguredState,
  resolveStartupSnapshot,
  getStateContent,
} = require('../readiness');

function makeVscodeConfig(values) {
  return {
    workspace: {
      getConfiguration() {
        return {
          get(key, fallback) {
            return key in values ? values[key] : fallback;
          },
        };
      },
    },
  };
}

const NON_READY_STATES = STARTUP_STATES.filter((s) => s !== 'ready');

test('getStateContent is deterministic per state (titles match STATE_CONTENT)', () => {
  STARTUP_STATES.forEach((state) => {
    const c = getStateContent(state);
    const expected = STATE_CONTENT[state] || STATE_CONTENT.needs_auth_or_setup;
    assert.equal(c.title, expected.title, `title for ${state}`);
    assert.ok(typeof c.detail === 'string' && c.detail.length > 0, `detail for ${state}`);
    assert.ok(Array.isArray(c.actions), `actions for ${state}`);
  });
});

test('each non-ready state has deterministic remediation or explicit empty checking', () => {
  NON_READY_STATES.forEach((state) => {
    const c = getStateContent(state);
    if (state === 'checking') {
      assert.equal(c.actions.length, 0, 'checking uses copy-only UX');
      return;
    }
    assert.ok(c.actions.length > 0, `${state} must expose at least one action`);
    c.actions.forEach((a) => {
      assert.ok(a.id && a.label, `${state} action has id and label`);
    });
  });
});

test('expected action ids for Ollama and workspace remediation states', () => {
  assert.deepEqual(
    getStateContent('needs_ollama').actions.map((a) => a.id),
    ['openOllamaSetupHelp'],
  );
  assert.deepEqual(
    getStateContent('needs_model').actions.map((a) => a.id),
    ['openModelPullHelp'],
  );
  assert.deepEqual(
    getStateContent('needs_auth_or_setup').actions.map((a) => a.id),
    ['openWorkspaceSetup'],
  );
});

test('getConfiguredState falls back when devStartupState is invalid', () => {
  const vscodeMock = makeVscodeConfig({ devStartupState: 'not_a_real_state' });
  assert.equal(getConfiguredState(vscodeMock), 'needs_auth_or_setup');
});

test('resolveStartupSnapshot dev override returns each startup state deterministically', async () => {
  for (const state of STARTUP_STATES) {
    const vscodeMock = makeVscodeConfig({
      useLiveOllamaReadiness: false,
      devStartupState: state,
    });
    const snap = await resolveStartupSnapshot(vscodeMock);
    assert.equal(snap.state, state, `dev override for ${state}`);
    assert.equal(snap.diagnostics.mode, 'dev_override');
    assert.equal(snap.detailOverride, null);
  }
});
