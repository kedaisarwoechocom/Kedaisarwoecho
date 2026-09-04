# -*- coding: utf-8 -*-
"""Corrections issues de l'audit technique."""
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")

# ═══ P1 — l'iframe de la carte capturait le focus clavier ═══
# 9 arrets de tabulation consecutifs dans la carte, apres quoi le pied de page
# devenait inatteignable au clavier. L'adresse en texte et le bouton d'itineraire
# donnent exactement la meme information : la carte sort du parcours clavier.
h = ROOT / "index.html"
s = h.read_text(encoding="utf-8")
old = '''<iframe id="fMap" title="Peta lokasi Kedai Sarwo Echo" loading="lazy"
                referrerpolicy="no-referrer-when-downgrade" src="about:blank"></iframe>'''
new = '''<iframe id="fMap" title="Peta lokasi Kedai Sarwo Echo" loading="lazy" tabindex="-1"
                aria-hidden="true" referrerpolicy="no-referrer-when-downgrade" src="about:blank"></iframe>'''
assert old in s
s = s.replace(old, new, 1)
h.write_text(s, encoding="utf-8")
print("P1 : carte retiree du parcours clavier (adresse et itineraire la remplacent)")

# ═══ tokens : les teintes d'ombre ne vivent plus en dur dans les composants ═══
t = ROOT / "assets/css/tokens.css"
c = t.read_text(encoding="utf-8")
old_sh = "  --sh-float: 0 30px 60px -30px rgba(110,82,71,.5);"
new_sh = """  --sh-float: 0 30px 60px -30px rgba(110,82,71,.5);
  --sh-btn-active: 0 3px 0 -2px rgba(74,93,85,.28);
  --sh-nav: 0 1px 0 rgba(206,188,178,.7), 0 10px 26px -20px rgba(110,82,71,.5);
  --sh-nav-off: 0 1px 0 rgba(206,188,178,0), 0 10px 26px -20px rgba(110,82,71,0);
  --glow-hub: drop-shadow(0 22px 26px rgba(110,82,71,.22));
  --line-soft: rgba(206,188,178,.45);
  --halo-hub: rgba(206,188,178,.22);"""
assert old_sh in c
c = c.replace(old_sh, new_sh, 1)
t.write_text(c, encoding="utf-8")
print("tokens.css : 7 tokens d'ombre et de filet ajoutes")

# ═══ main.css : plus de rgba en dur, plus d'animation de padding ═══
m = ROOT / "assets/css/main.css"
a = m.read_text(encoding="utf-8")
rempl = [
    ("  box-shadow: 0 1px 0 rgba(206,188,178,0), 0 10px 26px -20px rgba(110,82,71,0);",
     "  box-shadow: var(--sh-nav-off);"),
    ("  box-shadow: 0 1px 0 rgba(206,188,178,.7), 0 10px 26px -20px rgba(110,82,71,.5);",
     "  box-shadow: var(--sh-nav);"),
    ("box-shadow: 0 3px 0 -2px rgba(74,93,85,.28); }", "box-shadow: var(--sh-btn-active); }"),
    ("rgba(206,188,178,.22) 72%", "var(--halo-hub) 72%"),
    ("filter: drop-shadow(0 22px 26px rgba(110,82,71,.22)); }", "filter: var(--glow-hub); }"),
]
for x, y in rempl:
    assert x in a, "INTROUVABLE: " + x[:60]
    a = a.replace(x, y, 1)

# P2 — la nav animait `padding` : propriete de mise en page, donc recalcul a chaque
# changement d'etat. On condense par une echelle du logo, calculee sur le GPU.
old_nav = """  position: sticky; top: 0; z-index: 40;
  transition: padding var(--dur-2) var(--ease-out);
}"""
new_nav = """  position: sticky; top: 0; z-index: 40;
}"""
assert old_nav in a
a = a.replace(old_nav, new_nav, 1)

old_stuck = ".nav.is-stuck { padding-top: clamp(8px, .9vw, 12px); padding-bottom: clamp(8px, .9vw, 12px); }"
new_stuck = """/* condensation par transform : anime sur le GPU, sans recalcul de mise en page */
.nav__logo img { transition: transform var(--dur-2) var(--ease-out); transform-origin: left center; }
.nav.is-stuck .nav__logo img { transform: scale(.84); }"""
assert old_stuck in a
a = a.replace(old_stuck, new_stuck, 1)
m.write_text(a, encoding="utf-8")
print("P2 : la nav ne transitionne plus `padding`, elle met le logo a l'echelle")
print("     5 valeurs rgba en dur remplacees par des tokens")

# ═══ sections.css : filet des horaires ═══
sc = ROOT / "assets/css/sections.css"
d = sc.read_text(encoding="utf-8")
assert "rgba(206, 188, 178, .45)" in d
d = d.replace("border-bottom: 1px solid rgba(206, 188, 178, .45);",
              "border-bottom: 1px solid var(--line-soft);", 1)
sc.write_text(d, encoding="utf-8")
print("sections.css : filet des horaires passe en token")
