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
      'carte.hint': 'Pilih hidangan yang Anda inginkan, isi nomor meja Anda, lalu tekan tombol pesan di bawah. Daftar pilihan Anda dikirim langsung ke dapur kami lewat WhatsApp, lengkap dengan nomor meja Anda.',
      'carte.table': 'Nomor meja',
      'carte.tableAide': 'Isi dulu nomor meja Anda, supaya pesanan diantar ke meja yang tepat.',
      'carte.top': 'Kembali ke atas halaman',
      'carte.all': 'Semua',
      'carte.add': 'Pilih',
      'carte.added': 'Dipilih',
      'carte.one': 'hidangan dipilih',
      'carte.many': 'hidangan dipilih',
      'carte.clear': 'Kosongkan',
      'carte.send': 'Kirim pesanan',
      'carte.vide': 'Tidak ada hidangan di kategori ini.',
      'carte.err': 'Kartu menu tidak dapat dimuat.',
      'carte.errCta': 'Hubungi kami lewat WhatsApp',
      'prov': 'harga sementara',
      'wa.hello': 'Halo Kedai Sarwo Echo! Saya ingin memesan',
      'wa.meja': 'Nomor meja',
      'wa.merci': 'Terima kasih!',
    },
    en: {
      'carte.skip': 'Skip to the dishes',
      'carte.back': 'Website',
      'carte.title': 'Menu Card',
      'carte.hint': 'Choose the dishes you would like, enter your table number, then tap the order button below. Your list is sent straight to our kitchen on WhatsApp, together with your table number.',
      'carte.table': 'Table no.',
      'carte.tableAide': 'Please enter your table number first, so your order reaches the right table.',
      'carte.top': 'Back to top of page',
      'carte.all': 'All',
      'carte.add': 'Choose',
      'carte.added': 'Chosen',
      'carte.one': 'dish chosen',
      'carte.many': 'dishes chosen',
      'carte.clear': 'Clear',
      'carte.send': 'Send order',
      'carte.vide': 'No dishes in this category.',
      'carte.err': 'The menu card could not be loaded.',
      'carte.errCta': 'Reach us on WhatsApp',
      'prov': 'provisional price',
      'wa.hello': 'Hello Kedai Sarwo Echo! I would like to order',
      'wa.meja': 'Table number',
      'wa.merci': 'Thank you!',
    },
  };

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  let lang = 'id', menu = null, site = null, cat = 'all';
  const choisis = new Set();

  const t = k => T[lang][k] ?? k;
  const rupiah = n => 'Rp ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  const nom  = p => (lang === 'id' ? p.nom_id : p.nom_en);
  const desc = p => (lang === 'id' ? p.desc_id : p.desc_en);
  const img  = (slug, w) => `assets/img/dishes/${slug}-${w}`;
  const prixVisible = () => menu?.restaurant?.afficher_les_prix === true;
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const waLien = msg =>
    `https://wa.me/${menu?.restaurant?.whatsapp || '6281328767156'}?text=${encodeURIComponent(msg)}`;

  /** numero de table saisi, nettoye ; chaine vide s'il manque */
  const meja = () => ($('#meja')?.value || '').trim().slice(0, 4);

  /** un seul message pour toute la selection, numero de table en tete */
  function messageCommande() {
    const lignes = menu.plats.filter(p => choisis.has(p.image)).map(p => {
      const q = prixVisible() ? `  (${rupiah(p.prix)}/${p.unite})` : '';
      return `• ${nom(p)}${q}`;
    });
    // la table d'abord : c'est la premiere chose que la cuisine doit lire
    const n = meja();
    const tete = n ? `${t('wa.hello')} :\n${t('wa.meja')} : ${n}` : `${t('wa.hello')} :`;
    return `${tete}\n${lignes.join('\n')}\n\n${t('wa.merci')}`;
  }

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
      const on = choisis.has(p.image);
      return `<li class="carte${on ? ' is-on' : ''}" data-id="${esc(p.image)}">
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
        <button type="button" class="carte__add" data-id="${esc(p.image)}"
                aria-pressed="${on}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#${on ? 'i-check' : 'i-plus'}"/></svg>
          <span>${on ? t('carte.added') : t('carte.add')}</span>
        </button>
      </li>`;
    }).join('');
  }

  /** met a jour UNE carte, sans toucher au reste de la liste */
  function majCarte(id) {
    const li = $(`.carte[data-id="${CSS.escape(id)}"]`);
    if (!li) return;
    const on = choisis.has(id);
    li.classList.toggle('is-on', on);
    const b = $('.carte__add', li);
    b.setAttribute('aria-pressed', String(on));
    $('use', b).setAttribute('href', on ? '#i-check' : '#i-plus');
    $('span', b).textContent = on ? t('carte.added') : t('carte.add');
  }

  function panier() {
    const n = choisis.size;
    $('#panier').hidden = n === 0;
    $('#panierNb').textContent = n;
    $('#panierMot').textContent = n > 1 ? t('carte.many') : t('carte.one');
    if (n) $('#panierCta').href = waLien(messageCommande());
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
      $('#cfWa').href = waLien(t('wa.hello') + ' :');
      $('#errWa').href = waLien(t('wa.hello') + ' :');
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

  function tout() { libelles(); chips(); cartes(); panier(); pied(); }

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
      if (chip) { cat = chip.dataset.cat; chips(); cartes(); return; }

      const add = e.target.closest('.carte__add');
      if (add) {
        const id = add.dataset.id;
        choisis.has(id) ? choisis.delete(id) : choisis.add(id);
        try { sessionStorage.setItem('kse-choix', JSON.stringify([...choisis])); } catch (_) {}
        majCarte(id); panier();
        return;
      }

      // Sans numero de table la cuisine sait quoi preparer, mais pas ou le
      // porter : on bloque l'envoi et on montre ou taper.
      const envoi = e.target.closest('#panierCta');
      if (envoi) {
        if (!meja()) {
          e.preventDefault();
          $('#panier').classList.add('is-manquant');
          $('#meja')?.focus();
          return;
        }
        envoi.href = waLien(messageCommande());   // toujours le message le plus frais
        return;
      }

      if (e.target.closest('#panierVider')) {
        const vides = [...choisis];
        choisis.clear();
        try { sessionStorage.removeItem('kse-choix'); } catch (_) {}
        vides.forEach(majCarte); panier();
      }
    });

    const champ = $('#meja');
    if (champ) {
      try { champ.value = sessionStorage.getItem('kse-meja') || ''; } catch (_) {}
      champ.addEventListener('input', () => {
        // chiffres et lettres seulement : certaines tables sont numerotees A1, B2
        champ.value = champ.value.replace(/[^0-9A-Za-z]/g, '').slice(0, 4).toUpperCase();
        try { sessionStorage.setItem('kse-meja', champ.value); } catch (_) {}
        if (champ.value) $('#panier').classList.remove('is-manquant');
        if (menu) panier();
      });
    }

    initHaut();

    // la selection survit a un rechargement de page pendant le repas
    try {
      const gard = JSON.parse(sessionStorage.getItem('kse-choix') || '[]');
      if (Array.isArray(gard)) gard.forEach(x => choisis.add(x));
    } catch (_) {}

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
        // on ne garde que des plats qui existent encore
        const ids = new Set(menu.plats.map(p => p.image));
        [...choisis].forEach(x => { if (!ids.has(x)) choisis.delete(x); });
        tout();
      });
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
