'use strict';

const { clipTextByBudget } = require('./workspace-context.js');

/** Hard cap on symbol nodes expanded (task-n14-2). */
const OUTLINE_MAX_SYMBOL_NODES = 200;

/** Max nesting depth when walking DocumentSymbol trees. */
const OUTLINE_MAX_DEPTH = 8;

/**
 * Mirrors `vscode.SymbolKind` numeric values (stable for outline text).
 * @see https://code.visualstudio.com/api/references/vscode-api#SymbolKind
 */
/** Aligns with `vscode.SymbolKind` (0–25). */
const SYMBOL_KIND_LABELS = Object.freeze({
  0: 'File',
  1: 'Module',
  2: 'Namespace',
  3: 'Package',
  4: 'Class',
  5: 'Method',
  6: 'Property',
  7: 'Field',
  8: 'Constructor',
  9: 'Enum',
  10: 'Interface',
  11: 'Function',
  12: 'Variable',
  13: 'Constant',
  14: 'String',
  15: 'Number',
  16: 'Boolean',
  17: 'Array',
  18: 'Object',
  19: 'Key',
  20: 'Null',
  21: 'EnumMember',
  22: 'Struct',
  23: 'Event',
  24: 'Operator',
  25: 'TypeParameter',
});

/**
 * @param {number} kind
 * @returns {string}
 */
function symbolKindLabel(kind) {
  const k = typeof kind === 'number' ? kind : Number(kind);
  return SYMBOL_KIND_LABELS[k] != null ? SYMBOL_KIND_LABELS[k] : `SymbolKind(${k})`;
}

/**
 * @param {*} sym
 * @returns {boolean}
 */
function isSymbolInformationLike(sym) {
  return Boolean(sym && sym.location && typeof sym.name === 'string');
}

/**
 * Normalize mixed SymbolInformation / DocumentSymbol trees for walking.
 * @param {*} sym
 * @returns {{ name: string, kind: number, detail?: string, children: *[], flat?: boolean }}
 */
function normalizeSymbolNode(sym) {
  if (!sym || typeof sym.name !== 'string') {
    return { name: '(symbol)', kind: 0, children: [] };
  }
  if (isSymbolInformationLike(sym)) {
    return {
      name: sym.name,
      kind: sym.kind,
      detail: sym.containerName,
      children: [],
      flat: true,
    };
  }
  return {
    name: sym.name,
    kind: sym.kind,
    detail: sym.detail,
    children: Array.isArray(sym.children) ? sym.children : [],
  };
}

/**
 * @param {*} sym
 * @param {number} depth
 * @param {number} maxDepth
 * @param {number} maxNodes
 * @param {{ count: number, lines: string[] }} acc
 */
function walkSymbols(sym, depth, maxDepth, maxNodes, acc) {
  if (acc.count >= maxNodes || depth > maxDepth) {
    return;
  }
  const n = normalizeSymbolNode(sym);
  const indent = '  '.repeat(Math.max(0, depth));
  const detail = n.detail ? ` ${String(n.detail)}` : '';
  acc.lines.push(`${indent}- ${symbolKindLabel(n.kind)} ${n.name}${detail}`);
  acc.count += 1;
  if (n.flat || !n.children.length) {
    return;
  }
  for (const ch of n.children) {
    if (acc.count >= maxNodes) {
      break;
    }
    walkSymbols(ch, depth + 1, maxDepth, maxNodes, acc);
  }
}

/**
 * @param {unknown} symbols raw from `vscode.executeDocumentSymbolProvider`
 * @param {{
 *   pathLabel: string,
 *   maxChars: number,
 *   maxLines: number,
 *   maxNodes?: number,
 *   maxDepth?: number,
 * }} opts
 * @returns {string}
 */
function outlineTextFromSymbols(symbols, opts) {
  const pathLabel = opts.pathLabel || '(unknown)';
  const maxChars = opts.maxChars;
  const maxLines = opts.maxLines;
  const maxNodes = opts.maxNodes != null ? opts.maxNodes : OUTLINE_MAX_SYMBOL_NODES;
  const maxDepth = opts.maxDepth != null ? opts.maxDepth : OUTLINE_MAX_DEPTH;
  const list = Array.isArray(symbols) ? symbols : [];
  const acc = { count: 0, lines: [] };
  for (const sym of list) {
    if (acc.count >= maxNodes) {
      break;
    }
    walkSymbols(sym, 0, maxDepth, maxNodes, acc);
  }
  const body = acc.lines.join('\n');
  const header = [
    `Outline (single file, language outline provider): ${pathLabel}`,
    'Bounded local outline — not a full-repo or cloud index (see README Epic N14).',
    '---',
    body || '(no symbols)',
  ].join('\n');
  return clipTextByBudget(header, maxChars, maxLines);
}

/**
 * @param {typeof import('vscode')} vscode
 * @param {() => { maxCharsPerFile: number, maxLinesPerFile: number }} getBudget
 * @returns {Promise<
 *   | { ok: true, path: string, content: string, kind: 'outline' }
 *   | { ok: false, userMessage: string }
 * >}
 */
async function fetchCurrentFileOutlineForContext(vscode, getBudget) {
  const ed = vscode.window.activeTextEditor;
  if (!ed || ed.document.uri.scheme !== 'file') {
    return { ok: false, userMessage: 'Lé Vibe Chat: open a workspace file in the editor first (file scheme).' };
  }
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) {
    return { ok: false, userMessage: 'Open a folder workspace first.' };
  }
  const uri = ed.document.uri;
  const rel = vscode.workspace.asRelativePath(uri, false);
  if (!rel || rel.startsWith('..')) {
    return { ok: false, userMessage: 'Lé Vibe Chat: active file must be under the workspace folder.' };
  }
  let raw;
  try {
    raw = await vscode.commands.executeCommand('vscode.executeDocumentSymbolProvider', uri);
  } catch (e) {
    const msg = e && e.message ? String(e.message) : String(e);
    return { ok: false, userMessage: `Lé Vibe Chat: outline failed — ${msg}` };
  }
  if (!raw || !Array.isArray(raw) || raw.length === 0) {
    return {
      ok: false,
      userMessage:
        'Lé Vibe Chat: no outline symbols for this file (install a language extension or use a supported language).',
    };
  }
  const budget = getBudget();
  const content = outlineTextFromSymbols(raw, {
    pathLabel: rel,
    maxChars: budget.maxCharsPerFile,
    maxLines: budget.maxLinesPerFile,
    maxNodes: OUTLINE_MAX_SYMBOL_NODES,
    maxDepth: OUTLINE_MAX_DEPTH,
  });
  return { ok: true, path: rel, content, kind: 'outline' };
}

module.exports = {
  OUTLINE_MAX_SYMBOL_NODES,
  OUTLINE_MAX_DEPTH,
  symbolKindLabel,
  outlineTextFromSymbols,
  fetchCurrentFileOutlineForContext,
};
