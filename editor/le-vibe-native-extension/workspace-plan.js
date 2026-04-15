'use strict';

const { validateEditProposal, EDIT_PROPOSAL_KIND } = require('./edit-proposal.js');

const WORKSPACE_PLAN_KIND = 'levibe.workspace_plan.v1';

const OPS = new Set(['create_file', 'apply_edit', 'delete_file', 'move_file']);

/**
 * @param {string[]} errors
 * @returns {string}
 */
function formatPlanValidationForUser(errors) {
  const list = errors.slice(0, 10);
  const detail = list.join('; ');
  const suffix = errors.length > 10 ? ` … (+${errors.length - 10} more)` : '';
  return `Lé Vibe Chat: workspace plan invalid — ${detail}${suffix}`;
}

/**
 * @param {unknown} raw
 * @returns {{ ok: true, value: object } | { ok: false, errors: string[], userMessage: string }}
 */
function validateWorkspacePlan(raw) {
  const errors = [];
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) {
    const e = ['root must be a non-null object'];
    return { ok: false, errors: e, userMessage: formatPlanValidationForUser(e) };
  }
  const o = /** @type {Record<string, unknown>} */ (raw);

  if (o.kind !== WORKSPACE_PLAN_KIND) {
    errors.push(`kind must be "${WORKSPACE_PLAN_KIND}"`);
  }

  if (!Array.isArray(o.steps) || o.steps.length < 1) {
    errors.push('steps must be a non-empty array');
  } else {
    const seen = new Set();
    o.steps.forEach((step, i) => {
      validatePlanStep(step, `steps[${i}]`, errors, seen);
    });
  }

  for (const k of Object.keys(o)) {
    if (k !== 'kind' && k !== 'steps') errors.push(`unexpected property: ${k}`);
  }

  if (errors.length) {
    return { ok: false, errors, userMessage: formatPlanValidationForUser(errors) };
  }

  return { ok: true, value: { kind: WORKSPACE_PLAN_KIND, steps: o.steps } };
}

/**
 * @param {unknown} step
 * @param {string} path
 * @param {string[]} errors
 * @param {Set<string>} seenIds
 */
function validatePlanStep(step, path, errors, seenIds) {
  if (step === null || typeof step !== 'object' || Array.isArray(step)) {
    errors.push(`${path} must be an object`);
    return;
  }
  const s = /** @type {Record<string, unknown>} */ (step);

  if (typeof s.id !== 'string' || s.id.length < 1 || s.id.length > 128) {
    errors.push(`${path}.id must be a non-empty string (max 128)`);
  } else if (seenIds.has(s.id)) {
    errors.push(`${path}.id duplicate: ${s.id}`);
  } else {
    seenIds.add(s.id);
  }

  if (typeof s.op !== 'string' || !OPS.has(s.op)) {
    errors.push(`${path}.op must be one of: ${[...OPS].join(', ')}`);
    return;
  }

  const op = s.op;

  if (op === 'create_file') {
    if (typeof s.targetUri !== 'string' || !s.targetUri.startsWith('file://')) {
      errors.push(`${path}.targetUri must be a file:// URI`);
    }
    if ('content' in s && typeof s.content !== 'string') {
      errors.push(`${path}.content must be a string when present`);
    }
    for (const k of Object.keys(s)) {
      if (!['id', 'op', 'targetUri', 'content'].includes(k)) errors.push(`${path}: unexpected property ${k}`);
    }
    return;
  }

  if (op === 'apply_edit') {
    if (typeof s.targetUri !== 'string' || !s.targetUri.startsWith('file://')) {
      errors.push(`${path}.targetUri must be a file:// URI`);
    }
    const nested = {
      kind: EDIT_PROPOSAL_KIND,
      proposals: [{ targetUri: s.targetUri, edit: s.edit }],
    };
    const v = validateEditProposal(nested);
    if (!v.ok) {
      v.errors.forEach((e) => errors.push(`${path} edit: ${e}`));
    }
    for (const k of Object.keys(s)) {
      if (!['id', 'op', 'targetUri', 'edit'].includes(k)) errors.push(`${path}: unexpected property ${k}`);
    }
    return;
  }

  if (op === 'delete_file') {
    if (typeof s.targetUri !== 'string' || !s.targetUri.startsWith('file://')) {
      errors.push(`${path}.targetUri must be a file:// URI`);
    }
    for (const k of Object.keys(s)) {
      if (!['id', 'op', 'targetUri'].includes(k)) errors.push(`${path}: unexpected property ${k}`);
    }
    return;
  }

  if (op === 'move_file') {
    if (typeof s.fromUri !== 'string' || !s.fromUri.startsWith('file://')) {
      errors.push(`${path}.fromUri must be a file:// URI`);
    }
    if (typeof s.toUri !== 'string' || !s.toUri.startsWith('file://')) {
      errors.push(`${path}.toUri must be a file:// URI`);
    }
    for (const k of Object.keys(s)) {
      if (!['id', 'op', 'fromUri', 'toUri'].includes(k)) errors.push(`${path}: unexpected property ${k}`);
    }
    return;
  }
}

module.exports = {
  WORKSPACE_PLAN_KIND,
  validateWorkspacePlan,
  formatPlanValidationForUser,
};
