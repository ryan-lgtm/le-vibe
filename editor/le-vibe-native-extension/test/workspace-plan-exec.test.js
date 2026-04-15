'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { WORKSPACE_PLAN_KIND } = require('../workspace-plan.js');
const {
  formatWorkspacePlanProgressStatus,
  buildAuditRecord,
  buildRollbackAuditRecord,
  applyWorkspacePlanRollbackInverses,
  executeValidatedWorkspacePlan,
} = require('../workspace-plan-exec.js');

test('formatWorkspacePlanProgressStatus (task-n10-2)', () => {
  const s = formatWorkspacePlanProgressStatus(0, 3, 'create_file', '.lvibe/x.txt', 'running');
  assert.ok(s.includes('plan step 1/3'));
  assert.ok(s.includes('create_file'));
  assert.ok(s.includes('.lvibe/x.txt'));
  assert.ok(s.includes('running'));
});

test('buildAuditRecord uses lvibe.workspace_plan_audit.v1 contract (task-n10-2)', () => {
  const r = buildAuditRecord({
    workspaceUri: 'file:///ws',
    stepIndex: 0,
    stepTotal: 1,
    stepId: 'a',
    op: 'create_file',
    pathLabel: 'x.txt',
    phase: 'start',
    runCancelled: false,
  });
  assert.equal(r.contract_version, 'lvibe.workspace_plan_audit.v1');
  assert.equal(r.event_type, 'workspace_plan_step');
  assert.equal(r.local_only, true);
});

/**
 * Minimal vscode stub for workspace-plan-exec + workspace-edit-apply.
 * @param {{ fileExistsSeq?: boolean[], snapshotReads?: { miss?: boolean, utf8?: string }[] }} opts
 */
function mockVscodePlanExec(opts = {}) {
  const { fileExistsSeq = [false, true], snapshotReads = [{ miss: true }, { miss: false, utf8: 'a\n' }] } = opts;
  let statCalls = 0;
  let snapReadCalls = 0;

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

    deleteFile() {
      this.ops.push('deleteFile');
    }

    renameFile() {
      this.ops.push('renameFile');
    }
  }

  const vscode = {
    Position,
    Range,
    WorkspaceEdit,
    Uri: {
      parse(s) {
        const fsPath = s.replace(/^file:\/\//, '/');
        return { toString: () => s, fsPath };
      },
    },
    workspace: {
      asRelativePath(uri) {
        const p = uri.fsPath || '';
        return p.replace(/^\/tmp\/ws\//, '');
      },
      fs: {
        readFile: async () => {
          const spec = snapshotReads[snapReadCalls];
          snapReadCalls += 1;
          if (!spec || spec.miss) {
            const e = new Error('not found');
            /** @type {any} */ (e).code = 'FileNotFound';
            throw e;
          }
          return Buffer.from(spec.utf8 ?? '', 'utf8');
        },
        stat: async () => {
          const exists = fileExistsSeq[statCalls];
          statCalls += 1;
          if (!exists) {
            const e = new Error('not found');
            /** @type {any} */ (e).code = 'FileNotFound';
            throw e;
          }
          return {};
        },
        rename: async () => {},
      },
      openTextDocument: async (uri) => {
        const pathStr = typeof uri === 'string' ? uri : uri.toString();
        const content = pathStr.endsWith('b.txt') ? 'b\n' : 'a\n';
        const lines = content.split('\n');
        return {
          lineCount: Math.max(1, lines.length),
          lineAt: (i) => ({ text: lines[i] !== undefined ? lines[i] : '' }),
        };
      },
      applyEdit: async () => true,
    },
  };

  return vscode;
}

test('executeValidatedWorkspacePlan runs steps and writes audit JSONL (task-n10-2)', async () => {
  const vscode = mockVscodePlanExec({ fileExistsSeq: [false, true] });
  const wfUri = vscode.Uri.parse('file:///tmp/ws/');
  const auditPath = path.join(os.tmpdir(), `levibe-plan-audit-${Date.now()}.jsonl`);
  try {
    const plan = {
      kind: WORKSPACE_PLAN_KIND,
      steps: [
        {
          id: 's1',
          op: 'create_file',
          targetUri: 'file:///tmp/ws/a.txt',
          content: 'a\n',
        },
        {
          id: 's2',
          op: 'apply_edit',
          targetUri: 'file:///tmp/ws/a.txt',
          edit: { kind: 'full_file', content: 'b\n' },
        },
      ],
    };
    const lines = [];
    const r = await executeValidatedWorkspacePlan(vscode, plan, {
      workspaceFolder: { uri: wfUri },
      workspaceUriStr: wfUri.toString(),
      auditPath,
      onProgress: (x) => lines.push(x),
    });
    assert.equal(r.ok, true);
    assert.equal(r.cancelled, false);
    assert.equal(r.completedSteps, 2);
    assert.ok(lines.some((l) => l.includes('plan step 1/2')));
    assert.ok(lines.some((l) => l.includes('plan step 2/2')));
    assert.ok(lines.some((l) => l.includes('plan finished')));
    const raw = fs.readFileSync(auditPath, 'utf8').trim().split('\n').filter(Boolean);
    assert.ok(raw.length >= 4, 'start+completed per step');
    const first = JSON.parse(raw[0]);
    assert.equal(first.contract_version, 'lvibe.workspace_plan_audit.v1');
  } finally {
    try {
      fs.unlinkSync(auditPath);
    } catch {
      // ignore
    }
  }
});

test('executeValidatedWorkspacePlan respects shouldCancel before remaining steps (task-n10-2)', async () => {
  const vscode = mockVscodePlanExec({ fileExistsSeq: [false], snapshotReads: [{ miss: true }] });
  const wfUri = vscode.Uri.parse('file:///tmp/ws/');
  const auditPath = path.join(os.tmpdir(), `levibe-plan-audit-${Date.now()}-c.jsonl`);
  let cancelBeforeStep2 = false;
  try {
    const plan = {
      kind: WORKSPACE_PLAN_KIND,
      steps: [
        { id: 's1', op: 'create_file', targetUri: 'file:///tmp/ws/b.txt', content: 'x\n' },
        { id: 's2', op: 'delete_file', targetUri: 'file:///tmp/ws/b.txt' },
      ],
    };
    const r = await executeValidatedWorkspacePlan(vscode, plan, {
      workspaceFolder: { uri: wfUri },
      workspaceUriStr: wfUri.toString(),
      auditPath,
      shouldCancel: () => cancelBeforeStep2,
      onProgress: (line) => {
        if (line.includes('plan step 1/2') && line.includes('done')) {
          cancelBeforeStep2 = true;
        }
      },
    });
    assert.equal(r.ok, true);
    assert.equal(r.cancelled, true);
    assert.equal(r.completedSteps, 1);
  } finally {
    try {
      fs.unlinkSync(auditPath);
    } catch {
      // ignore
    }
  }
});

test('buildRollbackAuditRecord (task-n10-3)', () => {
  const r = buildRollbackAuditRecord({ workspaceUri: 'file:///ws', stepsUndone: 2 });
  assert.equal(r.contract_version, 'lvibe.workspace_plan_audit.v1');
  assert.equal(r.event_type, 'workspace_plan_rollback');
  assert.equal(r.steps_undone, 2);
});

test('executeValidatedWorkspacePlan failure returns rollbackInverses (task-n10-3)', async () => {
  const vscode = mockVscodePlanExec({
    fileExistsSeq: [false, true],
    snapshotReads: [{ miss: true }, { miss: false, utf8: 'a\n' }],
  });
  const wfUri = vscode.Uri.parse('file:///tmp/ws/');
  const auditPath = path.join(os.tmpdir(), `levibe-plan-audit-${Date.now()}-f.jsonl`);
  try {
    const plan = {
      kind: WORKSPACE_PLAN_KIND,
      steps: [
        { id: 's1', op: 'create_file', targetUri: 'file:///tmp/ws/a.txt', content: 'a\n' },
        { id: 's2', op: 'apply_edit', targetUri: 'file:///tmp/ws/a.txt', edit: { kind: 'full_file', content: 'b\n' } },
      ],
    };
    const r = await executeValidatedWorkspacePlan(vscode, plan, {
      workspaceFolder: { uri: wfUri },
      workspaceUriStr: wfUri.toString(),
      auditPath,
      failStepAtIndex: 1,
    });
    assert.equal(r.ok, false);
    assert.equal(r.completedSteps, 1);
    assert.ok(Array.isArray(r.rollbackInverses));
    assert.equal(r.rollbackInverses.length, 1);
    assert.equal(r.rollbackInverses[0].op, 'delete_file');
    assert.ok(String(r.rollbackInverses[0].targetUri).includes('a.txt'));
  } finally {
    try {
      fs.unlinkSync(auditPath);
    } catch {
      // ignore
    }
  }
});

test('applyWorkspacePlanRollbackInverses applies inverses in reverse order (task-n10-3)', async () => {
  const vscode = mockVscodePlanExec({
    fileExistsSeq: [true, true],
    snapshotReads: [],
  });
  const ops = [];
  const origApply = vscode.workspace.applyEdit.bind(vscode.workspace);
  vscode.workspace.applyEdit = async (we) => {
    ops.push(we);
    return true;
  };
  const auditPath = path.join(os.tmpdir(), `levibe-rollback-${Date.now()}.jsonl`);
  try {
    const inverses = [
      { op: 'delete_file', targetUri: 'file:///tmp/ws/z.txt' },
      { op: 'write_full', targetUri: 'file:///tmp/ws/y.txt', content: 'rollback\n' },
    ];
    const r = await applyWorkspacePlanRollbackInverses(vscode, inverses, {
      auditPath,
      workspaceUriStr: 'file:///tmp/ws',
    });
    assert.equal(r.ok, true);
    assert.equal(ops.length, 2);
    vscode.workspace.applyEdit = origApply;
    const tail = fs.readFileSync(auditPath, 'utf8').trim().split('\n').pop();
    const row = JSON.parse(tail);
    assert.equal(row.event_type, 'workspace_plan_rollback');
    assert.equal(row.steps_undone, 2);
  } finally {
    try {
      fs.unlinkSync(auditPath);
    } catch {
      // ignore
    }
  }
});
