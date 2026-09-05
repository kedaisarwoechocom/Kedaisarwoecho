/* ============================================================
   Kedai Sarwo Echo — carte numerique (page du QR code)
   Les clients cochent leurs plats, la liste part en un seul message WhatsApp.
   Memes fichiers de donnees que le site : data/menu.json et data/site.json.
   ============================================================ */
(() => {
  'use strict';

  const T = {
    id: {
      'carte.skip': 'Langsung ke daftar hidangan',
      'carte.back': 'Situs',
      'carte.title': 'Kartu Menu',
      'carte.hint': 'Semua hidangan Kedai Sarwo Echo, lengkap dengan fotonya. Silakan lihat-lihat dengan tenang.',
      'carte.top': 'Kembali ke atas halaman',
      'carte.all': 'Semua',
      'carte.vide': 'Tidak ada hidangan di kategori ini.',
      'carte.err': 'Kartu menu tidak dapat dimuat.',
      'carte.errCta': 'Hubungi kami lewat WhatsApp',
      'prov': 'harga sementara',
    },
    en: {
      'carte.skip': 'Skip to the dishes',
      'carte.back': 'Website',
      'carte.title': 'Menu Card',
      'carte.hint': 'Every dish at Kedai Sarwo Echo, with photos. Take your time browsing.',
      'carte.top': 'Back to top of page',
      'carte.all': 'All',
      'carte.vide': 'No dishes in this category.',
      'carte.err': 'The menu card could not be loaded.',
      'carte.errCta': 'Reach us on WhatsApp',
      'prov': 'provisional price',
    },
  };

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  let lang = 'id', menu = null, site = null, cat = 'all';

  const t = k => T[lang][k] ?? k;
  const rupiah = n => 'Rp ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  const nom  = p => (lang === 'id' ? p.nom_id : p.nom_en);
  const desc = p => (lang === 'id' ? p.desc_id : p.desc_en);
  const img  = (slug, w) => `assets/img/dishes/${slug}-${w}`;
  const prixVisible = () => menu?.restaurant?.afficher_les_prix === true;
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* Contact seulement : la carte ne prend pas de commande, elle presente. */
  const waLien = () => `https://wa.me/${menu?.restaurant?.whatsapp || '6281328767156'}`;

  /* ---------- rendu ---------- */
  function chips() {
    const cats = [{ id: 'all', nom_id: t('carte.all'), nom_en: t('carte.all') }, ...menu.categories];
    $('#chips').innerHTML = cats.map(c => {
      const n = c.id === 'all' ? c.nom_id : (lang === 'id' ? c.nom_id : c.nom_en);
      const combien = c.id === 'all' ? menu.plats.length
                                     : menu.plats.filter(p => p.categorie === c.id).length;
      return `<li><button type="button" class="chip" data-cat="${esc(c.id)}"
                aria-pressed="${c.id === cat}">${esc(n)} <span aria-hidden="true">&middot; ${combien}</span></button></li>`;
    }).join('');
  }

  function cartes() {
    const liste = cat === 'all' ? menu.plats : menu.plats.filter(p => p.categorie === cat);
    $('#vide').hidden = liste.length > 0;
    $('#liste').innerHTML = liste.map(p => {
      const c = menu.categories.find(x => x.id === p.categorie);
      const nomCat = c ? (lang === 'id' ? c.nom_id : c.nom_en) : '';
      const prix = prixVisible()
        ? `<p class="carte__prix">${rupiah(p.prix)} / ${esc(p.unite)}` +
          (p.prix_provisoire ? ` <span class="carte__prov">(${t('prov')})</span>` : '') + '</p>'
        : '';
      return `<li class="carte" data-id="${esc(p.image)}">
        <div class="carte__img">
          <picture>
            <source type="image/avif" srcset="${img(p.image, 240)}.avif">
            <source type="image/webp" srcset="${img(p.image, 240)}.webp">
            <img src="${img(p.image, 480)}.png" alt="${esc(nom(p))}" width="240" height="240"
                 loading="lazy" decoding="async">
          </picture>
        </div>
        <div class="carte__corps">
          <p class="carte__cat">${esc(nomCat)}</p>
          <h2 class="carte__nom">${esc(nom(p))}</h2>
          <p class="carte__desc">${esc(desc(p))}</p>
          ${prix}
        </div>
      </li>`;
    }).join('');
  }

  function pied() {
    const l = site?.lieu, r = menu?.restaurant;
    if (l) {
      const ht = l.horaires_texte || {};
      $('#cfHoraires').textContent = (lang === 'id' ? ht.id : ht.en) || '';
      $('#cfAdresse').innerHTML = [l.adresse_l1, l.adresse_l2, l.adresse_l3]
        .filter(Boolean).map(esc).join('<br>');
      $('#chLieu').textContent = l.adresse_l1 || '';
    }
    if (r) {
      $('#cfTel').textContent = r.whatsapp_affiche || '';
      $('#cfWa').href = waLien();
      $('#errWa').href = waLien();
    }
  }

  function libelles() {
    document.documentElement.lang = lang;
    $$('[data-i18n]').forEach(el => {
      const v = T[lang][el.dataset.i18n];
      if (v != null) el.textContent = v;
    });
    $$('[data-i18n-label]').forEach(el => {
      const v = T[lang][el.dataset.i18nLabel];
      if (v != null) el.setAttribute('aria-label', v);
    });
  }

  function tout() { libelles(); chips(); cartes(); pied(); }

  /* ---------- revenir en haut ---------- */
  /* Efface au repos : la carte se lit en descendant, un bouton permanent
     mangerait une main de contenu sur un telephone. */
  function initHaut() {
    const b = $('#toTop');
    if (!b) return;
    const SEUIL = 620, REPOS = 1600;
    let minuteur = 0;
    const cacher = () => b.classList.remove('is-on');
    const montrer = () => {
      clearTimeout(minuteur);
      if (scrollY < SEUIL) { cacher(); return; }
      b.classList.add('is-on');
      minuteur = setTimeout(cacher, REPOS);
    };
    const doux = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    addEventListener('scroll', montrer, { passive: true });
    b.addEventListener('click', () => {
      clearTimeout(minuteur); cacher();
      scrollTo({ top: 0, behavior: doux ? 'smooth' : 'auto' });
    });
    b.addEventListener('pointerenter', () => clearTimeout(minuteur));
    b.addEventListener('pointerleave', montrer);
  }

  /* ---------- interactions ---------- */
  function init() {
    document.addEventListener('click', e => {
      const chip = e.target.closest('.chip');
      if (chip) { cat = chip.dataset.cat; chips(); cartes(); }
    });

    initHaut();

    const forced = new URLSearchParams(location.search).get('lang');
    const navEn = (navigator.language || '').toLowerCase().startsWith('en');
    let sauve = null;
    try { sauve = localStorage.getItem('kse-lang'); } catch (_) {}
    lang = (T[forced] ? forced : null) || sauve || (navEn ? 'en' : 'id');

    const charge = f => fetch(f).then(r => (r.ok ? r.json() : Promise.reject(new Error(f))));
    Promise.allSettled([charge('data/menu.json'), charge('data/site.json')])
      .then(([m, s]) => {
        if (m.status !== 'fulfilled') {
          libelles(); pied(); $('#err').hidden = false; $('#liste').hidden = true;
          $('.filtres').hidden = true;
          console.warn(m.reason.message);
          return;
        }
        menu = m.value;
        if (s.status === 'fulfilled') site = s.value;
        tout();
      });
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
