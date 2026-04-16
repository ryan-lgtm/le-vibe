const test = require('node:test');
const assert = require('node:assert/strict');
const {
  fullDocumentRange,
  applyEditProposalBatchAsWorkspaceEdit,
} = require('../workspace-edit-apply.js');
const { mockVscode } = require('./mock-vscode-workspace-edit.js');

test('fullDocumentRange spans entire document (task-n9-3)', () => {
  const vscode = mockVscode({ docLines: ['a', 'bc'] });
  const doc = { lineCount: 2, lineAt: (i) => ({ text: i === 0 ? 'a' : 'bc' }) };
  const r = fullDocumentRange(vscode, doc);
  assert.equal(r.start.line, 0);
  assert.equal(r.end.line, 1);
  assert.equal(r.end.character, 2);
});

test('applyEditProposalBatchAsWorkspaceEdit one full_file uses single applyEdit (task-n9-3)', async () => {
  const vscode = mockVscode({ fileExists: true, docLines: ['x'] });
  const proposal = {
    kind: 'levibe.edit_proposal.v1',
    proposals: [
      {
        targetUri: 'file:///tmp/demo.txt',
        edit: { kind: 'full_file', content: 'y\n' },
      },
    ],
  };
  await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
  assert.equal(vscode.getApplyCount(), 1);
  const we = vscode.getLastWorkspaceEdit();
  assert.ok(we);
  assert.ok(we.ops.includes('replace'));
  assert.equal(we.ops.filter((o) => o === 'replace').length, 1);
});

test('applyEditProposalBatchAsWorkspaceEdit new file uses create+insert in one applyEdit (task-n9-3)', async () => {
  const vscode = mockVscode({ fileExists: false });
  const proposal = {
    kind: 'levibe.edit_proposal.v1',
    proposals: [
      {
        targetUri: 'file:///tmp/new.txt',
        edit: { kind: 'full_file', content: 'new\n' },
      },
    ],
  };
  await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
  assert.equal(vscode.getApplyCount(), 1);
  const we = vscode.getLastWorkspaceEdit();
  assert.ok(we.ops.includes('createFile'));
  assert.ok(we.ops.includes('insert'));
});

test('applyEditProposalBatchAsWorkspaceEdit batches two files in one applyEdit (task-n9-3)', async () => {
  const vscode = mockVscode({ fileExists: true, docLines: ['a'] });
  const proposal = {
    kind: 'levibe.edit_proposal.v1',
    proposals: [
      {
        targetUri: 'file:///tmp/one.txt',
        edit: { kind: 'full_file', content: '1\n' },
      },
      {
        targetUri: 'file:///tmp/two.txt',
        edit: { kind: 'full_file', content: '2\n' },
      },
    ],
  };
  await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
  assert.equal(vscode.getApplyCount(), 1);
  const we = vscode.getLastWorkspaceEdit();
  assert.equal(we.ops.filter((o) => o === 'replace').length, 2);
});

test('applyEditProposalBatchAsWorkspaceEdit range_replace single replace (task-n9-3)', async () => {
  const vscode = mockVscode({ fileExists: true, docLines: ['abcdef'] });
  const proposal = {
    kind: 'levibe.edit_proposal.v1',
    proposals: [
      {
        targetUri: 'file:///tmp/r.ts',
        edit: {
          kind: 'range_replace',
          range: {
            start: { line: 0, character: 0 },
            end: { line: 0, character: 3 },
          },
          newText: 'XYZ',
        },
      },
    ],
  };
  await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
  assert.equal(vscode.getApplyCount(), 1);
  const we = vscode.getLastWorkspaceEdit();
  assert.deepEqual(we.ops, ['replace']);
});
