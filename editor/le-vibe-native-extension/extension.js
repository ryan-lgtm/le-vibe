'use strict';

const crypto = require('node:crypto');

const OPEN_AGENT_SURFACE_COMMAND = 'leVibeNative.openAgentSurface';
const OPEN_OLLAMA_SETUP_HELP_COMMAND = 'leVibeNative.openOllamaSetupHelp';
const OPEN_MODEL_PULL_HELP_COMMAND = 'leVibeNative.openModelPullHelp';
const OPEN_WORKSPACE_SETUP_COMMAND = 'leVibeNative.openWorkspaceSetup';
const START_NEW_CHAT_SESSION_COMMAND = 'leVibeNative.startNewChatSession';
const RESTORE_RECENT_PROMPT_COMMAND = 'leVibeNative.restoreRecentPrompt';
const VIEW_CHAT_USAGE_COMMAND = 'leVibeNative.viewChatUsage';
const EXPORT_CHAT_TRANSCRIPT_COMMAND = 'leVibeNative.exportChatTranscript';
const CLEAR_CHAT_TRANSCRIPT_COMMAND = 'leVibeNative.clearChatTranscript';
const PICK_CONTEXT_FILE_COMMAND = 'leVibeNative.pickContextFile';
const CLEAR_CONTEXT_FILES_COMMAND = 'leVibeNative.clearContextFiles';
const EMIT_OPERATOR_HANDOFF_COMMAND = 'leVibeNative.emitOperatorHandoff';
const OPEN_THIRD_PARTY_MIGRATION_COMMAND = 'leVibeNative.openThirdPartyMigrationGuide';
const APPLY_SELECTION_DEMO_REPLACE_COMMAND = 'leVibeNative.applySelectionDemoReplace';
const CREATE_WORKSPACE_FILE_COMMAND = 'leVibeNative.createWorkspaceFile';
const CREATE_WORKSPACE_FOLDER_COMMAND = 'leVibeNative.createWorkspaceFolder';
const MOVE_WORKSPACE_PATH_COMMAND = 'leVibeNative.moveWorkspacePath';
const DELETE_WORKSPACE_PATH_COMMAND = 'leVibeNative.deleteWorkspacePath';
const ASK_CHAT_ABOUT_SELECTION_COMMAND = 'leVibeNative.askChatAboutSelection';
const RUN_COMMAND_IN_INTEGRATED_TERMINAL_COMMAND = 'leVibeNative.runCommandInIntegratedTerminal';
const CLEAR_TERMINAL_SESSION_ALLOW_COMMAND = 'leVibeNative.clearTerminalSessionAllow';
const ADD_CONTEXT_AT_FILE_COMMAND = 'leVibeNative.addContextAtFile';
const ADD_CONTEXT_AT_FOLDER_COMMAND = 'leVibeNative.addContextAtFolder';
const ADD_CURRENT_FILE_OUTLINE_COMMAND = 'leVibeNative.addCurrentFileOutlineToContext';

/** @type {null | { path: string, content: string, selectionRange: { startLine: number, startCharacter: number, endLine: number, endCharacter: number } }} */
let pendingSelectionContext = null;

const { STARTUP_STATES, resolveStartupSnapshot, getStateContent } = require('./readiness');
const { createOllamaClient } = require('./ollama');
const { createChatController } = require('./chat');
const { isSafeRelativePath, clipTextByBudget, buildPromptWithContext } = require('./workspace-context');
const {
  loadGitignoreMatcher,
  loadContextFileWithGuards,
  relativePosixForGitignore,
} = require('./context-file-guards');
const { buildSelectionContextEntry, prefillPromptForSelection } = require('./selection-chat-context');
const { QUICK_ACTION_ID, getQuickActionTemplate } = require('./chat-quick-actions');

/** Panel `data-action` → quick template id (task-n12-2). */
const PANEL_QUICK_ACTION_MAP = {
  quickActionExplain: QUICK_ACTION_ID.EXPLAIN,
  quickActionRefactorSelection: QUICK_ACTION_ID.REFACTOR_SELECTION,
  quickActionGenerateTests: QUICK_ACTION_ID.GENERATE_TESTS,
};
const {
  validateWorkspaceRelativeCreatePath,
  createWorkspaceFile,
  createWorkspaceFolder,
  moveWorkspaceEntry,
  deleteWorkspaceEntry,
  uriForNormalizedRelative,
} = require('./workspace-fs-actions');
const {
  workspaceFsOpsAuditPath,
  buildWorkspaceFsOpsAuditEvent,
  appendWorkspaceFsOpsAudit,
} = require('./workspace-fs-ops-audit');
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
  loadTranscript,
  getTranscriptStats,
  readTranscriptRaw,
  clearTranscript,
} = require('./chat-transcript');
const { isFirstPartyAgentSurfaceEnabled } = require('./feature-flags');
const { runThirdPartyMigrationGuide, scheduleThirdPartyMigrationNudge } = require('./third-party-migration');
const { validateEditProposal, EDIT_PROPOSAL_KIND, formatEditProposalValidationForUser } = require('./edit-proposal');
const { buildUnifiedDiff, canApplyAfterPreview } = require('./edit-preview');
const { applyEditProposalBatchAsWorkspaceEdit } = require('./workspace-edit-apply');
const { resolveSingleSelectionForPartialApply } = require('./selection-apply');
const { buildPreviewRevision, checkDiskContentMatchesRevision } = require('./edit-conflict');
const { validateWorkspacePlan, WORKSPACE_PLAN_KIND } = require('./workspace-plan');
const {
  executeValidatedWorkspacePlan,
  applyWorkspacePlanRollbackInverses,
} = require('./workspace-plan-exec');
const { dryRunValidatedWorkspacePlan } = require('./workspace-plan-dry-run');
const { runCommandInVisibleTerminal, clearTerminalSessionAllow } = require('./terminal-exec');
const {
  pickAtFileContext,
  pickAtFolderContext,
  FILE_PICKER_MAX_SCAN_URIS,
} = require('./at-mention-context');
const { fetchCurrentFileOutlineForContext } = require('./outline-context');
const { registerLeVibeChatStatusBar } = require('./status-bar-entry');

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WebviewPanel | null} panel
 * @returns {Promise<import('vscode').Uri | null>}
 */
async function runCreateWorkspaceFileInteractive(vscode, panel) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Open a folder workspace first.' });
    }
    return null;
  }
  const rel = await vscode.window.showInputBox({
    title: 'Create file under workspace',
    prompt:
      'Workspace-relative path only. Blocked segments: .git, .ssh, .gnupg, node_modules, .env — no .. or absolute paths.',
    placeHolder: 'e.g. notes/demo.md',
    validateInput: (value) => {
      const r = validateWorkspaceRelativeCreatePath(value);
      return r.ok ? undefined : r.userMessage.replace(/^Lé Vibe Chat: /, '');
    },
  });
  if (!rel) {
    return null;
  }
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const openAfter = config.get('openDocumentAfterWorkspaceCreate', true);
  const result = await createWorkspaceFile(vscode, folder, rel, { openAfterCreate: openAfter });
  if (!result.ok) {
    await vscode.window.showWarningMessage(result.userMessage);
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: result.userMessage });
    }
    return null;
  }
  const label = vscode.workspace.asRelativePath(result.uri, false);
  await vscode.window.showInformationMessage(`Lé Vibe Chat: created ${label}`);
  if (panel) {
    panel.webview.postMessage({ type: 'chatUpdate', status: `Created file: ${label}` });
  }
  return result.uri;
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WebviewPanel | null} panel
 * @returns {Promise<import('vscode').Uri | null>}
 */
async function runCreateWorkspaceFolderInteractive(vscode, panel) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Open a folder workspace first.' });
    }
    return null;
  }
  const rel = await vscode.window.showInputBox({
    title: 'Create folder under workspace',
    prompt:
      'Workspace-relative path only. Blocked segments: .git, .ssh, .gnupg, node_modules, .env — no .. or absolute paths.',
    placeHolder: 'e.g. src/components/widgets',
    validateInput: (value) => {
      const r = validateWorkspaceRelativeCreatePath(value);
      return r.ok ? undefined : r.userMessage.replace(/^Lé Vibe Chat: /, '');
    },
  });
  if (!rel) {
    return null;
  }
  const result = await createWorkspaceFolder(vscode, folder, rel);
  if (!result.ok) {
    await vscode.window.showWarningMessage(result.userMessage);
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: result.userMessage });
    }
    return null;
  }
  const label = vscode.workspace.asRelativePath(result.uri, false);
  await vscode.window.showInformationMessage(`Lé Vibe Chat: created folder ${label}`);
  if (panel) {
    panel.webview.postMessage({ type: 'chatUpdate', status: `Created folder: ${label}` });
  }
  return result.uri;
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WebviewPanel | null} panel
 * @returns {Promise<{ from: string, to: string } | null>}
 */
async function runMoveWorkspacePathInteractive(vscode, panel) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Open a folder workspace first.' });
    }
    return null;
  }
  const promptOpts = {
    prompt:
      'Workspace-relative path only. Blocked segments: .git, .ssh, .gnupg, node_modules, .env — no .. or absolute paths.',
    validateInput: (value) => {
      const r = validateWorkspaceRelativeCreatePath(value);
      return r.ok ? undefined : r.userMessage.replace(/^Lé Vibe Chat: /, '');
    },
  };
  const fromRel = await vscode.window.showInputBox({
    title: 'Move / rename — source path',
    placeHolder: 'e.g. notes/old-name.md',
    ...promptOpts,
  });
  if (!fromRel) {
    return null;
  }
  const toRel = await vscode.window.showInputBox({
    title: 'Move / rename — destination path',
    placeHolder: 'e.g. notes/new-name.md',
    ...promptOpts,
  });
  if (!toRel) {
    return null;
  }
  const result = await moveWorkspaceEntry(vscode, folder, fromRel, toRel);
  if (!result.ok) {
    await vscode.window.showWarningMessage(result.userMessage);
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: result.userMessage });
    }
    return null;
  }
  const fromLabel = vscode.workspace.asRelativePath(result.fromUri, false);
  const toLabel = vscode.workspace.asRelativePath(result.toUri, false);
  await vscode.window.showInformationMessage(`Lé Vibe Chat: moved ${fromLabel} → ${toLabel}`);
  if (panel) {
    panel.webview.postMessage({ type: 'chatUpdate', status: `Moved: ${fromLabel} → ${toLabel}` });
  }
  return { from: fromLabel, to: toLabel };
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WebviewPanel | null} panel
 * @returns {Promise<import('vscode').Uri | null>}
 */
async function runDeleteWorkspacePathInteractive(vscode, panel) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Open a folder workspace first.' });
    }
    return null;
  }
  const promptOpts = {
    prompt:
      'Workspace-relative path only. Blocked segments: .git, .ssh, .gnupg, node_modules, .env — no .. or absolute paths. Step 2 is a confirmation dialog — nothing is deleted until you confirm there.',
    validateInput: (value) => {
      const r = validateWorkspaceRelativeCreatePath(value);
      return r.ok ? undefined : r.userMessage.replace(/^Lé Vibe Chat: /, '');
    },
  };
  const rel = await vscode.window.showInputBox({
    title: 'Delete file or folder — path (step 1 of 2)',
    placeHolder: 'e.g. tmp/old-file.txt',
    ...promptOpts,
  });
  if (!rel) {
    return null;
  }
  const vf = validateWorkspaceRelativeCreatePath(rel);
  if (!vf.ok) {
    await vscode.window.showWarningMessage(vf.userMessage);
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: vf.userMessage });
    }
    return null;
  }
  const displayPath = vf.normalizedRelative;
  const pick = await vscode.window.showWarningMessage(
    `Permanently delete "${displayPath}" from this workspace? This cannot be undone from Lé Vibe Chat. A line is appended to workspace-fs-ops-audit.jsonl under ~/.config/le-vibe/levibe-native-chat/.`,
    { modal: true },
    'Delete',
  );
  if (pick !== 'Delete') {
    return null;
  }

  const auditFile = workspaceFsOpsAuditPath();
  const wsUri = folder.uri.toString();
  const targetUriGuess = uriForNormalizedRelative(vscode, folder.uri, displayPath);

  const result = await deleteWorkspaceEntry(vscode, folder, displayPath);
  if (result.ok) {
    appendWorkspaceFsOpsAudit(
      auditFile,
      buildWorkspaceFsOpsAuditEvent({
        op: 'delete',
        workspaceUri: wsUri,
        relativePath: displayPath,
        targetUri: result.uri.toString(),
        outcome: 'success',
        isDirectory: result.isDirectory,
      }),
    );
    const label = vscode.workspace.asRelativePath(result.uri, false);
    await vscode.window.showInformationMessage(`Lé Vibe Chat: deleted ${label}`);
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: `Deleted: ${label}` });
    }
    return result.uri;
  }

  appendWorkspaceFsOpsAudit(
    auditFile,
    buildWorkspaceFsOpsAuditEvent({
      op: 'delete',
      workspaceUri: wsUri,
      relativePath: displayPath,
      targetUri: targetUriGuess.toString(),
      outcome: 'failed',
      detail: result.userMessage,
    }),
  );
  await vscode.window.showWarningMessage(result.userMessage);
  if (panel) {
    panel.webview.postMessage({ type: 'chatUpdate', status: result.userMessage });
  }
  return null;
}

function buildSampleDemoWorkspacePlan(vscode, folder) {
  const stamp = Date.now();
  const relA = `.lvibe/levibe-plan-demo-${stamp}.txt`;
  const relB = `.lvibe/levibe-plan-demo-${stamp}-moved.txt`;
  const uriA = vscode.Uri.joinPath(folder.uri, relA);
  const uriB = vscode.Uri.joinPath(folder.uri, relB);
  return {
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      {
        id: 'demo-create',
        op: 'create_file',
        targetUri: uriA.toString(),
        content: '# Lé Vibe workspace plan demo\n',
      },
      {
        id: 'demo-edit',
        op: 'apply_edit',
        targetUri: uriA.toString(),
        edit: {
          kind: 'full_file',
          content: '# Lé Vibe workspace plan demo\n# second line from apply_edit\n',
        },
      },
      {
        id: 'demo-move',
        op: 'move_file',
        fromUri: uriA.toString(),
        toUri: uriB.toString(),
      },
    ],
  };
}

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
      ? '<button type="button" id="wizNext" title="Next checkpoint" aria-label="Next checkpoint">Next checkpoint</button>'
      : '<button type="button" id="wizFinish" title="Finish and open agent surface" aria-label="Finish and open agent surface">Finish and open agent surface</button>';
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 1rem 1.25rem; line-height: 1.45; font-size: 13px; background: var(--vscode-editor-background); }
    h2 { margin-bottom: 0.35rem; }
    .muted { opacity: 0.85; }
    .card { border: 1px solid var(--vscode-panel-border); border-radius: 8px; padding: 0.85rem 1rem; margin-top: 0.75rem; background: var(--vscode-sideBar-background); }
    button { margin-right: 0.5rem; margin-top: 0.5rem; padding: 0.4rem 0.85rem; cursor: pointer; }
    .skip-link { position: absolute; left: -10000px; top: auto; width: 1px; height: 1px; overflow: hidden; }
    .skip-link:focus { position: static; width: auto; height: auto; left: auto; padding: 0.35rem 0.55rem; margin-bottom: 0.5rem; background: var(--vscode-button-background); color: var(--vscode-button-foreground); outline: 1px solid var(--vscode-focusBorder); z-index: 1; }
  </style>
</head>
<body>
  <a class="skip-link" href="#levibe-wizard-main">Skip to first-run wizard content</a>
  <main id="levibe-wizard-main" tabindex="-1">
  <h2 id="wizTitle">${escapeHtml(cur.title)}</h2>
  <p class="muted">${escapeHtml(progress)}</p>
  <div class="card">
    <p>${escapeHtml(cur.body)}</p>
  </div>
  <div>
    ${nextBtn}
    <button type="button" id="wizSkip" title="Skip onboarding" aria-label="Skip onboarding">Skip onboarding</button>
  </div>
  <p class="muted">Skipping still opens the full Lé Vibe surface with explicit readiness states and actions.</p>
  </main>
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
    .map(
      (action) =>
        `<button type="button" data-action="${escapeHtml(action.id)}" title="${escapeHtml(action.label)}" aria-label="${escapeHtml(action.label)}">${escapeHtml(action.label)}</button>`,
    )
    .join('');
  const actionsBlock = actionButtons || '<p class="muted">No actions required.</p>';
  const diagnosticsText = diagnostics ? `<pre class="diag">${escapeHtml(JSON.stringify(diagnostics, null, 2))}</pre>` : '';
  const states = STARTUP_STATES.map((value) => {
    const active = value === state ? 'class="active"' : '';
    return `<li ${active}>${escapeHtml(value)}</li>`;
  }).join('');
  return `<!DOCTYPE html>
<html lang="en">
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
    .skip-link { position: absolute; left: -10000px; top: auto; width: 1px; height: 1px; overflow: hidden; }
    .skip-link:focus { position: static; width: auto; height: auto; left: auto; padding: 0.35rem 0.55rem; margin-bottom: 0.5rem; background: var(--vscode-button-background); color: var(--vscode-button-foreground); outline: 1px solid var(--vscode-focusBorder); z-index: 1; }
    @media (prefers-reduced-motion: reduce) {
      * { scroll-behavior: auto !important; }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#levibe-chat-main">Skip to Lé Vibe Chat panel content</a>
  <main id="levibe-chat-main" tabindex="-1">
  <h2 id="panelStartupHeading">Lé Vibe Native Startup</h2>
  <p class="muted">Deterministic readiness state with local-first remediation actions.</p>
  <nav aria-label="Startup readiness states">
  <ul class="pill-list">${states}</ul>
  </nav>
  <div class="state"><strong>${escapeHtml(state)}</strong></div>
  <p>${escapeHtml(content.detail)}</p>
  <div>${actionsBlock}</div>
  <h3>Local prompt test</h3>
  <p class="muted">Send a prompt to local Ollama and receive streaming tokens.</p>
  <p class="muted" style="margin-bottom:0.25rem;">Quick actions (task-n12-2) — insert a template below. No network until you click <strong>Send Prompt</strong> (local Ollama only).</p>
  <div>
    <button type="button" data-action="quickActionExplain" title="Insert explain template" aria-label="Insert explain template">Explain…</button>
    <button type="button" data-action="quickActionRefactorSelection" title="Insert refactor selection template" aria-label="Insert refactor selection template">Refactor selection…</button>
    <button type="button" data-action="quickActionGenerateTests" title="Insert generate tests template" aria-label="Insert generate tests template">Generate tests…</button>
  </div>
  <label for="promptInput" class="muted" style="display:block;margin-top:0.35rem;">Prompt for local Ollama</label>
  <textarea id="promptInput" placeholder="Ask local model something..." aria-label="Prompt for local Ollama (Lé Vibe Chat sends to configured local endpoint only)"></textarea>
  <div>
    <button type="button" id="sendPrompt" title="Send prompt" aria-label="Send prompt">Send Prompt</button>
    <button type="button" id="cancelPrompt" title="Cancel in-flight request" aria-label="Cancel in-flight request">Cancel Request</button>
    <button type="button" id="retryLastPrompt" title="Retry last prompt" aria-label="Retry last prompt">Retry last prompt</button>
    <button type="button" id="startNewChatSession" title="Start new chat session" aria-label="Start new chat session">New chat</button>
    <button type="button" id="restoreRecentPrompt" title="Restore recent prompt" aria-label="Restore recent prompt">Restore recent…</button>
  </div>
  <div id="chatStatus" class="muted" role="status" aria-live="polite">Idle.</div>
  <div id="chatLog" class="chat-log" role="log" aria-live="polite" aria-relevant="additions text"></div>
  <h3>Edit preview (workspace)</h3>
  <p class="muted">Unified diff before writing. When <code>leVibeNative.requireEditPreviewBeforeApply</code> is on (default), click <strong>Accept preview</strong> then <strong>Apply to file</strong> — no silent whole-file overwrite.</p>
  <div>
    <button type="button" data-action="previewSampleWorkspaceEdit" title="Preview sample workspace edit" aria-label="Preview sample workspace edit">Preview sample workspace edit</button>
  </div>
  <label for="editProposalInput" class="muted" style="display:block;margin-top:0.5rem;">Validate edit proposal JSON (no writes on invalid)</label>
  <textarea id="editProposalInput" placeholder='{"kind":"levibe.edit_proposal.v1","proposals":[...]}' aria-label="Edit proposal JSON"></textarea>
  <div>
    <button type="button" data-action="validateEditProposalJson" title="Validate edit proposal JSON" aria-label="Validate edit proposal JSON">Validate proposal JSON</button>
  </div>
  <div id="editPreviewSection" style="display:none;margin-top:0.5rem;" aria-label="Edit preview diff">
    <pre id="editPreviewPre" class="diag" role="region" aria-label="Unified diff preview"></pre>
    <div>
      <button type="button" id="editPreviewAccept" title="Accept preview" aria-label="Accept preview">Accept preview</button>
      <button type="button" id="editPreviewReject" title="Reject preview" aria-label="Reject preview">Reject</button>
      <button type="button" id="editPreviewApply" disabled title="Apply preview to workspace file" aria-label="Apply preview to workspace file">Apply to file</button>
    </div>
  </div>
  <h3>Workspace plan (demo)</h3>
  <p class="muted">Epic N10 — per-step status in the chat line below; structured lines append to <code>workspace-plan-audit.jsonl</code> under ~/.config/le-vibe/levibe-native-chat/</p>
  <div>
    <button type="button" data-action="dryRunSampleWorkspacePlan" title="Dry-run sample plan" aria-label="Dry-run sample plan">Dry-run sample plan</button>
    <button type="button" data-action="runSampleWorkspacePlan" title="Run sample workspace plan" aria-label="Run sample workspace plan">Run sample workspace plan</button>
    <button type="button" id="cancelWorkspacePlanRun" disabled title="Cancel plan run" aria-label="Cancel plan run">Cancel plan run</button>
    <button type="button" id="undoWorkspacePlanRollback" disabled title="Undo completed plan steps" aria-label="Undo completed plan steps">Undo completed steps</button>
  </div>
  <h3>Workspace context</h3>
  <p class="muted">Token-budget rules: max ${escapeHtml(budget.maxFiles)} files; each excerpt up to ${escapeHtml(budget.maxCharsPerFile)} chars and ${escapeHtml(budget.maxLinesPerFile)} lines; total injected context capped at ${escapeHtml(budget.maxTotalChars)} chars. Paths matching <code>.gitignore</code>, binary files, and files larger than the per-file char budget are skipped with an explicit Lé Vibe Chat message.</p>
  <div>
    <button type="button" data-action="pickContextFile" title="Add workspace context file" aria-label="Add workspace context file">Add context file</button>
    <button type="button" data-action="addContextAtFile" title="Add workspace file to context (@file)" aria-label="Add workspace file to context (@file)">@file…</button>
    <button type="button" data-action="addContextAtFolder" title="Add folder listing to context (@folder)" aria-label="Add folder listing to context (@folder)">@folder…</button>
    <button type="button" data-action="addCurrentFileOutline" title="Add current file outline to context" aria-label="Add current file outline to context">Outline (file)…</button>
    <button type="button" data-action="clearContextFiles" title="Clear selected workspace context" aria-label="Clear selected workspace context">Clear context</button>
  </div>
  <h3>Workspace scaffold (N11)</h3>
  <p class="muted">Create paths under the open folder only — no <code>..</code>; segments <code>.git</code>, <code>.ssh</code>, <code>.gnupg</code>, <code>node_modules</code>, <code>.env</code> are blocked. Move/rename uses VS Code rename (no overwrite if destination exists). Delete asks for a path, then a modal confirmation — never silent; each attempt is logged.</p>
  <div>
    <button type="button" data-action="createWorkspaceFilePrompt" title="Create workspace file" aria-label="Create workspace file">Create file…</button>
    <button type="button" data-action="createWorkspaceFolderPrompt" title="Create workspace folder" aria-label="Create workspace folder">Create folder…</button>
    <button type="button" data-action="moveWorkspacePathPrompt" title="Move or rename workspace path" aria-label="Move or rename workspace path">Move / rename…</button>
    <button type="button" data-action="deleteWorkspacePathPrompt" title="Delete workspace file or folder" aria-label="Delete workspace file or folder">Delete file or folder…</button>
  </div>
  <h3>Terminal execution (N13)</h3>
  <p class="muted">Runs in a <strong>visible</strong> integrated terminal named <code>Lé Vibe Chat</code> — not a hidden PTY. Enable <code>leVibeNative.terminalExecutionEnabled</code> and allow-list patterns first. You confirm each batch unless you choose session-skip in the modal or set <code>leVibeNative.terminalSkipBatchConfirmation</code> (advanced).</p>
  <div>
    <button type="button" data-action="runCommandInIntegratedTerminalPrompt" title="Run command in integrated terminal" aria-label="Run command in integrated terminal">Run command in terminal…</button>
  </div>
  <h3>Operator handoff</h3>
  <p class="muted">Emit a reproducible handoff event to lvibe orchestration and append local audit evidence.</p>
  <div>
    <button type="button" data-action="emitOperatorHandoff" title="Emit operator handoff event" aria-label="Emit operator handoff event">Emit handoff event</button>
  </div>
  <h3>Third-party agent migration</h3>
  <p class="muted">Moving from Continue, Cline, or similar? Open the checklist to avoid duplicate agent surfaces (no automatic uninstall).</p>
  <div>
    <button type="button" data-action="openThirdPartyMigrationGuide" title="Open third-party migration guide" aria-label="Open third-party migration guide">Open migration guide</button>
  </div>
  <h3>Lé Vibe Chat storage</h3>
  <p class="muted">Local JSONL under ~/.config/le-vibe/levibe-native-chat/</p>
  <div>
    <button type="button" data-action="viewChatUsage" title="View transcript usage" aria-label="View transcript usage">View usage</button>
    <button type="button" data-action="exportChatTranscript" title="Export transcript" aria-label="Export transcript">Export transcript</button>
    <button type="button" data-action="clearChatTranscript" title="Clear transcript" aria-label="Clear transcript">Clear transcript</button>
  </div>
  ${diagnosticsText}
  </main>
  <script>
    const vscode = acquireVsCodeApi();
    document.querySelectorAll('button[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        const actionId = button.getAttribute('data-action');
        if (actionId === 'validateEditProposalJson') {
          return;
        }
        vscode.postMessage({ type: 'action', actionId });
      });
    });
    const validateBtn = document.querySelector('button[data-action="validateEditProposalJson"]');
    if (validateBtn) {
      validateBtn.addEventListener('click', () => {
        const input = document.getElementById('editProposalInput');
        vscode.postMessage({
          type: 'action',
          actionId: 'validateEditProposalJson',
          input: input ? input.value : '',
        });
      });
    }
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
    document.getElementById('startNewChatSession').addEventListener('click', () => {
      vscode.postMessage({ type: 'chat', actionId: 'startNewChatSession' });
    });
    document.getElementById('restoreRecentPrompt').addEventListener('click', () => {
      vscode.postMessage({ type: 'chat', actionId: 'restoreRecentPrompt' });
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
      if (msg && msg.type === 'planRunUpdate') {
        document.getElementById('cancelWorkspacePlanRun').disabled = !msg.cancelEnabled;
        return;
      }
      if (msg && msg.type === 'planRollbackUpdate') {
        document.getElementById('undoWorkspacePlanRollback').disabled = !msg.undoEnabled;
        return;
      }
      if (msg && msg.type === 'prefillPrompt' && typeof msg.text === 'string') {
        const el = document.getElementById('promptInput');
        if (el) {
          el.value = msg.text;
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
    document.getElementById('cancelWorkspacePlanRun').addEventListener('click', () => {
      vscode.postMessage({ type: 'action', actionId: 'cancelWorkspacePlanRun' });
    });
    document.getElementById('undoWorkspacePlanRollback').addEventListener('click', () => {
      vscode.postMessage({ type: 'action', actionId: 'undoWorkspacePlanRollback' });
    });
  </script>
</body>
</html>`;
}

/**
 * Queue editor selection + file path for the next Lé Vibe Chat panel, then open the agent surface (task-n12-1).
 */
async function runAskChatAboutSelection() {
  const vscode = require('vscode');
  if (!isFirstPartyAgentSurfaceEnabled(vscode)) {
    void vscode.window
      .showInformationMessage(
        'Lé Vibe first-party agent surface is disabled (rollback). Set leVibeNative.enableFirstPartyAgentSurface to true in Settings.',
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
    return;
  }
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.selection.isEmpty) {
    await vscode.window.showInformationMessage('Lé Vibe Chat: select text in an editor first.');
    return;
  }
  const doc = editor.document;
  if (doc.uri.scheme !== 'file') {
    await vscode.window.showInformationMessage('Lé Vibe Chat: only on-disk files are supported for selection context.');
    return;
  }
  if (!vscode.workspace.getWorkspaceFolder(doc.uri)) {
    await vscode.window.showWarningMessage('Lé Vibe Chat: file must be inside an open workspace folder.');
    return;
  }
  const rel = vscode.workspace.asRelativePath(doc.uri, false);
  if (!rel || rel.includes('..')) {
    await vscode.window.showWarningMessage('Lé Vibe Chat: could not resolve a safe workspace-relative path.');
    return;
  }
  const sel = editor.selection;
  const text = doc.getText(sel);
  const budget = getContextBudget(vscode);
  pendingSelectionContext = buildSelectionContextEntry(
    rel,
    text,
    {
      startLine: sel.start.line,
      startCharacter: sel.start.character,
      endLine: sel.end.line,
      endCharacter: sel.end.character,
    },
    budget,
  );
  await vscode.commands.executeCommand(OPEN_AGENT_SURFACE_COMMAND);
}

/**
 * @param {typeof import('vscode')} vscode
 * @param {import('vscode').ExtensionContext} context
 */
function registerSelectionChatCodeLens(vscode, context) {
  const emitter = new vscode.EventEmitter();
  context.subscriptions.push(
    vscode.window.onDidChangeTextEditorSelection(() => emitter.fire(undefined)),
    vscode.window.onDidChangeActiveTextEditor(() => emitter.fire(undefined)),
    vscode.languages.registerCodeLensProvider(
      { scheme: 'file' },
      {
        onDidChangeCodeLenses: emitter.event,
        provideCodeLenses(document) {
          if (!vscode.workspace.workspaceFolders?.length) {
            return [];
          }
          const ed = vscode.window.activeTextEditor;
          if (!ed || ed.document !== document || ed.selection.isEmpty) {
            return [];
          }
          const range = new vscode.Range(ed.selection.start, ed.selection.end);
          return [
            new vscode.CodeLens(range, {
              title: 'Ask Lé Vibe Chat about this selection',
              tooltip: 'Opens Lé Vibe Chat with this file path and selection in prompt context.',
              command: ASK_CHAT_ABOUT_SELECTION_COMMAND,
            }),
          ];
        },
      },
    ),
  );
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

  function collectRecentUserPrompts(limit = 12) {
    const rows = loadTranscript(transcriptFile)
      .filter((line) => line && line.role === 'user' && typeof line.content === 'string')
      .map((line) => String(line.content).trim())
      .filter((line) => line.length > 0);
    const out = [];
    const seen = new Set();
    for (let i = rows.length - 1; i >= 0 && out.length < limit; i -= 1) {
      const prompt = rows[i];
      if (seen.has(prompt)) {
        continue;
      }
      seen.add(prompt);
      out.push(prompt);
    }
    return out;
  }
  let editPreviewSession = null;
  /** @type {null | { cancelled: boolean; cancel: () => void }} */
  let planRunCanceller = null;
  /** Pending inverse ops after a failed plan run (same session); cleared after rollback or new run. */
  let pendingWorkspacePlanRollbackInverses = null;
  let wizardState = loadWizardState();
  const showFirstRunWizard = config.get('showFirstRunWizard', true);
  const useWizard = showFirstRunWizard && !wizardState.complete;

  const panel = vscode.window.createWebviewPanel(
    'leVibeNativeReadiness',
    'Lé Vibe Native Readiness',
    vscode.ViewColumn.Active,
    { enableScripts: true, retainContextWhenHidden: true },
  );

  function flushPendingSelectionContext() {
    if (!pendingSelectionContext) {
      return;
    }
    const payload = pendingSelectionContext;
    pendingSelectionContext = null;
    selectedContexts.length = 0;
    selectedContexts.push({
      path: payload.path,
      content: payload.content,
    });
    const r = payload.selectionRange;
    const rangeNote =
      r.startLine === r.endLine
        ? `L${r.startLine + 1}:c${r.startCharacter}-${r.endCharacter}`
        : `L${r.startLine + 1}-L${r.endLine + 1}`;
    panel.webview.postMessage({
      type: 'chatUpdate',
      status: `Lé Vibe Chat: added editor selection from "${payload.path}" (${rangeNote}). Add a question and Send Prompt.`,
    });
    panel.webview.postMessage({
      type: 'prefillPrompt',
      text: prefillPromptForSelection(payload.path, r),
    });
  }

  function postContextPick(picked, labelPrefix) {
    if (!picked) {
      return;
    }
    if (picked.skipMessage) {
      panel.webview.postMessage({ type: 'chatUpdate', status: picked.skipMessage });
      return;
    }
    if (selectedContexts.length >= contextBudget.maxFiles) {
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: `Context cap reached (${contextBudget.maxFiles}). Clear context or raise contextMaxFiles.`,
      });
      return;
    }
    const same = selectedContexts.find(
      (entry) => entry.path === picked.path && (entry.kind || 'file') === (picked.kind || 'file'),
    );
    if (same) {
      panel.webview.postMessage({ type: 'chatUpdate', status: `Context already selected: ${picked.path}` });
      return;
    }
    selectedContexts.push({
      path: picked.path,
      content: picked.content,
      ...(picked.kind ? { kind: picked.kind } : {}),
    });
    const tag =
      picked.kind === 'folder' ? 'folder' : picked.kind === 'outline' ? 'outline' : 'file';
    panel.webview.postMessage({
      type: 'chatUpdate',
      status: `${labelPrefix} (${selectedContexts.length}/${contextBudget.maxFiles}): ${picked.path} [${tag}]`,
    });
  }

  function beginMainReadiness() {
    panel.webview.html = panelHtml('checking', null, { mode: 'startup_probe' }, contextBudget);
    queueMicrotask(() => flushPendingSelectionContext());
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
      queueMicrotask(() => flushPendingSelectionContext());
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
            if (!editPreviewSession.proposal) {
              await vscode.window.showErrorMessage('Lé Vibe Chat: internal error — missing proposal on apply.');
              return;
            }
            if (editPreviewSession.previewRevision) {
              const conflict = await checkDiskContentMatchesRevision(
                vscode,
                editPreviewSession.targetUri,
                editPreviewSession.previewRevision,
              );
              if (!conflict.ok) {
                await vscode.window.showWarningMessage(conflict.panelMessage);
                panel.webview.postMessage({ type: 'chatUpdate', status: conflict.panelMessage });
                editPreviewSession = null;
                panel.webview.postMessage({ type: 'editPreviewUpdate', clear: true });
                return;
              }
            }
            await applyEditProposalBatchAsWorkspaceEdit(vscode, editPreviewSession.proposal);
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
          proposal: validated.value,
          targetUri,
          newText: after,
          previewShown: true,
          userAccepted: false,
          previewRevision: buildPreviewRevision(before),
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
    if (msg.type === 'action' && msg.actionId === 'validateEditProposalJson') {
      const raw = typeof msg.input === 'string' ? msg.input.trim() : '';
      if (!raw) {
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Lé Vibe Chat: provide edit proposal JSON first.',
        });
        return;
      }
      let parsed;
      try {
        parsed = JSON.parse(raw);
      } catch (e) {
        const detail = e && e.message ? e.message : String(e);
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: `Lé Vibe Chat: edit proposal parse error — ${detail}`,
        });
        return;
      }
      const validated = validateEditProposal(parsed);
      if (!validated.ok) {
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: formatEditProposalValidationForUser(validated.errors),
        });
        return;
      }
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: `Lé Vibe Chat: edit proposal valid (${validated.value.proposals.length} change(s)) — preview/apply flow required before writes.`,
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'dryRunSampleWorkspacePlan') {
      void (async () => {
        const folder = vscode.workspace.workspaceFolders?.[0];
        if (!folder) {
          await vscode.window.showWarningMessage('Open a folder workspace first to dry-run a workspace plan.');
          return;
        }
        const plan = buildSampleDemoWorkspacePlan(vscode, folder);
        const validated = validateWorkspacePlan(plan);
        if (!validated.ok) {
          panel.webview.postMessage({ type: 'chatUpdate', status: validated.userMessage });
          return;
        }
        const dry = await dryRunValidatedWorkspacePlan(vscode, validated.value, {
          workspaceFolder: folder,
        });
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Dry-run complete — no files changed. Use Run sample workspace plan to apply.',
          replaceLog: `${dry.lines.join('\n')}\n`,
        });
      })();
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'runSampleWorkspacePlan') {
      void (async () => {
        const folder = vscode.workspace.workspaceFolders?.[0];
        if (!folder) {
          await vscode.window.showWarningMessage('Open a folder workspace first to run a workspace plan.');
          return;
        }
        if (planRunCanceller !== null) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: 'A plan run is already in progress — use Cancel plan run or wait for completion.',
          });
          return;
        }
        const lvibeDir = vscode.Uri.joinPath(folder.uri, '.lvibe');
        try {
          await vscode.workspace.fs.stat(lvibeDir);
        } catch {
          await vscode.workspace.fs.createDirectory(lvibeDir);
        }
        const plan = buildSampleDemoWorkspacePlan(vscode, folder);
        const validated = validateWorkspacePlan(plan);
        if (!validated.ok) {
          panel.webview.postMessage({ type: 'chatUpdate', status: validated.userMessage });
          return;
        }
        const canceller = { cancelled: false, cancel() { this.cancelled = true; } };
        planRunCanceller = canceller;
        pendingWorkspacePlanRollbackInverses = null;
        panel.webview.postMessage({ type: 'planRollbackUpdate', undoEnabled: false });
        panel.webview.postMessage({ type: 'planRunUpdate', cancelEnabled: true });
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Running sample workspace plan (3 steps)…',
          replaceLog: '',
        });
        const result = await executeValidatedWorkspacePlan(vscode, validated.value, {
          workspaceFolder: folder,
          workspaceUriStr: folder.uri.toString(),
          shouldCancel: () => canceller.cancelled,
          onProgress: (line) => {
            panel.webview.postMessage({ type: 'chatUpdate', append: `${line}\n` });
          },
        });
        planRunCanceller = null;
        panel.webview.postMessage({ type: 'planRunUpdate', cancelEnabled: false });
        if (!result.ok) {
          pendingWorkspacePlanRollbackInverses = result.rollbackInverses || null;
          panel.webview.postMessage({
            type: 'planRollbackUpdate',
            undoEnabled: Boolean(pendingWorkspacePlanRollbackInverses?.length),
          });
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: `Plan failed: ${result.error}`,
          });
          return;
        }
        if (result.cancelled) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: `Plan cancelled after ${result.completedSteps} completed step(s). Remaining steps were not run.`,
          });
          return;
        }
        panel.webview.postMessage({
          type: 'chatUpdate',
          status:
            'Sample workspace plan finished — see chat log above. Audit lines: ~/.config/le-vibe/levibe-native-chat/workspace-plan-audit.jsonl',
        });
      })();
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'cancelWorkspacePlanRun') {
      if (planRunCanceller && !planRunCanceller.cancelled) {
        planRunCanceller.cancel();
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Cancellation requested — current step finishes, then remaining steps are skipped.',
        });
      }
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'undoWorkspacePlanRollback') {
      void (async () => {
        const inv = pendingWorkspacePlanRollbackInverses;
        if (!inv || inv.length === 0) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: 'No workspace plan rollback is pending.',
          });
          return;
        }
        const folder = vscode.workspace.workspaceFolders?.[0];
        const r = await applyWorkspacePlanRollbackInverses(vscode, inv, {
          workspaceUriStr: folder ? folder.uri.toString() : 'no-workspace',
        });
        pendingWorkspacePlanRollbackInverses = null;
        panel.webview.postMessage({ type: 'planRollbackUpdate', undoEnabled: false });
        if (!r.ok) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: `Rollback failed after ${r.applied} inverse step(s): ${r.error}`,
          });
          return;
        }
        panel.webview.postMessage({
          type: 'chatUpdate',
          status:
            'Rollback finished — prior completed plan steps were reverted best-effort (same session). See workspace-plan-audit.jsonl for rollback event.',
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
        postContextPick(picked ? { ...picked, kind: 'file' } : null, 'Context selected');
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'addContextAtFile') {
      void pickAtFileContext(vscode, () => getContextBudget(vscode)).then((picked) => {
        postContextPick(picked, '@file context');
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'addContextAtFolder') {
      void pickAtFolderContext(vscode, () => getContextBudget(vscode)).then((picked) => {
        postContextPick(picked, '@folder context');
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'addCurrentFileOutline') {
      void (async () => {
        const r = await fetchCurrentFileOutlineForContext(vscode, () => getContextBudget(vscode));
        if (!r.ok) {
          await vscode.window.showWarningMessage(r.userMessage);
          panel.webview.postMessage({ type: 'chatUpdate', status: r.userMessage });
          return;
        }
        postContextPick(r, 'Outline context');
      })();
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'clearContextFiles') {
      selectedContexts.length = 0;
      panel.webview.postMessage({ type: 'chatUpdate', status: 'Workspace context cleared.' });
      return;
    }
    if (msg.type === 'action' && PANEL_QUICK_ACTION_MAP[msg.actionId]) {
      const qid = PANEL_QUICK_ACTION_MAP[msg.actionId];
      const template = getQuickActionTemplate(qid);
      panel.webview.postMessage({ type: 'prefillPrompt', text: template });
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: `Lé Vibe Chat: "${qid}" template loaded — edit the prompt, then Send Prompt (local Ollama only).`,
      });
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'createWorkspaceFilePrompt') {
      void runCreateWorkspaceFileInteractive(vscode, panel);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'createWorkspaceFolderPrompt') {
      void runCreateWorkspaceFolderInteractive(vscode, panel);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'moveWorkspacePathPrompt') {
      void runMoveWorkspacePathInteractive(vscode, panel);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'deleteWorkspacePathPrompt') {
      void runDeleteWorkspacePathInteractive(vscode, panel);
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
    if (msg.type === 'action' && msg.actionId === 'runCommandInIntegratedTerminalPrompt') {
      void (async () => {
        const line = await vscode.window.showInputBox({
          title: 'Run in integrated terminal (Lé Vibe Chat)',
          prompt:
            'One-line shell command. Allow/deny policy applies; confirm each batch unless session-skip or terminalSkipBatchConfirmation.',
          validateInput: (value) => {
            if (!String(value || '').trim()) {
              return 'Enter a non-empty command.';
            }
            return undefined;
          },
        });
        if (!line) {
          return;
        }
        await runCommandInVisibleTerminal(vscode, line, { panel });
      })();
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
    if (msg.type === 'chat' && msg.actionId === 'startNewChatSession') {
      lastPromptPlain = null;
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: 'Started a new chat session in this panel. Transcript history is preserved (bounded JSONL).',
        replaceLog: '',
      });
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'restoreRecentPrompt') {
      void (async () => {
        const recent = collectRecentUserPrompts();
        if (!recent.length) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: 'No recent prompts found for this workspace yet.',
          });
          return;
        }
        const choice = await vscode.window.showQuickPick(
          recent.map((text, idx) => ({
            label: `${idx + 1}. ${text.slice(0, 90)}${text.length > 90 ? '…' : ''}`,
            detail: text,
          })),
          {
            title: 'Restore recent prompt (Lé Vibe Chat)',
            placeHolder: 'Pick a previous user prompt to prefill',
          },
        );
        if (!choice || !choice.detail) {
          return;
        }
        lastPromptPlain = choice.detail;
        panel.webview.postMessage({ type: 'prefillPrompt', text: choice.detail });
        panel.webview.postMessage({
          type: 'chatUpdate',
          status: 'Recent prompt restored to input. Edit if needed, then Send Prompt.',
        });
      })();
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
  registerSelectionChatCodeLens(vscode, context);
  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
      clearTerminalSessionAllow();
    }),
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
      const ig = await loadGitignoreMatcher(vscode, folder);
      const files = await vscode.workspace.findFiles('**/*', '**/{node_modules,.git,.lvibe}/**', FILE_PICKER_MAX_SCAN_URIS);
      if (!files.length) {
        await vscode.window.showInformationMessage('No workspace files available for context selection.');
        return null;
      }
      const items = files
        .map((uri) => ({
          label: vscode.workspace.asRelativePath(uri, false),
          uri,
        }))
        .filter((item) => !ig.ignores(relativePosixForGitignore(item.label)));
      if (!items.length) {
        await vscode.window.showInformationMessage(
          'Lé Vibe Chat: no files available for context — empty tree or every candidate matches .gitignore.',
        );
        return null;
      }
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
      const prep = await loadContextFileWithGuards(
        vscode,
        folder,
        choice.uri,
        choice.label,
        { maxCharsPerFile: ctx.maxCharsPerFile, maxLinesPerFile: ctx.maxLinesPerFile },
        ig,
      );
      if (!prep.ok) {
        await vscode.window.showWarningMessage(prep.userMessage);
        return null;
      }
      return { path: choice.label, content: prep.excerpt, kind: 'file' };
    }),
    vscode.commands.registerCommand(ADD_CONTEXT_AT_FILE_COMMAND, () =>
      pickAtFileContext(vscode, () => getContextBudget(vscode)),
    ),
    vscode.commands.registerCommand(ADD_CONTEXT_AT_FOLDER_COMMAND, () =>
      pickAtFolderContext(vscode, () => getContextBudget(vscode)),
    ),
    vscode.commands.registerCommand(ADD_CURRENT_FILE_OUTLINE_COMMAND, () =>
      fetchCurrentFileOutlineForContext(vscode, () => getContextBudget(vscode)),
    ),
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
    vscode.commands.registerCommand(APPLY_SELECTION_DEMO_REPLACE_COMMAND, async () => {
      const editor = vscode.window.activeTextEditor;
      const resolved = resolveSingleSelectionForPartialApply(editor);
      if (!resolved.ok) {
        await vscode.window.showWarningMessage(resolved.message);
        return;
      }
      const we = new vscode.WorkspaceEdit();
      const demo = '/* Lé Vibe Chat — selection demo (partial apply) */\n';
      we.replace(editor.document.uri, /** @type {import('vscode').Range} */ (resolved.range), demo);
      const applied = await vscode.workspace.applyEdit(we);
      if (applied) {
        await vscode.window.showInformationMessage('Lé Vibe Chat: selection range replaced (Undo to revert).');
      }
    }),
    vscode.commands.registerCommand(CREATE_WORKSPACE_FILE_COMMAND, () => runCreateWorkspaceFileInteractive(vscode, null)),
    vscode.commands.registerCommand(CREATE_WORKSPACE_FOLDER_COMMAND, () => runCreateWorkspaceFolderInteractive(vscode, null)),
    vscode.commands.registerCommand(MOVE_WORKSPACE_PATH_COMMAND, () => runMoveWorkspacePathInteractive(vscode, null)),
    vscode.commands.registerCommand(DELETE_WORKSPACE_PATH_COMMAND, () => runDeleteWorkspacePathInteractive(vscode, null)),
    vscode.commands.registerCommand(OPEN_THIRD_PARTY_MIGRATION_COMMAND, () => runThirdPartyMigrationGuide(vscode)),
    vscode.commands.registerCommand(ASK_CHAT_ABOUT_SELECTION_COMMAND, runAskChatAboutSelection),
    vscode.commands.registerCommand(RUN_COMMAND_IN_INTEGRATED_TERMINAL_COMMAND, async () => {
      const line = await vscode.window.showInputBox({
        title: 'Run in integrated terminal (Lé Vibe Chat)',
        prompt:
          'One-line shell command. Allow/deny policy applies; confirm each batch unless session-skip or terminalSkipBatchConfirmation.',
        validateInput: (value) => {
          if (!String(value || '').trim()) {
            return 'Enter a non-empty command.';
          }
          return undefined;
        },
      });
      if (!line) {
        return;
      }
      await runCommandInVisibleTerminal(vscode, line, {});
    }),
    vscode.commands.registerCommand(CLEAR_TERMINAL_SESSION_ALLOW_COMMAND, async () => {
      clearTerminalSessionAllow();
      await vscode.window.showInformationMessage(
        'Lé Vibe Chat: cleared “skip further prompts” for this extension host session (terminal commands).',
      );
    }),
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
    vscode.commands.registerCommand(START_NEW_CHAT_SESSION_COMMAND, async () => {
      await vscode.commands.executeCommand(OPEN_AGENT_SURFACE_COMMAND);
      await vscode.window.showInformationMessage(
        'Use the panel action "New chat" to reset in-panel conversation while preserving bounded transcript history.',
      );
    }),
    vscode.commands.registerCommand(RESTORE_RECENT_PROMPT_COMMAND, async () => {
      await vscode.commands.executeCommand(OPEN_AGENT_SURFACE_COMMAND);
      await vscode.window.showInformationMessage(
        'Use the panel action "Restore recent…" to pick and prefill a previous prompt from workspace transcript history.',
      );
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

  registerLeVibeChatStatusBar(vscode, context, {
    openAgentSurfaceCommand: OPEN_AGENT_SURFACE_COMMAND,
  });
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
  OPEN_AGENT_SURFACE_COMMAND,
  OPEN_OLLAMA_SETUP_HELP_COMMAND,
  OPEN_MODEL_PULL_HELP_COMMAND,
  OPEN_WORKSPACE_SETUP_COMMAND,
  START_NEW_CHAT_SESSION_COMMAND,
  RESTORE_RECENT_PROMPT_COMMAND,
  VIEW_CHAT_USAGE_COMMAND,
  EXPORT_CHAT_TRANSCRIPT_COMMAND,
  CLEAR_CHAT_TRANSCRIPT_COMMAND,
  PICK_CONTEXT_FILE_COMMAND,
  CLEAR_CONTEXT_FILES_COMMAND,
  EMIT_OPERATOR_HANDOFF_COMMAND,
  OPEN_THIRD_PARTY_MIGRATION_COMMAND,
  APPLY_SELECTION_DEMO_REPLACE_COMMAND,
  CREATE_WORKSPACE_FILE_COMMAND,
  CREATE_WORKSPACE_FOLDER_COMMAND,
  MOVE_WORKSPACE_PATH_COMMAND,
  DELETE_WORKSPACE_PATH_COMMAND,
  ASK_CHAT_ABOUT_SELECTION_COMMAND,
  RUN_COMMAND_IN_INTEGRATED_TERMINAL_COMMAND,
  CLEAR_TERMINAL_SESSION_ALLOW_COMMAND,
  ADD_CONTEXT_AT_FILE_COMMAND,
  ADD_CONTEXT_AT_FOLDER_COMMAND,
  ADD_CURRENT_FILE_OUTLINE_COMMAND,
  getTranscriptContext,
  getContextBudget,
  panelHtml,
  firstRunWizardHtml,
  isFirstPartyAgentSurfaceEnabled,
};
