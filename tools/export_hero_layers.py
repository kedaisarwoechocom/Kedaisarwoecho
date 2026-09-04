# -*- coding: utf-8 -*-
"""Export final des calques hero + layers.json (positions en % de la compo)."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers")
im = Image.open(SRC).convert("RGBA"); W,H = im.size
arr = np.array(im)
core = np.load(OUT/"_core.npy"); napkin = np.load(OUT/"_napkin.npy")
lbl = np.load(OUT/"_lineart_lbl.npy")

comps=[]
for i,sl in enumerate(ndi.find_objects(lbl), start=1):
    if sl is None: continue
    n=int((lbl[sl]==i).sum())
    if n<30: continue
    comps.append({"ids":[i],"n":n,"bbox":[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop]})
GAP=40
def near(b1,b2,g): return not (b1[2]+g<b2[0] or b2[2]+g<b1[0] or b1[3]+g<b2[1] or b2[3]+g<b1[1])
groups=comps; ch=True
while ch:
    ch=False
    for i in range(len(groups)):
        if groups[i] is None: continue
        for j in range(i+1,len(groups)):
            if groups[j] is None: continue
            if near(groups[i]["bbox"],groups[j]["bbox"],GAP):
                b1,b2=groups[i]["bbox"],groups[j]["bbox"]
                groups[i]["bbox"]=[min(b1[0],b2[0]),min(b1[1],b2[1]),max(b1[2],b2[2]),max(b1[3],b2[3])]
                groups[i]["ids"]+=groups[j]["ids"]; groups[i]["n"]+=groups[j]["n"]; groups[j]=None; ch=True
    groups=[g for g in groups if g is not None]
groups=[g for g in groups if g["n"]>=250]

# nommage par position/taille
def name_of(g):
    b=g["bbox"]; w=b[2]-b[0]; h=b[3]-b[1]
    cx=(b[0]+b[2])/2/W; cy=(b[1]+b[3])/2/H
    if g["n"]>15000 and cx>.6 and cy<.4: return "stamp"
    if cy>.7: return "shell"
    if cx<.3 and cy<.3: return "splash"
    if cx<.2: return "lemon-left"
    if cx>.75: return "lemon-right"
    return "lemon-top"
for g in groups: g["name"]=name_of(g)
seen={}
for g in groups:
    seen[g["name"]]=seen.get(g["name"],0)+1
    if seen[g["name"]]>1: g["name"]=f'{g["name"]}-{seen[g["name"]]}'

def save(mask, path, pad=2):
    ys,xs=np.nonzero(mask)
    if len(xs)==0: return None
    x0,y0,x1,y1=max(0,xs.min()-pad),max(0,ys.min()-pad),min(W,xs.max()+1+pad),min(H,ys.max()+1+pad)
    sub=arr[y0:y1,x0:x1].copy()
    sub[...,3]=np.where(mask[y0:y1,x0:x1], sub[...,3], 0)
    Image.fromarray(sub).save(path, optimize=True)
    return {"file":path.name,"px":[int(x0),int(y0),int(x1),int(y1)],
            "left_pct":round(x0/W*100,3),"top_pct":round(y0/H*100,3),
            "w_pct":round((x1-x0)/W*100,3),"h_pct":round((y1-y0)/H*100,3),
            "w":int(x1-x0),"h":int(y1-y0)}

layers={"source":"2.png","comp_w":W,"comp_h":H,"layers":{}}
layers["layers"]["plate"]=save(core|napkin, OUT/"hero-plate.png")
for g in groups:
    m=np.isin(lbl, g["ids"])
    layers["layers"][g["name"]]=save(m, OUT/f'hero-{g["name"]}.png')
json.dump(layers, open(OUT/"layers.json","w"), indent=2)
print(f"{len(layers['layers'])} calques exportes:")
for k,v in layers["layers"].items():
    print(f'  {k:14} {v["w"]:>4}x{v["h"]:<4}  @ {v["left_pct"]:>6.2f}% , {v["top_pct"]:>6.2f}%   larg {v["w_pct"]:>5.2f}%')
