/* Verifie la carte numerique : affichage des plats, filtres, langue, remontee.
   La carte presente le menu, elle ne prend pas de commande. */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://127.0.0.1:8899/menu.html';
const W = Number(process.argv[2] || 390);
const PORT = 9420 + (Date.now() % 60);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-carte-${PORT}`,
  'about:blank'], { stdio: 'ignore' });

let wsUrl;
for (let i = 0; i < 60; i++) {
  try { wsUrl = (await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json()).webSocketDebuggerUrl; break; }
  catch { await sleep(250); }
}
const ws = new WebSocket(wsUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pend = new Map(); const logs = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.method === 'Runtime.exceptionThrown')
    logs.push('ERREUR JS: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error')
    logs.push('console: ' + m.params.args.map(a => a.value ?? a.description).join(' '));
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
});
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const n = ++id; pend.set(n, m => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result));
  ws.send(JSON.stringify({ id: n, method, params, ...(sessionId ? { sessionId } : {}) }));
});
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Page.enable'); await S('Runtime.enable');
await S('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 860 });
await S('Page.navigate', { url: URL_ });
await sleep(2200);

const ev = async expr => (await S('Runtime.evaluate', { returnByValue: true, expression: expr })).result.value;

console.log(`CARTE NUMERIQUE a ${W}px`);
let v = await ev(`({ cartes: document.querySelectorAll('.carte').length,
                     chips: document.querySelectorAll('.chip').length,
                     images: document.querySelectorAll('.carte__img img').length,
                     sansAlt: [...document.querySelectorAll('.carte__img img')].filter(i => !i.alt).length,
                     boutons: document.querySelectorAll('.carte__add, #panier, #meja').length,
                     debord: document.documentElement.scrollWidth - document.documentElement.clientWidth })`);
console.log(`  depart : ${v.cartes} cartes, ${v.chips} filtres, ${v.images} photos, debordement ${v.debord}px`);
console.log(`  reliquat de commande (bouton, panier, table) : ${v.boutons === 0 ? 'aucun' : v.boutons + ' TROUVE(S) - a retirer'}`);
console.log(`  photos sans texte alternatif : ${v.sansAlt === 0 ? 'aucune' : v.sansAlt}`);

await ev(`document.querySelector('.chip[data-cat="nasi"]').click()`);
await sleep(350);
v = await ev(`({ cartes: document.querySelectorAll('.carte').length,
                 actif: document.querySelector('.chip[aria-pressed="true"]').textContent.trim() })`);
console.log(`  filtre "${v.actif}" : ${v.cartes} cartes affichees`);

await ev(`document.querySelector('.chip[data-cat="all"]').click()`);
await sleep(350);
console.log(`  retour a "Semua" : ${await ev(`document.querySelectorAll('.carte').length`)} cartes`);

const titre = await ev(`document.querySelector('.intro__d').textContent.trim()`);
console.log(`  texte d accueil : "${titre}"`);

const petites = await ev(`[...document.querySelectorAll('a[href],button')].filter(el => el.offsetParent !== null)
  .map(el => { const r = el.getBoundingClientRect(); return { n: el.className || el.tagName, w: Math.round(r.width), h: Math.round(r.height) }; })
  .filter(x => x.w > 0 && (x.w < 44 || x.h < 44)).map(x => x.n + ' ' + x.w + 'x' + x.h)`);
console.log(`  cibles tactiles < 44px : ${petites.length ? [...new Set(petites)].join(', ') : 'aucune'}`);
if (logs.length) console.log('  erreurs :\n    ' + logs.slice(0, 5).join('\n    '));
ws.close(); chrome.kill();
