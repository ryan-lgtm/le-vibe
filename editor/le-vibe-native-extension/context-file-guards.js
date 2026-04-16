'use strict';

const ignore = require('ignore');
const { clipTextByBudget } = require('./workspace-context.js');

/** Deterministic machine-readable skip reasons (task-n11-4). */
const CONTEXT_SKIP_REASON = Object.freeze({
  GITIGNORE: 'gitignore',
  FILE_TOO_LARGE: 'file_too_large',
  BINARY: 'binary',
});

const BINARY_PROBE_BYTES = 8192;

/**
 * @param {Buffer} buf
 * @returns {boolean}
 */
function bufferLooksBinary(buf) {
  if (!buf || buf.length === 0) {
    return false;
  }
  const n = Math.min(buf.length, BINARY_PROBE_BYTES);
  for (let i = 0; i < n; i++) {
    if (buf[i] === 0) {
      return true;
    }
  }
  return false;
}

/**
 * @param {string} label
 * @returns {string}
 */
function relativePosixForGitignore(label) {
  return String(label || '')
    .replace(/\\/g, '/')
    .replace(/^\.\//, '');
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 */
async function loadGitignoreMatcher(vscode, workspaceFolder) {
  const ig = ignore();
  try {
    const uri = vscode.Uri.joinPath(workspaceFolder.uri, '.gitignore');
    const bytes = await vscode.workspace.fs.readFile(uri);
    ig.add(Buffer.from(bytes).toString('utf8'));
  } catch {
    /* no or unreadable .gitignore */
  }
  return ig;
}

/**
 * @param {string} reason
 * @param {{ pathLabel: string, maxChars?: number, byteLength?: number }} detail
 * @returns {string}
 */
function formatContextGuardUserMessage(reason, detail) {
  const p = detail.pathLabel || '(unknown)';
  switch (reason) {
    case CONTEXT_SKIP_REASON.GITIGNORE:
      return `Lé Vibe Chat: skipped "${p}" — path matches .gitignore (not used as context).`;
    case CONTEXT_SKIP_REASON.FILE_TOO_LARGE: {
      const cap = detail.maxChars != null ? String(detail.maxChars) : '?';
      const bytes = detail.byteLength != null ? String(detail.byteLength) : '?';
      return `Lé Vibe Chat: skipped "${p}" — file exceeds per-file context budget (${cap} chars max from settings; ${bytes} bytes on disk).`;
    }
    case CONTEXT_SKIP_REASON.BINARY:
      return `Lé Vibe Chat: skipped "${p}" — binary or non-text content (context excerpts are text-only).`;
    default:
      return `Lé Vibe Chat: skipped "${p}" — reason: ${reason}.`;
  }
}

/**
 * Validate and load a text excerpt for prompt context (task-n11-4).
 *
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {import('vscode').Uri} fileUri
 * @param {string} pathLabel workspace-relative label from `asRelativePath`
 * @param {{ maxCharsPerFile: number, maxLinesPerFile: number }} budget
 * @param {*} gitignoreMatcher matcher from `ignore` package
 * @returns {Promise<
 *   | { ok: true, excerpt: string }
 *   | { ok: false, reason: string, userMessage: string }
 * >}
 */
async function loadContextFileWithGuards(vscode, workspaceFolder, fileUri, pathLabel, budget, gitignoreMatcher) {
  const rel = relativePosixForGitignore(pathLabel);
  if (gitignoreMatcher.ignores(rel)) {
    return {
      ok: false,
      reason: CONTEXT_SKIP_REASON.GITIGNORE,
      userMessage: formatContextGuardUserMessage(CONTEXT_SKIP_REASON.GITIGNORE, { pathLabel }),
    };
  }

  let stat;
  try {
    stat = await vscode.workspace.fs.stat(fileUri);
  } catch {
    return {
      ok: false,
      reason: 'stat_failed',
      userMessage: `Lé Vibe Chat: could not read "${pathLabel}" (file missing or inaccessible).`,
    };
  }

  if (stat.type !== vscode.FileType.File) {
    return {
      ok: false,
      reason: 'not_file',
      userMessage: `Lé Vibe Chat: skipped "${pathLabel}" — not a regular file.`,
    };
  }

  const maxChars = Math.max(200, budget.maxCharsPerFile);
  if (stat.size > maxChars) {
    return {
      ok: false,
      reason: CONTEXT_SKIP_REASON.FILE_TOO_LARGE,
      userMessage: formatContextGuardUserMessage(CONTEXT_SKIP_REASON.FILE_TOO_LARGE, {
        pathLabel,
        maxChars,
        byteLength: stat.size,
      }),
    };
  }

  let bytes;
  try {
    bytes = await vscode.workspace.fs.readFile(fileUri);
  } catch (e) {
    const msg = e && e.message ? e.message : String(e);
    return {
      ok: false,
      reason: 'read_failed',
      userMessage: `Lé Vibe Chat: could not read "${pathLabel}" — ${msg}`,
    };
  }

  const buf = Buffer.from(bytes);
  if (bufferLooksBinary(buf)) {
    return {
      ok: false,
      reason: CONTEXT_SKIP_REASON.BINARY,
      userMessage: formatContextGuardUserMessage(CONTEXT_SKIP_REASON.BINARY, { pathLabel }),
    };
  }

  const raw = buf.toString('utf8');
  const excerpt = clipTextByBudget(raw, maxChars, budget.maxLinesPerFile);
  return { ok: true, excerpt };
}

module.exports = {
  CONTEXT_SKIP_REASON,
  BINARY_PROBE_BYTES,
  bufferLooksBinary,
  relativePosixForGitignore,
  loadGitignoreMatcher,
  formatContextGuardUserMessage,
  loadContextFileWithGuards,
};
