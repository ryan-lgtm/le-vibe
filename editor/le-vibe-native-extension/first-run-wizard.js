'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const SCHEMA = 'first_run_wizard.v1';
const FINAL_STEP_INDEX = 3;

function defaultStatePath() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'levibe-native-chat', 'first-run-wizard.json');
}

function emptyState() {
  return {
    schema: SCHEMA,
    complete: false,
    step: 0,
    checkpoints: {
      welcome: false,
      local_first: false,
      ollama_note: false,
      workspace_note: false,
    },
  };
}

function loadWizardState(filePath = defaultStatePath()) {
  if (!fs.existsSync(filePath)) {
    return emptyState();
  }
  try {
    const raw = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (!raw || typeof raw !== 'object') {
      return emptyState();
    }
    return {
      schema: SCHEMA,
      complete: !!raw.complete,
      step: typeof raw.step === 'number' ? raw.step : 0,
      completedAt: raw.completedAt || null,
      checkpoints: raw.checkpoints || {},
    };
  } catch {
    return emptyState();
  }
}

function saveWizardState(state, filePath = defaultStatePath()) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const payload = {
    schema: SCHEMA,
    complete: !!state.complete,
    step: typeof state.step === 'number' ? state.step : 0,
    completedAt: state.completedAt || null,
    checkpoints: state.checkpoints || {},
  };
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  return payload;
}

function advanceStep(state) {
  const next = Math.min((state.step || 0) + 1, FINAL_STEP_INDEX);
  return { ...state, step: next };
}

function markCheckpoint(state, id) {
  const checkpoints = { ...(state.checkpoints || {}), [id]: true };
  return { ...state, checkpoints };
}

function completeWizard(state) {
  const now = new Date().toISOString();
  return {
    ...state,
    complete: true,
    step: FINAL_STEP_INDEX,
    completedAt: now,
    checkpoints: {
      ...(state.checkpoints || {}),
      finished: true,
    },
  };
}

module.exports = {
  SCHEMA,
  FINAL_STEP_INDEX,
  defaultStatePath,
  loadWizardState,
  saveWizardState,
  advanceStep,
  markCheckpoint,
  completeWizard,
};
