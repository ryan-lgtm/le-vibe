const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');
const assert = require('node:assert/strict');

const {
  readManagedOllamaHttpEndpointSync,
  getEffectiveOllamaEndpoint,
  readLockedOllamaModelSync,
  resolveEffectiveOllamaModel,
} = require('../ollama-endpoint-resolve');

test('readManagedOllamaHttpEndpointSync returns null when managed_ollama.json is missing', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  try {
    assert.equal(readManagedOllamaHttpEndpointSync(), null);
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});

test('readManagedOllamaHttpEndpointSync parses host and port from managed_ollama.json', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  fs.writeFileSync(
    path.join(tmp, 'le-vibe', 'managed_ollama.json'),
    JSON.stringify({
      pid: 712435,
      host: '127.0.0.1',
      port: 11435,
      session_id: 'default',
      started_at_unix: 0,
    }),
  );
  try {
    assert.equal(readManagedOllamaHttpEndpointSync(), 'http://127.0.0.1:11435');
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});

test('getEffectiveOllamaEndpoint prefers managed file over legacy default when user has not set the setting', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  fs.writeFileSync(
    path.join(tmp, 'le-vibe', 'managed_ollama.json'),
    JSON.stringify({
      pid: 1,
      host: '127.0.0.1',
      port: 11435,
      session_id: 'x',
      started_at_unix: 0,
    }),
  );
  const vscode = {
    workspace: {
      getConfiguration() {
        return {
          get(key, fallback) {
            if (key === 'ollamaEndpoint') {
              return 'http://127.0.0.1:11434';
            }
            return fallback;
          },
          inspect(key) {
            if (key === 'ollamaEndpoint') {
              return {
                defaultValue: 'http://127.0.0.1:11434',
                globalValue: undefined,
                workspaceValue: undefined,
                workspaceFolderValue: undefined,
              };
            }
            return undefined;
          },
        };
      },
    },
  };
  try {
    assert.equal(getEffectiveOllamaEndpoint(vscode), 'http://127.0.0.1:11435');
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});

test('getEffectiveOllamaEndpoint respects explicit user setting when inspect globalValue is set', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  fs.writeFileSync(
    path.join(tmp, 'le-vibe', 'managed_ollama.json'),
    JSON.stringify({
      pid: 1,
      host: '127.0.0.1',
      port: 11435,
      session_id: 'x',
      started_at_unix: 0,
    }),
  );
  const vscode = {
    workspace: {
      getConfiguration() {
        return {
          get(key, fallback) {
            if (key === 'ollamaEndpoint') {
              return 'http://127.0.0.1:11999';
            }
            return fallback;
          },
          inspect(key) {
            if (key === 'ollamaEndpoint') {
              return {
                defaultValue: 'http://127.0.0.1:11435',
                globalValue: 'http://127.0.0.1:11999',
                workspaceValue: undefined,
                workspaceFolderValue: undefined,
              };
            }
            return undefined;
          },
        };
      },
    },
  };
  try {
    assert.equal(getEffectiveOllamaEndpoint(vscode), 'http://127.0.0.1:11999');
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});

test('readLockedOllamaModelSync reads locked-model.json ollama_model', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  fs.writeFileSync(
    path.join(tmp, 'le-vibe', 'locked-model.json'),
    JSON.stringify({ ollama_model: 'deepseek-r1:14b' }),
  );
  try {
    assert.equal(readLockedOllamaModelSync(), 'deepseek-r1:14b');
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});

test('resolveEffectiveOllamaModel prefers locked model when user has no model override', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-oe-'));
  const prev = process.env.XDG_CONFIG_HOME;
  process.env.XDG_CONFIG_HOME = tmp;
  fs.mkdirSync(path.join(tmp, 'le-vibe'), { recursive: true });
  fs.writeFileSync(
    path.join(tmp, 'le-vibe', 'locked-model.json'),
    JSON.stringify({ ollama_model: 'deepseek-r1:14b' }),
  );
  const vscode = {
    workspace: {
      getConfiguration() {
        return {
          get(key, fallback) {
            if (key === 'ollamaModel') {
              return 'mistral:latest';
            }
            if (key === 'ollamaEndpoint') {
              return 'http://127.0.0.1:11435';
            }
            return fallback;
          },
          inspect(key) {
            if (key === 'ollamaModel') {
              return {
                defaultValue: 'mistral:latest',
                globalValue: undefined,
                workspaceValue: undefined,
                workspaceFolderValue: undefined,
              };
            }
            if (key === 'ollamaEndpoint') {
              return {
                defaultValue: 'http://127.0.0.1:11435',
                globalValue: undefined,
                workspaceValue: undefined,
                workspaceFolderValue: undefined,
              };
            }
            return undefined;
          },
        };
      },
    },
  };
  try {
    const model = await resolveEffectiveOllamaModel(vscode);
    assert.equal(model, 'deepseek-r1:14b');
  } finally {
    process.env.XDG_CONFIG_HOME = prev;
  }
});
