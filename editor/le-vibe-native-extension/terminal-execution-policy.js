'use strict';

/**
 * Normalize a one-line shell command for policy checks (task-n13-1).
 * @param {string} cmd
 * @returns {string}
 */
function normalizeCommandLine(cmd) {
  return String(cmd || '')
    .trim()
    .replace(/\s+/g, ' ');
}

/**
 * Match pattern against command: substring (case-insensitive), or `*` → `.*` between segments.
 * @param {string} commandLower normalized lowercased command
 * @param {string} pattern
 */
function commandMatchesPattern(commandLower, pattern) {
  const raw = String(pattern).trim();
  if (!raw) {
    return false;
  }
  if (!raw.includes('*')) {
    return commandLower.includes(raw.toLowerCase());
  }
  const esc = (s) => s.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
  const parts = raw.split('*').map((seg) => esc(seg.trim().toLowerCase()));
  try {
    return new RegExp(`^${parts.join('.*')}$`).test(commandLower);
  } catch {
    return false;
  }
}

/**
 * @param {string} commandLine
 * @param {{ enabled: boolean, allowPatterns: string[], denyPatterns: string[] }} policy
 * @returns {{ ok: true } | { ok: false, reason: string }}
 */
function evaluateTerminalCommand(commandLine, policy) {
  if (!policy || !policy.enabled) {
    return {
      ok: false,
      reason:
        'Lé Vibe Chat: terminal execution is disabled — set leVibeNative.terminalExecutionEnabled (prefer Workspace scope) and allow patterns before use.',
    };
  }
  const line = normalizeCommandLine(commandLine);
  const lower = line.toLowerCase();
  if (!line) {
    return { ok: false, reason: 'Lé Vibe Chat: empty command line.' };
  }
  const deny = Array.isArray(policy.denyPatterns) ? policy.denyPatterns : [];
  for (const d of deny) {
    if (commandMatchesPattern(lower, d)) {
      return {
        ok: false,
        reason: `Lé Vibe Chat: command blocked by deny pattern (${String(d).trim()}).`,
      };
    }
  }
  const allow = Array.isArray(policy.allowPatterns) ? policy.allowPatterns.filter(Boolean) : [];
  if (allow.length === 0) {
    return {
      ok: false,
      reason:
        'Lé Vibe Chat: terminal execution is enabled but leVibeNative.terminalCommandAllowPatterns is empty — add at least one allow pattern (allow-list mode).',
    };
  }
  const matched = allow.some((a) => commandMatchesPattern(lower, a));
  if (!matched) {
    return {
      ok: false,
      reason: 'Lé Vibe Chat: command does not match any entry in leVibeNative.terminalCommandAllowPatterns.',
    };
  }
  return { ok: true };
}

/**
 * Read policy from VS Code configuration (task-n13-1).
 * @param {import('vscode')} vscode
 * @returns {{ enabled: boolean, allowPatterns: string[], denyPatterns: string[] }}
 */
function getTerminalExecutionPolicy(vscode) {
  const cfg = vscode.workspace.getConfiguration('leVibeNative');
  return {
    enabled: cfg.get('terminalExecutionEnabled', false),
    allowPatterns: cfg.get('terminalCommandAllowPatterns', []) || [],
    denyPatterns: cfg.get('terminalCommandDenyPatterns', []) || [],
  };
}

module.exports = {
  normalizeCommandLine,
  commandMatchesPattern,
  evaluateTerminalCommand,
  getTerminalExecutionPolicy,
};
