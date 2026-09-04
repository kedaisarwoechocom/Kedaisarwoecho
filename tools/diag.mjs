/* Inspecte le style calcule d'un selecteur a plusieurs largeurs.
   usage : node tools/diag.mjs "<selecteur>" [w1 w2 ...] */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const SEL = process.argv[2] || '#navLinks';
const WIDTHS = (process.argv.slice(3).length ? process.argv.slice(3) : ['1440', '1024', '900', '860']).map(Number);
const PORT = 9500 + (Date.now() % 400);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:\\Users\\saido\\AppData\\Local\\Temp\\claude\\cdp-diag-${PORT}`,
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

for (const W of WIDTHS) {
  await S('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 860 });
  await S('Page.navigate', { url: 'http://127.0.0.1:8899/index.html' });
  await sleep(1400);
  const r = await S('Runtime.evaluate', {
    returnByValue: true,
    expression: `(() => {
      const n = document.querySelector(${JSON.stringify(SEL)});
      if (!n) return { erreur: 'introuvable' };
      const cs = getComputedStyle(n), b = n.getBoundingClientRect();
      return { W: innerWidth, position: cs.position, background: cs.backgroundColor,
               border: cs.borderTopWidth + ' ' + cs.borderTopColor, radius: cs.borderTopLeftRadius,
               shadow: cs.boxShadow.slice(0, 40), visibility: cs.visibility, opacity: cs.opacity,
               gap: cs.gap, dir: cs.flexDirection, padding: cs.padding,
               box: [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)],
               burger: getComputedStyle(document.querySelector('#burger')).display };
    })()`,
  });
  console.log(W + 'px :', JSON.stringify(r.result.value));
}
ws.close(); chrome.kill();
