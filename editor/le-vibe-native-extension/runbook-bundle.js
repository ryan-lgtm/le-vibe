'use strict';

const fs = require('node:fs');
const path = require('node:path');

const { levibeNativeChatDir } = require('./storage-inventory');
const { transcriptPath } = require('./chat-transcript');

const RUNBOOK_BUNDLES_DIR = 'runbook-bundles';

/**
 * Default relative path pattern for support runbook output (task-cp5-2).
 * Full path: ~/.config/le-vibe/levibe-native-chat/runbook-bundles/runbook-<ISO-timestamp>/
 */
function defaultRunbookBundleDir(stampIso) {
  return path.join(levibeNativeChatDir(), RUNBOOK_BUNDLES_DIR, `runbook-${stampIso}`);
}

/**
 * @param {string} filePath
 * @param {number} maxLines
 * @returns {string}
 */
function tailTextFileLines(filePath, maxLines) {
  const max = Math.max(1, Number(maxLines) || 1);
  try {
    if (!fs.existsSync(filePath)) {
      return '';
    }
    const raw = fs.readFileSync(filePath, 'utf8');
    const lines = raw.split(/\r?\n/);
    const nonEmpty = lines[lines.length - 1] === '' ? lines.slice(0, -1) : lines;
    if (nonEmpty.length <= max) {
      return nonEmpty.join('\n') + (nonEmpty.length ? '\n' : '');
    }
    return nonEmpty.slice(-max).join('\n') + '\n';
  } catch {
    return '';
  }
}

/**
 * @param {typeof import('vscode')} vscode
 * @returns {Record<string, unknown>}
 */
function collectLeVibeNativeSettingsInspect(vscode) {
  const cfg = vscode.workspace.getConfiguration('leVibeNative');
  if (typeof cfg.inspect !== 'function') {
    return { note: 'inspect unavailable' };
  }
  const out = {};
  const keys = [
    'openPanelOnStartup',
    'showStatusBarEntry',
    'showFirstRunWizard',
    'enableFirstPartyAgentSurface',
    'showThirdPartyMigrationNudge',
    'devStartupState',
    'useLiveOllamaReadiness',
    'ollamaEndpoint',
    'ollamaTimeoutMs',
    'ollamaMaxRetries',
    'ollamaRetryBackoffMs',
    'ollamaStreamStallMs',
    'ollamaStreamMaxMs',
    'ollamaModel',
    'inlineSuggestionsEnabled',
    'inlineSuggestionsDebounceMs',
    'chatTranscriptMaxBytes',
    'chatTranscriptMaxMessages',
    'contextMaxFiles',
    'contextMaxCharsPerFile',
    'contextMaxLinesPerFile',
    'contextMaxTotalChars',
    'requireEditPreviewBeforeApply',
    'openDocumentAfterWorkspaceCreate',
    'terminalExecutionEnabled',
    'terminalCommandAllowPatterns',
    'terminalCommandDenyPatterns',
    'terminalSkipBatchConfirmation',
  ];
  for (const key of keys) {
    const fullKey = `leVibeNative.${key}`;
    try {
      const i = cfg.inspect(key);
      if (i) {
        out[fullKey] = {
          default: i.defaultValue,
          global: i.globalValue,
          workspace: i.workspaceValue,
          workspaceFolder: i.workspaceFolderValue,
        };
      }
    } catch {
      out[fullKey] = { error: 'inspect failed' };
    }
  }
  return out;
}

/**
 * @param {object} opts
 * @param {typeof import('vscode')} opts.vscode
 * @param {string} [opts.workspaceFolderUri]
 * @param {string} [opts.outDir] absolute path; default runbook-bundles/runbook-<iso>
 * @param {string} [opts.levibeDir] override persistence root (tests)
 * @returns {{ outDir: string, files: string[] }}
 */
function writeRunbookBundle(opts) {
  const vscode = opts.vscode;
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const outDir = opts.outDir || defaultRunbookBundleDir(stamp);
  fs.mkdirSync(outDir, { recursive: true });

  const levibeDir = opts.levibeDir || levibeNativeChatDir();
  const workspaceUri = opts.workspaceFolderUri || 'no-workspace';

  const files = [];

  const settingsJson = JSON.stringify(
    {
      collected_at_iso: new Date().toISOString(),
      workspace_uri: workspaceUri,
      leVibeNative: collectLeVibeNativeSettingsInspect(vscode),
    },
    null,
    2,
  );
  const settingsPath = path.join(outDir, 'leVibeNative-settings.json');
  fs.writeFileSync(settingsPath, settingsJson, 'utf8');
  files.push('leVibeNative-settings.json');

  const auditTails = [
    { name: 'orchestrator-events-tail.jsonl', source: path.join(levibeDir, 'orchestrator-events.jsonl'), lines: 250 },
    { name: 'terminal-command-audit-tail.jsonl', source: path.join(levibeDir, 'terminal-command-audit.jsonl'), lines: 200 },
    { name: 'workspace-plan-audit-tail.jsonl', source: path.join(levibeDir, 'workspace-plan-audit.jsonl'), lines: 150 },
    { name: 'workspace-fs-ops-audit-tail.jsonl', source: path.join(levibeDir, 'workspace-fs-ops-audit.jsonl'), lines: 80 },
    { name: 'operator-handoff-audit-tail.jsonl', source: path.join(levibeDir, 'operator-handoff-audit.jsonl'), lines: 40 },
  ];
  for (const { name, source, lines } of auditTails) {
    const content = tailTextFileLines(source, lines);
    fs.writeFileSync(path.join(outDir, name), content || '(file missing or empty)\n', 'utf8');
    files.push(name);
  }

  if (workspaceUri !== 'no-workspace') {
    const tp = transcriptPath(workspaceUri);
    const transcriptTail = tailTextFileLines(tp, 120);
    fs.writeFileSync(
      path.join(outDir, 'transcript-tail.jsonl'),
      transcriptTail || '(transcript missing or empty)\n',
      'utf8',
    );
    files.push('transcript-tail.jsonl');
  }

  const readme = [
    'Lé Vibe Chat — runbook diagnostics bundle (task-cp5-2)',
    '',
    'Local-only: no network upload; files stay under your machine.',
    '',
    `Output directory: ${outDir}`,
    '',
    'Contents:',
    '- leVibeNative-settings.json — effective configuration inspect (defaults + overrides).',
    '- *-tail.jsonl — recent lines from append-only audit logs (orchestrator bridge, terminal, plan, fs ops, handoff).',
    ...(workspaceUri !== 'no-workspace' ? ['- transcript-tail.jsonl — recent chat JSONL for this workspace (bounded).'] : []),
    '',
    'Canonical persistence root:',
    `  ${levibeDir}`,
    '',
    'You can zip this folder and attach it to support tickets.',
  ].join('\n');
  fs.writeFileSync(path.join(outDir, 'README-runbook.txt'), readme, 'utf8');
  files.push('README-runbook.txt');

  return { outDir, files };
}

module.exports = {
  RUNBOOK_BUNDLES_DIR,
  defaultRunbookBundleDir,
  tailTextFileLines,
  collectLeVibeNativeSettingsInspect,
  writeRunbookBundle,
};
