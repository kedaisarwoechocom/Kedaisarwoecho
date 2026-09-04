# -*- coding: utf-8 -*-
"""Nav a droite sans bascule de langue ni coeur, horaires en une ligne + bouton,
signature du pied de page, amplitude de la vague, masques du titre anime."""
import json, re
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")

# ═══════════ 1. HTML ═══════════
h = ROOT / "index.html"
s = h.read_text(encoding="utf-8")

# 1a. bascule de langue et coeur retires de la barre
old_end = '''    <div class="nav__end">
      <!-- Bascule de langue -->
      <div class="lang" role="group" aria-label="Bahasa / Language">
        <button type="button" class="lang__btn is-on" data-lang="id" aria-pressed="true">ID</button>
        <span class="lang__sep" aria-hidden="true"></span>
        <button type="button" class="lang__btn" data-lang="en" aria-pressed="false">EN</button>
      </div>

      <!-- WhatsApp: toujours visible, y compris sur telephone -->'''
new_end = '''    <div class="nav__end">
      <!-- WhatsApp: toujours visible sur telephone, c'est l'action principale -->'''
assert old_end in s
s = s.replace(old_end, new_end, 1)

# 1b. horaires : une seule ligne, plus un bouton de commande
old_h = '''        <div class="finfo">
          <h3 class="finfo__t" data-i18n="find.hours">Jam buka</h3>
          <p class="finfo__note" id="fHoursNote" hidden data-i18n="find.hoursNote">Jam buka masih harus dikonfirmasi.</p>
          <ul class="hours" id="fHours"></ul>
        </div>'''
new_h = '''        <div class="finfo">
          <h3 class="finfo__t" data-i18n="find.hours">Jam buka</h3>
          <p class="hours-one" id="fHoursLine"></p>
          <a class="btn btn--wa finfo__cta" data-wa href="#" target="_blank" rel="noopener noreferrer">
            <span class="btn__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><use href="#i-wa"/></svg></span>
            <span data-i18n="hero.cta">Pesan Sekarang</span>
          </a>
        </div>'''
assert old_h in s
s = s.replace(old_h, new_h, 1)
h.write_text(s, encoding="utf-8")
print("index.html : nav allegee, horaires en une ligne + bouton de commande")

# ═══════════ 2. CSS ═══════════
m = ROOT / "assets/css/main.css"
c = m.read_text(encoding="utf-8")

# 2a. le menu passe a droite
old_nav = ".nav__links { display: flex; align-items: center; gap: clamp(18px, 3.4vw, 48px); }"
new_nav = (".nav__links { display: flex; align-items: center; gap: clamp(18px, 3.4vw, 48px);\n"
           "              margin-left: auto; }   /* le menu est cale a droite */")
assert old_nav in c
c = c.replace(old_nav, new_nav, 1)

# 2b. la barre de langue et le coeur n'existent plus
c = re.sub(r"\.lang \{[^}]*\}\n", "", c)
c = re.sub(r"\.lang__btn \{[^}]*\}\n", "", c)
c = re.sub(r"\.lang__btn\.is-on \{[^}]*\}\n", "", c)
c = re.sub(r"\.lang__btn:hover \{[^}]*\}\n", "", c)
c = re.sub(r"\.lang__sep \{[^}]*\}\n", "", c)
c = re.sub(r"/\* coeur decoratif de la maquette \(desktop seulement\) \*/\n\.nav__end::after \{.*?\n\}\n", "", c, flags=re.S)
c = c.replace("  .nav__end::after { display: none; }        /* coeur decoratif retire */\n", "")
c = c.replace("  .lang { gap: 2px; }\n", "")
c = c.replace("  .nav__links { margin-left: auto; }\n", "")

# 2c. sur telephone le menu deroulant ne doit plus pousser la barre
old_mob = "  .nav { min-height: var(--tap); gap: 10px; }"
new_mob = ("  .nav { min-height: var(--tap); gap: 10px; }\n"
           "  .nav__links { margin-left: 0; }")
assert old_mob in c
c = c.replace(old_mob, new_mob, 1)

# 2d. masques du titre anime + horaires en une ligne
c = c.replace(".hero__title .script {",
"""/* chaque mot du titre monte derriere un masque (anime par motion.js) */
.hero__title .mot { display: inline-block; overflow: hidden; vertical-align: bottom;
                    padding-bottom: .14em; margin-bottom: -.14em; }
.hero__title .mot__i { display: inline-block; will-change: transform; }
.hero__title .script {""", 1)
m.write_text(c, encoding="utf-8")
print("main.css : menu a droite, langue et coeur supprimes, masques du titre")

sc = ROOT / "assets/css/sections.css"
d = sc.read_text(encoding="utf-8")
old_hours = d[d.index(".hours { display: grid;"):d.index(".flinks {")]
new_hours = """.hours-one {
  font-family: var(--f-display); font-weight: 700; font-size: var(--t-dish);
  color: var(--fg-title); line-height: 1.35;
}

"""
d = d.replace(old_hours, new_hours, 1)
d = d.replace("  --amp: clamp(9px, 1.5vw, 24px);", "  --amp: clamp(16px, 2.6vw, 40px);")
sc.write_text(d, encoding="utf-8")
print("sections.css : horaires en une ligne, vague plus ample")

# ═══════════ 3. donnees ═══════════
p = ROOT / "data/site.json"
j = json.loads(p.read_text(encoding="utf-8"))
l = j["lieu"]
l.pop("horaires", None)
l["horaires_confirmes"] = True
l["horaires_texte"] = {
    "id": "Buka setiap hari, 08.00 – 22.00",
    "en": "Open every day, 8am to 10pm",
}
l["ouverture"] = "08:00"
l["fermeture"] = "22:00"
j["lieu"] = l
j["_lisez_moi"] = [x for x in j["_lisez_moi"]
                   if not x.lstrip().startswith(("horaires ", "horaires_confirmes"))]
i = next(k for k, x in enumerate(j["_lisez_moi"]) if x.startswith("galerie "))
j["_lisez_moi"][i:i] = [
    "horaires_texte     : la phrase affichee sous 'Jam buka'. Une seule ligne.",
    "ouverture / fermeture : les memes horaires en 24 h, pour Google (08:00 / 22:00).",
    "horaires_confirmes : true = les horaires partent aussi dans les donnees Google.",
    "",
]
p.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("site.json : horaires confirmes, ouvert tous les jours 08.00-22.00")
