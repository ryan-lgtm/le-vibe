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

/** File metadata changed (mtime / size drift from preview snapshot). */
const EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE =
  'Lé Vibe Chat: apply blocked — file metadata changed since preview (mtime/size mismatch). Re-open Preview sample workspace edit to refresh and re-accept.';

/**
 * @param {string} text
 * @returns {string}
 */
function sha256Utf8(text) {
  return crypto.createHash('sha256').update(String(text), 'utf8').digest('hex');
}

/**
 * @param {string} beforeUtf8 disk content at preview time
 * @param {null | { mtime?: number, size?: number }} fileStat
 * @returns {{ contentSha256: string, mtimeMs: number | null, sizeBytes: number | null }}
 */
function buildPreviewRevision(beforeUtf8, fileStat = null) {
  const mtimeMs =
    fileStat && typeof fileStat.mtime === 'number' && Number.isFinite(fileStat.mtime)
      ? fileStat.mtime
      : null;
  const sizeBytes =
    fileStat && typeof fileStat.size === 'number' && Number.isFinite(fileStat.size)
      ? fileStat.size
      : null;
  return {
    contentSha256: sha256Utf8(beforeUtf8),
    mtimeMs,
    sizeBytes,
  };
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
  if (revision && (revision.mtimeMs !== null || revision.sizeBytes !== null)) {
    try {
      const st = await vscode.workspace.fs.stat(uri);
      if (
        (typeof revision.mtimeMs === 'number' && st.mtime !== revision.mtimeMs) ||
        (typeof revision.sizeBytes === 'number' && st.size !== revision.sizeBytes)
      ) {
        return { ok: false, panelMessage: EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE };
      }
    } catch {
      return { ok: false, panelMessage: EDIT_PREVIEW_FILE_MISSING_MESSAGE };
    }
  }
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
  EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE,
  sha256Utf8,
  buildPreviewRevision,
  assertContentMatchesRevision,
  checkDiskContentMatchesRevision,
};
