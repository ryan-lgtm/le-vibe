'use strict';

function buildOrchestratorGroundedPrompt(userPrompt, envSummary, snippets = {}) {
  const prompt = String(userPrompt || '').trim();
  const sections = [
    'SYSTEM ROLE (LE VIBE IDENTITY LOCK):',
    '- You ARE the Le Vibe Operator/Orchestrator for this workspace session.',
    '- Never claim you are "not the orchestrator" or redirect identity to an external CLI role.',
    '- Speak as the active in-editor operator grounded in local workspace/runtime state.',
    '- If context is missing, ask one concrete follow-up question.',
    '',
    `Environment summary: ${JSON.stringify(envSummary || {})}`,
  ];

  if (snippets.sessionManifestSnippet) {
    sections.push(
      '',
      'Session manifest excerpt (.lvibe/session-manifest.json):',
      String(snippets.sessionManifestSnippet),
    );
  }
  if (snippets.orchestratorWorkflowSnippet) {
    sections.push(
      '',
      'Orchestrator workflow excerpt (.lvibe/workflows/native-extension-master-orchestrator-prompt.md):',
      String(snippets.orchestratorWorkflowSnippet),
    );
  }

  sections.push('', `User request: ${prompt}`);
  return sections.join('\n');
}

module.exports = {
  buildOrchestratorGroundedPrompt,
};

