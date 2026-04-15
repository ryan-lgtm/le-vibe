'use strict';

const { pathLabelForStep } = require('./workspace-plan-exec.js');

/** Default cap on dry-run chat lines (bounded UX). */
const DEFAULT_MAX_OUTPUT_LINES = 48;

/** Skip reading files larger than this for range_replace / delete estimates (bounded I/O). */
const MAX_READ_BYTES = 512 * 1024;

/**
 * Rough token proxy: UTF-8 bytes / 4 (bounded; not a tokenizer).
 *
 * @param {number} utf8Bytes
 * @returns {number}
 */
function roughTokenEstimate(utf8Bytes) {
  const b = Math.max(0, Math.floor(utf8Bytes));
  return Math.min(Math.ceil(b / 4), 2_000_000);
}

/**
 * @param {object} step
 * @returns {string}
 */
function primaryUriForStep(step) {
  if (step.op === 'move_file') {
    return step.fromUri;
  }
  return step.targetUri;
}

/**
 * @param {import('vscode')} vscode
 * @param {object} step
 * @param {import('vscode').WorkspaceFolder | undefined} wf
 * @param {number} stepIndex
 * @param {number} total
 * @param {string} pathLabel
 * @returns {Promise<{ line: string, estimatedBytes: number }>}
 */
async function estimateOneStep(vscode, step, wf, stepIndex, total, pathLabel) {
  const n = stepIndex + 1;
  const m = total;
  const prefix = `Lé Vibe Chat: plan dry-run ${n}/${m} — ${step.op} — ${pathLabel} —`;

  if (step.op === 'create_file') {
    const b = Buffer.byteLength(typeof step.content === 'string' ? step.content : '', 'utf8');
    return {
      line: `${prefix} would write ~${b} B (~${roughTokenEstimate(b)} tok est.)`,
      estimatedBytes: b,
    };
  }

  if (step.op === 'apply_edit') {
    const uri = vscode.Uri.parse(step.targetUri);
    const ed = step.edit;
    if (ed.kind === 'full_file') {
      let before = 0;
      try {
        const buf = await vscode.workspace.fs.readFile(uri);
        before = buf.length;
        if (before > MAX_READ_BYTES) {
          const after = Buffer.byteLength(ed.content || '', 'utf8');
          const est = Math.max(before, after);
          return {
            line: `${prefix} would replace whole file — large on-disk file (>${MAX_READ_BYTES} B read skipped); ~${est} B upper bound (~${roughTokenEstimate(est)} tok est.)`,
            estimatedBytes: est,
          };
        }
      } catch {
        before = 0;
      }
      const after = Buffer.byteLength(ed.content || '', 'utf8');
      const est = Math.max(before, after);
      return {
        line: `${prefix} would replace whole file ~${est} B affected (~${roughTokenEstimate(est)} tok est.)`,
        estimatedBytes: est,
      };
    }
    if (ed.kind === 'range_replace') {
      const newB = Buffer.byteLength(ed.newText || '', 'utf8');
      try {
        const doc = await vscode.workspace.openTextDocument(uri);
        const start = new vscode.Position(ed.range.start.line, ed.range.start.character);
        const end = new vscode.Position(ed.range.end.line, ed.range.end.character);
        const oldSlice = doc.getText(new vscode.Range(start, end));
        const oldB = Buffer.byteLength(oldSlice, 'utf8');
        const est = oldB + newB;
        return {
          line: `${prefix} would range_replace ~${est} B net (~${roughTokenEstimate(est)} tok est.)`,
          estimatedBytes: est,
        };
      } catch {
        return {
          line: `${prefix} would range_replace ~${newB} B new text (file missing or unreadable; lower bound) (~${roughTokenEstimate(newB)} tok est.)`,
          estimatedBytes: newB,
        };
      }
    }
    return {
      line: `${prefix} unknown edit kind (no estimate)`,
      estimatedBytes: 0,
    };
  }

  if (step.op === 'delete_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    try {
      const buf = await vscode.workspace.fs.readFile(uri);
      if (buf.length > MAX_READ_BYTES) {
        return {
          line: `${prefix} would delete file (>${MAX_READ_BYTES} B; size not fully read) — at least ~${MAX_READ_BYTES} B removed`,
          estimatedBytes: MAX_READ_BYTES,
        };
      }
      const b = buf.length;
      return {
        line: `${prefix} would delete ~${b} B (~${roughTokenEstimate(b)} tok est.)`,
        estimatedBytes: b,
      };
    } catch {
      return {
        line: `${prefix} would delete (file missing — no-op)`,
        estimatedBytes: 0,
      };
    }
  }

  if (step.op === 'move_file') {
    const toLabel = pathLabelForStep(vscode, wf, step.toUri);
    return {
      line: `${prefix} would move → ${toLabel} (~0 B net; metadata path change)`,
      estimatedBytes: 0,
    };
  }

  return {
    line: `${prefix} unsupported op`,
    estimatedBytes: 0,
  };
}

/**
 * Produce human-readable dry-run lines without writing to disk (reads allowed for sizing).
 *
 * @param {import('vscode')} vscode
 * @param {object} planValue validated workspace plan
 * @param {object} opts
 * @param {import('vscode').WorkspaceFolder | undefined} opts.workspaceFolder
 * @param {number} [opts.maxOutputLines]
 * @returns {Promise<{ lines: string[], totalEstimatedBytes: number, totalEstimatedTokens: number, truncated: boolean }>}
 */
async function dryRunValidatedWorkspacePlan(vscode, planValue, opts) {
  const wf = opts.workspaceFolder;
  const maxLines = Math.max(
    8,
    typeof opts.maxOutputLines === 'number' ? opts.maxOutputLines : DEFAULT_MAX_OUTPUT_LINES,
  );
  const steps = planValue.steps;
  const lines = [];
  let totalEstimatedBytes = 0;
  let truncated = false;

  lines.push('Lé Vibe Chat: plan dry-run (no disk writes) — rough byte/token estimates follow.');

  for (let i = 0; i < steps.length; i++) {
    if (lines.length >= maxLines - 1) {
      truncated = true;
      break;
    }
    const step = steps[i];
    const uriStr = primaryUriForStep(step);
    const pathLabel = pathLabelForStep(vscode, wf, uriStr);
    const row = await estimateOneStep(vscode, step, wf, i, steps.length, pathLabel);
    lines.push(row.line);
    totalEstimatedBytes += row.estimatedBytes;
  }

  if (truncated) {
    lines.push(`Lé Vibe Chat: plan dry-run — output truncated (cap ${maxLines} lines).`);
  }

  const totalEstimatedTokens = roughTokenEstimate(totalEstimatedBytes);
  lines.push(
    `Lé Vibe Chat: plan dry-run summary — ~${totalEstimatedBytes} B rough max touched, ~${totalEstimatedTokens} tok est., 0 disk writes.`,
  );

  return { lines, totalEstimatedBytes, totalEstimatedTokens, truncated };
}

module.exports = {
  DEFAULT_MAX_OUTPUT_LINES,
  MAX_READ_BYTES,
  roughTokenEstimate,
  dryRunValidatedWorkspacePlan,
};
