'use strict';

/**
 * Golden fixtures for `validateEditProposal` + `applyEditProposalBatchAsWorkspaceEdit`
 * (Epic N15 task-n15-2). No network — filesystem + pure validation only.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { validateEditProposal } = require('../edit-proposal.js');
const { applyEditProposalBatchAsWorkspaceEdit } = require('../workspace-edit-apply.js');
const { mockVscode } = require('./mock-vscode-workspace-edit.js');

const FIX_EDIT = path.join(__dirname, 'fixtures', 'n15-2', 'edit-proposal');
const FIX_WS = path.join(__dirname, 'fixtures', 'n15-2', 'workspace-edit');

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

for (const file of fs.readdirSync(FIX_EDIT).filter((f) => f.endsWith('.proposal.json'))) {
  const base = file.replace(/\.proposal\.json$/, '');
  test(`golden edit-proposal ${base} (task-n15-2)`, () => {
    const proposal = readJson(path.join(FIX_EDIT, file));
    const expected = readJson(path.join(FIX_EDIT, `${base}.expected.json`));
    const r = validateEditProposal(proposal);
    assert.equal(r.ok, expected.ok, JSON.stringify(r.ok ? r.value : r.errors));
    if (expected.ok) {
      assert.equal(r.ok, true);
      const v = r.value;
      assert.equal(v.kind, expected.kind);
      assert.equal(v.proposals.length, expected.proposalsLength);
      if (expected.hasRationale) {
        assert.equal(typeof v.rationale, 'string');
        assert.ok(v.rationale.length > 0);
      }
      if (expected.confidenceScore !== undefined) {
        assert.ok(v.confidence && typeof v.confidence === 'object');
        assert.equal(v.confidence.score, expected.confidenceScore);
      }
    } else {
      assert.equal(r.ok, false);
      assert.ok(Array.isArray(r.errors));
      for (const sub of expected.errorsContain) {
        assert.ok(
          r.errors.some((e) => e.includes(sub)),
          `expected an error containing "${sub}", got ${JSON.stringify(r.errors)}`,
        );
      }
    }
  });
}

for (const file of fs.readdirSync(FIX_WS).filter((f) => f.endsWith('.proposal.json'))) {
  const base = file.replace(/\.proposal\.json$/, '');
  test(`golden workspace-edit ${base} (task-n15-2)`, async () => {
    const proposal = readJson(path.join(FIX_WS, file));
    const meta = readJson(path.join(FIX_WS, `${base}.meta.json`));
    const validated = validateEditProposal(proposal);
    assert.equal(validated.ok, true, JSON.stringify(validated.ok ? validated.value : validated.errors));

    const vscode = mockVscode(meta.mock);
    await applyEditProposalBatchAsWorkspaceEdit(vscode, validated.value);
    assert.equal(vscode.getApplyCount(), meta.expectedApplyCount);
    const we = vscode.getLastWorkspaceEdit();
    assert.ok(we && we.ops);
    assert.deepEqual(we.ops, meta.expectedOps);
  });
}
