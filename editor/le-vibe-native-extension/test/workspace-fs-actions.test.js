'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  validateWorkspaceRelativeCreatePath,
  DEFAULT_DENIED_SEGMENTS,
  moveWorkspaceEntry,
  deleteWorkspaceEntry,
} = require('../workspace-fs-actions.js');

test('validateWorkspaceRelativeCreatePath rejects traversal (task-n11-1)', () => {
  const a = validateWorkspaceRelativeCreatePath('../outside.txt');
  assert.equal(a.ok, false);
  assert.ok(String(a.userMessage).includes('..'));

  const b = validateWorkspaceRelativeCreatePath('foo/../../etc/passwd');
  assert.equal(b.ok, false);

  const c = validateWorkspaceRelativeCreatePath('/abs/path.txt');
  assert.equal(c.ok, false);
});

test('validateWorkspaceRelativeCreatePath rejects denied segments (task-n11-1)', () => {
  assert.equal(validateWorkspaceRelativeCreatePath('.git/config').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('src/.git/hooks/x').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('node_modules/pkg/index.js').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('.ssh/known_hosts').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('x/.env').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('.GIT/config').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('src/Node_Modules/pkg/index.js').ok, false);
});

test('validateWorkspaceRelativeCreatePath accepts safe nested paths (task-n11-1)', () => {
  const r = validateWorkspaceRelativeCreatePath('notes/demo.md');
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.equal(r.normalizedRelative, 'notes/demo.md');
  }
});

test('validateWorkspaceRelativeCreatePath empty rejects (task-n11-1)', () => {
  assert.equal(validateWorkspaceRelativeCreatePath('').ok, false);
  assert.equal(validateWorkspaceRelativeCreatePath('   ').ok, false);
});

test('DEFAULT_DENIED_SEGMENTS includes expected roots (task-n11-1)', () => {
  assert.ok(DEFAULT_DENIED_SEGMENTS.has('.git'));
  assert.ok(DEFAULT_DENIED_SEGMENTS.has('node_modules'));
});

/**
 * @param {{ sourceMissing?: boolean, destExists?: boolean, applyOk?: boolean }} opts
 */
function mockVscodeForMove(opts = {}) {
  const { sourceMissing = false, destExists = false, applyOk = true } = opts;
  class WorkspaceEdit {
    constructor() {
      this.renameCalls = [];
    }

    renameFile(from, to, ropts) {
      this.renameCalls.push({ from: from.toString(), to: to.toString(), ropts });
    }
  }

  return {
    WorkspaceEdit,
    Uri: {
      parse(s) {
        const fsPath = s.replace(/^file:\/\//, '/');
        return { toString: () => s, fsPath };
      },
      /** Minimal VS Code-compatible join for `uriForNormalizedRelative` / move tests. */
      joinPath(base, ...pathSegments) {
        let p = base.fsPath || String(base.toString?.() ?? '').replace(/^file:\/\//, '/');
        p = p.replace(/\/+$/, '') || '/';
        for (const seg of pathSegments) {
          p += `/${seg}`;
        }
        const url = p.startsWith('//') ? `file:${p}` : `file://${p}`;
        return { toString: () => url, fsPath: p };
      },
    },
    workspace: {
      fs: {
        stat: async (uri) => {
          const u = uri.toString();
          if (u.includes('/a.txt')) {
            if (sourceMissing) {
              const e = new Error('ENOENT');
              /** @type {any} */ (e).code = 'FileNotFound';
              throw e;
            }
            return {};
          }
          if (u.includes('/b.txt')) {
            if (destExists) {
              return {};
            }
            const e = new Error('ENOENT');
            /** @type {any} */ (e).code = 'FileNotFound';
            throw e;
          }
          const e = new Error('ENOENT');
          /** @type {any} */ (e).code = 'FileNotFound';
          throw e;
        },
        rename: async () => {},
      },
      applyEdit: async () => applyOk,
    },
  };
}

test('moveWorkspaceEntry rejects missing source (task-n11-2)', async () => {
  const vscode = mockVscodeForMove({ sourceMissing: true });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'a.txt', 'b.txt');
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('nothing to move'));
});

test('moveWorkspaceEntry rejects existing destination (task-n11-2)', async () => {
  const vscode = mockVscodeForMove({ destExists: true });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'a.txt', 'b.txt');
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('destination already exists'));
});

test('moveWorkspaceEntry rejects identical paths (task-n11-2)', async () => {
  const vscode = mockVscodeForMove();
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'x/y.md', 'x/y.md');
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('same path'));
});

test('moveWorkspaceEntry succeeds when source exists and destination is free (task-n11-2)', async () => {
  const vscode = mockVscodeForMove({ applyOk: true });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'a.txt', 'b.txt');
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.ok(r.fromUri.toString().includes('a.txt'));
    assert.ok(r.toUri.toString().includes('b.txt'));
  }
});

test('moveWorkspaceEntry uses WorkspaceEdit.renameFile with overwrite false (task-cp3-2)', async () => {
  let seenWorkspaceEdit = null;
  class WorkspaceEdit {
    constructor() {
      this.renameCalls = [];
      seenWorkspaceEdit = this;
    }
    renameFile(from, to, ropts) {
      this.renameCalls.push({ from: from.toString(), to: to.toString(), ropts });
    }
  }
  const vscode = {
    WorkspaceEdit,
    Uri: {
      parse(s) {
        const fsPath = s.replace(/^file:\/\//, '/');
        return { toString: () => s, fsPath };
      },
      joinPath(base, ...pathSegments) {
        let p = base.fsPath || String(base.toString?.() ?? '').replace(/^file:\/\//, '/');
        p = p.replace(/\/+$/, '') || '/';
        for (const seg of pathSegments) p += `/${seg}`;
        const url = p.startsWith('//') ? `file:${p}` : `file://${p}`;
        return { toString: () => url, fsPath: p };
      },
    },
    workspace: {
      fs: {
        stat: async (uri) => {
          if (uri.toString().includes('/src.txt')) return {};
          throw Object.assign(new Error('ENOENT'), { code: 'FileNotFound' });
        },
      },
      applyEdit: async () => true,
    },
  };
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'src.txt', 'dst.txt');
  assert.equal(r.ok, true);
  assert.ok(seenWorkspaceEdit);
  assert.equal(seenWorkspaceEdit.renameCalls.length, 1);
  assert.equal(seenWorkspaceEdit.renameCalls[0].ropts.overwrite, false);
});

test('moveWorkspaceEntry fallback fs.rename maps destination exists to deterministic conflict (task-cp3-2)', async () => {
  class WorkspaceEdit {}
  const vscode = {
    WorkspaceEdit,
    Uri: {
      parse(s) {
        const fsPath = s.replace(/^file:\/\//, '/');
        return { toString: () => s, fsPath };
      },
      joinPath(base, ...pathSegments) {
        let p = base.fsPath || String(base.toString?.() ?? '').replace(/^file:\/\//, '/');
        p = p.replace(/\/+$/, '') || '/';
        for (const seg of pathSegments) p += `/${seg}`;
        const url = p.startsWith('//') ? `file:${p}` : `file://${p}`;
        return { toString: () => url, fsPath: p };
      },
    },
    workspace: {
      fs: {
        stat: async (uri) => {
          if (uri.toString().includes('/src.txt')) return {};
          throw Object.assign(new Error('ENOENT'), { code: 'FileNotFound' });
        },
        rename: async () => {
          throw Object.assign(new Error('file exists'), { code: 'EEXIST' });
        },
      },
      applyEdit: async () => true,
    },
  };
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await moveWorkspaceEntry(vscode, folder, 'src.txt', 'dst.txt');
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('destination already exists'));
});

/**
 * @param {{ missing?: boolean, applyOk?: boolean, isDirectory?: boolean }} opts
 */
function mockVscodeForDelete(opts = {}) {
  const { missing = false, applyOk = true, isDirectory = false } = opts;
  class WorkspaceEdit {
    constructor() {
      /** @type {{ uri: unknown, opts: unknown } | null} */
      this.lastDelete = null;
    }

    deleteFile(uri, delOpts) {
      this.lastDelete = { uri, opts: delOpts };
    }
  }

  return {
    FileType: { File: 1, Directory: 2 },
    WorkspaceEdit,
    Uri: {
      parse(s) {
        const fsPath = s.replace(/^file:\/\//, '/');
        return { toString: () => s, fsPath };
      },
      joinPath(base, ...pathSegments) {
        let p = base.fsPath || String(base.toString?.() ?? '').replace(/^file:\/\//, '/');
        p = p.replace(/\/+$/, '') || '/';
        for (const seg of pathSegments) {
          p += `/${seg}`;
        }
        const url = p.startsWith('//') ? `file:${p}` : `file://${p}`;
        return { toString: () => url, fsPath: p };
      },
    },
    workspace: {
      fs: {
        stat: async () => {
          if (missing) {
            const e = new Error('ENOENT');
            /** @type {any} */ (e).code = 'FileNotFound';
            throw e;
          }
          return { type: isDirectory ? 2 : 1 };
        },
        delete: async () => {},
      },
      applyEdit: async () => applyOk,
    },
  };
}

test('deleteWorkspaceEntry rejects missing path (task-n11-3)', async () => {
  const vscode = mockVscodeForDelete({ missing: true });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await deleteWorkspaceEntry(vscode, folder, 'gone.txt', { confirmedByUser: true });
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('nothing to delete'));
});

test('deleteWorkspaceEntry deletes file via WorkspaceEdit.deleteFile (task-n11-3)', async () => {
  const vscode = mockVscodeForDelete({ applyOk: true, isDirectory: false });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await deleteWorkspaceEntry(vscode, folder, 'x.txt', { confirmedByUser: true });
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.equal(r.isDirectory, false);
    assert.ok(r.uri.toString().includes('x.txt'));
  }
});

test('deleteWorkspaceEntry uses recursive delete for directories (task-n11-3)', async () => {
  const vscode = mockVscodeForDelete({ applyOk: true, isDirectory: true });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await deleteWorkspaceEntry(vscode, folder, 'sub/dir', { confirmedByUser: true });
  assert.equal(r.ok, true);
  if (r.ok) {
    assert.equal(r.isDirectory, true);
  }
});

test('deleteWorkspaceEntry surfaces applyEdit failure (task-n11-3)', async () => {
  const vscode = mockVscodeForDelete({ applyOk: false });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await deleteWorkspaceEntry(vscode, folder, 'locked.txt', { confirmedByUser: true });
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('not applied'));
});

test('deleteWorkspaceEntry blocks execution without explicit confirmation (task-cp3-3)', async () => {
  const vscode = mockVscodeForDelete({ applyOk: true, isDirectory: false });
  const folder = { uri: vscode.Uri.parse('file:///tmp/ws/') };
  const r = await deleteWorkspaceEntry(vscode, folder, 'x.txt');
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('requires explicit user confirmation'));
});
