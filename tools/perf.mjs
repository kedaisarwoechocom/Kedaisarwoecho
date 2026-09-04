/* Mesure de performance en profil mobile realiste : 4G lente + processeur bride.
   usage : node tools/perf.mjs */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://127.0.0.1:8899/index.html';
const PORT = 9900 + (Date.now() % 90);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-perf-${PORT}`,
  'about:blank'], { stdio: 'ignore' });

let wsUrl;
for (let i = 0; i < 60; i++) {
  try { wsUrl = (await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json()).webSocketDebuggerUrl; break; }
  catch { await sleep(250); }
}
const ws = new WebSocket(wsUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pend = new Map();
const req = new Map(); const finis = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.method === 'Network.responseReceived') req.set(m.params.requestId, m.params.response.url);
  if (m.method === 'Network.loadingFinished')
    finis.push({ url: req.get(m.params.requestId) || '?', taille: m.params.encodedDataLength });
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
});
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const n = ++id; pend.set(n, m => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result));
  ws.send(JSON.stringify({ id: n, method, params, ...(sessionId ? { sessionId } : {}) }));
});
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);

await S('Page.enable'); await S('Network.enable'); await S('Runtime.enable');
await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'no-preference' }] });
await S('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
// 4G lente, comme sur la cote de Gunungkidul
await S('Network.emulateNetworkConditions', {
  offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8,
});
await S('Emulation.setCPUThrottlingRate', { rate: 4 });
await S('Network.setCacheDisabled', { cacheDisabled: true });

const t0 = Date.now();
await S('Page.navigate', { url: URL_ });
await sleep(9000);

const { result } = await S('Runtime.evaluate', {
  returnByValue: true, awaitPromise: true,
  expression: `new Promise(res => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    let lcp = 0;
    try {
      new PerformanceObserver(l => { for (const e of l.getEntries()) lcp = e.startTime; })
        .observe({ type: 'largest-contentful-paint', buffered: true });
    } catch (_) {}
    setTimeout(() => {
      const fcp = performance.getEntriesByName('first-contentful-paint')[0];
      res({ dcl: Math.round(nav.domContentLoadedEventEnd || 0),
             load: Math.round(nav.loadEventEnd || 0),
             fcp: Math.round(fcp ? fcp.startTime : 0),
             lcp: Math.round(lcp),
             img: performance.getEntriesByType('resource').filter(r => r.initiatorType === 'img').length });
    }, 400);
  })`,
});
const v = result.value;

const total = finis.reduce((n, f) => n + f.taille, 0);
const parType = {};
for (const f of finis) {
  const ext = (f.url.split('?')[0].match(/\.(\w+)$/) || [, 'autre'])[1];
  parType[ext] = (parType[ext] || 0) + f.taille;
}
console.log('PROFIL MOBILE — 390x844 @2x, 4G lente (1,6 Mbit/s, 150 ms), processeur x4 plus lent, cache vide\n');
console.log(`  First Contentful Paint  ${v.fcp} ms`);
console.log(`  Largest Contentful Paint ${v.lcp} ms`);
console.log(`  DOM pret                ${v.dcl} ms`);
console.log(`  Chargement complet      ${v.load} ms`);
console.log(`\n  ${finis.length} requetes, ${(total / 1024).toFixed(0)} Ko transferes (${v.img} images)`);
for (const [k, n] of Object.entries(parType).sort((a, b) => b[1] - a[1]))
  console.log(`    ${k.padEnd(8)} ${(n / 1024).toFixed(1).padStart(8)} Ko`);
console.log('\n  plus gros fichiers :');
for (const f of finis.sort((a, b) => b.taille - a.taille).slice(0, 6))
  console.log(`    ${(f.taille / 1024).toFixed(1).padStart(8)} Ko  ${f.url.replace(/^https?:\/\/[^/]+\//, '')}`);
ws.close(); chrome.kill();
