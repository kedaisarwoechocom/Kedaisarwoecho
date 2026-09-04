# -*- coding: utf-8 -*-
"""Ajoute a app.js le rendu des sections 4 a 7 et du pied de page."""
from pathlib import Path

p = Path(r"e:\c\projet\Kedaisarwoecho\assets\js\app.js")
s = p.read_text(encoding="utf-8")
n = 0


def rep(a, b):
    global s, n
    assert a in s, "INTROUVABLE: " + a[:70]
    s = s.replace(a, b, 1)
    n += 1


# --- libelles ---
rep("""      'prov': 'harga sementara',
      'wa.hello': 'Halo Kedai Sarwo Echo! Saya ingin memesan'""",
    """      'gal.title': 'Suasana Kedai',
      'revw.title': 'Kata Mereka', 'revw.link': 'Baca ulasannya di Google',
      'find.title': 'Kunjungi Kami', 'find.addr': 'Alamat', 'find.hours': 'Jam buka',
      'find.hoursNote': 'Jam buka masih harus dikonfirmasi.',
      'find.contact': 'Kontak', 'find.route': 'Petunjuk arah',
      'find.mapNote': 'Titik peta masih perkiraan.',
      'foot.tag': 'Seafood segar, langsung dari laut ke meja Anda.',
      'foot.story': 'Cerita', 'foot.rights': 'Semua ilustrasi hidangan adalah milik kedai.',
      'prov': 'harga sementara',
      'wa.hello': 'Halo Kedai Sarwo Echo! Saya ingin memesan'""")

rep("""      'prov': 'provisional price',
      'wa.hello': 'Hello Kedai Sarwo Echo! I would like to order'""",
    """      'gal.title': 'Inside the kedai',
      'revw.title': 'What people say', 'revw.link': 'Read the reviews on Google',
      'find.title': 'Find Us', 'find.addr': 'Address', 'find.hours': 'Opening hours',
      'find.hoursNote': 'Opening hours still to be confirmed.',
      'find.contact': 'Contact', 'find.route': 'Get directions',
      'find.mapNote': 'The map pin is still approximate.',
      'foot.tag': 'Fresh seafood, straight from the sea to your table.',
      'foot.story': 'Our story', 'foot.rights': 'All dish illustrations belong to the kedai.',
      'prov': 'provisional price',
      'wa.hello': 'Hello Kedai Sarwo Echo! I would like to order'""")

# --- etat partage ---
rep("  let lang = 'id';\n  let data = null;",
    "  let lang = 'id';\n  let data = null;   // data/menu.json\n  let site = null;   // data/site.json")

rep("    if (data) { renderPicks(); Wheel.retitle(); }",
    "    if (data) { renderPicks(); Wheel.retitle(); }\n    if (site) Site.render();")

# --- module Site ---
rep("  /* ═══════════ tiroir de navigation ═══════════ */",
    """  /* ═══════════ sections 4 a 7 et pied de page ═══════════ */
  const Site = {
    render() {
      if (!site) return;
      this.story(); this.gallery(); this.reviews(); this.find(); this.footer();
    },

    story() {
      const h = site.histoire; if (!h) return;
      $('#stTitle').textContent  = lang === 'id' ? h.titre_id : h.titre_en;
      $('#stAccent').textContent = lang === 'id' ? h.accent_id : h.accent_en;
      const paras = (lang === 'id' ? h.texte_id : h.texte_en) || [];
      $('#stText').innerHTML = paras.map(x => `<p>${esc(x)}</p>`).join('');
      $('#stMarks').innerHTML = (h.reperes || []).map(r =>
        `<div><dt>${esc(lang === 'id' ? r.cle_id : r.cle_en)}</dt>` +
        `<dd>${esc(lang === 'id' ? r.valeur_id : r.valeur_en)}</dd></div>`).join('');
    },

    gallery() {
      const g = site.galerie || [];
      const sec = $('#galeri');
      sec.hidden = g.length === 0;          // pas de photos = pas de section
      if (!g.length) return;
      $('#galGrid').innerHTML = g.map(x => {
        const alt = esc(lang === 'id' ? (x.alt_id || '') : (x.alt_en || x.alt_id || ''));
        return `<li><img src="assets/img/lieu/${esc(x.fichier)}" alt="${alt}"
                  loading="lazy" decoding="async"></li>`;
      }).join('');
    },

    reviews() {
      const a = site.avis; if (!a) return;
      const note = Number(a.note) || 0;
      $('#rvNote').textContent = note.toLocaleString(lang === 'id' ? 'id-ID' : 'en-GB',
        { minimumFractionDigits: 1, maximumFractionDigits: 1 });
      $('#rvNb').textContent = a.nombre;
      $('#rvSrc').textContent = lang === 'id' ? a.source_id : a.source_en;
      $('#rvLink').href = a.lien || '#';

      const box = $('#rvStars'); box.innerHTML = '';
      for (let i = 1; i <= 5; i++) {
        const plein = note >= i, part = !plein && note > i - 1;
        if (part) {
          const cut = Math.round((1 - (note - (i - 1))) * 100);
          box.insertAdjacentHTML('beforeend',
            `<span class="half" style="--cut:${cut}%">
               <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>
               <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>
             </span>`);
        } else {
          box.insertAdjacentHTML('beforeend',
            `<svg class="${plein ? 'on' : ''}" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>`);
        }
      }
      box.setAttribute('aria-label',
        `${note} / 5 — ${a.nombre} ${lang === 'id' ? a.source_id : a.source_en}`);

      $('#rvQuotes').innerHTML = (a.citations || []).map(c =>
        `<li><blockquote>${esc(lang === 'id' ? (c.texte_id || c.texte) : (c.texte_en || c.texte))}</blockquote>` +
        `<cite>${esc(c.auteur || '')}</cite></li>`).join('');
    },

    find() {
      const l = site.lieu; if (!l) return;
      const adr = [l.adresse_l1, l.adresse_l2, l.adresse_l3].filter(Boolean);
      $('#fAddr').innerHTML = adr.map(esc).join('<br>');
      $('#footAddr').innerHTML = adr.map(esc).join('<br>');
      $('#fRoute').href = l.lien_itineraire || '#';
      $('#fWa').textContent = data?.restaurant?.whatsapp_affiche || '';

      $('#fHoursNote').hidden = l.horaires_confirmes === true;
      const auj = (new Date().getDay() + 6) % 7;   // 0 = lundi
      $('#fHours').innerHTML = (l.horaires || []).map((j, i) =>
        `<li class="${i === auj ? 'is-today' : ''}">
           <span>${esc(lang === 'id' ? j.jour_id : j.jour_en)}</span><b>${esc(j.h)}</b></li>`).join('');

      for (const [cle, li, a] of [['facebook', '#fFbLi', '#fFb'], ['instagram', '#fIgLi', '#fIg']]) {
        const url = l[cle];
        $(li).hidden = !url;
        if (url) $(a).href = url;
      }

      // Carte OpenStreetMap : libre, sans cle et sans traceur.
      const la = Number(l.latitude), lo = Number(l.longitude);
      if (Number.isFinite(la) && Number.isFinite(lo)) {
        const d = 0.008;
        $('#fMap').src = 'https://www.openstreetmap.org/export/embed.html?bbox=' +
          [lo - d, la - d / 1.6, lo + d, la + d / 1.6].map(v => v.toFixed(5)).join('%2C') +
          '&layer=mapnik&marker=' + la.toFixed(5) + '%2C' + lo.toFixed(5);
      }
      $('#fMapNote').hidden = l.coordonnees_a_verifier !== true;

      const vid = (site.video_youtube || '').trim();
      $('#vidWrap').hidden = !vid;
      if (vid) $('#vidFrame').src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(vid)}`;
    },

    footer() { $('#footYear').textContent = new Date().getFullYear(); },
  };

  /** echappe le texte venant des fichiers de donnees avant insertion en HTML */
  function esc(v) {
    return String(v ?? '').replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ═══════════ tiroir de navigation ═══════════ */""")

# --- chargement ---
rep("""    fetch('data/menu.json')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status))))
      .then(j => { data = j; applyLang(start); Wheel.init(); })
      .catch(err => {
        console.warn('menu.json indisponible :', err.message);
        applyLang(start);
        const fb = $('#menuFallback'), st = $('.menu__stage');
        if (fb) fb.hidden = false;
        if (st) st.hidden = true;
      });""",
    """    const charge = f => fetch(f).then(r => (r.ok ? r.json() : Promise.reject(new Error(f + ' HTTP ' + r.status))));

    Promise.allSettled([charge('data/menu.json'), charge('data/site.json')])
      .then(([m, sJ]) => {
        if (m.status === 'fulfilled') data = m.value;
        else {
          console.warn(m.reason.message);
          const fb = $('#menuFallback'), st = $('.menu__stage');
          if (fb) fb.hidden = false;
          if (st) st.hidden = true;
        }
        if (sJ.status === 'fulfilled') site = sJ.value; else console.warn(sJ.reason.message);
        applyLang(start);
        if (data) Wheel.init();
      });""")

p.write_text(s, encoding="utf-8")
print(f"app.js : {n} blocs ajoutes")
