# -*- coding: utf-8 -*-
"""Galerie maritime : cadres en arche poses sur une ligne de flottaison."""
import re
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")
p = ROOT / "assets/css/sections.css"
s = p.read_text(encoding="utf-8")

# remplace l'ancien bloc galerie (de son titre de section jusqu'au suivant)
debut = s.index("/* ══════════════ SECTION 5 — GALERIE")
fin = s.index("/* ══════════════ SECTION 6 — AVIS")
nouveau = r"""/* ══════════════ GALERIE — bande maritime sous la note ══════════════
   Cadres en arche, comme des hublots, poses sur une ligne de flottaison.
   Le decalage vertical suit une sinusoide : la bande ondule au lieu de
   s'aligner. sin() est calcule par le navigateur, sans une ligne de JS.   */
.gal { width: 100%; margin-top: clamp(22px, 3vw, 40px); position: relative; }
.gal__title {
  font-family: var(--f-script); font-weight: 400; font-size: var(--t-h3);
  color: var(--fg-accent); text-align: center; line-height: 1.2;
}
.gal__wave {
  --amp: clamp(9px, 1.5vw, 24px);
  margin-top: clamp(14px, 2vw, 26px);
  display: flex; align-items: center; gap: clamp(10px, 1.4vw, 20px);
  overflow-x: auto; overflow-y: hidden;
  scroll-snap-type: x proximity; overscroll-behavior-x: contain;
  padding: calc(var(--amp) + 16px) var(--pad-x) calc(var(--amp) + 20px);
  margin-inline: calc(-1 * var(--pad-x));
  scrollbar-width: none; -ms-overflow-style: none;
  /* la ligne de flottaison, derriere les cadres */
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='24' viewBox='0 0 240 24'%3E%3Cpath d='M0 12c20-10 40-10 60 0s40 10 60 0 40-10 60 0 40 10 60 0' fill='none' stroke='%23CEBCB2' stroke-width='1.6' stroke-linecap='round'/%3E%3C/svg%3E")
              repeat-x center 74%;
}
.gal__wave::-webkit-scrollbar { display: none; }

.gal__wave li {
  --a: calc(var(--i) * .82rad);
  flex: none; width: clamp(126px, 14.5vw, 186px); aspect-ratio: 4 / 5;
  scroll-snap-align: center;
  border-radius: 999px 999px var(--r-md) var(--r-md);   /* arche de hublot */
  overflow: hidden;
  background: var(--bg-raised);
  border: 5px solid var(--c-cream-100);
  box-shadow: var(--sh-card);
  transform: translateY(calc(sin(var(--a)) * var(--amp)))
             rotate(calc(sin(var(--a)) * -2.2deg));
  transition: transform var(--dur-3) var(--ease-out),
              box-shadow var(--dur-2) var(--ease-out);
}
.gal__wave li:hover, .gal__wave li:focus-within {
  transform: translateY(calc(sin(var(--a)) * var(--amp) - 9px)) rotate(0deg) scale(1.035);
  box-shadow: var(--sh-float);
}
.gal__wave img { width: 100%; height: 100%; object-fit: cover; }
/* les illustrations sont detourees : on les pose au lieu de les recadrer */
.gal__wave li.is-illu { background: var(--bg-card); }
.gal__wave li.is-illu img { object-fit: contain; padding: 8%; }

.gal__note {
  margin-top: 6px; text-align: center;
  font-size: var(--t-micro); color: var(--fg-muted); font-style: italic;
}

"""
s = s[:debut] + nouveau + s[fin:]
p.write_text(s, encoding="utf-8")
print("sections.css : galerie en vague, cadres en arche")


# ═══ JS : rendu de la galerie ═══
j = ROOT / "assets/js/app.js"
a = j.read_text(encoding="utf-8")
old = """    gallery() {
      const g = site.galerie || [];
      const sec = $('#galeri');
      sec.hidden = g.length === 0;          // pas de photos = pas de section
      if (!g.length) return;
      $('#galGrid').innerHTML = g.map(x => {
        const alt = esc(lang === 'id' ? (x.alt_id || '') : (x.alt_en || x.alt_id || ''));
        return `<li><img src="assets/img/lieu/${esc(x.fichier)}" alt="${alt}"
                  loading="lazy" decoding="async"></li>`;
      }).join('');
    },"""
new = """    gallery() {
      const g = site.galerie || [];
      const sec = $('#galeri');
      sec.hidden = g.length === 0;              // rien a montrer = pas de bande
      if (!g.length) return;

      const vraiesPhotos = g.some(x => x.source === 'photo');
      const ti = site.galerie_titre || {};
      $('#galTitle').textContent = vraiesPhotos
        ? (lang === 'id' ? ti.id_photos : ti.en_photos) || ''
        : (lang === 'id' ? ti.id : ti.en) || '';
      $('#galNote').hidden = vraiesPhotos;      // mention retiree des la 1re vraie photo

      $('#galGrid').innerHTML = g.map((x, i) => {
        const alt = esc(lang === 'id' ? (x.alt_id || '') : (x.alt_en || x.alt_id || ''));
        const illu = x.source !== 'photo';
        const media = illu
          ? `<picture>
               <source type="image/avif" srcset="${img(x.fichier, 480)}.avif">
               <source type="image/webp" srcset="${img(x.fichier, 480)}.webp">
               <img src="${img(x.fichier, 480)}.png" alt="${alt}" width="480" height="480"
                    loading="lazy" decoding="async">
             </picture>`
          : `<img src="assets/img/lieu/${esc(x.fichier)}" alt="${alt}"
                  loading="lazy" decoding="async">`;
        return `<li class="${illu ? 'is-illu' : ''}" style="--i:${i}">${media}</li>`;
      }).join('');
      // --i pose par CSSOM : la CSP interdit l'attribut style en ligne
      $$('#galGrid > li').forEach((li, i) => {
        li.removeAttribute('style');
        li.style.setProperty('--i', i);
      });
    },"""
assert old in a
a = a.replace(old, new, 1)
j.write_text(a, encoding="utf-8")
print("app.js : rendu de la galerie en vague")
