# ⏱️ Semi-Marathon de Cancale Saint-Malo · Statistiques

Tableau de bord interactif des résultats chronométriques du semi-marathon de Cancale Saint-Malo, réalisé avec [Streamlit](https://streamlit.io).

> [Lien vers le dashboard](https://statistiques-semi-cancale-saint-malo.streamlit.app/)

## Fonctionnalités

L'application comporte deux onglets : **Statistiques** (vue générale) et **Suivi individuel** (évolution individuelle).

### 📊 Statistiques

- **Sélecteur d'édition** : navigation entre les éditions 2022 à 2026, à droite des onglets.
- **Indicateurs clés** : nombre de participants, d'hommes et de femmes, avec le temps moyen de chacun.
- **Podiums** hommes et femmes, avec gestion des ex æquo.
- **Filtre par catégorie** (Scratch, CA, JU, ES, SE, M0 à M9) appliqué aux podiums, aux graphiques de distribution et à l'évolution de la densité.
- **Distribution des temps officiels**, au choix :
  - *Courbe* : densité de coureurs par sexe, sur les temps pistolet, avec un axe gradué toutes les 10 minutes ;
  - *Tranches* : nombre de coureurs par tranche de performance de 10 minutes (de « < 1h10 » à « ≥ 2h30 »).
- **Répartition hommes / femmes** sous forme d'anneau.
- **Évolution entre les éditions**, au choix :
  - *Nombre* : nombre de coureurs par édition, hommes et femmes ;
  - *Densité* : part des arrivants par tranche de 10 minutes, année après année (barres empilées à 100 %).

### 🏃 Suivi individuel

- **Recherche d'un coureur** par nom ou prénom, dans n'importe quel ordre, sans tenir compte des accents ni des majuscules. En cas d'homonymes, une liste permet de choisir le bon coureur.
- **Indicateurs personnels** : nombre d'éditions courues, meilleur temps (avec son année) et nombre de médailles (or, argent, bronze) obtenues sur les podiums au scratch.
- **Évolution des performances** : graphique du temps de chaque édition, avec le meilleur temps mis en évidence.
- **Détail par édition** : temps, place au scratch, place chez les hommes ou les femmes, catégorie et médaille éventuelle.
- **Carte récap en PDF** : chaque coureur peut télécharger une carte (format A5) avec son nom, le logo de la course, ses chiffres clés et l'évolution de ses temps.

Les couleurs suivent partout la même règle : **rouge pour les hommes, teal pour les femmes**.

## Structure du dépôt

```
.
├── streamlit_app.py     # application Streamlit
├── carte_pdf.py         # génération de la carte récap (PDF, reportlab)
├── assets/              # images utiles (fond et logo)
├── data/                # résultats chronométriques (une ligne par coureur)
├── pyproject.toml       # dépendances (uv)
└── README.md
```

### Format des données

`data/resultats.csv` contient une ligne par coureur, avec les colonnes :

| Colonne   | Description                                                        |
|-----------|--------------------------------------------------------------------|
| `Annee`   | Édition de la course (2022 à 2026)                                 |
| `Nom`     | Nom puis prénom du coureur (ex. `BLONDEL Marin`)                   |
| `Club`    | Club ou association (peut être vide)                               |
| `Sx`      | Sexe : `Homme`, `Femme` ou `X`                                     |
| `Cat`     | Catégorie (`SE`, `M0`…)                                            |
| `Temps_s` | Temps pistolet en secondes ; vide pour les abandons (DNF)          |

Les abandons sont comptés parmi les participants mais exclus des moyennes, des courbes, des tranches et des podiums.

## Crédits

- Résultats chronométriques : [résultats du semi-marathon de Cancale Saint-Malo](https://semicancalestmalo.fr/src/pages/resultats.html)
- Construit avec [Streamlit](https://streamlit.io), [pandas](https://pandas.pydata.org), [Plotly](https://plotly.com/python/) et [ReportLab](https://docs.reportlab.com/) pour la carte PDF.