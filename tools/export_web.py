# -*- coding: utf-8 -*-
"""Export web: AVIF + WebP multi-tailles, repli PNG. Downscale Lanczos depuis l'upscale 4x."""
import json, shutil
from pathlib import Path
from PIL import Image

ROOT   = Path(r"e:\c\projet\Kedaisarwoecho")
BUILD  = ROOT/"build"
IMG    = ROOT/"assets"/"img"
DISH_W = [240, 480, 880]        # vignette roue / fiche mobile / fiche desktop @2x
PNG_AT = 480                    # repli PNG: une seule taille
AVIF_Q, WEBP_Q = 58, 82

def emit(src: Image.Image, outdir: Path, stem: str, widths, png_at=None, report=None):
    outdir.mkdir(parents=True, exist_ok=True)
    w0, h0 = src.size
    for w in widths:
        if w > w0: continue
        h = max(1, round(h0 * w / w0))
        im = src.resize((w, h), Image.LANCZOS)
        im.save(outdir/f"{stem}-{w}.avif", quality=AVIF_Q)
        im.save(outdir/f"{stem}-{w}.webp", quality=WEBP_Q, method=6)
        if png_at == w:
            im.save(outdir/f"{stem}-{w}.png", optimize=True)
        if report is not None:
            for ext in ("avif","webp","png"):
                p = outdir/f"{stem}-{w}.{ext}"
                if p.exists(): report.append((p.relative_to(ROOT).as_posix(), p.stat().st_size))

rep = []
# ---------- 1. plats ----------
dishes = sorted((BUILD/"upscale-out").glob("*.png"))
for p in dishes:
    im = Image.open(p).convert("RGBA")
    # recadre sur le contenu reel: enleve le vide transparent, gagne des pixels utiles
    bb = im.getbbox()
    if bb: im = im.crop(bb)
    emit(im, IMG/"dishes", p.stem, DISH_W, PNG_AT, rep)
print(f"{len(dishes)} plats exportes")

# ---------- 2. calques hero ----------
L = json.load(open(BUILD/"hero-layers"/"layers.json"))
HERO_W = {"plate":[560,900,1400], "stamp":[320,640]}
manifest = {"comp_w": L["comp_w"], "comp_h": L["comp_h"], "layers": {}}
for name, v in L["layers"].items():
    im = Image.open(BUILD/"hero-layers"/v["file"]).convert("RGBA")
    widths = HERO_W.get(name, [v["w"]])
    widths = [w for w in widths if w <= im.width] or [im.width]
    emit(im, IMG/"hero", f"hero-{name}", widths, widths[len(widths)//2], rep)
    manifest["layers"][name] = {k: v[k] for k in ("left_pct","top_pct","w_pct","h_pct","w","h")}
    manifest["layers"][name]["widths"] = widths
(IMG/"hero").mkdir(parents=True, exist_ok=True)
json.dump(manifest, open(IMG/"hero"/"layers.json","w"), indent=2)
print(f"{len(L['layers'])} calques hero exportes")

# ---------- 3. logos ----------
lg = Image.open(BUILD/"logo-out"/"logo.png").convert("RGBA")
bb = lg.getbbox();  lg = lg.crop(bb) if bb else lg
emit(lg, IMG/"brand", "logo", [180, 300, 480], 300, rep)
ls = Image.open(BUILD/"logo-out"/"logo-short.png").convert("RGBA")
bb = ls.getbbox();  ls = ls.crop(bb) if bb else ls
emit(ls, IMG/"brand", "logo-short", [96, 192, 320], 192, rep)
print("logos exportes")

tot = sum(s for _, s in rep)
print(f"\n{len(rep)} fichiers, {tot/1024/1024:.2f} Mo au total")
big = sorted(rep, key=lambda r: -r[1])[:6]
for f, s in big: print(f"  {s//1024:>5} Ko  {f}")
