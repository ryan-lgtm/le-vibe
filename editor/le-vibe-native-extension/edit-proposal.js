'use strict';

/**
 * Parse and validate `levibe.edit_proposal.v1` payloads (see `schemas/levibe.edit-proposal.v1.json`).
 * Pure JS — no external JSON Schema engine (keeps the extension dependency-free).
 */

const KIND = 'levibe.edit_proposal.v1';

/**
 * @param {unknown} raw
 * @returns {{ ok: true, value: object } | { ok: false, errors: string[] }}
 */
function validateEditProposal(raw) {
  const errors = [];
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) {
    return { ok: false, errors: ['root must be a non-null object'] };
  }
  const o = /** @type {Record<string, unknown>} */ (raw);

  if (o.kind !== KIND) {
    errors.push(`kind must be "${KIND}"`);
  }

  if (!Array.isArray(o.proposals) || o.proposals.length < 1) {
    errors.push('proposals must be a non-empty array');
  } else {
    o.proposals.forEach((p, i) => {
      validateFileEdit(p, `proposals[${i}]`, errors);
    });
  }

  if ('rationale' in o) {
    if (typeof o.rationale !== 'string') {
      errors.push('rationale must be a string when present');
    } else if (o.rationale.length > 16000) {
      errors.push('rationale exceeds maxLength 16000');
    }
  }

  if ('confidence' in o && o.confidence !== undefined) {
    validateConfidence(o.confidence, 'confidence', errors);
  }

  const allowed = new Set(['kind', 'proposals', 'rationale', 'confidence']);
  for (const k of Object.keys(o)) {
    if (!allowed.has(k)) errors.push(`unexpected property: ${k}`);
  }

  if (errors.length) return { ok: false, errors };

  return {
    ok: true,
    value: {
      kind: KIND,
      proposals: o.proposals,
      ...(typeof o.rationale === 'string' ? { rationale: o.rationale } : {}),
      ...(o.confidence && typeof o.confidence === 'object' && !Array.isArray(o.confidence)
        ? { confidence: o.confidence }
        : {}),
    },
  };
}

/**
 * Convert parse/validation failures into a deterministic, user-visible string.
 * @param {string[]} errors
 * @returns {string}
 */
function formatEditProposalValidationForUser(errors) {
  if (!Array.isArray(errors) || errors.length === 0) {
    return 'Lé Vibe Chat: edit proposal invalid — unknown validation error.';
  }
  const detail = errors.slice(0, 6).join('; ');
  const suffix = errors.length > 6 ? ` (+${errors.length - 6} more)` : '';
  return `Lé Vibe Chat: edit proposal invalid — ${detail}${suffix}`;
}

/**
 * @param {unknown} c
 * @param {string} path
 * @param {string[]} errors
 */
function validateConfidence(c, path, errors) {
  if (c === null || typeof c !== 'object' || Array.isArray(c)) {
    errors.push(`${path} must be an object`);
    return;
  }
  const o = /** @type {Record<string, unknown>} */ (c);
  if ('score' in o) {
    if (typeof o.score !== 'number' || Number.isNaN(o.score)) {
      errors.push(`${path}.score must be a number`);
    } else if (o.score < 0 || o.score > 1) {
      errors.push(`${path}.score must be between 0 and 1`);
    }
  }
  if ('flags' in o) {
    if (!Array.isArray(o.flags)) {
      errors.push(`${path}.flags must be an array of strings`);
    } else {
      const flagRe = /^[a-z][a-z0-9_]{0,63}$/;
      o.flags.forEach((f, i) => {
        if (typeof f !== 'string' || !flagRe.test(f)) {
          errors.push(`${path}.flags[${i}] must match /^[a-z][a-z0-9_]{0,63}$/`);
        }
      });
    }
  }
  for (const k of Object.keys(o)) {
    if (k !== 'score' && k !== 'flags') errors.push(`${path}: unexpected property ${k}`);
  }
}

/**
 * @param {unknown} p
 * @param {string} path
 * @param {string[]} errors
 */
function validateFileEdit(p, path, errors) {
  if (p === null || typeof p !== 'object' || Array.isArray(p)) {
    errors.push(`${path} must be an object`);
    return;
  }
  const o = /** @type {Record<string, unknown>} */ (p);

  if (typeof o.targetUri !== 'string' || o.targetUri.length < 8 || !o.targetUri.startsWith('file://')) {
    errors.push(`${path}.targetUri must be a file:// URI string`);
  }

  if (o.edit === null || typeof o.edit !== 'object' || Array.isArray(o.edit)) {
    errors.push(`${path}.edit must be an object`);
    return;
  }
  const edit = /** @type {Record<string, unknown>} */ (o.edit);

  if (edit.kind === 'full_file') {
    if (typeof edit.content !== 'string') errors.push(`${path}.edit.content must be a string for full_file`);
    for (const k of Object.keys(edit)) {
      if (k !== 'kind' && k !== 'content') errors.push(`${path}.edit: unexpected property ${k}`);
    }
  } else if (edit.kind === 'range_replace') {
    if (typeof edit.newText !== 'string') errors.push(`${path}.edit.newText must be a string`);
    validateRange(edit.range, `${path}.edit.range`, errors);
    for (const k of Object.keys(edit)) {
      if (!['kind', 'range', 'newText'].includes(k)) errors.push(`${path}.edit: unexpected property ${k}`);
    }
  } else {
    errors.push(`${path}.edit.kind must be "range_replace" or "full_file"`);
  }

  for (const k of Object.keys(o)) {
    if (k !== 'targetUri' && k !== 'edit') errors.push(`${path}: unexpected property ${k}`);
  }
}

/**
 * @param {unknown} r
 * @param {string} path
 * @param {string[]} errors
 */
function validateRange(r, path, errors) {
  if (r === null || typeof r !== 'object' || Array.isArray(r)) {
    errors.push(`${path} must be an object`);
    return;
  }
  const o = /** @type {Record<string, unknown>} */ (r);
  const start = validatePosition(o.start, `${path}.start`, errors);
  const end = validatePosition(o.end, `${path}.end`, errors);
  if (start && end && !rangeOrderingOk(start, end)) {
    errors.push(`${path}: start must be before or equal to end (line/character order)`);
  }
  for (const k of Object.keys(o)) {
    if (k !== 'start' && k !== 'end') errors.push(`${path}: unexpected property ${k}`);
  }
}

/**
 * @param {unknown} pos
 * @param {string} path
 * @param {string[]} errors
 * @returns {{ line: number, character: number } | null}
 */
function validatePosition(pos, path, errors) {
  if (pos === null || typeof pos !== 'object' || Array.isArray(pos)) {
    errors.push(`${path} must be an object`);
    return null;
  }
  const o = /** @type {Record<string, unknown>} */ (pos);
  if (typeof o.line !== 'number' || !Number.isInteger(o.line) || o.line < 0) {
    errors.push(`${path}.line must be a non-negative integer`);
    return null;
  }
  if (typeof o.character !== 'number' || !Number.isInteger(o.character) || o.character < 0) {
    errors.push(`${path}.character must be a non-negative integer`);
    return null;
  }
  for (const k of Object.keys(o)) {
    if (k !== 'line' && k !== 'character') errors.push(`${path}: unexpected property ${k}`);
  }
  return { line: o.line, character: o.character };
}

/**
 * @param {{ line: number, character: number }} a
 * @param {{ line: number, character: number }} b
 */
function rangeOrderingOk(a, b) {
  if (a.line < b.line) return true;
  if (a.line > b.line) return false;
  return a.character <= b.character;
}

module.exports = {
  EDIT_PROPOSAL_KIND: KIND,
  validateEditProposal,
  formatEditProposalValidationForUser,
};
