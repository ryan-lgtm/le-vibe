'use strict';

const { clipTextByBudget } = require('./workspace-context.js');

/**
 * Build a workspace context entry from the active editor selection (task-n12-1).
 *
 * @param {string} relPath workspace-relative path
 * @param {string} text raw selection text
 * @param {{ startLine: number, startCharacter: number, endLine: number, endCharacter: number }} range VS Code 0-based
 * @param {{ maxCharsPerFile: number, maxLinesPerFile: number }} budget
 */
function buildSelectionContextEntry(relPath, text, range, budget) {
  const excerpt = clipTextByBudget(text, budget.maxCharsPerFile, budget.maxLinesPerFile);
  const line1 = range.startLine + 1;
  const line2 = range.endLine + 1;
  const rangeLabel =
    line1 === line2
      ? `line ${line1}, columns ${range.startCharacter}-${range.endCharacter}`
      : `lines ${line1}-${line2}`;
  const content = `[Editor selection · ${relPath} · ${rangeLabel}]\n\n${excerpt}`;
  return {
    path: relPath,
    content,
    selectionRange: {
      startLine: range.startLine,
      startCharacter: range.startCharacter,
      endLine: range.endLine,
      endCharacter: range.endCharacter,
    },
  };
}

/**
 * @param {string} relPath
 * @param {{ startLine: number, endLine: number }} range 0-based lines
 */
function prefillPromptForSelection(relPath, range) {
  const a = range.startLine + 1;
  const b = range.endLine + 1;
  const where = a === b ? `line ${a}` : `lines ${a}-${b}`;
  return `Question about the selection in ${relPath} (${where}):\n`;
}

module.exports = {
  buildSelectionContextEntry,
  prefillPromptForSelection,
};
