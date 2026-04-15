'use strict';

const { createOllamaClient } = require('./ollama');

const STARTUP_STATES = Object.freeze([
  'checking',
  'ready',
  'needs_ollama',
  'needs_model',
  'needs_auth_or_setup',
]);

const STATE_CONTENT = Object.freeze({
  checking: {
    title: 'Checking local runtime',
    detail: 'Running startup checks for local Lé Vibe prerequisites.',
    actions: [],
  },
  ready: {
    title: 'Ready',
    detail: 'Local startup checks passed. You can start an agent interaction.',
    actions: [],
  },
  needs_ollama: {
    title: 'Ollama is not reachable',
    detail: 'Lé Vibe needs local Ollama running on this machine before agent chat can start.',
    actions: [{ id: 'openOllamaSetupHelp', label: 'Open Ollama Setup Help' }],
  },
  needs_model: {
    title: 'No local model is available',
    detail: 'Install at least one local Ollama model to continue with local-first agent runs.',
    actions: [{ id: 'openModelPullHelp', label: 'Show Local Model Install Steps' }],
  },
  needs_auth_or_setup: {
    title: 'Workspace setup is required',
    detail: 'Complete workspace setup to enable deterministic agent startup behavior.',
    actions: [{ id: 'openWorkspaceSetup', label: 'Open Setup Workflow' }],
  },
});

function getConfiguredState(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const configured = config.get('devStartupState', 'needs_auth_or_setup');
  return STARTUP_STATES.includes(configured) ? configured : 'needs_auth_or_setup';
}

function mapOllamaErrorToDetail(error) {
  if (!error || !error.code) {
    return 'Could not validate local Ollama. Start it and retry.';
  }
  if (error.code === 'OLLAMA_TIMEOUT') {
    return 'Local Ollama timed out. Ensure it is running and responsive, then retry.';
  }
  if (error.code === 'OLLAMA_BAD_ENDPOINT') {
    return 'Configured Ollama endpoint is invalid. Fix leVibeNative.ollamaEndpoint and retry.';
  }
  if (error.code === 'OLLAMA_HTTP_ERROR') {
    return 'Local Ollama returned an unexpected HTTP status. Verify Ollama service health and retry.';
  }
  return 'Could not connect to local Ollama. Start Ollama locally and retry.';
}

function getOllamaConfig(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  return {
    endpoint: config.get('ollamaEndpoint', 'http://127.0.0.1:11434'),
    timeoutMs: config.get('ollamaTimeoutMs', 2500),
  };
}

async function resolveStartupSnapshot(vscode, createClient = createOllamaClient) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (config.get('useLiveOllamaReadiness', true) === false) {
    const forcedState = getConfiguredState(vscode);
    return {
      state: forcedState,
      diagnostics: { mode: 'dev_override' },
      detailOverride: null,
    };
  }

  const { endpoint, timeoutMs } = getOllamaConfig(vscode);
  const client = createClient({ endpoint, timeoutMs });
  try {
    await client.probeHealth();
    const models = await client.listModels();
    if (!models.length) {
      return {
        state: 'needs_model',
        diagnostics: { endpoint, modelCount: 0 },
        detailOverride: 'Ollama is reachable but no local model is installed.',
      };
    }
    return {
      state: 'ready',
      diagnostics: { endpoint, modelCount: models.length },
      detailOverride: `Ollama is reachable at ${endpoint} with ${models.length} local model(s).`,
    };
  } catch (error) {
    return {
      state: 'needs_ollama',
      diagnostics: { endpoint, errorCode: error && error.code ? error.code : 'UNKNOWN' },
      detailOverride: mapOllamaErrorToDetail(error),
    };
  }
}

function getStateContent(state, detailOverride) {
  const content = STATE_CONTENT[state] || STATE_CONTENT.needs_auth_or_setup;
  if (!detailOverride) {
    return content;
  }
  return {
    ...content,
    detail: detailOverride,
  };
}

module.exports = {
  STARTUP_STATES,
  STATE_CONTENT,
  resolveStartupSnapshot,
  getStateContent,
  mapOllamaErrorToDetail,
};
