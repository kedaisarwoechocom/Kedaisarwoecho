# -*- coding: utf-8 -*-
"""app.js : horaires en une ligne, signature du pied de page, nettoyage de la
bascule de langue devenue invisible, donnees Google adaptees."""
from pathlib import Path

p = Path(r"e:\c\projet\Kedaisarwoecho\assets\js\app.js")
s = p.read_text(encoding="utf-8")
n = 0


def rep(a, b):
    global s, n
    assert a in s, "INTROUVABLE: " + a[:70]
    s = s.replace(a, b, 1)
    n += 1


# ── signature du pied de page, mot pour mot ce que le proprietaire a ecrit ──
rep("      'foot.tag': 'Seafood segar, langsung dari laut ke meja Anda.',",
    "      'foot.tag': 'Masakan Indonesia dan ikan terbaik, lebih segar dan lebih lezat.',")
rep("      'foot.tag': 'Fresh seafood, straight from the sea to your table.',",
    "      'foot.tag': 'For great Indonesian food and fish, fresher and tastier.',")

# ── la mention 'a confirmer' n'a plus de raison d'etre ──
rep("      'find.hoursNote': 'Jam buka masih harus dikonfirmasi.',\n", "")
rep("      'find.hoursNote': 'Opening hours still to be confirmed.',\n", "")

# ── il n'y a plus de boutons de langue a mettre a jour ──
rep("""    $$('.lang__btn').forEach(b => {
      const on = b.dataset.lang === lang;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', String(on));
    });
""", "")
rep("    $$('.lang__btn').forEach(b => b.addEventListener('click', () => applyLang(b.dataset.lang)));\n", "")

# ── horaires : une phrase au lieu d'un tableau de sept lignes ──
rep("""      $('#fHoursNote').hidden = l.horaires_confirmes === true;
      const auj = (new Date().getDay() + 6) % 7;   // 0 = lundi
      $('#fHours').innerHTML = (l.horaires || []).map((j, i) =>
        `<li class="${i === auj ? 'is-today' : ''}">
           <span>${esc(lang === 'id' ? j.jour_id : j.jour_en)}</span><b>${esc(j.h)}</b></li>`).join('');
""",
    """      const ht = l.horaires_texte || {};
      $('#fHoursLine').textContent = (lang === 'id' ? ht.id : ht.en) || '';
""")

# ── donnees Google : ouvert tous les jours, une seule specification ──
rep("""      // horaires publies seulement une fois confirmes : mieux vaut rien qu'un faux
      if (l.horaires_confirmes === true)
        ld.openingHoursSpecification = (l.horaires || []).map((x, i) => {
          const [o, f] = String(x.h).split(/\\s*[–-]\\s*/);
          return o && f ? { '@type': 'OpeningHoursSpecification', dayOfWeek: jours[i],
                            opens: o.replace('.', ':'), closes: f.replace('.', ':') } : null;
        }).filter(Boolean);""",
    """      // horaires publies seulement une fois confirmes : mieux vaut rien qu'un faux
      if (l.horaires_confirmes === true && l.ouverture && l.fermeture)
        ld.openingHoursSpecification = [{
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: jours, opens: l.ouverture, closes: l.fermeture,
        }];""")

p.write_text(s, encoding="utf-8")
print(f"app.js : {n} modifications")
