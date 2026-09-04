# Kedai Sarwo Echo — site vitrine

Site statique du restaurant de fruits de mer **Kedai Sarwo Echo**, sur la plage de
Pulang Sawal, Tepus, Gunungkidul, Yogyakarta.

Aucun outil payant, aucune dépendance à installer, aucune étape de compilation :
ce sont des fichiers HTML, CSS, JS et images, servis tels quels.

---

## Modifier le contenu sans toucher au code

Deux fichiers, et rien d'autre.

### `data/menu.json` — les plats et les prix

| Champ | À quoi ça sert |
|---|---|
| `prix` | entier en Rupiah, sans point ni espace : `85000` |
| `unite` | `porsi`, `ons`, `pcs` ou `ekor` |
| `prix_provisoire` | `true` tant que le prix n'est pas confirmé |
| `populaire` | `true` = le plat apparaît dans « Pilihan Kami » sur l'accueil |
| `categorie` | doit exister dans la liste `categories` du même fichier |
| `nom_id` / `nom_en` | nom du plat, indonésien et anglais |
| `desc_id` / `desc_en` | description, indonésien et anglais |

**Les prix ne sont pas affichés pour l'instant** : la description prend leur place.
Pour les rallumer partout d'un coup, dans `restaurant` :

```json
"afficher_les_prix": true
```

### `data/site.json` — le reste du site

Horaires, adresse, coordonnées de la carte, réseaux sociaux, citations de clients,
galerie photos, vidéo YouTube. Chaque champ est commenté en tête du fichier.

Deux interrupteurs à connaître :

- `horaires_confirmes` : tant qu'il vaut `false`, le site affiche « à confirmer »
  sous les horaires, et ne les publie **pas** dans les données Google.
- `coordonnees_a_verifier` : idem pour le point sur la carte.

Après modification : enregistrer, recharger la page. C'est tout.

---

## Ajouter les photos du lieu

1. Déposer les fichiers dans `assets/img/lieu/`.
2. Les déclarer dans `data/site.json`, section `galerie` :

```json
"galerie": [
  { "fichier": "terrasse.jpg", "alt_id": "Teras menghadap laut", "alt_en": "Terrace facing the sea" }
]
```

Tant que la liste est vide, **la section Galerie ne s'affiche pas du tout** — le site
ne montre jamais un emplacement vide.

> ⚠️ N'utiliser que **vos propres photos**. Sur Google Maps, les photos appartiennent
> à l'auteur de l'avis qui les a postées, pas au restaurant. Les republier expose à une
> réclamation. L'onglet « photos du propriétaire » et la page Facebook du restaurant
> sont les bonnes sources.

---

## Voir le site en local

```bash
python -m http.server 8899
```

puis ouvrir <http://127.0.0.1:8899>.

Un simple double-clic sur `index.html` **ne suffit pas** : le navigateur bloque la
lecture des fichiers de données en `file://`.

---

## Mettre en ligne sur GitHub Pages

Le dépôt doit être **public** : GitHub Pages ne publie pas depuis un dépôt privé sur
un compte gratuit.

```bash
git push -u origin main
```

Puis dans **Settings → Pages** : source « Deploy from a branch », branche `main`,
dossier `/ (root)`. Le fichier `.nojekyll` est déjà là, il évite que GitHub ignore
certains dossiers.

### Nom de domaine

1. Créer un fichier `CNAME` à la racine contenant le domaine, une seule ligne.
2. Chez le registrar, pointer le domaine vers GitHub :
   - apex (`exemple.com`) → enregistrements `A` vers `185.199.108.153`,
     `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` → enregistrement `CNAME` vers `kedaisarwoechocom.github.io`
3. Dans Settings → Pages, cocher **Enforce HTTPS** une fois le certificat émis.

Après le branchement du domaine, remplacer l'URL dans `sitemap.xml`, `robots.txt`
et la balise `<link rel="canonical">` de `index.html`.

---

## Ce qui a été mesuré, pas estimé

- **Profil mobile 4G lente** (1,6 Mbit/s, 150 ms de latence, processeur 4× plus lent,
  cache vide) : premier affichage ~1,5 s, plus gros élément affiché ~1,6 s.
- **Aucun débordement horizontal** et **toutes les cibles tactiles ≥ 44 px** en
  360, 390, 768, 1024, 1440 et 1920 px.
- **Contrastes WCAG AA** vérifiés sur chaque paire texte / fond utilisée.
- `prefers-reduced-motion` : les 130 Ko de bibliothèques d'animation ne sont
  **pas téléchargés** si le visiteur a demandé à réduire les animations, ou si son
  navigateur signale une connexion économe.

## Structure

```
index.html              la page
assets/css/             tokens.css (couleurs, tailles) puis main.css et sections.css
assets/js/app.js        langue, navigation, roue du menu, sections
assets/js/motion.js     animations (chargé seulement si utile)
assets/js/vendor/       GSAP, ScrollTrigger, Lenis — hébergés avec le site
assets/img/             illustrations, calques du hero, logos, favicons
assets/fonts/           Baloo 2, Lato, Sriracha (licence OFL, sous-ensemble latin)
data/                   menu.json et site.json — les deux seuls fichiers à éditer
tools/                  scripts de préparation et de vérification (hors site)
```

Le dossier `tools/` n'est pas servi aux visiteurs : il sert à préparer les images et à
vérifier le rendu. On peut le supprimer sans rien casser.
