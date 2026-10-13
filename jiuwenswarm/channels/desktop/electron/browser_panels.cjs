const { createHash } = require('node:crypto');

const SHARED_BROWSER_PARTITION = 'persist:jiuwenswarm-browser';
// OpenCLI runs on its own worker page in the same partition: it shares the
// login state with the Browser Agent page but never navigates that page.
const WORKER_ROLES = new Set(['opencli']);
const BODY_LIMIT_BYTES = 64 * 1024;
const HOLD_DECISIONS = new Set(['resolved', 'abandoned']);

function panelIdentity(sessionId, memberId = '', label = '', role = '') {
  const sid = String(sessionId || '').trim() || 'default';
  const member = String(memberId || '').trim();
  const kind = String(role || '').trim();
  let panelId = sid;
  if (kind) {
    panelId = `${kind}:${createHash('sha256').update(JSON.stringify([sid, member, kind])).digest('hex')}`;
  } else if (member) {
    panelId = `member:${createHash('sha256').update(JSON.stringify([sid, member])).digest('hex')}`;
  }
  const identity = { panelId, sessionId: sid, memberId: member, label: String(label || member).trim() };
  if (kind) identity.role = kind;
  return identity;
}

function processAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    // Permission errors must not turn a live owner's page into an eviction candidate.
    return error.code !== 'ESRCH';
  }
}

function hasLiveLease(entry, isAlive = processAlive) {
  for (const [id, pid] of entry.leases) {
    if (!isAlive(pid)) entry.leases.delete(id);
  }
  return entry.leases.size > 0;
}

// The user's decision on an "awaiting user" hold, or 'expired' / 'pending'.
function holdStatus(hold, now = Date.now()) {
  if (!hold) return null;
  if (HOLD_DECISIONS.has(hold.state)) return hold.state;
  return now > Number(hold.until || 0) ? 'expired' : 'pending';
}

function applyHoldDecision(entry, blockId, decision) {
  if (!entry?.hold || !HOLD_DECISIONS.has(decision)) return false;
  // A late click on an older block must not release a newer one.
  if (entry.hold.blockId !== blockId || holdStatus(entry.hold) !== 'pending') return false;
  entry.hold = { ...entry.hold, state: decision };
  return true;
}

function evictionCandidates(views, preserveId, activeId, isAlive = processAlive, now = Date.now()) {
  return [...views.entries()]
    .filter(([id, entry]) => id !== preserveId && id !== activeId && !entry.visible
      && !entry.creating && holdStatus(entry.hold, now) !== 'pending' && !hasLiveLease(entry, isAlive))
    // Idle worker pages carry no state worth keeping, so they go first.
    .sort(([, a], [, b]) => (WORKER_ROLES.has(b.role) - WORKER_ROLES.has(a.role)) || (a.lastActive - b.lastActive));
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', chunk => {
      size += chunk.length;
      if (size > BODY_LIMIT_BYTES) {
        reject(new Error('request body too large'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      if (!chunks.length) return resolve({});
      try {
        const parsed = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        resolve(parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

function createTargetHandler({
  token, ensureView, getView, changed,
  pageEndpoint = () => '', resetView = null, requestConfirm = null, requestAttention = () => {},
}) {
  return async (req, res) => {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    const reply = (status, body) => {
      res.statusCode = status;
      res.end(JSON.stringify(body));
    };
    // This endpoint is for local MCP clients, never browser-origin requests.
    if (req.headers.origin || req.headers.authorization !== `Bearer ${token}`) {
      reply(403, { error: 'browser target authorization required' });
      return;
    }
    try {
      const url = new URL(req.url || '/', 'http://127.0.0.1');
      const segments = url.pathname.replace(/^\/+/, '').split('/');
      const sessionId = decodeURIComponent(segments[0] || '');
      const action = segments[1] || '';
      if (!sessionId) return reply(400, { error: 'session id required' });
      const role = String(url.searchParams.get('role') || '').trim();
      if (role && !WORKER_ROLES.has(role)) return reply(400, { error: 'unsupported panel role' });
      if (action && !role) return reply(404, { error: 'unknown browser target action' });
      const identity = panelIdentity(sessionId, url.searchParams.get('member'), url.searchParams.get('label'), role);
      if (role) identity.visibility = url.searchParams.get('visibility') === 'hidden' ? 'hidden' : 'sidebar';

      if (action === 'hold') {
        if (req.method !== 'POST') return reply(405, { error: 'POST required' });
        const body = await readJsonBody(req);
        const entry = getView(identity.panelId);
        if (!entry) return reply(404, { error: 'worker page not found' });
        const ttlMs = Math.max(60, Math.min(Number(body.ttl_s) || 1800, 24 * 3600)) * 1000;
        entry.hold = {
          blockId: String(body.block_id || ''),
          state: 'pending',
          reason: String(body.reason || ''),
          instructions: String(body.instructions || ''),
          until: Date.now() + ttlMs,
        };
        changed();
        requestAttention(entry, 'human');
        return reply(200, { held: true, until: entry.hold.until });
      }
      if (action === 'reset') {
        if (req.method !== 'POST' || !resetView) return reply(405, { error: 'POST required' });
        const entry = await resetView(identity);
        if (!entry) return reply(503, { error: 'browser sideview disabled' });
        changed();
        return reply(200, { targetId: entry.targetId, webSocketDebuggerUrl: pageEndpoint(entry.targetId) });
      }
      if (action === 'confirm') {
        if (req.method !== 'POST' || !requestConfirm) return reply(405, { error: 'POST required' });
        const body = await readJsonBody(req);
        const decision = await requestConfirm(identity, {
          command: String(body.command || ''),
          args: Array.isArray(body.args) ? body.args.map(String) : [],
          warnings: Array.isArray(body.warnings) ? body.warnings.map(String) : [],
          timeoutMs: Math.max(5, Math.min(Number(body.timeout_s) || 90, 600)) * 1000,
        });
        return reply(200, { decision });
      }
      if (action) return reply(404, { error: 'unknown browser target action' });

      const leaseId = url.searchParams.get('lease');
      const ownerPid = Number(url.searchParams.get('pid'));
      if (!leaseId || !Number.isSafeInteger(ownerPid) || ownerPid <= 0) {
        return reply(400, { error: 'MCP lease and owner pid required' });
      }
      if (req.method === 'DELETE') {
        const entry = getView(identity.panelId);
        if (entry?.leases.get(leaseId) === ownerPid) {
          entry.leases.delete(leaseId);
          changed();
        }
        return reply(200, { released: true });
      }
      if (req.method !== 'POST') return reply(405, { error: 'POST or DELETE required' });
      if (role) {
        // The hold is enforced here, not by the caller: until the user decides
        // in the sidebar, no automatic task may take (and navigate) the page.
        const current = getView(identity.panelId);
        const status = holdStatus(current?.hold);
        if (status === 'pending') {
          return reply(409, {
            error: 'awaiting_user', reason: current.hold.reason, instructions: current.hold.instructions,
          });
        }
        if (status) {
          current.hold = null;
          if (status !== 'resolved' && resetView) await resetView(identity);
          changed();
        }
      }
      const entry = await ensureView(identity, { leaseId, ownerPid });
      if (!entry) return reply(503, { error: 'browser sideview disabled' });
      changed();
      const body = { ...identity, targetId: entry.targetId };
      if (role) body.webSocketDebuggerUrl = pageEndpoint(entry.targetId);
      return reply(200, body);
    } catch (error) {
      return reply(500, { error: String(error?.message || error) });
    }
  };
}

module.exports = {
  SHARED_BROWSER_PARTITION,
  WORKER_ROLES,
  panelIdentity,
  hasLiveLease,
  holdStatus,
  applyHoldDecision,
  evictionCandidates,
  createTargetHandler,
};
