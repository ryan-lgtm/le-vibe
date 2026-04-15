const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { validateEditProposal, EDIT_PROPOSAL_KIND } = require('../edit-proposal.js');

const sampleUri = 'file:///home/user/project/src/foo.ts';

function minimalValid() {
  return {
    kind: EDIT_PROPOSAL_KIND,
    proposals: [
      {
        targetUri: sampleUri,
        edit: { kind: 'full_file', content: 'export const x = 1;\n' },
      },
    ],
  };
}

test('levibe.edit-proposal.v1 schema file is valid JSON (task-n9-1)', () => {
  const p = path.join(__dirname, '..', 'schemas', 'levibe.edit-proposal.v1.json');
  const raw = fs.readFileSync(p, 'utf8');
  const parsed = JSON.parse(raw);
  assert.equal(parsed.properties.kind.const, EDIT_PROPOSAL_KIND);
});

test('validateEditProposal accepts full_file proposal (task-n9-1)', () => {
  const r = validateEditProposal(minimalValid());
  assert.equal(r.ok, true);
  assert.equal(r.value.proposals.length, 1);
});

test('validateEditProposal accepts range_replace with rationale and confidence (task-n9-1)', () => {
  const r = validateEditProposal({
    kind: EDIT_PROPOSAL_KIND,
    proposals: [
      {
        targetUri: sampleUri,
        edit: {
          kind: 'range_replace',
          range: {
            start: { line: 2, character: 0 },
            end: { line: 2, character: 4 },
          },
          newText: 'let',
        },
      },
    ],
    rationale: 'Rename for block scope.',
    confidence: { score: 0.92, flags: ['uncertain_api'] },
  });
  assert.equal(r.ok, true);
});

test('validateEditProposal rejects wrong kind', () => {
  const r = validateEditProposal({ ...minimalValid(), kind: 'other' });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some((e) => e.includes('kind')));
});

test('validateEditProposal rejects empty proposals', () => {
  const r = validateEditProposal({ kind: EDIT_PROPOSAL_KIND, proposals: [] });
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects non-file targetUri', () => {
  const o = minimalValid();
  o.proposals[0].targetUri = 'https://example.com/x';
  const r = validateEditProposal(o);
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects inverted range (task-n9-1)', () => {
  const r = validateEditProposal({
    kind: EDIT_PROPOSAL_KIND,
    proposals: [
      {
        targetUri: sampleUri,
        edit: {
          kind: 'range_replace',
          range: {
            start: { line: 5, character: 0 },
            end: { line: 2, character: 0 },
          },
          newText: '',
        },
      },
    ],
  });
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects extra top-level property', () => {
  const o = { ...minimalValid(), extra: 1 };
  const r = validateEditProposal(o);
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects rationale over max length', () => {
  const o = { ...minimalValid(), rationale: 'x'.repeat(16001) };
  const r = validateEditProposal(o);
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects confidence score out of range', () => {
  const r = validateEditProposal({
    ...minimalValid(),
    confidence: { score: 1.5 },
  });
  assert.equal(r.ok, false);
});

test('validateEditProposal rejects invalid confidence flag token', () => {
  const r = validateEditProposal({
    ...minimalValid(),
    confidence: { flags: ['Bad_Case'] },
  });
  assert.equal(r.ok, false);
});
