'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { WORKSPACE_PLAN_KIND } = require('../workspace-plan.js');
const {
  roughTokenEstimate,
  dryRunValidatedWorkspacePlan,
  DEFAULT_MAX_OUTPUT_LINES,
} = require('../workspace-plan-dry-run.js');

test('roughTokenEstimate is bytes/4 ceiling (bounded) (task-n10-4)', () => {
  assert.equal(roughTokenEstimate(0), 0);
  assert.equal(roughTokenEstimate(3), 1);
  assert.equal(roughTokenEstimate(4), 1);
  assert.equal(roughTokenEstimate(5), 2);
});

test('dryRunValidatedWorkspacePlan lists steps without writes (task-n10-4)', async () => {
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
  const vscode = {
    Position,
    Range,
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
          throw Object.assign(new Error('missing'), { code: 'FileNotFound' });
        },
      },
      openTextDocument: async () => {
        throw new Error('no doc');
      },
    },
  };
  const wfUri = vscode.Uri.parse('file:///tmp/ws/');
  const plan = {
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      { id: 'a', op: 'create_file', targetUri: 'file:///tmp/ws/x.txt', content: 'hi' },
      {
        id: 'b',
        op: 'apply_edit',
        targetUri: 'file:///tmp/ws/x.txt',
        edit: { kind: 'full_file', content: 'hello' },
      },
    ],
  };
  const r = await dryRunValidatedWorkspacePlan(vscode, plan, {
    workspaceFolder: { uri: wfUri },
    maxOutputLines: DEFAULT_MAX_OUTPUT_LINES,
  });
  assert.ok(r.lines.length >= 3);
  assert.ok(r.lines[0].includes('no disk writes'));
  assert.ok(r.lines.some((l) => l.includes('create_file')));
  assert.ok(r.lines.some((l) => l.includes('apply_edit')));
  assert.ok(r.lines.some((l) => l.includes('summary')));
  assert.equal(r.totalEstimatedBytes, 2 + 5);
  assert.ok(r.lines[r.lines.length - 1].includes('0 disk writes'));
});
