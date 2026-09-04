# -*- coding: utf-8 -*-
"""Mesure geometrique des maquettes: bords, cartes, rayons, positions texte."""
import numpy as np
from PIL import Image
from pathlib import Path
from scipy import ndimage as ndi

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed")

def near(a, c, tol=10):
    return (np.abs(a[...,0].astype(int)-c[0])<tol) & (np.abs(a[...,1].astype(int)-c[1])<tol) & (np.abs(a[...,2].astype(int)-c[2])<tol)

def dominant(a, box):
    x0,y0,x1,y1 = box
    px = a[y0:y1, x0:x1].reshape(-1,3)
    cols, cnt = np.unique(px, axis=0, return_counts=True)
    return [(tuple(int(v) for v in cols[i]), int(cnt[i])) for i in np.argsort(-cnt)[:4]]

# ---------------- HERO ----------------
im = Image.open(SRC/"halo.jpeg").convert("RGB"); A = np.array(im); H,W,_ = A.shape
print(f"=== halo.jpeg {W}x{H} ===")
print("fond page (coin)   :", dominant(A,(0,0,40,40))[0])
print("panneau (centre-g) :", dominant(A,(600,150,700,200))[0])
# bords du panneau creme: balayage depuis les bords sur la ligne mediane
mid = H//2
row = A[mid]
def edge(row, frm, to, step):
    base = row[frm]
    for x in range(frm, to, step):
        if np.abs(row[x].astype(int)-base.astype(int)).max() > 12: return x
    return None
L = edge(row, 0, W//2, 1); R = edge(row, W-1, W//2, -1)
col = A[:, 60]
T = edge(col, 0, H//2, 1); B = edge(col, H-1, H//2, -1)
print(f"panneau creme      : x {L}..{R}  y {T}..{B}   (marge G/D {L}/{W-1-R}, H/B {T}/{H-1-B})")

# bouton vert: cherche les pixels sauge
sage = near(A, (92,118,109), 26) | near(A, (95,120,110), 26)
lb, n = ndi.label(sage)
objs = ndi.find_objects(lb)
cands = []
for i, sl in enumerate(objs, start=1):
    npx = int((lb[sl]==i).sum())
    if npx < 2000: continue
    cands.append((npx, sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
cands.sort(reverse=True)
for npx,x0,y0,x1,y1 in cands[:3]:
    print(f"bloc sauge         : {x1-x0}x{y1-y0} @ {x0},{y0}  ({npx}px)")

# rouge du logo / accents
red = near(A,(203,13,13),40)
lb2,_ = ndi.label(red)
for i, sl in enumerate(ndi.find_objects(lb2), start=1):
    npx=int((lb2[sl]==i).sum())
    if npx>1500: print(f"bloc rouge         : {sl[1].stop-sl[1].start}x{sl[0].stop-sl[0].start} @ {sl[1].start},{sl[0].start} ({npx}px)")

# ---------------- SECTION 2 ----------------
im2 = Image.open(SRC/"section2.jpeg").convert("RGB"); B2 = np.array(im2); H2,W2,_ = B2.shape
print(f"\n=== section2.jpeg {W2}x{H2} ===")
print("hors panneau       :", dominant(B2,(0,0,30,10))[0])
print("panneau            :", dominant(B2,(760,700,860,760))[0])
print("carte rose         :", dominant(B2,(250,300,330,340))[0])
rose = near(B2,(227,218,212),9)
lb3,_ = ndi.label(rose)
cards=[]
for i, sl in enumerate(ndi.find_objects(lb3), start=1):
    npx=int((lb3[sl]==i).sum())
    if npx>20000: cards.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop, npx))
cards.sort()
for k,(x0,y0,x1,y1,npx) in enumerate(cards):
    print(f"carte {k+1}            : {x1-x0}x{y1-y0} @ {x0},{y0}")
if len(cards)>1: print(f"gouttiere entre cartes: {cards[1][0]-cards[0][2]}px")
