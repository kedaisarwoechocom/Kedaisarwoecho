# -*- coding: utf-8 -*-
"""Audit netteté / résolution des assets Kedai Sarwo Echo.
Sortie: tableau + JSON de décision upscale.
"""
import json, sys, os
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\tools\audit.json")

# Besoin d'affichage: fiche plat en grand ~560px CSS -> 1120px @2x.
TARGET_CONTENT_W = 1120
# Seuil de netteté (variance du Laplacien normalisée sur le contenu)
SHARP_MIN = 90.0

def laplacian_var(gray):
    k = np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32)
    h, w = gray.shape
    if h < 5 or w < 5:
        return 0.0
    # convolution valide, sans scipy
    out = (
        gray[:-2,1:-1]*k[0,1] + gray[1:-1,:-2]*k[1,0] + gray[1:-1,1:-1]*k[1,1]
        + gray[1:-1,2:]*k[1,2] + gray[2:,1:-1]*k[2,1]
    )
    return float(out.var())

def audit(p: Path):
    im = Image.open(p)
    im.load()
    w, h = im.size
    mode = im.mode
    has_alpha = mode in ("RGBA","LA") or "transparency" in im.info
    rgba = im.convert("RGBA")
    a = np.array(rgba)
    alpha = a[...,3]
    if has_alpha and alpha.min() < 250:
        ys, xs = np.nonzero(alpha > 12)
        if len(xs) == 0:
            bbox = (0,0,w,h)
        else:
            bbox = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
    else:
        bbox = (0,0,w,h)
    bw, bh = bbox[2]-bbox[0], bbox[3]-bbox[1]
    # zone de contenu, en gris, pondérée par alpha (évite de mesurer le vide)
    crop = a[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    gray = (0.299*crop[...,0] + 0.587*crop[...,1] + 0.114*crop[...,2]).astype(np.float32)
    m = crop[...,3] > 200
    if m.sum() < 100:
        m = np.ones_like(gray, dtype=bool)
    g = gray.copy()
    g[~m] = float(gray[m].mean())
    lv = laplacian_var(g)
    fill = float(m.sum()) / max(1, bw*bh)
    return {
        "file": p.name, "w": w, "h": h, "mode": mode, "alpha": bool(has_alpha),
        "bbox": bbox, "content_w": bw, "content_h": bh,
        "fill_pct": round(fill*100, 1),
        "lapvar": round(lv, 1),
        "bytes": p.stat().st_size,
    }

def main():
    files = sorted([p for p in SRC.iterdir() if p.suffix.lower() in (".png",".jpg",".jpeg")])
    rows = [audit(p) for p in files]
    # décision
    for r in rows:
        need_res = r["content_w"] < TARGET_CONTENT_W
        need_sharp = r["lapvar"] < SHARP_MIN
        r["upscale"] = bool(need_res or need_sharp)
        r["why"] = ("résolution" if need_res else "") + ("+netteté" if need_res and need_sharp else ("netteté" if need_sharp else ""))
        if not r["upscale"]:
            r["why"] = "—"
    hdr = f'{"fichier":38} {"taille":>11} {"contenu":>11} {"remplis":>7} {"netteté":>9} {"Ko":>7}  upscale'
    print(hdr); print("-"*len(hdr))
    for r in rows:
        print(f'{r["file"][:38]:38} {r["w"]}x{r["h"]:<6} {r["content_w"]}x{r["content_h"]:<6} '
              f'{r["fill_pct"]:>6}% {r["lapvar"]:>9} {r["bytes"]//1024:>7}  '
              f'{"OUI ("+r["why"]+")" if r["upscale"] else "non"}')
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    n = sum(1 for r in rows if r["upscale"])
    print(f"\n{n}/{len(rows)} fichiers à upscaler. -> {OUT}")

main()
