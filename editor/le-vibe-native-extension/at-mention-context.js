'use strict';

const { isSafeRelativePath, clipTextByBudget } = require('./workspace-context.js');
const {
  loadGitignoreMatcher,
  loadContextFileWithGuards,
  relativePosixForGitignore,
} = require('./context-file-guards.js');

/** VS Code `findFiles` max results for @file / @folder discovery (task-n14-1). */
const FILE_PICKER_MAX_SCAN_URIS = 400;

/** Max distinct folder paths offered in @folder QuickPick (task-n14-1). */
const FOLDER_QUICKPICK_MAX_CANDIDATES = 200;

const FIND_EXCLUDE = '**/{node_modules,.git,.lvibe}/**';

/**
 * @template T
 * @param {T[]} arr
 * @param {number} cap
 * @returns {T[]}
 */
function sliceToCap(arr, cap) {
  if (!Array.isArray(arr) || cap <= 0) {
    return [];
  }
  return arr.slice(0, cap);
}

/**
 * @param {string} fileLabel workspace-relative posix path to a file
 * @returns {string[]} unique folder prefixes (posix, relative), excluding empty root handled separately
 */
function parentFolderPrefixes(fileLabel) {
  const rel = String(fileLabel || '').replace(/\\/g, '/').replace(/^\.\//, '');
  if (!rel || rel.endsWith('/')) {
    return [];
  }
  const parts = rel.split('/').filter(Boolean);
  if (parts.length < 2) {
    return [];
  }
  const out = [];
  for (let i = 0; i < parts.length - 1; i += 1) {
    out.push(parts.slice(0, i + 1).join('/'));
  }
  return out;
}

/**
 * @param {import('ignore').Ignore} ig
 * @param {string} folderRel posix path without trailing slash
 * @returns {boolean}
 */
function folderIgnoredByGitignore(ig, folderRel) {
  const rel = relativePosixForGitignore(folderRel);
  if (!rel) {
    return false;
  }
  if (ig.ignores(rel)) {
    return true;
  }
  if (ig.ignores(`${rel}/`)) {
    return true;
  }
  return false;
}

/**
 * @param {string[]} fileLabels
 * @param {import('ignore').Ignore} ig
 * @returns {string[]}
 */
function uniqueFolderCandidatesFromFiles(fileLabels, ig) {
  const set = new Set();
  set.add('');
  for (const label of fileLabels) {
    for (const p of parentFolderPrefixes(label)) {
      if (!folderIgnoredByGitignore(ig, p)) {
        set.add(p);
      }
    }
  }
  const list = Array.from(set).sort((a, b) => a.localeCompare(b));
  return sliceToCap(list, FOLDER_QUICKPICK_MAX_CANDIDATES);
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder} workspaceFolder
 * @param {string} relFolder '' or posix path
 * @param {{ maxCharsPerFile: number, maxLinesPerFile: number }} budget
 * @returns {Promise<string>}
 */
async function buildFolderListingExcerpt(vscode, workspaceFolder, relFolder, budget) {
  const parts = String(relFolder || '')
    .replace(/\\/g, '/')
    .split('/')
    .filter((s) => s.length > 0 && s !== '.' && s !== '..');
  const base = workspaceFolder.uri;
  const folderUri = parts.length ? vscode.Uri.joinPath(base, ...parts) : base;
  let entries;
  try {
    entries = await vscode.workspace.fs.readDirectory(folderUri);
  } catch {
    return '(could not read directory listing)';
  }
  const lines = entries
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([name, type]) => {
      const isDir = type === vscode.FileType.Directory;
      return `${isDir ? '[dir] ' : '[file] '}${name}`;
    });
  const text = lines.join('\n');
  return clipTextByBudget(text, budget.maxCharsPerFile, budget.maxLinesPerFile);
}

/**
 * @param {typeof import('vscode')} vscode
 * @param {() => { maxCharsPerFile: number, maxLinesPerFile: number }} getBudget from Settings (contextMax*)
 * @returns {Promise<null | { path: string, content: string, kind?: 'file' | 'folder' }>}
 */
async function pickAtFileContext(vscode, getBudget) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    return null;
  }
  const ig = await loadGitignoreMatcher(vscode, folder);
  const files = await vscode.workspace.findFiles('**/*', FIND_EXCLUDE, FILE_PICKER_MAX_SCAN_URIS);
  if (!files.length) {
    await vscode.window.showInformationMessage('No workspace files available for @file context.');
    return null;
  }
  const items = sliceToCap(files, FILE_PICKER_MAX_SCAN_URIS)
    .map((uri) => ({
      label: vscode.workspace.asRelativePath(uri, false),
      uri,
    }))
    .filter((item) => !ig.ignores(relativePosixForGitignore(item.label)));
  if (!items.length) {
    await vscode.window.showInformationMessage(
      'Lé Vibe Chat: no @file candidates — empty tree or matches exceed cap / .gitignore.',
    );
    return null;
  }
  const choice = await vscode.window.showQuickPick(items, {
    title: 'Lé Vibe Chat: @file — add workspace file to context',
    placeHolder: `Search capped at ${FILE_PICKER_MAX_SCAN_URIS} paths (context excerpts use contextMax* settings)`,
  });
  if (!choice) {
    return null;
  }
  if (!isSafeRelativePath(choice.label)) {
    await vscode.window.showWarningMessage('Unsafe file reference blocked.');
    return null;
  }
  const budget = getBudget();
  const prep = await loadContextFileWithGuards(
    vscode,
    folder,
    choice.uri,
    choice.label,
    { maxCharsPerFile: budget.maxCharsPerFile, maxLinesPerFile: budget.maxLinesPerFile },
    ig,
  );
  if (!prep.ok) {
    await vscode.window.showWarningMessage(prep.userMessage);
    return null;
  }
  return { path: choice.label, content: prep.excerpt, kind: 'file' };
}

/**
 * @param {typeof import('vscode')} vscode
 * @param {() => { maxCharsPerFile: number, maxLinesPerFile: number }} getBudget
 * @returns {Promise<null | { path: string, content: string, kind?: 'file' | 'folder' }>}
 */
async function pickAtFolderContext(vscode, getBudget) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    await vscode.window.showWarningMessage('Open a folder workspace first.');
    return null;
  }
  const ig = await loadGitignoreMatcher(vscode, folder);
  const files = await vscode.workspace.findFiles('**/*', FIND_EXCLUDE, FILE_PICKER_MAX_SCAN_URIS);
  const labels = sliceToCap(files, FILE_PICKER_MAX_SCAN_URIS).map((u) =>
    vscode.workspace.asRelativePath(u, false),
  );
  const filteredLabels = labels.filter((l) => !ig.ignores(relativePosixForGitignore(l)));
  const folderChoices = uniqueFolderCandidatesFromFiles(filteredLabels, ig).map((rel) => ({
    label: rel === '' ? '.' : rel,
    rel,
  }));
  if (!folderChoices.length) {
    await vscode.window.showInformationMessage('No workspace folders available for @folder context.');
    return null;
  }
  const choice = await vscode.window.showQuickPick(folderChoices, {
    title: 'Lé Vibe Chat: @folder — add folder listing to context',
    placeHolder: `Folders derived from scanned files (max ${FOLDER_QUICKPICK_MAX_CANDIDATES} entries; max ${FILE_PICKER_MAX_SCAN_URIS} files scanned)`,
  });
  if (!choice) {
    return null;
  }
  const rel = choice.rel;
  const displayPath = rel === '' ? '.' : rel;
  if (rel !== '' && !isSafeRelativePath(rel)) {
    await vscode.window.showWarningMessage('Unsafe folder reference blocked.');
    return null;
  }
  const budget = getBudget();
  const excerpt = await buildFolderListingExcerpt(vscode, folder, rel, budget);
  return { path: displayPath, content: excerpt, kind: 'folder' };
}

module.exports = {
  FILE_PICKER_MAX_SCAN_URIS,
  FOLDER_QUICKPICK_MAX_CANDIDATES,
  FIND_EXCLUDE,
  sliceToCap,
  parentFolderPrefixes,
  uniqueFolderCandidatesFromFiles,
  buildFolderListingExcerpt,
  pickAtFileContext,
  pickAtFolderContext,
};
