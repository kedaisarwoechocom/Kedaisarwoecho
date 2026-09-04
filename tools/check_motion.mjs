/* Verifie qu'aucun contenu ne reste invisible apres animation, en conditions
   reelles : viewport normal, defilement progressif. */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://127.0.0.1:8899/index.html';
const W = Number(process.argv[2] || 1440), H = Number(process.argv[3] || 900);
const PORT = 9800 + (Date.now() % 150);
mkdirSync('build/shots', { recursive: true });

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-mo-${PORT}`,
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
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type !== 'log')
    logs.push(m.params.type + ': ' + m.params.args.map(a => a.value ?? a.description).join(' '));
  if (m.method === 'Runtime.exceptionThrown')
    logs.push('ERREUR JS: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
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
// Chrome headless annonce 'reduce' par defaut : on force la preference normale
// pour pouvoir tester les animations telles que les verra un visiteur.
await S('Emulation.setEmulatedMedia', {
  features: [{ name: 'prefers-reduced-motion', value: process.argv[4] === 'reduce' ? 'reduce' : 'no-preference' }],
});
await S('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: W < 860 });
await S('Page.navigate', { url: URL_ });
await sleep(2500);

const shot = async nom => {
  const { data } = await S('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`build/shots/_mo-${nom}.png`, Buffer.from(data, 'base64'));
};

const hauteur = (await S('Runtime.evaluate', { returnByValue: true, expression: 'document.body.scrollHeight' })).result.value;
console.log(`page ${W}x${H}, hauteur totale ${hauteur}px`);
await shot('haut');

// defilement progressif, comme un vrai visiteur
for (let y = 0; y <= hauteur; y += Math.round(H * 0.7)) {
  await S('Runtime.evaluate', { expression: `window.scrollTo(0, ${y})` });
  await sleep(500);
}
await sleep(1500);
await shot('bas');

const { result } = await S('Runtime.evaluate', {
  returnByValue: true,
  expression: `(() => {
    const nom = el => el.id ? '#' + el.id
      : (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/)[0] : el.tagName.toLowerCase());
    const invisibles = [...document.querySelectorAll('main *, .foot *')].filter(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      if (el.closest('[hidden]')) return false;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return false;
      return parseFloat(cs.opacity) < 0.9;
    }).map(el => nom(el) + ' opacite ' + getComputedStyle(el).opacity);
    return {
      invisibles: [...new Set(invisibles)].slice(0, 12),
      lenis: !!window.Lenis, gsap: !!window.gsap, st: !!window.ScrollTrigger,
      navStuck: document.querySelector('.nav')?.classList.contains('is-stuck') ?? null,
      navPos: getComputedStyle(document.querySelector('.nav')).position,
      scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
      jsonLd: (() => { const e = document.querySelector('script[type="application/ld+json"]');
                       if (!e) return 'ABSENT';
                       try { const o = JSON.parse(e.textContent);
                             return o['@type'] + ' / ' + (o.aggregateRating ? 'note ' + o.aggregateRating.ratingValue : 'sans note') +
                                    ' / ' + (o.geo ? 'geo ok' : 'sans geo') + ' / ' + (o.openingHoursSpecification ? 'horaires publies' : 'horaires non publies'); }
                       catch (x) { return 'JSON INVALIDE'; } })(),
      carte: document.querySelector('#fMap')?.src?.slice(0, 46) || 'absente',
      police: [...document.fonts].filter(f => f.status === 'loaded').length,
    };
  })()`,
});
const v = result.value;
console.log(`  bibliotheques chargees : gsap=${v.gsap} ScrollTrigger=${v.st} Lenis=${v.lenis}`);
console.log(`  nav : position ${v.navPos}, condensee ${v.navStuck}`);
console.log(`  debordement horizontal : ${v.scrollW - v.clientW}px`);
console.log(`  donnees structurees : ${v.jsonLd}`);
console.log(`  carte : ${v.carte}`);
console.log(`  polices chargees : ${v.police}`);
console.log(`  elements restes invisibles : ${v.invisibles.length ? '\n    - ' + v.invisibles.join('\n    - ') : 'aucun'}`);
if (logs.length) console.log('  console :\n    ' + logs.slice(0, 8).join('\n    '));
ws.close(); chrome.kill();
