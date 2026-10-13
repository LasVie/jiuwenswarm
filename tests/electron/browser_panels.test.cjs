const assert = require('node:assert/strict');
const { test } = require('node:test');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { panelIdentity, evictionCandidates, createTargetHandler, holdStatus, applyHoldDecision } = require('../../jiuwenswarm/channels/desktop/electron/browser_panels.cjs');
const { acquireTarget, filterServerMessage, blockedToolResponse } = require('../../jiuwenswarm/channels/desktop/electron/target_mcp_wrapper.cjs');

test('both Electron packagers include the browser panel runtime', () => {
  for (const script of ['build-electron-exe.ps1', 'build-electron-exe.sh']) {
    const source = fs.readFileSync(path.join(__dirname, '../../scripts', script), 'utf8');
    assert.match(source, /(?:Copy-Item|cp).*browser_panels\.cjs/);
  }
});

test('member/page identities do not collide across sessions or punctuation', () => {
  assert.equal(panelIdentity('session').panelId, 'session');
  const identities = [['a-b', 'c'], ['a', 'b-c'], ['a/b', 'c'], ['a_b', 'c']];
  assert.equal(new Set(identities.map(args => panelIdentity(...args).panelId)).size, 4);
  assert.deepEqual(panelIdentity(' one ', ' worker ', 'Worker'), panelIdentity('one', 'worker', 'Worker'));
});

function entry(extra = {}) {
  return { visible: false, creating: false, lastActive: 0, leases: new Map(), ...extra };
}

test('eviction skips hidden live MCP owners, including more than eight owners', () => {
  const views = new Map(Array.from({ length: 12 }, (_, i) => [String(i), entry({ leases: new Map([['lease', 42]]) })]));
  assert.deepEqual(evictionCandidates(views, 'new', '', () => true), []);
  views.set('idle', entry());
  views.set('selected', entry());
  views.set('visible', entry({ visible: true }));
  views.set('creating', entry({ creating: true }));
  assert.deepEqual(evictionCandidates(views, 'new', 'selected', () => true).map(([id]) => id), ['idle']);
});

test('dead owners are reclaimed, one live owner still protects a shared connection', () => {
  const page = entry({ leases: new Map([['dead', 1], ['live', 2]]) });
  const views = new Map([['page', page]]);
  assert.equal(evictionCandidates(views, '', '', pid => pid === 2).length, 0);
  assert.equal(page.leases.size, 1);
  page.leases.delete('live');
  assert.equal(evictionCandidates(views, '', '').length, 1);
});

test('SDK run-code tools are listed; close/install/tab management remain shell-owned', () => {
  const result = filterServerMessage({ result: { tools: ['browser_run_code_unsafe', 'browser_snapshot', 'browser_close', 'browser_tabs'].map(name => ({ name })) } });
  assert.deepEqual(result.result.tools.map(tool => tool.name), ['browser_run_code_unsafe', 'browser_snapshot', 'browser_run_code']);
  for (const name of ['browser_run_code', 'browser_run_code_unsafe']) {
    assert.equal(blockedToolResponse({ method: 'tools/call', params: { name } }), null);
  }
  assert.equal(blockedToolResponse({ method: 'tools/call', params: { name: 'browser_close' } }).result.isError, true);
});

test('MCP target acquisition/release is authenticated, lazy and member-scoped', async t => {
  const views = new Map();
  const server = http.createServer(createTargetHandler({
    token: 'test-token', getView: id => views.get(id), changed: () => {},
    ensureView: async (identity, lease) => {
      let view = views.get(identity.panelId);
      if (!view) {
        view = { ...entry(), ...identity, targetId: `target-${views.size}` };
        views.set(identity.panelId, view);
      }
      view.leases.set(lease.leaseId, lease.ownerPid);
      return view;
    },
  }));
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { server.close(resolve); server.closeAllConnections(); }));
  const base = `http://127.0.0.1:${server.address().port}`;
  const env = { PLAYWRIGHT_MCP_TARGET_RESOLVER: base, PLAYWRIGHT_MCP_SESSION_ID: 'session / one', PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN: 'test-token' };
  const one = await acquireTarget({ ...env, PLAYWRIGHT_MCP_MEMBER_ID: 'member-a' });
  const two = await acquireTarget({ ...env, PLAYWRIGHT_MCP_MEMBER_ID: 'member-b' });
  const repeat = await acquireTarget({ ...env, PLAYWRIGHT_MCP_MEMBER_ID: 'member-a' });
  assert.notEqual(one.targetId, two.targetId);
  assert.equal(one.targetId, repeat.targetId);
  const first = views.get(panelIdentity('session / one', 'member-a').panelId);
  assert.equal(first.leases.size, 2);
  await one.release();
  assert.equal(first.leases.size, 1);
  await repeat.release();
  await two.release();
  assert.equal(first.leases.size, 0);
  assert.equal((await fetch(`${base}/session`, { method: 'POST' })).status, 403);
  assert.equal((await fetch(`${base}/session?pid=1&lease=x`, { method: 'POST', headers: { authorization: 'Bearer test-token', origin: 'http://example.com' } })).status, 403);
  await assert.rejects(acquireTarget({ ...env, PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN: 'wrong' }), /403/);
  await assert.rejects(acquireTarget({ ...env, PLAYWRIGHT_MCP_SESSION_ID: '' }), /SESSION_ID/);
  await assert.rejects(acquireTarget({ ...env, PLAYWRIGHT_MCP_TARGET_RESOLVER: 'http://example.com' }), /loopback/);
});

test('OpenCLI worker pages get their own identity next to the member page', () => {
  const member = panelIdentity('s', 'm');
  const worker = panelIdentity('s', 'm', 'OpenCLI · m', 'opencli');
  assert.notEqual(worker.panelId, member.panelId);
  assert.equal(worker.role, 'opencli');
  assert.equal(member.role, undefined);
  assert.notEqual(panelIdentity('s', '', '', 'opencli').panelId, panelIdentity('s').panelId);
});

test('a hold is released only by the user decision on its own block, or by expiry', () => {
  const page = entry({ hold: { blockId: 'b1', state: 'pending', until: Date.now() + 60_000 } });
  assert.equal(holdStatus(page.hold), 'pending');
  assert.equal(applyHoldDecision(page, 'old-block', 'resolved'), false);
  assert.equal(applyHoldDecision(page, 'b1', 'bogus'), false);
  assert.equal(applyHoldDecision(page, 'b1', 'resolved'), true);
  assert.equal(holdStatus(page.hold), 'resolved');
  assert.equal(applyHoldDecision(page, 'b1', 'abandoned'), false);
  assert.equal(holdStatus({ blockId: 'x', state: 'pending', until: 1 }), 'expired');
});

test('held worker pages are never evicted; idle worker pages are evicted first', () => {
  const now = Date.now();
  const views = new Map([
    ['member', entry({ lastActive: 1 })],
    ['worker-idle', entry({ lastActive: 5, role: 'opencli' })],
    ['worker-held', entry({ role: 'opencli', hold: { blockId: 'b', state: 'pending', until: now + 60_000 } })],
  ]);
  assert.deepEqual(evictionCandidates(views, '', '', () => true, now).map(([id]) => id), ['worker-idle', 'member']);
});

test('worker page routes: ws endpoint, hold enforcement, reset and confirm', async t => {
  const views = new Map();
  const calls = { reset: 0, attention: 0, confirm: [] };
  let nextTarget = 0;
  const ensureView = async (identity, lease) => {
    let view = views.get(identity.panelId);
    if (!view) {
      view = { ...entry(), ...identity, targetId: `target-${nextTarget++}` };
      views.set(identity.panelId, view);
    }
    if (lease) view.leases.set(lease.leaseId, lease.ownerPid);
    return view;
  };
  const server = http.createServer(createTargetHandler({
    token: 'tk', getView: id => views.get(id), changed: () => {}, ensureView,
    pageEndpoint: targetId => `ws://127.0.0.1:9/devtools/page/${targetId}`,
    resetView: async identity => { calls.reset += 1; views.delete(identity.panelId); return ensureView(identity); },
    requestAttention: () => { calls.attention += 1; },
    requestConfirm: async (identity, request) => { calls.confirm.push(request); return 'approve'; },
  }));
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { server.close(resolve); server.closeAllConnections(); }));
  const base = `http://127.0.0.1:${server.address().port}/${encodeURIComponent('s 1')}`;
  const headers = { authorization: 'Bearer tk', 'content-type': 'application/json' };
  const query = 'member=m&role=opencli';
  const post = (suffix, params, body) => fetch(`${base}${suffix}?${params}`, { method: 'POST', headers, body: body && JSON.stringify(body) });

  const first = await (await post('', `${query}&lease=l1&pid=1`)).json();
  assert.equal(first.role, 'opencli');
  assert.equal(first.webSocketDebuggerUrl, `ws://127.0.0.1:9/devtools/page/${first.targetId}`);
  assert.equal((await post('/hold', query, { block_id: 'b1', reason: 'captcha', instructions: 'solve it', ttl_s: 600 })).status, 200);
  assert.equal(calls.attention, 1);

  const blocked = await post('', `${query}&lease=l2&pid=1`);
  assert.equal(blocked.status, 409);
  assert.deepEqual(await blocked.json(), { error: 'awaiting_user', reason: 'captcha', instructions: 'solve it' });

  const worker = views.get(first.panelId);
  assert.equal(applyHoldDecision(worker, 'b1', 'resolved'), true);
  const resumed = await (await post('', `${query}&lease=l3&pid=1`)).json();
  assert.equal(resumed.targetId, first.targetId, 'a resolved hold keeps the page the user worked on');
  assert.equal(views.get(first.panelId).hold, null);

  await post('/hold', query, { block_id: 'b2', ttl_s: 600 });
  applyHoldDecision(views.get(first.panelId), 'b2', 'abandoned');
  const replaced = await (await post('', `${query}&lease=l4&pid=1`)).json();
  assert.notEqual(replaced.targetId, first.targetId, 'an abandoned hold resets the page');
  assert.equal(calls.reset, 1);

  const reset = await (await post('/reset', query)).json();
  assert.match(reset.webSocketDebuggerUrl, /^ws:\/\/127\.0\.0\.1:9\/devtools\/page\/target-/);
  const decision = await (await post('/confirm', query, { command: 'site cmd', args: ['a=1'], warnings: ['w'], timeout_s: 30 })).json();
  assert.deepEqual(decision, { decision: 'approve' });
  assert.deepEqual(calls.confirm[0], { command: 'site cmd', args: ['a=1'], warnings: ['w'], timeoutMs: 30_000 });

  assert.equal((await fetch(`${base}/hold`, { method: 'POST', headers })).status, 404, 'actions need a worker role');
  assert.equal((await post('', 'role=other&lease=x&pid=1')).status, 400);
});
