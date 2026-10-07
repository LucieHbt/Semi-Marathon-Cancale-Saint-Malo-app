# 🏁 Semi-Marathon de Cancale – Saint-Malo · Statistiques 2022-2026

Tableau de bord interactif des résultats chronométriques du semi-marathon de Cancale Saint-Malo, réalisé avec [Streamlit](https://streamlit.io).

[Lien vers le dashboard](https://statistiques-semi-cancale-saint-malo.streamlit.app/)

## Fonctionnalités

- **Sélecteur d'édition** : navigation entre les éditions 2022 à 2026.
- **Indicateurs clés** : nombre de participants, d'hommes et de femmes, avec le temps moyen de chacun.
- **Podiums** hommes et femmes, avec gestion des ex æquo.
- **Filtre par catégorie** (Scratch, CA, JU, ES, SE, M0 à M9) appliqué aux podiums, à la courbe de distribution et à la répartition par sexe.
- **Distribution des temps** : densité de coureurs par sexe, sur les temps pistolet.
- **Répartition hommes / femmes** sous forme d'anneau.

## Structure du dépôt

```
.
├── streamlit_app.py     # application Streamlit
├── data/
│   └── resultats.csv    # résultats de toutes les éditions (une ligne par coureur)
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

Les abandons sont comptés parmi les participants mais exclus des moyennes, des courbes et des podiums.

## Crédits

- Résultats chronométriques : [résultats du semi-marathon de Cancale Saint-Malo.](https://semicancalestmalo.fr/src/pages/resultats.html)
- Construit avec [Streamlit](https://streamlit.io), [pandas](https://pandas.pydata.org) et [Plotly](https://plotly.com/python/).
