# -*- coding: utf-8 -*-
"""Genere assets/css/tokens.css — 3 couches, echelle fluide clamp() calculee.
Les tailles desktop sont MESUREES sur halo.jpeg/section2.jpeg (viewport 1440).
Les tailles mobile sont CONCUES (360), pas deduites d'une reduction.
"""
from pathlib import Path
VMIN, VMAX = 360, 1440
def clamp(lo, hi, unit="rem"):
    """clamp fluide entre VMIN et VMAX, en rem (base 16)."""
    if lo == hi: return f"{lo/16:.4g}rem"
    slope = (hi-lo)/(VMAX-VMIN)
    inter = lo - VMIN*slope
    return f"clamp({lo/16:.4g}rem, {inter/16:.4g}rem + {slope*100:.4g}vw, {hi/16:.4g}rem)"

# nom: (mobile 360, desktop 1440)  -- desktop mesure sur maquette
TYPE = {
 "h1":        (34, 62),   "h2":        (27, 43),   "h3":        (20, 26),
 "script-lg": (24, 34),   "eyebrow":   (17, 22),
 "body":      (16, 18),   "body-sm":   (14, 16),   "nav":       (16, 16),
 "dish":      (17, 20),   "price":     (16, 18),   "btn":       (16, 18),
 "micro":     (12, 13),
}
SPACE = {
 "sec-y":  (56, 104), "gut":    (20, 62),  "stack":  (28, 44),
 "card-p": (24, 36),  "card-g": (18, 48),
}
lines = []
A = lines.append
A("/* ============================================================\n"
  "   Kedai Sarwo Echo — design tokens\n"
  "   Couche 1 primitifs -> couche 2 semantiques -> couche 3 composants.\n"
  "   Couleurs echantillonnees sur halo.jpeg / section2.jpeg (non devinees).\n"
  "   Tailles desktop mesurees a 1440px ; tailles mobile concues a 360px.\n"
  "   ============================================================ */\n")
A(":root{")
A("  /* ---------- COUCHE 1 — PRIMITIFS ---------- */")
A("  /* couleurs relevees pixel par pixel sur les maquettes */")
for n,v,c in [("sage-500","#5A7168","titres — 4.53:1 sur creme, AA"),
              ("sage-600","#5C766D","boutons — blanc dessus 4.92:1, AA"),
              ("sage-700","#4A5D55","survol bouton"),
              ("sage-800","#3E5049","petit texte sauge si besoin de marge"),
              ("brick-500","#AC1A19","script manuscrit + prix — 6.21:1 sur creme"),
              ("brick-600","#8F1514","survol lien brique"),
              ("logo-red","#CB0D0D","RESERVE au logo, jamais du texte"),
              ("cream-100","#FBF7F3","surface haute"),
              ("cream-200","#F4EDE7","fond principal (panneau)"),
              ("rose-300","#E3DAD4","cartes section 2"),
              ("taupe-400","#CEBCB2","cadre de page, filets"),
              ("brown-600","#6E5247","texte courant — 6.12:1 sur creme"),
              ("brown-400","#8A6E61","texte secondaire"),
              ("white","#FFFFFF","")]:
    A(f"  --c-{n}: {v};{'  /* '+c+' */' if c else ''}")
A("")
A("  --f-display: 'Baloo 2', 'Trebuchet MS', system-ui, sans-serif;")
A("  --f-script:  'Sriracha', 'Comic Sans MS', cursive;")
A("  --f-body:    'Lato', 'Segoe UI', system-ui, -apple-system, sans-serif;")
A("  --f-brand:   'Bad Script', 'Sriracha', cursive;  /* nom du resto en texte */")
A("")
A("  /* echelle typographique fluide 360 -> 1440 */")
for k,(lo,hi) in TYPE.items(): A(f"  --t-{k}: {clamp(lo,hi)};")
A("")
A("  --lh-tight: 1.08;  --lh-snug: 1.25;  --lh-body: 1.5;  --lh-loose: 1.65;")
A("  --tr-wide: .14em;  --tr-tight: -.01em;")
A("")
A("  /* espacements fluides */")
for k,(lo,hi) in SPACE.items(): A(f"  --s-{k}: {clamp(lo,hi)};")
A("  --s-1:.25rem; --s-2:.5rem; --s-3:.75rem; --s-4:1rem; --s-5:1.5rem;")
A("  --s-6:2rem; --s-7:2.5rem; --s-8:3rem; --s-9:4rem;")
A("")
A("  --r-pill: 999px; --r-lg: 34px; --r-md: 18px; --r-sm: 10px;")
A("  --sh-btn: 0 6px 0 -2px rgba(74,93,85,.28), 0 10px 22px -12px rgba(46,32,25,.45);")
A("  --sh-card: 0 2px 3px rgba(110,82,71,.05), 0 18px 34px -22px rgba(110,82,71,.4);")
A("  --sh-float: 0 30px 60px -30px rgba(110,82,71,.5);")
A("")
A("  --ease-out: cubic-bezier(.22,1,.36,1);")
A("  --ease-soft: cubic-bezier(.32,.72,0,1);")
A("  --dur-1: .18s; --dur-2: .32s; --dur-3: .55s;")
A("")
A("  --wrap-max: 1440px;   /* largeur des maquettes */")
A("  --panel-max: 1316px;  /* panneau creme mesure: 1316 de 1440 */")
A("  --tap: 44px;          /* cible tactile minimale */")
A("")
A("  /* ---------- COUCHE 2 — SEMANTIQUES ---------- */")
for a,b in [("bg-page","var(--c-taupe-400)"),("bg-panel","var(--c-cream-200)"),
            ("bg-raised","var(--c-cream-100)"),("bg-card","var(--c-rose-300)"),
            ("fg-title","var(--c-sage-500)"),("fg-accent","var(--c-brick-500)"),
            ("fg-body","var(--c-brown-600)"),("fg-muted","var(--c-brown-400)"),
            ("fg-on-accent","var(--c-white)"),("line","var(--c-taupe-400)"),
            ("focus","var(--c-brick-500)")]:
    A(f"  --{a}: {b};")
A("")
A("  /* ---------- COUCHE 3 — COMPOSANTS ---------- */")
for a,b in [("btn-bg","var(--c-sage-600)"),("btn-bg-hover","var(--c-sage-700)"),
            ("btn-fg","var(--fg-on-accent)"),("btn-h","clamp(48px, 3.2vw + 36px, 62px)"),
            ("btn-px","clamp(22px, 1.6vw + 16px, 34px)"),
            ("nav-fg","var(--c-brown-600)"),("nav-fg-active","var(--c-sage-500)"),
            ("card-bg","var(--bg-card)"),("card-title","var(--fg-accent)"),
            ("card-body","var(--fg-body)"),("card-icon","var(--c-sage-500)"),
            ("lineart","rgba(110,82,71,.17)"),("price-fg","var(--fg-accent)")]:
    A(f"  --{a}: {b};")
A("}")
A("")
A("/* Pas de mode sombre : l'identite du restaurant est une palette creme/sauge\n"
  "   chaude, sans equivalent sombre dans les maquettes. Les couleurs sont peintes\n"
  "   explicitement pour que le rendu soit identique quel que soit le theme systeme. */")
A(":root{ color-scheme: light; }")
Path("assets/css/tokens.css").write_text("\n".join(lines), encoding="utf-8")
print(f"tokens.css genere — {len(lines)} lignes")
for k in ("h1","h2","body","btn"): print(f"  --t-{k}: {clamp(*TYPE[k])}")
