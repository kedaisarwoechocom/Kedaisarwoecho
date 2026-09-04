# -*- coding: utf-8 -*-
"""Decoupe 2.png (compo hero) en calques independants pour l'animation GSAP.
Methode: composantes connexes sur le canal alpha, puis regroupement spatial.
Deterministe et exact — pas de selection manuelle.
Sortie: build/hero-layers/*.png + layers.json (positions relatives, en %).
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers")
OUT.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA")
W, H = im.size
a = np.array(im)
alpha = a[..., 3]
mask = alpha > 16
print(f"source {W}x{H}, pixels opaques {mask.sum():,}")

# --- composantes connexes 8-voisins, iteratif (pile) ---
lab = np.zeros((H, W), dtype=np.int32)
cur = 0
comps = []
ys, xs = np.nonzero(mask)
order = np.argsort(-(alpha[ys, xs]))  # demarre par les pixels les plus opaques
stack = []
for idx in order:
    sy, sx = int(ys[idx]), int(xs[idx])
    if lab[sy, sx] != 0:
        continue
    cur += 1
    lab[sy, sx] = cur
    stack.append((sy, sx))
    minx = maxx = sx; miny = maxy = sy; n = 0
    while stack:
        y, x = stack.pop()
        n += 1
        if x < minx: minx = x
        if x > maxx: maxx = x
        if y < miny: miny = y
        if y > maxy: maxy = y
        y0, y1 = max(0, y-1), min(H, y+2)
        x0, x1 = max(0, x-1), min(W, x+2)
        sub_m = mask[y0:y1, x0:x1]
        sub_l = lab[y0:y1, x0:x1]
        nyy, nxx = np.nonzero(sub_m & (sub_l == 0))
        for k in range(len(nyy)):
            yy, xx = int(nyy[k]) + y0, int(nxx[k]) + x0
            lab[yy, xx] = cur
            stack.append((yy, xx))
    comps.append({"id": cur, "n": n, "bbox": [minx, miny, maxx+1, maxy+1]})

comps.sort(key=lambda c: -c["n"])
print(f"{len(comps)} composantes. 6 plus grosses: " +
      ", ".join(f'#{c["id"]}({c["n"]:,}px {c["bbox"][2]-c["bbox"][0]}x{c["bbox"][3]-c["bbox"][1]})' for c in comps[:6]))

# --- regroupement: fusionne les bbox proches (line-art = multiples traits) ---
GAP = 60
groups = [{"ids": [c["id"]], "bbox": list(c["bbox"]), "n": c["n"]} for c in comps]

def near(b1, b2, g):
    return not (b1[2]+g < b2[0] or b2[2]+g < b1[0] or b1[3]+g < b2[1] or b2[3]+g < b1[1])

changed = True
while changed:
    changed = False
    for i in range(len(groups)):
        if groups[i] is None: continue
        for j in range(i+1, len(groups)):
            if groups[j] is None: continue
            if near(groups[i]["bbox"], groups[j]["bbox"], GAP):
                b1, b2 = groups[i]["bbox"], groups[j]["bbox"]
                groups[i]["bbox"] = [min(b1[0],b2[0]), min(b1[1],b2[1]), max(b1[2],b2[2]), max(b1[3],b2[3])]
                groups[i]["ids"] += groups[j]["ids"]
                groups[i]["n"] += groups[j]["n"]
                groups[j] = None
                changed = True
    groups = [g for g in groups if g is not None]

groups.sort(key=lambda g: -g["n"])
print(f"\n{len(groups)} groupes apres fusion (gap {GAP}px):")
for g in groups:
    b = g["bbox"]
    print(f'  {g["n"]:>9,}px  bbox {b[0]:>4},{b[1]:>4} -> {b[2]:>4},{b[3]:>4}  ({b[2]-b[0]}x{b[3]-b[1]})  {len(g["ids"])} traits')

json.dump([{"n": g["n"], "bbox": g["bbox"], "traits": len(g["ids"])} for g in groups],
          open(OUT / "_groups_raw.json", "w"), indent=2)
np.save(OUT / "_lab.npy", lab)
json.dump({"W": W, "H": H, "groups": [{"ids": g["ids"], "bbox": g["bbox"], "n": g["n"]} for g in groups]},
          open(OUT / "_meta.json", "w"))
