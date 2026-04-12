'use strict';

/**
 * Sync VS Code `leVibe.*` settings ↔ ~/.config/le-vibe/user-settings.json
 * (schema user-settings.v1 — see schemas/user-settings.v1.example.json).
 */

const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const os = require('os');

const SECTION = 'leVibe';

function userSettingsPath() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'user-settings.json');
}

function atomicWrite(filePath, text) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const tmp = `${filePath}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, text, 'utf8');
  fs.renameSync(tmp, filePath);
}

function diskFromConfig() {
  const c = vscode.workspace.getConfiguration(SECTION);
  const cap = c.get('lvibeCapMbDefault');
  return {
    schema_version: 'user-settings.v1',
    lvibe_cap_mb_default: cap === undefined ? null : cap,
    model: {
      use_recommended: c.get('model.useRecommended') !== false,
      override_tag: c.get('model.overrideTag') ?? null,
      allow_pull_if_disk_ok: c.get('model.allowPullIfDiskOk') !== false,
    },
    ide: {
      show_chat_commands_help: c.get('ide.showChatCommandsHelp') !== false,
      show_new_workspace_hints: c.get('ide.showNewWorkspaceHints') !== false,
    },
    meta: {
      note: 'Optional ~/.config/le-vibe/user-settings.json — synced from VS Code Settings (Lé Vibe).',
    },
  };
}

function readDisk() {
  const p = userSettingsPath();
  if (!fs.existsSync(p)) {
    return null;
  }
  try {
    const raw = JSON.parse(fs.readFileSync(p, 'utf8'));
    return raw && typeof raw === 'object' ? raw : null;
  } catch {
    return null;
  }
}

function escapeHtml(t) {
  return String(t)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * @param {vscode.ExtensionContext} context
 */
function showChatCommandsHelpPanel(context) {
  const c = vscode.workspace.getConfiguration(SECTION);
  if (c.get('ide.showChatCommandsHelp') === false) {
    void vscode.window.showInformationMessage(
      'Lé Vibe: enable Settings → Lé Vibe → IDE: Show chat commands help to use this panel.',
    );
    return;
  }
  const mdPath = path.join(context.extensionPath, 'help-chat-commands.md');
  let body = 'help-chat-commands.md not found in extension.';
  try {
    body = fs.readFileSync(mdPath, 'utf8');
  } catch {
    /* keep fallback */
  }
  const panel = vscode.window.createWebviewPanel(
    'leVibeChatCommandsHelp',
    'Lé Vibe — Chat commands & mentions',
    vscode.ViewColumn.Active,
    { enableScripts: true, retainContextWhenHidden: true },
  );
  const nonce = String(Math.random()).slice(2);
  panel.webview.html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';" />
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 1rem 1.25rem; line-height: 1.45; font-size: 13px; }
    pre { white-space: pre-wrap; word-break: break-word; margin: 0 0 1rem 0; }
    button { margin-top: 0.5rem; padding: 0.35rem 0.75rem; cursor: pointer; }
    code { font-family: var(--vscode-editor-font-family); background: var(--vscode-textCodeBlock-background); padding: 0 0.2rem; }
  </style>
</head>
<body>
  <pre>${escapeHtml(body)}</pre>
  <button id="openWf">Open .lvibe/workflows/setup-workspace.md (if present)</button>
  <script nonce="${nonce}">
    const vscode = acquireVsCodeApi();
    document.getElementById('openWf').addEventListener('click', () => {
      vscode.postMessage({ type: 'openWorkflow' });
    });
  </script>
</body>
</html>`;
  panel.webview.onDidReceiveMessage((msg) => {
    if (msg && msg.type === 'openWorkflow') {
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      if (!folder) {
        void vscode.window.showWarningMessage('Open a folder workspace first.');
        return;
      }
      const uri = vscode.Uri.joinPath(folder.uri, '.lvibe', 'workflows', 'setup-workspace.md');
      void vscode.workspace.fs.stat(uri).then(
        () => void vscode.window.showTextDocument(uri),
        () =>
          void vscode.window.showInformationMessage(
            'setup-workspace.md not found — run workspace prepare or copy from le-vibe/templates/workflows/setup-workspace.md',
          ),
      );
    }
  });
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  let suppress = false;

  async function pushDiskToConfig() {
    const data = readDisk();
    if (!data) {
      return;
    }
    const c = vscode.workspace.getConfiguration(SECTION);
    const updates = [];
    if ('lvibe_cap_mb_default' in data) {
      updates.push(c.update('lvibeCapMbDefault', data.lvibe_cap_mb_default, vscode.ConfigurationTarget.Global));
    }
    const m = data.model;
    if (m && typeof m === 'object') {
      if ('use_recommended' in m) {
        updates.push(c.update('model.useRecommended', !!m.use_recommended, vscode.ConfigurationTarget.Global));
      }
      if ('override_tag' in m) {
        updates.push(c.update('model.overrideTag', m.override_tag, vscode.ConfigurationTarget.Global));
      }
      if ('allow_pull_if_disk_ok' in m) {
        updates.push(c.update('model.allowPullIfDiskOk', !!m.allow_pull_if_disk_ok, vscode.ConfigurationTarget.Global));
      }
    }
    const ide = data.ide;
    if (ide && typeof ide === 'object') {
      if ('show_chat_commands_help' in ide) {
        updates.push(c.update('ide.showChatCommandsHelp', !!ide.show_chat_commands_help, vscode.ConfigurationTarget.Global));
      }
      if ('show_new_workspace_hints' in ide) {
        updates.push(c.update('ide.showNewWorkspaceHints', !!ide.show_new_workspace_hints, vscode.ConfigurationTarget.Global));
      }
    }
    if (updates.length === 0) {
      return;
    }
    suppress = true;
    try {
      await Promise.all(updates);
    } finally {
      suppress = false;
    }
  }

  function writeConfigToDisk() {
    if (suppress) {
      return;
    }
    const obj = diskFromConfig();
    const text = `${JSON.stringify(obj, null, 2)}\n`;
    try {
      atomicWrite(userSettingsPath(), text);
    } catch (e) {
      void vscode.window.showWarningMessage(`Lé Vibe: could not write user-settings.json: ${e}`);
    }
  }

  const sub = vscode.workspace.onDidChangeConfiguration((e) => {
    if (e.affectsConfiguration(SECTION)) {
      writeConfigToDisk();
    }
  });

  context.subscriptions.push(sub);

  context.subscriptions.push(
    vscode.commands.registerCommand('leVibe.showChatCommandsHelp', () => showChatCommandsHelpPanel(context)),
  );

  void pushDiskToConfig().then(() => {
    writeConfigToDisk();
  });
}

function deactivate() {}

module.exports = { activate, deactivate };
