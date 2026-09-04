/* ============================================================
   Kedai Sarwo Echo — animations
   Lenis pour le defilement, GSAP + ScrollTrigger pour le reste.

   Parti pris : le mouvement sert le contenu, il ne le remplace pas.
   Durees courtes (0,4 a 0,7 s), distances faibles (16 a 28 px), une seule
   sortie d'ease, aucun rebond. Tout part d'un etat VISIBLE : si ce fichier
   ne se charge pas, la page reste parfaitement lisible.

   Ce fichier n'est meme pas telecharge si le visiteur a demande a reduire
   les animations, ou si son navigateur signale une connexion econome.
   ============================================================ */
(() => {
  'use strict';
  if (!window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  const EASE = 'power2.out';
  const DUR  = 0.55;

  /* ---------- defilement fluide ---------- */
  let lenis = null;
  if (window.Lenis) {
    lenis = new Lenis({
      duration: 1.05,
      easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      // sur telephone on laisse le defilement natif : il est deja fluide,
      // et le detourner casse les gestes du systeme.
      smoothTouch: false,
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);

    // les ancres du menu passent par Lenis pour garder le meme glissement
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const cible = document.querySelector(id);
      if (!cible) return;
      e.preventDefault();
      lenis.scrollTo(cible, { offset: -70 });
    });
  }

  /* ---------- entree du hero, une seule fois au chargement ---------- */
  const intro = gsap.timeline({ defaults: { ease: EASE, duration: DUR } });

  intro.from('.nav__logo, .nav__links a, .nav__end > *',
    { y: -14, autoAlpha: 0, duration: 0.45, stagger: 0.04 });

  const comp = $('.comp__box');
  if (comp) {
    intro.from('.comp__l--plate', { y: 34, scale: 0.985, autoAlpha: 0, duration: 0.85 }, 0.05);
    intro.from('.comp__l--stamp', { autoAlpha: 0, rotate: -8, duration: 0.9 }, 0.25);
    intro.from('.comp__l--lemon-top, .comp__l--lemon-right, .comp__l--lemon-left, .comp__l--shell, .comp__l--splash',
      { autoAlpha: 0, scale: 0.9, duration: 0.7, stagger: 0.07 }, 0.35);
  }

  intro.from(['.hero__title', '.hero__lede', '.hero .btn--wa', '.pick'],
    { y: 18, autoAlpha: 0, stagger: 0.09 }, 0.15);

  /* ---------- parallaxe de la compo : les calques prennent de la profondeur ---------- */
  if (comp && $('.hero')) {
    const prof = [
      ['.comp__l--plate', -26], ['.comp__l--stamp', -74],
      ['.comp__l--lemon-top', -56], ['.comp__l--lemon-right', -44],
      ['.comp__l--lemon-left', -62], ['.comp__l--shell', -38], ['.comp__l--splash', -68],
    ];
    prof.forEach(([sel, y]) => {
      const el = $(sel); if (!el) return;
      gsap.to(el, {
        y, ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 0.6 },
      });
    });
  }

  /* ---------- entrees au defilement ---------- */
  const monte = (cible, opts = {}) => {
    const els = typeof cible === 'string' ? $$(cible) : cible;
    if (!els.length) return;
    gsap.from(els, {
      y: opts.y ?? 22, autoAlpha: 0, duration: opts.duration ?? DUR, ease: EASE,
      stagger: opts.stagger ?? 0.08,
      scrollTrigger: { trigger: opts.trigger || els[0], start: opts.start || 'top 86%', once: true },
    });
  };

  monte('.why__title');
  monte('.wcard', { trigger: '.why__grid', y: 26, stagger: 0.1 });
  monte('.why__cta', { trigger: '.why__cta' });

  monte('.menu__title, .menu__sub, .chips', { trigger: '.menu__head', stagger: 0.07 });
  const wheel = $('.wheel');
  if (wheel) {
    gsap.from(wheel, {
      autoAlpha: 0, scale: 0.94, duration: 0.75, ease: EASE,
      scrollTrigger: { trigger: '.menu__stage', start: 'top 82%', once: true },
    });
    gsap.from('.dish > *', {
      y: 18, autoAlpha: 0, duration: DUR, ease: EASE, stagger: 0.06,
      scrollTrigger: { trigger: '.menu__stage', start: 'top 76%', once: true },
    });
  }

  monte('.story__title, .story__text p, .marks div', { trigger: '.story__inner', stagger: 0.07 });
  monte('.revw__title, .revw__card', { trigger: '.revw', stagger: 0.09 });
  monte('.find__title, .finfo, .find__map', { trigger: '.find', stagger: 0.08 });
  monte('.gal__grid li', { trigger: '.gal__grid', stagger: 0.05 });
  monte('.foot__inner > *', { trigger: '.foot', y: 16, stagger: 0.07 });

  /* ---------- trace progressif des icones de la section 2 ---------- */
  $$('.wcard__ico svg').forEach((svg, i) => {
    const paths = $$('path, circle', svg);
    paths.forEach(p => {
      const len = typeof p.getTotalLength === 'function' ? p.getTotalLength() : 0;
      if (!len) return;
      gsap.set(p, { strokeDasharray: len, strokeDashoffset: len });
    });
    gsap.to($$('path, circle', svg), {
      strokeDashoffset: 0, duration: 1.1, ease: 'power1.inOut', stagger: 0.05,
      scrollTrigger: { trigger: svg.closest('.wcard'), start: 'top 82%', once: true },
      delay: i * 0.08,
    });
  });

  /* ---------- parallaxe legere des decors line-art ---------- */
  [['.why__deco', 40], ['.story__deco', 34]].forEach(([sel, y]) => {
    const el = $(sel); if (!el) return;
    gsap.to(el, {
      y, ease: 'none',
      scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: 0.8 },
    });
  });

  /* ---------- barre de navigation condensee au defilement ---------- */
  const nav = $('.nav');
  if (nav) {
    ScrollTrigger.create({
      start: 'top -60',
      onUpdate: self => nav.classList.toggle('is-stuck', self.scroll() > 60),
      onRefresh: self => nav.classList.toggle('is-stuck', self.scroll() > 60),
    });
  }

  // le contenu injecte apres coup (roue, sections) change la hauteur de page
  addEventListener('load', () => ScrollTrigger.refresh());
  setTimeout(() => ScrollTrigger.refresh(), 900);
})();
