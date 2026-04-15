const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {
  WORKSPACE_PLAN_KIND,
  validateWorkspacePlan,
  formatPlanValidationForUser,
} = require('../workspace-plan.js');

const sampleUri = 'file:///tmp/ws/demo.txt';

function minimalValidPlan() {
  return {
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      {
        id: 'a',
        op: 'create_file',
        targetUri: sampleUri,
        content: 'x',
      },
    ],
  };
}

test('levibe.workspace-plan.v1 schema file parses (task-n10-1)', () => {
  const p = path.join(__dirname, '..', 'schemas', 'levibe.workspace-plan.v1.json');
  const j = JSON.parse(fs.readFileSync(p, 'utf8'));
  assert.equal(j.properties.kind.const, WORKSPACE_PLAN_KIND);
});

test('validateWorkspacePlan accepts create_file step (task-n10-1)', () => {
  const r = validateWorkspacePlan(minimalValidPlan());
  assert.equal(r.ok, true);
});

test('validateWorkspacePlan accepts mixed ordered steps (task-n10-1)', () => {
  const r = validateWorkspacePlan({
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      { id: '1', op: 'create_file', targetUri: 'file:///a.txt' },
      {
        id: '2',
        op: 'apply_edit',
        targetUri: 'file:///a.txt',
        edit: { kind: 'full_file', content: 'b\n' },
      },
      { id: '3', op: 'move_file', fromUri: 'file:///a.txt', toUri: 'file:///b.txt' },
      { id: '4', op: 'delete_file', targetUri: 'file:///b.txt' },
    ],
  });
  assert.equal(r.ok, true);
});

test('validateWorkspacePlan rejects wrong kind (task-n10-1)', () => {
  const r = validateWorkspacePlan({ ...minimalValidPlan(), kind: 'other' });
  assert.equal(r.ok, false);
  assert.ok(r.userMessage.startsWith('Lé Vibe Chat: workspace plan invalid'));
});

test('validateWorkspacePlan rejects empty steps (task-n10-1)', () => {
  const r = validateWorkspacePlan({ kind: WORKSPACE_PLAN_KIND, steps: [] });
  assert.equal(r.ok, false);
});

test('validateWorkspacePlan rejects duplicate step ids (task-n10-1)', () => {
  const r = validateWorkspacePlan({
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      { id: 'x', op: 'delete_file', targetUri: 'file:///y' },
      { id: 'x', op: 'delete_file', targetUri: 'file:///z' },
    ],
  });
  assert.equal(r.ok, false);
  assert.ok(String(r.userMessage).includes('duplicate'));
});

test('validateWorkspacePlan rejects apply_edit with invalid nested edit (task-n10-1)', () => {
  const r = validateWorkspacePlan({
    kind: WORKSPACE_PLAN_KIND,
    steps: [
      {
        id: 'e',
        op: 'apply_edit',
        targetUri: sampleUri,
        edit: { kind: 'full_file' },
      },
    ],
  });
  assert.equal(r.ok, false);
});

test('validateWorkspacePlan rejects extra top-level property (task-n10-1)', () => {
  const r = validateWorkspacePlan({ ...minimalValidPlan(), extra: 1 });
  assert.equal(r.ok, false);
});

test('formatPlanValidationForUser truncates long error lists (task-n10-1)', () => {
  const msg = formatPlanValidationForUser(new Array(12).fill('e'));
  assert.ok(msg.includes('…'));
});
