# -*- coding: utf-8 -*-
"""Decoupe finale 2.png -> calques animables.
1. core   = plus grande composante opaque (assiette + homard)
2. deco   = le reste (serviette + line-art)
3. erosion morphologique: la serviette (bloc plein) survit, les traits fins disparaissent
4. line-art = deco - serviette, puis regroupement spatial en elements nommes
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers"); OUT.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
arr = np.array(im); alpha = arr[..., 3]

def disk(r):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    return (x*x + y*y) <= r*r

core = np.load(OUT/"_core.npy")
deco = (alpha > 8) & ~core

seed = ndi.binary_erosion(deco, disk(5))
napkin = ndi.binary_propagation(seed, mask=deco)
lineart = deco & ~napkin
lineart = ndi.binary_opening(lineart, disk(1))
print(f"core {core.sum():,}  serviette {napkin.sum():,}  line-art {lineart.sum():,}")

dl, dn = ndi.label(lineart, structure=np.ones((3,3)))
comps = []
for i, sl in enumerate(ndi.find_objects(dl), start=1):
    if sl is None: continue
    n = int((dl[sl] == i).sum())
    if n < 30: continue
    comps.append({"id": i, "n": n, "bbox": [sl[1].start, sl[0].start, sl[1].stop, sl[0].stop]})
print(f"{len(comps)} traits line-art")

GAP = 80
groups = [{"ids":[c["id"]], "bbox":list(c["bbox"]), "n":c["n"]} for c in comps]
def near(b1,b2,g): return not (b1[2]+g<b2[0] or b2[2]+g<b1[0] or b1[3]+g<b2[1] or b2[3]+g<b1[1])
ch=True
while ch:
    ch=False
    for i in range(len(groups)):
        if groups[i] is None: continue
        for j in range(i+1,len(groups)):
            if groups[j] is None: continue
            if near(groups[i]["bbox"],groups[j]["bbox"],GAP):
                b1,b2=groups[i]["bbox"],groups[j]["bbox"]
                groups[i]["bbox"]=[min(b1[0],b2[0]),min(b1[1],b2[1]),max(b1[2],b2[2]),max(b1[3],b2[3])]
                groups[i]["ids"]+=groups[j]["ids"]; groups[i]["n"]+=groups[j]["n"]
                groups[j]=None; ch=True
    groups=[g for g in groups if g is not None]
groups=[g for g in groups if g["n"]>=250]
groups.sort(key=lambda g:-(g["bbox"][2]-g["bbox"][0])*(g["bbox"][3]-g["bbox"][1]))
print(f"\n{len(groups)} elements line-art:")
for k,g in enumerate(groups):
    b=g["bbox"]
    print(f'  [{k}] {b[2]-b[0]:>4}x{b[3]-b[1]:<4} @ {b[0]:>4},{b[1]:<5} centre {(b[0]+b[2])/2/W*100:5.1f}%,{(b[1]+b[3])/2/H*100:5.1f}%  {g["n"]:>6,}px')

np.save(OUT/"_napkin.npy", napkin); np.save(OUT/"_lineart_lbl.npy", dl)
json.dump({"W":W,"H":H,"groups":[{"ids":[int(x) for x in g["ids"]],"bbox":[int(v) for v in g["bbox"]],"n":int(g["n"])} for g in groups]},
          open(OUT/"_lineart_clusters.json","w"), indent=1)

vis=np.full((H,W,3),(244,237,231),np.uint8)
vis[napkin]=(206,188,178); vis[core]=(90,113,104); vis[lineart]=(172,26,25)
Image.fromarray(vis).resize((700,619)).save(OUT/"_preview_mask2.png")
