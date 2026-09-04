/* Releve les rectangles de plusieurs elements a plusieurs largeurs.
   usage : node tools/rects.mjs [w1 w2 ...] */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://127.0.0.1:8899/index.html';
const WIDTHS = (process.argv.slice(2).length ? process.argv.slice(2) : ['1440', '1920']).map(Number);
const PORT = 9600 + (Date.now() % 300);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-rects-${PORT}`,
  'about:blank'], { stdio: 'ignore' });

let wsUrl;
for (let i = 0; i < 60; i++) {
  try { wsUrl = (await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json()).webSocketDebuggerUrl; break; }
  catch { await sleep(250); }
}
const ws = new WebSocket(wsUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pend = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const n = ++id; pend.set(n, m => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result));
  ws.send(JSON.stringify({ id: n, method, params, ...(sessionId ? { sessionId } : {}) }));
});
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Page.enable'); await S('Runtime.enable');

const SELS = [
  ['nav (logo)', '.nav__logo'],
  ['titre H1', '.hero__title'],
  ['vignette 1', '.pick__thumb'],
  ['compo hero', '.comp__box'],
  ['bloc cartes S2', '.why__grid'],
  ['carte 1', '.wcard'],
  ['roue', '.wheel'],
  ['bloc roue+fiche', '.menu__stage'],
];

for (const W of WIDTHS) {
  await S('Page.navigate', { url: 'about:blank' }); await sleep(150);
  await S('Emulation.setDeviceMetricsOverride', { width: W, height: 1000, deviceScaleFactor: 1, mobile: W < 860 });
  await S('Page.navigate', { url: URL_ });
  await sleep(1600);
  const { result } = await S('Runtime.evaluate', {
    returnByValue: true,
    expression: `(() => {
      const out = {};
      ${JSON.stringify(SELS)}.forEach(([nom, sel]) => {
        const el = document.querySelector(sel);
        if (!el) { out[nom] = null; return; }
        const r = el.getBoundingClientRect();
        out[nom] = { g: Math.round(r.left), d: Math.round(innerWidth - r.right),
                     h: Math.round(r.top + scrollY), l: Math.round(r.width) };
      });
      out._padx = getComputedStyle(document.querySelector('.hero')).paddingLeft;
      out._navpt = getComputedStyle(document.querySelector('.nav')).paddingTop;
      return out;
    })()`,
  });
  const v = result.value;
  console.log(`\n=== ${W}px  (--pad-x ${v._padx}, nav padding-top ${v._navpt}) ===`);
  console.log(`  ${'element'.padEnd(18)}${'gauche'.padStart(8)}${'droite'.padStart(8)}${'largeur'.padStart(9)}`);
  for (const [nom] of SELS) {
    const r = v[nom];
    console.log(r ? `  ${nom.padEnd(18)}${String(r.g).padStart(8)}${String(r.d).padStart(8)}${String(r.l).padStart(9)}`
                  : `  ${nom.padEnd(18)}  absent`);
  }
}
ws.close(); chrome.kill();
