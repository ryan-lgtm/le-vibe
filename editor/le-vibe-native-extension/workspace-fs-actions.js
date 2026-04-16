'use strict';

const path = require('node:path');
const { isSafeRelativePath } = require('./workspace-context.js');

/** Blocked first-or-inner path segments (sensitive / heavy roots). */
const DEFAULT_DENIED_SEGMENTS = new Set(['.git', '.ssh', '.gnupg', 'node_modules', '.env']);

const MAX_RELATIVE_PATH_LEN = 512;

/**
 * @param {string} relativePath
 * @param {{ deniedSegments?: Set<string> }} [options]
 * @returns {{ ok: true, normalizedRelative: string } | { ok: false, userMessage: string }}
 */
function validateWorkspaceRelativeCreatePath(relativePath, options = {}) {
  const denied = options.deniedSegments || DEFAULT_DENIED_SEGMENTS;
  const deniedLower = new Set(Array.from(denied, (seg) => String(seg).toLowerCase()));
  if (!relativePath || typeof relativePath !== 'string') {
    return {
      ok: false,
      userMessage: 'Lé Vibe Chat: path must be a non-empty workspace-relative string.',
    };
  }
  const trimmed = relativePath.trim();
  if (!trimmed) {
    return { ok: false, userMessage: 'Lé Vibe Chat: path must not be empty.' };
  }
  if (trimmed.length > MAX_RELATIVE_PATH_LEN) {
    return {
      ok: false,
      userMessage: `Lé Vibe Chat: path too long (max ${MAX_RELATIVE_PATH_LEN} characters).`,
    };
  }
  if (!isSafeRelativePath(trimmed)) {
    return {
      ok: false,
      userMessage: 'Lé Vibe Chat: path must be workspace-relative (no ".." segments or absolute paths).',
    };
  }
  const normalized = path.posix.normalize(trimmed.replace(/\\/g, '/'));
  const segments = normalized.split('/').filter((s) => s.length > 0);
  for (const seg of segments) {
    if (deniedLower.has(seg.toLowerCase())) {
      return {
        ok: false,
        userMessage: `Lé Vibe Chat: path segment "${seg}" is blocked (sensitive or disallowed root).`,
      };
    }
  }
  return { ok: true, normalizedRelative: normalized };
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').Uri} folderUri
 * @param {string} normalizedRelative posix path under workspace root
 * @returns {import('vscode').Uri}
 */
function uriForNormalizedRelative(vscode, folderUri, normalizedRelative) {
  const parts = normalizedRelative.split('/').filter(Boolean);
  let u = folderUri;
  for (const p of parts) {
    u = vscode.Uri.joinPath(u, p);
  }
  return u;
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').Uri} folderUri
 * @param {string} normalizedDirRelative directory path only (no trailing slash)
 * @returns {Promise<{ ok: true } | { ok: false, userMessage: string }>}
 */
async function ensureDirectoryChain(vscode, folderUri, normalizedDirRelative) {
  const v = validateWorkspaceRelativeCreatePath(normalizedDirRelative);
  if (!v.ok) {
    return v;
  }
  const parts = v.normalizedRelative.split('/').filter(Boolean);
  let current = folderUri;
  for (const p of parts) {
    current = vscode.Uri.joinPath(current, p);
    try {
      await vscode.workspace.fs.stat(current);
    } catch {
      await vscode.workspace.fs.createDirectory(current);
    }
  }
  return { ok: true };
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {string} relativePath
 * @param {{ initialContent?: string, openAfterCreate?: boolean }} [options]
 * @returns {Promise<{ ok: true, uri: import('vscode').Uri } | { ok: false, userMessage: string }>}
 */
async function createWorkspaceFile(vscode, workspaceFolder, relativePath, options = {}) {
  const v = validateWorkspaceRelativeCreatePath(relativePath);
  if (!v.ok) {
    return v;
  }
  const fileUri = uriForNormalizedRelative(vscode, workspaceFolder.uri, v.normalizedRelative);
  try {
    await vscode.workspace.fs.stat(fileUri);
    return { ok: false, userMessage: 'Lé Vibe Chat: file already exists.' };
  } catch {
    // missing — ok
  }

  const segs = v.normalizedRelative.split('/').filter(Boolean);
  if (segs.length > 1) {
    const parentRel = segs.slice(0, -1).join('/');
    const ensured = await ensureDirectoryChain(vscode, workspaceFolder.uri, parentRel);
    if (!ensured.ok) {
      return ensured;
    }
  }

  const initial = typeof options.initialContent === 'string' ? options.initialContent : '';
  const we = new vscode.WorkspaceEdit();
  we.createFile(fileUri, { overwrite: false });
  we.insert(fileUri, new vscode.Position(0, 0), initial);
  const applied = await vscode.workspace.applyEdit(we);
  if (!applied) {
    return { ok: false, userMessage: 'Lé Vibe Chat: could not create file (workspace edit was not applied).' };
  }

  if (options.openAfterCreate) {
    const doc = await vscode.workspace.openTextDocument(fileUri);
    await vscode.window.showTextDocument(doc);
  }

  return { ok: true, uri: fileUri };
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {string} relativePath
 * @returns {Promise<{ ok: true, uri: import('vscode').Uri } | { ok: false, userMessage: string }>}
 */
async function createWorkspaceFolder(vscode, workspaceFolder, relativePath) {
  const v = validateWorkspaceRelativeCreatePath(relativePath);
  if (!v.ok) {
    return v;
  }
  const dirUri = uriForNormalizedRelative(vscode, workspaceFolder.uri, v.normalizedRelative);
  try {
    await vscode.workspace.fs.stat(dirUri);
    return { ok: false, userMessage: 'Lé Vibe Chat: folder already exists.' };
  } catch {
    // ok
  }

  const parts = v.normalizedRelative.split('/').filter(Boolean);
  let current = workspaceFolder.uri;
  for (const p of parts) {
    current = vscode.Uri.joinPath(current, p);
    try {
      await vscode.workspace.fs.stat(current);
    } catch {
      await vscode.workspace.fs.createDirectory(current);
    }
  }

  return { ok: true, uri: dirUri };
}

/**
 * Move or rename a file or folder within the workspace root using **`WorkspaceEdit.renameFile`**
 * when available (lets the workbench/git integration treat it as a rename when possible).
 * **`overwrite`** is always **`false`** — if the destination exists, the move aborts with a clear message.
 *
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {string} fromRelative
 * @param {string} toRelative
 * @returns {Promise<
 *   | { ok: true, fromUri: import('vscode').Uri, toUri: import('vscode').Uri }
 *   | { ok: false, userMessage: string }
 * >}
 */
async function moveWorkspaceEntry(vscode, workspaceFolder, fromRelative, toRelative) {
  const vf = validateWorkspaceRelativeCreatePath(fromRelative);
  if (!vf.ok) {
    return vf;
  }
  const vt = validateWorkspaceRelativeCreatePath(toRelative);
  if (!vt.ok) {
    return vt;
  }
  if (vf.normalizedRelative === vt.normalizedRelative) {
    return {
      ok: false,
      userMessage: 'Lé Vibe Chat: source and destination are the same path.',
    };
  }

  const fromUri = uriForNormalizedRelative(vscode, workspaceFolder.uri, vf.normalizedRelative);
  const toUri = uriForNormalizedRelative(vscode, workspaceFolder.uri, vt.normalizedRelative);

  try {
    await vscode.workspace.fs.stat(fromUri);
  } catch {
    return {
      ok: false,
      userMessage: 'Lé Vibe Chat: nothing to move — source path does not exist.',
    };
  }

  try {
    await vscode.workspace.fs.stat(toUri);
    return {
      ok: false,
      userMessage:
        'Lé Vibe Chat: destination already exists — move aborted (no overwrite). Remove or rename the destination first.',
    };
  } catch {
    // destination must be absent
  }

  const toSegs = vt.normalizedRelative.split('/').filter(Boolean);
  if (toSegs.length > 1) {
    const parentRel = toSegs.slice(0, -1).join('/');
    const ensured = await ensureDirectoryChain(vscode, workspaceFolder.uri, parentRel);
    if (!ensured.ok) {
      return ensured;
    }
  }

  const we = new vscode.WorkspaceEdit();
  if (typeof we.renameFile === 'function') {
    we.renameFile(fromUri, toUri, { overwrite: false });
    const applied = await vscode.workspace.applyEdit(we);
    if (!applied) {
      return {
        ok: false,
        userMessage:
          'Lé Vibe Chat: move was not applied — destination may exist, or the workspace rejected the rename.',
      };
    }
    return { ok: true, fromUri, toUri };
  }

  try {
    await vscode.workspace.fs.rename(fromUri, toUri, { overwrite: false });
  } catch (e) {
    const msg = e && e.message ? e.message : String(e);
    return {
      ok: false,
      userMessage: `Lé Vibe Chat: move failed — ${msg}`,
    };
  }
  return { ok: true, fromUri, toUri };
}

/**
 * Delete a file or folder under the workspace root. Uses **`WorkspaceEdit.deleteFile`** when available
 * (with **`recursive: true`** for directories). Never runs without caller-side confirmation.
 *
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {string} relativePath
 * @returns {Promise<
 *   | { ok: true, uri: import('vscode').Uri, isDirectory: boolean }
 *   | { ok: false, userMessage: string }
 * >}
 */
async function deleteWorkspaceEntry(vscode, workspaceFolder, relativePath) {
  const v = validateWorkspaceRelativeCreatePath(relativePath);
  if (!v.ok) {
    return v;
  }
  const targetUri = uriForNormalizedRelative(vscode, workspaceFolder.uri, v.normalizedRelative);
  let st;
  try {
    st = await vscode.workspace.fs.stat(targetUri);
  } catch {
    return {
      ok: false,
      userMessage: 'Lé Vibe Chat: nothing to delete — path does not exist.',
    };
  }
  const isDirectory = st.type === vscode.FileType.Directory;

  const we = new vscode.WorkspaceEdit();
  if (typeof we.deleteFile === 'function') {
    we.deleteFile(targetUri, { recursive: isDirectory });
    const applied = await vscode.workspace.applyEdit(we);
    if (!applied) {
      return {
        ok: false,
        userMessage:
          'Lé Vibe Chat: delete was not applied — the workspace rejected the operation (file may be busy or protected).',
      };
    }
    return { ok: true, uri: targetUri, isDirectory };
  }

  try {
    await vscode.workspace.fs.delete(targetUri, { recursive: isDirectory });
  } catch (e) {
    const msg = e && e.message ? e.message : String(e);
    return {
      ok: false,
      userMessage: `Lé Vibe Chat: delete failed — ${msg}`,
    };
  }
  return { ok: true, uri: targetUri, isDirectory };
}

module.exports = {
  DEFAULT_DENIED_SEGMENTS,
  MAX_RELATIVE_PATH_LEN: MAX_RELATIVE_PATH_LEN,
  validateWorkspaceRelativeCreatePath,
  uriForNormalizedRelative,
  createWorkspaceFile,
  createWorkspaceFolder,
  moveWorkspaceEntry,
  deleteWorkspaceEntry,
};
