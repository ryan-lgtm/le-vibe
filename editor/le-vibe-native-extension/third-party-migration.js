'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const SCHEMA = 'third_party_migration.v1';
const AUDIT_CONTRACT = 'lvibe.third_party_migration.v1';

/** Known third-party agent surfaces often co-installed with Lé Vibe stacks (Open VSX / marketplace ids). */
const EXTENSION_WATCHLIST = Object.freeze([
  { id: 'Continue.continue', label: 'Continue' },
  { id: 'saoudrizwan.claude-dev', label: 'Cline (saoudrizwan.claude-dev)' },
]);

function configDir() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'levibe-native-chat');
}

function defaultStatePath() {
  return path.join(configDir(), 'third-party-migration-state.json');
}

function migrationAuditPath() {
  return path.join(configDir(), 'third-party-migration-audit.jsonl');
}

function emptyState() {
  return {
    schema: SCHEMA,
    status: 'pending',
    updatedAt: null,
    lastDetectedIds: [],
  };
}

function loadMigrationState(filePath = defaultStatePath()) {
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
      status: ['pending', 'skipped', 'remediated'].includes(raw.status) ? raw.status : 'pending',
      updatedAt: raw.updatedAt || null,
      lastDetectedIds: Array.isArray(raw.lastDetectedIds) ? raw.lastDetectedIds : [],
    };
  } catch {
    return emptyState();
  }
}

function saveMigrationState(state, filePath = defaultStatePath()) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const payload = {
    schema: SCHEMA,
    status: state.status,
    updatedAt: state.updatedAt || new Date().toISOString(),
    lastDetectedIds: state.lastDetectedIds || [],
  };
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  return payload;
}

function appendMigrationAudit(filePath, entry) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const line = `${JSON.stringify({ ts: new Date().toISOString(), contract: AUDIT_CONTRACT, ...entry })}\n`;
  fs.appendFileSync(filePath, line, 'utf8');
}

function matchWatchlist(installedIds) {
  const set = new Set(installedIds);
  return EXTENSION_WATCHLIST.filter((w) => set.has(w.id));
}

function detectInstalledThirdParty(vscode) {
  const extensions = vscode.extensions && vscode.extensions.all ? vscode.extensions.all : [];
  const ids = extensions.map((e) => e && e.id).filter(Boolean);
  return matchWatchlist(ids).map((w) => {
    const ext = extensions.find((e) => e.id === w.id);
    return {
      id: w.id,
      label: w.label,
      isActive: ext ? !!ext.isActive : false,
    };
  });
}

function buildMigrationGuideMarkdown(detected) {
  const lines = [
    '# Lé Vibe — third-party agent migration',
    '',
    'Use this checklist when moving from a **third-party** chat/agent extension (e.g. Continue, Cline) to **Lé Vibe Chat** (first-party, local-first).',
    '',
    '## Guardrails',
    '',
    '- This extension **does not** delete or modify other extensions\' data automatically.',
    '- Migration state and audit entries live only under `~/.config/le-vibe/levibe-native-chat/`.',
    '- Disable or uninstall conflicting extensions from **your** editor if you want a single agent surface.',
    '',
    '## Remediation steps (deterministic)',
    '',
    '1. Open the Extensions view and **disable** or **uninstall** third-party agent extensions you no longer want.',
    '2. Ensure **Settings → Lé Vibe Native Extension → `leVibeNative.enableFirstPartyAgentSurface`** is **true** (default).',
    '3. Run **Lé Vibe Chat: Open Agent Surface** and confirm the readiness panel and local Ollama remediation appear (no empty gray view).',
    '4. Optional: export legacy transcripts from the other tool before uninstall if you still need them.',
    '',
  ];
  if (detected.length) {
    lines.push('## Detected in this editor session');
    lines.push('');
    detected.forEach((d) => {
      lines.push(`- **${d.label}** (\`${d.id}\`)${d.isActive === false ? ' — inactive' : ''}`);
    });
    lines.push('');
  } else {
    lines.push('## Detected in this editor session');
    lines.push('');
    lines.push('None from the built-in watchlist. If you still see duplicate UIs, review Extensions manually.');
    lines.push('');
  }
  return lines.join('\n');
}

/**
 * @param {import('vscode')} vscode
 */
async function runThirdPartyMigrationGuide(vscode, { statePath, auditPath } = {}) {
  const { isFirstPartyAgentSurfaceEnabled } = require('./feature-flags');
  if (!isFirstPartyAgentSurfaceEnabled(vscode)) {
    await vscode.window.showWarningMessage(
      'Enable leVibeNative.enableFirstPartyAgentSurface in Settings before using the migration guide.',
    );
    return null;
  }

  const detected = detectInstalledThirdParty(vscode);
  const md = buildMigrationGuideMarkdown(detected);
  const doc = await vscode.workspace.openTextDocument({
    content: md,
    language: 'markdown',
  });
  await vscode.window.showTextDocument(doc, { preview: true });

  const choice = await vscode.window.showInformationMessage(
    'Lé Vibe Chat: follow the migration checklist in the editor tab. Mark complete when you have disabled conflicting extensions and verified Lé Vibe Chat.',
    'Mark remediated',
    'Open Extensions',
    'Close',
  );

  const ap = auditPath || migrationAuditPath();
  const sp = statePath || defaultStatePath();

  if (choice === 'Mark remediated') {
    const state = saveMigrationState(
      {
        status: 'remediated',
        lastDetectedIds: detected.map((d) => d.id),
        updatedAt: new Date().toISOString(),
      },
      sp,
    );
    appendMigrationAudit(ap, { action: 'remediated', detectedIds: detected.map((d) => d.id) });
    await vscode.window.showInformationMessage(
      `Migration marked remediated. State: ${sp}`,
    );
    return state;
  }
  if (choice === 'Open Extensions') {
    appendMigrationAudit(ap, { action: 'open_extensions', detectedIds: detected.map((d) => d.id) });
    await vscode.commands.executeCommand('workbench.view.extensions');
    return loadMigrationState(sp);
  }
  appendMigrationAudit(ap, { action: 'guide_closed', detectedIds: detected.map((d) => d.id) });
  return loadMigrationState(sp);
}

/**
 * One-time nudge when watchlist extensions are installed and state is still pending.
 * @param {import('vscode')} vscode
 */
async function scheduleThirdPartyMigrationNudge(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (config.get('showThirdPartyMigrationNudge', true) === false) {
    return;
  }
  const { isFirstPartyAgentSurfaceEnabled } = require('./feature-flags');
  if (!isFirstPartyAgentSurfaceEnabled(vscode)) {
    return;
  }

  const statePath = defaultStatePath();
  let state = loadMigrationState(statePath);
  if (state.status === 'remediated' || state.status === 'skipped') {
    return;
  }

  const detected = detectInstalledThirdParty(vscode);
  if (!detected.length) {
    return;
  }

  const choice = await vscode.window.showInformationMessage(
    `Lé Vibe Chat: third-party agent extension(s) detected (${detected.map((d) => d.label).join(', ')}). Open the migration guide for a safe checklist?`,
    'Open guide',
    'Not now',
  );

  if (choice === 'Open guide') {
    await runThirdPartyMigrationGuide(vscode, { statePath, auditPath: migrationAuditPath() });
    return;
  }
  if (choice === 'Not now') {
    saveMigrationState(
      {
        status: 'skipped',
        lastDetectedIds: detected.map((d) => d.id),
        updatedAt: new Date().toISOString(),
      },
      statePath,
    );
    appendMigrationAudit(migrationAuditPath(), {
      action: 'nudge_dismissed',
      detectedIds: detected.map((d) => d.id),
    });
  }
}

module.exports = {
  SCHEMA,
  AUDIT_CONTRACT,
  EXTENSION_WATCHLIST,
  configDir,
  defaultStatePath,
  migrationAuditPath,
  loadMigrationState,
  saveMigrationState,
  appendMigrationAudit,
  matchWatchlist,
  detectInstalledThirdParty,
  buildMigrationGuideMarkdown,
  runThirdPartyMigrationGuide,
  scheduleThirdPartyMigrationNudge,
};
