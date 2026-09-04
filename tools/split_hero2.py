# -*- coding: utf-8 -*-
"""Etape 2: isole la masse principale, puis regroupe les traits line-art entre eux."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers")
im = Image.open(SRC).convert("RGBA"); W, H = im.size
a = np.array(im)
lab = np.load(OUT / "_lab.npy")
meta = json.load(open(OUT / "_meta.json"))
comps = meta["groups"][0]["ids"]  # tous les ids

# recalcule bbox + taille par composante
ids, counts = np.unique(lab[lab > 0], return_counts=True)
info = {}
for i, c in zip(ids.tolist(), counts.tolist()):
    ys, xs = np.nonzero(lab == i)
    info[i] = {"n": c, "bbox": [int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1]}

main_id = max(info, key=lambda i: info[i]["n"])
rest = [i for i in info if i != main_id]
print(f"masse principale = #{main_id} ({info[main_id]['n']:,}px). {len(rest)} traits restants.")

# clustering des traits restants uniquement
GAP = 90
groups = [{"ids": [i], "bbox": list(info[i]["bbox"]), "n": info[i]["n"]} for i in rest]
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
groups.sort(key=lambda g: -(g["bbox"][2]-g["bbox"][0])*(g["bbox"][3]-g["bbox"][1]))
print(f"\n{len(groups)} amas line-art (gap {GAP}px):")
for k, g in enumerate(groups):
    b = g["bbox"]; cx = (b[0]+b[2])/2/W*100; cy = (b[1]+b[3])/2/H*100
    print(f'  [{k}] {b[2]-b[0]:>4}x{b[3]-b[1]:<4} @ {b[0]:>4},{b[1]:<4}  centre {cx:5.1f}%,{cy:5.1f}%  {g["n"]:>6,}px  {len(g["ids"]):>3} traits')
json.dump({"main_id": int(main_id), "W": W, "H": H,
           "groups": [{"ids": [int(x) for x in g["ids"]], "bbox": g["bbox"], "n": int(g["n"])} for g in groups]},
          open(OUT / "_clusters.json", "w"), indent=1)
