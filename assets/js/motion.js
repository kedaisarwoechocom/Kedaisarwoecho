/* ============================================================
   Kedai Sarwo Echo — animations
   Lenis pour le defilement, GSAP + ScrollTrigger pour le reste.

   Le site doit respirer : la mer bouge, le tampon tourne, le homard flotte.
   Le mouvement de fond est lent et continu ; les entrees sont franches mais
   courtes. Aucun rebond, aucune propriete de mise en page animee.

   Tout part d'un etat VISIBLE : si ce fichier ne se charge pas, la page reste
   parfaitement lisible. Il n'est meme pas telecharge si le visiteur a demande
   a reduire les animations, ou si son navigateur signale une connexion econome.
   ============================================================ */
(() => {
  'use strict';
  if (!window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  const OUT  = 'power3.out';
  const SOFT = 'power2.inOut';

  /* ═══════════ defilement fluide ═══════════ */
  if (window.Lenis) {
    const lenis = new Lenis({
      duration: 1.1,
      easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      smoothTouch: false,   // le defilement natif du telephone est deja bon
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);

    document.addEventListener('click', e => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const cible = document.querySelector(id);
      if (!cible) return;
      e.preventDefault();
      lenis.scrollTo(cible, { offset: -74 });
    });
  }

  /* ═══════════ decoupe du titre en mots ═══════════
     Chaque mot monte derriere un masque. On ne touche qu'aux noeuds texte :
     le <em> du script garde sa couleur et sa fonte.                        */
  function decouper(racine) {
    const mots = [];
    $$(':scope > *', racine).forEach(bloc => {
      const texte = bloc.textContent;
      bloc.textContent = '';
      texte.split(/(\s+)/).forEach(part => {
        if (!part.trim()) { bloc.appendChild(document.createTextNode(part)); return; }
        const masque = document.createElement('span');
        masque.className = 'mot';
        const interieur = document.createElement('span');
        interieur.className = 'mot__i';
        interieur.textContent = part;
        masque.appendChild(interieur);
        bloc.appendChild(masque);
        mots.push(interieur);
      });
    });
    return mots;
  }

  /* ═══════════ entree, au chargement ═══════════ */
  const intro = gsap.timeline({ defaults: { ease: OUT } });

  /* .nav__end entre d'un seul bloc : anime element par element, le bouton
     WhatsApp et le burger se decalaient l'un par rapport a l'autre, et un
     transform residuel laissait le bouton 18 px trop haut si l'animation
     etait interrompue. clearProps rend la main au CSS une fois fini. */
  intro.from('.nav__logo, .langsw, .nav__links a, .nav__end',
    { y: -18, autoAlpha: 0, duration: .5, stagger: .045,
      clearProps: 'transform,opacity,visibility' });

  const titre = $('.hero__title');
  if (titre) {
    const mots = decouper(titre);
    intro.from(mots, { yPercent: 118, duration: .85, stagger: .045, ease: 'power4.out' }, .1);
  }

  const comp = $('.comp__box');
  if (comp) {
    intro.from('.comp__l--plate', { y: 56, scale: .94, autoAlpha: 0, duration: 1.15 }, 0);
    intro.from('.comp__l--stamp', { autoAlpha: 0, rotate: -26, scale: .8, duration: 1.2 }, .3);
    intro.from('.comp__l--lemon-top, .comp__l--lemon-right, .comp__l--lemon-left, .comp__l--shell, .comp__l--splash',
      { autoAlpha: 0, scale: .72, duration: .8, stagger: .08, ease: 'back.out(1.5)' }, .45);
  }

  intro.from(['.hero__lede', '.hero .btn--wa'], { y: 26, autoAlpha: 0, duration: .6, stagger: .1 }, .5)
       .from('.pick__head', { y: 20, autoAlpha: 0, duration: .55 }, .7)
       .from('.pick__rule', { scaleX: 0, transformOrigin: 'left center', duration: .8 }, .78)
       .from('.pick__item', { x: -26, autoAlpha: 0, duration: .55, stagger: .1 }, .8);

  /* ═══════════ mouvement de fond, continu ═══════════
     Ce qui empeche la page d'avoir l'air figee quand on ne fait rien.       */
  const flotte = (sel, dy, dur, rot = 0) => {
    const el = $(sel); if (!el) return;
    gsap.to(el, { y: `+=${dy}`, rotation: rot, duration: dur, ease: SOFT,
                  yoyo: true, repeat: -1, delay: Math.random() * 1.2 });
  };
  flotte('.comp__l--lemon-top',   -13, 4.2,  4);
  flotte('.comp__l--lemon-right',  15, 5.1, -5);
  flotte('.comp__l--lemon-left',  -16, 4.6,  5);
  flotte('.comp__l--shell',        12, 5.6, -3);
  flotte('.comp__l--splash',      -10, 3.8,  7);

  // le tampon tourne tres lentement, comme une roue de gouvernail
  const tampon = $('.comp__l--stamp');
  if (tampon) gsap.to(tampon, { rotation: 360, duration: 190, ease: 'none', repeat: -1 });

  // l'assiette respire
  const plat = $('.comp__l--plate');
  if (plat) gsap.to(plat, { scale: 1.014, duration: 6.5, ease: SOFT, yoyo: true, repeat: -1 });

  /* ═══════════ parallaxe de la compo ═══════════ */
  if (comp && $('.hero')) {
    [['.comp__l--plate', -46], ['.comp__l--stamp', -132],
     ['.comp__l--lemon-top', -104], ['.comp__l--lemon-right', -78],
     ['.comp__l--lemon-left', -116], ['.comp__l--shell', -66], ['.comp__l--splash', -124],
    ].forEach(([sel, y]) => {
      const el = $(sel); if (!el) return;
      gsap.to(el, { yPercent: y / 6, ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .7 } });
    });
  }

  /* ═══════════ titres de section : balayage par masque ═══════════ */
  $$('.why__title, .menu__title, .story__title, .revw__title, .find__title').forEach(t => {
    gsap.from(t, {
      clipPath: 'inset(0 100% 0 0)', y: 14, duration: .95, ease: 'power4.out',
      scrollTrigger: { trigger: t, start: 'top 88%', once: true },
    });
  });

  /* ═══════════ entrees au defilement ═══════════ */
  const monte = (cible, o = {}) => {
    const els = typeof cible === 'string' ? $$(cible) : cible;
    if (!els.length) return;
    gsap.from(els, {
      y: o.y ?? 34, autoAlpha: 0, rotate: o.rotate ?? 0, scale: o.scale ?? 1,
      duration: o.duration ?? .7, ease: OUT, stagger: o.stagger ?? .1,
      scrollTrigger: { trigger: o.trigger || els[0], start: o.start || 'top 87%', once: true },
    });
  };

  monte('.wcard', { trigger: '.why__grid', y: 46, rotate: -2.5, scale: .95, stagger: .12 });
  monte('.why__cta', { y: 22 });
  monte('.menu__sub', { trigger: '.menu__head', y: 16 });
  monte('.chip', { trigger: '.chips', y: 18, stagger: .05, duration: .5 });

  /* la roue arrive en tournant : c'est la piece maitresse, elle a droit a une entree */
  const roue = $('.wheel');
  if (roue) {
    gsap.from(roue, {
      autoAlpha: 0, scale: .82, rotate: -22, duration: 1.15, ease: 'power3.out',
      scrollTrigger: { trigger: '.menu__stage', start: 'top 84%', once: true },
    });
    gsap.from('.wheel__hub', {
      autoAlpha: 0, scale: .6, duration: .9, ease: 'back.out(1.4)', delay: .35,
      scrollTrigger: { trigger: '.menu__stage', start: 'top 84%', once: true },
    });
    monte('.dish > *', { trigger: '.menu__stage', y: 12, stagger: .05, start: 'top 78%' });
  }

  monte('.story__text p', { trigger: '.story__inner', y: 28, stagger: .12 });
  monte('.marks div', { trigger: '.marks', y: 22, stagger: .1 });
  monte('.revw__card', { y: 30, scale: .94 });
  monte('.finfo, .find__map', { trigger: '.find__grid', y: 30, stagger: .12 });
  monte('.foot__inner > *', { trigger: '.foot', y: 22, stagger: .1 });

  /* la bande de la galerie arrive en vague, un cadre apres l'autre */
  const vague = $$('.gal__wave li');
  if (vague.length) {
    gsap.from(vague, {
      y: 60, autoAlpha: 0, rotate: 5, scale: .88,
      duration: .8, ease: 'back.out(1.2)', stagger: .07,
      scrollTrigger: { trigger: '.gal__wave', start: 'top 90%', once: true },
    });
  }

  /* ═══════════ la note monte a la lecture ═══════════ */
  const note = $('#rvNote'), nb = $('#rvNb');
  if (note) {
    const cible = parseFloat(note.textContent.replace(',', '.')) || 0;
    const dec = String(note.textContent).includes(',') ? ',' : '.';
    const o = { v: 0 };
    gsap.to(o, {
      v: cible, duration: 1.5, ease: 'power2.out',
      onUpdate: () => { note.textContent = o.v.toFixed(1).replace('.', dec); },
      scrollTrigger: { trigger: '.revw__card', start: 'top 85%', once: true },
    });
  }
  if (nb) {
    const cible = parseInt(nb.textContent, 10) || 0;
    const o = { v: 0 };
    gsap.to(o, {
      v: cible, duration: 1.4, ease: 'power2.out',
      onUpdate: () => { nb.textContent = Math.round(o.v); },
      scrollTrigger: { trigger: '.revw__card', start: 'top 85%', once: true },
    });
  }
  // les etoiles s'allument une par une
  gsap.from('.revw__stars > *', {
    scale: 0, autoAlpha: 0, duration: .5, ease: 'back.out(2)', stagger: .09,
    scrollTrigger: { trigger: '.revw__card', start: 'top 85%', once: true },
  });

  /* ═══════════ trace progressif des icones ═══════════ */
  $$('.wcard__ico svg').forEach((svg, i) => {
    const traits = $$('path, circle', svg);
    traits.forEach(p => {
      const len = typeof p.getTotalLength === 'function' ? p.getTotalLength() : 0;
      if (len) gsap.set(p, { strokeDasharray: len, strokeDashoffset: len });
    });
    gsap.to(traits, {
      strokeDashoffset: 0, duration: 1.3, ease: 'power1.inOut', stagger: .05, delay: i * .1,
      scrollTrigger: { trigger: svg.closest('.wcard'), start: 'top 84%', once: true },
    });
  });

  /* ═══════════ decors de fond, parallaxe et derive ═══════════ */
  [['.why__deco', 70], ['.story__deco', 58]].forEach(([sel, y]) => {
    const el = $(sel); if (!el) return;
    gsap.to(el, { y, ease: 'none',
      scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: .8 } });
    gsap.to(el, { xPercent: 1.4, duration: 9, ease: SOFT, yoyo: true, repeat: -1 });
  });

  /* ═══════════ barre de navigation ═══════════ */
  const nav = $('.nav');
  if (nav) {
    const maj = y => nav.classList.toggle('is-stuck', y > 60);
    ScrollTrigger.create({ start: 'top -60', onUpdate: s => maj(s.scroll()), onRefresh: s => maj(s.scroll()) });
  }

  /* le contenu injecte apres coup change la hauteur de page */
  addEventListener('load', () => ScrollTrigger.refresh());
  setTimeout(() => ScrollTrigger.refresh(), 1000);
})();
