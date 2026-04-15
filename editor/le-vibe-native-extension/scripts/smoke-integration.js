#!/usr/bin/env node
'use strict';

/**
 * Integration smoke (task-n6-2): no VS Code host required.
 * - Verifies readiness webview HTML is never blank for every startup state + wizard.
 * - Probes local Ollama using the same client as the extension (optional strict fail).
 * - When run from the r-vibe monorepo, verifies the `lvibe` launcher script matches `lvibe .` entry.
 *
 * Env:
 * - LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1 — exit 1 if Ollama is unreachable (local dev with Ollama CI).
 * - LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1 — skip packaging/bin/lvibe check (extension-only trees).
 */

const fs = require('node:fs');
const path = require('node:path');

const { STARTUP_STATES } = require('../readiness');
const { createOllamaClient } = require('../ollama');
const ext = require('../extension');

const MIN_HTML = 400;

function assertNonBlankPanel() {
  for (const state of STARTUP_STATES) {
    const html = ext.panelHtml(state);
    if (!html || html.length < MIN_HTML) {
      throw new Error(`panelHtml(${state}) too short or empty (${html ? html.length : 0} chars)`);
    }
    if (!html.includes('Lé Vibe Native Startup')) {
      throw new Error(`panelHtml(${state}) missing Lé Vibe Native Startup marker`);
    }
    if (!html.includes(`<strong>${state}</strong>`)) {
      throw new Error(`panelHtml(${state}) missing state marker`);
    }
    if (!html.includes('Send Prompt') || !html.includes('Cancel Request')) {
      throw new Error(`panelHtml(${state}) missing chat controls`);
    }
  }
  for (let step = 0; step <= 3; step += 1) {
    const w = ext.firstRunWizardHtml(step);
    if (!w || w.length < MIN_HTML) {
      throw new Error(`firstRunWizardHtml(${step}) too short`);
    }
    const branded = w.includes('Lé Vibe') || w.includes('Checkpoint');
    if (!branded || !w.includes('wizSkip')) {
      throw new Error(`firstRunWizardHtml(${step}) missing wizard markers`);
    }
  }
}

async function smokeOllama() {
  const strict = process.env.LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA === '1';
  const endpoint = process.env.LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT || 'http://127.0.0.1:11434';
  const timeoutMs = Number(process.env.LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS || 2500);
  const client = createOllamaClient({
    endpoint,
    timeoutMs,
    maxRetries: 0,
    retryDelayMs: 100,
  });
  try {
    const health = await client.probeHealth();
    console.log(`smoke: Ollama wiring OK at ${endpoint} (modelCount: ${health.modelCount})`);
    return true;
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);
    console.error(`smoke: Ollama probe failed: ${msg}`);
    if (strict) {
      console.error('smoke: set LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=0 (unset) to allow skip when Ollama is down.');
      throw err;
    }
    console.log('smoke: Ollama unreachable — skipped (non-strict; expected in CI without daemon)');
    return false;
  }
}

function smokeLvibeLauncher() {
  if (process.env.LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER === '1') {
    console.log('smoke: lvibe launcher check skipped (LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1)');
    return true;
  }
  const repoRoot = path.join(__dirname, '..', '..', '..');
  const lvibe = path.join(repoRoot, 'packaging', 'bin', 'lvibe');
  if (!fs.existsSync(lvibe)) {
    console.log(`smoke: packaging/bin/lvibe not found at ${lvibe} — skip launcher contract (extension-only tree)`);
    return true;
  }
  const text = fs.readFileSync(lvibe, 'utf8');
  if (!text.includes('python3 -m le_vibe.launcher')) {
    throw new Error('packaging/bin/lvibe must exec python3 -m le_vibe.launcher (lvibe . contract)');
  }
  if (!text.includes('exec python3')) {
    throw new Error('packaging/bin/lvibe expected to exec python3 launcher');
  }
  console.log(`smoke: lvibe launcher contract OK (${lvibe}) — opens editor workspace (e.g. lvibe .)`);
  return true;
}

async function main() {
  console.log('smoke: Lé Vibe native extension integration smoke');
  assertNonBlankPanel();
  console.log('smoke: panel + wizard HTML non-blank checks OK');
  await smokeOllama();
  smokeLvibeLauncher();
  console.log('smoke: done');
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
