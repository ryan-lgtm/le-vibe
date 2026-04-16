const test = require('node:test');
const assert = require('node:assert/strict');

const { buildOrchestratorGroundedPrompt } = require('../orchestrator-grounding');

test('grounded prompt enforces orchestrator identity lock', () => {
  const out = buildOrchestratorGroundedPrompt('Plan next steps', { workspace_uri: 'file:///ws' }, {});
  assert.ok(out.includes('SYSTEM ROLE (LE VIBE IDENTITY LOCK):'));
  assert.ok(out.includes('You ARE the Le Vibe Operator/Orchestrator'));
  assert.ok(out.includes('Never claim you are "not the orchestrator"'));
  assert.ok(out.includes('User request: Plan next steps'));
});

test('grounded prompt includes session/workflow snippets when present', () => {
  const out = buildOrchestratorGroundedPrompt(
    'Need implementation details',
    { workspace_uri: 'file:///ws' },
    {
      sessionManifestSnippet: '{"session":"abc"}',
      orchestratorWorkflowSnippet: '# workflow',
    },
  );
  assert.ok(out.includes('Session manifest excerpt (.lvibe/session-manifest.json):'));
  assert.ok(out.includes('{"session":"abc"}'));
  assert.ok(out.includes('Orchestrator workflow excerpt (.lvibe/workflows/native-extension-master-orchestrator-prompt.md):'));
  assert.ok(out.includes('# workflow'));
});

