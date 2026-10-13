// Real main.cjs page management + preload + React prompts + Python tools + bundled CLI.
// All traffic and writes are restricted to a local fixture, in an isolated profile.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const readline = require('node:readline');
const { spawn, execFileSync } = require('node:child_process');

const repo = path.resolve(__dirname, '../..');
const frontend = path.join(repo, 'jiuwenswarm/channels/web/frontend');
const desktop = path.join(repo, 'jiuwenswarm/channels/desktop/electron');
const manifest = JSON.parse(fs.readFileSync(path.join(repo, 'jiuwenswarm/resources/runtime/playwright-mcp/manifest.json')));
const modules = process.env.SWARM_TEST_MODULES || path.join(os.homedir(), '.jiuwenswarm/runtime/playwright-mcp',
  manifest.version, manifest.archive_sha256.slice(0, 12), 'node_modules');
if (!fs.existsSync(path.join(modules, 'playwright'))) {
  throw new Error('Materialize the pinned Playwright MCP runtime, or set SWARM_TEST_MODULES to its node_modules.');
}
const { _electron } = require(path.join(modules, 'playwright'));
const { build } = require(path.join(frontend, 'node_modules/esbuild'));
const electronExe = require(path.join(desktop, 'node_modules/electron'));
const python = path.join(repo, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const driverPath = path.join(__dirname, 'opencli_worker_page_driver.py');
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'swarm-opencli-worker-'));
const workspace = path.join(scratch, 'workspace');
const children = new Set();
const checks = [];
const snapshots = [];
const realSite = process.argv.includes('--real-site');
const settingsChecks = process.argv.includes('--settings');
const pythonEnv = { ...process.env, PYTHONPATH: [repo, path.join(repo, '../agent-core'), process.env.PYTHONPATH]
  .filter(Boolean).join(path.delimiter), SMOKE_ELECTRON: electronExe, SMOKE_WORKSPACE: workspace };

function passed(name) {
  checks.push(name);
  console.log(`PASS: ${name}`);
}

function jsonLinesDriver(env) {
  const child = spawn(python, ['-W', 'ignore::SyntaxWarning', driverPath, 'serve'], {
    cwd: repo, env, windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'],
  });
  children.add(child);
  let sequence = 0;
  let stderr = '';
  const waiting = new Map();
  child.stderr.on('data', chunk => { stderr += chunk; fs.appendFileSync(path.join(scratch, 'driver.log'), chunk); });
  readline.createInterface({ input: child.stdout }).on('line', line => {
    let response;
    try { response = JSON.parse(line); } catch { fs.appendFileSync(path.join(scratch, 'driver.log'), `${line}\n`); return; }
    const pending = waiting.get(response.id);
    if (!pending) return;
    clearTimeout(pending.timer);
    waiting.delete(response.id);
    if (response.error) pending.reject(new Error(response.error));
    else pending.resolve(response);
  });
  const fail = error => {
    for (const pending of waiting.values()) { clearTimeout(pending.timer); pending.reject(error); }
    waiting.clear();
  };
  child.on('error', fail);
  child.on('exit', code => fail(new Error(`Python driver exited ${code}: ${stderr.slice(-3000)}`)));
  const request = (action, params = {}) => {
    const id = ++sequence;
    const promise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => { waiting.delete(id); reject(new Error(`Driver request ${id} timed out: ${stderr.slice(-2000)}`)); }, 100000);
      waiting.set(id, { resolve, reject, timer });
      child.stdin.write(`${JSON.stringify({ id, action, ...params })}\n`);
    });
    return { id, promise };
  };
  return { request, call: async (action, params) => (await request(action, params).promise).data };
}

function writeAdapters(home, origin) {
  const dir = path.join(home, '.opencli/clis/fixture');
  fs.mkdirSync(dir, { recursive: true });
  const header = `import {cli, Strategy} from '@jackwener/opencli/registry';
import {AuthRequiredError, CommandExecutionError} from '@jackwener/opencli/errors';
const ORIGIN = ${JSON.stringify(origin)};
const command = {site:'fixture', domain:'127.0.0.1', strategy:Strategy.COOKIE, browser:true,
  navigateBefore:ORIGIN+'/worker', args:[]};\n`;
  const post = `await page.evaluate(async () => {
    const response = await fetch('/api/post', {method:'POST', credentials:'include'});
    if (!response.ok) throw new Error('fixture write failed');
    return response.json();
  });`;
  const slow = `await page.evaluate(() => {
    setInterval(() => { fetch('/tick').catch(() => {}); }, 100); return true;
  }); await new Promise(resolve => setTimeout(resolve, 90000));`;
  const adapters = {
    read: `cli({...command,name:'read',access:'read',description:'shared cookie read',columns:['title','rank'],
      args:[{name:'page',type:'int',default:1}],
      func:async (page, args) => {
        const result = await page.evaluate(async pageNum => {
          const response = await fetch('/api/items?page='+pageNum, {credentials:'include'});
          return {status:response.status, body:await response.json()};
        }, args.page);
        if (result.status !== 200) throw new AuthRequiredError('127.0.0.1');
        return result.body.items;
      }});`,
    write: `cli({...command,name:'write',access:'write',description:'fixture write',columns:['status'],
      func:async page => {${post} return [{status:'posted'}];}});`,
    'write-lost': `cli({...command,name:'write-lost',access:'write',description:'unknown write',
      func:async page => {${post} throw new CommandExecutionError('connection dropped after submit');}});`,
    'write-slow': `cli({...command,name:'write-slow',access:'write',description:'cancelled write',
      func:async page => {${post} ${slow} return [];}});`,
    slow: `cli({...command,name:'slow',access:'read',description:'timed out read',
      func:async page => {${slow} return [];}});`,
    captcha: `cli({...command,name:'captcha',access:'read',description:'captcha hold',
      func:async page => {await page.goto(ORIGIN+'/captcha');
        throw new AuthRequiredError('127.0.0.1','Captcha verification required');}});`,
  };
  for (const [name, body] of Object.entries(adapters)) fs.writeFileSync(path.join(dir, `${name}.js`), header + body);
}

async function until(probe, message, timeout = 15000) {
  const deadline = Date.now() + timeout;
  do {
    const value = await probe();
    if (value) return value;
    await new Promise(resolve => setTimeout(resolve, 50));
  } while (Date.now() < deadline);
  throw new Error(message);
}

async function main() {
  const { transform } = require(path.join(frontend, 'node_modules/@svgr/core'));
  const jsxPlugin = require(path.join(frontend, 'node_modules/@svgr/plugin-jsx'));
  await build({ entryPoints: [path.join(__dirname, 'opencli_worker_page_fixture.tsx')], bundle: true,
    outfile: path.join(scratch, 'ui.js'), jsx: 'automatic', absWorkingDir: frontend,
    nodePaths: [path.join(frontend, 'node_modules')],
    loader: { '.svg': 'dataurl', '.png': 'dataurl', '.woff2': 'dataurl', '.woff': 'dataurl', '.ttf': 'dataurl' },
    define: { 'process.env.NODE_ENV': '"development"', 'import.meta.env': '{}' },
    plugins: [{ name: 'fixture-react-svg', setup(builder) {
      builder.onResolve({ filter: /\.svg\?react$/ }, args => ({
        path: path.resolve(args.resolveDir, args.path.slice(0, -6)), namespace: 'react-svg',
      }));
      builder.onLoad({ filter: /.*/, namespace: 'react-svg' }, async args => ({
        contents: await transform(fs.readFileSync(args.path, 'utf8'),
          { plugins: [jsxPlugin.default || jsxPlugin], jsxRuntime: 'automatic' }, { componentName: 'SvgIcon' }),
        loader: 'jsx', resolveDir: path.dirname(args.path),
      }));
    } }],
  });
  let posts = 0;
  let ticks = 0;
  const itemPages = [];
  let driver;
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://fixture');
    if (url.pathname === '/settings') {
      const chunks = [];
      req.on('data', chunk => chunks.push(chunk));
      req.on('end', async () => {
        res.setHeader('Content-Type', 'application/json');
        try {
          const request = JSON.parse(Buffer.concat(chunks).toString('utf8'));
          const result = await driver.call('config', request);
          return res.end(JSON.stringify(result.payload));
        } catch (error) {
          res.statusCode = 500;
          return res.end(JSON.stringify({ error: String(error.message) }));
        }
      });
      return;
    }
    if (url.pathname === '/ui.js' || url.pathname === '/ui.css') {
      res.setHeader('Content-Type', url.pathname.endsWith('.js') ? 'text/javascript' : 'text/css');
      return res.end(fs.readFileSync(path.join(scratch, url.pathname.slice(1))));
    }
    if (url.pathname.startsWith('/api/') || url.pathname === '/tick') {
      res.setHeader('Content-Type', 'application/json');
      if (url.pathname === '/tick') { ticks += 1; return res.end('{}'); }
      if (!String(req.headers.cookie).includes('server-login=synthetic-account')) {
        res.statusCode = 401; return res.end('{}');
      }
      if (url.pathname === '/api/post') {
        if (req.method !== 'POST') { res.statusCode = 405; return res.end('{}'); }
        posts += 1; return res.end(JSON.stringify({ id: posts }));
      }
      if (url.pathname === '/api/items') itemPages.push(Number(url.searchParams.get('page')));
      return res.end(JSON.stringify({ items: [{ title: 'First item', rank: 1 }, { title: 'Second item', rank: 2 }] }));
    }
    res.setHeader('Content-Type', 'text/html');
    if (url.pathname === '/') return res.end(`<!doctype html><html data-theme="default" data-color-mode="light">
      <head><title>OpenCLI worker UI fixture</title><link rel="stylesheet" href="/ui.css"><style>
      body{margin:0;font-family:var(--font-body);color:var(--color-text-primary);background:var(--color-surface-page)}
      #root,.fixture-shell{display:flex;height:100vh;width:100%}.fixture-controls{width:150px;flex-shrink:0;padding:12px;box-sizing:border-box}output{display:block;overflow-wrap:anywhere}
      .fixture-shell--settings{flex-direction:column}.fixture-shell--settings>.fixture-controls{width:100%;display:flex;gap:8px;padding:4px 12px}.fixture-shell--settings>.fixture-controls output{display:none}
      .fixture-shell--settings>.settings-page{flex:1;min-height:0}
      .desktop-browser-pane{flex:1;min-width:0}button{color:inherit;font-family:inherit}
      </style></head><body><div id="root"></div><script src="/ui.js"></script></body></html>`);
    if (url.pathname === '/login') {
      res.setHeader('Set-Cookie', 'server-login=synthetic-account; Path=/; Max-Age=3600; HttpOnly; SameSite=Lax');
    }
    if (url.pathname === '/captcha') return res.end(`<!doctype html><title>Fixture verification</title><h1>Verification required</h1>
      <button onclick="document.cookie='verified=yes; Path=/';document.querySelector('h1').textContent='Verification completed'">Solve fixture</button>`);
    res.end('<!doctype html><title>Fixture page</title><h1>Local fixture page</h1>');
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const portServer = http.createServer();
  await new Promise(resolve => portServer.listen(0, '127.0.0.1', resolve));
  const cdpPort = portServer.address().port;
  await new Promise(resolve => portServer.close(resolve));
  let electron;
  try {
    const launchEnv = { ...process.env, SWARM_TEST_PROFILE: path.join(scratch, 'profile'),
      SWARM_TEST_URL: base, JIUWENSWARM_ELECTRON_CDP_PORT: String(cdpPort) };
    // Never accept an inherited broad allow-list in the default fixture run.
    launchEnv.SWARM_TEST_ALLOW_HOSTS = realSite ? 'bilibili.com,hdslb.com,biliapi.net,bilivideo.com,biliimg.com' : '';
    delete launchEnv.ELECTRON_RUN_AS_NODE;
    electron = await _electron.launch({ executablePath: electronExe,
      args: [path.join(__dirname, 'browser_fixture.cjs')], env: launchEnv, timeout: 30000 });
    const ui = await electron.firstWindow();
    await ui.getByTestId('fixture-other-tab').waitFor();
    const payload = await electron.evaluate(() => global.browserTest.endpoints);
    const prepared = execFileSync(python, ['-W', 'ignore::SyntaxWarning', driverPath, 'prepare'], {
      cwd: repo, env: pythonEnv, encoding: 'utf8', windowsHide: true, timeout: 30000,
    });
    const runtime = JSON.parse(prepared.trim().split(/\r?\n/).at(-1));
    writeAdapters(runtime.home_dir, base);
    driver = jsonLinesDriver({ ...pythonEnv, PYTHONIOENCODING: 'utf-8', SMOKE_RESOLVER: payload.target_resolver,
      SMOKE_TOKEN: payload.env_json.PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN,
      SMOKE_CDP_ENDPOINT: payload.cdp_endpoint, SMOKE_MCP_WRAPPER: path.join(desktop, 'target_mcp_wrapper.cjs'),
      SMOKE_FIXTURE_ORIGIN: base,
      SMOKE_MCP_PATH: `${path.join(modules, '.bin')}${path.delimiter}${process.env.PATH}` });
    await electron.evaluate(async (_, base) => {
      const entry = await global.browserTest.ensureBrowserView('session-one');
      await entry.view.webContents.loadURL(`${base}/login`);
      await entry.view.webContents.loadURL(`${base}/agent`);
    }, base);
    const state = () => electron.evaluate(() => [...global.browserTest.browserViews.values()].map(entry => ({
      panelId: entry.panelId, targetId: entry.targetId, role: entry.role || 'agent',
      url: entry.view.webContents.getURL(), hold: entry.hold, leases: entry.leases.size,
      visible: entry.visible, label: entry.label,
    })));
    const worker = async () => (await state()).find(entry => entry.role === 'opencli');
    const shot = async (name, captureWorker = true) => {
      // Use Electron's capture API for both WebContents. CDP renderer captures
      // timed out after native view switches despite the UI being interactive.
      const rendererImage = await electron.evaluate(async ({ BrowserWindow }) =>
        (await BrowserWindow.getAllWindows()[0].webContents.capturePage()).toPNG().toString('base64'));
      const file = path.join(scratch, `${name}.png`);
      fs.writeFileSync(file, Buffer.from(rendererImage, 'base64')); snapshots.push(file);
      if (!captureWorker) return;
      // Renderer screenshots omit the native WebContentsView. Capture its
      // pixels separately to verify the actual page, not its placeholder.
      const pageImage = await electron.evaluate(async () => {
        const entry = [...global.browserTest.browserViews.values()].find(entry => entry.role === 'opencli');
        if (!entry?.visible) throw new Error('the worker page was not revealed');
        return (await entry.view.webContents.capturePage()).toPNG().toString('base64');
      });
      const workerFile = path.join(scratch, `${name}-page.png`);
      fs.writeFileSync(workerFile, Buffer.from(pageImage, 'base64')); snapshots.push(workerFile);
    };
    const confirm = async command => {
      const request = driver.request('run', { command });
      await ui.getByTestId('desktop-browser-opencli-confirm').waitFor();
      return request;
    };
    const described = await driver.call('describe');
    assert.equal(described.commands.length, 6);
    assert.equal((await state()).length, 1);
    passed('describe does not create a worker page');
    const read = await driver.call('run', { command: 'read' });
    assert.equal(read.reason, 'ok'); assert.equal(read.observed_count, 2);
    assert.equal((await state()).find(entry => entry.role === 'agent').url, `${base}/agent`);
    passed('real host worker shares HttpOnly login and leaves the agent page unchanged');

    // Simulate the actual browser tab having been explicitly closed, then a write arrives.
    await ui.evaluate(() => localStorage.setItem('jiuwenclaw_desktop_browser_tab_flags:session-one',
      JSON.stringify({ requested: false, closed: true })));
    let request = await confirm('write');
    const flags = await ui.evaluate(() => JSON.parse(localStorage.getItem('jiuwenclaw_desktop_browser_tab_flags:session-one')));
    assert.deepEqual(flags, { requested: true, closed: false });
    assert.equal(posts, 0); await shot('write-confirm');
    await ui.getByTestId('desktop-browser-opencli-approve').click();
    assert.equal((await request.promise).data.executed, 'yes'); assert.equal(posts, 1);
    passed('persistent shell attention reopens a closed/unmounted browser tab and real UI approval executes once');

    await ui.getByTestId('fixture-collapse').click();
    request = await confirm('write');
    await ui.getByTestId('desktop-browser-opencli-reject').click();
    assert.equal((await request.promise).data.executed, 'no'); assert.equal(posts, 1);
    passed('real UI rejection starts no command');
    request = driver.request('run', { command: 'write', confirm_timeout_s: 2 });
    assert.equal((await request.promise).data.reason, 'not_confirmed'); assert.equal(posts, 1);
    passed('unanswered real host confirmation times out without a write');

    request = await confirm('write-lost');
    await ui.getByTestId('desktop-browser-opencli-approve').click();
    assert.equal((await request.promise).data.executed, 'unknown'); assert.equal(posts, 2);
    assert.equal((await driver.call('pending')).length, 1);
    request = await confirm('write-lost');
    assert.match(await ui.getByTestId('desktop-browser-opencli-warning').innerText(), /unknown outcome/);
    await electron.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].setSize(540, 780));
    await shot('write-warning-narrow');
    await ui.getByTestId('desktop-browser-opencli-reject').click();
    await request.promise; assert.equal(posts, 2);
    await electron.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].setSize(1100, 780));
    passed('unknown write persists and the next real confirmation shows its warning');

    await ui.getByTestId('fixture-collapse').click();
    const held = await driver.call('run', { command: 'captcha' });
    assert.equal(held.reason, 'needs_user');
    await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
    const heldPage = await worker();
    assert.equal(heldPage.hold.state, 'pending'); assert.equal(heldPage.url, `${base}/captcha`);
    assert.equal((await driver.call('run', { command: 'read' })).reason, 'needs_user');
    assert.equal((await worker()).targetId, heldPage.targetId);
    await shot('captcha-hold');
    passed('captcha reveals the real banner and a later automatic command cannot navigate the held page');
    await electron.evaluate(async () => {
      const entry = [...global.browserTest.browserViews.values()].find(entry => entry.role === 'opencli');
      await entry.view.webContents.executeJavaScript("document.querySelector('button').click()");
    });
    await ui.getByTestId('desktop-browser-opencli-done').click();
    await ui.waitForFunction(() => document.querySelector('[data-testid="fixture-message"]').textContent.includes('Please continue'));
    assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
    assert.equal((await worker()).targetId, heldPage.targetId);
    const verified = await electron.evaluate(async ({ session }, base) =>
      (await session.fromPartition('persist:jiuwenswarm-browser').cookies.get({ url: base, name: 'verified' }))[0]?.value, base);
    assert.equal(verified, 'yes');
    passed('Done releases the same page, keeps verification state, and sends the fixed continuation event');

    await driver.call('run', { command: 'captcha' });
    await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
    const abandonedPage = await worker();
    await ui.getByTestId('desktop-browser-opencli-abandon').click();
    assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
    assert.notEqual((await worker()).targetId, abandonedPage.targetId);
    assert.equal((await worker()).visible, true, 'reset hid the selected worker page');
    assert.equal((await worker()).label, 'OpenCLI', 'reset lost the worker page label');
    await shot('worker-after-reset');
    passed('Give up rebuilds the production worker page before the next command and keeps the selected page visible');

    const oldPage = await worker();
    const beforeTicks = ticks;
    request = await confirm('write-slow');
    await ui.getByTestId('desktop-browser-opencli-approve').click();
    await until(() => ticks > beforeTicks + 2, 'adapter page script did not start');
    assert.equal((await driver.call('cancel', { target: request.id })).requested, true);
    assert.equal((await request.promise).cancelled, true);
    assert.notEqual((await worker()).targetId, oldPage.targetId);
    assert.ok((await driver.call('pending')).some(record => record.command === 'fixture/write-slow'));
    const stoppedTicks = ticks;
    await new Promise(resolve => setTimeout(resolve, 500));
    assert.equal(ticks, stoppedTicks);
    assert.equal((await worker()).leases, 0);
    assert.equal((await worker()).visible, true, 'cancellation reset hid the selected worker page');
    assert.equal((await worker()).label, 'OpenCLI', 'cancellation reset lost the worker page label');
    assert.equal((await state()).find(entry => entry.role === 'agent').url, `${base}/agent`);
    passed('cancelled real CLI write kills the process, records unknown outcome, releases lease and rebuilds the page to stop its scripts');
    assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
    passed('commands continue after cancellation with the shared login intact');

    const task = await driver.call('task', { command: 'read' });
    fs.writeFileSync(path.join(scratch, 'agent-list-task.json'), JSON.stringify(task, null, 2));
    assert.equal(task.result.authoritative_browser_result.status, 'completed');
    assert.equal(task.model_calls, 3);
    assert.ok(task.local_core.replaceAll('\\', '/').includes('/agent-core/openjiuwen/'));
    passed('Swarm contribution and real local-Core Browser Agent finish an adapter-only list task with authoritative completed status');
    const blockedTask = await driver.call('task', { command: 'captcha' });
    fs.writeFileSync(path.join(scratch, 'agent-blocked-task.json'), JSON.stringify(blockedTask, null, 2));
    assert.equal(blockedTask.result.authoritative_browser_result.status, 'blocked');
    assert.equal(blockedTask.result.authoritative_browser_result.retryable, false);
    assert.equal(blockedTask.model_calls, 2);
    await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
    assert.equal((await worker()).hold.state, 'pending');
    assert.equal((await worker()).label, 'OpenCLI');
    await shot('captcha-after-reset');
    await ui.getByTestId('desktop-browser-opencli-abandon').click();
    passed('real Browser Agent captcha task is force-finished as blocked without another model call and host hold remains until the UI decision');
    await ui.getByTestId('fixture-collapse').click();
    const hybridTask = await driver.call('task', { command: 'hybrid' });
    fs.writeFileSync(path.join(scratch, 'agent-hybrid-task.json'), JSON.stringify(hybridTask, null, 2));
    assert.equal(hybridTask.result.authoritative_browser_result.status, 'completed');
    assert.equal(hybridTask.model_calls, 5);
    assert.equal(hybridTask.executed_calls.filter(name => name.endsWith('opencli_run')).length, 2);
    assert.equal(hybridTask.executed_calls.filter(name => name.endsWith('browser_navigate')).length, 1);
    assert.equal((await state()).find(entry => entry.role === 'agent').url, `${base}/playwright-fallback`);
    assert.equal((await worker()).url, `${base}/worker`);
    assert.equal((await worker()).visible, false, 'background reset reopened a hidden worker page');
    passed('the same Browser Agent switches from adapter to real Playwright and back to adapter, with both pages independent and background reset still hidden');
    const multipleTask = await driver.call('task', { command: 'multiple' });
    fs.writeFileSync(path.join(scratch, 'agent-multiple-task.json'), JSON.stringify(multipleTask, null, 2));
    assert.equal(multipleTask.result.authoritative_browser_result.status, 'completed');
    assert.equal(multipleTask.model_calls, 5);
    assert.equal(multipleTask.task_state.external_actions.attempts, 3);
    assert.equal(Object.keys(multipleTask.task_state.external_actions.signatures).length, 3);
    assert.deepEqual(itemPages.slice(-3), [1, 2, 3]);
    passed('three adapter calls with different nested arguments execute through the real Agent without a false repeated-command block');
    if (settingsChecks) {
      const status = ui.getByTestId('settings-opencli-status');
      const enable = ui.locator('[data-testid="settings-switch"][data-variant="browser-opencli-enabled"]');
      const display = ui.locator('[data-testid="settings-select"][data-variant="browser-opencli-worker-page"]');
      const config = async params => driver.call('config', { method: params ? 'path.set' : 'path.get', params });
      const scrollSettingsToEnd = async () => {
        // Capture after the resize and React's dependent rows have committed.
        await ui.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        await ui.getByTestId('settings-main').evaluate(element => { element.scrollTop = element.scrollHeight; });
        await ui.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      };
      await ui.getByTestId('fixture-settings').click();
      await status.waitFor();
      assert.equal(await status.getAttribute('data-variant'), 'off');
      assert.equal(await display.count(), 0);
      const off = await driver.call('assembly');
      assert.deepEqual(off.tools, []); assert.equal(off.prompt, '');
      await shot('settings-off', false);
      passed('settings default off collapses the worker mode and contributes no tools or routing prompt');

      const beforeTarget = (await worker()).targetId;
      await enable.click();
      await until(async () => await status.getAttribute('data-variant') === 'available', 'available status did not arrive');
      assert.match(await status.innerText(), /1 websites.*1\.8\.8/);
      const enabled = await driver.call('assembly');
      assert.deepEqual(enabled.tools, ['opencli_describe', 'opencli_run']);
      assert.match(enabled.prompt, /bilibili/);
      assert.equal((await worker()).targetId, beforeTarget, 'saving the switch rebuilt a browser page');
      await scrollSettingsToEnd();
      await shot('settings-on', false);
      passed('the production settings switch persists through ConfigAdapter, reports restricted site count and enables the next contribution');

      await ui.locator('[data-testid="settings-nav-button"][data-variant="general"]').click();
      await ui.locator('[data-testid="settings-select"][data-variant="preferred-language"]').waitFor();
      await shot('settings-general-comparison', false);
      await ui.locator('[data-testid="settings-nav-button"][data-variant="browser"]').click();
      await display.waitFor();
      await display.click();
      await ui.getByRole('option', { name: 'Run in background', exact: true }).click();
      await until(async () => (await config()).payload.opencli.worker_page === 'hidden' && await display.isEnabled(),
        'hidden mode did not persist');
      assert.deepEqual((await config()).payload.opencli.enabled_sites, ['bilibili']);
      assert.equal((await worker()).targetId, beforeTarget);
      await electron.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].setSize(540, 780));
      await scrollSettingsToEnd();
      await shot('settings-hidden-narrow', false);
      await enable.click();
      await until(async () => await status.getAttribute('data-variant') === 'off', 'disabled state did not arrive');
      await scrollSettingsToEnd();
      await shot('settings-off-narrow', false);
      await enable.click();
      await until(async () => await status.getAttribute('data-variant') === 'available', 'available state did not return');
      await electron.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].setSize(1100, 780));
      passed('worker mode uses a partial patch, retains enabled_sites and existing targets, and expanded/collapsed settings render at narrow width');

      assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
      assert.equal((await worker()).targetId, beforeTarget);
      assert.equal((await worker()).visible, false);
      await ui.getByTestId('fixture-browser').click();
      await ui.getByTestId('desktop-browser-pane').waitFor();
      assert.equal(await ui.getByRole('tab', { name: 'OpenCLI', exact: true }).count(), 0);
      await electron.evaluate(async (_, base) => {
        const entry = await global.browserTest.ensureBrowserView({ panelId: 'fixture-member', sessionId: 'session-one',
          memberId: 'research', label: 'Research browser' });
        await entry.view.webContents.loadURL(`${base}/member`);
      }, base);
      await ui.getByRole('tab', { name: 'Research browser', exact: true }).click();
      passed('the next real CLI read changes the existing worker to background mode and removes it from the tab list');

      request = await confirm('write');
      await until(async () => (await worker()).visible, 'background confirmation did not reveal the native page');
      await shot('hidden-write-confirm');
      await ui.getByTestId('desktop-browser-opencli-approve').click();
      assert.equal((await request.promise).data.executed, 'yes');
      await until(async () => !(await worker()).visible, 'background confirmation page stayed visible');
      await until(async () => await ui.getByRole('tab', { name: 'Research browser', exact: true }).getAttribute('aria-selected') === 'true',
        'the prior member page was not restored');
      assert.equal(await ui.getByRole('tab', { name: 'OpenCLI', exact: true }).count(), 0);
      passed('hidden write confirmation temporarily reveals the page, then hides it and restores the previously selected member page');

      const hiddenCaptcha = await driver.call('run', { command: 'captcha' });
      assert.equal(hiddenCaptcha.reason, 'needs_user');
      await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
      await until(async () => (await worker()).visible, 'background captcha page did not appear');
      await shot('hidden-captcha');
      await electron.evaluate(() => [...global.browserTest.browserViews.values()].find(entry => entry.role === 'opencli')
        .view.webContents.executeJavaScript("document.querySelector('button').click()"));
      const heldTarget = (await worker()).targetId;
      await ui.getByTestId('desktop-browser-opencli-done').click();
      await until(async () => !(await worker()).visible, 'solved hidden page did not return to background');
      assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
      assert.equal((await worker()).targetId, heldTarget);
      assert.equal((await worker()).visible, false);
      passed('hidden captcha handling preserves the verified target, restores background operation and allows the next read');

      const postsBeforeTimeout = posts;
      const timeoutRequest = driver.request('run', { command: 'write', confirm_timeout_s: 5 });
      await ui.getByTestId('desktop-browser-opencli-confirm').waitFor();
      assert.equal((await timeoutRequest.promise).data.executed, 'no');
      await until(async () => !(await worker()).visible, 'timed-out hidden confirmation remained visible');
      assert.equal(posts, postsBeforeTimeout);
      passed('an unanswered hidden confirmation times out without a write and restores background visibility');

      await driver.call('run', { command: 'captcha' });
      await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
      const abandoned = (await worker()).targetId;
      await ui.getByTestId('desktop-browser-opencli-abandon').click();
      await until(async () => !(await worker()).visible, 'abandoned hidden page stayed visible');
      assert.equal((await driver.call('run', { command: 'read' })).reason, 'ok');
      assert.notEqual((await worker()).targetId, abandoned);
      assert.equal((await worker()).visible, false);
      passed('Give up on a hidden page removes the temporary tab and the next command resets it without reopening it');

      await ui.getByTestId('fixture-settings').click();
      await status.waitFor();
      const modify = ui.locator('[data-testid="settings-inline-input-modify-btn"][data-variant="browser-path"]');
      await modify.click();
      await ui.locator('[data-testid="settings-inline-input-field"][data-variant="browser-path"]').fill('/fixture/external-chrome');
      await ui.locator('[data-testid="settings-inline-input-save-btn"][data-variant="browser-path"]').click();
      await until(async () => await status.getAttribute('data-variant') === 'unsupported_browser_mode', 'external browser was not diagnosed');
      await shot('settings-external-browser', false);
      const external = await config();
      assert.equal(external.payload.opencli.enabled, true);
      assert.deepEqual(external.payload.opencli.enabled_sites, ['bilibili']);
      assert.equal((await driver.call('assembly')).tools.length, 0);
      await enable.click();
      await until(async () => await status.getAttribute('data-variant') === 'off', 'final disable did not persist');
      assert.deepEqual((await driver.call('assembly')).tools, []);
      assert.equal((await driver.call('assembly')).prompt, '');
      await config({ chrome_path: '' });
      passed('external-browser settings show the unsupported state and disabling the feature removes its next-task contribution');
    }
    if (realSite) {
      const siteChecks = [];
      const agentUrl = (await state()).find(entry => entry.role === 'agent').url;
      for (const [command, args] of [
        ['hot', { limit: 3 }], ['ranking', { limit: 3 }], ['search', { query: 'openJiuwen', limit: 3 }],
      ]) {
        const description = await driver.call('site', { command, operation: 'describe' });
        assert.equal(description.ok, true);
        assert.equal(description.access, 'read');
        const result = await driver.call('site', { command, args });
        siteChecks.push({ command, description, result });
        fs.writeFileSync(path.join(scratch, 'bilibili-read-checks.json'), JSON.stringify(siteChecks, null, 2));
        assert.equal((await state()).find(entry => entry.role === 'agent').url, agentUrl);
        console.log(`SITE: bilibili/${command}: ${result.reason}, observed=${result.observed_count ?? 0}`);
        if (result.reason === 'needs_user') {
          await ui.getByTestId('desktop-browser-opencli-hold').waitFor();
          await shot('bilibili-needs-user');
          await ui.getByTestId('desktop-browser-opencli-abandon').click();
          break;
        }
      }
      const successful = siteChecks.filter(check => check.result.reason === 'ok' && check.result.observed_count > 0);
      assert.ok(successful.length > 0, 'no real Bilibili command returned evidence; see bilibili-read-checks.json');
      passed('original bundled Bilibili read adapters return real data on the production worker page and preserve the agent page');
    }
    fs.writeFileSync(path.join(scratch, 'results.json'), JSON.stringify({ checks, snapshots }, null, 2));
    console.log(`ALL ${checks.length} production host/UI checks passed. Artifacts: ${scratch}`);
  } finally {
    for (const child of children) {
      if (child.exitCode !== null) continue;
      if (process.platform === 'win32') {
        try { execFileSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' }); } catch { /* exited */ }
      } else child.kill('SIGKILL');
    }
    if (electron) await electron.close().catch(() => {});
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
}

main().catch(error => { console.error(error); console.error(`Artifacts: ${scratch}`); process.exitCode = 1; });
