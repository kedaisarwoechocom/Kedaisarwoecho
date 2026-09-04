# -*- coding: utf-8 -*-
"""Re-extraction des decors line-art de 2.png par signature couleur.
Le trait decoratif est NEUTRE (saturation ~0) et semi-transparent ; la serviette
est chaude (sat ~36) et l'assiette saturee (sat ~133). Aucun traitement
morphologique : les traits fins restent intacts.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = Path(r"e:\c\projet\Kedaisarwoecho\wetransfer_kedai-sarwo-echo_2026-09-04_0958\BC removed\2.png")
OUT = Path(r"e:\c\projet\Kedaisarwoecho\build\hero-layers")
im = Image.open(SRC).convert("RGBA"); W, H = im.size
a = np.array(im).astype(int)
rgb, al = a[..., :3], a[..., 3]
sat = rgb.max(axis=2) - rgb.min(axis=2)
lum = rgb.mean(axis=2)

# regions relevees sur la compo (x0,y0,x1,y1)
REG = {
  "stamp":       (1105,  10, 1740,  515),
  "lemon-top":   ( 830,  95, 1070,  250),
  "splash":      ( 315, 150,  495,  305),
  "lemon-right": (1480, 565, 1635,  745),
  "lemon-left":  (  10, 595,  160,  790),
  "shell":       ( 295,1165,  500, 1405),
}
SAT_MAX, A_MAX, L_MIN, L_MAX = 20, 246, 120, 228   # L_MAX ecarte le bord blanc de l assiette

# le bord de l'assiette est blanc, donc peu sature lui aussi : on l'ecarte avec
# le masque de la masse principale, dilate pour couvrir son ombre douce.
core = np.load(OUT / "_core.npy")
core = ndi.binary_dilation(core, np.ones((3, 3)), iterations=8)

layers = {}
for name, (x0, y0, x1, y1) in REG.items():
    m = np.zeros((H, W), bool)
    sub = (al[y0:y1, x0:x1] > 10) & (sat[y0:y1, x0:x1] <= SAT_MAX) \
        & (al[y0:y1, x0:x1] <= A_MAX) & (lum[y0:y1, x0:x1] >= L_MIN) & (lum[y0:y1, x0:x1] <= L_MAX) & ~core[y0:y1, x0:x1]
    m[y0:y1, x0:x1] = sub
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{name}: VIDE"); continue
    bx = (int(xs.min())-1, int(ys.min())-1, int(xs.max())+2, int(ys.max())+2)
    crop = a[bx[1]:bx[3], bx[0]:bx[2]].copy()
    crop[..., 3] = np.where(m[bx[1]:bx[3], bx[0]:bx[2]], crop[..., 3], 0)
    Image.fromarray(crop.astype(np.uint8)).save(OUT / f"hero-{name}.png", optimize=True)
    layers[name] = {"file": f"hero-{name}.png", "px": list(bx),
        "left_pct": round(bx[0]/W*100, 3), "top_pct": round(bx[1]/H*100, 3),
        "w_pct": round((bx[2]-bx[0])/W*100, 3), "h_pct": round((bx[3]-bx[1])/H*100, 3),
        "w": bx[2]-bx[0], "h": bx[3]-bx[1]}
    print(f"{name:12} {bx[2]-bx[0]:>4}x{bx[3]-bx[1]:<4} @ {bx[0]:>4},{bx[1]:<4}  {int(sub.sum()):>6} px de trait")

# l'assiette reste celle deja extraite (core + serviette), on ne la retouche pas
old = json.load(open(OUT / "layers.json"))
old["layers"].update(layers)
json.dump(old, open(OUT / "layers.json", "w"), indent=2)

# apercu compose sur creme
canvas = Image.new("RGBA", (W, H), (244, 237, 231, 255))
for k, v in old["layers"].items():
    lay = Image.open(OUT / v["file"]).convert("RGBA")
    canvas.alpha_composite(lay, (v["px"][0], v["px"][1]))
canvas.convert("RGB").resize((640, 566)).save(OUT / "_recompose2.png")
print("apercu -> _recompose2.png")
