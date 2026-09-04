# -*- coding: utf-8 -*-
"""Branche le chargement conditionnel des animations + barre de nav collante."""
from pathlib import Path

# ---------- app.js : chargeur ----------
p = Path(r"e:\c\projet\Kedaisarwoecho\assets\js\app.js")
s = p.read_text(encoding="utf-8")

old = """  /* ═══════════ demarrage ═══════════ */"""
new = """  /* ═══════════ animations, chargees seulement si elles ont du sens ═══════════ */
  function chargerAnimations() {
    // respect de prefers-reduced-motion : on ne telecharge meme pas les 130 Ko
    if (reduceMotion()) return;
    const c = navigator.connection;
    if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ''))) return;

    const fichiers = [
      'assets/js/vendor/gsap.min.js',
      'assets/js/vendor/ScrollTrigger.min.js',
      'assets/js/vendor/lenis.min.js',
      'assets/js/motion.js',
    ];
    (function suivant(i) {
      if (i >= fichiers.length) return;
      const el = document.createElement('script');
      el.src = fichiers[i];
      el.onload = () => suivant(i + 1);
      el.onerror = () => console.warn('animation non chargee :', fichiers[i]);
      document.head.appendChild(el);
    })(0);
  }

  /* ═══════════ demarrage ═══════════ */"""
assert old in s
s = s.replace(old, new, 1)

old2 = """        if (sJ.status === 'fulfilled') site = sJ.value; else console.warn(sJ.reason.message);
        applyLang(start);
        if (data) Wheel.init();
      });"""
new2 = """        if (sJ.status === 'fulfilled') site = sJ.value; else console.warn(sJ.reason.message);
        applyLang(start);
        if (data) Wheel.init();
        // apres le rendu : ScrollTrigger mesure ainsi la page dans son etat final
        requestAnimationFrame(() => requestAnimationFrame(chargerAnimations));
      });"""
assert old2 in s
s = s.replace(old2, new2, 1)
p.write_text(s, encoding="utf-8")
print("app.js : chargeur d'animations branche")

# ---------- main.css : nav collante ----------
c = Path(r"e:\c\projet\Kedaisarwoecho\assets\css\main.css")
t = c.read_text(encoding="utf-8")

oldc = """.nav {
  display: flex; align-items: center;
  gap: clamp(12px, 2vw, 28px);
  min-height: 62px;
  padding: clamp(10px, 1.3vw, 20px) var(--pad-x) 0;
  position: relative; z-index: 20;
}"""
newc = """.nav {
  display: flex; align-items: center;
  gap: clamp(12px, 2vw, 28px);
  min-height: 62px;
  padding: clamp(10px, 1.3vw, 20px) var(--pad-x) clamp(6px, .8vw, 12px);
  position: sticky; top: 0; z-index: 40;
  transition: padding var(--dur-2) var(--ease-out);
}
/* la bande de fond deborde jusqu'aux bords de l'ecran : sans ca, le contenu
   defilerait a nu de chaque cote de la colonne pendant que la nav reste collee. */
.nav::before {
  content: ""; position: absolute; inset: 0 50% 0 50%;
  width: 100vw; transform: translateX(-50%); z-index: -1;
  background: var(--bg-panel);
  box-shadow: 0 1px 0 rgba(206,188,178,0), 0 10px 26px -20px rgba(110,82,71,0);
  transition: box-shadow var(--dur-2) var(--ease-out);
}
.nav.is-stuck { padding-top: clamp(8px, .9vw, 12px); padding-bottom: clamp(8px, .9vw, 12px); }
.nav.is-stuck::before {
  box-shadow: 0 1px 0 rgba(206,188,178,.7), 0 10px 26px -20px rgba(110,82,71,.5);
}"""
assert oldc in t
t = t.replace(oldc, newc, 1)
c.write_text(t, encoding="utf-8")
print("main.css : barre de navigation collante")
