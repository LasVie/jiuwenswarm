// OpenCLI worker page smoke test (WP0): a minimal Electron main with two pages
// in the shared browser partition, a local fixture site and fixture adapters.
//
// Part A drives the bundled OpenCLI directly (Electron Node mode, page-level
// CDP) to check upstream behaviour; part B runs opencli_smoke_driver.py, which
// goes through the real Python stack (runtime, source, tool, page slot) against
// the real createTargetHandler routes.
//
// Run from the Electron package directory: npm run test:opencli:smoke
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');
const { randomUUID } = require('node:crypto');

const REPO = path.resolve(__dirname, '..', '..');
const ELECTRON_DIR = path.join(REPO, 'jiuwenswarm', 'channels', 'desktop', 'electron');

// Started by plain Node, or with ELECTRON_RUN_AS_NODE inherited from an
// Electron-based editor: relaunch as a real Electron main process.
if (!process.versions.electron || process.env.ELECTRON_RUN_AS_NODE) {
  const electronBinary = require(require.resolve('electron', { paths: [ELECTRON_DIR] }));
  const env = { ...process.env };
  delete env.ELECTRON_RUN_AS_NODE;
  const relaunched = spawnSync(electronBinary, [__filename], { env, stdio: 'inherit' });
  process.exit(relaunched.status ?? 1);
}

const { app, BrowserWindow, WebContentsView } = require('electron');
const {
  SHARED_BROWSER_PARTITION, panelIdentity, createTargetHandler, applyHoldDecision,
} = require(path.join(ELECTRON_DIR, 'browser_panels.cjs'));

const PYTHON = process.env.SMOKE_PYTHON
  || path.join(REPO, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const DRIVER = path.join(__dirname, 'opencli_smoke_driver.py');
const DAEMON_PORT = 19825;
const WATCHDOG_MS = 8 * 60 * 1000;

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'opencli-smoke-'));
app.setPath('userData', path.join(tmpRoot, 'userData'));
app.commandLine.appendSwitch('remote-debugging-address', '127.0.0.1');
app.commandLine.appendSwitch('remote-debugging-port', '0');

const results = [];
function check(id, ok, detail = '') {
  results.push({ part: 'A', id, ok: Boolean(ok), detail });
  const text = typeof detail === 'string' ? detail : JSON.stringify(detail);
  console.log(`${ok ? 'PASS' : 'FAIL'} A:${id}${text ? ` - ${text}` : ''}`);
}
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// ---------------------------------------------------------------- fixture site

const fixture = { ticks: 0, posts: 0 };
let origin = '';
let win = null;
let cdpPort = 0;
const views = new Map();
const attention = [];
let confirmMode = 'approve';
let lastConfirm = null;

function parseCookies(header) {
  return Object.fromEntries(String(header || '').split(';')
    .map(part => part.trim().split('='))
    .filter(pair => pair[0]));
}

function viewState(entry) {
  const destroyed = entry.view.webContents.isDestroyed();
  return {
    panelId: entry.panelId,
    memberId: entry.memberId,
    role: entry.role || '',
    targetId: entry.targetId,
    url: destroyed ? '' : entry.view.webContents.getURL(),
    hold: entry.hold,
    leases: entry.leases.size,
    destroyed,
  };
}

function handleControl(url, reply) {
  const action = url.pathname.slice('/__control/'.length);
  if (action === 'state') {
    return reply(200, { views: [...views.values()].map(viewState), fixture, attention, lastConfirm });
  }
  if (action === 'confirm-mode') {
    confirmMode = url.searchParams.get('decision') || 'approve';
    return reply(200, { confirmMode });
  }
  if (action === 'decide') {
    const entry = views.get(url.searchParams.get('panelId'));
    const applied = applyHoldDecision(entry, url.searchParams.get('blockId'), url.searchParams.get('decision'));
    return reply(200, { applied });
  }
  return reply(404, { error: 'unknown control action' });
}

function startFixture() {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url || '/', 'http://127.0.0.1');
    const authed = parseCookies(req.headers.cookie).sid === 's3cret';
    const json = (status, body) => {
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(body));
    };
    const html = (body, headers = {}) => {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', ...headers });
      res.end(`<!doctype html><title>fixture</title><body>${body}</body>`);
    };
    if (url.pathname.startsWith('/__control/')) return handleControl(url, json);
    switch (url.pathname) {
      case '/login':
        return html('logged in', {
          'Set-Cookie': ['sid=s3cret; Path=/; HttpOnly; SameSite=Lax', 'visible=1; Path=/'],
        });
      case '/api/items':
        return authed
          ? json(200, { items: ['alpha', 'beta', 'gamma', 'delta'].map((title, index) => ({ title, rank: index + 1 })) })
          : json(401, { error: 'login required' });
      case '/api/public':
        return json(200, { items: [{ name: 'public-a' }, { name: 'public-b' }] });
      case '/api/post':
        if (req.method === 'POST' && authed) {
          fixture.posts += 1;
          return json(200, { id: fixture.posts });
        }
        return json(401, { error: 'login required' });
      case '/tick':
        fixture.ticks += 1;
        return json(200, {});
      default:
        return html(url.pathname);
    }
  });
  return new Promise(resolve => server.listen(0, '127.0.0.1', () => resolve(server)));
}

// Records everything that reaches the OpenCLI daemon port. An installed
// OpenCLI Chrome extension polls GET /ping here (with <all_urls> host
// permission it sends no Origin header); the CLI itself never requests /ping,
// which only the daemon serves. Everything else comes from the CLI.
const daemon = { hits: 0, available: false, log: [] };
const isExtensionPing = r => r.origin.startsWith('chrome-extension://') || (r.method === 'GET' && r.url === '/ping');
const cliRequests = since => daemon.log.slice(since).filter(r => !isExtensionPing(r));
const extensionRequests = since => daemon.log.slice(since).filter(isExtensionPing);
let running = '';
function startDaemonProbe() {
  const server = http.createServer((req, res) => {
    daemon.hits += 1;
    daemon.log.push({
      method: req.method, url: req.url, origin: req.headers.origin || '', userAgent: req.headers['user-agent'] || '',
      during: running || '(no command running)',
    });
    res.writeHead(503, { 'Content-Type': 'application/json' });
    res.end('{"error":"smoke daemon probe"}');
  });
  return new Promise((resolve, reject) => {
    // The no-CDP counterexample must never reach a daemon owned by the user.
    server.once('error', error => reject(new Error(`Cannot exclusively bind daemon probe port ${DAEMON_PORT}: ${error.message}`)));
    server.listen(DAEMON_PORT, '127.0.0.1', () => {
      daemon.available = true;
      resolve(server);
    });
  });
}

// ----------------------------------------------------------- fixture adapters

function writeAdapters(dir) {
  fs.mkdirSync(dir, { recursive: true });
  const header = [
    "import { cli, Strategy } from '@jackwener/opencli/registry';",
    "import { AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';",
    `const ORIGIN = ${JSON.stringify(origin)};`,
    `const browserCommand = { site: 'fixture', domain: '127.0.0.1', strategy: Strategy.COOKIE, browser: true, navigateBefore: ORIGIN + '/' };`,
    '',
  ].join('\n');
  const adapters = {
    read: `cli({ ...browserCommand, name: 'read', access: 'read', description: 'items behind the login cookie',
  args: [{ name: 'limit', type: 'int', default: 3 }], columns: ['title', 'rank'],
  func: async (page, kwargs) => {
    const res = await page.evaluate(\`async () => {
      const r = await fetch('/api/items', { credentials: 'include' });
      return { status: r.status, body: await r.json() };
    }\`);
    if (res.status === 401) throw new AuthRequiredError('127.0.0.1');
    return res.body.items.slice(0, kwargs.limit);
  } });`,
    public: `cli({ site: 'fixture', name: 'public', access: 'read', description: 'no browser', strategy: Strategy.PUBLIC,
  browser: false, args: [], columns: ['name'],
  func: async () => (await (await fetch(ORIGIN + '/api/public')).json()).items });`,
    write: `cli({ ...browserCommand, name: 'write', access: 'write', description: 'posts once',
  args: [{ name: 'text', type: 'str', required: true }], columns: ['status', 'id'],
  func: async (page) => {
    const res = await page.evaluate(\`async () => {
      const r = await fetch('/api/post', { method: 'POST', credentials: 'include' });
      return { status: r.status, body: await r.json() };
    }\`);
    if (res.status !== 200) throw new AuthRequiredError('127.0.0.1');
    return [{ status: 'posted', id: res.body.id }];
  } });`,
    'write-lost': `cli({ ...browserCommand, name: 'write-lost', access: 'write', description: 'posts, then fails',
  args: [{ name: 'text', type: 'str', required: true }], columns: ['status'],
  func: async (page) => {
    await page.evaluate(\`async () => { await fetch('/api/post', { method: 'POST', credentials: 'include' }); }\`);
    throw new CommandExecutionError('connection dropped after submit');
  } });`,
    captcha: `cli({ ...browserCommand, name: 'captcha', access: 'read', description: 'hits a captcha', args: [],
  func: async (page) => {
    await page.goto(ORIGIN + '/captcha');
    throw new AuthRequiredError('127.0.0.1', 'Captcha verification required');
  } });`,
    'empty-throw': `cli({ ...browserCommand, name: 'empty-throw', access: 'read', description: 'no rows', args: [],
  func: async () => { throw new EmptyResultError('fixture empty-throw'); } });`,
    'empty-return': `cli({ ...browserCommand, name: 'empty-return', access: 'read', description: 'no rows', args: [],
  func: async () => [] });`,
    echo: `cli({ site: 'fixture', name: 'echo', access: 'read', description: 'returns its arguments',
  strategy: Strategy.PUBLIC, browser: false, columns: ['query'],
  args: [
    { name: 'query', positional: true, required: true },
    { name: 'flag', type: 'boolean', default: false },
    { name: 'limit', type: 'int', default: 5 },
    { name: 'text', type: 'str' },
  ],
  func: async (kwargs) => [{ query: kwargs.query, flag: kwargs.flag, limit: kwargs.limit, text: kwargs.text ?? null }] });`,
    cookies: `cli({ ...browserCommand, name: 'cookies', access: 'read', description: 'cookies over CDP', args: [],
  columns: ['name', 'httpOnly'],
  func: async (page) => (await page.getCookies({ url: ORIGIN })).map(c => ({ name: c.name, httpOnly: c.httpOnly })) });`,
    slow: `cli({ ...browserCommand, name: 'slow', access: 'read', description: 'starts page activity, then waits',
  args: [],
  func: async (page) => {
    await page.evaluate(\`() => { setInterval(() => { fetch('/tick').catch(() => {}); }, 100); return true; }\`);
    await new Promise(resolve => setTimeout(resolve, 90000));
    return [];
  } });`,
  };
  for (const [name, body] of Object.entries(adapters)) {
    fs.writeFileSync(path.join(dir, `${name}.js`), `${header}${body}\n`);
  }
}

// ------------------------------------------------------------------- views

async function waitForCdpTarget(targetId) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    try {
      const response = await fetch(`http://127.0.0.1:${cdpPort}/json/list`);
      const targets = await response.json();
      if (targets.some(target => target.id === targetId)) return;
    } catch { /* not ready */ }
    await sleep(100);
  }
  throw new Error(`CDP target ${targetId} did not appear`);
}

async function ensureView(identity, lease = null) {
  let entry = views.get(identity.panelId);
  if (!entry || entry.view.webContents.isDestroyed()) {
    const view = new WebContentsView({
      webPreferences: {
        contextIsolation: true, nodeIntegration: false, sandbox: true, backgroundThrottling: false,
        partition: SHARED_BROWSER_PARTITION,
      },
    });
    win.contentView.addChildView(view);
    view.setBounds({ x: 0, y: 0, width: 1024, height: 768 });
    view.setVisible(false);
    entry = { ...identity, view, targetId: '', leases: new Map(), hold: null, visible: false, lastActive: Date.now() };
    views.set(identity.panelId, entry);
    await view.webContents.loadURL(`about:blank#jiuwen-session=${encodeURIComponent(identity.panelId)}`);
    entry.targetId = view.webContents.getOrCreateDevToolsTargetId();
    await waitForCdpTarget(entry.targetId);
  }
  if (lease) entry.leases.set(lease.leaseId, lease.ownerPid);
  return entry;
}

async function resetView(identity) {
  const existing = views.get(identity.panelId);
  if (existing) {
    views.delete(identity.panelId);
    win.contentView.removeChildView(existing.view);
    if (!existing.view.webContents.isDestroyed()) existing.view.webContents.close();
  }
  return ensureView(identity);
}

async function requestConfirm(_identity, request) {
  lastConfirm = { ...request };
  if (confirmMode === 'timeout') {
    await sleep(request.timeoutMs);
    return 'timeout';
  }
  await sleep(50);
  return confirmMode;
}

const pageEndpoint = targetId => `ws://127.0.0.1:${cdpPort}/devtools/page/${targetId}`;

function startTargetResolver(token) {
  const handler = createTargetHandler({
    token,
    ensureView,
    getView: panelId => views.get(panelId),
    changed: () => {},
    pageEndpoint,
    resetView,
    requestConfirm,
    requestAttention: (entry, kind) => attention.push({ panelId: entry.panelId, kind }),
  });
  const server = http.createServer(handler);
  return new Promise(resolve => server.listen(0, '127.0.0.1', () => resolve(server)));
}

// ------------------------------------------------------------ OpenCLI runs

const noNodePath = process.platform === 'win32' ? path.join(process.env.SystemRoot || 'C:\\Windows', 'System32') : '/nonexistent';

function killTree(pid) {
  if (process.platform === 'win32') spawnSync('taskkill', ['/T', '/F', '/PID', String(pid)], { windowsHide: true });
  else try { process.kill(pid, 'SIGKILL'); } catch { /* gone */ }
}

// Mirrors build_argv / build_env in jiuwenswarm/extensions/opencli/sources/opencli.py.
function runOpencli(cliPath, home, argv, { endpoint = '', timeoutMs = 60000, onSpawn = null } = {}) {
  const env = {
    SystemRoot: process.env.SystemRoot || '', WINDIR: process.env.WINDIR || '',
    TEMP: process.env.TEMP || os.tmpdir(), TMP: process.env.TMP || os.tmpdir(), PATH: noNodePath,
    ELECTRON_RUN_AS_NODE: '1', HOME: home, USERPROFILE: home,
    OPENCLI_CACHE_DIR: path.join(home, '..', 'cache'), OPENCLI_CONFIG_DIR: path.join(home, '.opencli'),
    OPENCLI_SITE_SESSION: 'ephemeral', NO_COLOR: '1',
  };
  if (endpoint) env.OPENCLI_CDP_ENDPOINT = endpoint;
  return new Promise(resolve => {
    const started = Date.now();
    const child = spawn(process.execPath, [cliPath, ...argv], { env, windowsHide: true });
    running = argv.slice(0, 2).join(' ');
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    const timer = setTimeout(() => killTree(child.pid), timeoutMs);
    child.on('close', code => {
      clearTimeout(timer);
      running = '';
      resolve({ code, stdout: stdout.trim(), stderr: stderr.trim(), ms: Date.now() - started });
    });
    if (onSpawn) onSpawn(child);
  });
}

const JSON_FLAGS = ['-f', 'json', '--trace', 'off'];
const BROWSER_FLAGS = [...JSON_FLAGS, '--site-session', 'ephemeral'];

function parseRows(stdout) {
  try { return JSON.parse(stdout); } catch { return null; }
}

function firstLine(text) {
  return String(text || '').split(/\r?\n/).find(line => line.trim()) || '';
}

async function partA(runtime) {
  const home = path.join(tmpRoot, 'home-a', 'home');
  writeAdapters(path.join(home, '.opencli', 'clis', 'fixture'));
  const run = (argv, options) => runOpencli(runtime.cli_path, home, argv, options);

  const whereNode = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['node'], {
    env: { ...process.env, PATH: noNodePath }, windowsHide: true,
  });
  const version = await run(['--version']);
  check('electron-node-mode', version.code === 0 && version.stdout === runtime.version && whereNode.status !== 0,
    { exit: version.code, stdout: version.stdout, nodeOnPath: whereNode.status === 0, ms: version.ms });

  const agent = await ensureView(panelIdentity('smoke', 'researcher'));
  const workerIdentity = panelIdentity('smoke', 'researcher', 'OpenCLI · researcher', 'opencli');
  let worker = await ensureView(workerIdentity);
  await agent.view.webContents.loadURL(`${origin}/login`);
  await agent.view.webContents.loadURL(`${origin}/agent-page`);
  const agentUrl = agent.view.webContents.getURL();

  const hitsBefore = daemon.hits;
  const read = await run(['fixture', 'read', '--limit', '3', ...BROWSER_FLAGS], { endpoint: pageEndpoint(worker.targetId) });
  const rows = parseRows(read.stdout);
  check('page-cdp-read-shares-httponly-cookie',
    read.code === 0 && Array.isArray(rows) && rows.map(row => row.title).join(',') === 'alpha,beta,gamma',
    { exit: read.code, rows, stderr: firstLine(read.stderr), ms: read.ms });
  check('no-cross-navigation',
    agent.view.webContents.getURL() === agentUrl && worker.view.webContents.getURL().startsWith(origin),
    { agent: agent.view.webContents.getURL(), worker: worker.view.webContents.getURL() });

  const cookies = await run(['fixture', 'cookies', ...BROWSER_FLAGS], { endpoint: pageEndpoint(worker.targetId) });
  const cookieRows = parseRows(cookies.stdout) || [];
  check('network-getcookies-over-page-cdp', cookieRows.some(row => row.name === 'sid' && row.httpOnly === true),
    { exit: cookies.code, rows: cookieRows, stderr: firstLine(cookies.stderr) });

  // Argument syntax: how values reach the adapter.
  const echo = async (label, argv, expected) => {
    const result = await run(['fixture', 'echo', ...argv]);
    const row = (parseRows(result.stdout) || [])[0] || null;
    const ok = result.code === 0 && row && Object.entries(expected).every(([key, value]) => row[key] === value);
    check(label, ok,
      { argv, exit: result.code, row, matches: Boolean(ok), stderr: firstLine(result.stderr) });
  };
  await echo('args-space-separated', ['hello', '--flag', 'true', '--limit', '3', '--text', 'abc', ...JSON_FLAGS],
    { query: 'hello', flag: true, limit: 3, text: 'abc' });
  await echo('args-bool-false-space', ['hello', '--flag', 'false', ...JSON_FLAGS], { flag: false });
  await echo('args-dash-value-space', ['q', '--text', '-5', ...JSON_FLAGS], { text: '-5' });
  const bareDash = await run(['fixture', 'echo', '-dash', ...JSON_FLAGS]);
  check('args-dash-positional-bare-rejected', bareDash.code !== 0 && bareDash.stderr.includes('unknown option'),
    {exit: bareDash.code, stderr: firstLine(bareDash.stderr)});
  await echo('args-equals-form', ['q', '--text=-5', '--flag=false', '--limit=3', ...JSON_FLAGS],
    { query: 'q', text: '-5', flag: false, limit: 3 });
  await echo('args-equals-bool-true', ['q', '--flag=true', ...JSON_FLAGS], { flag: true });
  await echo('args-positional-after-double-dash', ['--text=x', ...JSON_FLAGS, '--', '-dash'], { query: '-dash', text: 'x' });
  await echo('args-value-with-spaces-and-equals', ['--text=a b=c', ...JSON_FLAGS, '--', 'x y'], { query: 'x y', text: 'a b=c' });

  const postsBefore = fixture.posts;
  const write = await run(['fixture', 'write', '--text', 'hello', ...BROWSER_FLAGS], { endpoint: pageEndpoint(worker.targetId) });
  check('ephemeral-write-runs', write.code === 0 && fixture.posts === postsBefore + 1,
    { exit: write.code, stdout: write.stdout, stderr: firstLine(write.stderr) });
  if (daemon.available) {
    check('ephemeral-read-write-no-daemon', cliRequests(hitsBefore).length === 0,
      { cli: cliRequests(hitsBefore), extensionPings: extensionRequests(hitsBefore).length });
    const persistentBefore = daemon.hits;
    const persistent = await run(['fixture', 'write', '--text', 'x', ...JSON_FLAGS, '--site-session', 'persistent'],
      { endpoint: pageEndpoint(worker.targetId) });
    check('persistent-write-contacts-daemon (probe control)', cliRequests(persistentBefore).length > 0,
      { exit: persistent.code, cli: cliRequests(persistentBefore), ms: persistent.ms });
  } else throw new Error('Daemon isolation probe is not active');

  const publicRun = await run(['fixture', 'public', ...JSON_FLAGS]);
  check('browser-free-without-site-session', publicRun.code === 0 && parseRows(publicRun.stdout)?.length === 2,
    { exit: publicRun.code, stderr: firstLine(publicRun.stderr) });
  const publicFlag = await run(['fixture', 'public', ...BROWSER_FLAGS]);
  check('browser-free-rejects-site-session', publicFlag.code !== 0,
    { exit: publicFlag.code, stderr: firstLine(publicFlag.stderr) });

  const endpoint = pageEndpoint(worker.targetId);
  const captcha = await run(['fixture', 'captcha', ...BROWSER_FLAGS], { endpoint });
  check('auth-required-exit-77', captcha.code === 77 && /code:\s*AUTH_REQUIRED/.test(captcha.stderr),
    { exit: captcha.code, stderr: captcha.stderr.slice(0, 300) });
  const emptyThrow = await run(['fixture', 'empty-throw', ...BROWSER_FLAGS], { endpoint });
  check('empty-result-exit-66', emptyThrow.code === 66, { exit: emptyThrow.code, stderr: firstLine(emptyThrow.stderr) });
  const emptyReturn = await run(['fixture', 'empty-return', ...BROWSER_FLAGS], { endpoint });
  check('empty-rows-exit', emptyReturn.code === 0 && Array.isArray(parseRows(emptyReturn.stdout))
    && parseRows(emptyReturn.stdout).length === 0, { exit: emptyReturn.code, stdout: emptyReturn.stdout.slice(0, 80) });
  const badArg = await run(['fixture', 'read', '--limit', 'abc', ...BROWSER_FLAGS], { endpoint });
  check('invalid-arg-exit-2', badArg.code === 2, { exit: badArg.code, stderr: firstLine(badArg.stderr) });
  const unknown = await run(['fixture', 'nope', ...JSON_FLAGS]);
  check('unknown-command-exit (recorded)', unknown.code !== 0, { exit: unknown.code, stderr: firstLine(unknown.stderr) });
  const noEndpoint = await run(['fixture', 'read', ...BROWSER_FLAGS]);
  check('browser-command-without-endpoint (recorded)', noEndpoint.code !== 0,
    { exit: noEndpoint.code, stderr: firstLine(noEndpoint.stderr), daemonHits: daemon.hits });

  // Kill the CLI while the adapter's page script is running.
  fixture.ticks = 0;
  let child = null;
  const slow = run(['fixture', 'slow', ...BROWSER_FLAGS], { endpoint, onSpawn: spawned => { child = spawned; } });
  for (let i = 0; i < 200 && fixture.ticks === 0; i += 1) await sleep(100);
  const startedTicks = fixture.ticks > 0;
  killTree(child.pid);
  const killed = await slow;
  await sleep(300);
  const t0 = fixture.ticks;
  await sleep(1500);
  const t1 = fixture.ticks;
  check('kill-leaves-page-activity-running', startedTicks && t1 > t0,
    { exit: killed.code, ticksAfterKill: t1 - t0 });
  check('worker-and-agent-survive-ws-close',
    !worker.view.webContents.isDestroyed() && agent.view.webContents.getURL() === agentUrl,
    { workerUrl: worker.view.webContents.getURL() });
  const again = await run(['fixture', 'read', ...BROWSER_FLAGS], { endpoint });
  check('same-page-reusable-after-kill', again.code === 0, { exit: again.code, stderr: firstLine(again.stderr) });

  const oldTarget = worker.targetId;
  worker = await resetView(workerIdentity);
  await sleep(300);
  const t2 = fixture.ticks;
  await sleep(1500);
  const t3 = fixture.ticks;
  check('reset-stops-page-activity', worker.targetId !== oldTarget && t3 === t2,
    { oldTarget, newTarget: worker.targetId, ticksAfterReset: t3 - t2 });
  const stale = await run(['fixture', 'read', ...BROWSER_FLAGS], { endpoint: pageEndpoint(oldTarget), timeoutMs: 30000 });
  check('stale-endpoint-fails (recorded)', stale.code !== 0, { exit: stale.code, stderr: firstLine(stale.stderr), ms: stale.ms });
  const fresh = await run(['fixture', 'read', ...BROWSER_FLAGS], { endpoint: pageEndpoint(worker.targetId) });
  check('reset-page-keeps-login', fresh.code === 0, { exit: fresh.code, stderr: firstLine(fresh.stderr) });
  await resetView(workerIdentity);
}

// ----------------------------------------------------------------- driver

function runDriver(mode, env) {
  return new Promise(resolve => {
    const child = spawn(PYTHON, ['-W', 'ignore::SyntaxWarning', DRIVER, mode], {
      cwd: REPO, env: { ...process.env, ...env }, windowsHide: true,
    });
    let stdout = '';
    child.stdout.on('data', chunk => {
      stdout += chunk;
      if (mode === 'run') process.stdout.write(chunk);
    });
    child.stderr.on('data', chunk => process.stderr.write(chunk));
    child.on('close', code => resolve({ code, stdout }));
  });
}

async function main() {
  const watchdog = setTimeout(() => {
    console.error('smoke watchdog fired');
    app.exit(3);
  }, WATCHDOG_MS);
  await app.whenReady();
  win = new BrowserWindow({ show: false, width: 1200, height: 800 });
  const portFile = path.join(app.getPath('userData'), 'DevToolsActivePort');
  for (let i = 0; i < 100 && !fs.existsSync(portFile); i += 1) await sleep(100);
  cdpPort = Number(fs.readFileSync(portFile, 'utf8').split(/\r?\n/)[0]);

  const fixtureServer = await startFixture();
  origin = `http://127.0.0.1:${fixtureServer.address().port}`;
  const daemonServer = await startDaemonProbe();
  const token = randomUUID();
  const resolverServer = await startTargetResolver(token);
  const adapters = path.join(tmpRoot, 'adapters');
  writeAdapters(adapters);

  const agentCore = path.resolve(REPO, '..', 'agent-core');
  const driverEnv = {
    SMOKE_ELECTRON: process.execPath,
    SMOKE_WORKSPACE: path.join(tmpRoot, 'workspace'),
    SMOKE_ADAPTERS: adapters,
    SMOKE_RESOLVER: `http://127.0.0.1:${resolverServer.address().port}`,
    SMOKE_TOKEN: token,
    SMOKE_CONTROL: `${origin}/__control`,
    PYTHONPATH: [REPO, fs.existsSync(agentCore) ? agentCore : ''].filter(Boolean).join(path.delimiter),
  };
  let failed = false;
  const prepared = await runDriver('prepare', driverEnv);
  let runtime = null;
  try { runtime = JSON.parse(prepared.stdout.trim().split(/\r?\n/).pop()); } catch { /* reported below */ }
  if (prepared.code !== 0 || !runtime) {
    console.log(`FAIL prepare_runtime - exit ${prepared.code}: ${prepared.stdout.slice(-500)}`);
    failed = true;
  } else {
    console.log(`runtime ${runtime.version}, Electron Node ${runtime.node_version}, cli ${runtime.cli_path}`);
    console.log(`Electron ${process.versions.electron}, Chromium ${process.versions.chrome}`);
    try {
      await partA(runtime);
    } catch (error) {
      check('part-a-crashed', false, String(error?.stack || error));
    }
    fixture.ticks = 0;
    const driver = await runDriver('run', driverEnv);
    if (driver.code !== 0) failed = true;
  }
  failed = failed || results.some(result => !result.ok);
  fs.writeFileSync(path.join(tmpRoot, 'part-a.json'), JSON.stringify({ results, daemon: daemon.log }, null, 2));
  const pings = extensionRequests(0);
  if (pings.length) console.log(`note: ${pings.length} request(s) on ${DAEMON_PORT} came from the OpenCLI Chrome extension (${pings[0].userAgent || pings[0].origin})`);
  console.log(`\n${failed ? 'SMOKE FAILED' : 'SMOKE PASSED'} (artifacts: ${tmpRoot})`);
  clearTimeout(watchdog);
  for (const server of [fixtureServer, daemonServer, resolverServer]) server?.close();
  app.exit(failed ? 1 : 0);
}

app.on('window-all-closed', () => {});
main().catch(error => {
  console.error(error);
  app.exit(2);
});
