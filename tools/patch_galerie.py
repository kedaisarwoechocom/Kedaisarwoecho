# -*- coding: utf-8 -*-
"""Galerie maritime placee juste sous la note Google, en vague."""
import json
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")

# ═══ 1. HTML : la galerie remonte a l'interieur de la section avis ═══
h = ROOT / "index.html"
s = h.read_text(encoding="utf-8")

ancienne = '''  <!-- ══════════════ SECTION 5 — GALERIE (masquee tant qu'il n'y a pas de photos) ═══ -->
  <section class="gal" id="galeri" hidden>
    <h2 class="gal__title" data-i18n="gal.title">Suasana Kedai</h2>
    <ul class="gal__grid" id="galGrid"></ul>
  </section>

'''
assert ancienne in s
s = s.replace(ancienne, "", 1)

ancre = '''    <ul class="revw__quotes" id="rvQuotes"></ul>
  </section>'''
nouvelle = '''    <ul class="revw__quotes" id="rvQuotes"></ul>

    <!-- Galerie, juste sous la note. Disposition en vague : les cadres suivent une
         sinusoide, comme une ligne de flottaison. Masquee si aucune photo. -->
    <div class="gal" id="galeri" hidden>
      <h3 class="gal__title" id="galTitle">Dari Dapur Kami</h3>
      <ul class="gal__wave" id="galGrid"></ul>
      <p class="gal__note" id="galNote" hidden data-i18n="gal.note">
        Illustrations du kedai en attendant les photos du lieu.</p>
    </div>
  </section>'''
assert ancre in s
s = s.replace(ancre, nouvelle, 1)
h.write_text(s, encoding="utf-8")
print("index.html : galerie placee sous la note Google")

# ═══ 2. site.json : entrees par defaut + consigne claire ═══
p = ROOT / "data/site.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["_lisez_moi"] = [x for x in d["_lisez_moi"] if not x.startswith("galerie")]
i = d["_lisez_moi"].index("horaires_confirmes : false = le site affiche une mention 'a confirmer'.") \
    if "horaires_confirmes : false = le site affiche une mention 'a confirmer'." in d["_lisez_moi"] else 4
d["_lisez_moi"][i:i] = [
    "galerie         : la bande de photos sous la note Google.",
    "                  Deposez vos fichiers dans assets/img/lieu/ puis remplacez",
    "                  les entrees ci-dessous. 'source' vaut 'illustration' pour",
    "                  les dessins actuels et 'photo' pour vos vraies photos ;",
    "                  des qu'une seule entree est en 'photo', la mention",
    "                  'en attendant les photos du lieu' disparait.",
    "                  N'utilisez QUE vos propres photos : celles des avis Google",
    "                  appartiennent aux clients qui les ont postees, pas au kedai.",
    "                  L'onglet 'photos du proprietaire' sur Google et votre page",
    "                  Facebook sont les bonnes sources.",
    "galerie_titre   : le titre affiche au-dessus de la bande.",
]
d["galerie_titre"] = {
    "id": "Dari Dapur Kami", "en": "From our kitchen",
    "id_photos": "Suasana Kedai", "en_photos": "Inside the kedai",
}
d["galerie"] = [
    {"fichier": "seafood-tumpah",                "source": "illustration",
     "alt_id": "Seafood Tumpah, wajan besar untuk berbagi", "alt_en": "Seafood Tumpah, a big pan to share"},
    {"fichier": "lobster-saos-asam-manis-2",     "source": "illustration",
     "alt_id": "Lobster saus asam manis", "alt_en": "Sweet and sour lobster"},
    {"fichier": "kapiting-saos-asam-manis",      "source": "illustration",
     "alt_id": "Kepiting saus asam manis", "alt_en": "Sweet and sour crab"},
    {"fichier": "ikan-bakar",                    "source": "illustration",
     "alt_id": "Ikan bakar bumbu kecap", "alt_en": "Grilled fish with soy glaze"},
    {"fichier": "udang-asam-manis",              "source": "illustration",
     "alt_id": "Udang asam manis", "alt_en": "Sweet and sour prawns"},
    {"fichier": "kerang-asam-manis",             "source": "illustration",
     "alt_id": "Kerang hijau segar", "alt_en": "Fresh green clams"},
    {"fichier": "cumi-crispy",                   "source": "illustration",
     "alt_id": "Cumi goreng tepung renyah", "alt_en": "Crisp battered squid"},
    {"fichier": "mangut-lele",                   "source": "illustration",
     "alt_id": "Mangut lele kuah santan pedas", "alt_en": "Catfish in spicy coconut broth"},
]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"site.json : {len(d['galerie'])} entrees par defaut (illustrations), a remplacer par les photos")
