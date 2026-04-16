const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');
const { registerLeVibeChatStatusBar, REFRESH_INTERVAL_MS } = require('../status-bar-entry');

test('package.json contributes leVibeNative.showStatusBarEntry default false (task-n17-3)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const p = props['leVibeNative.showStatusBarEntry'];
  assert.ok(p);
  assert.equal(p.type, 'boolean');
  assert.equal(p.default, false);
});

test('registerLeVibeChatStatusBar creates item when enabled + first-party on (task-n17-3)', () => {
  const created = [];
  const vscode = {
    StatusBarAlignment: { Right: 1 },
    window: {
      createStatusBarItem(alignment, priority) {
        const self = {
          text: '',
          tooltip: '',
          command: '',
          name: '',
          show() {},
          dispose() {
            created.push('disposed');
          },
        };
        created.push({ alignment, priority, self });
        return self;
      },
    },
    workspace: {
      getConfiguration() {
        return {
          get(key, def) {
            const map = {
              showStatusBarEntry: true,
              enableFirstPartyAgentSurface: true,
              ollamaEndpoint: 'http://127.0.0.1:11434',
              ollamaTimeoutMs: 100,
              ollamaModel: 'mistral:latest',
              ollamaStreamStallMs: 60000,
              ollamaStreamMaxMs: 120000,
              ollamaMaxRetries: 0,
              ollamaRetryBackoffMs: 100,
            };
            return key in map ? map[key] : def;
          },
        };
      },
      onDidChangeConfiguration() {
        return { dispose() {} };
      },
    },
    Disposable: class {
      constructor(fn) {
        this._fn = fn;
      }
      dispose() {
        this._fn();
      }
    },
  };

  const subs = [];
  const context = { subscriptions: subs };
  registerLeVibeChatStatusBar(vscode, context, { openAgentSurfaceCommand: 'leVibeNative.openAgentSurface' });
  assert.ok(created.length >= 1);
  const first = created[0];
  assert.equal(first.alignment, vscode.StatusBarAlignment.Right);
  assert.equal(first.priority, 25);
  assert.equal(first.self.command, 'leVibeNative.openAgentSurface');
  assert.equal(first.self.name, 'Lé Vibe Chat status');
  assert.equal(typeof REFRESH_INTERVAL_MS, 'number');
  assert.equal(subs.length, 1);
  subs[0].dispose();
  assert.ok(created.includes('disposed'));
});

test('registerLeVibeChatStatusBar skips item when showStatusBarEntry is false (task-n17-3)', () => {
  let createCount = 0;
  const vscode = {
    StatusBarAlignment: { Right: 1 },
    window: {
      createStatusBarItem() {
        createCount += 1;
        return { text: '', show() {}, dispose() {} };
      },
    },
    workspace: {
      getConfiguration() {
        return {
          get(key, def) {
            if (key === 'showStatusBarEntry') {
              return false;
            }
            return def;
          },
        };
      },
      onDidChangeConfiguration() {
        return { dispose() {} };
      },
    },
    Disposable: class {
      constructor(fn) {
        this._fn = fn;
      }
      dispose() {
        this._fn();
      }
    },
  };
  const context = { subscriptions: [] };
  registerLeVibeChatStatusBar(vscode, context, { openAgentSurfaceCommand: 'leVibeNative.openAgentSurface' });
  assert.equal(createCount, 0);
  context.subscriptions[0].dispose();
});

test('registerLeVibeChatStatusBar skips when first-party surface disabled (task-n17-3)', () => {
  let createCount = 0;
  const vscode = {
    StatusBarAlignment: { Right: 1 },
    window: {
      createStatusBarItem() {
        createCount += 1;
        return { text: '', show() {}, dispose() {} };
      },
    },
    workspace: {
      getConfiguration() {
        return {
          get(key, def) {
            if (key === 'showStatusBarEntry') {
              return true;
            }
            if (key === 'enableFirstPartyAgentSurface') {
              return false;
            }
            return def;
          },
        };
      },
      onDidChangeConfiguration() {
        return { dispose() {} };
      },
    },
    Disposable: class {
      constructor(fn) {
        this._fn = fn;
      }
      dispose() {
        this._fn();
      }
    },
  };
  const context = { subscriptions: [] };
  registerLeVibeChatStatusBar(vscode, context, { openAgentSurfaceCommand: 'x' });
  assert.equal(createCount, 0);
  context.subscriptions[0].dispose();
});
