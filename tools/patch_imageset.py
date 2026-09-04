# -*- coding: utf-8 -*-
"""Les decors en fond CSS n'ont pas de negociation de format : sans image-set(),
le navigateur telecharge le PNG meme quand il sait lire l'AVIF."""
import re
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")


def iset(png_rel):
    """url(x.png) -> image-set(AVIF, WebP, PNG)"""
    base = png_rel[:-4]
    return (f'image-set(url("{base}.avif") type("image/avif"),\n'
            f'                    url("{base}.webp") type("image/webp"),\n'
            f'                    url("{base}.png") type("image/png"))')


def convertir(css, nom):
    """Duplique chaque background-image en une version image-set placee juste apres :
    un navigateur qui ignore image-set garde la declaration url() precedente."""
    out, n = [], 0
    for bloc in re.split(r"(background-image:[^;]+;)", css):
        out.append(bloc)
        if not bloc.startswith("background-image:"):
            continue
        pngs = re.findall(r'url\("([^"]+\.png)"\)', bloc)
        if not pngs:
            continue
        manquants = [p for p in pngs
                     if not (ROOT / "assets/css" / p).resolve().with_suffix(".avif").exists()]
        if manquants:
            print(f"  {nom}: AVIF absent pour {manquants}, laisse en PNG")
            continue
        nouveau = bloc
        for p in pngs:
            nouveau = nouveau.replace(f'url("{p}")', iset(p), 1)
        out.append("\n  " + nouveau)
        n += 1
    print(f"  {nom}: {n} declaration(s) converties")
    return "".join(out)


for f in ("main.css", "sections.css"):
    p = ROOT / "assets/css" / f
    p.write_text(convertir(p.read_text(encoding="utf-8"), f), encoding="utf-8")
