/* Pilote Chrome via CDP — viewport exact (Chrome/Windows impose sinon une
   largeur de fenetre minimale, ce qui fausse les captures mobiles).
   usage : node tools/shoot.mjs <url> <suffixe> [w1xh1 w2xh2 ...]           */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const URL_ = process.argv[2] || 'http://127.0.0.1:8899/index.html';
const SUF = process.argv[3] || '';
const SIZES = (process.argv.slice(4).length ? process.argv.slice(4)
  : ['360x800', '390x844', '768x1024', '1024x768', '1440x1024']).map(s => s.split('x').map(Number));
const OUT = 'build/shots';
mkdirSync(OUT, { recursive: true });

const PORT = 9333 + (Date.now() % 500);
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:\\Users\\saido\\AppData\\Local\\Temp\\claude\\cdp-${PORT}`,
  'about:blank',
], { stdio: 'ignore' });

async function endpoint() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      return (await r.json()).webSocketDebuggerUrl;
    } catch { await sleep(250); }
  }
  throw new Error('Chrome DevTools injoignable');
}

const ws = new WebSocket(await endpoint());
await new Promise(res => ws.addEventListener('open', res, { once: true }));
let id = 0; const waiting = new Map();
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
});
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const n = ++id;
  waiting.set(n, m => (m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)));
  ws.send(JSON.stringify({ id: n, method, params, ...(sessionId ? { sessionId } : {}) }));
});

const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Page.enable'); await S('Runtime.enable');

const report = [];
for (const [w, h] of SIZES) {
  // page vierge avant de changer le viewport : sinon l'etat CSS de la largeur
  // precedente (tiroir de nav, transitions) fuit sur la capture suivante.
  await S('Page.navigate', { url: 'about:blank' });
  await sleep(200);
  await S('Emulation.setDeviceMetricsOverride', {
    width: w, height: h, deviceScaleFactor: 1,
    mobile: w < 860, screenWidth: w, screenHeight: h,
  });
  await S('Page.navigate', { url: URL_ });
  await sleep(1800);
  // page entiere
  const { cssContentSize } = await S('Page.getLayoutMetrics');
  const full = Math.min(Math.ceil(cssContentSize.height), 16000);
  await S('Emulation.setDeviceMetricsOverride', {
    width: w, height: full, deviceScaleFactor: 1, mobile: w < 860,
    screenWidth: w, screenHeight: full,
  });
  await sleep(700);
  const diag = await S('Runtime.evaluate', {
    returnByValue: true,
    expression: `(() => {
      const d = document.documentElement;
      const over = [...document.querySelectorAll('body *')]
        .filter(el => el.getBoundingClientRect().right > d.clientWidth + 1)
        .slice(0, 6)
        .map(el => el.className && typeof el.className === 'string'
             ? '.' + el.className.trim().split(/\\s+/).join('.')
             : el.tagName.toLowerCase());
      return { vw: d.clientWidth, scrollW: d.scrollWidth,
               overflow: d.scrollWidth - d.clientWidth, culprits: [...new Set(over)] };
    })()`,
  });
  const { data } = await S('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${OUT}/${w}${SUF}.png`, Buffer.from(data, 'base64'));
  const v = diag.result.value;
  report.push(v);
  console.log(`${String(w).padStart(5)}px  viewport=${v.vw}  scrollWidth=${v.scrollW}  ` +
    `debordement=${v.overflow > 0 ? '+' + v.overflow + '  <- ' + v.culprits.join(' ') : 'aucun'}`);
}
ws.close(); chrome.kill();
