'use strict';

const crypto = require('node:crypto');

const OPEN_AGENT_SURFACE_COMMAND = 'leVibeNative.openAgentSurface';
const OPEN_OLLAMA_SETUP_HELP_COMMAND = 'leVibeNative.openOllamaSetupHelp';
const OPEN_MODEL_PULL_HELP_COMMAND = 'leVibeNative.openModelPullHelp';
const OPEN_WORKSPACE_SETUP_COMMAND = 'leVibeNative.openWorkspaceSetup';
const VIEW_CHAT_USAGE_COMMAND = 'leVibeNative.viewChatUsage';
const EXPORT_CHAT_TRANSCRIPT_COMMAND = 'leVibeNative.exportChatTranscript';
const CLEAR_CHAT_TRANSCRIPT_COMMAND = 'leVibeNative.clearChatTranscript';
const PICK_CONTEXT_FILE_COMMAND = 'leVibeNative.pickContextFile';
const CLEAR_CONTEXT_FILES_COMMAND = 'leVibeNative.clearContextFiles';
const EMIT_OPERATOR_HANDOFF_COMMAND = 'leVibeNative.emitOperatorHandoff';
const OPEN_THIRD_PARTY_MIGRATION_COMMAND = 'leVibeNative.openThirdPartyMigrationGuide';

const { STARTUP_STATES, resolveStartupSnapshot, getStateContent } = require('./readiness');
const { createOllamaClient } = require('./ollama');
const { createChatController } = require('./chat');
const { isSafeRelativePath, clipTextByBudget, buildPromptWithContext } = require('./workspace-context');
const { handoffAuditPath, buildOperatorHandoffEvent, appendOperatorHandoffAudit } = require('./operator-handoff');
const { formatOllamaDiagnostic } = require('./retry-helpers');
const {
  loadWizardState,
  saveWizardState,
  advanceStep,
  markCheckpoint,
  completeWizard,
  FINAL_STEP_INDEX,
} = require('./first-run-wizard');
const {
  transcriptPath,
  appendEntry,
  getTranscriptStats,
  readTranscriptRaw,
  clearTranscript,
} = require('./chat-transcript');
const { isFirstPartyAgentSurfaceEnabled } = require('./feature-flags');
const { runThirdPartyMigrationGuide, scheduleThirdPartyMigrationNudge } = require('./third-party-migration');
const { validateEditProposal, EDIT_PROPOSAL_KIND } = require('./edit-proposal');
const { buildUnifiedDiff, canApplyAfterPreview } = require('./edit-preview');

function getTranscriptContext(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const workspaceUri = vscode.workspace.workspaceFolders?.[0]?.uri.toString() ?? 'no-workspace';
  return {
    workspaceUri,
    transcriptFile: transcriptPath(workspaceUri),
    transcriptCaps: {
      maxBytes: config.get('chatTranscriptMaxBytes', 524288),
      maxMessages: config.get('chatTranscriptMaxMessages', 200),
    },
  };
}

function getContextBudget(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  return {
    maxFiles: config.get('contextMaxFiles', 4),
    maxCharsPerFile: config.get('contextMaxCharsPerFile', 1200),
    maxLinesPerFile: config.get('contextMaxLinesPerFile', 80),
    maxTotalChars: config.get('contextMaxTotalChars', 3200),
  };
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function firstRunWizardHtml(step) {
  const safeStep = Math.min(Math.max(Number(step) || 0, 0), FINAL_STEP_INDEX);
  const steps = [
    {
      title: 'Lé Vibe Chat — Welcome',
      body: 'This first-run checklist ends in an actionable agent surface (no empty gray panel). Lé Vibe Chat is local-first: no silent cloud fallback.',
    },
    {
      title: 'Checkpoint 1 — Local-first and storage',
      body: 'Transcripts and audit data live under ~/.config/le-vibe/ with explicit caps. You can view usage, export, and clear from the panel after setup.',
    },
    {
      title: 'Checkpoint 2 — Local Ollama',
      body: 'After this wizard, the panel shows live readiness (reachable Ollama, model present). If you are not ready yet, use the remediation buttons (Open Ollama Setup Help, model install steps).',
    },
    {
      title: 'Checkpoint 3 — Workspace',
      body: 'Open a folder workspace for full context and workflows (e.g. .lvibe/workflows). Then use Local prompt test when the runtime state is ready or follow the on-screen actions.',
    },
  ];
  const cur = steps[safeStep];
  const progress = `Step ${safeStep + 1} of ${FINAL_STEP_INDEX + 1}`;
  const nextBtn =
    safeStep < FINAL_STEP_INDEX
      ? '<button id="wizNext">Next checkpoint</button>'
      : '<button id="wizFinish">Finish and open agent surface</button>';
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 1rem 1.25rem; line-height: 1.45; font-size: 13px; background: var(--vscode-editor-background); }
    h2 { margin-bottom: 0.35rem; }
    .muted { opacity: 0.85; }
    .card { border: 1px solid var(--vscode-panel-border); border-radius: 8px; padding: 0.85rem 1rem; margin-top: 0.75rem; background: var(--vscode-sideBar-background); }
    button { margin-right: 0.5rem; margin-top: 0.5rem; padding: 0.4rem 0.85rem; cursor: pointer; }
  </style>
</head>
<body>
  <h2>${escapeHtml(cur.title)}</h2>
  <p class="muted">${escapeHtml(progress)}</p>
  <div class="card">
    <p>${escapeHtml(cur.body)}</p>
  </div>
  <div>
    ${nextBtn}
    <button id="wizSkip">Skip onboarding</button>
  </div>
  <p class="muted">Skipping still opens the full Lé Vibe surface with explicit readiness states and actions.</p>
  <script>
    const vscode = acquireVsCodeApi();
    const next = document.getElementById('wizNext');
    const finish = document.getElementById('wizFinish');
    if (next) next.addEventListener('click', () => vscode.postMessage({ type: 'wizard', action: 'next' }));
    if (finish) finish.addEventListener('click', () => vscode.postMessage({ type: 'wizard', action: 'finish' }));
    document.getElementById('wizSkip').addEventListener('click', () => vscode.postMessage({ type: 'wizard', action: 'skip' }));
  </script>
</body>
</html>`;
}

function panelHtml(state, detailOverride, diagnostics, contextBudget) {
  const budget = contextBudget || {
    maxFiles: 4,
    maxCharsPerFile: 1200,
    maxLinesPerFile: 80,
    maxTotalChars: 3200,
  };
  const content = getStateContent(state, detailOverride);
  const actionButtons = content.actions
    .map((action) => `<button data-action="${escapeHtml(action.id)}">${escapeHtml(action.label)}</button>`)
    .join('');
  const actionsBlock = actionButtons || '<p class="muted">No actions required.</p>';
  const diagnosticsText = diagnostics ? `<pre class="diag">${escapeHtml(JSON.stringify(diagnostics, null, 2))}</pre>` : '';
  const states = STARTUP_STATES.map((value) => {
    const active = value === state ? 'class="active"' : '';
    return `<li ${active}>${escapeHtml(value)}</li>`;
  }).join('');
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 1rem 1.25rem; line-height: 1.45; font-size: 13px; }
    h2 { margin-bottom: 0.35rem; }
    .state { margin: 0.5rem 0 0.75rem 0; }
    .muted { opacity: 0.8; }
    .pill-list { display: flex; flex-wrap: wrap; gap: 0.35rem; list-style: none; padding: 0; margin: 0.25rem 0 1rem 0; }
    .pill-list li { border: 1px solid var(--vscode-panel-border); border-radius: 999px; padding: 0.15rem 0.55rem; }
    .pill-list li.active { border-color: var(--vscode-focusBorder); }
    button { margin-right: 0.5rem; margin-top: 0.5rem; padding: 0.35rem 0.75rem; cursor: pointer; }
    textarea { width: 100%; box-sizing: border-box; margin-top: 0.5rem; margin-bottom: 0.5rem; min-height: 74px; }
    .chat-log { margin-top: 0.75rem; border: 1px solid var(--vscode-panel-border); border-radius: 6px; padding: 0.6rem; min-height: 80px; white-space: pre-wrap; word-break: break-word; }
    .diag { margin-top: 0.75rem; background: var(--vscode-textCodeBlock-background); padding: 0.6rem; border-radius: 6px; white-space: pre-wrap; word-break: break-word; }
  </style>
</head>
<body>
  <h2>Lé Vibe Native Startup</h2>
  <p class="muted">Deterministic readiness state with local-first remediation actions.</p>
  <ul class="pill-list">${states}</ul>
  <div class="state"><strong>${escapeHtml(state)}</strong></div>
  <p>${escapeHtml(content.detail)}</p>
  <div>${actionsBlock}</div>
  <h3>Local prompt test</h3>
  <p class="muted">Send a prompt to local Ollama and receive streaming tokens.</p>
  <textarea id="promptInput" placeholder="Ask local model something..."></textarea>
  <div>
    <button id="sendPrompt">Send Prompt</button>
    <button id="cancelPrompt">Cancel Request</button>
    <button id="retryLastPrompt">Retry last prompt</button>
  </div>
  <div id="chatStatus" class="muted">Idle.</div>
  <div id="chatLog" class="chat-log"></div>
  <h3>Edit preview (workspace)</h3>
  <p class="muted">Unified diff before writing. When <code>leVibeNative.requireEditPreviewBeforeApply</code> is on (default), click <strong>Accept preview</strong> then <strong>Apply to file</strong> — no silent whole-file overwrite.</p>
  <div>
    <button data-action="previewSampleWorkspaceEdit">Preview sample workspace edit</button>
  </div>
  <div id="editPreviewSection" style="display:none;margin-top:0.5rem;">
    <pre id="editPreviewPre" class="diag"></pre>
    <div>
      <button type="button" id="editPreviewAccept">Accept preview</button>
      <button type="button" id="editPreviewReject">Reject</button>
      <button type="button" id="editPreviewApply" disabled>Apply to file</button>
    </div>
  </div>
  <h3>Workspace context</h3>
  <p class="muted">Token-budget rules: max ${escapeHtml(budget.maxFiles)} files; each excerpt up to ${escapeHtml(budget.maxCharsPerFile)} chars and ${escapeHtml(budget.maxLinesPerFile)} lines; total injected context capped at ${escapeHtml(budget.maxTotalChars)} chars.</p>
  <div>
    <button data-action="pickContextFile">Add context file</button>
    <button data-action="clearContextFiles">Clear context</button>
  </div>
  <h3>Operator handoff</h3>
  <p class="muted">Emit a reproducible handoff event to lvibe orchestration and append local audit evidence.</p>
  <div>
    <button data-action="emitOperatorHandoff">Emit handoff event</button>
  </div>
  <h3>Third-party agent migration</h3>
  <p class="muted">Moving from Continue, Cline, or similar? Open the checklist to avoid duplicate agent surfaces (no automatic uninstall).</p>
  <div>
    <button data-action="openThirdPartyMigrationGuide">Open migration guide</button>
  </div>
  <h3>Lé Vibe Chat storage</h3>
  <p class="muted">Local JSONL under ~/.config/le-vibe/levibe-native-chat/</p>
  <div>
    <button data-action="viewChatUsage">View usage</button>
    <button data-action="exportChatTranscript">Export transcript</button>
    <button data-action="clearChatTranscript">Clear transcript</button>
  </div>
  ${diagnosticsText}
  <script>
    const vscode = acquireVsCodeApi();
    document.querySelectorAll('button[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        vscode.postMessage({ type: 'action', actionId: button.getAttribute('data-action') });
      });
    });
    document.getElementById('sendPrompt').addEventListener('click', () => {
      const prompt = document.getElementById('promptInput').value || '';
      vscode.postMessage({ type: 'chat', actionId: 'sendPrompt', prompt });
    });
    document.getElementById('cancelPrompt').addEventListener('click', () => {
      vscode.postMessage({ type: 'chat', actionId: 'cancelPrompt' });
    });
    document.getElementById('retryLastPrompt').addEventListener('click', () => {
      vscode.postMessage({ type: 'chat', actionId: 'retryLastPrompt' });
    });
    window.addEventListener('message', (event) => {
      const msg = event.data;
      if (msg && msg.type === 'editPreview') {
        const sec = document.getElementById('editPreviewSection');
        const pre = document.getElementById('editPreviewPre');
        const applyBtn = document.getElementById('editPreviewApply');
        sec.style.display = 'block';
        pre.textContent = msg.unifiedDiff || '';
        applyBtn.disabled = msg.applyEnabled !== true;
        return;
      }
      if (msg && msg.type === 'editPreviewUpdate') {
        if (msg.clear) {
          document.getElementById('editPreviewSection').style.display = 'none';
          document.getElementById('editPreviewPre').textContent = '';
          document.getElementById('editPreviewApply').disabled = true;
          return;
        }
        if (msg.applyEnabled) {
          document.getElementById('editPreviewApply').disabled = false;
        }
        return;
      }
      if (!msg || msg.type !== 'chatUpdate') {
        return;
      }
      const status = document.getElementById('chatStatus');
      const log = document.getElementById('chatLog');
      if (msg.status) {
        status.textContent = msg.status;
      }
      if (typeof msg.replaceLog === 'string') {
        log.textContent = msg.replaceLog;
      } else if (typeof msg.append === 'string') {
        log.textContent += msg.append;
      }
    });
    document.getElementById('editPreviewAccept').addEventListener('click', () => {
      vscode.postMessage({ type: 'editPreview', action: 'accept' });
    });
    document.getElementById('editPreviewReject').addEventListener('click', () => {
      vscode.postMessage({ type: 'editPreview', action: 'reject' });
    });
    document.getElementById('editPreviewApply').addEventListener('click', () => {
      vscode.postMessage({ type: 'editPreview', action: 'apply' });
    });
  </script>
</body>
</html>`;
}

function openAgentSurface() {
  const vscode = require('vscode');
  if (!isFirstPartyAgentSurfaceEnabled(vscode)) {
    void vscode.window
      .showInformationMessage(
        'Lé Vibe first-party agent surface is disabled (rollback). Set leVibeNative.enableFirstPartyAgentSurface to true in Settings to restore the Lé Vibe Chat panel.',
        'Open Settings',
      )
      .then((choice) => {
        if (choice === 'Open Settings') {
          void vscode.commands.executeCommand(
            'workbench.action.openSettings',
            'leVibeNative.enableFirstPartyAgentSurface',
          );
        }
      });
    return undefined;
  }
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const client = createOllamaClient({
    endpoint: config.get('ollamaEndpoint', 'http://127.0.0.1:11434'),
    timeoutMs: config.get('ollamaTimeoutMs', 2500),
    model: config.get('ollamaModel', 'mistral:latest'),
    streamStallMs: config.get('ollamaStreamStallMs', 60000),
    streamMaxMs: config.get('ollamaStreamMaxMs', 120000),
    maxRetries: config.get('ollamaMaxRetries', 2),
    retryDelayMs: config.get('ollamaRetryBackoffMs', 400),
  });
  const chat = createChatController(client, {
    maxRetries: config.get('ollamaMaxRetries', 2),
    retryDelayMs: config.get('ollamaRetryBackoffMs', 400),
  });
  const { transcriptFile, transcriptCaps } = getTranscriptContext(vscode);
  const contextBudget = getContextBudget(vscode);
  const selectedContexts = [];
  let latestStartupState = 'checking';
  let latestDiagnostics = { mode: 'startup_probe' };
  let lastPromptPlain = null;
  let editPreviewSession = null;
  let wizardState = loadWizardState();
  const showFirstRunWizard = config.get('showFirstRunWizard', true);
  const useWizard = showFirstRunWizard && !wizardState.complete;

  const panel = vscode.window.createWebviewPanel(
    'leVibeNativeReadiness',
    'Lé Vibe Native Readiness',
    vscode.ViewColumn.Active,
    { enableScripts: true, retainContextWhenHidden: true },
  );

  function beginMainReadiness() {
    panel.webview.html = panelHtml('checking', null, { mode: 'startup_probe' }, contextBudget);
    resolveStartupSnapshot(vscode).then((snapshot) => {
      latestStartupState = snapshot.state;
      latestDiagnostics = snapshot.diagnostics || {};
      panel.webview.html = panelHtml(snapshot.state, snapshot.detailOverride, snapshot.diagnostics, contextBudget);
      panel.webview.postMessage({
        type: 'chatUpdate',
        status:
          snapshot.state === 'ready'
            ? 'Lé Vibe Chat: runtime ready. Use Local prompt test below.'
            : 'Lé Vibe Chat: follow the highlighted readiness state and use the action buttons.',
      });
    });
  }

  if (useWizard) {
    panel.webview.html = firstRunWizardHtml(wizardState.step);
  } else {
    beginMainReadiness();
  }

  function runPromptSend(promptPlain, { skipUserTranscript = false } = {}) {
    const trimmed = String(promptPlain || '').trim();
    if (!trimmed) {
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Enter a prompt first.' });
      return;
    }
    lastPromptPlain = trimmed;
    const promptWithContext = buildPromptWithContext(trimmed, selectedContexts, contextBudget.maxTotalChars);
    if (!skipUserTranscript) {
      try {
        appendEntry(
          transcriptFile,
          {
            id: `u-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
            ts: Date.now(),
            role: 'user',
            content: trimmed,
          },
          transcriptCaps,
        );
      } catch {
        /* ignore transcript write failures; chat still works */
      }
    }
    let assistantBuffer = '';
    panel.webview.postMessage({
      type: 'chatUpdate',
      status: 'Streaming response from local Ollama...',
      replaceLog: '',
    });
    void chat.sendPrompt(promptWithContext, {
      onToken(token) {
        assistantBuffer += token;
        panel.webview.postMessage({ type: 'chatUpdate', append: token });
      },
      onRetry({ attempt, maxAttempts, willRetry, error }) {
        const detail = formatOllamaDiagnostic(error, client.endpoint);
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: willRetry
            ? `${detail} Retrying (${attempt}/${maxAttempts})...`
            : detail,
        });
      },
      onDone(cancelled) {
        if (!cancelled && assistantBuffer.length > 0) {
          try {
            appendEntry(
              transcriptFile,
              {
                id: `a-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
                ts: Date.now(),
                role: 'assistant',
                content: assistantBuffer,
              },
              transcriptCaps,
            );
          } catch {
            /* ignore */
          }
        }
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: cancelled ? 'Request cancelled.' : 'Response complete.',
        });
      },
      onError(error) {
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: formatOllamaDiagnostic(error, client.endpoint),
        });
      },
    });
  }

  panel.webview.onDidReceiveMessage((msg) => {
    if (!msg) {
      return;
    }
    if (msg.type === 'editPreview') {
      if (msg.action === 'accept') {
        if (editPreviewSession) {
          editPreviewSession.userAccepted = true;
        }
        panel.webview.postMessage({ type: 'editPreviewUpdate', applyEnabled: true });
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Edit preview accepted — you can Apply to file.',
        });
        return;
      }
      if (msg.action === 'reject') {
        editPreviewSession = null;
        panel.webview.postMessage({ type: 'editPreviewUpdate', clear: true });
        panel.webview.postMessage({ type: 'chatUpdate', status: 'Edit preview rejected.' });
        return;
      }
      if (msg.action === 'apply') {
        void (async () => {
          const cfg = vscode.workspace.getConfiguration('leVibeNative');
          const requirePreview = cfg.get('requireEditPreviewBeforeApply', true);
          if (!editPreviewSession) {
            await vscode.window.showWarningMessage('No pending edit preview.');
            return;
          }
          const gate = canApplyAfterPreview({
            requireEditPreviewBeforeApply: requirePreview,
            previewShown: editPreviewSession.previewShown,
            userAcceptedPreview: editPreviewSession.userAccepted,
          });
          if (!gate.ok) {
            await vscode.window.showWarningMessage(gate.reason);
            return;
          }
          try {
            await vscode.workspace.fs.writeFile(
              editPreviewSession.targetUri,
              Buffer.from(editPreviewSession.newText, 'utf8'),
            );
            const rel = vscode.workspace.asRelativePath(editPreviewSession.targetUri, false);
            await vscode.window.showInformationMessage(`Lé Vibe Chat: applied edit to ${rel}`);
          } catch (e) {
            await vscode.window.showErrorMessage(e && e.message ? e.message : String(e));
          }
          editPreviewSession = null;
          panel.webview.postMessage({ type: 'editPreviewUpdate', clear: true });
          panel.webview.postMessage({ type: 'chatUpdate', status: 'Edit applied to workspace file.' });
        })();
        return;
      }
      return;
    }
    if (msg.type === 'wizard') {
      const checkpointOrder = ['welcome', 'local_first', 'ollama_note', 'workspace_note'];
      if (msg.action === 'next') {
        const idx = wizardState.step;
        if (idx < FINAL_STEP_INDEX) {
          wizardState = markCheckpoint(wizardState, checkpointOrder[idx]);
          wizardState = advanceStep(wizardState);
          saveWizardState(wizardState);
          panel.webview.html = firstRunWizardHtml(wizardState.step);
        }
        return;
      }
      if (msg.action === 'finish') {
        wizardState = markCheckpoint(wizardState, checkpointOrder[FINAL_STEP_INDEX]);
        wizardState = completeWizard(wizardState);
        saveWizardState(wizardState);
        beginMainReadiness();
        return;
      }
      if (msg.action === 'skip') {
        wizardState = completeWizard(wizardState);
        saveWizardState(wizardState);
        beginMainReadiness();
        return;
      }
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'previewSampleWorkspaceEdit') {
      void (async () => {
        const folder = vscode.workspace.workspaceFolders?.[0];
        if (!folder) {
          await vscode.window.showWarningMessage('Open a folder workspace first to preview a sample edit.');
          return;
        }
        const rel = '.levibe-edit-preview-demo.txt';
        const targetUri = vscode.Uri.joinPath(folder.uri, rel);
        let before = '';
        try {
          const bytes = await vscode.workspace.fs.readFile(targetUri);
          before = Buffer.from(bytes).toString('utf8');
        } catch {
          before = '';
        }
        const after =
          before.length === 0
            ? '# Lé Vibe edit preview demo\n'
            : `${before.replace(/\s+$/, '')}\n# Lé Vibe edit preview demo\n`;
        const proposal = {
          kind: EDIT_PROPOSAL_KIND,
          proposals: [
            {
              targetUri: targetUri.toString(),
              edit: { kind: 'full_file', content: after },
            },
          ],
        };
        const validated = validateEditProposal(proposal);
        if (!validated.ok) {
          await vscode.window.showErrorMessage(`Invalid proposal: ${validated.errors.join('; ')}`);
          return;
        }
        const requirePreview = vscode.workspace
          .getConfiguration('leVibeNative')
          .get('requireEditPreviewBeforeApply', true);
        const diff = buildUnifiedDiff(before, after, rel);
        editPreviewSession = {
          targetUri,
          newText: after,
          previewShown: true,
          userAccepted: false,
        };
        panel.webview.postMessage({
          type: 'editPreview',
          unifiedDiff: diff,
          applyEnabled: !requirePreview,
        });
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: requirePreview
            ? 'Sample diff shown — Accept preview then Apply to file (or Reject).'
            : 'Sample diff shown — Apply to file is allowed without Accept (requireEditPreviewBeforeApply is off).',
        });
      })();
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openOllamaSetupHelp') {
      void vscode.commands.executeCommand(OPEN_OLLAMA_SETUP_HELP_COMMAND);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openModelPullHelp') {
      void vscode.commands.executeCommand(OPEN_MODEL_PULL_HELP_COMMAND);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openWorkspaceSetup') {
      void vscode.commands.executeCommand(OPEN_WORKSPACE_SETUP_COMMAND);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'pickContextFile') {
      void vscode.commands.executeCommand(PICK_CONTEXT_FILE_COMMAND).then((picked) => {
        if (!picked) {
          return;
        }
        if (selectedContexts.length >= contextBudget.maxFiles) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: `Context file cap reached (${contextBudget.maxFiles}). Clear context or raise cap.`,
          });
          return;
        }
        if (selectedContexts.find((entry) => entry.path === picked.path)) {
          panel.webview.postMessage({ type: 'chatUpdate', status: `Context already selected: ${picked.path}` });
          return;
        }
        selectedContexts.push(picked);
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: `Context selected (${selectedContexts.length}/${contextBudget.maxFiles}): ${picked.path}`,
        });
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'clearContextFiles') {
      selectedContexts.length = 0;
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Workspace context cleared.' });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openThirdPartyMigrationGuide') {
      void vscode.commands.executeCommand(OPEN_THIRD_PARTY_MIGRATION_COMMAND);
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Opening third-party migration guide…' });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'emitOperatorHandoff') {
      void vscode.commands.executeCommand(EMIT_OPERATOR_HANDOFF_COMMAND, {
        startupState: latestStartupState,
        diagnostics: latestDiagnostics,
        selectedContextPaths: selectedContexts.map((item) => item.path),
        transcriptFile,
        transcriptCaps,
        contextBudget,
      });
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Operator handoff event emitted.' });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'viewChatUsage') {
      const stats = getTranscriptStats(transcriptFile);
      void vscode.window.showInformationMessage(
        `Lé Vibe Chat: ${stats.lineCount} line(s), ${stats.fileBytes} byte(s) on disk. Path: ${stats.path}`,
      );
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: `Lé Vibe Chat usage: ${stats.lineCount} lines, ${stats.fileBytes} bytes.`,
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'exportChatTranscript') {
      void (async () => {
        const raw = readTranscriptRaw(transcriptFile);
        if (!raw.trim()) {
          await vscode.window.showInformationMessage('Lé Vibe Chat: nothing to export for this workspace.');
          return;
        }
        const uri = await vscode.window.showSaveDialog({
          defaultUri: vscode.Uri.file('levibe-chat-transcript.jsonl'),
          filters: { 'JSON Lines': ['jsonl'], 'All files': ['*'] },
          saveLabel: 'Export',
        });
        if (!uri) {
          return;
        }
        try {
          await vscode.workspace.fs.writeFile(uri, Buffer.from(raw, 'utf8'));
          await vscode.window.showInformationMessage(`Lé Vibe Chat transcript exported to ${uri.fsPath}`);
        } catch (e) {
          await vscode.window.showErrorMessage(`Export failed: ${e && e.message ? e.message : e}`);
        }
      })();
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'clearChatTranscript') {
      void (async () => {
        const pick = await vscode.window.showWarningMessage(
          'Clear Lé Vibe Chat transcript for this workspace? This cannot be undone.',
          { modal: true },
          'Clear',
        );
        if (pick !== 'Clear') {
          return;
        }
        try {
          clearTranscript(transcriptFile);
          await vscode.window.showInformationMessage('Lé Vibe Chat transcript cleared.');
          panel.webview.postMessage({ type: 'chatUpdate', status: 'Transcript cleared.' });
        } catch (e) {
          await vscode.window.showErrorMessage(`Clear failed: ${e && e.message ? e.message : e}`);
        }
      })();
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'sendPrompt') {
      runPromptSend(msg.prompt, { skipUserTranscript: false });
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'retryLastPrompt') {
      if (!lastPromptPlain) {
        panel.webview.postMessage({ type: 'chatUpdate', status: 'No previous prompt to retry.' });
        return;
      }
      runPromptSend(lastPromptPlain, { skipUserTranscript: true });
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'cancelPrompt') {
      const didCancel = chat.cancelPrompt();
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: didCancel ? 'Cancelling request...' : 'No request is currently running.',
      });
    }
  });
  return panel;
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const vscode = require('vscode');
  context.subscriptions.push(
    vscode.commands.registerCommand(EMIT_OPERATOR_HANDOFF_COMMAND, async (input) => {
      const config = vscode.workspace.getConfiguration('leVibeNative');
      const { workspaceUri, transcriptFile, transcriptCaps } = getTranscriptContext(vscode);
      const event = buildOperatorHandoffEvent({
        workspaceUri,
        startupState: input && input.startupState ? input.startupState : 'checking',
        diagnostics: (input && input.diagnostics) || {},
        ollamaEndpoint: config.get('ollamaEndpoint', 'http://127.0.0.1:11434'),
        ollamaModel: config.get('ollamaModel', 'mistral:latest'),
        selectedContextPaths: (input && input.selectedContextPaths) || [],
        contextBudget: (input && input.contextBudget) || getContextBudget(vscode),
        transcriptFile,
        transcriptCaps,
      });
      const auditFile = handoffAuditPath();
      appendOperatorHandoffAudit(auditFile, event);
      await vscode.window.showInformationMessage(
        `Lé Vibe Chat handoff event recorded: ${auditFile}`,
      );
    }),
    vscode.commands.registerCommand(PICK_CONTEXT_FILE_COMMAND, async () => {
      const folder = vscode.workspace.workspaceFolders?.[0];
      if (!folder) {
        await vscode.window.showWarningMessage('Open a folder workspace first.');
        return null;
      }
      const files = await vscode.workspace.findFiles('**/*', '**/{node_modules,.git,.lvibe}/**', 300);
      if (!files.length) {
        await vscode.window.showInformationMessage('No workspace files available for context selection.');
        return null;
      }
      const items = files.map((uri) => ({
        label: vscode.workspace.asRelativePath(uri, false),
        uri,
      }));
      const choice = await vscode.window.showQuickPick(items, {
        title: 'Select workspace file for Lé Vibe Chat context',
        placeHolder: 'Choose one file to include as prompt context excerpt',
      });
      if (!choice) {
        return null;
      }
      if (!isSafeRelativePath(choice.label)) {
        await vscode.window.showWarningMessage('Unsafe file reference blocked.');
        return null;
      }
      const ctx = getContextBudget(vscode);
      const bytes = await vscode.workspace.fs.readFile(choice.uri);
      const raw = Buffer.from(bytes).toString('utf8');
      const excerpt = clipTextByBudget(raw, ctx.maxCharsPerFile, ctx.maxLinesPerFile);
      return { path: choice.label, content: excerpt };
    }),
    vscode.commands.registerCommand(CLEAR_CONTEXT_FILES_COMMAND, async () => {
      await vscode.window.showInformationMessage(
        'Use the panel action "Clear context" to clear currently selected workspace context files.',
      );
    }),
    vscode.commands.registerCommand(VIEW_CHAT_USAGE_COMMAND, async () => {
      const { transcriptFile } = getTranscriptContext(vscode);
      const stats = getTranscriptStats(transcriptFile);
      await vscode.window.showInformationMessage(
        `Lé Vibe Chat: ${stats.lineCount} line(s), ${stats.fileBytes} byte(s) on disk.\n${stats.path}`,
      );
    }),
    vscode.commands.registerCommand(EXPORT_CHAT_TRANSCRIPT_COMMAND, async () => {
      const { transcriptFile } = getTranscriptContext(vscode);
      const raw = readTranscriptRaw(transcriptFile);
      if (!raw.trim()) {
        await vscode.window.showInformationMessage('Lé Vibe Chat: nothing to export for this workspace.');
        return;
      }
      const uri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file('levibe-chat-transcript.jsonl'),
        filters: { 'JSON Lines': ['jsonl'], 'All files': ['*'] },
        saveLabel: 'Export',
      });
      if (!uri) {
        return;
      }
      try {
        await vscode.workspace.fs.writeFile(uri, Buffer.from(raw, 'utf8'));
        await vscode.window.showInformationMessage(`Lé Vibe Chat transcript exported to ${uri.fsPath}`);
      } catch (e) {
        await vscode.window.showErrorMessage(`Export failed: ${e && e.message ? e.message : e}`);
      }
    }),
    vscode.commands.registerCommand(CLEAR_CHAT_TRANSCRIPT_COMMAND, async () => {
      const { transcriptFile } = getTranscriptContext(vscode);
      const pick = await vscode.window.showWarningMessage(
        'Clear Lé Vibe Chat transcript for this workspace? This cannot be undone.',
        { modal: true },
        'Clear',
      );
      if (pick !== 'Clear') {
        return;
      }
      try {
        clearTranscript(transcriptFile);
        await vscode.window.showInformationMessage('Lé Vibe Chat transcript cleared.');
      } catch (e) {
        await vscode.window.showErrorMessage(`Clear failed: ${e && e.message ? e.message : e}`);
      }
    }),
    vscode.commands.registerCommand(OPEN_THIRD_PARTY_MIGRATION_COMMAND, () => runThirdPartyMigrationGuide(vscode)),
    vscode.commands.registerCommand(OPEN_AGENT_SURFACE_COMMAND, openAgentSurface),
    vscode.commands.registerCommand(OPEN_OLLAMA_SETUP_HELP_COMMAND, () =>
      vscode.env.openExternal(vscode.Uri.parse('https://ollama.com/download/linux')),
    ),
    vscode.commands.registerCommand(OPEN_MODEL_PULL_HELP_COMMAND, () =>
      vscode.window.showInformationMessage('Run `ollama pull mistral:latest` to install a local model.'),
    ),
    vscode.commands.registerCommand(OPEN_WORKSPACE_SETUP_COMMAND, async () => {
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      if (!folder) {
        await vscode.window.showWarningMessage('Open a folder workspace first.');
        return;
      }
      const workflowUri = vscode.Uri.joinPath(folder.uri, '.lvibe', 'workflows', 'setup-workspace.md');
      try {
        await vscode.workspace.fs.stat(workflowUri);
        await vscode.window.showTextDocument(workflowUri);
      } catch {
        await vscode.window.showInformationMessage(
          'setup-workspace.md not found. Prepare the workspace to generate it.',
        );
      }
    }),
  );

  const config = vscode.workspace.getConfiguration('leVibeNative');
  const openStartup =
    config.get('openPanelOnStartup', true) && config.get('enableFirstPartyAgentSurface', true);
  if (openStartup) {
    setTimeout(() => {
      void vscode.commands.executeCommand(OPEN_AGENT_SURFACE_COMMAND);
    }, 0);
  }

  setTimeout(() => {
    void scheduleThirdPartyMigrationNudge(vscode);
  }, 4000);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
  OPEN_AGENT_SURFACE_COMMAND,
  OPEN_OLLAMA_SETUP_HELP_COMMAND,
  OPEN_MODEL_PULL_HELP_COMMAND,
  OPEN_WORKSPACE_SETUP_COMMAND,
  VIEW_CHAT_USAGE_COMMAND,
  EXPORT_CHAT_TRANSCRIPT_COMMAND,
  CLEAR_CHAT_TRANSCRIPT_COMMAND,
  PICK_CONTEXT_FILE_COMMAND,
  CLEAR_CONTEXT_FILES_COMMAND,
  EMIT_OPERATOR_HANDOFF_COMMAND,
  OPEN_THIRD_PARTY_MIGRATION_COMMAND,
  getTranscriptContext,
  getContextBudget,
  panelHtml,
  firstRunWizardHtml,
  isFirstPartyAgentSurfaceEnabled,
};
