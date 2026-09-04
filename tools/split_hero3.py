# -*- coding: utf-8 -*-
"""Decoupe finale de 2.png en calques animables.
Critere: le line-art decoratif est semi-transparent (alpha faible),
l'assiette/homard/serviette est opaque. Separation par seuil + composantes connexes.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers")
OUT.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
a = np.array(im).astype(np.int16)
alpha = a[..., 3]

core_seed = alpha > 225
lbl, n = ndi.label(core_seed, structure=np.ones((3,3)))
sizes = ndi.sum(core_seed, lbl, range(1, n+1))
core_id = int(np.argmax(sizes)) + 1
core = (lbl == core_id)
# recupere le bord antialiase du core (dilatation 3px) sans avaler le line-art
core_grown = ndi.binary_dilation(core, np.ones((3,3)), iterations=3)
core_full = core_grown & (alpha > 8)
print(f"masse principale: {core.sum():,}px -> {core_full.sum():,}px apres recuperation du bord")

deco = (alpha > 8) & ~core_full
dl, dn = ndi.label(deco, structure=np.ones((3,3)))
objs = ndi.find_objects(dl)
comps = []
for i, sl in enumerate(objs, start=1):
    if sl is None: continue
    npx = int((dl[sl] == i).sum())
    if npx < 40: continue
    comps.append({"id": i, "n": npx,
                  "bbox": [sl[1].start, sl[0].start, sl[1].stop, sl[0].stop]})
print(f"{len(comps)} traits decoratifs (>=40px)")

GAP = 70
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
                groups[i]["ids"] += groups[j]["ids"]; groups[i]["n"] += groups[j]["n"]
                groups[j] = None; changed = True
    groups = [g for g in groups if g is not None]
groups = [g for g in groups if g["n"] >= 300]
groups.sort(key=lambda g: (g["bbox"][1], g["bbox"][0]))

print(f"\n{len(groups)} amas line-art:")
for k, g in enumerate(groups):
    b = g["bbox"]
    print(f'  [{k}] {b[2]-b[0]:>4}x{b[3]-b[1]:<4} @ {b[0]:>4},{b[1]:<5} {g["n"]:>6,}px {len(g["ids"]):>3} traits')
np.save(OUT/"_deco_lbl.npy", dl); np.save(OUT/"_core.npy", core_full)
json.dump({"W":W,"H":H,"groups":[{"ids":[int(x) for x in g["ids"]],"bbox":[int(v) for v in g["bbox"]],"n":int(g["n"])} for g in groups]},
          open(OUT/"_clusters.json","w"), indent=1)
