/* ============================================================
   Kedai Sarwo Echo — comportements de base
   - bascule de langue ID / EN
   - tiroir de navigation (telephone)
   - liens WhatsApp avec message pre-rempli
   - "Pilihan Kami" rendu depuis data/menu.json (source unique des prix)
   ============================================================ */
(() => {
  'use strict';

  /* ---------- dictionnaire d'interface ---------- */
  const T = {
    id: {
      'skip': 'Langsung ke konten',
      'nav.home': 'Beranda', 'nav.menu': 'Menu', 'nav.about': 'Tentang', 'nav.contact': 'Kontak',
      'nav.order': 'Pesan', 'nav.toggle': 'Buka menu',
      'hero.t1': 'Kami ciptakan kenangan', 'hero.t2': 'Seafood Segar', 'hero.t3': 'untuk Anda!',
      'hero.lede': 'Berawal dari kecintaan pada hasil laut segar, Kedai Sarwo Echo kini menjadi tempat untuk segala macam hidangan seafood yang lezat — dan masih banyak lagi.',
      'hero.cta': 'Pesan Sekarang', 'hero.pick': 'Pilihan Kami',
      'why.title': 'Kenapa memilih kami?',
      'why.c1t': 'Tangkapan Hari Ini', 'why.c1p': 'Dijamin segar dari laut ke meja Anda',
      'why.c2t': 'Rasa Otentik',       'why.c2p': 'Masakan otentik yang hanya ada di sini',
      'why.c3t': 'Kualitas Terjamin',  'why.c3p': 'Bahan-bahan masakan yang terjamin kualitasnya',
      'why.cta': 'Lihat Menu',
      'prov': 'harga sementara',
      'wa.hello': 'Halo Kedai Sarwo Echo! Saya ingin memesan',
      'wa.dish': 'Halo Kedai Sarwo Echo! Saya ingin memesan'
    },
    en: {
      'skip': 'Skip to content',
      'nav.home': 'Home', 'nav.menu': 'Menu', 'nav.about': 'About', 'nav.contact': 'Contact',
      'nav.order': 'Order', 'nav.toggle': 'Open menu',
      'hero.t1': 'Let us create', 'hero.t2': 'Fresh Seafood', 'hero.t3': 'memory for you!',
      'hero.lede': 'Founded upon a passion for fresh ocean bounty, Kedai Sarwo Echo has become a one-stop shop for all kinds of delectable, delicious seafood — and then some.',
      'hero.cta': 'Order Now', 'hero.pick': 'Our Selection',
      'why.title': 'Why choose us?',
      'why.c1t': "Today's Catch",     'why.c1p': 'Guaranteed fresh from the sea to your table',
      'why.c2t': 'Authentic Taste',   'why.c2p': 'Authentic cooking you will only find here',
      'why.c3t': 'Guaranteed Quality','why.c3p': 'Ingredients whose quality we stand behind',
      'why.cta': 'See the Menu',
      'prov': 'provisional price',
      'wa.hello': 'Hello Kedai Sarwo Echo! I would like to order',
      'wa.dish': 'Hello Kedai Sarwo Echo! I would like to order'
    }
  };

  const STORE = 'kse-lang';
  let lang = 'id';
  let data = null;

  /* ---------- utilitaires ---------- */
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /** 85000 -> "Rp 85.000" (format indonesien: point comme separateur de milliers) */
  const rupiah = n => 'Rp ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');

  const waLink = (msg) => {
    const num = data?.restaurant?.whatsapp || '6281328767156';
    return `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
  };

  /* ---------- langue ---------- */
  function applyLang(next) {
    lang = T[next] ? next : 'id';
    document.documentElement.lang = lang;
    try { localStorage.setItem(STORE, lang); } catch (_) {}

    $$('[data-i18n]').forEach(el => {
      const v = T[lang][el.dataset.i18n];
      if (v != null) el.textContent = v;
    });
    $$('.lang__btn').forEach(b => {
      const on = b.dataset.lang === lang;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', String(on));
    });
    $$('[data-wa]').forEach(a => { a.href = waLink(T[lang]['wa.hello'] + ' :'); });
    if (data) renderPicks();
  }

  /* ---------- Pilihan Kami ---------- */
  function renderPicks() {
    const host = $('#pickList');
    if (!host || !data) return;
    const picks = data.plats.filter(p => p.populaire).slice(0, 2);
    host.innerHTML = picks.map(p => {
      const nom = lang === 'id' ? p.nom_id : p.nom_en;
      const unite = p.unite ? `/${p.unite}` : '';
      const prov = p.prix_provisoire
        ? ` <span class="pick__prov">(${T[lang]['prov']})</span>` : '';
      const img = `assets/img/dishes/${p.image}`;
      return `<li class="pick__item">
        <a class="pick__thumb" href="${waLink(`${T[lang]['wa.dish']} : ${nom}`)}"
           target="_blank" rel="noopener noreferrer" aria-label="${nom}">
          <picture>
            <source type="image/avif" srcset="${img}-240.avif">
            <source type="image/webp" srcset="${img}-240.webp">
            <img src="${img}-480.png" alt="${nom}" width="240" height="240" loading="lazy" decoding="async">
          </picture>
        </a>
        <div class="pick__body">
          <p class="pick__name">${nom}</p>
          <p class="pick__price">
            <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-heart"/></svg>
            <span>${rupiah(p.prix)}${unite}</span>${prov}
          </p>
        </div>
      </li>`;
    }).join('');
  }

  /* ---------- tiroir de navigation ---------- */
  function initNav() {
    const burger = $('#burger'), links = $('#navLinks');
    if (!burger || !links) return;
    const setOpen = open => {
      burger.setAttribute('aria-expanded', String(open));
      links.classList.toggle('is-open', open);
    };
    burger.addEventListener('click', () =>
      setOpen(burger.getAttribute('aria-expanded') !== 'true'));
    links.addEventListener('click', e => { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
    document.addEventListener('click', e => {
      if (!e.target.closest('#navLinks') && !e.target.closest('#burger')) setOpen(false);
    });
  }

  /* ---------- demarrage ---------- */
  function init() {
    initNav();
    $$('.lang__btn').forEach(b => b.addEventListener('click', () => applyLang(b.dataset.lang)));

    // Indonesien par defaut (clientele locale d'abord) ; anglais si le
    // navigateur est anglophone. ?lang=en dans l'URL force la langue, ce qui
    // permet de partager un lien deja traduit. Le choix du visiteur prime ensuite.
    let saved = null;
    try { saved = localStorage.getItem(STORE); } catch (_) {}
    const forced = new URLSearchParams(location.search).get('lang');
    const navEn = (navigator.language || '').toLowerCase().startsWith('en');
    const start = (T[forced] ? forced : null) || saved || (navEn ? 'en' : 'id');

    fetch('data/menu.json')
      .then(r => r.ok ? r.json() : Promise.reject(new Error(r.status)))
      .then(j => { data = j; applyLang(start); })
      .catch(err => { console.warn('menu.json indisponible :', err.message); applyLang(start); });
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
