'use strict';

const path = require('node:path');

function isSafeRelativePath(relativePath) {
  if (!relativePath || typeof relativePath !== 'string') {
    return false;
  }
  if (path.isAbsolute(relativePath)) {
    return false;
  }
  const normalized = path.posix.normalize(relativePath.replace(/\\/g, '/'));
  if (normalized.startsWith('../') || normalized === '..') {
    return false;
  }
  return true;
}

function clipTextByBudget(text, maxChars, maxLines) {
  const lines = String(text || '').split('\n').slice(0, Math.max(1, maxLines));
  const clipped = lines.join('\n').slice(0, Math.max(1, maxChars));
  return clipped;
}

function buildPromptWithContext(userPrompt, contexts, maxTotalChars) {
  const prompt = String(userPrompt || '').trim();
  const selected = Array.isArray(contexts) ? contexts : [];
  if (!selected.length) {
    return prompt;
  }
  const sections = [];
  let used = 0;
  for (const item of selected) {
    if (!item || !item.path || !item.content) {
      continue;
    }
    const label = String(item.path);
    const body = String(item.content);
    const header = item.kind === 'folder' ? '### FOLDER' : '### FILE';
    const block = `${header}: ${label}\n${body}\n`;
    if (used + block.length > maxTotalChars) {
      break;
    }
    sections.push(block);
    used += block.length;
  }
  if (!sections.length) {
    return prompt;
  }
  return [
    'Use the following workspace context excerpts when answering. Treat them as local file snapshots.',
    '',
    ...sections,
    '',
    `### USER PROMPT`,
    prompt,
  ].join('\n');
}

module.exports = {
  isSafeRelativePath,
  clipTextByBudget,
  buildPromptWithContext,
};
