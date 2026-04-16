'use strict';

/**
 * Minimal vscode mock for {@link ../workspace-edit-apply.js} tests (no network).
 */

/**
 * @param {{ fileExists?: boolean, docLines?: string[] }} opts
 */
function mockVscode({ fileExists = true, docLines = ['hello'] } = {}) {
  let applyCount = 0;
  /** @type {unknown} */
  let lastWe = null;

  class Position {
    constructor(line, character) {
      this.line = line;
      this.character = character;
    }
  }

  class Range {
    constructor(start, end) {
      this.start = start;
      this.end = end;
    }
  }

  class WorkspaceEdit {
    constructor() {
      this.ops = [];
    }

    createFile() {
      this.ops.push('createFile');
    }

    insert() {
      this.ops.push('insert');
    }

    replace() {
      this.ops.push('replace');
    }
  }

  const vscode = {
    Position,
    Range,
    WorkspaceEdit,
    Uri: {
      parse(s) {
        return { toString: () => s, fsPath: s.replace(/^file:\/\//, '') };
      },
    },
    workspace: {
      fs: {
        stat: async () => {
          if (!fileExists) {
            const e = new Error('not found');
            /** @type {any} */ (e).code = 'FileNotFound';
            throw e;
          }
          return {};
        },
      },
      openTextDocument: async () => ({
        lineCount: docLines.length,
        lineAt: (i) => ({ text: docLines[i] }),
      }),
      applyEdit: async (we) => {
        applyCount += 1;
        lastWe = we;
        return true;
      },
    },
    getApplyCount: () => applyCount,
    getLastWorkspaceEdit: () => lastWe,
  };

  return vscode;
}

module.exports = { mockVscode };
