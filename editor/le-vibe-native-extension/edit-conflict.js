'use strict';

const crypto = require('node:crypto');

/**
 * Stale-preview detection (Epic N9 task-n9-5): snapshot UTF-8 content hash at preview time;
 * block apply if disk content no longer matches.
 */

/** Deterministic panel + toast copy (do not vary — tests assert). */
const EDIT_PREVIEW_STALE_CONFLICT_MESSAGE =
  'Lé Vibe Chat: apply blocked — file contents changed since this preview (stale proposal). Re-open Preview sample workspace edit.';

/** File removed after preview. */
const EDIT_PREVIEW_FILE_MISSING_MESSAGE =
  'Lé Vibe Chat: apply blocked — file no longer exists on disk. Re-open Preview sample workspace edit after restoring the file.';

/**
 * @param {string} text
 * @returns {string}
 */
function sha256Utf8(text) {
  return crypto.createHash('sha256').update(String(text), 'utf8').digest('hex');
}

/**
 * @param {string} beforeUtf8 disk content at preview time
 * @returns {{ contentSha256: string }}
 */
function buildPreviewRevision(beforeUtf8) {
  return { contentSha256: sha256Utf8(beforeUtf8) };
}

/**
 * @param {string} currentUtf8
 * @param {{ contentSha256: string }} revision
 * @returns {{ ok: true } | { ok: false, panelMessage: string }}
 */
function assertContentMatchesRevision(currentUtf8, revision) {
  const now = sha256Utf8(currentUtf8);
  if (now !== revision.contentSha256) {
    return { ok: false, panelMessage: EDIT_PREVIEW_STALE_CONFLICT_MESSAGE };
  }
  return { ok: true };
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').Uri} uri
 * @param {{ contentSha256: string }} revision
 * @returns {Promise<{ ok: true } | { ok: false, panelMessage: string }>}
 */
async function checkDiskContentMatchesRevision(vscode, uri, revision) {
  let bytes;
  try {
    bytes = await vscode.workspace.fs.readFile(uri);
  } catch {
    return { ok: false, panelMessage: EDIT_PREVIEW_FILE_MISSING_MESSAGE };
  }
  const current = Buffer.from(bytes).toString('utf8');
  return assertContentMatchesRevision(current, revision);
}

module.exports = {
  EDIT_PREVIEW_STALE_CONFLICT_MESSAGE,
  EDIT_PREVIEW_FILE_MISSING_MESSAGE,
  sha256Utf8,
  buildPreviewRevision,
  assertContentMatchesRevision,
  checkDiskContentMatchesRevision,
};
