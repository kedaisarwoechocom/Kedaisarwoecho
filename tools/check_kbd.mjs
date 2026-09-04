/* Parcours au clavier : ordre de tabulation, indicateur de focus, pieges. */
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL_ = 'http://127.0.0.1:8899/index.html';
const W = Number(process.argv[2] || 1440);
const PORT = 9950 + (Date.now() % 40);

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=C:/Users/saido/AppData/Local/Temp/claude/cdp-kbd-${PORT}`,
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
await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
await S('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 860 });
await S('Page.navigate', { url: URL_ });
await sleep(2200);

const decrire = `(() => {
  const a = document.activeElement;
  if (!a || a === document.body) return 'body';
  const nom = a.id ? '#' + a.id
    : (typeof a.className === 'string' && a.className ? '.' + a.className.trim().split(/\\s+/)[0] : a.tagName.toLowerCase());
  const cs = getComputedStyle(a);
  const lbl = (a.getAttribute('aria-label') || a.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 26);
  const r = a.getBoundingClientRect();
  return nom + ' [' + lbl + ']' + (r.width < 44 || r.height < 44 ? ' PETIT' : '');
})()`;

const vus = [];
for (let i = 0; i < 34; i++) {
  await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await sleep(45);
  const { result } = await S('Runtime.evaluate', { returnByValue: true, expression: decrire });
  vus.push(result.value);
}
console.log(`ORDRE DE TABULATION a ${W}px (${vus.length} tabulations)`);
vus.forEach((v, i) => console.log(`  ${String(i + 1).padStart(2)}. ${v}`));

const boucle = vus.findIndex((v, i) => i > 3 && v === vus[0]);
console.log(boucle > 0 ? `\n  retour au debut apres ${boucle} tabulations (pas de piege)`
                       : '\n  pas de bouclage observe sur 34 tabulations');

const { result } = await S('Runtime.evaluate', {
  returnByValue: true,
  expression: `(() => {
    const focusables = [...document.querySelectorAll('a[href],button,[tabindex]:not([tabindex="-1"]),iframe')]
      .filter(el => el.offsetParent !== null || el.tagName === 'IFRAME');
    const sansNom = focusables.filter(el =>
      !(el.getAttribute('aria-label') || el.textContent.trim() || el.getAttribute('title'))).length;
    return { total: focusables.length, sansNom,
             roleListbox: !!document.querySelector('[role=listbox]'),
             activedesc: document.querySelector('[role=listbox]')?.getAttribute('aria-activedescendant') || '' };
  })()`,
});
const v = result.value;
console.log(`\n  ${v.total} elements focusables, ${v.sansNom} sans nom accessible`);
console.log(`  roue : role=listbox ${v.roleListbox}, aria-activedescendant "${v.activedesc}"`);
ws.close(); chrome.kill();
