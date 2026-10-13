// A busy daemon port must abort WP0 before any OpenCLI command can run.
const assert = require('node:assert/strict');
const http = require('node:http');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { test } = require('node:test');

test('WP0 aborts before CLI execution when its isolation probe cannot bind', { timeout: 30000 }, async t => {
  const hits = [];
  const probe = http.createServer((req, res) => {
    hits.push({ path: req.url, userAgent: req.headers['user-agent'] || '' });
    res.setHeader('Content-Type', 'application/json');
    res.end('{"ok":false}');
  });
  try {
    await new Promise((resolve, reject) => {
      probe.once('error', reject);
      probe.listen(19825, '127.0.0.1', resolve);
    });
  } catch (error) {
    if (error.code !== 'EADDRINUSE') throw error;
    t.skip('Another process already owns port 19825; leave that process untouched.');
    return;
  }
  const env = { ...process.env };
  delete env.ELECTRON_RUN_AS_NODE;
  const electron = require('../../jiuwenswarm/channels/desktop/electron/node_modules/electron');
  let child;
  try {
    const result = await new Promise((resolve, reject) => {
      child = spawn(electron, [path.join(__dirname, 'opencli_smoke.cjs')], {
        env, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'],
      });
      let output = '';
      child.stdout.on('data', chunk => { output += chunk; });
      child.stderr.on('data', chunk => { output += chunk; });
      child.once('error', reject);
      child.once('exit', code => resolve({ code, output }));
    });
    assert.equal(result.code, 2);
    assert.match(result.output, /Cannot exclusively bind daemon probe port 19825/);
    assert.doesNotMatch(result.output, /PASS A:|runtime 1\.8\.8|SMOKE PASSED/);
    assert.equal(hits.filter(hit => hit.userAgent === 'node' || hit.path === '/command').length, 0);
  } finally {
    if (child && child.exitCode === null) child.kill();
    probe.closeAllConnections();
    await new Promise(resolve => probe.close(resolve));
  }
});
