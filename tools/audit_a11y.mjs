/* Controle qualite : cibles tactiles >= 44px, debordement horizontal,
   images sans alt, hierarchie des titres. usage : node tools/audit_a11y.mjs */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = process.argv[2] || 'http://127.0.0.1:8899/index.html';
const PORT = 9700 + (Date.now() % 200);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-a11y-${PORT}`,
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

const EXPR = `(() => {
  const nom = el => el.id ? '#' + el.id
    : (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/)[0] : el.tagName.toLowerCase());
  const petites = [...document.querySelectorAll('a[href], button, [role=button]')]
    .filter(el => el.offsetParent !== null)
    .map(el => { const b = el.getBoundingClientRect(); return { n: nom(el), w: Math.round(b.width), h: Math.round(b.height) }; })
    .filter(x => x.w > 0 && (x.w < 44 || x.h < 44));
  const sansAlt = [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).map(nom);
  const titres = [...document.querySelectorAll('h1,h2,h3')].map(h => h.tagName + ' ' + h.textContent.trim().replace(/\\s+/g, ' ').slice(0, 28));
  const d = document.documentElement;
  return { petites, sansAlt, titres, h1: document.querySelectorAll('h1').length,
           debordement: d.scrollWidth - d.clientWidth,
           police: getComputedStyle(document.querySelector('.hero__lede')).fontSize };
})()`;

for (const W of [360, 390, 768, 1024, 1440]) {
  await S('Page.navigate', { url: 'about:blank' }); await sleep(150);
  await S('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 860 });
  await S('Page.navigate', { url: URL_ });
  await sleep(1500);
  const { result } = await S('Runtime.evaluate', { returnByValue: true, expression: EXPR });
  const v = result.value;
  console.log(`\n=== ${W}px ===`);
  console.log(`  debordement horizontal : ${v.debordement}px`);
  console.log(`  cibles tactiles < 44px : ${v.petites.length ? v.petites.map(x => `${x.n} ${x.w}x${x.h}`).join(', ') : 'aucune'}`);
  console.log(`  images sans attribut alt : ${v.sansAlt.length ? v.sansAlt.join(', ') : 'aucune'}`);
  console.log(`  taille du texte courant : ${v.police}`);
  if (W === 1440) {
    console.log(`  nombre de h1 : ${v.h1}`);
    console.log(`  hierarchie   : ${v.titres.join(' | ')}`);
  }
}
ws.close(); chrome.kill();
