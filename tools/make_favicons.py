# -*- coding: utf-8 -*-
"""Favicons + icones PWA depuis logo-short.png (upscale 4x)."""
from pathlib import Path
from PIL import Image

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")
SRC  = ROOT/"build"/"logo-out"/"logo-short.png"
OUT  = ROOT/"assets"/"img"/"brand"
OUT.mkdir(parents=True, exist_ok=True)
CREAM = (244, 237, 231, 255)

src = Image.open(SRC).convert("RGBA")
bb = src.getbbox(); src = src.crop(bb) if bb else src

def square(img, size, scale, bg=None):
    """Place l'icone centree sur un canevas carre, occupant `scale` de la largeur."""
    canvas = Image.new("RGBA", (size, size), bg if bg else (0,0,0,0))
    target = int(size*scale)
    r = min(target/img.width, target/img.height)
    im = img.resize((max(1,round(img.width*r)), max(1,round(img.height*r))), Image.LANCZOS)
    canvas.alpha_composite(im, ((size-im.width)//2, (size-im.height)//2))
    return canvas

# favicon.ico — fond transparent, icone large (lisible a 16px)
ico = square(src, 256, 0.94)
ico.save(OUT/"favicon.ico", sizes=[(16,16),(32,32),(48,48)])
square(src, 96, 0.94).save(OUT/"favicon-96.png", optimize=True)
square(src, 32, 0.96).save(OUT/"favicon-32.png", optimize=True)

# Apple: pas de transparence -> fond creme
square(src, 180, 0.76, CREAM).convert("RGB").save(OUT/"apple-touch-icon.png", optimize=True)

# PWA: 192/512 "any" + 512 maskable (zone de securite 40% -> icone a 60%)
square(src, 192, 0.80, CREAM).save(OUT/"icon-192.png", optimize=True)
square(src, 512, 0.80, CREAM).save(OUT/"icon-512.png", optimize=True)
square(src, 512, 0.58, CREAM).save(OUT/"icon-512-maskable.png", optimize=True)

# SVG monogramme de repli (safari pinned tab) — silhouette du blob
for f in sorted(OUT.glob("favicon*")) + sorted(OUT.glob("icon-*")) + [OUT/"apple-touch-icon.png"]:
    print(f"  {f.name:24} {f.stat().st_size//1024 or 1:>3} Ko")
