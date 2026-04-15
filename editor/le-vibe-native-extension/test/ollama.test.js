const test = require('node:test');
const assert = require('node:assert/strict');

const { mapOllamaErrorToDetail, resolveStartupSnapshot } = require('../readiness');

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

test('maps Ollama timeout to explicit remediation detail', () => {
  const detail = mapOllamaErrorToDetail({ code: 'OLLAMA_TIMEOUT' });
  assert.ok(detail.includes('timed out'));
});

test('startup snapshot returns needs_ollama when probe fails', async () => {
  const vscodeMock = makeVscodeConfig({
    useLiveOllamaReadiness: true,
    ollamaEndpoint: 'http://127.0.0.1:11434',
    ollamaTimeoutMs: 2500,
  });
  const snapshot = await resolveStartupSnapshot(vscodeMock, () => ({
    probeHealth: async () => {
      throw { code: 'OLLAMA_UNREACHABLE' };
    },
    listModels: async () => [],
  }));
  assert.equal(snapshot.state, 'needs_ollama');
  assert.equal(snapshot.diagnostics.errorCode, 'OLLAMA_UNREACHABLE');
});

test('startup snapshot returns needs_model when no models are installed', async () => {
  const vscodeMock = makeVscodeConfig({
    useLiveOllamaReadiness: true,
    ollamaEndpoint: 'http://127.0.0.1:11434',
    ollamaTimeoutMs: 2500,
  });
  const snapshot = await resolveStartupSnapshot(vscodeMock, () => ({
    probeHealth: async () => ({ ok: true }),
    listModels: async () => [],
  }));
  assert.equal(snapshot.state, 'needs_model');
  assert.equal(snapshot.diagnostics.modelCount, 0);
});

test('startup snapshot returns ready with live model count', async () => {
  const vscodeMock = makeVscodeConfig({
    useLiveOllamaReadiness: true,
    ollamaEndpoint: 'http://127.0.0.1:11434',
    ollamaTimeoutMs: 2500,
  });
  const snapshot = await resolveStartupSnapshot(vscodeMock, () => ({
    probeHealth: async () => ({ ok: true }),
    listModels: async () => [{ name: 'mistral:latest' }],
  }));
  assert.equal(snapshot.state, 'ready');
  assert.equal(snapshot.diagnostics.modelCount, 1);
});
