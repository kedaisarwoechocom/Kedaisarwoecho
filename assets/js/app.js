/* ============================================================
   Kedai Sarwo Echo
   - bascule de langue ID / EN
   - tiroir de navigation (telephone)
   - liens WhatsApp avec message pre-rempli
   - "Pilihan Kami" et la roue du menu, rendus depuis data/menu.json
     (source unique des prix : l'editer suffit, aucun code a toucher)
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
      'menu.title': 'Menu Kami', 'menu.sub': 'Putar rodanya untuk menjelajah',
      'menu.dishes': 'hidangan', 'menu.order': 'Pesan hidangan ini',
      'menu.all': 'Semua',
      'menu.carte': 'Lihat kartu menu lengkap',
      'menu.fallback': 'Menu tidak dapat dimuat.',
      'menu.fallbackCta': 'Hubungi kami lewat WhatsApp',
      'gal.title': 'Suasana Kedai',
      'gal.note': 'Ilustrasi hidangan kami, sambil menunggu foto tempatnya.',
      'revw.title': 'Kata Mereka', 'revw.link': 'Baca ulasannya di Google',
      'find.title': 'Kunjungi Kami', 'find.addr': 'Alamat', 'find.hours': 'Jam buka',
      'find.contact': 'Kontak', 'find.route': 'Petunjuk arah',
      'find.mapNote': 'Titik peta masih perkiraan.',
      'foot.tag': 'Masakan Indonesia dan ikan terbaik, lebih segar dan lebih lezat.',
      'foot.story': 'Cerita', 'foot.rights': 'Semua ilustrasi hidangan adalah milik kedai.',
      'prov': 'harga sementara',
      'wa.hello': 'Halo Kedai Sarwo Echo! Saya ingin memesan'
    },
    en: {
      'skip': 'Skip to content',
      'nav.home': 'Home', 'nav.menu': 'Menu', 'nav.about': 'About', 'nav.contact': 'Contact',
      'nav.order': 'Order', 'nav.toggle': 'Open menu',
      'hero.t1': 'Let us create', 'hero.t2': 'Fresh Seafood', 'hero.t3': 'memory for you!',
      'hero.lede': 'Founded upon a passion for fresh ocean bounty, Kedai Sarwo Echo has become a one-stop shop for all kinds of delectable, delicious seafood — and then some.',
      'hero.cta': 'Order Now', 'hero.pick': 'Our Selection',
      'why.title': 'Why choose us?',
      'why.c1t': "Today's Catch",      'why.c1p': 'Guaranteed fresh from the sea to your table',
      'why.c2t': 'Authentic Taste',    'why.c2p': 'Authentic cooking you will only find here',
      'why.c3t': 'Guaranteed Quality', 'why.c3p': 'Ingredients whose quality we stand behind',
      'why.cta': 'See the Menu',
      'menu.title': 'Our Menu', 'menu.sub': 'Spin the wheel to explore',
      'menu.dishes': 'dishes', 'menu.order': 'Order this dish',
      'menu.all': 'All',
      'menu.carte': 'See the full menu card',
      'menu.fallback': 'The menu could not be loaded.',
      'menu.fallbackCta': 'Reach us on WhatsApp',
      'gal.title': 'Inside the kedai',
      'gal.note': 'Our dish illustrations, while we wait for photos of the place.',
      'revw.title': 'What people say', 'revw.link': 'Read the reviews on Google',
      'find.title': 'Find Us', 'find.addr': 'Address', 'find.hours': 'Opening hours',
      'find.contact': 'Contact', 'find.route': 'Get directions',
      'find.mapNote': 'The map pin is still approximate.',
      'foot.tag': 'For great Indonesian food and fish, fresher and tastier.',
      'foot.story': 'Our story', 'foot.rights': 'All dish illustrations belong to the kedai.',
      'prov': 'provisional price',
      'wa.hello': 'Hello Kedai Sarwo Echo! I would like to order'
    }
  };

  const STORE = 'kse-lang';
  let lang = 'id';
  let data = null;   // data/menu.json
  let site = null;   // data/site.json

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const t  = k => T[lang][k] ?? k;

  /** 85000 -> "Rp 85.000" (le point separe les milliers en indonesien) */
  const rupiah = n => 'Rp ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  const nom  = p => (lang === 'id' ? p.nom_id : p.nom_en);
  const desc = p => (lang === 'id' ? p.desc_id : p.desc_en);

  const waLink = msg => {
    const num = data?.restaurant?.whatsapp || '6281328767156';
    return `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
  };
  const waDish = p => waLink(showPrice()
    ? `${t('wa.hello')} : ${nom(p)} — ${rupiah(p.prix)}/${p.unite}`
    : `${t('wa.hello')} : ${nom(p)}`);

  const img = (slug, w) => `assets/img/dishes/${slug}-${w}`;
  const showPrice = () => data?.restaurant?.afficher_les_prix === true;
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ═══════════ langue ═══════════ */
  function applyLang(next) {
    lang = T[next] ? next : 'id';
    document.documentElement.lang = lang;
    try { localStorage.setItem(STORE, lang); } catch (_) {}

    $$('[data-i18n]').forEach(el => {
      const v = T[lang][el.dataset.i18n];
      if (v != null) el.textContent = v;
    });
    $$('[data-wa]').forEach(a => { a.href = waLink(t('wa.hello') + ' :'); });
    if (data) { renderPicks(); Wheel.retitle(); }
    if (site) Site.render();
  }

  /* ═══════════ Pilihan Kami ═══════════ */
  function renderPicks() {
    const host = $('#pickList');
    if (!host || !data) return;
    host.innerHTML = data.plats.filter(p => p.populaire).slice(0, 2).map(p => {
      const src  = img(p.image, 240);
      const unite = p.unite ? `/${p.unite}` : '';
      const prov  = p.prix_provisoire ? ` <span class="pick__prov">(${t('prov')})</span>` : '';
      const sous = showPrice()
        ? `<p class="pick__price">
             <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-heart"/></svg>
             <span>${rupiah(p.prix)}${unite}</span>${prov}
           </p>`
        : `<p class="pick__desc">${desc(p)}</p>`;
      return `<li class="pick__item">
        <a class="pick__thumb" href="${waDish(p)}" target="_blank" rel="noopener noreferrer"
           aria-label="${nom(p)}">
          <picture>
            <source type="image/avif" srcset="${src}.avif">
            <source type="image/webp" srcset="${src}.webp">
            <img src="${img(p.image, 480)}.png" alt="${nom(p)}" width="240" height="240"
                 loading="lazy" decoding="async">
          </picture>
        </a>
        <div class="pick__body">
          <p class="pick__name">${nom(p)}</p>
          ${sous}
        </div>
      </li>`;
    }).join('');
  }

  /* ═══════════ la roue du menu ═══════════ */
  const Wheel = {
    all: [], items: [], cat: 'all', index: 0, rot: 0, dragging: false, raf: 0,

    get big() { return matchMedia('(min-width: 861px)').matches; },
    get step() { return this.items.length ? 360 / this.items.length : 0; },

    init() {
      this.ring = $('#ring'); this.hub = $('#hubImg');
      this.avif = $('#hubAvif'); this.webp = $('#hubWebp');
      if (!this.ring || !data) return;
      this.all = data.plats;
      $('#menuTotal').textContent = this.all.length;
      $('#wTot').textContent = this.all.length;
      $('#chips').addEventListener('click', e => {
        const b = e.target.closest('.chip');
        if (b) this.filter(b.dataset.cat);
      });
      this.ring.addEventListener('click', e => {
        const b = e.target.closest('.sat');
        if (b && !this.moved) this.select(+b.dataset.i);
      });
      this.buildChips();
      this.filter('all');

      // molette : un cran par geste
      let lock = 0;
      this.ring.addEventListener('wheel', e => {
        if (!this.big) return;
        e.preventDefault();
        const now = Date.now();
        if (now - lock < 140) return;
        lock = now;
        this.go(Math.sign(e.deltaY) || 1);
      }, { passive: false });

      this.initDrag();

      this.ring.addEventListener('keydown', e => {
        const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (k) { e.preventDefault(); this.go(k); }
        else if (e.key === 'Home') { e.preventDefault(); this.select(0); }
        else if (e.key === 'End')  { e.preventDefault(); this.select(this.items.length - 1); }
      });

      // telephone : la selection suit le defilement de l'arc
      this.ring.addEventListener('scroll', () => {
        if (this.big || this.dragging) return;
        cancelAnimationFrame(this.raf);
        this.raf = requestAnimationFrame(() => this.fromScroll());
      }, { passive: true });

      $('#dPrev').addEventListener('click', () => this.go(-1));
      $('#dNext').addEventListener('click', () => this.go(1));

      addEventListener('resize', () => {
        clearTimeout(this._rz);
        this._rz = setTimeout(() => this.layout(false), 140);
      });
      matchMedia('(min-width: 861px)').addEventListener('change', () => this.layout(false));
    },

    buildChips() {
      const host = $('#chips');
      const cats = [{ id: 'all', nom_id: t('menu.all'), nom_en: t('menu.all') }, ...data.categories];
      host.innerHTML = cats.map(c =>
        `<li><button type="button" class="chip" data-cat="${c.id}"
           aria-pressed="${c.id === this.cat}">${lang === 'id' ? c.nom_id : c.nom_en}</button></li>`
      ).join('');
    },

    filter(cat) {
      this.cat = cat;
      $$('#chips .chip').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.cat === cat)));
      this.items = cat === 'all' ? this.all.slice() : this.all.filter(p => p.categorie === cat);
      $('#wTot').textContent = this.items.length;
      this.ring.innerHTML = this.items.map((p, i) => {
        const src = img(p.image, 240);
        return `<button type="button" class="sat" role="option" id="sat${i}" data-i="${i}"
                  aria-selected="${i === 0}" tabindex="-1" title="${nom(p)}">
          <picture>
            <source type="image/avif" srcset="${src}.avif">
            <source type="image/webp" srcset="${src}.webp">
            <img src="${img(p.image, 480)}.png" alt="${nom(p)}" width="120" height="120"
                 loading="lazy" decoding="async">
          </picture>
        </button>`;
      }).join('');
      this.index = 0;
      this.layout(false);
      this.select(0, false);
    },

    /** place les vignettes : cercle sur desktop, arc au fil du defilement sinon */
    layout(animate = true) {
      const sats = $$('.sat', this.ring);
      if (!sats.length) return;
      if (this.big) {
        const w = this.ring.clientWidth || 1;
        const R = w * 0.44;
        this.rot = -90 - this.index * this.step;
        sats.forEach((s, i) => {
          const a = (i * this.step + this.rot) * Math.PI / 180;
          s.style.transition = animate && !reduceMotion()
            ? 'transform .55s cubic-bezier(.22,1,.36,1)' : 'none';
          s.style.transform = `translate(${(Math.cos(a) * R).toFixed(1)}px, ${(Math.sin(a) * R).toFixed(1)}px)`;
        });
        this.ring.scrollLeft = 0;
      } else {
        sats.forEach(s => { s.style.transition = 'none'; });
        this.arc();
      }
    },

    /** telephone : leger galbe, les vignettes s'abaissent en s'eloignant du centre */
    arc() {
      const mid = this.ring.scrollLeft + this.ring.clientWidth / 2;
      $$('.sat', this.ring).forEach(s => {
        const d = Math.max(-1, Math.min(1,
          (s.offsetLeft + s.offsetWidth / 2 - mid) / (this.ring.clientWidth / 2 || 1)));
        s.style.transform = `translateY(${(d * d * 46).toFixed(1)}px) scale(${(1 - Math.abs(d) * .26).toFixed(3)})`;
      });
    },

    fromScroll() {
      this.arc();
      const mid = this.ring.scrollLeft + this.ring.clientWidth / 2;
      let best = 0, bd = Infinity;
      $$('.sat', this.ring).forEach((s, i) => {
        const d = Math.abs(s.offsetLeft + s.offsetWidth / 2 - mid);
        if (d < bd) { bd = d; best = i; }
      });
      if (best !== this.index) { this.index = best; this.render(); }
    },

    go(dir) {
      const n = this.items.length;
      if (!n) return;
      this.select((this.index + dir % n + n) % n);
    },

    select(i, animate = true) {
      const n = this.items.length;
      if (!n) return;
      this.index = ((i % n) + n) % n;
      if (this.big) this.layout(animate);
      else {
        const s = $$('.sat', this.ring)[this.index];
        if (s) this.ring.scrollTo({
          left: s.offsetLeft + s.offsetWidth / 2 - this.ring.clientWidth / 2,
          behavior: animate && !reduceMotion() ? 'smooth' : 'auto',
        });
      }
      this.render();
    },

    render() {
      const p = this.items[this.index];
      if (!p) return;
      $$('.sat', this.ring).forEach((s, i) => s.setAttribute('aria-selected', String(i === this.index)));
      this.ring.setAttribute('aria-activedescendant', `sat${this.index}`);

      const s4 = img(p.image, 480), s8 = img(p.image, 880);
      const sizes = '(max-width: 860px) 52vw, 290px';
      this.avif.srcset = `${s4}.avif 480w, ${s8}.avif 880w`; this.avif.sizes = sizes;
      this.webp.srcset = `${s4}.webp 480w, ${s8}.webp 880w`; this.webp.sizes = sizes;
      this.hub.src = `${s4}.png`;
      this.hub.alt = nom(p);

      const cat = data.categories.find(c => c.id === p.categorie);
      $('#dCat').textContent = cat ? (lang === 'id' ? cat.nom_id : cat.nom_en) : '';
      $('#dName').textContent = nom(p);
      $('#dPriceRow').hidden = !showPrice();
      $('#dPrice').textContent = `${rupiah(p.prix)} / ${p.unite}`;
      $('#dProv').textContent = p.prix_provisoire ? `(${t('prov')})` : '';
      $('#dDesc').textContent = desc(p);
      $('#dOrder').href = waDish(p);
      $('#wCur').textContent = this.index + 1;
    },

    retitle() {
      if (!this.items.length) return;
      const keep = this.index;
      this.buildChips(); this.filter(this.cat); this.select(keep, false);
    },

    /** desktop : faire tourner la roue au glisser */
    initDrag() {
      const ring = this.ring;
      let id = null, a0 = 0, r0 = 0;
      this.moved = false;
      const angle = e => {
        const b = ring.getBoundingClientRect();
        return Math.atan2(e.clientY - (b.top + b.height / 2),
                          e.clientX - (b.left + b.width / 2)) * 180 / Math.PI;
      };
      ring.addEventListener('pointerdown', e => {
        if (!this.big || e.button !== 0) return;
        id = e.pointerId; a0 = angle(e); r0 = this.rot; this.moved = false;
        this.dragging = true; ring.classList.add('is-drag');
        ring.setPointerCapture(id);
      });
      ring.addEventListener('pointermove', e => {
        if (id === null || e.pointerId !== id) return;
        const d = angle(e) - a0;
        if (Math.abs(d) > 2) this.moved = true;
        this.rot = r0 + d;
        const R = (ring.clientWidth || 1) * 0.44;
        $$('.sat', ring).forEach((s, i) => {
          const a = (i * this.step + this.rot) * Math.PI / 180;
          s.style.transition = 'none';
          s.style.transform = `translate(${(Math.cos(a) * R).toFixed(1)}px, ${(Math.sin(a) * R).toFixed(1)}px)`;
        });
      });
      const end = e => {
        if (id === null || (e && e.pointerId !== id)) return;
        ring.releasePointerCapture?.(id);
        id = null; this.dragging = false; ring.classList.remove('is-drag');
        if (!this.moved) return;
        const n = this.items.length;
        this.select(((Math.round((-90 - this.rot) / this.step) % n) + n) % n);
      };
      ring.addEventListener('pointerup', end);
      ring.addEventListener('pointercancel', end);
      // un clic net ne doit pas etre avale par la fin du glisser
      ring.addEventListener('pointerdown', () => { this.moved = false; }, true);
    },
  };

  /* ═══════════ sections 4 a 7 et pied de page ═══════════ */
  const Site = {
    render() {
      if (!site) return;
      this.story(); this.gallery(); this.reviews(); this.find(); this.footer();
      if (!this._ld) { this._ld = true; this.jsonLd(); }
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
      sec.hidden = g.length === 0;              // rien a montrer = pas de bande
      if (!g.length) return;

      const vraiesPhotos = g.some(x => x.source === 'photo');
      const ti = site.galerie_titre || {};
      $('#galTitle').textContent = vraiesPhotos
        ? (lang === 'id' ? ti.id_photos : ti.en_photos) || ''
        : (lang === 'id' ? ti.id : ti.en) || '';
      $('#galNote').hidden = vraiesPhotos;      // mention retiree des la 1re vraie photo

      $('#galGrid').innerHTML = g.map((x, i) => {
        const alt = esc(lang === 'id' ? (x.alt_id || '') : (x.alt_en || x.alt_id || ''));
        const illu = x.source !== 'photo';
        const media = illu
          ? `<picture>
               <source type="image/avif" srcset="${img(x.fichier, 480)}.avif">
               <source type="image/webp" srcset="${img(x.fichier, 480)}.webp">
               <img src="${img(x.fichier, 480)}.png" alt="${alt}" width="480" height="480"
                    loading="lazy" decoding="async">
             </picture>`
          : `<img src="assets/img/lieu/${esc(x.fichier)}" alt="${alt}"
                  loading="lazy" decoding="async">`;
        return `<li class="${illu ? 'is-illu' : ''}" style="--i:${i}">${media}</li>`;
      }).join('');
      // --i pose par CSSOM : la CSP interdit l'attribut style en ligne
      $$('#galGrid > li').forEach((li, i) => {
        li.removeAttribute('style');
        li.style.setProperty('--i', i);
      });
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
          // pose par CSSOM et non en attribut style : la CSP interdit le style en ligne
          const sp = document.createElement('span');
          sp.className = 'half';
          sp.style.setProperty('--cut', Math.round((1 - (note - (i - 1))) * 100) + '%');
          sp.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>' +
                         '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-star"/></svg>';
          box.appendChild(sp);
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

      const ht = l.horaires_texte || {};
      $('#fHoursLine').textContent = (lang === 'id' ? ht.id : ht.en) || '';

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
      if (l.horaires_confirmes === true && l.ouverture && l.fermeture)
        ld.openingHoursSpecification = [{
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: jours, opens: l.ouverture, closes: l.fermeture,
        }];
      const prix = data.plats.map(p => p.prix).filter(Number.isFinite);
      if (prix.length && r.afficher_les_prix === true)
        ld.priceRange = 'Rp ' + Math.min(...prix).toLocaleString('id-ID') +
                        ' - Rp ' + Math.max(...prix).toLocaleString('id-ID');

      const el = document.createElement('script');
      el.type = 'application/ld+json';
      el.textContent = JSON.stringify(ld);
      document.head.appendChild(el);
    },
  };

  /** echappe le texte venant des fichiers de donnees avant insertion en HTML */
  function esc(v) {
    return String(v ?? '').replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ═══════════ tiroir de navigation ═══════════ */
  function initNav() {
    const burger = $('#burger'), links = $('#navLinks');
    if (!burger || !links) return;
    const setOpen = open => {
      burger.setAttribute('aria-expanded', String(open));
      links.classList.toggle('is-open', open);
    };
    burger.addEventListener('click', () => setOpen(burger.getAttribute('aria-expanded') !== 'true'));
    links.addEventListener('click', e => { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
    document.addEventListener('click', e => {
      if (!e.target.closest('#navLinks') && !e.target.closest('#burger')) setOpen(false);
    });
  }

  /* ═══════════ animations, chargees seulement si elles ont du sens ═══════════ */
  function chargerAnimations() {
    // respect de prefers-reduced-motion : on ne telecharge meme pas les 130 Ko
    if (reduceMotion()) return;
    const c = navigator.connection;
    if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ''))) return;

    const fichiers = [
      'assets/js/vendor/gsap.min.js',
      'assets/js/vendor/ScrollTrigger.min.js',
      'assets/js/vendor/lenis.min.js',
      'assets/js/motion.js',
    ];
    (function suivant(i) {
      if (i >= fichiers.length) return;
      const el = document.createElement('script');
      el.src = fichiers[i];
      el.onload = () => suivant(i + 1);
      el.onerror = () => console.warn('animation non chargee :', fichiers[i]);
      document.head.appendChild(el);
    })(0);
  }

  /* ═══════════ demarrage ═══════════ */
  function init() {
    initNav();

    // Indonesien par defaut (clientele locale d'abord) ; anglais si le navigateur
    // est anglophone. ?lang=en force la langue, pour partager un lien traduit.
    let saved = null;
    try { saved = localStorage.getItem(STORE); } catch (_) {}
    const forced = new URLSearchParams(location.search).get('lang');
    const navEn = (navigator.language || '').toLowerCase().startsWith('en');
    const start = (T[forced] ? forced : null) || saved || (navEn ? 'en' : 'id');

    const charge = f => fetch(f).then(r => (r.ok ? r.json() : Promise.reject(new Error(f + ' HTTP ' + r.status))));

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
        // apres le rendu : ScrollTrigger mesure ainsi la page dans son etat final
        requestAnimationFrame(() => requestAnimationFrame(chargerAnimations));
      });
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
