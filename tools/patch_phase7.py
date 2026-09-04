# -*- coding: utf-8 -*-
"""Phase 7 : securite (CSP), referencement local, performance, mise en ligne."""
from pathlib import Path

ROOT = Path(r"e:\c\projet\Kedaisarwoecho")

# ═══════════ 1. plus aucun attribut style en ligne ═══════════
h = ROOT / "index.html"
s = h.read_text(encoding="utf-8")
s = s.replace('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">',
              '<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false">')

# ═══════════ 2. en-tete : CSP, referencement, partage, preload ═══════════
old_head = '''<meta name="theme-color" content="#F4EDE7">'''
new_head = '''<meta name="theme-color" content="#F4EDE7">

<!-- Content-Security-Policy en balise : GitHub Pages ne permet pas d'en-tetes HTTP.
     Aucun script ni style en ligne, aucun domaine tiers hors la carte et la video. -->
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; base-uri 'none'; form-action 'none'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; manifest-src 'self'; media-src 'self'; frame-src https://www.openstreetmap.org https://www.youtube-nocookie.com; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">

<link rel="canonical" href="https://kedaisarwoechocom.github.io/Kedaisarwoecho/">
<meta property="og:type" content="restaurant.restaurant">
<meta property="og:site_name" content="Kedai Sarwo Echo">
<meta property="og:locale" content="id_ID">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:title" content="Kedai Sarwo Echo — Seafood Segar di Pantai Pulang Sawal">
<meta property="og:description" content="Lobster, kepiting, cumi dan ikan segar, langsung dari laut ke meja Anda. Di tepi Pantai Pulang Sawal, Tepus, Gunungkidul.">
<meta property="og:image" content="assets/img/brand/icon-512.png">
<meta name="twitter:card" content="summary_large_image">

<!-- l'illustration du hero est le plus gros element visible : on la demande tot -->
<link rel="preload" as="image" href="assets/img/hero/hero-plate-900.avif" type="image/avif"
      imagesrcset="assets/img/hero/hero-plate-560.avif 560w, assets/img/hero/hero-plate-900.avif 900w, assets/img/hero/hero-plate-1400.avif 1400w"
      imagesizes="(max-width:900px) 92vw, 58vw" fetchpriority="high">'''
assert old_head in s
s = s.replace(old_head, new_head, 1)
h.write_text(s, encoding="utf-8")
print("index.html : CSP, referencement, partage et preload poses")

# ═══════════ 3. la classe du sprite ═══════════
c = ROOT / "assets/css/main.css"
t = c.read_text(encoding="utf-8")
t = t.replace("[hidden] { display: none !important; }",
              "[hidden] { display: none !important; }\n"
              ".sprite { position: absolute; width: 0; height: 0; overflow: hidden; }")
c.write_text(t, encoding="utf-8")
print("main.css : classe .sprite (plus d'attribut style en ligne)")

# ═══════════ 4. app.js : --cut pose par CSSOM, et JSON-LD genere ═══════════
j = ROOT / "assets/js/app.js"
a = j.read_text(encoding="utf-8")

old_star = """        if (part) {
          const cut = Math.round((1 - (note - (i - 1))) * 100);
          box.insertAdjacentHTML('beforeend',
            `<span class="half" style="--cut:${cut}%">
               <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>
               <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>
             </span>`);
        } else {"""
new_star = """        if (part) {
          // pose par CSSOM et non en attribut style : la CSP interdit le style en ligne
          const sp = document.createElement('span');
          sp.className = 'half';
          sp.style.setProperty('--cut', Math.round((1 - (note - (i - 1))) * 100) + '%');
          sp.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>' +
                         '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>';
          box.appendChild(sp);
        } else {"""
assert old_star in a
a = a.replace(old_star, new_star, 1)

old_foot = "    footer() { $('#footYear').textContent = new Date().getFullYear(); },"
new_foot = """    footer() { $('#footYear').textContent = new Date().getFullYear(); },

    /* Donnees structurees Restaurant : c'est ce qui fait remonter le restaurant
       dans Google Maps. Genere depuis les fichiers de donnees pour qu'il n'y ait
       jamais deux verites a maintenir. */
    jsonLd() {
      if (!site || !data) return;
      const r = data.restaurant, l = site.lieu, av = site.avis;
      const jours = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const ld = {
        '@context': 'https://schema.org', '@type': 'Restaurant',
        name: r.nom,
        description: document.querySelector('meta[name="description"]')?.content || '',
        url: location.origin + location.pathname,
        image: new URL('assets/img/brand/icon-512.png', location.href).href,
        telephone: '+' + r.whatsapp,
        servesCuisine: ['Seafood', 'Indonesian'],
        address: {
          '@type': 'PostalAddress',
          streetAddress: [l.adresse_l1, l.adresse_l2].filter(Boolean).join(', '),
          addressLocality: 'Tepus', addressRegion: 'DI Yogyakarta',
          postalCode: '55881', addressCountry: 'ID',
        },
      };
      if (Number.isFinite(+l.latitude) && Number.isFinite(+l.longitude))
        ld.geo = { '@type': 'GeoCoordinates', latitude: +l.latitude, longitude: +l.longitude };
      if (av?.note && av?.nombre)
        ld.aggregateRating = { '@type': 'AggregateRating', ratingValue: av.note,
                               reviewCount: av.nombre, bestRating: 5 };
      // horaires publies seulement une fois confirmes : mieux vaut rien qu'un faux
      if (l.horaires_confirmes === true)
        ld.openingHoursSpecification = (l.horaires || []).map((x, i) => {
          const [o, f] = String(x.h).split(/\\s*[–-]\\s*/);
          return o && f ? { '@type': 'OpeningHoursSpecification', dayOfWeek: jours[i],
                            opens: o.replace('.', ':'), closes: f.replace('.', ':') } : null;
        }).filter(Boolean);
      const prix = data.plats.map(p => p.prix).filter(Number.isFinite);
      if (prix.length && r.afficher_les_prix === true)
        ld.priceRange = 'Rp ' + Math.min(...prix).toLocaleString('id-ID') +
                        ' - Rp ' + Math.max(...prix).toLocaleString('id-ID');

      const el = document.createElement('script');
      el.type = 'application/ld+json';
      el.textContent = JSON.stringify(ld);
      document.head.appendChild(el);
    },"""
assert old_foot in a
a = a.replace(old_foot, new_foot, 1)
a = a.replace("      this.story(); this.gallery(); this.reviews(); this.find(); this.footer();",
              "      this.story(); this.gallery(); this.reviews(); this.find(); this.footer();\n"
              "      if (!this._ld) { this._ld = true; this.jsonLd(); }")
j.write_text(a, encoding="utf-8")
print("app.js : etoiles sans style en ligne, donnees structurees Restaurant")

# ═══════════ 5. fichiers de mise en ligne ═══════════
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\n\n"
    "Sitemap: https://kedaisarwoechocom.github.io/Kedaisarwoecho/sitemap.xml\n", encoding="utf-8")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n'
    '    <loc>https://kedaisarwoechocom.github.io/Kedaisarwoecho/</loc>\n'
    '    <changefreq>monthly</changefreq>\n'
    '    <priority>1.0</priority>\n'
    '  </url>\n'
    '</urlset>\n', encoding="utf-8")
print(".nojekyll, robots.txt et sitemap.xml crees")
