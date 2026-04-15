'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { levibeNativeChatDir } = require('./storage-inventory');
const { WORKSPACE_PLAN_KIND } = require('./workspace-plan.js');
const {
  applyEditProposalBatchAsWorkspaceEdit,
  applyFullFileAsSingleWorkspaceEdit,
} = require('./workspace-edit-apply.js');
const { EDIT_PROPOSAL_KIND } = require('./edit-proposal.js');

/**
 * @typedef {object} RollbackInverse
 * @property {'delete_file'|'write_full'|'move_file'} op
 * @property {string} [targetUri]
 * @property {string} [content]
 * @property {string} [fromUri]
 * @property {string} [toUri]
 */

function workspacePlanAuditPath() {
  return path.join(levibeNativeChatDir(), 'workspace-plan-audit.jsonl');
}

/**
 * @param {string} auditPath
 * @param {object} record
 */
function appendWorkspacePlanAuditLine(auditPath, record) {
  const dir = path.dirname(auditPath);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(auditPath, `${JSON.stringify(record)}\n`, 'utf8');
}

/**
 * @param {number} stepIndex 0-based
 * @param {number} totalSteps
 * @param {string} op
 * @param {string} pathLabel workspace-relative or fs path
 * @param {'running'|'done'|'failed'|'cancelled'} status
 * @returns {string}
 */
function formatWorkspacePlanProgressStatus(stepIndex, totalSteps, op, pathLabel, status) {
  const n = stepIndex + 1;
  const m = totalSteps;
  const p = String(pathLabel || '—');
  return `Lé Vibe Chat: plan step ${n}/${m} — ${op} — ${p} — ${status}`;
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder | undefined} folder
 * @param {string} uriStr
 */
function pathLabelForStep(vscode, folder, uriStr) {
  try {
    const u = vscode.Uri.parse(uriStr);
    if (folder) {
      return vscode.workspace.asRelativePath(u, false);
    }
    return u.fsPath;
  } catch {
    return uriStr;
  }
}

/**
 * @param {object} params
 * @returns {object}
 */
function buildRollbackAuditRecord(params) {
  return {
    contract_version: 'lvibe.workspace_plan_audit.v1',
    event_type: 'workspace_plan_rollback',
    timestamp_iso: new Date().toISOString(),
    workspace_uri: params.workspaceUri || 'no-workspace',
    plan_kind: WORKSPACE_PLAN_KIND,
    steps_undone: params.stepsUndone,
    local_only: true,
  };
}

function buildAuditRecord(params) {
  return {
    contract_version: 'lvibe.workspace_plan_audit.v1',
    event_type: 'workspace_plan_step',
    timestamp_iso: new Date().toISOString(),
    workspace_uri: params.workspaceUri || 'no-workspace',
    plan_kind: WORKSPACE_PLAN_KIND,
    step_index: params.stepIndex,
    step_total: params.stepTotal,
    step_id: params.stepId,
    op: params.op,
    path: params.pathLabel,
    phase: params.phase,
    run_cancelled: Boolean(params.runCancelled),
    error: params.error || undefined,
    local_only: true,
  };
}

/**
 * Capture workspace state immediately before a plan step mutates the tree.
 *
 * @param {import('vscode')} vscode
 * @param {object} step
 * @returns {Promise<object>}
 */
async function capturePreStepSnapshot(vscode, step) {
  if (step.op === 'create_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    try {
      const bytes = await vscode.workspace.fs.readFile(uri);
      return { kind: 'create_file', hadFile: true, priorUtf8: Buffer.from(bytes).toString('utf8') };
    } catch {
      return { kind: 'create_file', hadFile: false };
    }
  }
  if (step.op === 'apply_edit') {
    const uri = vscode.Uri.parse(step.targetUri);
    try {
      const bytes = await vscode.workspace.fs.readFile(uri);
      return { kind: 'apply_edit', hadFile: true, priorUtf8: Buffer.from(bytes).toString('utf8') };
    } catch {
      return { kind: 'apply_edit', hadFile: false };
    }
  }
  if (step.op === 'delete_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    try {
      const bytes = await vscode.workspace.fs.readFile(uri);
      return { kind: 'delete_file', priorUtf8: Buffer.from(bytes).toString('utf8') };
    } catch {
      return { kind: 'delete_file', noop: true };
    }
  }
  if (step.op === 'move_file') {
    return { kind: 'move_file' };
  }
  throw new Error(`unsupported op: ${step.op}`);
}

/**
 * Build one inverse WorkspaceEdit-worth of semantics to undo a successful step (best-effort).
 *
 * @param {object} step
 * @param {object} snapshot
 * @returns {RollbackInverse | null}
 */
function inverseAfterSuccessfulStep(step, snapshot) {
  if (step.op === 'create_file') {
    if (snapshot.kind !== 'create_file') {
      return null;
    }
    if (!snapshot.hadFile) {
      return { op: 'delete_file', targetUri: step.targetUri };
    }
    return { op: 'write_full', targetUri: step.targetUri, content: snapshot.priorUtf8 };
  }
  if (step.op === 'apply_edit') {
    if (snapshot.kind !== 'apply_edit') {
      return null;
    }
    if (!snapshot.hadFile) {
      return { op: 'delete_file', targetUri: step.targetUri };
    }
    return { op: 'write_full', targetUri: step.targetUri, content: snapshot.priorUtf8 };
  }
  if (step.op === 'delete_file') {
    if (snapshot.kind !== 'delete_file' || snapshot.noop) {
      return null;
    }
    return { op: 'write_full', targetUri: step.targetUri, content: snapshot.priorUtf8 };
  }
  if (step.op === 'move_file') {
    return { op: 'move_file', fromUri: step.toUri, toUri: step.fromUri };
  }
  return null;
}

/**
 * Apply rollback inverses in reverse order (LIFO). Best-effort; stops on first error.
 *
 * @param {import('vscode')} vscode
 * @param {RollbackInverse[]} inverses
 * @param {object} [opts]
 * @param {string} [opts.auditPath]
 * @param {string} [opts.workspaceUriStr]
 * @returns {Promise<{ ok: true } | { ok: false, error: string, applied: number }>}
 */
async function applyWorkspacePlanRollbackInverses(vscode, inverses, opts = {}) {
  const auditPath = opts.auditPath || workspacePlanAuditPath();
  const workspaceUriStr = opts.workspaceUriStr || 'no-workspace';
  const list = inverses.slice();
  let applied = 0;
  for (let k = list.length - 1; k >= 0; k -= 1) {
    const inv = list[k];
    try {
      await applyOneRollbackInverse(vscode, inv);
      applied += 1;
    } catch (e) {
      const msg = e && e.message ? e.message : String(e);
      return { ok: false, error: msg, applied };
    }
  }
  appendWorkspacePlanAuditLine(auditPath, buildRollbackAuditRecord({ workspaceUri: workspaceUriStr, stepsUndone: applied }));
  return { ok: true };
}

/**
 * @param {import('vscode')} vscode
 * @param {RollbackInverse} inv
 */
async function applyOneRollbackInverse(vscode, inv) {
  if (inv.op === 'delete_file') {
    const uri = vscode.Uri.parse(inv.targetUri);
    const we = new vscode.WorkspaceEdit();
    we.deleteFile(uri, { recursive: false, ignoreIfNotExists: true });
    const ok = await vscode.workspace.applyEdit(we);
    if (!ok) {
      throw new Error('rollback delete_file applyEdit returned false');
    }
    return;
  }
  if (inv.op === 'write_full') {
    const uri = vscode.Uri.parse(inv.targetUri);
    const text = typeof inv.content === 'string' ? inv.content : '';
    const ok = await applyFullFileAsSingleWorkspaceEdit(vscode, uri, text);
    if (!ok) {
      throw new Error('rollback write_full applyEdit returned false');
    }
    return;
  }
  if (inv.op === 'move_file') {
    const from = vscode.Uri.parse(inv.fromUri);
    const to = vscode.Uri.parse(inv.toUri);
    const we = new vscode.WorkspaceEdit();
    if (typeof we.renameFile === 'function') {
      we.renameFile(from, to, { overwrite: false });
      const ok = await vscode.workspace.applyEdit(we);
      if (!ok) {
        throw new Error('rollback move renameFile applyEdit returned false');
      }
      return;
    }
    await vscode.workspace.fs.rename(from, to, { overwrite: false });
    return;
  }
  throw new Error(`unsupported rollback op: ${inv.op}`);
}

/**
 * @param {import('vscode')} vscode
 * @param {object} planValue validated workspace plan
 * @param {object} opts
 * @param {import('vscode').WorkspaceFolder | undefined} opts.workspaceFolder
 * @param {string} opts.workspaceUriStr
 * @param {(statusLine: string) => void} [opts.onProgress]
 * @param {() => boolean} [opts.shouldCancel]
 * @param {string} [opts.auditPath]
 * @param {number} [opts.failStepAtIndex] test-only: throw before executing this 0-based step (after snapshot)
 * @returns {Promise<
 *   | { ok: true, completedSteps: number, cancelled: boolean }
 *   | { ok: false, error: string, completedSteps: number, rollbackInverses?: RollbackInverse[] }
 * >}
 */
async function executeValidatedWorkspacePlan(vscode, planValue, opts) {
  const auditPath = opts.auditPath || workspacePlanAuditPath();
  const wf = opts.workspaceFolder;
  const workspaceUriStr = opts.workspaceUriStr || (wf ? wf.uri.toString() : 'no-workspace');
  const onProgress = typeof opts.onProgress === 'function' ? opts.onProgress : () => {};
  const shouldCancel = typeof opts.shouldCancel === 'function' ? opts.shouldCancel : () => false;

  const steps = planValue.steps;
  const total = steps.length;
  /** @type {RollbackInverse[]} */
  const rollbackInverses = [];

  const logAudit = (partial) => {
    appendWorkspacePlanAuditLine(
      auditPath,
      buildAuditRecord({
        workspaceUri: workspaceUriStr,
        stepIndex: partial.stepIndex,
        stepTotal: total,
        stepId: partial.stepId,
        op: partial.op,
        pathLabel: partial.pathLabel,
        phase: partial.phase,
        runCancelled: partial.runCancelled,
        error: partial.error,
      }),
    );
  };

  for (let i = 0; i < total; i++) {
    if (shouldCancel()) {
      logAudit({
        stepIndex: i,
        stepId: steps[i].id,
        op: steps[i].op,
        pathLabel: pathLabelForStep(vscode, wf, primaryUriForStep(steps[i])),
        phase: 'cancelled',
        runCancelled: true,
      });
      onProgress(
        `Lé Vibe Chat: plan run cancelled after ${i}/${total} step(s) — no further steps executed.`,
      );
      return { ok: true, completedSteps: i, cancelled: true };
    }

    const step = steps[i];
    const pathLabel = pathLabelForStep(vscode, wf, primaryUriForStep(step));
    onProgress(formatWorkspacePlanProgressStatus(i, total, step.op, pathLabel, 'running'));
    logAudit({
      stepIndex: i,
      stepId: step.id,
      op: step.op,
      pathLabel,
      phase: 'start',
      runCancelled: false,
    });

    let snapshot;
    try {
      snapshot = await capturePreStepSnapshot(vscode, step);
    } catch (snapErr) {
      const msg = snapErr && snapErr.message ? snapErr.message : String(snapErr);
      logAudit({
        stepIndex: i,
        stepId: step.id,
        op: step.op,
        pathLabel,
        phase: 'failed',
        runCancelled: false,
        error: msg,
      });
      onProgress(`Lé Vibe Chat: plan step failed (before apply) — ${step.op} — ${pathLabel} — ${msg}`);
      return { ok: false, error: msg, completedSteps: i, rollbackInverses };
    }

    try {
      if (typeof opts.failStepAtIndex === 'number' && opts.failStepAtIndex === i) {
        throw new Error(
          typeof opts.failStepMessage === 'string' ? opts.failStepMessage : 'injected plan failure',
        );
      }
      await runOneStep(vscode, step);
      onProgress(formatWorkspacePlanProgressStatus(i, total, step.op, pathLabel, 'done'));
      logAudit({
        stepIndex: i,
        stepId: step.id,
        op: step.op,
        pathLabel,
        phase: 'completed',
        runCancelled: false,
      });
      const inv = inverseAfterSuccessfulStep(step, snapshot);
      if (inv) {
        rollbackInverses.push(inv);
      }
    } catch (e) {
      const msg = e && e.message ? e.message : String(e);
      logAudit({
        stepIndex: i,
        stepId: step.id,
        op: step.op,
        pathLabel,
        phase: 'failed',
        runCancelled: false,
        error: msg,
      });
      onProgress(`Lé Vibe Chat: plan step failed — ${step.op} — ${pathLabel} — ${msg}`);
      onProgress(
        rollbackInverses.length
          ? `Lé Vibe Chat: plan stopped in a partial state — ${rollbackInverses.length} prior step(s) succeeded. Click Undo completed steps in the panel to best-effort revert those writes (same session).`
          : 'Lé Vibe Chat: plan failed on the first step — nothing to roll back.',
      );
      return { ok: false, error: msg, completedSteps: i, rollbackInverses };
    }
  }

  onProgress(`Lé Vibe Chat: plan finished — ${total}/${total} step(s) completed.`);
  return { ok: true, completedSteps: total, cancelled: false };
}

/**
 * @param {object} step
 */
function primaryUriForStep(step) {
  if (step.op === 'move_file') return step.fromUri;
  return step.targetUri;
}

/**
 * @param {import('vscode')} vscode
 * @param {object} step
 */
async function runOneStep(vscode, step) {
  if (step.op === 'create_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    const content = typeof step.content === 'string' ? step.content : '';
    const ok = await applyFullFileAsSingleWorkspaceEdit(vscode, uri, content);
    if (!ok) {
      throw new Error('WorkspaceEdit apply returned false');
    }
    return;
  }
  if (step.op === 'apply_edit') {
    const proposal = {
      kind: EDIT_PROPOSAL_KIND,
      proposals: [{ targetUri: step.targetUri, edit: step.edit }],
    };
    const ok = await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
    if (!ok) {
      throw new Error('WorkspaceEdit apply returned false');
    }
    return;
  }
  if (step.op === 'delete_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    const we = new vscode.WorkspaceEdit();
    we.deleteFile(uri, { recursive: false, ignoreIfNotExists: true });
    const ok = await vscode.workspace.applyEdit(we);
    if (!ok) {
      throw new Error('deleteFile applyEdit returned false');
    }
    return;
  }
  if (step.op === 'move_file') {
    const from = vscode.Uri.parse(step.fromUri);
    const to = vscode.Uri.parse(step.toUri);
    const we = new vscode.WorkspaceEdit();
    if (typeof we.renameFile === 'function') {
      we.renameFile(from, to, { overwrite: false });
      const ok = await vscode.workspace.applyEdit(we);
      if (!ok) {
        throw new Error('renameFile applyEdit returned false');
      }
      return;
    }
    await vscode.workspace.fs.rename(from, to, { overwrite: false });
    return;
  }
  throw new Error(`unsupported op: ${step.op}`);
}

module.exports = {
  workspacePlanAuditPath,
  appendWorkspacePlanAuditLine,
  formatWorkspacePlanProgressStatus,
  pathLabelForStep,
  buildAuditRecord,
  buildRollbackAuditRecord,
  capturePreStepSnapshot,
  inverseAfterSuccessfulStep,
  applyWorkspacePlanRollbackInverses,
  executeValidatedWorkspacePlan,
};
