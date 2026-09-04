# -*- coding: utf-8 -*-
"""Genere le rapport de livraison (7 phases) avec captures embarquees."""
import base64
from pathlib import Path

SHOTS = Path(r"e:\c\projet\Kedaisarwoecho\build\shots")
OUT = Path(r"C:\Users\saido\AppData\Local\Temp\claude\e--c-projet-Kedaisarwoecho\6489d88b-c21d-4fa7-83bc-9a1b9f749db7\scratchpad\rendu-kedai-sarwo-echo.html")
OUT.parent.mkdir(parents=True, exist_ok=True)

def uri(stem):
    return "data:image/webp;base64," + base64.b64encode((SHOTS / f"{stem}_web.webp").read_bytes()).decode()

IMG = {k: uri(k) for k in ("360", "390", "768", "1024", "1440", "1920")}

def frame(stem, w, titre, notes, h=580):
    lis = "".join(f"<li>{n}</li>" for n in notes)
    return f"""<figure class="shot">
  <figcaption class="shot__cap"><span class="shot__w">{w}<i>px</i></span><span class="shot__t">{titre}</span></figcaption>
  <div class="shot__screen" style="--h:{h}px"><img src="{IMG[stem]}" alt="Rendu du site a {w} pixels de large"></div>
  <ul class="shot__notes">{lis}</ul>
</figure>"""

HTML = f"""<title>Rendu Kedai Sarwo Echo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Lato:ital,wght@0,400;0,700;1,400&family=Sriracha&display=swap">
<style>
:root{{
  --cream:#F4EDE7; --rose:#E3DAD4; --taupe:#CEBCB2;
  --sage:#5A7168; --brick:#AC1A19; --brown:#6E5247;
  --ground:#FBF7F3; --surface:#FFFFFF; --sunken:#F2EBE4;
  --line:#E2D6CC; --line-soft:#EFE6DE;
  --ink:#2A1E18; --ink-2:#6E5247; --ink-3:#9C8879;
  --ok:#3F6B52; --wait:#A8752A;
  --shadow:0 1px 2px rgba(70,45,30,.05),0 14px 30px -18px rgba(70,45,30,.32);
  --f-d:"Baloo 2",system-ui,sans-serif; --f-b:"Lato","Segoe UI",system-ui,sans-serif;
  --f-s:"Sriracha",cursive; --f-m:ui-monospace,"Cascadia Mono","SF Mono",Menlo,monospace;
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --cream:#241D19; --rose:#332822; --taupe:#4C3D34;
  --sage:#93B3A5; --brick:#E8756C; --brown:#C3AA9B;
  --ground:#16110F; --surface:#1F1916; --sunken:#191310;
  --line:#3A2E27; --line-soft:#2A211C;
  --ink:#F3E9E2; --ink-2:#C3AA9B; --ink-3:#8B7566;
  --ok:#7FBE97; --wait:#D6A15A;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 30px -18px rgba(0,0,0,.8);
}}}}
:root[data-theme="dark"]{{
  --cream:#241D19; --rose:#332822; --taupe:#4C3D34;
  --sage:#93B3A5; --brick:#E8756C; --brown:#C3AA9B;
  --ground:#16110F; --surface:#1F1916; --sunken:#191310;
  --line:#3A2E27; --line-soft:#2A211C;
  --ink:#F3E9E2; --ink-2:#C3AA9B; --ink-3:#8B7566;
  --ok:#7FBE97; --wait:#D6A15A;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 30px -18px rgba(0,0,0,.8);
}}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:var(--f-b);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}}
img{{display:block;max-width:100%}}
.wrap{{max-width:1120px;margin:0 auto;padding:clamp(28px,4vw,56px) clamp(16px,3.4vw,40px) 88px}}
h1,h2,h3{{margin:0;font-family:var(--f-d);font-weight:800;line-height:1.1;text-wrap:balance}}
h1{{font-size:clamp(2rem,4.6vw,3.1rem);color:var(--sage);letter-spacing:-.015em}}
h1 em{{font-family:var(--f-s);font-style:normal;font-weight:400;color:var(--brick);font-size:.9em}}
h2{{font-size:clamp(1.35rem,2.4vw,1.72rem);color:var(--sage)}}
h3{{font-size:1.02rem;font-weight:700;color:var(--ink)}}
p{{margin:0}}
a{{color:var(--brick);text-underline-offset:2px}}
a:focus-visible{{outline:3px solid var(--brick);outline-offset:3px;border-radius:4px}}
.eyebrow{{font-size:.7rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3)}}

header{{display:flex;flex-direction:column;gap:14px;padding-bottom:26px;border-bottom:2px solid var(--line)}}
.lede{{font-size:1.06rem;color:var(--ink-2);max-width:64ch}}
section{{margin-top:clamp(40px,5.2vw,64px);display:flex;flex-direction:column;gap:20px}}
.sec-head{{display:flex;align-items:baseline;gap:13px;flex-wrap:wrap}}
.sec-head .n{{font-family:var(--f-d);font-weight:800;font-size:.78rem;color:var(--brick);
  background:var(--rose);border-radius:99px;padding:3px 12px;letter-spacing:.04em;flex:none}}

.figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.fig{{background:var(--surface);padding:15px 17px;display:flex;flex-direction:column;gap:3px}}
.fig b{{font-family:var(--f-d);font-weight:800;font-size:1.5rem;color:var(--sage);
  line-height:1.05;font-variant-numeric:tabular-nums}}
.fig b small{{font-size:.62em}}
.fig span{{font-size:.79rem;color:var(--ink-3);line-height:1.35}}

.steps{{display:flex;flex-direction:column;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.step{{background:var(--surface);padding:13px 17px;display:grid;
  grid-template-columns:auto auto minmax(0,1fr);gap:14px;align-items:baseline}}
.step .k{{font-family:var(--f-d);font-weight:800;color:var(--taupe);font-variant-numeric:tabular-nums}}
.step .ok{{color:var(--ok);font-weight:700;font-size:.8rem}}
.step b{{font-family:var(--f-d);font-weight:700;color:var(--ink)}}
.step span.d{{color:var(--ink-2);font-size:.92rem}}

.shots{{display:grid;gap:clamp(18px,2.4vw,28px)}}
.shots--duo{{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}}
.shot{{margin:0;display:flex;flex-direction:column;gap:11px}}
.shot__cap{{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap}}
.shot__w{{font-family:var(--f-d);font-weight:800;font-size:1.12rem;color:var(--ink);
  font-variant-numeric:tabular-nums}}
.shot__w i{{font-style:normal;font-size:.72rem;font-weight:700;color:var(--ink-3);
  margin-left:2px;letter-spacing:.04em}}
.shot__t{{font-size:.87rem;color:var(--ink-2)}}
.shot__screen{{height:var(--h);overflow-y:auto;overflow-x:hidden;
  background:var(--sunken);border:1px solid var(--line);border-radius:12px;
  box-shadow:var(--shadow);scrollbar-width:thin}}
.shot__screen img{{width:100%}}
.shot__notes{{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:4px;
  font-size:.85rem;color:var(--ink-2)}}
.shot__notes li::marker{{color:var(--taupe)}}
.hint{{font-size:.78rem;color:var(--ink-3);font-style:italic}}

.tbl{{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--surface)}}
.tbl__row{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) minmax(0,1fr) auto;
  gap:12px;padding:10px 16px;border-top:1px solid var(--line-soft);font-size:.9rem;align-items:center}}
.tbl__row:first-child{{border-top:none;background:var(--sunken)}}
.tbl__row:first-child span{{font-size:.71rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3)}}
.num{{font-family:var(--f-m);font-size:.84rem;font-variant-numeric:tabular-nums}}
.pass{{color:var(--ok);font-weight:700}} .warn{{color:var(--wait);font-weight:700}}
.swatch{{display:inline-block;width:13px;height:13px;border-radius:3px;
  border:1px solid rgba(110,82,71,.25);vertical-align:-2px;margin-right:7px}}

.calls{{display:flex;flex-direction:column;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.call{{background:var(--surface);padding:15px 18px;display:grid;
  grid-template-columns:auto minmax(0,1fr);gap:14px;align-items:start}}
.call__k{{font-family:var(--f-d);font-weight:800;font-size:.76rem;letter-spacing:.06em;
  text-transform:uppercase;padding:4px 10px;border-radius:99px;white-space:nowrap;
  background:var(--cream);color:var(--brown);border:1px solid var(--line)}}
.call__k--fix{{background:var(--rose);color:var(--brick)}}
.call p{{font-size:.92rem;color:var(--ink-2)}}
.call p b{{color:var(--ink)}}
.call p+p{{margin-top:5px}}

.ask{{display:flex;flex-direction:column;gap:10px}}
.ask__i{{display:grid;grid-template-columns:auto minmax(0,1fr);gap:13px;padding:13px 16px;
  background:var(--cream);border:1px solid var(--line);border-radius:10px;font-size:.93rem}}
.ask__i b{{font-family:var(--f-d);font-weight:800;color:var(--brick);font-variant-numeric:tabular-nums}}
.ask__i span{{color:var(--ink-2)}} .ask__i span b{{font-family:var(--f-b);color:var(--ink)}}

code{{font-family:var(--f-m);font-size:.86em;background:var(--sunken);
  border:1px solid var(--line-soft);border-radius:4px;padding:1px 5px}}
footer{{margin-top:58px;padding-top:22px;border-top:2px solid var(--line);
  font-size:.85rem;color:var(--ink-3);display:flex;flex-direction:column;gap:6px}}
@media (max-width:620px){{
  .tbl__row{{grid-template-columns:1fr auto;row-gap:3px}}
  .call,.step{{grid-template-columns:1fr;gap:6px}}
}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style>

<div class="wrap">

<header>
  <p class="eyebrow">Livraison &middot; les 7 phases</p>
  <h1>Kedai Sarwo Echo<br><em>le site</em></h1>
  <p class="lede">Le site est complet : sept sections, la roue du menu, les animations, la
  securite et le referencement local. Il tient dans un dossier de fichiers statiques, sans
  aucune etape de compilation. Voici le rendu aux six largeurs, ce qui a ete mesure, et les
  quatre choses qu'il me manque encore de ta part.</p>
</header>

<section>
  <div class="sec-head"><span class="n">Etat</span><h2>Les sept phases</h2></div>
  <div class="steps">
    <div class="step"><span class="k">1</span><span class="ok">FAIT</span><div>
      <b>Preparation des images.</b> <span class="d">Nettete des 22 plats mesuree avant tout
      traitement : aucune n'etait floue. Agrandissement Upscayl, export AVIF et WebP
      multi-tailles, hero decoupe en 7 calques animables, favicons.</span></div></div>
    <div class="step"><span class="k">2</span><span class="ok">FAIT</span><div>
      <b>Design system en code.</b> <span class="d">Tokens a trois couches, echelle fluide en
      clamp(), contrastes calcules sur chaque paire, polices auto-hebergees.</span></div></div>
    <div class="step"><span class="k">3</span><span class="ok">FAIT</span><div>
      <b>Sections 1 et 2.</b> <span class="d">Desktop cale sur les mesures des maquettes,
      telephone et tablette concus a part.</span></div></div>
    <div class="step"><span class="k">4</span><span class="ok">FAIT</span><div>
      <b>La roue du menu.</b> <span class="d">Cercle de 22 plats sur ordinateur, arc balayable
      au doigt sur telephone, filtres par categorie.</span></div></div>
    <div class="step"><span class="k">5</span><span class="ok">FAIT</span><div>
      <b>Les sections manquantes.</b> <span class="d">Notre histoire, galerie, avis, nous
      trouver, pied de page. Carte OpenStreetMap sans cle ni traceur.</span></div></div>
    <div class="step"><span class="k">6</span><span class="ok">FAIT</span><div>
      <b>Animations.</b> <span class="d">Lenis et GSAP, parallaxe des 7 calques, entrees au
      defilement, trace des icones. Non telechargees si le visiteur les refuse.</span></div></div>
    <div class="step"><span class="k">7</span><span class="ok">FAIT</span><div>
      <b>Optimisation, securite, referencement.</b> <span class="d">CSP stricte, donnees
      structurees Restaurant, sitemap. Reste la mise en ligne, qui attend ton feu vert.</span></div></div>
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Mesure</span><h2>Ce qui a ete verifie, pas estime</h2></div>
  <div class="figs">
    <div class="fig"><b>1,56 <small>s</small></b><span>plus gros element affiche, en 4G lente et processeur bride</span></div>
    <div class="fig"><b>573 <small>Ko</small></b><span>page entiere, cache vide, 31 requetes</span></div>
    <div class="fig"><b>0</b><span>debordement horizontal, aux six largeurs</span></div>
    <div class="fig"><b>44 <small>px</small></b><span>cible tactile minimale, respectee partout</span></div>
    <div class="fig"><b>30</b><span>arrets au clavier couvrant toute la page, sans piege</span></div>
    <div class="fig"><b>0</b><span>couleur en dur : tout passe par les tokens</span></div>
  </div>
  <p class="hint">Profil de test : 390&times;844 en densite 2, 4G lente (1,6&nbsp;Mbit/s,
  150&nbsp;ms de latence), processeur quatre fois plus lent, cache vide. C'est volontairement
  plus dur que ce que vivra un client sur la cote de Gunungkidul.</p>
</section>

<section>
  <div class="sec-head"><span class="n">Rendu</span><h2>Telephone</h2></div>
  <p class="lede">C'est le cas principal, pas une reduction du desktop. Le homard passe au-dessus
  du titre en pleine largeur, les liens rentrent dans un tiroir, et le bouton WhatsApp reste
  visible en permanence dans la barre collante.</p>
  <p class="hint">Les cadres defilent : fais glisser a l'interieur pour voir la page entiere.</p>
  <div class="shots shots--duo">
    {frame("360","360","le plus petit ecran courant",[
      "Le libelle du bouton WhatsApp se reduit a l'icone pour tenir 44&nbsp;px de cible",
      "Les 3 cartes passent en colonne, icone au-dessus du titre",
      "L'arc du menu se balaye au doigt, avec accrochage sur le plat centre"], 620)}
    {frame("390","390","iPhone et Android courants",[
      "Texte courant a 16&nbsp;px : jamais en dessous, quelle que soit la largeur",
      "Le line-art de fond est allege : 3 motifs au lieu de 8",
      "Fiche du plat directement sous l'arc, bouton de commande en pleine largeur"], 620)}
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Rendu</span><h2>Tablette</h2></div>
  <div class="shots shots--duo">
    {frame("768","768","tablette en portrait",[
      "Le homard est calme volontairement pour ne pas avaler l'ecran",
      "Cartes en ligne : icone a gauche, titre au-dessus de son texte",
      "La roue reste en arc a cette largeur"], 580)}
    {frame("1024","1024","tablette en paysage",[
      "Bascule vers la mise en page cote a cote",
      "La roue redevient un cercle, la fiche passe a droite",
      "Nous trouver passe en deux colonnes : infos et carte"], 580)}
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Rendu</span><h2>Ordinateur</h2></div>
  <div class="shots">
    {frame("1440","1440","la largeur de reference des maquettes",[
      "Aucun cadre : le creme occupe tout l'ecran",
      "Toutes les sections partagent exactement les memes bords gauche et droit",
      "L'illustration s'arrete pile sur la gouttiere, jamais rognee par le bord"], 640)}
    {frame("1920","1920","grand ecran",[
      "L'illustration grandit avec l'ecran au lieu de rester figee",
      "Le texte suit la meme echelle jusqu'a 1760&nbsp;px, puis se stabilise",
      "Au-dela, le contenu se centre sur du creme : aucune bordure visible"], 640)}
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Audit</span><h2>Deux vrais defauts trouves, et corriges</h2></div>
  <div class="calls">
    <div class="call"><span class="call__k call__k--fix">corrige</span><div>
      <p><b>La carte capturait le clavier.</b> L'iframe OpenStreetMap prenait neuf arrets de
      tabulation d'affilee : un visiteur au clavier restait coince dedans et n'atteignait
      jamais le pied de page. La carte est sortie du parcours clavier &mdash; l'adresse en
      texte et le bouton d'itineraire portent exactement la meme information.</p></div></div>
    <div class="call"><span class="call__k call__k--fix">corrige</span><div>
      <p><b>La barre de navigation animait sa hauteur.</b> Elle transitionnait
      <code>padding</code>, une propriete de mise en page, donc un recalcul complet a chaque
      changement d'etat. Elle se condense maintenant par une mise a l'echelle du logo, calculee
      sur la carte graphique.</p></div></div>
    <div class="call"><span class="call__k">nettoye</span><div>
      <p><b>Plus une seule couleur en dur.</b> Les six dernieres valeurs <code>rgba()</code>
      qui trainaient dans les composants sont devenues des tokens. Changer une couleur se fait
      desormais a un seul endroit.</p></div></div>
    <div class="call"><span class="call__k">technique</span><div>
      <p><b>43&nbsp;Ko de PNG partaient pour rien.</b> Les decors en fond CSS n'ont pas de
      negociation de format : le navigateur tirait le PNG meme quand il savait lire l'AVIF.
      Corrige avec <code>image-set()</code>. Les icones PWA sont passees de 275 a 41&nbsp;Ko.</p></div></div>
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Design</span><h2>Contrastes verifies</h2></div>
  <div class="tbl">
    <div class="tbl__row"><span>Paire</span><span>Rapport</span><span>Norme AA</span><span>Usage</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#AC1A19"></i>Brique sur creme</span><span class="num">6,21</span><span class="pass">oui</span><span>script, accents</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#6E5247"></i>Brun sur creme</span><span class="num">6,12</span><span class="pass">oui</span><span>texte courant</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#AC1A19"></i>Brique sur rose</span><span class="num">5,23</span><span class="pass">oui</span><span>titres de cartes</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#FFFFFF"></i>Blanc sur bouton</span><span class="num">4,92</span><span class="pass">oui</span><span>libelles de boutons</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#5A7168"></i>Sauge sur creme</span><span class="num">4,53</span><span class="pass">oui, juste</span><span>titres</span></div>
    <div class="tbl__row"><span><i class="swatch" style="background:#5A7168"></i>Sauge sur taupe</span><span class="num">2,87</span><span class="warn">non</span><span>ecarte du code</span></div>
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Choix</span><h2>Ce que j'ai decide, et pourquoi</h2></div>
  <div class="calls">
    <div class="call"><span class="call__k call__k--fix">change</span><div>
      <p><b>Les prix ne sont pas affiches.</b> La description du plat prend leur place. Les
      montants provisoires restent dans <code>data/menu.json</code> : passe
      <code>afficher_les_prix</code> a <code>true</code> et ils reviennent partout d'un coup,
      y compris dans les donnees envoyees a Google.</p></div></div>
    <div class="call"><span class="call__k call__k--fix">change</span><div>
      <p><b>Le cadre beige a disparu.</b> C'etait la couleur d'artboard de ton fichier de
      design, pas un cadre voulu.</p></div></div>
    <div class="call"><span class="call__k">a savoir</span><div>
      <p><b>La galerie ne s'affiche pas du tout</b> tant qu'aucune photo n'est declaree. Le
      site ne montre jamais un emplacement vide : la section apparaitra le jour ou tu deposeras
      tes photos dans <code>assets/img/lieu/</code>.</p></div></div>
    <div class="call"><span class="call__k">a savoir</span><div>
      <p><b>Les horaires ne sont pas publies dans Google.</b> Ceux affiches sur le site sont
      marques &laquo;&nbsp;a confirmer&nbsp;&raquo; et volontairement absents des donnees
      structurees : un faux horaire dans Google Maps fait plus de mal que pas d'horaire du
      tout. Meme logique pour le point sur la carte.</p></div></div>
    <div class="call"><span class="call__k">technique</span><div>
      <p><b>Les animations ne se telechargent pas toujours.</b> Si le visiteur a demande a
      reduire les animations, ou si son navigateur signale une connexion econome, les
      130&nbsp;Ko de bibliotheques ne partent jamais. Le site reste entierement lisible sans
      elles.</p></div></div>
    <div class="call"><span class="call__k">technique</span><div>
      <p><b>Une politique de securite stricte.</b> Aucun script ni style en ligne, aucun
      domaine tiers hors la carte et la video. Aucune donnee visiteur collectee, donc aucune
      banniere cookies a poser.</p></div></div>
  </div>
</section>

<section>
  <div class="sec-head"><span class="n">Toi</span><h2>Les quatre choses qu'il me manque</h2></div>
  <div class="ask">
    <div class="ask__i"><b>1</b><span><b>Les prix reels.</b> Ils sont deja tous dans
      <code>data/menu.json</code> a titre provisoire : remplace les nombres, puis passe
      <code>afficher_les_prix</code> a <code>true</code>.</span></div>
    <div class="ask__i"><b>2</b><span><b>Les horaires d'ouverture</b> et les jours de fermeture,
      dans <code>data/site.json</code>. Passe ensuite <code>horaires_confirmes</code> a
      <code>true</code> pour qu'ils partent aussi dans Google.</span></div>
    <div class="ask__i"><b>3</b><span><b>Tes photos du lieu</b> &mdash; celles de l'onglet
      &laquo;&nbsp;photos du proprietaire&nbsp;&raquo; et celles de Facebook. Les photos des
      avis Google appartiennent a leurs auteurs, je ne peux pas les reprendre.</span></div>
    <div class="ask__i"><b>4</b><span><b>Le feu vert pour pousser</b> sur
      <code>kedaisarwoechocom/Kedaisarwoecho</code>, et le nom de domaine quand tu l'auras.
      Le depot devra etre public : GitHub Pages ne publie pas depuis un depot prive sur un
      compte gratuit.</span></div>
  </div>
</section>

<footer>
  <p>Les sept phases sont terminees et commitees en local, en huit commits. Le depot distant
  repond et il est vide : rien n'a ete pousse, comme convenu.</p>
  <p>Le mode d'emploi complet &mdash; modifier les prix, ajouter des photos, brancher le
  domaine &mdash; est dans le <code>README.md</code> a la racine du projet.</p>
</footer>

</div>
"""
OUT.write_text(HTML, encoding="utf-8")
print(f"{OUT}  —  {OUT.stat().st_size/1024/1024:.2f} Mo")
